#mlflow
import mlflow
print("MLflow version:", mlflow.__version__, end = "/n")

from mlflow.tracking.client import MlflowClient

#other packages
import argparse
import sys
import os
import numpy as np
import psycopg2
from datetime import datetime

def save_prediction_to_db(date, value):
    conn = get_db()  # Function to get a database connection
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO predictions (prediction_date, prediction_value) VALUES (%s, %s);"
            cursor.execute(query, (date, value))
            conn.commit()
    except Exception as e:
        print(f"Error saving prediction to database: {e}")
    finally:
        conn.close()

def get_db():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'crypto'),
        password=os.getenv('DB_PASSWORD', 'crypto'),
        dbname=os.getenv('DB_NAME', 'cryptoDb')
    )
    return conn

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
from src.data.import_raw_data import load_data_2
from src.features.preprocess import normalize_data2
from src.evaluation.ml_flow import get_check_experiment, load_best_model, init_mlflow_experiment

#supprimer warnings GPU tensorflow
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

#Arguments du script
parser = argparse.ArgumentParser(prog ='predict.py',description="Pipeline de prediction pour le projet MLops de prédiction des prix du bticoin")
parser.add_argument('--currency', choices= ['BTC-USD','BTC-EUR'], required=True, help="Selectionne la devise")
parser.add_argument('--asset', required=True, help="Sélectionne le nom de la paire correspondante dans la table ohlc")

#parser.add_argument('--bitcoin', choices= ['BTC'], required=True, help="Selectionne le bitcoin")
#parser.add_argument('--currency', choices= ['-USD','-EUR'], required=True, help="Selectionne la devise")
#parser.add_argument('--period', choices= ['1d','5d'], required=True, help="Selectionne la période de prédiction") # on garde une prédiction à un jour
args = parser.parse_args()


# Update the tracking URI to point to the MLflow server container
#tracking_uri = "postgresql://mlflow:mlflow@mlflow_db:5432/mlflow"
tracking_uri = "http://mlflow-server:5000"
mlflow.set_tracking_uri(tracking_uri)
client = MlflowClient(tracking_uri=tracking_uri)

exp_name = "Projet_Bitcoin_price_prediction"

# get MLFlow experiment_id
experiment_id = init_mlflow_experiment(exp_name = exp_name)

# recupérer les arguments du scripts
ticker = args.currency   
asset = args.asset
period='1d'
pas_temps=14





def pipeline_predict():
    """
    pipeline de commandes pour la prédiction de la valeur du lendemain d'un asset (paramètres ticker)
    """
    model_name = f"tf-lstm-reg-model-{period}"
    #model_name = f"tf-lstm-reg-model-{ticker}-{period}"
    model_version = "latest"

    #new_way
    # #load_tranform
    #data, df_index, scaler = load_transform_data2(table='ohlc',period=period)

    try:
        # Data loading 
        df = load_data_2(table='ohlc', asset=asset)
        print("Chargement des données KRAKEN effectué")
   
        # remove useless columns
        df.drop(columns= ['asset','dtutc','open','high','low','volume','trades'], axis=1, inplace =True)

        # tf np.array
        df_array = np.array(df, dtype=np.float64)
      
    except Exception as e:
        print(f"Error loading data: {e}") 
        print("Le chargement ou la normalisation des données Kraken a échoué")

    try:
        #Création du dataset de test
        X_test = make_dataset_for_testing(data = df_array, pas_temps = pas_temps)
        #print("X_test: ", X_test/scaler.scale_[0])
        print("Le chargement des données de test a réussi")
    except Exception as e:
        print(e)
        print ("Le chargement des données de test a échoué")
    
    #load best_model
    best_model = load_best_model(experiment_id=experiment_id,model_name =model_name, model_version = model_version, tracking_uri = tracking_uri)
        
    #prediction
    test_predict = best_model.predict(X_test)
    
    prediction_value = float(test_predict[-1].item())
    prediction_date = datetime.now()

    print(f"La valeur du Bitcoin était de {int(X_test[-1, 0].item())} {ticker} hier à la fermeture. Le modèle prédit une valeur de {prediction_value} {ticker} pour {prediction_date}")

    # Save the prediction to the database
    save_prediction_to_db(prediction_date, prediction_value)

    return {"prediction": prediction_value}

if __name__ == "__main__":
    prediction = pipeline_predict()