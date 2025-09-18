# Dropouts
SIH problem statement 25102 (AI-based drop-out prediction and counseling system)

## Introduction 
In many educational institutions, the data that signals a student is struggling is scattered across isolated spreadsheets—attendance in one, test scores in another. By the time
term-end marks officially confirm a problem, many of these students have already disengaged beyond recovery. This project tackles this challenge by building an early-warning
dashboard for educators. It automatically ingests and fuses disparate student data into a single, intuitive interface. Using clear, rule-based logic and machine learning
approaches, the system flags at-risk students in real-time, empowering mentors to intervene proactively long before it's too late. Our goal is to transform fragmented data into
an actionable tool that helps reduce dropout rates and foster student success.

## Requirements

#### Functional Requirements
1. Data Upload: Users must be able to upload multiple spreadsheets (attendance, scores, etc.).
2. Data Merging: The system must automatically link data for the same student across different files (using a unique ID like a student roll number).
3. Risk Calculation: The system must apply predefined logic to calculate a risk score for each student.
4. Dashboard View: Display an overview of all students, sorted by risk level.
5. Detailed Student Profile: Show individual student data, trends over time (e.g., a chart of their test scores), and the specific factors contributing to their risk score.
6. Automated Notifications: Send scheduled email reports to registered mentors.

#### Non-Functional Requirements
1. Usability: The interface must be extremely intuitive for non-technical users (teachers, counselors).
2. Transparency: The reason for a student's risk score must be clearly explained.
3. Low Maintenance: The system should run without needing constant technical intervention.
4. Configurability: Ideally, administrators should be able to tweak the risk thresholds (e.g., change the definition of "low attendance" from <75% to <80%).

## Tech Stack 
_**Backend**_: Python with Flask (lightweight and fast to set up) and Pandas (for data manipulation).

_**Frontend**_: Plain HTML, CSS, and JavaScript with Chart.js (for graphs) and Bootstrap (for a clean UI without much effort).


### Dataset Characteristics 

https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention
Marital status: The marital status of the student. (Categorical)
Application mode: The method of application used by the student. (Categorical)
Application order: The order in which the student applied. (Numerical)
Course: The course taken by the student. (Categorical)
Daytime/evening attendance: Whether the student attends classes during the day or in the evening. (Categorical)
Previous qualification: The qualification obtained by the student before enrolling in higher education. (Categorical)
Nacionality: The nationality of the student. (Categorical)
Mother's qualification: The qualification of the student's mother. (Categorical)
Father's qualification: The qualification of the student's father. (Categorical)
Mother's occupation: The occupation of the student's mother. (Categorical)
Father's occupation: The occupation of the student's father. (Categorical)
Displaced: Whether the student is a displaced person. (Categorical)
Educational special needs: Whether the student has any special educational needs. (Categorical)
Debtor: Whether the student is a debtor. (Categorical)
Tuition fees up to date: Whether the student's tuition fees are up to date. (Categorical)
Gender: The gender of the student. (Categorical)
Scholarship holder: Whether the student is a scholarship holder. (Categorical)
Age at enrollment: The age of the student at the time of enrollment. (Numerical)
International: Whether the student is an international student. (Categorical)
Curricular units 1st sem (credited): The number of curricular units credited by the student in the first semester. (Numerical)
Curricular units 1st sem (enrolled): The number of curricular units enrolled by the student in the first semester. (Numerical)
Curricular units 1st sem (evaluations): The number of curricular units evaluated by the student in the first semester. (Numerical)
Curricular units 1st sem (approved): The number of curricular units approved by the student in the first semester. (Numerical)



