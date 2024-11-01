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

            # Log and register the model
            mlflow.tensorflow.log_model(
                model=model, 
                artifact_path="model", 
                registered_model_name="Bitcoin_LSTM_Model"
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
