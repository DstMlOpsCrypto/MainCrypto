import requests
import pytest
import mlflow
from unittest.mock import Mock, MagicMock, patch

#a mettre dans __init__ si possible
import os
import sys

from evaluation.ml_flow import init_mlflow_experiment, get_best_model, get_check_experiment, load_best_model

 
   
# test load best_model
@pytest.fixture
def mock_experiment():
    mock_experiment = MagicMock()
    mock_experiment.experiment_id = "12345"
    return mock_experiment

@pytest.fixture
def mock_run():
    mock_run = MagicMock()
    mock_run.info.run_id = "abcde12345"
    mock_run.data.metrics = {"mean_squarred_error_test": 0.01}
    return mock_run

@patch("mlflow.tensorflow.load_model")
@patch("evaluation.ml_flow.get_check_experiment")
@patch("evaluation.ml_flow.MlflowClient")
def test_load_best_model_success(mock_MlflowClient, mock_get_check_experiment, mock_load_model, mock_experiment, mock_run):
    # Configuration des mocks
    mock_get_check_experiment.return_value = mock_experiment
    mock_client = mock_MlflowClient.return_value
    mock_client.search_runs.return_value = [mock_run]
    mock_load_model.return_value = "mocked_model"

    # Variables de test
    exp_name = "test_experiment"
    model_name = "test_model"
    model_version = "1"
    period = "1d"
    tracking_uri = "http://mock_tracking_uri"
    
    # Appel de la fonction
    best_model = load_best_model(exp_name, model_name, model_version, period, tracking_uri)

    # Assertions
    mock_get_check_experiment.assert_called_once_with(exp_name, tracking_uri)
    mock_client.search_runs.assert_called_once_with(mock_experiment.experiment_id, order_by=["metrics.mean_squarred_error_test ASC"])
    model_uri = f"models:/{model_name}/{model_version}"
    mock_load_model.assert_called_once_with(model_uri=model_uri)
    assert best_model == "mocked_model"
    
@patch("evaluation.ml_flow.mlflow.tensorflow.load_model")
@patch("evaluation.ml_flow.MlflowClient")
@patch("evaluation.ml_flow.get_check_experiment")  # Ensure this path is correct
def test_load_best_model_failure(mock_get_check_experiment, mock_MlflowClient, mock_load_model, mock_experiment):
    # Configuration des mocks
    mock_get_check_experiment.return_value = mock_experiment
    mock_client = mock_MlflowClient.return_value
    mock_client.search_runs.return_value = []  # Aucun run trouvé
    mock_load_model.side_effect = mlflow.exceptions.MlflowException("Model not found")

    # Variables de test
    exp_name = "test_experiment"
    model_name = "test_model"
    model_version = "1"
    period = "1d"
    tracking_uri = "http://mock_tracking_uri"
    
    # Appel de la fonction
    best_model = load_best_model(exp_name, model_name, model_version, period, tracking_uri)
    
    # Assertions
    mock_get_check_experiment.assert_called_once_with(exp_name, tracking_uri)
    mock_client.search_runs.assert_called_once_with(mock_experiment.experiment_id, order_by=["metrics.mean_squarred_error_test ASC"])
    mock_load_model.assert_not_called()  # Puisqu'aucun run n'est trouvé, load_model ne devrait pas être appelé
    assert best_model is None
    
    
    