# app/prediction/router.py

from fastapi import APIRouter, HTTPException, Path, Query, status, Body
import requests
from requests.auth import HTTPBasicAuth
import os
import pandas as pd
import mlflow
import logging
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import numpy as np
import joblib
from prometheus_client import Counter, Gauge
from app.registry import registry, PREDICTION_COUNT, MODEL_SCORE



router = APIRouter()
logger = logging.getLogger(__name__)

def get_db():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'crypto'),
        password=os.getenv('DB_PASSWORD', 'crypto'),
        dbname=os.getenv('DB_NAME', 'cryptoDb')
    )
    return conn


class InputData(BaseModel):
    data: List[float]  # A list of floats with length 14

# MLflow configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000")
# Set the tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Airflow API URL
AIRFLOW_API_URL = "http://airflow-webserver:8080/api/v1"

# Airflow credentials (consider using environment variables for security)
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "airflow")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "airflow")



@router.get("/latest-prediction", summary="Get the latest prediction")
async def get_latest_prediction():
    PREDICTION_COUNT.inc()
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
            SELECT prediction_date, prediction_value
            FROM predictions
            ORDER BY prediction_date DESC
            LIMIT 1;
            """
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return {
                    "prediction_date": result['prediction_date'].isoformat(),
                    "prediction_value": float(result['prediction_value'])
                }
            else:
                raise HTTPException(status_code=404, detail="No predictions found")
    except Exception as e:
        logger.error(f"Error retrieving prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@router.get("/model-evaluation", summary="Get the latest model evaluation metrics")
async def get_latest_evaluation():
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
            SELECT evaluation_date, mse_train, r2_score_train, mse_test, r2_score_test
            FROM model_evaluation
            ORDER BY evaluation_date DESC
            LIMIT 1;
            """
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                MODEL_SCORE.set(float(result['r2_score_test']))
                return {
                    "evaluation_date": result['evaluation_date'].isoformat(),
                    "mse_train": float(result['mse_train']),
                    "r2_score_train": float(result['r2_score_train']),
                    "mse_test": float(result['mse_test']),
                    "r2_score_test": float(result['r2_score_test'])
                }
            else:
                raise HTTPException(status_code=404, detail="No evaluation metrics found")
    except Exception as e:
        logger.error(f"Error retrieving evaluation metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/best-model", summary="Get the best model based on evaluation metrics")
async def get_best_model():
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # Modify the query based on your criteria for "best"
            query = """
            SELECT model_name, model_version, evaluation_date, mse_train, r2_score_train, mse_test, r2_score_test
            FROM model_evaluation
            ORDER BY mse_test ASC  -- Assuming lower mse_test is better
            LIMIT 1;
            """
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return {
                    "model_name": result['model_name'],
                    "model_version": result['model_version'],
                    "evaluation_date": result['evaluation_date'].isoformat(),
                    "mse_train": float(result['mse_train']),
                    "r2_score_train": float(result['r2_score_train']),
                    "mse_test": float(result['mse_test']),
                    "r2_score_test": float(result['r2_score_test'])
                }
            else:
                raise HTTPException(status_code=404, detail="No evaluation metrics found")
    except Exception as e:
        logger.error(f"Error retrieving best model: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/models", summary="List available models")
async def list_models():
    try:
        client = mlflow.tracking.MlflowClient()
        # Get all registered models
        registered_models = client.search_registered_models()
        models = []
        for rm in registered_models:
            model_info = {
                "name": rm.name,
                "latest_versions": []
            }
            # Obtenir les versions via search_model_versions
            versions = client.search_model_versions(f"name='{rm.name}'")
            for mv in versions:
                model_info["latest_versions"].append({
                    "version": mv.version,
                    "stage": mv.current_stage,
                    "description": mv.description,
                    "run_id": mv.run_id
                })
            models.append(model_info)
        return {"models": models}
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))



def trigger_dag(dag_id: str):
    url = f"{AIRFLOW_API_URL}/dags/{dag_id}/dagRuns"
    response = requests.post(
        url,
        auth=HTTPBasicAuth(AIRFLOW_USERNAME, AIRFLOW_PASSWORD),
        json={},  # Empty JSON payload
    )
    if response.status_code == 200:
        return {"message": f"DAG {dag_id} triggered successfully"}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Failed to trigger DAG {dag_id}: {response.text}",
        )

@router.post("/train", status_code=status.HTTP_202_ACCEPTED)
async def trigger_training_dag():
    return trigger_dag("training_dag")

@router.post("/score", status_code=status.HTTP_202_ACCEPTED)
async def trigger_scoring_dag():
    return trigger_dag("scoring_model_dag")

@router.post("/predict", status_code=status.HTTP_202_ACCEPTED)
async def trigger_prediction_dag():
    return trigger_dag("prediction_dag")
