import pytest
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from unittest.mock import MagicMock

from src.evaluation.evaluate import scaling, score


#ficture pour un mock du scaler
@pytest.fixture
def mock_scaler():
    """Fixture pour un mock de scaler"""
    mock_scaler = MagicMock() # instanciation mock
    mock_scaler.scale_ = np.array([10])  # Simule une échelle de 10 pour le scaler en lui attribuant un attribut
    return mock_scaler


def test_scaling(mock_scaler):
    # Données d'entrée simulées
    train_predict = np.array([10, 20, 30])
    test_predict = np.array([15, 25, 35])
    y_train = np.array([100, 200, 300])
    y_test = np.array([150, 250, 350])

    # Appel de la fonction
    train_predict_scaled, test_predict_scaled, y_train_scaled, y_test_scaled = scaling(
        train_predict, test_predict, y_train, y_test, mock_scaler
    )

    # Assertions
    assert np.array_equal(train_predict_scaled, train_predict / mock_scaler.scale_[0])
    assert np.array_equal(test_predict_scaled, test_predict / mock_scaler.scale_[0])
    assert np.array_equal(y_train_scaled, y_train.reshape(-1, 1) / mock_scaler.scale_[0])
    assert np.array_equal(y_test_scaled, y_test.reshape(-1, 1) / mock_scaler.scale_[0])

    # Vérifie que scaler.scale_[0] est bien utilisé
    assert np.all(train_predict_scaled == train_predict / 10)
    assert np.all(test_predict_scaled == test_predict / 10)
    assert np.all(y_train_scaled == y_train.reshape(-1, 1) / 10)
    assert np.all(y_test_scaled == y_test.reshape(-1, 1) / 10)
    
    
    
    
def test_lstmmodel_score():
    train_predict = np.array([1, 2, 3])
    test_predict = np.array([1, 2, 3])
    y_train = np.array([1, 2, 3])
    y_test = np.array([1, 2, 3])
    
    mse_train, r2_train, mse_test, r2_test = LSTMModel.score(train_predict, test_predict, y_train, y_test)
    
    assert mse_train == mean_squared_error(y_train, train_predict)
    assert r2_train == r2_score(y_train, train_predict)
    assert mse_test == mean_squared_error(y_test, test_predict)
    assert r2_test == r2_score(y_test, test_predict)
    
    
 
@pytest.mark.parametrize("y_train, train_predict, y_test, test_predict, expected_mse_train, expected_r2_train, expected_mse_test, expected_r2_test", [
    # Cas parfait (précédent)
    (
        np.array([1, 2, 3, 4]),  # y_train
        np.array([1, 2, 3, 4]),  # train_predict
        np.array([2, 4, 6, 8]),  # y_test
        np.array([2, 4, 6, 8]),  # test_predict
        0.0,  # expected_mse_train
        1.0,  # expected_r2_train
        0.0,  # expected_mse_test
        1.0   # expected_r2_test
    ),
    # Cas avec des erreurs dans les prédictions
    (
        np.array([1, 2, 3, 4]),  # y_train
        np.array([1, 2, 3, 5]),  # train_predict
        np.array([2, 4, 6, 8]),  # y_test
        np.array([2, 3, 6, 8]),  # test_predict
        mean_squared_error([1, 2, 3, 4], [1, 2, 3, 5]),  # expected_mse_train
        r2_score([1, 2, 3, 4], [1, 2, 3, 5]),            # expected_r2_train
        mean_squared_error([2, 4, 6, 8], [2, 3, 6, 8]),  # expected_mse_test
        r2_score([2, 4, 6, 8], [2, 3, 6, 8])             # expected_r2_test
    ),
    # Cas où les prédictions sont complètement décalées
    (
        np.array([1, 2, 3, 4]),  # y_train
        np.array([4, 3, 2, 1]),  # train_predict
        np.array([2, 4, 6, 8]),  # y_test
        np.array([8, 6, 4, 2]),  # test_predict
        mean_squared_error([1, 2, 3, 4], [4, 3, 2, 1]),  # expected_mse_train
        r2_score([1, 2, 3, 4], [4, 3, 2, 1]),            # expected_r2_train
        mean_squared_error([2, 4, 6, 8], [8, 6, 4, 2]),  # expected_mse_test
        r2_score([2, 4, 6, 8], [8, 6, 4, 2])             # expected_r2_test
    ),
])
def test_lstmmodel_score_2(y_train, train_predict, y_test, test_predict, expected_mse_train, expected_r2_train, expected_mse_test, expected_r2_test):
    
    # Appel de la fonction
    mse_train, r2_train, mse_test, r2_test = LSTMModel.score(train_predict, test_predict, y_train, y_test)

    # Vérification des résultats attendus
    assert np.isclose(mse_train, expected_mse_train), f"Expected MSE train to be {expected_mse_train} but got {mse_train}"
    assert np.isclose(r2_train, expected_r2_train), f"Expected R2 train to be {expected_r2_train} but got {r2_train}"

    assert np.isclose(mse_test, expected_mse_test), f"Expected MSE test to be {expected_mse_test} but got {mse_test}"
    assert np.isclose(r2_test, expected_r2_test), f"Expected R2 test to be {expected_r2_test}"
    
    
    
    

    
    