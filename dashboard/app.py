import os
import pickle
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import sqlite3

# Set page config
st.set_page_config(
    page_title="HR Attrition Predictor & Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_employee_attrition.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "attrition_pipeline.pkl")
IMPORTANCE_PATH = os.path.join(BASE_DIR, "dataset", "feature_importances.csv")
DB_PATH = os.path.join(BASE_DIR, "employee_attrition.db")

# Load data helper
@st.cache_data
def load_clean_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Cleaned dataset not found at {DATA_PATH}. Please run data_cleaning.py first.")
        return None
    return pd.read_csv(DATA_PATH)

# Load model helper
def load_ml_model():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

# SQL Query Executor
def run_sql_query(query):
    conn = sqlite3.connect(DB_PATH)
    try:
        res = pd.read_sql_query(query, conn)
        conn.close()
        return res, None
    except Exception as e:
        conn.close()
        return None, str(e)

# Main Dashboard Logic
def main():
    st.title("Employee Attrition Prediction & HR Analytics Dashboard")
    st.markdown("An end-to-end analytical tool to diagnose attrition drivers, simulate flight risk, and query HR records.")
    
    df = load_clean_data()
    model = load_ml_model()
    
    if df is None:
        st.info("Execute `src/data_cleaning.py` to initialize data sources.")
        return

    # Sidebar KPI Quick Summary
    st.sidebar.header("HR Quick Overview")
    total_emp = len(df)
    att_rate = (df['Attrition'].value_counts(normalize=True).get('Yes', 0)) * 100
    avg_sal = df['MonthlyIncome'].mean()
    avg_age = df['Age'].mean()
    
    st.sidebar.metric("Total Employees", f"{total_emp:,}")
    st.sidebar.metric("Attrition Rate", f"{att_rate:.1f}%")
    st.sidebar.metric("Average Salary", f"${avg_sal:,.2f}")
    st.sidebar.metric("Average Age", f"{avg_age:.1f} Yrs")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive Summary", 
        "🔮 What-If Risk Simulator", 
        "💻 SQL Analytics Playground", 
        "🎯 Attrition Drivers (ML)"
    ])

    # Tab 1: Executive Summary
    with tab1:
        st.subheader("HR Health Indicators & Historical Turnover")
        
        # Row 1: KPI Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Department vs Attrition Bar Chart
            dept_att = df.groupby(['Department', 'Attrition']).size().reset_index(name='Count')
            fig_dept = px.bar(
                dept_att, 
                x="Department", 
                y="Count", 
                color="Attrition", 
                barmode="group",
                title="Employee Turnover by Department",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_dept, width="stretch")
            
        with col2:
            # Monthly Income vs Attrition Box plot
            fig_inc = px.box(
                df, 
                x="Attrition", 
                y="MonthlyIncome", 
                points="all",
                title="Monthly Income Distribution by Attrition Status",
                color="Attrition",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_inc, width="stretch")

        # Row 2: KPI Visualizations
        col3, col4 = st.columns(2)
        
        with col3:
            # Overtime vs Attrition
            ot_att = df.groupby(['OverTime', 'Attrition']).size().reset_index(name='Count')
            fig_ot = px.bar(
                ot_att, 
                x="OverTime", 
                y="Count", 
                color="Attrition", 
                barmode="group",
                title="Attrition Impact of Working Overtime",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_ot, width="stretch")
            
        with col4:
            # Job Satisfaction Stacked Bar Chart
            sat_att = df.groupby(['JobSatisfaction', 'Attrition']).size().reset_index(name='Count')
            fig_sat = px.bar(
                sat_att, 
                x="JobSatisfaction", 
                y="Count", 
                color="Attrition",
                title="Turnover across Job Satisfaction Levels (1=Low, 4=High)",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_sat, width="stretch")

    # Tab 2: What-If Risk Simulator
    with tab2:
        st.subheader("Interactive Employee Flight-Risk Evaluator")
        
        if model is None:
            st.warning("⚠️ Machine learning model file `attrition_pipeline.pkl` is missing. Run `src/model.py` first to train and serialize the model.")
        else:
            st.markdown("Adjust the characteristics of an employee below to predict their likelihood of leaving in real-time.")
            
            # Form setup
            with st.form("simulator_form"):
                sc1, sc2, sc3 = st.columns(3)
                
                with sc1:
                    age = st.slider("Age", 18, 60, 35)
                    gender = st.selectbox("Gender", ["Male", "Female"])
                    marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
                    travel = st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
                    dist = st.slider("Distance From Home (miles)", 1, 30, 5)
                    
                with sc2:
                    dept = st.selectbox("Department", ["Research & Development", "Sales", "Human Resources"])
                    role = st.selectbox("Job Role", [
                        "Sales Executive", "Research Scientist", "Laboratory Technician", 
                        "Manufacturing Director", "Healthcare Representative", "Manager", 
                        "Sales Representative", "Research Director", "Human Resources"
                    ])
                    income = st.slider("Monthly Income ($)", 1000, 20000, 5000)
                    overtime = st.selectbox("Working Overtime?", ["Yes", "No"])
                    stock = st.selectbox("Stock Option Level", [0, 1, 2, 3])

                with sc3:
                    job_sat = st.slider("Job Satisfaction Level (1-4)", 1, 4, 3)
                    env_sat = st.slider("Environment Satisfaction Level (1-4)", 1, 4, 3)
                    wl_balance = st.slider("Work-Life Balance Level (1-4)", 1, 4, 3)
                    invol = st.slider("Job Involvement Level (1-4)", 1, 4, 3)
                    tenure = st.slider("Years at Company", 0, 40, 5)
                    
                # Hidden/Default values for minor variables
                col_defaults = {
                    'DailyRate': 800, 'HourlyRate': 65, 'MonthlyRate': 14000,
                    'Education': 3, 'EducationField': 'Life Sciences', 'EmployeeCount': 1,
                    'EmployeeNumber': 9999, 'NumCompaniesWorked': 2, 'PercentSalaryHike': 15,
                    'PerformanceRating': 3, 'RelationshipSatisfaction': 3, 'StandardHours': 80,
                    'TotalWorkingYears': max(tenure, 8), 'TrainingTimesLastYear': 2,
                    'YearsInCurrentRole': max(0, tenure - 2), 'YearsSinceLastPromotion': 0,
                    'YearsWithCurrManager': max(0, tenure - 1), 'Over18': 'Y'
                }
                
                submitted = st.form_submit_button("Predict Flight Risk")
                
                if submitted:
                    # Construct input DataFrame matching original schema
                    input_data = {
                        'Age': [age], 'BusinessTravel': [travel], 'DailyRate': [col_defaults['DailyRate']],
                        'Department': [dept], 'DistanceFromHome': [dist], 'Education': [col_defaults['Education']],
                        'EducationField': [col_defaults['EducationField']], 'EmployeeCount': [col_defaults['EmployeeCount']],
                        'EmployeeNumber': [col_defaults['EmployeeNumber']], 'EnvironmentSatisfaction': [env_sat],
                        'Gender': [gender], 'HourlyRate': [col_defaults['HourlyRate']], 'JobInvolvement': [invol],
                        'JobLevel': [min(5, max(1, int(income / 4000)))], 'JobRole': [role], 'JobSatisfaction': [job_sat],
                        'MaritalStatus': [marital], 'MonthlyIncome': [income], 'MonthlyRate': [col_defaults['MonthlyRate']],
                        'NumCompaniesWorked': [col_defaults['NumCompaniesWorked']], 'Over18': [col_defaults['Over18']],
                        'OverTime': [overtime], 'PercentSalaryHike': [col_defaults['PercentSalaryHike']],
                        'PerformanceRating': [col_defaults['PerformanceRating']], 'RelationshipSatisfaction': [col_defaults['RelationshipSatisfaction']],
                        'StandardHours': [col_defaults['StandardHours']], 'StockOptionLevel': [stock],
                        'TotalWorkingYears': [col_defaults['TotalWorkingYears']], 'TrainingTimesLastYear': [col_defaults['TrainingTimesLastYear']],
                        'WorkLifeBalance': [wl_balance], 'YearsAtCompany': [tenure], 'YearsInCurrentRole': [col_defaults['YearsInCurrentRole']],
                        'YearsSinceLastPromotion': [col_defaults['YearsSinceLastPromotion']], 'YearsWithCurrManager': [col_defaults['YearsWithCurrManager']]
                    }
                    
                    input_df = pd.DataFrame(input_data)
                    
                    # Compute prediction probabilities
                    prob = model.predict_proba(input_df)[0][1]
                    risk_pct = prob * 100
                    
                    # Display results
                    st.write("---")
                    st.subheader("Model Risk Diagnosis")
                    
                    col_res, col_recs = st.columns([1, 2])
                    
                    with col_res:
                        if risk_pct < 30:
                            st.success(f"**Low Risk ({risk_pct:.1f}%)**")
                            st.info("Employee is stable. Maintain standard engagement.")
                        elif risk_pct < 65:
                            st.warning(f"**Medium Risk ({risk_pct:.1f}%)**")
                            st.markdown("⚠️ **Watch List**: Employee displays moderate flight risk. Monitor feedback.")
                        else:
                            st.error(f"**High Risk ({risk_pct:.1f}%)**")
                            st.markdown("🚨 **Immediate Action Required**: Extremely high likelihood of exit.")
                            
                    with col_recs:
                        st.write("💡 **Actionable Retention Recommendations:**")
                        recs = []
                        if overtime == 'Yes':
                            recs.append("- **Review Overtime load**: Overtime is a strong attrition predictor. Consider distributing workload or offering compensations.")
                        if income < 4500:
                            recs.append("- **Salary Adjustment**: Monthly salary is below standard thresholds. Review position market rates.")
                        if job_sat <= 2:
                            recs.append("- **Job Alignment Sync**: Schedule a feedback session to review task friction and role alignment.")
                        if env_sat <= 2:
                            recs.append("- **Workplace Comfort Check**: Address potential cultural or team environment challenges.")
                        if wl_balance <= 2:
                            recs.append("- **Flexible Work Scheduling**: Offer remote or structured flexible options to improve balance.")
                            
                        if not recs:
                            recs.append("- No immediate risk indicators triggered. Continue supportive management.")
                            
                        st.markdown("\n".join(recs))

    # Tab 3: SQL Analytics Playground
    with tab3:
        st.subheader("SQL Playground & HR Database Explorer")
        st.markdown("Review and run SQL queries against the local SQLite database. Below is the table schema for reference.")
        
        # Display schema info
        schema_cols = [
            "Age", "Attrition (Yes/No)", "BusinessTravel", "Department", "DistanceFromHome", 
            "EducationField", "EnvironmentSatisfaction (1-4)", "Gender", "JobRole", 
            "JobSatisfaction (1-4)", "MonthlyIncome", "OverTime (Yes/No)", "YearsAtCompany"
        ]
        st.caption(f"**Available Columns in 'employees' table:** {', '.join(schema_cols)}")
        
        # Predefined Query selection
        queries = {
            "Select a preset query...": "",
            "1. Attrition count by Department": "SELECT Department, COUNT(*) as Total_Employees, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) as Leavers FROM employees GROUP BY Department;",
            "2. Average Monthly Income by Attrition State": "SELECT Attrition, AVG(MonthlyIncome) as Average_Income FROM employees GROUP BY Attrition;",
            "3. Attrition Rate of Employees working Overtime": "SELECT OverTime, COUNT(*) as Total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) as Leavers, (CAST(SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 as Attrition_Rate FROM employees GROUP BY OverTime;",
            "4. Top 5 Job Roles with Attrition 'Yes'": "SELECT JobRole, COUNT(*) as Attrition_Count FROM employees WHERE Attrition='Yes' GROUP BY JobRole ORDER BY Attrition_Count DESC LIMIT 5;"
        }
        
        preset_choice = st.selectbox("Preloaded Queries", list(queries.keys()))
        sql_input = st.text_area("Write SQL Query", value=queries[preset_choice] if preset_choice != "Select a preset query..." else "SELECT * FROM employees LIMIT 5;", height=120)
        
        if st.button("Run SQL Command"):
            res, err = run_sql_query(sql_input)
            if err:
                st.error(f"SQL Error: {err}")
            else:
                st.dataframe(res, width="stretch")

    # Tab 4: Attrition Drivers (ML)
    with tab4:
        st.subheader("Model-Derived Attrition Drivers")
        st.markdown("This chart displays feature importance values derived from the Random Forest model. These weights represent which factors contribute most heavily to predicting a departure.")
        
        if not os.path.exists(IMPORTANCE_PATH):
            st.warning("⚠️ Feature importances not found. Please execute `src/model.py` to train the model and generate feature importances.")
        else:
            imp_df = pd.read_csv(IMPORTANCE_PATH)
            
            # Map clean names for readibility
            imp_df['Feature'] = imp_df['Feature'].str.replace('num__', '').str.replace('cat__', '')
            
            # Plot
            fig_imp = px.bar(
                imp_df.head(15), 
                x="Importance", 
                y="Feature", 
                orientation="h",
                title="Top 15 Predictors of Employee Flight-Risk",
                labels={"Importance": "Predictive Weight", "Feature": "Employee Attribute"},
                color="Importance",
                color_continuous_scale="Viridis"
            )
            fig_imp.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_imp, width="stretch")
            
            # Analytical takeaways
            st.markdown("""
            ### 💡 Core Takeaways for HR Managers
            Based on the analysis of the dataset, several variables dominate flight risk:
            1. **Overtime Work**: Working Overtime is the strongest categorical driver of attrition. High overtime correlates strongly with employee burnout and flight risk.
            2. **Compensation (Monthly Income)**: Low baseline income increases attrition, particularly in junior roles. Adjusting compensation bands to align with role seniority reduces turnover.
            3. **Job Satisfaction**: Employees scoring 1 or 2 on Job Satisfaction are disproportionately likely to leave. Tracking satisfaction metrics regularly is critical.
            4. **Age and Tenure (Years at Company)**: Younger employees with lower tenures leave at higher rates. Early onboarding support and structured early career development help lock in early talent.
            """)

if __name__ == "__main__":
    main()
