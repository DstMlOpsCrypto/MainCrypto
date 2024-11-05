import pytest
import numpy as np
import joblib
import os
from unittest.mock import MagicMock, patch
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
from sklearn.metrics import mean_squared_error, r2_score

from src.models.model_LSTM import LSTMModel


def test_lstmmodel_init():
    
    model = LSTMModel(neurons=50, input_shape=(10, 1), activ_func='tanh', loss='mae', metrics=['mae'], optimizer='sgd')
    
    assert model.neurons == 50
    assert model.input_shape == (10, 1)
    assert model.activ_func == 'tanh'
    assert model.loss == 'mae'
    assert model.metrics == ['mae']
    assert model.optimizer == 'sgd'
    assert isinstance(model.model, Sequential)

@patch('src.models.model_LSTM.Sequential.fit')
def test_lstmmodel_fit(mock_fit):
    # Préparer des données fictives
    X_train = np.random.rand(10, 10, 1)
    y_train = np.random.rand(10)
    X_test = np.random.rand(5, 10, 1)
    y_test = np.random.rand(5)
    
    # Créer un modèle
    model = LSTMModel(neurons=50)
    
    # Configurer les mocks
    mock_fit.return_value = MagicMock()  # Simule l'objet retourné par fit
    
    # Appeler la méthode
    history, model_obj, duration = model.fit(X_train, y_train, X_test, y_test, None, None)
    
    # Assertions
    mock_fit.assert_called_once_with(X_train, y_train, batch_size=10, epochs=100, verbose=0, validation_data=[X_test, y_test], callbacks=[None, None])
    assert isinstance(history, MagicMock)
    assert isinstance(model_obj, Sequential)


@patch('src.models.model_LSTM.Sequential.predict')
def test_lstmmodel_predict(mock_predict):
    
    # Préparer des données fictives
    X_test = np.random.rand(5, 10, 1)
    
    # Créer un modèle
    model = LSTMModel(neurons=50)
    
    # Configurer les mocks
    mock_predict.return_value = np.random.rand(10)
    
    
    # Appeler la méthode
    test_predict = model.predict (X_test)
    
    # Assertions
    mock_predict.assert_called_once_with(X_test)
    
    assert isinstance(test_predict, np.ndarray)
 
    
@patch('joblib.dump')
def test_lstmmodel_save_model(mock_dump):
    model = LSTMModel(neurons=50)
    path = 'test_model.joblib'
    
    model.save_model(path=path)
    
    mock_dump.assert_called_once_with(model.model, path)
    

@patch('joblib.load')
@patch('os.path.exists')
def test_lstmmodel_load_model(mock_exists, mock_load):
    path = 'test_model.joblib'
    model = LSTMModel(neurons=50)
    
    # Simule que le fichier existe
    mock_exists.return_value = True
    # Simule le retour d'un objet chargé par joblib.load
    mock_load.return_value = MagicMock()
    
    # Appel de la méthode de chargement
    model.load_model(path=path)
    
    # Vérifie que os.path.exists a été appelé avec le bon chemin
    mock_exists.assert_called_once_with(path)
    # Vérifie que joblib.load a été appelé avec le bon chemin
    mock_load.assert_called_once_with(path)
    # Vérifie que le modèle interne a été remplacé par le mock
    assert isinstance(model.model, MagicMock)
    
    # Test pour vérifier si le fichier n'existe pas
    mock_exists.return_value = False
    model.load_model(path=path)
    # Si le fichier n'existe pas, model.model ne devrait pas être modifié par joblib.load
    assert mock_load.call_count == 1  # Toujours 1 car il ne devrait pas être rappelé
    
    
def test_lstmmodel_get_params():
    model = LSTMModel(neurons=50)
    params = model.get_params()
    assert params == {'neurons': 50}

def test_lstmmodel_set_params():
    model = LSTMModel(neurons=50)
    model.set_params(neurons=100)
    assert model.neurons == 100
    
def test_lstmmodel_str():
    model = LSTMModel(neurons=50)
    assert str(model) == "LSTM(neurons=50)"
    
