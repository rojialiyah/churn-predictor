from fastapi import FastAPI
from schemas import CustomerData
import joblib
import pandas as pd
import os

# 1. Start the API Manager
app = FastAPI(title="Telecom Churn Predictor API")

# 2. Load the model ONCE when the app starts, not on every single request
# (Make sure you moved your model.joblib file into the models/ folder!)
model = joblib.load("../models/model.joblib")

# 3. Read the business threshold from the environment (defaults to 30% if not set)
# We use a lower threshold because missing a churner costs more than offering a discount.
CHURN_THRESHOLD = float(os.getenv("CHURN_THRESHOLD", "0.30"))

@app.get("/health")
def health_check():
    """Returns a simple status message to prove the server is awake."""
    return {"status": "healthy", "message": "API is up and running."}

@app.get("/model-info")
def model_info():
    """Returns metadata about the deployed model."""
    return {
        "model_name": "Gradient Boosting Pipeline",
        "training_date": "2026",
        "library_versions": {"scikit-learn": "1.2.2"}, 
        "test_metrics": {"ROC-AUC": 0.84, "Precision": 0.65, "Recall": 0.72}
    }

@app.post("/predict")
def predict_churn(data: CustomerData):
    """Accepts customer JSON, validates it, and returns the churn risk band."""
    
    # Convert the validated Pydantic data back into a Pandas DataFrame for the AI
    # by_alias=True puts the spaces back in the column names (e.g. "Monthly Charges")
    try:
        input_dict = data.model_dump(by_alias=True)
    except AttributeError:
        input_dict = data.dict(by_alias=True) # For older versions of Pydantic
        
    df = pd.DataFrame([input_dict])
    
    # Get the exact probability (a decimal between 0.0 and 1.0)
    churn_prob = model.predict_proba(df)[0][1]
    
    # Calculate the label based on our strict business threshold
    predicted_label = 1 if churn_prob >= CHURN_THRESHOLD else 0
    
    # Assign a Risk Band
    if churn_prob >= 0.70:
        risk_band = "High"
    elif churn_prob >= CHURN_THRESHOLD:
        risk_band = "Medium"
    else:
        risk_band = "Low"
        
    return {
        "churn_probability": round(churn_prob, 3),
        "predicted_label": predicted_label,
        "risk_band": risk_band,
        "threshold_used": CHURN_THRESHOLD
    }
