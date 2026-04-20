# Dropouts – AI-Based Student Dropout Prediction & Counseling

Dropouts is a Flask-based web application that predicts student dropout risk from institutional data and presents results in an educator-friendly dashboard.  
This project was built for **SIH problem statement 25102**.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Data Requirements](#data-requirements)
- [Local Setup](#local-setup)
- [Run with Docker](#run-with-docker)
- [Configuration](#configuration)
- [Application Routes](#application-routes)
- [Model Artifacts and Scripts](#model-artifacts-and-scripts)
- [Known Limitations](#known-limitations)
- [Dataset Source](#dataset-source)

## Overview
Many institutions keep attendance, fee, and performance data in separate files. This application merges those records using a common student identifier, runs a trained machine learning model, and classifies students as low/medium/high dropout risk.

The goal is to help teachers and mentors intervene earlier with students who need support.

## Key Features
- Upload 3 input files (Attendance, Marks, Fees) in `.csv`, `.xls`, or `.xlsx` format.
- Automatically merge data using `Roll_No`.
- Predict dropout probability with a pre-trained model (`dropout_prediction.pkl`).
- Show risk level categories:
  - **Low**: `<= 40%`
  - **Medium**: `> 40% and < 70%`
  - **High**: `>= 70%`
- Display model confidence per student.
- Provide student-level details with Chart.js visualizations.
- User registration/login with password hashing.
- PostgreSQL-backed user storage (SQLAlchemy ORM).
- Dockerized deployment with `docker-compose`.

## Tech Stack
**Backend**
- Python 3.11
- Flask
- SQLAlchemy / Flask-SQLAlchemy
- Pandas, NumPy
- scikit-learn, XGBoost
- psycopg2-binary

**Frontend**
- Jinja2 templates
- HTML/CSS/JavaScript
- Bootstrap (login/register pages)
- Chart.js (student charts)

**Database**
- PostgreSQL 17 (containerized in compose setup)

## Project Structure
```text
Dropouts/
├── README.md
└── SIH_Project/
    ├── app.py
    ├── ml_model.py
    ├── update_metrics.py
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env
    ├── dropout_prediction.pkl
    ├── xgboost_model.json
    ├── Datasets/
    │   ├── Dataset1.csv
    │   └── student_records_weighted.csv
    ├── templates/
    │   ├── index.html
    │   ├── student_details.html
    │   ├── login.html
    │   └── register.html
    └── migrations/
```

## How It Works
1. User uploads attendance, marks, and fees files from the main page.
2. Backend reads each file and merges on `Roll_No`.
3. Required features are extracted and passed to the loaded model.
4. Model predicts classes/probabilities (`predict` + `predict_proba`).
5. App maps dropout probability to risk tiers and renders a result table.
6. Clicking a student row opens detailed visual performance charts.

## Data Requirements
The merged dataset must include:
- `Roll_No`
- `Name`
- All model input fields listed below:
  - `Marital status`
  - `Application mode`
  - `Daytime/evening attendance`
  - `Previous qualification`
  - `Mother's occupation`
  - `Father's occupation`
  - `Displaced`
  - `Debtor`
  - `Tuition fees up to date`
  - `Scholarship holder`
  - `Age at enrollment`
  - `International`
  - `Curricular units 1st sem (evaluations)`
  - `Curricular units 1st sem (approved)`
  - `Curricular units 1st sem (grade)`
  - `Curricular units 2nd sem (evaluations)`
  - `Curricular units 2nd sem (approved)`
  - `Curricular units 2nd sem (grade)`
  - `Attendance`

If required columns are missing, the app returns a validation error.

## Local Setup
From `/home/runner/work/Dropouts/Dropouts/SIH_Project`:

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure PostgreSQL is running and create database `user_db`.

4. Configure environment variables (see [Configuration](#configuration)).

5. Start the app:
   ```bash
   python app.py
   ```

6. Open:
   ```text
   http://localhost:5000
   ```

## Run with Docker
From `/home/runner/work/Dropouts/Dropouts/SIH_Project`:

```bash
docker compose up --build
```

This starts:
- `web` service on `http://localhost:5000`
- `db` service (PostgreSQL) on port `5432`

Stop services:
```bash
docker compose down
```

## Configuration
Environment variables used by the app:

| Variable | Purpose | Example |
|---|---|---|
| `DB_USER` | PostgreSQL username | `sih_demo` |
| `DB_PASSWORD` | PostgreSQL password | `SIH_DEMO` |
| `DB_HOST` | PostgreSQL host | `localhost` or `db` |
| `DB_NAME` | PostgreSQL database name | `user_db` |
| `DB_PORT` | PostgreSQL port | `5432` |

Notes:
- `.env` is loaded via `python-dotenv`.
- For Docker Compose, `DB_HOST=db`.
- For local host-based DB, `DB_HOST=localhost`.

## Application Routes
| Route | Method(s) | Description |
|---|---|---|
| `/` | GET, POST | Main page; upload files and view predictions |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/student_details/<roll_no>` | GET | Student details + charts |
| `/model_info` | GET | Returns model metric JSON |
| `/send_mentor_alert` | POST | Sends email alert for high-risk students |

## Model Artifacts and Scripts
- `dropout_prediction.pkl`: Serialized trained model used in app inference.
- `xgboost_model.json`: Model artifact from training workflow.
- `ml_model.py`: SHAP-based interpretability analysis script.
- `update_metrics.py`: Utility to compute model metrics and update `MODEL_METRICS` in `app.py`.
- `prediction.ipynb`: Notebook for experimentation/training workflow.

## Known Limitations
- Email alert route uses placeholder sender credentials and must be configured before production use.
- `students_data` is an in-memory list and is not populated from `/` prediction results; as a result, mentor alerts and direct `student_details/<roll_no>` lookups may return no student data unless the app explicitly assigns uploaded prediction rows to `students_data` during request handling.
- Input schema is strict; uploaded files must match expected field names.
- Production security hardening is still needed (for example: HTTPS/TLS termination, secure cookie/session settings, CSRF protection on form routes, rotation of secrets outside `.env`, and running behind a production WSGI server instead of Flask debug mode).

## Dataset Source
- Kaggle:  
  https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention

---

If you use this project in institutional pilots or SIH demonstrations, consider sharing improvements for data quality checks, model explainability, and intervention workflows.
