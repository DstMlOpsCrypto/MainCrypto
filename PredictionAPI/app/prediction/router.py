from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import mlflow
from mlflow import MlflowClient
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import joblib
import json
from sklearn.metrics import mean_squared_error, mean_absolute_error

@contextmanager
def get_db():
    conn = psycopg2.connect(
        dbname="cryptoDb",
        user="crypto",
        password="crypto",
        host="db",
        port="5432"
    )
    try:
        yield conn.cursor(cursor_factory=RealDictCursor)
    finally:
        conn.close()


router = APIRouter()

class TrainRequest(BaseModel):
    asset: str
    epochs: int = 10
    batch_size: int = 32
    pas_temps: int = 14  # Time steps
    neurons: int = 50  # Number of neurons in LSTM layer

class TrainResponse(BaseModel):
    asset: str
    training_date: datetime
    duration_seconds: float
    metrics: dict
    message: str




class PredictionRequest(BaseModel):
    asset: str

class PredictionResponse(BaseModel):
    asset: str
    prediction_date: datetime
    predicted_price: float
    message: str




class EvaluationRequest(BaseModel):
    asset: str
    metrics: list = ['mean_squared_error']

class EvaluationResponse(BaseModel):
    asset: str
    evaluation_date: datetime
    metrics: dict
    message: str



def load_data_from_db(asset: str):
    """
    Load historical data for the given asset from the PostgreSQL database.
    """
    import pandas as pd

    with get_db() as cursor:
        query = """
            SELECT dtutc, close
            FROM ohlc
            WHERE asset = %s
            ORDER BY dtutc ASC;
        """
        cursor.execute(query, (asset,))
        result = cursor.fetchall()

    if not result:
        raise ValueError(f"No data found for asset {asset}")

    df = pd.DataFrame(result)
    df['dtutc'] = pd.to_datetime(df['dtutc'])
    df.set_index('dtutc', inplace=True)
    return df


def preprocess_data(df):
    """
    Preprocess the data by scaling the 'close' prices using MinMaxScaler.
    """
    data = df['close'].values.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler

def create_dataset(data, pas_temps):
    X, y = [], []
    for i in range(pas_temps, len(data)):
        X.append(data[i - pas_temps:i, 0])
        y.append(data[i, 0])
    X, y = np.array(X), np.array(y)
    # Reshape to (samples, time steps, features)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y






# Exemple de requête pour train
# curl -X POST "http://localhost:3001/train" \
#   -H "Content-Type: application/json" \
#   -d '{
#       "asset": "XXBTZUSD",
#       "epochs": 5,
#       "batch_size": 32,
#       "pas_temps": 14,
#       "neurons": 50
#   }'

