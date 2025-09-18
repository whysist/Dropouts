import pickle
import pandas as pd
from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

# Load the trained model (replace with actual model loading)
try:
    with open('Dropouts\\SIH Project\\dropout_prediction.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception:
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

# def get_cumulative_score(row):
#     sem1 = row.get("Curricular units 1st sem (grade)", 0)
#     sem2 = row.get("Curricular units 2nd sem (grade)", 0)
#     try:
#         return round((float(sem1) + float(sem2)) / 2, 2)
#     except Exception:
#         return None

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
    app.run(debug=True)
