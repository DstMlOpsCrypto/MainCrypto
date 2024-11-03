from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

#from airflow.providers.docker.operators.docker import DockerOperator
#from airflow.operators.python import PythonOperator

# from airflow.models import Variable
# from airflow.utils.task_group import TaskGroup


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 2,
    'schedule_interval': None,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id="training_dag_2",
    default_args=default_args,
    description="Un DAG pour lancer l'entrainement du modèle",
    schedule_interval=None,
    catchup=False,
    tags=['model', 'training'],

) as my_dag:

    # train_model = PythonOperator(
    #         task_id='training_model,
    #     #         op_kwargs={'n_files': 20, 'filename': 'data.csv'},
    #         dag=my_dag)

    train_model = BashOperator(
        bash_command= " cd ../../app/scripts && python3 train2.py --currency='BTC-USD'",
        task_id="training_model",
        dag=my_dag)