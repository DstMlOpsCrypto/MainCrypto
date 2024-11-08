from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from airflow.utils.state import DagRunState
from custom_sensors import ExternalDagRunSensor


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 2,
    #'schedule_interval': None,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="prediction_dag",
    default_args=default_args,
    description="Un DAG pour lancer une prédiction du modèle",
    schedule_interval="@daily", #None,
    catchup=False,
    tags=['model', 'prediction'],

) as my_dag:

    wait_for_crypto_ohlc_dag = ExternalDagRunSensor(
        task_id='wait_for_crypto_ohlc_dag',
        external_dag_id='crypto_ohlc_dag',
        mode='reschedule',
        poke_interval=60,
        timeout=600,
    )

    predict_model = BashOperator(
        bash_command= " cd ../../app/scripts && python3 predict2.py --currency='BTC-USD'",
        task_id="prediction_model",
        dag=my_dag)

    wait_for_crypto_ohlc_dag >> predict_model