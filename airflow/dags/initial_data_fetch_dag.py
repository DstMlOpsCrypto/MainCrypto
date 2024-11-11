import logging
import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'initial_data_fetch_dag',
    default_args=default_args,
    description='Fetch OHLC data for XXBTZUSD from 2024-10-28',
    schedule_interval=None,  # Exécuter manuellement ou une seule fois au démarrage
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=60)
)

def get_conn():
    connection = BaseHook.get_connection('postgres_crypto')
    engine = create_engine(
        f'postgresql+psycopg2://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}'
    )
    return {"engine": engine, "schema": connection.schema}

def fetch_data(**kwargs):
    asset = 'XXBTZUSD'
    interval = 1440  # Données journalières
    start_date = datetime(2024, 10, 28)
    since_timestamp = int(start_date.timestamp())

    logging.info(f"Fetching data since timestamp {since_timestamp}")

    url = 'https://api.kraken.com/0/public/OHLC'
    params = {
        'pair': asset,
        'interval': interval,
        'since': since_timestamp
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['error']:
        raise Exception(f"Error fetching data from Kraken API: {data['error']}")
    result = data['result']
    ohlc_data = result[asset]

    conn_info = get_conn()
    engine = conn_info['engine']

    # Processus des données et insertion dans la base de données
    with engine.connect() as conn:
        for entry in ohlc_data:
            timestamp = int(entry[0])
            dtutc = datetime.utcfromtimestamp(timestamp)
            open_price = float(entry[1])
            high_price = float(entry[2])
            low_price = float(entry[3])
            close_price = float(entry[4])
            vwap = float(entry[5])
            volume = float(entry[6])
            trades = int(entry[7])

            # Insertion dans la base de données
            query = """
            INSERT INTO ohlc (asset, dtutc, open, high, low, close, volume, trades)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """
            conn.execute(query, (asset, dtutc, open_price, high_price, low_price, close_price, volume, trades))

task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    provide_context=True,
    dag=dag,
)
