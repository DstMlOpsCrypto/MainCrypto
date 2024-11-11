 # fonction get_check_experiment
import requests
import pytest
import mlflow
from unittest.mock import Mock, MagicMock, patch

#a mettre dans __init__ si possible
import os
import sys

from evaluation.ml_flow import init_mlflow_experiment, get_best_model, get_check_experiment, load_best_model

class MockMlflowClient:
    def __init__(self, experiments):
        self.experiments = experiments

    def get_experiment_by_name(self, name):
        return self.experiments.get(name, None)

# Patch `MlflowClient` in the `evaluation.ml_flow` module to use `MockMlflowClient` instead
@patch('evaluation.ml_flow.MlflowClient', return_value= MockMlflowClient({'exp1': Mock(experiment_id='1')}))
def test_get_check_experiment_found(mock_client, capsys):
    tracking_uri = 'http://mock-tracking-uri'
    result = get_check_experiment('exp1', tracking_uri)
    
    # Vérifiez que la fonction retourne le bon objet d'expérience
    assert result.experiment_id == '1'
    
    # Vérifiez les impressions
    captured = capsys.readouterr()
    assert not "Aucune expérience trouvée" in captured.out