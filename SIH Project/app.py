from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files
    attendance_file = pd.read_excel(files['attendance'])
    scores_file = pd.read_excel(files['scores'])
    fee_file = pd.read_excel(files['fees'])

    # Merge spreadsheets on StudentID
    df = attendance_file.merge(scores_file, on='StudentID').merge(fee_file, on='StudentID')

    # Rule-based risk calculation
    def calculate_risk(row):
        if row['AttendancePct'] < 75 or row['AverageScore'] < 50 or row['FeeOverdue'] == 1:
            return 'High'
        elif row['AttendancePct'] < 85 or row['AverageScore'] < 65:
            return 'Medium'
        else:
            return 'Low'

    df['risk_level'] = df.apply(calculate_risk, axis=1)

    # Return JSON
    result = df[['StudentID','Name','AttendancePct','AverageScore','FeeOverdue','risk_level']].to_dict(orient='records')
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
