import pickle
import pandas as pd
from flask import Flask,request, render_template,jsonify,redirect,url_for,session
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from dotenv import load_dotenv
import os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from sqlalchemy.exc import OperationalError
from sklearn.metrics import f1_score, accuracy_score, classification_report

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='supersecretkey'

db=SQLAlchemy(app)


class User(db.Model):                    
    __tablename__ = "users"
    username = db.Column(db.String(80), primary_key=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120), unique=True, nullable=False)
    # created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone=request.form.get('phone')

        if not username or not password or not email:
            return render_template("register.html", error="Username and password must not be left blank")

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Email already registered")

        if User.query.filter_by(email=email).first():
            return render_template("register.html", error="Email already registered")

        new_user = User(username=username, phone=phone, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["username"] = user.username
            return redirect(url_for("index"))   # go to prediction page
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

students_data=[]
def send_email_with_link(sender_email, sender_password, recipient_email, subject, body, link_text, link_url):
    try:
        # Create the email
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Create plain text version (fallback)
        text_part = f"{body}\n\n{link_text}: {link_url}"

        # Create HTML version with a clickable link
        html_part = f"""
        <html>
            <body>
                <p>{body}</p>
                <p><a href="{link_url}">{link_text}</a></p>
            </body>
        </html>
        """

        # Attach both plain and HTML versions
        msg.attach(MIMEText(text_part, "plain"))
        msg.attach(MIMEText(html_part, "html"))

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        print("Email sent successfully!")

        server.quit()
        return True
    except Exception as e:
        print("Error:", e)
        return False

def get_high_risk_students():
    return [
        {
            'name': s.get('Name', 'Unknown'),
            'roll_no': s.get('Roll_No', 'Unknown'),
            'risk_percentage': s.get('risk_level', 'N/A'),
            'attendance': s.get('Attendance', 'N/A'),
            'fee_status': s.get('FeeStatus', 'N/A')
        }
        for s in students_data if str(s.get('risk_level', '')).startswith('High')
    ]



@app.route('/model_info')
def model_info():
    """Route to display model performance metrics"""
    return jsonify(MODEL_METRICS)
        
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "dropout_prediction.pkl")
    
# Load the trained model (replace with actual model loading)
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    model = None
    print(f"Model loading failed: {e}")

# Store model performance metrics (these would typically be calculated once and stored)
MODEL_METRICS = {
    'f1_score_macro': 0.79,  # Replace with actual F1 score from your evaluation
    'f1_score_weighted': 0.83,  # Replace with actual weighted F1 score
    'accuracy': 0.83,  # Replace with actual accuracy
    'auc_score': 0.9255  # Replace with actual AUC score
}


FIELDS=['Marital status', 'Application mode', 'Daytime/evening attendance',
       'Previous qualification', "Mother's occupation", "Father's occupation",
       'Displaced', 'Debtor', 'Tuition fees up to date', 'Scholarship holder',
       'Age at enrollment', 'International',
       'Curricular units 1st sem (evaluations)',
       'Curricular units 1st sem (approved)',
       'Curricular units 1st sem (grade)',
       'Curricular units 2nd sem (evaluations)',
       'Curricular units 2nd sem (approved)',
       'Curricular units 2nd sem (grade)', 'Attendance']

REQUIRED_FIELDS = FIELDS + ["Roll_No", "Name"]

