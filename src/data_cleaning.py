import os
import pandas as pd
from sqlalchemy import create_engine

DATASET_URL = "https://raw.githubusercontent.com/nelson-wu/employee-attrition-ml/master/WA_Fn-UseC_-HR-Employee-Attrition.csv"
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset"))
RAW_PATH = os.path.join(DATA_DIR, "employee_attrition.csv")
CLEANED_PATH = os.path.join(DATA_DIR, "cleaned_employee_attrition.csv")
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../employee_attrition.db"))

def setup_directories():
    os.makedirs(DATA_DIR, exist_ok=True)

def download_data():
    if not os.path.exists(RAW_PATH):
        print(f"Downloading dataset from {DATASET_URL}...")
        df = pd.read_csv(DATASET_URL)
        df.to_csv(RAW_PATH, index=False)
        print("Dataset downloaded and saved to raw directory.")
    else:
        print("Raw dataset already exists.")

def clean_data():
    print("Loading and cleaning dataset...")
    df = pd.read_csv(RAW_PATH)
    
    print(f"Initial shape: {df.shape}")
    null_counts = df.isnull().sum().sum()
    if null_counts > 0:
        print(f"Found {null_counts} null values. Dropping rows with nulls...")
        df = df.dropna()
    
    categorical_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in categorical_cols:
        df[col] = df[col].astype(str).str.strip()
    
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"Removing {duplicates} duplicate rows...")
        df = df.drop_duplicates()
        
    print(f"Cleaned shape: {df.shape}")
    df.to_csv(CLEANED_PATH, index=False)
    print(f"Cleaned data saved to {CLEANED_PATH}")
    return df

def load_to_sqlite(df):
    print(f"Loading data into SQLite database at {DB_PATH}...")
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df.to_sql("employees", con=engine, if_exists="replace", index=False)
    print("Database table 'employees' successfully populated.")

if __name__ == "__main__":
    setup_directories()
    download_data()
    clean_df = clean_data()
    load_to_sqlite(clean_df)
