#packages
import argparse
import sys
import os
import subprocess

#mlflow
import mlflow
from mlflow.tracking import MlflowClient

# CLI parameters
parser = argparse.ArgumentParser(prog ='main.py',description="Pipeline d'exécution pour le projet MLops de prédiction des prix du bticoin")
parser.add_argument('--currency', choices= ['BTC-USD','BTC-EUR'], required=True, help="Selectionne la devise")
parser.add_argument('--period', choices= ['1d','5d','1wk'], required=True, help="Selectionne la période de prédiction")
args = parser.parse_args()


exp_name = "Projet_Bitcoin_price_prediction"
tracking_uri = "http://0.0.0.0:5000"


# MLflow Tracking client
client = MlflowClient(tracking_uri= tracking_uri)

# Set your MLflow experiment
mlflow.set_experiment(exp_name)


def pipeline():
    
    # recupérer les arguments du scripts
    ticker = args.currency
    period = args.period
        
    # Get the latest version of the model from MLflow
    model_name = f"tf-lstm-reg-model-{period}"
    model_version = "latest"
    best_model = load_best_model(period = period, exp_name = exp_name, model_name =model_name, model_version = model_version, tracking_uri = tracking_uri)
        
    # model_version = client.get_latest_versions(name="your-model-name", stages=["Production"])[0].version

    # Build the Docker image
    image_name = "python:3.12.4"
    model_version = "latest"
    subprocess.run(["docker", "build", "-t", image_name, "--build-arg", f"MODEL_VERSION={model_version}", "."])


    # Tag the Docker image
    image_tag = f"{image_name}:{model_version}" 
    subprocess.run(["docker", "tag", image_name, image_tag])

    # Push the Docker image to a registry (optional)
    subprocess.run(["docker", "push", image_tag])

    # Deploy the Docker container (this will depend on your specific deployment environment)
    # For example, if you're using Kubernetes, you might use the `kubectl` command to deploy the container


if __name__ == "__mai
