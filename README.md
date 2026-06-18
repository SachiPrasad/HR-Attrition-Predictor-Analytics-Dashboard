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

## Setup & Running Instructions

### 1. Install Dependencies
Ensure you have Python 3.10+ installed. In your terminal, run:
```bash
pip install -r requirements.txt
```

### 2. Preprocess Data & Initialize SQLite
Run the cleaning script to download the raw dataset, generate the cleaned CSV, and load it into the database:
```bash
python src/data_cleaning.py
```

### 3. Train the Model Pipeline
Run the model script to preprocess features, train the Random Forest Classifier, serialize the pipeline, and output metrics:
```bash
python src/model.py
```

### 4. Interactive Dashboard
Launch the Streamlit dashboard:
```bash
https://hr-attrition-predictor-analytics-dashboard-bvlsgz3k6mx8cwfalom.streamlit.app/
```

## Features & Highlights

- **Machine Learning Pipeline**: Uses `ColumnTransformer` to bundle numerical scaling and categorical one-hot encoding with a `RandomForestClassifier`. Evaluates performance using stratified splits and handles class imbalance directly.
- **What-If Risk Simulator**: An interactive panel where HR managers can adjust employee attributes (e.g., age, salary, overtime, satisfaction) and see an instant risk assessment paired with automated retention recommendations.
- **Embedded SQL Playground**: A SQL runner tab inside the dashboard allowing recruiters to query the SQLite table (`employees`) directly, see results in real-time, and run preset analytic queries.
- **Tableau Readiness**: Exports clean datasets ready to load into Tableau, backed by a detailed design guide (`reports/Tableau_Guide.md`).
