from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# ML model loading example (uncomment and modify as needed)
# import joblib
# model = joblib.load('your_model_path.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        files = request.files
        required_keys = {'attendance', 'scores', 'fees'}
        if not required_keys.issubset(files.keys()):
            return jsonify({'error': 'Missing one or more required files: attendance, scores, fees'}), 400

        attendance_file = pd.read_excel(files['attendance'])
        scores_file = pd.read_excel(files['scores'])
        fee_file = pd.read_excel(files['fees'])

        # Validate columns exist in each file
        for df, name in zip([attendance_file, scores_file, fee_file], ['attendance', 'scores', 'fees']):
            if 'StudentID' not in df.columns:
                return jsonify({'error': f"Missing 'StudentID' column in {name} file"}), 400

        # Merge spreadsheets on StudentID
        df = attendance_file.merge(scores_file, on='StudentID').merge(fee_file, on='StudentID')

        # Optional: ML Model prediction
        # features = df[['AttendancePct', 'AverageScore', 'FeeOverdue']].values
        # df['risk_level'] = model.predict(features)

        # Rule-based risk calculation (fallback or baseline)
        def calculate_risk(row):
            if row['AttendancePct'] < 75 or row['AverageScore'] < 50 or row['FeeOverdue'] == 1:
                return 'High'
            elif row['AttendancePct'] < 85 or row['AverageScore'] < 65:
                return 'Medium'
            else:
                return 'Low'

        df['risk_level'] = df.apply(calculate_risk, axis=1)

        result = df[['StudentID','Name','AttendancePct','AverageScore','FeeOverdue','risk_level']].to_dict(orient='records')
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
