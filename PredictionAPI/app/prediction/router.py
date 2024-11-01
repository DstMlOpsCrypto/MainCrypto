from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class PredictionRequest(BaseModel):
    asset: str
    prediction_horizon: int = 1  # en jours

class PredictionResponse(BaseModel):
    asset: str
    prediction_date: datetime
    message: str

@router.post("/price", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    try:
        return PredictionResponse(
            asset=request.asset,
            prediction_date=datetime.now(),
            message="Ici sera la prédiction"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))