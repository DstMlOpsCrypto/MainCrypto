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
from src.features.preprocess import normalize_data2
from src.data.make_dataset import make_dataset
from src.data.import_raw_data import load_data_2
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

# recupérer les arguments du scripts
ticker = args.currency   
period='1d'
pas_temps=3

# bitcoin = args.bitcoin
    # currency = args.currency    
    # ticker = bitcoin + currency
def pipeline():
    """
    Fonction which evaluate production model and send back score
    """

    print("je suis entré dans le pipeline")

    model_name = f"tf-lstm-reg-model-{period}"
    #model_name = f"tf-lstm-reg-model-{ticker}-{period}"
    model_version = "latest"

    try:
        # Data loading 
        df = load_data_2(table='ohlc')
        print("Chargement des données KRAKEN effectué")
        # Data Normalization
        df_array, df.index, scaler = normalize_data2(df= df, period=period)
        print("Normalisation des données effectuée")
      
    except Exception as e:
        print(f"Error loading data: {e}") 
        print("Le chargement ou la normalisation des données Kraken a échoué")


    # Building dataset for computing score
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
    score = pipeline()