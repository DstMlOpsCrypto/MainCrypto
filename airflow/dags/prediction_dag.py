from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 2,
    'schedule_interval': None,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="prediction_dag",
    default_args=default_args,
    description="Un DAG pour lancer une prédiction du modèle",
    schedule_interval=None,
    catchup=False,
    tags=['model', 'prediction'],

) as my_dag:

    prediction_task = BashOperator(
        bash_command= " cd ../../app/scripts && python3 predict2.py --currency='BTC-USD'",
        task_id="prediction_model",
        dag=my_dag)

    evaluate_model = BashOperator(
        task_id="evaluate_model",
        bash_command= " cd ../../app/scripts && python3 evaluate_model2.py --currency='BTC-USD'",
        do_xcom_push=True,
        dag=my_dag
    )
     
    prediction_task  >> evaluate_model 