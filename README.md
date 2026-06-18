# Employee Attrition Prediction & HR Analytics Dashboard

An end-to-end data science and machine learning system that diagnoses the structural drivers of employee turnover, builds a predictive pipeline to assess flight risk, and provides an interactive dashboard for HR managers.

## Project Structure

```
Employee_Attrition_Project/
├── dataset/
│   ├── employee_attrition.csv          # Raw downloaded dataset
│   ├── cleaned_employee_attrition.csv  # Preprocessed dataset for modeling/Tableau
│   └── feature_importances.csv         # Feature weights exported from the model
├── notebooks/
│   └── EDA_and_Modeling.ipynb          # Step-by-step EDA and pipeline workbook
├── src/
│   ├── data_cleaning.py               # Preprocessing and SQLite database loader
│   └── model.py                        # ColumnTransformer & Random Forest training pipeline
├── dashboard/
│   └── app.py                          # Streamlit interactive multi-tab application
├── reports/
│   ├── Tableau_Guide.md               # Visual layout steps for Tableau
│   └── Business_Insights.md            # Strategic business recommendations
└── employee_attrition.db               # Local SQLite database containing HR records
```

# Employee Attrition Prediction & HR Analytics Dashboard

An end-to-end HR Analytics solution that identifies employee attrition patterns, predicts employee turnover risk using Machine Learning, and provides actionable workforce insights through interactive dashboards.

---

## Live Dashboard

🚀 **Interactive Dashboard**

[Open Live Dashboard](https://hr-attrition-predictor-analytics-dashboard-bvlsgz3k6mx8cwfalom.streamlit.app/)

---

## Project Overview

Employee attrition is one of the most critical challenges faced by organizations. High turnover leads to increased hiring costs, reduced productivity, and loss of organizational knowledge.

This project helps HR teams:

* Analyze workforce trends
* Identify key attrition drivers
* Predict employees at risk of leaving
* Generate data-driven retention strategies

---

## Features

### HR Analytics Dashboard

* Employee Attrition Rate
* Department-wise Attrition Analysis
* Salary vs Attrition Analysis
* Overtime Impact Analysis
* Job Satisfaction Insights

### Employee Attrition Prediction

Predicts whether an employee is likely to leave based on:

* Age
* Monthly Income
* Overtime Status
* Job Satisfaction
* Years at Company
* Work Environment Factors

### Attrition Risk Simulator

Interactive What-If analysis allowing HR managers to:

* Modify employee attributes
* Assess turnover risk instantly
* Receive retention recommendations

### SQL Analytics Module

Run custom SQL queries directly on employee data to perform:

* Department Analysis
* Workforce Distribution
* Compensation Analysis
* Attrition Investigation

---

## Machine Learning Pipeline

Dataset
↓
Data Cleaning
↓
Exploratory Data Analysis
↓
Feature Engineering
↓
Random Forest Classification
↓
Prediction
↓
Interactive Dashboard

---

## Technology Stack

### Programming

* Python

### Data Analysis

* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* Random Forest Classifier

### Visualization

* Plotly
* Matplotlib
* Seaborn

### Dashboard

* Streamlit

### Database

* SQLite
* SQLAlchemy

---

## Results

### Model Performance

* Accuracy: XX%
* Precision: XX%
* Recall: XX%
* F1 Score: XX%

### Top Attrition Drivers

1. Overtime
2. Monthly Income
3. Job Satisfaction
4. Age
5. Years At Company

---

## Business Insights

Key findings from the analysis:

* Employees working overtime exhibited significantly higher attrition rates.
* Lower-income employees demonstrated increased turnover probability.
* Employees with low job satisfaction were more likely to leave.
* Early-career employees showed higher attrition risk than experienced employees.

---

## Project Structure

Employee_Attrition_Project/

├── dataset/

├── notebooks/

├── src/

├── dashboard/

├── reports/

├── assets/

└── employee_attrition.db

---

## Future Enhancements

* XGBoost Model Integration
* Employee Segmentation using K-Means Clustering
* Real-Time HR Monitoring
* Automated Retention Recommendations
* Cloud Deployment

---

## Author
Sachi Prasad

