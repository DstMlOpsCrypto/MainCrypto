#mlflow
import mlflow
print("MLflow version:", mlflow.__version__, end = "/n")

from mlflow.tracking.client import MlflowClient

#other packages
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

#import des modules
from src.data.make_dataset import make_dataset_for_testing
from src.data.import_raw_data import load_data, load_transform_data, load_transform_data2
from src.features.preprocess import normalize_data
from src.evaluation.ml_flow import get_check_experiment, load_best_model, init_mlflow_experiment

#supprimer warnings GPU tensorflow
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

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

exp_name = "Projet_Bitcoin_price_prediction"

# get MLFlow experiment_id
experiment_id = init_mlflow_experiment(exp_name = exp_name)

# recupérer les arguments du scripts
ticker = args.currency   
period='1d'

# Mise en place des nouveaux arguments
# bitcoin = args.bitcoin
# currency = args.currency
# ticker = bitcoin + currency

def pipeline_predict():
    """
    pipeline de commandes pour la prédiction de la valeur du lendemain d'un asset (paramètres ticker)
    """
    model_name = f"tf-lstm-reg-model-{period}"
    #model_name = f"tf-lstm-reg-model-{ticker}-{period}"
    model_version = "latest"

    #new_way
    #load_tranform
    #X_test, df_index, scaler = load_transform_data2(table='ohlc',period=period)
 
    #Récupération des données
    data, df_index, scaler = load_transform_data(ticker=ticker, period=period)
    
    print('data shape :', data.shape)

    try:
        #Création du dataset de test
        X_test = make_dataset_for_testing(data, pas_temps=14)
        print("X_test: ", X_test)
        print("X_test_shape: ", X_test.shape)
    except Exception as e:
        print(e)
        print ("Le chargement des données de test a échoué")
    
    #modif old way
    #df_array = load_transform_data(ticker=ticker, period=period)

    #load best_model
    best_model = load_best_model(experiment_id=experiment_id,model_name =model_name, model_version = model_version, tracking_uri = tracking_uri)
        
    #prediction
    test_predict = best_model.predict(X_test)
    
    #scaling
    test_predict = test_predict/scaler.scale_[0]
    X_test = X_test/scaler.scale_[0]    

    print("test_predict :", test_predict)
    print("test_predict shape", test_predict.shape)

    prediction = int(test_predict[-1,0])
    
    print(f"La valeur du Bitcoin était de {int(X_test[-1,0])} {ticker} hier à la fermeture. Le modèle prédit une valeur de {prediction} {ticker} pour aujourd'hui")

    return {"prediction": prediction}

if __name__ == "__main__":
    prediction = pipeline_predict()







