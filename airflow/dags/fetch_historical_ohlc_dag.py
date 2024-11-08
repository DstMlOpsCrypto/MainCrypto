import pandas as pd
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_historical_ohlc',
    default_args=default_args,
    description='Fetch historical OHLC data for a given asset',
    schedule_interval=None,  # This DAG will be triggered manually
    catchup=False
)

def get_conn():
    connection = BaseHook.get_connection('postgres_crypto')
    engine = create_engine(
        f'postgresql+psycopg2://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}'
    )
    return {
        "engine": engine,
        "schema": connection.schema
    }

def fetch_historical_ohlc(**context):
    dag_run = context.get('dag_run')
    if dag_run and dag_run.conf:
        asset = dag_run.conf.get('asset')
        if not asset:
            raise ValueError("Asset not provided in dag_run.conf")
    else:
        raise ValueError("dag_run.conf is missing or empty")

    logging.info(f"Fetching OHLC data for asset: {asset}")

    interval = 1440  # Données journalières
    url = f"https://api.kraken.com/0/public/OHLC?pair={asset}&interval={interval}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['result']
        data_keys = [key for key in result.keys() if key != 'last']
        if not data_keys:
            raise Exception(f"No data keys found in response for asset {asset}")
        data_key = data_keys[0]
        logging.info(f"Using data key: {data_key}")
        data = result[data_key]
        if not data:
            logging.info("No data to insert.")
            return

        # Préparation des données
        df = pd.DataFrame(data, columns=[
            'time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'
        ])
        df = df.drop(columns=['vwap'])
        df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)
        df['asset'] = data_key
        df = df.rename(columns={'time': 'dtutc', 'count': 'trades'})
        df['dtutc'] = df['dtutc'].dt.tz_convert('UTC')

        # Conversion des types de colonnes
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        df['trades'] = df['trades'].astype(int)

        df = df[['asset', 'dtutc', 'open', 'high', 'low', 'close', 'volume', 'trades']]

        # Récupération des dates existantes pour l'actif
        conn_info = get_conn()
        engine = conn_info['engine']

        with engine.connect() as conn:
            query = "SELECT dtutc FROM ohlc WHERE asset = %s"
            result = conn.execute(query, (asset,))
            existing_dates = set(row[0] for row in result)

        logging.info(f"Found {len(existing_dates)} existing records for asset {asset}")

        # Filtrer les enregistrements déjà existants
        df = df[~df['dtutc'].isin(existing_dates)]

        if df.empty:
            logging.info("No new data to insert after filtering existing records.")
            return

        # Insertion des nouvelles données
        df.to_sql('ohlc', engine, if_exists='append', index=False)
        logging.info("Data inserted successfully.")
    else:
        raise Exception(f"Failed to fetch data: {response.text}")

fetch_historical_ohlc_task = PythonOperator(
    task_id='fetch_historical_ohlc_task',
    python_callable=fetch_historical_ohlc,
    dag=dag,
)
