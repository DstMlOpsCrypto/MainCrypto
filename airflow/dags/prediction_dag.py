from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.utils.dates import days_ago
# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
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
        task_id="prediction_model",
        bash_command= " cd ../../app/scripts && python3 predict2.py --currency='BTC-USD' --asset='XXBTZUSD'",
        dag=my_dag
    )

    evaluate_model = BashOperator(
        task_id="evaluate_model",
        bash_command= " cd ../../app/scripts && python3 evaluate_model2.py --currency='BTC-USD' --asset='XXBTZUSD'",
        do_xcom_push=True,
        dag=my_dag
    )

    wait_for_crypto_ohlc_dag >> predict_model >> evaluate_model 
