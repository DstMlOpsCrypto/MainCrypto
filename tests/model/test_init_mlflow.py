import requests
import pytest
import mlflow
from unittest.mock import Mock, MagicMock, patch

#a mettre dans __init__ si possible
import os
import sys

from evaluation.ml_flow import init_mlflow_experiment, get_best_model, get_check_experiment, load_best_model

# test de init_mlflow_experiment

@pytest.fixture
def mock_experiment():
    # Mock de l'objet expérimentation
    mock_experiment = MagicMock()
    mock_experiment.experiment_id = "12345"
    return mock_experiment

@patch('mlflow.get_experiment_by_name')
@patch('mlflow.create_experiment')
@patch('mlflow.get_experiment')
def test_init_mlflow_experiment(mock_get_experiment, mock_create_experiment, mock_get_experiment_by_name, capsys):
    # Définir le nom de l'expérience à utiliser dans le test
    exp_name = "test_experiment"
    
    # Créer un mock pour l'objet experiment
    mock_experiment = MagicMock()
    mock_experiment.experiment_id = "12345"
    mock_experiment.name = exp_name
    mock_experiment.creation_time = 1234567890

    # Cas 1: Lorsque l'expérience existe déjà
    mock_get_experiment_by_name.return_value = mock_experiment
    mock_get_experiment.return_value = mock_experiment  # Mock get_experiment pour retourner l'expérience

    experiment_id = init_mlflow_experiment(exp_name)

    # Capturer la sortie imprimée
    captured = capsys.readouterr()

    # Assertions
    assert experiment_id == "12345"
    assert "Using existing experiment: test_experiment" in captured.out

    # Cas 2: Lorsque l'expérience n'existe pas, simuler la création d'une nouvelle expérience
    mock_get_experiment_by_name.return_value = None
    mock_create_experiment.return_value = "12345"
    mock_get_experiment.return_value = mock_experiment  # Mock le retour de l'expérience après la création

    experiment_id = init_mlflow_experiment(exp_name)

    # Capturer à nouveau la sortie imprimée
    captured = capsys.readouterr()

    # Assertions pour la création d'une nouvelle expérience
    assert experiment_id == "12345"
    assert "Created a new experiment: test_experiment" in captured.out
    assert "Experiment name: test_experiment" in captured.out
    assert "Timestamp creation:" in captured.out  # Vérifier la présence de l'information de timestamp