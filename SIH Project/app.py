from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for frontend-backend communication

app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'student_data' not in request.files:
            return jsonify({'error': 'Missing student data file.'}), 400

        file = request.files['student_data']
        df = pd.read_excel(file)

        # Validate all required columns exist
        required_columns = {'StudentID', 'Name', 'AttendancePct', 'AverageScore', 'FeeOverdue'}
        if not required_columns.issubset(df.columns):
            return jsonify({'error': f"Missing columns. Required: {', '.join(required_columns)}"}), 400

        # Rule-based risk calculation
        def calculate_risk(row):
            if row['AttendancePct'] < 75 or row['AverageScore'] < 50 or row['FeeOverdue'] == 1:
                return 'High'
            elif row['AttendancePct'] < 85 or row['AverageScore'] < 65:
                return 'Medium'
            else:
                return 'Low'

        df['risk_level'] = df.apply(calculate_risk, axis=1)

        result = df[['StudentID', 'Name', 'AttendancePct', 'AverageScore', 'FeeOverdue', 'risk_level']].to_dict(orient='records')
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
