import pandas as pd
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from datetime import datetime, timezone, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date':days_ago(0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize the DAG
dag = DAG(
    'crypto_ohlc_dag',
    default_args=default_args,
    description='A simple DAG to get daily OHLC data from Kraken API',
    schedule_interval=timedelta(days=1),  # timedelta(seconds=5, minutes=5, hours=1, days=1) for hourly runs
    catchup=False
)

# Function to get non-duplicate assets from PostgreSQL

def get_conn():
    """Airflow postgreSQL connection (must be pre param within Airflow GUI)
    """
    connection = BaseHook.get_connection('postgres_crypto')
    engine = create_engine(f'postgresql+psycopg2://{connection.login}:{connection.password}@{connection.host}:{connection.port}/{connection.schema}')
    return {
        "engine": engine,
        "schema": connection.schema
        }


def get_non_duplicate_assets():
    """Function to get non-duplicate assets from PostgreSQL
    Arguments:
        none -- _description_
    KeywordArguments:
        none -- _description_
    Raises:
        none -- _description_
    Returns:
        dataframe of existing assets in the database
    """
    # Airflow postgreSQL connection (must be pre param within Airflow GUI)
    conn = get_conn()
    
    # SQL query to get non-duplicate assets
    query = """
    SELECT *
	FROM public.assets;
    """
    df = pd.read_sql(query, conn['engine'])
    return list(df['asset'])

def get_ohlc_data(asset):
    """Function to get OHLC data from Kraken API and save to PostgreSQL
    Arguments:
        asset -- asset to get OHLC data for
    KeywordArguments:
        none -- _description_
    Raises:
        none -- _description_
    Returns:
        dataframe of existing assets in the database
    """
    # set today's date at midnight UTC
    current_datetime_utc = datetime.now(timezone.utc)
    # url of provider
    url = "https://api.kraken.com/0/public/Ticker?pair="+ asset
    payload = {}
    headers = {
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        result = response.json()['result'][asset]
        # https://docs.kraken.com/api/docs/rest-api/get-ticker-information
        for key in result:
            if isinstance(result[key], list):
                result[key] = result[key][0]
        # Create a DataFrame, rename and select mandatory columns
        df = pd.DataFrame([result])
        df.rename(columns={
            'o': 'open', 
            'h':'high',
            'l':'low',
            'c':'close',
            'v':'volume',
            't':'trades'
            }, 
            inplace=True
            )
        df = df[['open', 'high', 'low', 'close', 'volume', 'trades']]        
        # insert asset and today_midnight_utc        
        df.insert(0, 'asset', asset)
        df.insert(1, 'dtutc', current_datetime_utc)
        # convert columns to float
        columns_to_convert = ['open', 'high', 'low', 'close', 'volume', 'trades']
        df[columns_to_convert] = df[columns_to_convert].astype(float)
        conn = get_conn()
        df.to_sql('ohlc', conn['engine'], if_exists='append', index=False)

# Define the tasks
get_assets_task = PythonOperator(
    task_id='get_non_duplicate_assets',
    python_callable=get_non_duplicate_assets,
    dag=dag,
)

for asset in get_non_duplicate_assets():
    get_ohlc_task = PythonOperator(
        task_id=f'get_ohlc_data_{asset}',
        python_callable=get_ohlc_data,
        op_args=[asset],
        dag=dag,
    )
    get_assets_task >> get_ohlc_task