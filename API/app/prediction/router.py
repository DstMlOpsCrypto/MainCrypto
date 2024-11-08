from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from ..authentification.security import get_current_user, User
import httpx
import os
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

PREDICTION_API_URL = os.getenv("PREDICTION_API_URL", "http://prediction-api:3001/predict")

class PredictionResponse(BaseModel):
    prediction_date: datetime
    prediction_value: float

@router.get("/latest-prediction", response_model=PredictionResponse)
async def get_latest_prediction(current_user: User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PREDICTION_API_URL}/latest-prediction")
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.get("/model-evaluation")
async def get_latest_evaluation(current_user: User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PREDICTION_API_URL}/model-evaluation")
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.get("/best-model")
async def get_best_model(current_user: User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PREDICTION_API_URL}/best-model")
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.get("/models")
async def list_models(current_user: User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PREDICTION_API_URL}/models")
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.post("/train", status_code=status.HTTP_202_ACCEPTED)
async def trigger_training_dag(current_user: User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{PREDICTION_API_URL}/train")
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.post("/score", status_code=status.HTTP_202_ACCEPTED)
async def trigger_scoring_dag(current_user: User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{PREDICTION_API_URL}/score")
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.post("/predict", status_code=status.HTTP_202_ACCEPTED)
async def trigger_prediction_dag(current_user: User = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{PREDICTION_API_URL}/predict")
            response.raise_for_status()
            data = response.json()
            return data
        except httpx.HTTPError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
