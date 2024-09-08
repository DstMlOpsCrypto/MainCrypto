from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import psycopg2
import requests
import os


# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize the DAG
dag = DAG(
    'crypto_ohlc_dag',
    default_args=default_args,
    description='A simple DAG to get OHLC data from Kraken API',
    schedule_interval=timedelta(minutes=1),  # timedelta(seconds=5, minutes=5, hours=1, days=1) for hourly runs
)

def get_engin_conn():
    engine = create_engine('postgresql://crypto:crypto@localhost:5432/cryptoDb')
    return engin

# Function to get non-duplicate assets from PostgreSQL
def get_non_duplicate_assets():
    engine = get_engin_conn()

    query = """
    SELECT DISTINCT asset
    FROM your_table
    """

    df = pd.read_sql(query, engine)
    return df

# Function to get OHLC data from Kraken API and save to PostgreSQL
def get_ohlc_data(asset):
    response = requests.get('https://api.kraken.com/0/public/OHLC?pair=XXBTZUSD')
    data = response.json()['result']['XXBTZUSD']
    df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
    df.insert(0, 'asset', 'XXBTZUSD')
    df.rename(columns={"time": "epoch"})
    ohcl = df[['asset', 'epoch', 'open', 'high', 'low','close', 'volume']]
    engine = get_engin_conn()
    ohcl.to_sql('ohlc', engine, index=False)


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
