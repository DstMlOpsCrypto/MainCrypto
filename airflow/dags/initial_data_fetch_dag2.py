import logging
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from fetch_historical_ohlc_dag import fetch_historical_ohlc

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
    description='Fetch missing OHLC data for XXBTZUSD upon application launch',
    schedule_interval=None,  # Run manually or once at startup
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

def get_missing_date_range(asset, **kwargs):
    conn = get_conn()
    query = f"SELECT MAX(dtutc) FROM ohlc WHERE asset = '{asset}';"
    result = conn['engine'].execute(query).fetchone()
    last_date_in_db = result[0]
    if last_date_in_db:
        start_date = (last_date_in_db + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        start_date = '2024-10-28'  # Date after the last date in the CSV for BTC
    end_date = datetime.now().strftime('%Y-%m-%d')
    logging.info(f"Missing data from {start_date} to {end_date}")
    kwargs['ti'].xcom_push(key='start_date', value=start_date)
    kwargs['ti'].xcom_push(key='end_date', value=end_date)
    return asset

def fetch_missing_data(**kwargs):
    asset = kwargs['ti'].xcom_pull(task_ids='get_missing_date_range')
    start_date = kwargs['ti'].xcom_pull(key='start_date', task_ids='get_missing_date_range')
    end_date = kwargs['ti'].xcom_pull(key='end_date', task_ids='get_missing_date_range')
    
    fetch_historical_ohlc(
        asset,
        **{
            'start_date': start_date,
            'end_date': end_date
        }
    )

get_missing_date_range_task = PythonOperator(
    task_id='get_missing_date_range',
    python_callable=get_missing_date_range,
    op_kwargs={'asset': 'XXBTZUSD'},
    provide_context=True,
    dag=dag,
)

fetch_missing_data_task = PythonOperator(
    task_id='fetch_missing_data',
    python_callable=fetch_missing_data,
    provide_context=True,
    dag=dag,
)

get_missing_date_range_task >> fetch_missing_data_task