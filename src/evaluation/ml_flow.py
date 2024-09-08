import mlflow
from mlflow import MlflowClient
import time

def init_mlflow_experiment(exp_name):
    """
    Args :
    - exp_name (str) : Name of the MLflow experiment.

    Returns:
    ID of the existing or newly created MLflow experiment (str).
    """                
    # Link experiment and run
    experiment = mlflow.set_experiment(exp_name)    
        
    # Print the Experiment Name and Creation Date
    print("Experiment name: {}".format(exp_name))
    print("Timestamp creation: {}".format(experiment.creation_time), end= "\n\n")
    
    return experiment


def get_check_experiment(exp_name, tracking_uri):
    """
    Check if an experiment exist with an exp_name
    - args : exp_nam (str) : experience name
    return :
    experiment object
    """    
    client = MlflowClient(tracking_uri=tracking_uri) 
    # Vérify is experiment exist

    experiment = client.get_experiment_by_name(exp_name)
    
    if experiment is None:
        print(f"Aucune expérience trouvée avec le nom '{exp_name}'.")
        return None
    else:
        return experiment 
    
    
    
def get_best_model(exp_name, metric_name, ticker, period, tracking_uri, order='ASC'):
    """
    Fetch the best model from MLflow server based on a specific metric.

    Args:
    - exp_name (str) : Name of the MLflow experiment.
    - metric_name (str) : Metric used to compare models.
    - period (str) : Prediction period, e.g., '1 day' or '5 day'.
    - ticker (str) : Currency symbol, e.g., 'USD'.
    - tracking_uri (str) : HTTP address of the MLflow tracking server.
    - order (str, optional) : Order of the metrics. 'DESC' for descending (default) or 'ASC' for ascending.

    Returns:
    - dict : A dictionary containing information about the best model: id, params, metrics, and model path.
    """
    client = MlflowClient(tracking_uri = tracking_uri)
    
    try:
        # Obtain the experiment
        experiment = get_check_experiment(exp_name, tracking_uri)

        # Obtain experiment ID
        experiment_id = experiment.experiment_id

        # Search for the best run in the experiment
        runs = client.search_runs(experiment_id, order_by=[f"metrics.{metric_name} {order}"])
        
        if runs:
            
            print("runs :", len(runs))
            
            # Get the best model according to the metric
            best_run = runs[0]

            # Fetch information about the best model
            run_id = best_run.info.run_id
            params = best_run.data.params
            metrics = best_run.data.metrics
            model_path = best_run.info.artifact_uri + "/model"
            
            best_model_info = {
                "run_id": run_id,
                "params": params,
                "metrics": metrics,
                "model_path": model_path
            }
            
            print(f"Best model for currency {ticker} and a period of {period}:")
            print(f"Run id : {best_model_info['run_id']}")
            print(f"Params : {best_model_info['params']}")
            print(f"Metric value : {best_model_info['metrics']}")
            return best_model_info

        else:
            print("No runs found in the specified experiment.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        print("je suis là")
        return None
    

def load_best_model(exp_name, model_name, model_version, period, tracking_uri, metric_name = "mean_squarred_error_test", order='ASC'):
    #client
    client = MlflowClient(tracking_uri = tracking_uri)
             
    # Check and obtain experiment
    experiment = get_check_experiment(exp_name, tracking_uri)
            
    # Get experiment ID
    experiment_id = experiment.experiment_id
    
    # Search for all runs
    runs = client.search_runs(experiment_id, order_by=[f"metrics.{metric_name} {order}"])
        
    model_uri = f"models:/{model_name}/{model_version}"
    #model_uri = f"mlruns/{experiment_id}/{run_id}/artifacts/tf-lstm-reg-model-{period}"
        
    try:
        best_model = mlflow.tensorflow.load_model(model_uri =model_uri)        
    except mlflow.exceptions.MlflowException as e: 
        print(f"aucun modèle enregistré n'a été trouvé dans model_uri : {model_uri}. Erreur: {e}")
        best_model = None  # Retourner None ou une valeur par défaut en cas d'erreur
        
    return best_model