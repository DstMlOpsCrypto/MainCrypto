
# ajouter le chemin d'accès à MLflow à la variable d'environnement PYTHONPATH 
import os
#os.environ['PYTHONPATH'] = '/home/airflow/.local/lib/python3.12/site-packages'
#print(os.environ['PYTHONPATH'])

import sys
sys.path.append('/home/airflow/.local/lib/python3.12/site-packages')

#mlflow
import mlflow
from mlflow.tracking.client import MlflowClient
#other packages
import argparse
from datetime import datetime, timedelta

#airflow
from airflow import DAG
#from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

#from airflow.providers.docker.operators.docker import DockerOperator
# from airflow.models import Variable
# from airflow.utils.task_group import TaskGroup


#PATH
# Récupérer le chemin du répertoire courant (repertoire dags de Airflow)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Récupérer le répertoire parent (Airflow)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Récupérer le répertoire gd-parent (Racine du projet)
grand_parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

# Construire le chemin vers le répertoire scripts
src_dir = os.path.join(parent_dir, 'scripts')

#ajout des chemins
sys.path.append(current_dir)
sys.path.append(parent_dir)
sys.path.append(grand_parent_dir)
sys.path.append(script_dir)

#import des modules
from scripts.train import pipeline_train

#Arguments du script
# parser = argparse.ArgumentParser(prog ='predict.py',description="Pipeline d'entraînement pour le projet MLops de prédiction des prix du bitcoin")
# parser.add_argument('--currency', choices= ['BTC-USD','BTC-EUR'], required=True, help="Selectionne la devise")
#parser.add_argument('--bitcoin', choices= ['BTC'], required=True, help="Selectionne le bitcoin")
#parser.add_argument('--currency', choices= ['-USD','-EUR'], required=True, help="Selectionne la devise")
#parser.add_argument('--period', choices= ['1d','5d'], required=True, help="Selectionne la période de prédiction") # on garde une prédiction à un jour
# args = parser.parse_args()

# paramètres mlflow
exp_name = "Projet_Bitcoin_price_prediction"
run_name = "first_run"

tracking_uri = "postgresql://mlflow:mlflow@mlflow_db:5432/mlflow"
mlflow.set_tracking_uri(tracking_uri)

#paramètre du modèle
neurons = 350

# MLflow Tracking client
client = MlflowClient(tracking_uri= tracking_uri)

# Initialize MLFlow experiment
experiment_id = init_mlflow_experiment(exp_name)

# paramètre du modèle
period='1d'

#Paramètre de lancement du script
param_training = {'currency':'BTC-USD'},

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 2,
    'schedule_interval': None,
    'retry_delay': timedelta(minutes=2),
}

def pipeline_train_task(**kwargs):
    ticker = kwargs['currency']
    pipeline_train()

with DAG(
    dag_id="training_model_dag",
    default_args=default_args,
    description="Un DAG pour lancer l'entrainement du modèle",
    schedule_interval=None,
    catchup=False,
    tags=['model', 'training'],

) as my_dag:
    train_model = PythonOperator(
    task_id = 'training_model',
    python_callable = pipeline_train_task,
    op_kwargs = param_training,
             dag = my_dag)

