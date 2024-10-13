#mlflow
import mlflow
from mlflow.tracking.client import MlflowClient

#PATH
# Récupérer le chemin du répertoire courant
current_dir = os.path.dirname(os.path.abspath(__file__))
# Naviguer vers le répertoire parent de 
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# Construire le chemin vers le répertoire `src`
src_dir = os.path.join(parent_dir, 'src')

#ajout du chemin
sys.path.append(current_dir)
sys.path.append(src_dir)
sys.path.append(parent_dir)

from src.evaluation.ml_flow import init_mlflow_experiment, load_best_model
from src.data.import_raw_data import load_transform_data2

#Arguments du script
parser = argparse.ArgumentParser(prog ='predict.py',description="Pipeline de prediction pour le projet MLops de prédiction des prix du bticoin")
parser.add_argument('--currency', choices= ['BTC-USD','BTC-EUR'], required=True, help="Selectionne la devise")
args = parser.parse_args()

# Update the tracking URI to point to the MLflow server container
tracking_uri = "postgresql://mlflow:mlflow@mlflow_db:5432/mlflow"
mlflow.set_tracking_uri(tracking_uri)
client = MlflowClient(tracking_uri=tracking_uri)

# get MLFlow experiment_id
exp_name = "Projet_Bitcoin_price_prediction"
experiment_id = init_mlflow_experiment(exp_name = exp_name)

#parameters
model_name = f"tf-lstm-reg-model-{period}"
model_version = "latest"


def pipeline():
    """
    Fonction which evaluate production model and send back score
    """
    # recupérer les arguments du scripts
    ticker = args.currency
    period='1d'

    # new_way
    #load_tranform data 2
    #X_test, df_index, scaler = load_transform_data2(table='ohlc',period=period)

    #old way
    #load_tranform data
    X_test, df_index, scaler = load_transform_data(ticker=ticker, period=period)

    #load best_model
    best_model = load_best_model(experiment_id=experiment_id,model_name =model_name, model_version = model_version, tracking_uri = tracking_uri)

    # make a prediction
    test_predict = best_model.predict(X_test)
    
    #scaling
    test_predict = test_predict/scaler.scale_[0]
    X_test = X_test/scaler.scale_[0]

    # TO BE DONE
    # TO BE DONE

    client = MlflowClient(tracking_uri = tracking_uri)

    return score_best_model    