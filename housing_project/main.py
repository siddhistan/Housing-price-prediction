from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from pydantic import BaseModel
import os

app = FastAPI()

#  CORS (clean + correct)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ideal-waddle-4jjxwrx667v4f7945-5173.app.github.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Load model once
model_path = os.path.join(os.path.dirname(__file__), "models", "model_v1.pkl")
model = joblib.load(model_path)

#  Feature order (important)
features = ['OverallQual', 'GrLivArea', 'GarageCars', 'TotalBsmtSF', 'FullBath']

#  Input validation
class HouseInput(BaseModel):
    OverallQual: int
    GrLivArea: float
    GarageCars: int
    TotalBsmtSF: float
    FullBath: int

@app.get("/")
def home():
    return {"message": "House Price API is running"}

@app.post("/predict")
def predict(data: HouseInput):
    try:
        df = pd.DataFrame([[ 
            data.OverallQual,
            data.GrLivArea,
            data.GarageCars,
            data.TotalBsmtSF,
            data.FullBath
        ]], columns=features)

        prediction = model.predict(df)[0]

        return {"predicted_price": float(prediction)}

    except Exception as e:
        return {"error": str(e)}