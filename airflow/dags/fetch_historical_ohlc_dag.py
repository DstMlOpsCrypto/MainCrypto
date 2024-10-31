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
    description='Fetch historical OHLC data for a given asset and date range',
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
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')
    logging.info(f"Fetching OHLC data for asset: {asset} from {start_date} to {end_date}")
    # Convert dates to Unix timestamps
    since = int(datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
    until = int(datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
    interval = 1440  # Daily data
    url = f"https://api.kraken.com/0/public/OHLC?pair={asset}&interval={interval}&since={since}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()['result']
        data_keys = [key for key in result.keys() if key != 'last']
        if not data_keys:
            raise Exception(f"No data keys found in response for asset {asset}")
        data_key = data_keys[0]
        logging.info(f"Using data key: {data_key}")
        data = result[data_key]
        # Filter data up to 'until' timestamp
        data = [row for row in data if int(row[0]) <= until]
        if not data:
            logging.info("No new data to insert.")
            return
        df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
        df = df.drop(columns=['vwap'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df['asset'] = data_key
        df = df.rename(columns={'time': 'dtutc', 'count': 'trades'})
        # Convert columns to appropriate types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        df['trades'] = df['trades'].astype(int)
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
    op_kwargs={
        'asset': '{{ dag_run.conf["asset"] }}',
        'start_date': '{{ dag_run.conf["start_date"] }}',
        'end_date': '{{ dag_run.conf["end_date"] }}',
    },
    dag=dag,
)