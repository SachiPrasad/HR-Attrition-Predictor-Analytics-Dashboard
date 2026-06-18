import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dataset"))
CLEANED_PATH = os.path.join(DATA_DIR, "cleaned_employee_attrition.csv")
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models"))
MODEL_PATH = os.path.join(MODEL_DIR, "attrition_pipeline.pkl")
IMPORTANCE_PATH = os.path.join(DATA_DIR, "feature_importances.csv")

def load_data():
    if not os.path.exists(CLEANED_PATH):
        raise FileNotFoundError(f"Cleaned dataset not found at {CLEANED_PATH}. Please run data_cleaning.py first.")
    return pd.read_csv(CLEANED_PATH)

def train_model():
    df = load_data()
    
    # Drop irrelevant columns or zero-variance ones
    cols_to_drop = ['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])
    
    target_col = 'Attrition'
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")
        
    y = df[target_col].apply(lambda x: 1 if str(x).lower() == 'yes' else 0)
    X = df.drop(columns=[target_col])
    
    categorical_cols = X.select_dtypes(include=['object', 'string']).columns.tolist()
    numerical_cols = X.select_dtypes(exclude=['object', 'string']).columns.tolist()
    
    # Preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
        ]
    )
    
    # RF with balanced class weights due to attrition class imbalance
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=12,
        class_weight='balanced',
        random_state=42
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', clf)
    ])
    
    # Stratified split to preserve target ratio
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training Random Forest classifier pipeline...")
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    y_probs = pipeline.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_probs)
    
    print("\n=== Model Evaluation ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC-AUC:  {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save trained pipeline
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"Pipeline successfully serialized and saved to {MODEL_PATH}")
    
    # Feature Importance Extraction
    cat_transformer = pipeline.named_steps['preprocessor'].named_transformers_['cat']
    encoded_cat_names = cat_transformer.get_feature_names_out(categorical_cols).tolist()
    feature_names = numerical_cols + encoded_cat_names
    
    importances = pipeline.named_steps['classifier'].feature_importances_
    
    feat_imp_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    feat_imp_df.to_csv(IMPORTANCE_PATH, index=False)
    print(f"Feature importances exported to {IMPORTANCE_PATH}")
    
    print("\nTop 10 Feature Importances:")
    print(feat_imp_df.head(10).to_string(index=False))

if __name__ == "__main__":
    train_model()
