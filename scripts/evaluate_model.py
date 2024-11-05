#mlflow
import mlflow
from mlflow.tracking.client import MlflowClient

#packages
import argparse
import sys
import os

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
from src.data.import_raw_data import load_transform_data, load_transform_data2
from src.features.preprocess import normalize_data,normalize_data2
from src.data.make_dataset import make_dataset
from src.data.import_raw_data import load_data, load_data_2
from src.evaluation.evaluate import scaling, score

#Arguments du script
parser = argparse.ArgumentParser(prog ='predict.py',description="Pipeline de prediction pour le projet MLops de prédiction des prix du bticoin")
parser.add_argument('--currency', choices= ['BTC-USD','BTC-EUR'], required=True, help="Selectionne la devise")

#parser.add_argument('--bitcoin', choices= ['BTC'], required=True, help="Selectionne le bitcoin")
#parser.add_argument('--currency', choices= ['-USD','-EUR'], required=True, help="Selectionne la devise")

#parser.add_argument('--period', choices= ['1d','5d'], required=True, help="Selectionne la période de prédiction") # on garde une prédiction à un jour

args = parser.parse_args()

# Update the tracking URI to point to the MLflow server container
tracking_uri = "postgresql://mlflow:mlflow@mlflow_db:5432/mlflow"
mlflow.set_tracking_uri(tracking_uri)
client = MlflowClient(tracking_uri=tracking_uri)

# get MLFlow experiment_id
exp_name = "Projet_Bitcoin_price_prediction"
experiment_id = init_mlflow_experiment(exp_name = exp_name)

model_version = "latest"

def pipeline():
    """
    Fonction which evaluate production model and send back score
    """

    print("je suis entré dans le pipeline")

    # recupérer les arguments du scripts
    ticker = args.currency
    period='1d'

    
    # bitcoin = args.bitcoin
    # currency = args.currency    
    # ticker = bitcoin + currency

    model_name = f"tf-lstm-reg-model-{period}"
    # model_name = f"tf-lstm-reg-model-{ticker}-{period}"

    model_version = "latest"

    #old_way       
    # Data loading 
    try:
        # Data loading 
        df = load_data(ticker=ticker, start = "2014-07-01", end = "2024-08-01", interval = period, start_new_data = "2024-08-01")
        print("Chargement des données yfinance effectué")
        # Data Normalization
        df_array, df.index, scaler = normalize_data(df= df, period=period)
        print("Normalisation des données effectuée") 
    
    except Exception as e:
        print(e)
        print("Le chargement des données yfinance a échoué")

     # new_way
    #load_tranform data 2
    #X_test, df_index, scaler = load_transform_data2(table='ohlc',period=period)

    # Building dataset for computing score
    pas_temps = 5
    X_train, X_test, y_train, y_test= make_dataset(data = df_array, pas_temps=pas_temps, test_size=0.3)
    
    #load best_model
    best_model = load_best_model(experiment_id=experiment_id,model_name =model_name, model_version = model_version, tracking_uri = tracking_uri)
  
    # Prediction
    train_predict = best_model.predict(X_train)
    test_predict = best_model.predict(X_test)

    # Scaling
    train_predict, test_predict, y_train, y_test = scaling(train_predict, test_predict, y_train, y_test, scaler)
                        
    #scores mse et r2
    mse_train, r2_score_train, mse_test, r2_score_test = score(train_predict = train_predict, test_predict= test_predict, y_train = y_train, y_test = y_test)
    # on se base au final sur la métrique mean_squared_error_test calculé sur l'éch. de test (mse_test)     

    print("mse_test",mse_test)
    print("r2_score_test :", r2_score_test)

    return {"mse_test": mse_test, "r2_score_test": r2_score_test} 

if __name__ == "__main__":
        pipeline()