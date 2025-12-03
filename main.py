# ============================================
# FastAPI Backend - Fire Weather Index (FWI) Prediction
# ============================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd

app = FastAPI(title="FWI Prediction API")

# Allow Streamlit to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (you can restrict to localhost:8501)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model
model_data = joblib.load("PolynomialRegression_FWI_model.joblib")
model = model_data["model"]
scaler = model_data["scaler"]
imputer = model_data["imputer"]
poly = model_data["poly"]
features = model_data["features"]

@app.get("/")
def home():
    return {"message": "Welcome to the Fire Weather Index Prediction API!"}

@app.post("/api/predict")
def predict(data: dict):
    """Predict Fire Weather Index (FWI) from input features"""
    try:
        input_values = [data[f] for f in features]
        df_input = pd.DataFrame([input_values], columns=features)

        # Preprocess
        df_imputed = imputer.transform(df_input)
        df_poly = poly.transform(df_imputed)
        df_scaled = scaler.transform(df_poly)

        pred = round(model.predict(df_scaled)[0], 3)
        return {"predicted_FWI": pred}

    except Exception as e:
        return {"error": str(e)}
