import shap
import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "dropout_prediction.pkl")

def load_model():
    """Load the trained model"""
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Model loading failed: {e}")
        return None

def preprocess_data(df):
    """Preprocess data same as training - this is crucial for SHAP"""
    # Add attendance column (same as in your notebook)
    if 'Attendance' not in df.columns:
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
    if 'Target' in df.columns:
        df['Target'] = df['Target'].map({
            'Dropout': 1,
            'Graduate': 0,
            'Enrolled': 2
        })
    
    # Drop unnecessary columns (same as your training)
    columns_to_drop = [
        'GDP', 'Unemployment rate', 'Inflation rate', 'Nacionality',
        'Application order', 'Course', "Mother's qualification",
        "Father's qualification", "Educational special needs", "Gender",
        "Curricular units 1st sem (enrolled)", "Curricular units 1st sem (credited)",
        "Curricular units 1st sem (without evaluations)", "Curricular units 2nd sem (credited)",
        "Curricular units 2nd sem (enrolled)", "Curricular units 2nd sem (without evaluations)"
    ]
    
    # Only drop columns that exist
    columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df = df.drop(columns=columns_to_drop)
    
    # Remove outliers in Age at enrollment
    if 'Age at enrollment' in df.columns:
        Q1 = df['Age at enrollment'].quantile(0.25)
        Q3 = df['Age at enrollment'].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - (1.5 * IQR)
        upper = Q3 + (1.5 * IQR)
        df = df[((df['Age at enrollment'] >= lower) & (df['Age at enrollment'] <= upper))]
    
    return df

def main():
    """Main function to run SHAP analysis"""
    try:
        # Load and preprocess training data
        print("Loading training data...")
        X_train_raw = pd.read_csv("Datasets/Dataset1.csv")
        X_train_processed = preprocess_data(X_train_raw.copy())
        
        # Separate features and target
        if 'Target' in X_train_processed.columns:
            X_train = X_train_processed.drop(columns=['Target'])
            y_train = X_train_processed['Target']
        else:
            X_train = X_train_processed
        
        # Load test data
        print("Loading test data...")
        X_test_raw = pd.read_csv("Datasets/student_records_weighted.csv")
        
        # Check if test data has Target column
        if 'Target' in X_test_raw.columns:
            X_test_processed = preprocess_data(X_test_raw.copy())
            X_test = X_test_processed.drop(columns=['Target'])
        else:
            # If no Target column, add dummy values for preprocessing
            X_test_raw['Target'] = 'Graduate'  # Dummy value
            X_test_processed = preprocess_data(X_test_raw.copy())
            X_test = X_test_processed.drop(columns=['Target'])
        
        # Ensure both datasets have same columns
        common_columns = list(set(X_train.columns) & set(X_test.columns))
        X_train = X_train[common_columns]
        X_test = X_test[common_columns]
        
        print(f"Training data shape: {X_train.shape}")
        print(f"Test data shape: {X_test.shape}")
        
        # Load model
        model = load_model()
        if model is None:
            return
        
        # Create SHAP explainer
        print("Creating SHAP explainer...")
        # Use a smaller sample for faster computation
        background_sample = shap.sample(X_train, min(100, len(X_train)))
        explainer = shap.KernelExplainer(model.predict_proba, background_sample)
        
        # Calculate SHAP values for first few test samples
        print("Calculating SHAP values...")
        n_samples = min(5, len(X_test))  # Limit to first 5 samples for speed
        shap_values = explainer.shap_values(X_test.iloc[:n_samples])
        
        # Initialize SHAP JavaScript
        shap.initjs()
        
        # Create force plot for first sample, dropout class (class 1)
        print("Creating SHAP plots...")
        force_plot = shap.force_plot(
            explainer.expected_value[1], 
            shap_values[1][0], 
            X_test.iloc[0, :],
            matplotlib=True
        )
        
        # Summary plot
        shap.summary_plot(shap_values[1], X_test.iloc[:n_samples], plot_type="bar")
        
        print("SHAP analysis completed successfully!")
        
    except Exception as e:
        print(f"Error in SHAP analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

