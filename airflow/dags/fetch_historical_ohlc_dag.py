import pandas as pd
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from datetime import datetime, timezone, timedelta
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
    description='Fetch historical OHLC data for a newly created asset',
    schedule_interval=None,  # This DAG will be triggered manually
    catchup=False
)

def get_conn():
    connection = BaseHook.get_connection('postgres_crypto')
    engine = create_engine(f'postgresql+psycopg2://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}')
    return {
        "engine": engine,
        "schema": connection.schema
    }

def fetch_historical_ohlc(asset, **kwargs):
    import logging
    logging.info(f"Fetching OHLC data for asset: {asset}")
    url = f"https://api.kraken.com/0/public/OHLC?pair={asset}&interval=1440"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['result']
        # Exclude 'last' key and get the actual data key
        data_keys = [key for key in result.keys() if key != 'last']
        if not data_keys:
            raise Exception(f"No data keys found in response for asset {asset}")
        data_key = data_keys[0]
        logging.info(f"Using data key: {data_key}")
        data = result[data_key]

        # Include all 8 columns when creating the DataFrame
        df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        
        # Drop the 'vwap' column since it's not in your database
        df = df.drop(columns=['vwap'])

        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['asset'] = data_key  # Use the actual data key
        df = df.rename(columns={'time': 'dtutc', 'count': 'trades'})
        
        # Convert columns to appropriate types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        df['trades'] = df['trades'].astype(int)
        
        # Reorder columns to match your database table
        df = df[['asset', 'dtutc', 'open', 'high', 'low', 'close', 'volume', 'trades']]
        
        # Save to database
        conn = get_conn()
        df.to_sql('ohlc', conn['engine'], if_exists='append', index=False)
    else:
        raise Exception(f"Failed to fetch data: {response.text}")

# Define the task
fetch_historical_ohlc_task = PythonOperator(
    task_id='fetch_historical_ohlc_task',
    python_callable=fetch_historical_ohlc,
    op_kwargs={'asset': '{{ dag_run.conf["asset"] }}'},
    dag=dag,
)