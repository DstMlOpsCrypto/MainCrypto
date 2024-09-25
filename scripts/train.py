## Entrainer et sauvergarder le modèle
 
#mlflow
import mlflow
from mlflow import MlflowClient
from mlflow.models.signature import infer_signature

#packages
import argparse
import sys
import os
import time


# PATH# Récupérer le chemin d'accès du répertoire courant du dossier
current_dir = os.getcwd()
# Accéder au répertoire parent en utilisant os.pardir
parent_current_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
#ajout du chemin dans sys
sys.path.append(parent_current_dir)

# Import des modules
from src.data.make_dataset import make_dataset, prepare_sequential_data 
from src.data.import_raw_data import load_data, load_transform_data
from src.features.preprocess import normalize_data
from src.evaluation.ml_flow import get_best_model, init_mlflow_experiment
from src.evaluation.evaluate import scaling, score
from src.models.model_LSTM import LSTMModel
from src.models.train_model import create_callbacks, train

#supprimer warnings GPU tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# CLI parameters
parser = argparse.ArgumentParser(prog ='main.py',description="Pipeline d'exécution pour le projet MLops de prédiction des prix du bticoin")
parser.add_argument('--currency', choices= ['BTC-USD','BTC-EUR'], required=True, help="Selectionne la devise")
#parser.add_argument('--period', choices= ['1d','5d','1wk'], required=True, help="Selectionne la période de prédiction")
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

# Start the MLflow run

def pipeline():  

    # End any active run
    mlflow.end_run()

    #recupérer les arguments du script
    ticker = args.currency
    #period= args.period
    period='1d'
             
    # Data loading 
    df = load_data(ticker=ticker, start = "2014-07-01", end = "2024-08-01", interval = period, start_new_data = "2024-08-01")
    print("Chargement des données effectué")
            
    # Data Normalization
    df_array, df.index, scaler = normalize_data(df= df, period=period)
    print("Normalisation des données effectuée")   


    with mlflow.start_run (run_name=run_name, experiment_id=experiment_id):           
        print("MLflow run started")
        
        for pas_temps in [1,2,3,5,10,14]:  #14          
                for batch_size in [5]:#,10,15,20]:
                                   
                    # Initializing run                
                    with mlflow.start_run(run_name=run_name, experiment_id=experiment_id, nested=True):

                        print(f"Début de l'entrainement du modèle suivant : pas_temps = {pas_temps},batch_size = {batch_size}, neurons = {neurons}, currency = {ticker}, period = {period}", end= "\n\n")
                        
                        #Building dataset for a pas_temps value
                        X_train, X_test, y_train,y_test= make_dataset(data = df_array, pas_temps=pas_temps, test_size=0.3)
                        print("Construction du Dataset terminée")      
                                        
                        # Model instanciation
                        model=LSTMModel(neurons=350)
                        
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

                        # log params
                        params = {'pas_temps':pas_temps, 'batch_size': batch_size}
                        mlflow.log_params(params)
                        
                        # log metrics
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
          
        best_model_info = get_best_model(experiment_id=experiment_id, metric_name="mean_squared_error_test", ticker=ticker, period=period, tracking_uri=tracking_uri)
        
        #une fois les run terminés, détermination des meilleurs paramètres
        #best_model_info = get_best_model(experiment=experiment, metric_name="mean_squarred_error_test", ticker=ticker, period = period, tracking_uri = tracking_uri)    

    # best model re training
    #fetching best params
    if best_model_info is not None:
        print(best_model_info)
        pas_temps = int(best_model_info['params']['pas_temps'])
        batch_size = int(best_model_info['params']['batch_size'])
        run_id = best_model_info['run_id']
            
        with mlflow.start_run(run_name=run_name, nested=True):
            #Building dataset for a pas_temps value
            X_train, X_test, y_train, y_test= make_dataset(data = df_array, pas_temps=pas_temps, test_size=0.3)

            # Model instanciation
            model = LSTMModel(neurons=350)

            # Best model Training
            history, model, duration_seconds = train(X_train, y_train, X_test, y_test, model, batch_size)

            # load_tranform
            X_test, _ , scaler = load_transform_data(period = period,ticker = ticker) 
            test_predict = model.predict(X_test)

            X_test =  X_test/scaler.scale_[0]
            test_predict = test_predict/scaler.scale_[0]

            print(f"La valeur du Bitcoin était de {(int(X_test[-1]))} {ticker} hier à la fermeture. Le modèle prédit une valeur de {test_predict[-1]} {ticker} ")

            # model_name
            model_name = f"tf-lstm-reg-model-{period}"

            # Signature creation
            signature = infer_signature(X_test, model.predict(X_test))

            # Log the model
            try:
                model_info = mlflow.tensorflow.log_model(model, artifact_path = model_name, signature=signature, registered_model_name = f"tf-lstm-reg-model-{period}")
                # Print the run_id of the logged model
                print(f"The run_id of the logged model is: {model_info.run_id}")

            except Exception as e:
                print(f"An error occurred while logging the model: {e}")

    else:
        print("Le dictionnaire best_model_info est vide")

if __name__ == "__main__":
    pipeline()  
 



        

