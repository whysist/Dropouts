import os
import pickle
import pandas as pd
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, 'dropout_prediction.pkl')
    print(f"Attempting to load model from: {model_path}")

    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        model = None
    else:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            print("Model loaded successfully!")
            print(f"Model type: {type(model)}")
            print(f"Model attributes: {dir(model)}")
except Exception as e:
    import sys
    print(f"Error loading model: {e}")
    print(f"Python version: {sys.version}")
    model = None

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

students_data = []

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
    """Get list of students with high risk levels (marked red)"""
    high_risk_students = []
    for student in students_data:
        risk_level = student.get('risk_level', '')
        if risk_level.startswith('High'):
            high_risk_students.append({
                'name': student.get('Name', 'Unknown'),
                'roll_no': student.get('Roll_No', 'Unknown'),
                'risk_percentage': risk_level.split()[-1] if len(risk_level.split()) > 1 else 'N/A',
                'attendance': student.get('Attendance', 'N/A'),
                'fee_status': student.get('FeeStatus', 'N/A')
            })
    return high_risk_students

# def get_cumulative_score(row):
#     sem1 = row.get("Curricular units 1st sem (grade)", 0)
#     sem2 = row.get("Curricular units 2nd sem (grade)", 0)
#     try:
#         return round((float(sem1) + float(sem2)) / 2, 2)
#     except Exception:
#         return None

@app.route('/send_mentor_alert', methods=['POST'])
def send_mentor_alert():
    """Send email alert to mentor with list of high-risk students"""
    try:
        data = request.get_json()
        mentor_email = data.get('mentor_email')
        sender_email =  'sirnasaivishnu@gmail.com'  # Configure with actual sender
        sender_password =  'sial zqqr egqu bpws' # Configure with app password
        
        if not mentor_email:
            return jsonify({'success': False, 'message': 'Mentor email is required'})
        
        high_risk_students = get_high_risk_students()
        
        if not high_risk_students:
            return jsonify({'success': False, 'message': 'No high-risk students found'})
        
        # Create email content
        subject = "High-Risk Student Alert - Immediate Attention Required"
        
        student_list = ""
        for student in high_risk_students:
            student_list += f"""
            • {student['name']} (Roll No: {student['roll_no']})
              - Risk Level: {student['risk_percentage']}
              - Attendance: {student['attendance']}%
              - Fee Status: {student['fee_status']}
                \n
            """
        
        body = f"""
        Dear Mentor,

        This is an automated alert from the Student Dropout Risk Prediction System.

        The following students have been identified as having HIGH RISK of dropout and require immediate attention:

        {student_list}

        Please reach out to these students for counseling and support as soon as possible.

        Best regards,
        Student Support System
        """
        
        # Dashboard link (you can customize this URL)
        dashboard_url = "http://localhost:5000"  # Update with your actual URL
        link_text = "View Full Dashboard"
        
        success = send_email_with_link(
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=mentor_email,
            subject=subject,
            body=body,
            link_text=link_text,
            link_url=dashboard_url
        )
        
        try:
            if success:
                return jsonify({
                    'success': True, 
                    'message': f'Alert sent successfully to {mentor_email}. {len(high_risk_students)} high-risk students reported.'
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to send email. Please check email configuration.'})
        except Exception as e:
            print(f"Error while sending email: {str(e)}")
            return jsonify({'success': False, 'message': f'Error while sending email: {str(e)}'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/', methods=['GET', 'POST'])
def index():
    global students_data
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
                    df.columns = df.columns.str.strip()  # Strip whitespace from column names
                    missing = [col for col in REQUIRED_FIELDS if col not in df.columns]
                    if missing:
                        error = f'Missing required fields: {", ".join(missing)}'
                    else:
                        # Prepare input for model
                        input_df = df[FIELDS]
                        # Predict risk level (replace with actual model prediction)
                        if model:
                            print("Making predictions with model...")
                            print(f"Input shape: {input_df.shape}")
                            preds = model.predict(input_df)
                            probs = model.predict_proba(input_df)
                            print(f"Raw predictions: {preds[:5]}")  # Show first 5 predictions
                            print(f"Raw probabilities: {probs[:5]}")  # Show first 5 probabilities
                            probabilities = probs[:,1]
                            probabilities = np.round((probabilities),4)
                        else:
                            print("Warning: Model is None, using default predictions")
                            preds = ["Low"] * len(input_df)
                            probabilities = np.zeros(len(input_df))  # Add this line
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
                                'risk_level':risk,
                                'Math_s1': row.get('Math_sem1', 0),
                                'Eng_s1': row.get('English_sem1', 0),
                                'Sci_s1': row.get('Science_sem1', 0),
                                'Math_s2': row.get('Math_sem2', 0),
                                'Eng_s2': row.get('English_sem2', 0),
                                'Sci_s2': row.get('Science_sem2', 0),

                            })
                            students_data = predictions
            except Exception as e:
                error = f'Error processing file: {str(e)}'
        # Render only the table for JS
        return render_template('index.html', predictions=predictions, error=error)
    # Initial page load
    return render_template('index.html', predictions=None, error=None)

# In your Flask route
@app.route('/student_details/<roll_no>')
def student_details(roll_no):
    student = next((s for s in students_data if str(s['Roll_No']) == str(roll_no)), None)
    if student:
        # Directly extract the grades from the student dictionary
        sem1 = float(student.get('Sem_1_score', 0) or 0)
        sem2 = float(student.get('Sem_2_score', 0) or 0)
        marks = [sem1, sem2]
        subjects = [student.get('Math_s1', 0), student.get('Eng_s1', 0), student.get('Sci_s1', 0)]
        

        print(student.keys(),'\n\n\n\n')
    else:
        marks = [0, 0]
    return render_template('student_details.html', student=student, marks=marks)

if __name__ == '__main__':
    app.run(debug=True)
