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
# from flask_migrate import Migrate


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='supersecretkey'

db=SQLAlchemy(app)
# migrate = Migrate(app, db)

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
        
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "dropout_prediction.pkl")
    
# Load the trained model (replace with actual model loading)
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception:
    model = None
    print("model nope")


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
        if 'file' not in request.files or request.files['file'].filename == '':
            error = 'No file uploaded.'
        else:
            file = request.files['file']
            filename = file.filename.lower()
            try:
                if filename.endswith('.xlsx') or filename.endswith('.xls'):
                    df = pd.read_excel(file)
                elif filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    error = 'Unsupported file type. Please upload a .csv or .xlsx file.'
                    df = None
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
                            probs=model.predict_proba(input_df)
                            probabilities=probs[:,1]
                            probabilities=np.round((probabilities),4)
                        else:
                            preds = ["Low"] * len(input_df)
                        # Build predictions list for rendering
                        for i, row in df.iterrows():
                            FeeOverdue = 'Pending' if str(row.get('Tuition fees up to date', '')).strip().lower() in ['1'] else "Paid"
                            prob=np.round(probabilities[i]*100,1)   
                            risk=''
                            sem1=row.get("Curricular units 1st sem (grade)", 0)
                            sem2=row.get("Curricular units 2nd sem (grade)", 0)
                            if prob<=40:
                                risk=f'Low {prob}'
                            elif 40<prob<70:
                                risk=f'Medium {prob}'
                            else:
                                risk=f'High {prob}'
                            
                            predictions.append({
                                'Roll_No': row.get('Roll_No', i+1),
                                'Name': row.get('Name', f'Student {i+1}'),
                                'Attendance': row.get('Attendance', None),
                                'Sem_1_score':sem1,
                                'Sem_2_score':sem2,
                                'FeeStatus': FeeOverdue,
                                'risk_level':risk  
                            })
            except Exception as e:
                error = f'Error processing file: {str(e)}'
        # Render only the table for JS
        return render_template('index.html', predictions=predictions, error=error)
    # Initial page load
    return render_template('index.html', predictions=None, error=None)
  
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
