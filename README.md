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




