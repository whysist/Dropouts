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

1.Marital status: The marital status of the student. (Categorical)

2.Application mode: The method of application used by the student. (Categorical)

3.Application order: The order in which the student applied. (Numerical)

4.Course: The course taken by the student. (Categorical)

5.Daytime/evening attendance: Whether the student attends classes during the day or in the evening. (Categorical)

6.Previous qualification: The qualification obtained by the student before enrolling in higher education. (Categorical)

7.Nacionality: The nationality of the student. (Categorical)

8.Mother's qualification: The qualification of the student's mother. (Categorical)

9.Father's qualification: The qualification of the student's father. (Categorical)

10.Mother's occupation: The occupation of the student's mother. (Categorical)

11.Father's occupation: The occupation of the student's father. (Categorical)

12.Displaced: Whether the student is a displaced person. (Categorical)

13.Educational special needs: Whether the student has any special educational needs. (Categorical)

14.Debtor: Whether the student is a debtor. (Categorical)

15.Tuition fees up to date: Whether the student's tuition fees are up to date. (Categorical)

16.Gender: The gender of the student. (Categorical)

17.Scholarship holder: Whether the student is a scholarship holder. (Categorical)

18.Age at enrollment: The age of the student at the time of enrollment. (Numerical)

19.International: Whether the student is an international student. (Categorical)

20.Curricular units 1st sem (credited): The number of curricular units credited by the student in the first semester. (Numerical)

21.Curricular units 1st sem (enrolled): The number of curricular units enrolled by the student in the first semester. (Numerical)

22.Curricular units 1st sem (evaluations): The number of curricular units evaluated by the student in the first semester. (Numerical)

23.Curricular units 1st sem (approved): The number of curricular units approved by the student in the first semester. (Numerical)

24.Attendance



| S/N | Field                                | Description                                                       | Categories/Values                                                                                                    |
|-----|---------------------------------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| 1   | Marital status                       | The marital status of the student                                 | 1—Single, 2—Married, 3—Widower, 4—Divorced, 5—Facto union, 6—Legally separated                                       |
| 2   | Application mode                     | Method of application used by student                             | 1—1st phase—general contingent, 2—Ordinance No. 612/93, 3—1st phase—special contingent (Azores Island), ... , 18—Change in institution/course (International) |
| 3   | Application order                    | The order in which the student applied                            | Numeric                                                                                                               |
| 4   | Course                               | The course taken by the student                                   | 1—Biofuel Production Technologies, 2—Animation and Multimedia Design, 3—Social Service (evening), ... , 17—Management (evening) |
| 5   | Daytime/evening attendance           | Whether the student attends classes during the day or evening     | 1—Daytime, 0—Evening                                                                                                 |
| 6   | Previous qualification               | Qualification obtained before enrolling in higher education       | 1—Secondary education, 2—Higher ed bachelor’s, 3—Higher ed degree, 4—Master’s, 5—Doctorate, ... , 17—Master’s (2nd cycle) |
| 7   | Nationality                          | Nationality of the student                                        | 1—Portuguese, 2—German, 3—Spanish, 4—Italian, 5—Dutch, 6—English, ... , 21—Colombian                                |
| 8   | Mother’s qualification / Father’s qualification | Qualification of student’s parents                        | 1—Secondary education, 2—Bachelor’s, 3—Degree, 4—Master’s, 5—Doctorate, ... , 34—Doctorate (3rd cycle)              |
| 9   | Mother’s occupation / Father’s occupation | Occupation of student’s parents                              | 1—Student, 2—Legislative/Executive, 3—Specialists, 4—Technicians, 5—Admin staff, ... , 46—Street vendors             |
| 10  | Displaced                            | Whether the student is displaced                                  | 1—Yes, 0—No                                                                                                          |
| 11  | Educational special needs            | Whether the student has special educational needs                 | 1—Yes, 0—No                                                                                                          |
| 12  | Debtor                               | Whether the student is a debtor                                   | 1—Yes, 0—No                                                                                                          |
| 13  | Tuition fees up to date              | Whether tuition fees are up to date                               | 1—Yes, 0—No                                                                                                          |
| 14  | Gender                               | Gender of the student                                             | 1—Male, 0—Female                                                                                                     |
| 15  | Scholarship holder                   | Whether the student holds a scholarship                           | 1—Yes, 0—No                                                                                                          |
| 16  | Age at enrollment                    | Age of the student at enrollment                                  | Numeric                                                                                                               |
| 17  | International                        | Whether the student is an international student                   | 1—Yes, 0—No                                                                                                          |
| 18  | Curricular units 1st & 2nd sem (credited)  | Number of curricular units credited                               | Numeric                                                                                                               |
| 19  | Curricular units 1st & 2nd sem (enrolled)  | Number of curricular units enrolled                               | Numeric                                                                                                               |
| 20  | Curricular units 1st & 2nd sem (evaluations) | Number of curricular units evaluated                             | Numeric                                                                                                               |
| 21  | Curricular units 1st & 2nd sem (approved) | Number of curricular units approved                              | Numeric                                                                                                               |
| 22  | Curricular units 1st & 2nd sem (grade) | Number of curricular units grade                                 | Numeric                                                                                                               |
| 23  | Unemployment rate                    | Unemployment rate (%)                                             | Percentage                                                                                                            |
| 24  | Inflation rate                       | Inflation rate (%)                                                | Percentage                                                                                                            |
| 25  | GDP                                  | GDP per capita (USD)                                              | Numeric                                                                                                               |
| 26  | Target                               | Status of the student                                             | Graduate, Dropout, Enrolled                                                                                           |



