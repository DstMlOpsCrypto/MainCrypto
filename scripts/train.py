#mlflow
import mlflow
from mlflow import MlflowClient
from mlflow.models.signature import infer_signature
#import asyncio

#packages
import argparse
import sys
import os
import time

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

# Import des modules
from src.data.make_dataset import make_dataset
from src.data.import_raw_data import load_data, load_data_2, load_transform_data,load_transform_data2
from src.features.preprocess import normalize_data,normalize_data2
from src.evaluation.ml_flow import get_best_model, init_mlflow_experiment
from src.evaluation.evaluate import scaling, score
from src.models.model_LSTM import LSTMModel
from src.models.train_model import create_callbacks, train

#supprimer warnings GPU tensorflow
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# CLI parameters
parser = argparse.ArgumentParser(prog ='main.py',description="Pipeline d'exécution pour le projet MLops de prédiction des prix du bticoin")
parser.add_argument('--currency', choices= ['BTC-USD','BTC-EUR'], required=True, help="Selectionne la devise")

#parser.add_argument('--bitcoin', choices= ['BTC'], required=True, help="Selectionne le bitcoin")
#parser.add_argument('--currency', choices= ['-USD','-EUR'], required=True, help="Selectionne la devise")
#parser.add_argument('--period', choices= ['1d','5d','1wk'], required=True, help="Selectionne la période de prédiction") # non conservé
args = parser.parse_args()

# scripts variables
exp_name = "Projet_Bitcoin_price_prediction"
run_name = "first_run"

tracking_uri = "postgresql://mlflow:mlflow@mlflow_db:5432/mlflow"
mlflow.set_tracking_uri(tracking_uri)

neurons = 350

# MLflow Tracking client
client = MlflowClient(tracking_uri= tracking_uri)

# Initialize MLFlow experiment
experiment_id = init_mlflow_experiment(exp_name)


#recupérer les arguments du script
ticker = args.currency
#period= args.period # non conservé
period='1d'

# bitcoin = args.bitcoin
# currency = args.currency    
# ticker = bitcoin + currency

# Start the MLflow run

def pipeline_train():  

    # End any active run
    mlflow.end_run()
    
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
        print("Le chargement ou la normalisation des données yfinance a échoué")

    #New_way
    # Data loading 
    # try:
    #     df = load_data_2(table='ohlc')
    # except Exception as e:
    #     print(f"Error loading data: {e}")              
    
    # # # Data Normalization 2
    # df_array, df.index, scaler = normalize_data2(df= df, period=period)
    # print("Normalisation des données effectuée")

    with mlflow.start_run (run_name=run_name, experiment_id=experiment_id):           
        print("MLflow run started")
        
        for pas_temps in [3]:  #[1,2,3,5,8,10,12,14,16,20] # paramater finally chosen to 14        
                for batch_size in [1,2,5,10,20]:#15,20]:
                                   
                    # Initializing run                
                    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id, nested=True):

                        print(f"Début de l'entrainement du modèle suivant : pas_temps = {pas_temps},batch_size = {batch_size}, neurons = {neurons}, currency = {ticker}, period = {period}", end= "\n\n")
                        
                        #Building dataset for a pas_temps value
                        X_train, X_test, y_train, y_test= make_dataset(data = df_array, pas_temps=pas_temps, test_size=0.3)
                        print("Construction du Dataset terminée")      
                                        
                        # Model instanciation
                        model = LSTMModel(neurons=350)
                        # Training
                        history, model, duration_seconds = train(X_train, y_train, X_test, y_test, model, batch_size)
                        print(f"Entrainement du modèle {model} effectué en {duration_seconds} secondes.")

                        # Prediction
                        train_predict = model.predict(X_train)
                        test_predict = model.predict(X_test)
                        
                        # Scaling
                        train_predict, test_predict, y_train, y_test = scaling(train_predict, test_predict, y_train, y_test, scaler)
                        
                        #scores mse et r2
                        mse_train, r2_score_train, mse_test, r2_score_test = score(train_predict = train_predict, test_predict= test_predict, y_train = y_train, y_test = y_test)
                        # on se base au final sur la métrique mean_squared_error_test calculé sur l'éch. de test (mse_test)                        

                        # log params into tracking server
                        params = {'pas_temps':pas_temps, 'batch_size': batch_size}
                        mlflow.log_params(params)
                        
                        # log metrics to tracking server
                        mlflow.log_metrics(
                            {
                            "mean_squared_error_train": mse_train,
                            "r2_train_score": r2_score_train,
                            "mean_squared_error_test" : mse_test,
                            "r2_test_score" : r2_score_test
                            }
                        )
                        print("mean_squared_error_test", mse_test)
                        print("r2_test_score", r2_score_test)
          
        best_model_info = get_best_model(experiment_id = experiment_id, metric_name="mean_squared_error_test", ticker=ticker, period=period, tracking_uri=tracking_uri)
        # autre option : best_model_info = get_best_model(experiment_id = experiment_id, metric_name="r2_test_score", ticker=ticker, period=period, tracking_uri=tracking_uri)
     

    # training with best params

    #fetching best params
    if best_model_info is not None:
        print(best_model_info)
        pas_temps = int(best_model_info['params']['pas_temps'])
        batch_size = int(best_model_info['params']['batch_size'])
        run_id = best_model_info['run_id']
            
        with mlflow.start_run(run_name=run_name, nested=True):
            
            # Building dataset for a pas_temps value
            X_train, X_test, y_train, y_test= make_dataset(data = df_array, pas_temps=pas_temps, test_size=0.3)

            # Model instanciation
            model = LSTMModel(neurons=350)

            # Best model Training
            history, model, duration_seconds = train(X_train, y_train, X_test, y_test, model, batch_size)

            # model_name
            model_name = f"tf-lstm-reg-model-{period}"
            # model_name = f"tf-lstm-reg-model-{ticker}-{period}"

            # Signature creation
            signature = infer_signature(X_test, model.predict(X_test))

            # Log the model
            try:
                model_info = mlflow.tensorflow.log_model(model, artifact_path = model_name, signature=signature, registered_model_name = f"tf-lstm-reg-model-{period}")
                # model_info = mlflow.tensorflow.log_model(model, artifact_path = model_name, signature=signature, registered_model_name = f"tf-lstm-reg-model-{ticker}-{period}")
                
                # Print the run_id of the logged model
                print(f"The run_id of the logged model is: {model_info.run_id}")
            
            except Exception as e:
                print(f"An error occurred while logging the model: {e}")

    else:
        print("Le dictionnaire best_model_info est vide")

if __name__ == "__main__":
    pipeline_train()

        