@app.route('/', methods=['GET', 'POST'])
def index():
    predictions = []
    error = None
    if request.method == 'POST':
        att_file = request.files.get("Attfile")
        fees_file = request.files.get("Feesfile")
        scores_file = request.files.get("Marksfile")
        if not att_file or not fees_file or not scores_file:
            return "All three files are required", 400
        else:
    
            att_filename = att_file.filename.lower()
            fees_filename = fees_file.filename.lower()
            scores_filename = scores_file.filename.lower()
            try:
                if att_filename.endswith('.xlsx') or att_filename.endswith('.xls'):
                    df1 = pd.read_excel(att_file)
                elif att_filename.endswith('.csv'):
                    df1 = pd.read_csv(att_file)
                else:
                    error = 'Unsupported file   type. Please upload a .csv or .xlsx file.'
                    df1 = None
                if fees_filename.endswith('.xlsx') or fees_filename.endswith('.xls'):
                    df2 = pd.read_excel(fees_file)
                elif fees_filename.endswith('.csv'):
                    df2 = pd.read_csv(fees_file)
                else:
                    error = 'Unsupported file   type. Please upload a .csv or .xlsx file.'
                    df2 = None
                    
                if scores_filename.endswith('.xlsx') or scores_filename.endswith('.xls'):
                    df3 = pd.read_excel(scores_file)
                elif att_filename.endswith('.csv'):
                    df3 = pd.read_csv(scores_file)
                else:
                    error = 'Unsupported file   type. Please upload a .csv or .xlsx file.'
                    df3 = None
                    
                df_temp=pd.merge(df1,df2,on="Roll_No",how='outer')
                df=pd.merge(df_temp,df3,on='Roll_No',how='outer')
                
                if df is not None:
                    missing = [col for col in REQUIRED_FIELDS if col not in df.columns]
                    if missing:
                        error = f'Missing required fields: {", ".join(missing)}'
                    else:
                        # Prepare input for model
                        input_df = df[FIELDS]
                        # Predict risk level (replace with actual model prediction)
                        if model:
                            preds = model.predict(input_df)
                            probs = model.predict_proba(input_df)
                        
                            confidence_scores = np.max(probs, axis=1)
                            
                            # Get probabilities for dropout class (class 1)
                            dropout_probabilities = probs[:, 1]  # Class 1 is dropout
                            dropout_probabilities = np.round(dropout_probabilities, 4)
                        else:
                            preds = ["Low"] * len(input_df)
                            confidence_scores = [0.5] * len(input_df)
            
                        
                        # Build predictions list for rendering
                        for i, row in df.iterrows():
                            FeeOverdue = 'Pending' if str(row.get('Tuition fees up to date', '')).strip().lower() in ['1'] else "Paid"
                            dropout_prob = np.round(dropout_probabilities[i] * 100, 1)
                            confidence = np.round(confidence_scores[i] * 100, 1)
                            
                            # Determine risk level based on dropout probability
                            if dropout_prob <= 40:
                                risk = f'Low ({dropout_prob}%)'
                            elif 40 < dropout_prob < 70:
                                risk = f'Medium ({dropout_prob}%)'
                            else:
                                risk = f'High ({dropout_prob}%)'
                            
                            sem1 = row.get("Curricular units 1st sem (grade)", 0)
                            sem2 = row.get("Curricular units 2nd sem (grade)", 0)
                            
                            predictions.append({
                                'Roll_No': row.get('Roll_No', i+1),
                                'Name': row.get('Name', f'Student {i+1}'),
                                'Attendance': row.get('Attendance', None),
                                'Sem_1_score': sem1,
                                'Sem_2_score': sem2,
                                'FeeStatus': FeeOverdue,
                                'risk_level': risk,
                                'confidence': f'{confidence}%',
                                # 'dropout_probability': f'{dropout_prob}%'
                            })
            except Exception as e:
                error = f'Error processing file: {str(e)}'
        # Render only the table for JS
        return render_template('index.html', predictions=predictions, error=error, model_metrics=MODEL_METRICS)
    # Initial page load
    return render_template('index.html', predictions=None, error=None, model_metrics=MODEL_METRICS)
  
@app.route('/send_mentor_alert', methods=['POST'])
def send_mentor_alert():
    data = request.get_json()
    mentor_email = data.get("mentor_email")
    if not mentor_email:
        return jsonify({"success": False, "message": "Email required"})
    high_risk = get_high_risk_students()
    if not high_risk:
        return jsonify({"success": False, "message": "No high-risk students"})
    body = "High-risk students:\n" + "\n".join([f"{s['name']} ({s['roll_no']}) - {s['risk_percentage']}" for s in high_risk])
    success = send_email_with_link("your_email@gmail.com", "app_password", mentor_email,
                                   "High-Risk Student Alert", body, "Dashboard", "http://localhost:5000")
    return jsonify({"success": success})

@app.route('/student_details/<roll_no>')
def student_details(roll_no):
    student = next((s for s in students_data if str(s['Roll_No']) == str(roll_no)), None)
    if student:
        sem1, sem2 = float(student.get('Sem_1_score', 0) or 0), float(student.get('Sem_2_score', 0) or 0)
        marks = [sem1, sem2]
        subjects = [student.get('Math_s1', 0), student.get('Eng_s1', 0), student.get('Sci_s1', 0)]
        print(student.keys(),'\n\n\n\n')

    else:
        marks = [0,0]
    return render_template("student_details.html", student=student, marks=marks)  

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
