from keras.models import Sequential
from keras.layers import LSTM, Dense,Input
import datetime
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os


from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


class LSTMModel:
    def __init__(self,neurons,input_shape=(None,1),activ_func = "relu",loss= 'mse', metrics=['mse'], optimizer='adam'):
        """
        Initialisation du modèle LSTM avec un hyperparamètre de base.
        """

        #Construction du modèle et initialition des attributs
        self.neurons=neurons
        self.input_shape = input_shape
        self.activ_func = activ_func
        self.loss = loss
        self.metrics = metrics
        self.optimizer = optimizer
        self.name = "LSTM"
        
        self.model = Sequential()
        
        # Add the input layer
        self.model.add(Input(shape=self.input_shape))
        
        # Add the LSTM layer
        self.model.add(LSTM(self.neurons, activation=self.activ_func))
        
        # add dense layer for prediction
        self.model.add(Dense(1))
        
        #compilation
        self.model.compile(loss=self.loss, metrics=self.metrics, optimizer=self.optimizer)
                

    def fit(self, X_train, y_train, X_test, y_test, early_stopping, reduce_learning_rate, batch_size = 10):
        """
        Entraîne le modèle LSTM sur les données fournies.
        
        """
        # Enregistrer l'heure de début
        start_time = datetime.datetime.now()
        print("debut de l'entrainement")
        history = self.model.fit(X_train, y_train,
                        batch_size= batch_size,
                        epochs=100, verbose=0,
                        validation_data = [X_test, y_test],
                        callbacks=[reduce_learning_rate, early_stopping])
        
        # Enregistrer l'heure de fin
        end_time = datetime.datetime.now()
        # Calculer la durée
        duration = end_time - start_time
        duration_seconds = duration.total_seconds()

        return history, self.model, duration_seconds
    
    def predict(self,X):
        """
        Prédiction avec le modèle LSTM.
        """           
        print(f"Prédiction du modèle {self.model} effectué.")
        return self.model.predict(X)    
   
 
    def save_model(self, path='model.joblib'):
            """
            Sauvegarde le modèle entraîné sur le disque (chemin path).
            """
            joblib.dump(self.model,path)
            print(f"Modèle sauvegardé à l'emplacement : {path}")
            

    def load_model(self, path='model.joblib'):
        """
        Charge un modèle depuis le disque (chemin path).
        """
        if os.path.exists(path):
            self.model = joblib.load(path)
            print(f"Modèle chargé depuis : {path}")
        else:
            print("Le chemin du modèle spécifié n'existe pas.")
    
    def get_params(self, deep=True):
        return {
            'neurons': self.neurons 
        }

    def set_params(self, **params):
        if 'neurons' in params:
            self.neurons = params['neurons']
        return self

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne de l'objet LSTM.
        """
        return f"{self.name}(neurons={self.neurons})"