@router.post("/train", response_model=TrainResponse)
async def train_model(request: TrainRequest):
    try:
        start_time = time.time()
        asset = request.asset.upper()
        epochs = request.epochs
        batch_size = request.batch_size
        pas_temps = request.pas_temps
        neurons = request.neurons

        # Set MLflow tracking URI
        mlflow.set_tracking_uri("http://mlflow-server:5000")
        client = MlflowClient()

        # Start MLflow run
        with mlflow.start_run(run_name=f"Training {asset}") as run:
            # Log parameters
            mlflow.log_params({
                "asset": asset,
                "epochs": epochs,
                "batch_size": batch_size,
                "pas_temps": pas_temps,
                "neurons": neurons
            })

            # Load historical data
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = '2014-07-01'  # Start date can be adjusted
            df = load_data_from_db(asset)

            # Preprocess the data
            scaled_data, scaler = preprocess_data(df)

            # Create training dataset
            X, y = create_dataset(scaled_data, pas_temps)

            # Split into training and testing sets
            split = int(0.8 * len(X))
            X_train, X_test = X[:split], X[split:]
            y_train, y_test = y[:split], y[split:]

            # Build the model
            model = Sequential()
            model.add(LSTM(neurons, return_sequences=False, input_shape=(X_train.shape[1], 1)))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mean_squared_error')

            # Train the model
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test, y_test), verbose=1)

            # Evaluate the model
            train_loss = history.history['loss'][-1]
            val_loss = history.history['val_loss'][-1]

            # Log metrics
            mlflow.log_metrics({
                "train_loss": train_loss,
                "val_loss": val_loss
            })

            # Save the scaler
            scaler_path = "scaler.pkl"
            joblib.dump(scaler, scaler_path)
            mlflow.log_artifact(scaler_path)

            # Save pas_temps
            params = {'pas_temps': pas_temps}
            params_path = "params.json"
            with open(params_path, 'w') as f:
                json.dump(params, f)
            mlflow.log_artifact(params_path)

            # Log and register the model
            mlflow.keras.log_model(
                model=model, 
                artifact_path="model", 
                registered_model_name=f"{asset}_LSTM_Model"
            )


            # Get the run ID
            run_id = run.info.run_id

            # Transition the model to 'Production'
            client = MlflowClient()
            model_name = f"{asset}_LSTM_Model"
            # Find the model version corresponding to the current run
            model_versions = client.search_model_versions(f"name='{model_name}'")
            model_version = None
            for mv in model_versions:
                if mv.run_id == run_id:
                    model_version = mv.version
                    break

            if model_version is None:
                raise Exception("Model version not found.")

            client.transition_model_version_stage(
                name=model_name,
                version=model_version,
                stage="Production"
            )

            duration_seconds = time.time() - start_time

            message = f"Training completed for {asset} in {duration_seconds:.2f} seconds."

            return TrainResponse(
                asset=asset,
                training_date=datetime.now(),
                duration_seconds=duration_seconds,
                metrics={
                    "train_loss": train_loss,
                    "val_loss": val_loss
                },
                message=message
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Exemple de requête pour predict
# curl -X POST "http://localhost:3001/predict" \
#  -H "Content-Type: application/json" \
#  -d '{
#      "asset": "XXBTZUSD"
#  }'

@router.post("/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    try:
        asset = request.asset.upper()
        mlflow.set_tracking_uri("http://mlflow-server:5000")
        client = MlflowClient()

        # Load the latest production model for the asset
        model_name = f"{asset}_LSTM_Model"
        latest_versions = client.get_latest_versions(name=model_name, stages=['Production'])
        if not latest_versions:
            raise HTTPException(status_code=404, detail=f"No production model found for asset {asset}")

        model_version_details = latest_versions[0]
        run_id = model_version_details.run_id

        # Load the model
        model_uri = f"models:/{model_name}/Production"
        model = mlflow.keras.load_model(model_uri)

        # Download artifacts
        scaler_path = client.download_artifacts(run_id=run_id, path="scaler.pkl")
        params_path = client.download_artifacts(run_id=run_id, path="params.json")

        # Load the scaler
        scaler = joblib.load(scaler_path)

        # Load pas_temps
        with open(params_path, 'r') as f:
            params = json.load(f)
        pas_temps = params['pas_temps']

        # Load latest pas_temps data points for the asset
        df = load_data_from_db(asset)
        if len(df) < pas_temps:
            raise HTTPException(status_code=400, detail=f"Not enough data to make prediction. Required: {pas_temps}, Available: {len(df)}")

        # Get the last pas_temps data points
        df_recent = df.iloc[-pas_temps:]
        # Preprocess the data
        data = df_recent['close'].values.reshape(-1, 1)
        scaled_data = scaler.transform(data)

        # Create input sequence
        X_input = np.reshape(scaled_data, (1, pas_temps, 1))

        # Make prediction
        prediction_scaled = model.predict(X_input)

        # Inverse transform the prediction
        prediction = scaler.inverse_transform(prediction_scaled)

        predicted_price = float(prediction[0][0])
        prediction_date = datetime.now()

        message = f"Prediction for {asset} on {prediction_date}: {predicted_price}"

        return PredictionResponse(
            asset=asset,
            prediction_date=prediction_date,
            predicted_price=predicted_price,
            message=message
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# Exemple de requête pour evaluate
# curl -X POST "http://localhost:3001/evaluate" \
#  -H "Content-Type: application/json" \
#  -d '{
#      "asset": "XXBTZUSD",
#      "metrics": ["mean_squared_error", "mean_absolute_error"]
#  }'

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_model(request: EvaluationRequest):
    try:
        asset = request.asset.upper()
        mlflow.set_tracking_uri("http://mlflow-server:5000")
        client = MlflowClient()

        # Load the latest production model for the asset
        model_name = f"{asset}_LSTM_Model"
        latest_versions = client.get_latest_versions(name=model_name, stages=['Production'])
        if not latest_versions:
            raise HTTPException(status_code=404, detail=f"No production model found for asset {asset}")

        model_version_details = latest_versions[0]
        run_id = model_version_details.run_id

        # Load the model
        model_uri = f"models:/{model_name}/Production"
        model = mlflow.keras.load_model(model_uri)

        # Download artifacts
        scaler_path = client.download_artifacts(run_id=run_id, path="scaler.pkl")
        params_path = client.download_artifacts(run_id=run_id, path="params.json")

        # Load the scaler
        scaler = joblib.load(scaler_path)

        # Load pas_temps
        with open(params_path, 'r') as f:
            params = json.load(f)
        pas_temps = params['pas_temps']

        # Load data
        df = load_data_from_db(asset)
        scaled_data, _ = preprocess_data(df)

        # Create dataset
        X, y = create_dataset(scaled_data, pas_temps)

        # Split into training and testing sets
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        # Make predictions on test set
        y_pred_scaled = model.predict(X_test)

        # Inverse transform predictions and actual values
        y_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
        y_true = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

        # Compute metrics
        metrics = {}
        if 'mean_squared_error' in request.metrics:
            mse = mean_squared_error(y_true, y_pred)
            metrics['mean_squared_error'] = mse
        if 'mean_absolute_error' in request.metrics:
            mae = mean_absolute_error(y_true, y_pred)
            metrics['mean_absolute_error'] = mae

        evaluation_date = datetime.now()
        message = f"Evaluation completed for {asset}"

        return EvaluationResponse(
            asset=asset,
            evaluation_date=evaluation_date,
            metrics=metrics,
            message=message
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
