  
import numpy as np
import pytest
from sklearn.metrics import mean_squared_error, r2_score
from unittest.mock import MagicMock

from src.evaluation.evaluate import scaling, score
from src.models import model_LSTM

@pytest.fixture
def data():
    # Données fictives pour entraîner et tester
    y_train = np.array([1.0, 2.0, 3.0, 4.0])
    y_test = np.array([2.5, 3.0, 3.5, 4.0])
    train_predict = np.array([1.1, 2.1, 3.0, 3.9])
    test_predict = np.array([2.6, 2.9, 3.4, 4.1])
    return train_predict, test_predict, y_train, y_test

def test_score_mse_r2(data):
    train_predict, test_predict, y_train, y_test = data

    # Calculs attendus
    expected_mse_train = mean_squared_error(y_train, train_predict)
    expected_r2_score_train = r2_score(y_train, train_predict)
    expected_mse_test = mean_squared_error(y_test, test_predict)
    expected_r2_score_test = r2_score(y_test, test_predict)

    # Exécution de la fonction score
    mse_train, r2_train, mse_test, r2_test = score(train_predict, test_predict, y_train, y_test)

    # Vérification des résultats
    assert mse_train == pytest.approx(expected_mse_train)
    assert r2_train == pytest.approx(expected_r2_score_train)
    assert mse_test == pytest.approx(expected_mse_test)
    assert r2_test == pytest.approx(expected_r2_score_test)

def test_score_zero_error():
    # Cas où les prédictions sont parfaites
    y_train = np.array([1.0, 2.0, 3.0, 4.0])
    y_test = np.array([2.5, 3.0, 3.5, 4.0])
    train_predict = y_train
    test_predict = y_test

    mse_train, r2_train, mse_test, r2_test = score(train_predict, test_predict, y_train, y_test)

    assert mse_train == pytest.approx(0.0)
    assert r2_train == pytest.approx(1.0)
    assert mse_test == pytest.approx(0.0)
    assert r2_test == pytest.approx(1.0)

def test_score_negative_r2():
    # Cas où les prédictions sont complètement incorrectes
    y_train = np.array([1.0, 2.0, 3.0, 4.0])
    y_test = np.array([2.5, 3.0, 3.5, 4.0])
    train_predict = np.array([4.0, 3.0, 2.0, 1.0])  # Complètement opposé
    test_predict = np.array([4.0, 3.5, 3.0, 2.5])

    mse_train, r2_train, mse_test, r2_test = score(train_predict, test_predict, y_train, y_test)

    assert r2_train < 0  # r2_score devrait être négatif pour de mauvaises prédictions
    assert r2_test < 0
