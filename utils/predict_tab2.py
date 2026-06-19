import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.filterwarnings('ignore')

# Global cache so we don't retrain the model on every click
_MODEL_CACHE = None
_ENCODERS_CACHE = {}

def train_model():
    """Trains the classification model using the local dataset."""
    global _MODEL_CACHE, _ENCODERS_CACHE
    
    df = pd.read_csv("data/tab2.csv")
    
    # Separate features and target
    X = df.drop(columns=["Perforated"])
    y = df["Perforated"]
    
    # Identify categorical columns
    cat_cols = ["Calibre", "Projectile Type", "Shape", "s_type", "Material", "Plate Material"]
    
    # Encode categorical features
    for col in cat_cols:
        le = LabelEncoder()
        # Convert to string to prevent mixed type errors
        X[col] = le.fit_transform(X[col].astype(str))
        _ENCODERS_CACHE[col] = le
        
    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    _MODEL_CACHE = model
    return model

def predict_perforation(input_data):
    """
    Takes a dictionary of input parameters and predicts if the target is perforated.
    """
    df = pd.read_csv("data/tab2.csv")
    
    # 1. Check if an exact record exists in the dataset
    # We'll use a subset of key continuous values with a tolerance to find a match
    tolerance = 1e-3
    match_condition = (
        (df["Calibre"].astype(str) == input_data["Calibre"]) & 
        (df["Material"].astype(str) == input_data["Material"]) &
        (abs(df["Actual Velocity"] - input_data["Actual Velocity"]) < tolerance) &
        (abs(df["Kinetic Energy"] - input_data["Kinetic Energy"]) < tolerance)
    )
    
    matched_records = df[match_condition]
    
    actual_perforated = None
    dataset_found = False
    
    if not matched_records.empty:
        dataset_found = True
        actual_perforated = matched_records.iloc[0]["Perforated"]

    # 2. Prepare data for model prediction
    if _MODEL_CACHE is None:
        train_model()
        
    model = _MODEL_CACHE
    
    # Create DataFrame for single input
    input_df = pd.DataFrame([input_data])
    
    # Reorder columns to match training exactly
    training_cols = pd.read_csv("data/tab2.csv").drop(columns=["Perforated"]).columns
    input_df = input_df[training_cols]
    
    # Encode categoricals using cached encoders
    cat_cols = ["Calibre", "Projectile Type", "Shape", "s_type", "Material", "Plate Material"]
    for col in cat_cols:
        le = _ENCODERS_CACHE[col]
        # Handle unseen labels gracefully by assigning them a default/unknown class if needed
        try:
            input_df[col] = le.transform(input_df[col].astype(str))
        except ValueError:
            # Fallback for entirely new dropdown categories not in original CSV
            input_df[col] = 0 

    # Predict
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities) * 100

    return {
        "dataset_found": dataset_found,
        "actual_perforated": actual_perforated,
        "predicted_perforated": int(prediction),
        "confidence": confidence,
        "best_model": "Random Forest Classifier (Ensemble)"
    }