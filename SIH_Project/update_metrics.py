#!/usr/bin/env python3
"""
Update model metrics in app.py with actual calculated values
Run this script to get the real F1 score and other metrics for your model
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
import re

def calculate_actual_metrics():
    """Calculate actual model metrics and update app.py"""
    
    print("Loading dataset and preprocessing...")
    
    # Load and preprocess data (same as your notebook)
    df = pd.read_csv("Datasets/Dataset1.csv")
    
    # Add attendance column
    attendance = []
    for s in df['Target']:
        if s == 'Dropout':
            val = np.random.normal(60, 9)
        elif s == 'Graduate':
            val = np.random.normal(85, 7)
        else:
            val = np.random.normal(75, 10)
        val = np.clip(val, 40, 100)
        attendance.append(val)
    
    df.insert(len(df.columns)-1, "Attendance", np.round(attendance, 1))
    
    # Map target values
    df['Target'] = df['Target'].map({
        'Dropout': 1,
        'Graduate': 0,
        'Enrolled': 2
    })
    
    # Drop unnecessary columns
    columns_to_drop = [
        'GDP', 'Unemployment rate', 'Inflation rate', 'Nacionality',
        'Application order', 'Course', "Mother's qualification",
        "Father's qualification", "Educational special needs", "Gender",
        "Curricular units 1st sem (enrolled)", "Curricular units 1st sem (credited)",
        "Curricular units 1st sem (without evaluations)", "Curricular units 2nd sem (credited)",
        "Curricular units 2nd sem (enrolled)", "Curricular units 2nd sem (without evaluations)"
    ]
    df.drop(columns=columns_to_drop, inplace=True)
    
    # Remove outliers
    Q1 = df['Age at enrollment'].quantile(0.25)
    Q3 = df['Age at enrollment'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - (1.5 * IQR)
    upper = Q3 + (1.5 * IQR)
    df = df[((df['Age at enrollment'] >= lower) & (df['Age at enrollment'] <= upper))]
    
    # Prepare features and target
    X = df.drop(columns=["Target"])
    y = df['Target']
    
    # Split data (same random state as notebook)
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    print("Loading trained model...")
    
    # Load the trained model
    with open("dropout_prediction.pkl", 'rb') as f:
        model = pickle.load(f)
    
    print("Making predictions...")
    
    # Make predictions
    y_pred = model.predict(x_test)
    y_pred_proba = model.predict_proba(x_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    auc_score = roc_auc_score(y_test, y_pred_proba, multi_class='ovr')
    
    print("\n" + "="*50)
    print("CALCULATED MODEL PERFORMANCE METRICS")
    print("="*50)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1 Score (Macro): {f1_macro:.4f}")
    print(f"F1 Score (Weighted): {f1_weighted:.4f}")
    print(f"ROC AUC Score: {auc_score:.4f}")
    print("="*50)
    
    # Update app.py with actual metrics
    print("\nUpdating app.py with calculated metrics...")
    
    # Read current app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Create new MODEL_METRICS block
    new_metrics = f"""MODEL_METRICS = {{
    'f1_score_macro': {f1_macro:.4f},
    'f1_score_weighted': {f1_weighted:.4f},
    'accuracy': {accuracy:.4f},
    'auc_score': {auc_score:.4f}
}}"""
    
    # Replace the MODEL_METRICS section
    pattern = r'MODEL_METRICS = \{[^}]+\}'
    if re.search(pattern, content):
        content = re.sub(pattern, new_metrics, content)
        
        # Write back to file
        with open('app.py', 'w') as f:
            f.write(content)
        
        print("✅ Successfully updated app.py with actual model metrics!")
    else:
        print("❌ Could not find MODEL_METRICS section in app.py")
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'auc_score': auc_score
    }

if __name__ == "__main__":
    try:
        metrics = calculate_actual_metrics()
        print(f"\n🎉 Model evaluation complete!")
        print(f"Your model's F1 score (macro): {metrics['f1_macro']:.4f}")
        print(f"Your model's F1 score (weighted): {metrics['f1_weighted']:.4f}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure your dataset and model files are in the correct location.")