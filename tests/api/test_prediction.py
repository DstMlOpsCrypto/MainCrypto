# tests/api/test_prediction.py

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import List
import pytest

app = FastAPI()
router = APIRouter()

class Prediction(BaseModel):
    prediction_date: str
    prediction_value: float

# Base de données fictive des prédictions
fake_predictions_db = [
    {"prediction_date": "2024-11-09T00:00:00Z", "prediction_value": 50000.0}
]

@router.get("/prediction/latest-prediction", response_model=Prediction)
async def get_latest_prediction():
    if fake_predictions_db:
        return fake_predictions_db[-1]
    else:
        raise HTTPException(status_code=404, detail="No predictions found")

app.include_router(router)

# Début des tests
client = TestClient(app)

def test_get_latest_prediction():
    response = client.get("/prediction/latest-prediction")
    assert response.status_code == 200
    data = response.json()
    assert "prediction_date" in data
    assert "prediction_value" in data
    assert data["prediction_value"] == 50000.0
