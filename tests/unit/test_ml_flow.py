import requests
import pytest
import mlflow

from unittest.mock import Mock, MagicMock, patch

#a mettre dans __init__ si possible
import os
import sys
from os.path import dirname, join, normpath, abspath

# Récupérer le chemin d'accès du répertoire courant du dossier
current_dir = os.getcwd()
# Accéder au répertoire parent en utilisant os.pardir
parent_current_dir = abspath(os.path.join(current_dir, os.pardir))

# Accéder au répertoire grand parent
grand_parent_dir = abspath(os.path.join(parent_current_dir, os.pardir))

SRC_DIR = normpath(join(grand_parent_dir, 'src'))
SCRIPTS_DIR = normpath(join(grand_parent_dir, 'scripts'))


#ajout du chemin dans sys
sys.path.append(grand_parent_dir)
sys.path.append(SRC_DIR)
sys.path.append(SCRIPTS_DIR)

from evaluation.ml_flow import init_mlflow_experiment, get_best_model, get_check_experiment, load_best_model

# test de init_mlflow_experiment


@pytest.fixture
def mock_experiment():
    # Mock de l'objet expérimentation
    mock_experiment = MagicMock()
    mock_experiment.experiment_id = "12345"
    return mock_experiment

@patch('mlflow.set_experiment')
def test_init_mlflow_experiment(mock_set_experiment, capsys):
    # Créez un mock pour l'objet d'expérience
    mock_experiment = Mock()
    mock_experiment.experiment_id = '12345'
    mock_experiment.creation_time = '2024-08-22T12:00:00Z'
    
    # Configurez le mock pour `mlflow.set_experiment`
    mock_set_experiment.return_value = mock_experiment
    
    exp_name = 'test_experiment'
    result = init_mlflow_experiment(exp_name)
    
    # Vérifiez que `mlflow.set_experiment` a été appelé avec le bon nom
    mock_set_experiment.assert_called_once_with(exp_name)
    
    # Vérifiez que la fonction retourne le bon objet d'expérience
    assert result == mock_experiment
    
    # Vérifiez les impressions
    captured = capsys.readouterr()
    assert "Experiment name: {}".format(exp_name) in captured.out
    assert "Timestamp creation: {}".format(mock_experiment.creation_time) in captured.out


# fonction get_check_experiment

class MockMlflowClient:
    def __init__(self, experiments):
        self.experiments = experiments

    def get_experiment_by_name(self, name):
        return self.experiments.get(name, None)

# Patch `MlflowClient` in the `evaluation.ml_flow` module to use `MockMlflowClient` instead
@patch('evaluation.ml_flow.MlflowClient', return_value=MockMlflowClient({'exp1': Mock(experiment_id='1')}))
def test_get_check_experiment_found(mock_client, capsys):
    tracking_uri = 'http://mock-tracking-uri'
    result = get_check_experiment('exp1', tracking_uri)
    
    # Vérifiez que la fonction retourne le bon objet d'expérience
    assert result.experiment_id == '1'
    
    # Vérifiez les impressions
    captured = capsys.readouterr()
    assert not "Aucune expérience trouvée" in captured.out
    

# Fonction get_best_model

# @patch('evaluation.ml_flow.MlflowClient')
# @patch('evaluation.ml_flow.get_check_experiment')
# def test_get_best_model(mock_get_check_experiment, MockMlflowClient):
#     # Préparer le mock pour get_check_experiment
#     mock_experiment = MagicMock()
#     mock_experiment.experiment_id = '1'
#     mock_get_check_experiment.return_value = mock_experiment
    
#     # Préparer le mock pour MlflowClient
#     mock_client = MockMlflowClient.return_value
#     mock_run = MagicMock()
#     mock_run.info.run_id = 'run_123'
#     mock_run.data.params = {'param1': 'value1'}
#     mock_run.data.metrics = {'metric1': 0.95}
#     mock_run.info.artifact_uri = 'http://path/to/model'
#     mock_client.search_runs.return_value = [mock_run]
    
#     # Appeler la fonction avec des valeurs de test
#     result = get_best_model(
#         exp_name='test_exp',
#         metric_name='metric1',
#         ticker='USD',
#         period='1 day',
#         tracking_uri='http://localhost:5000'
#     )
    
#     # Vérifier les résultats
#     assert result is not None
#     assert result['run_id'] == 'run_123'
#     assert result['params'] == {'param1': 'value1'}
#     assert result['metrics'] == {'metric1': 0.95}
#     assert result['model_path'] == 'http://path/to/model/model'
    
#     # Vérifier les appels aux mocks
#     mock_get_check_experiment.assert_called_once_with('test_exp', 'http://localhost:5000')
#     MockMlflowClient.assert_called_once_with(tracking_uri='http://localhost:5000')
#     mock_client.search_runs.assert_called_once_with('1', order_by=['metrics.metric1 ASC'])

# @patch('evaluation.ml_flow.MlflowClient')
# @patch('evaluation.ml_flow.get_check_experiment')
# def test_get_best_model_no_runs(mock_get_check_experiment, MockMlflowClient):
#     # Préparer le mock pour get_check_experiment
#     mock_experiment = MagicMock()
#     mock_experiment.experiment_id = '1'
#     mock_get_check_experiment.return_value = mock_experiment
    
#     # Préparer le mock pour MlflowClient
#     mock_client = MockMlflowClient.return_value
#     mock_client.search_runs.return_value = []  # Aucun run trouvé
    
#     # Appeler la fonction avec des valeurs de test
#     result = get_best_model(
#         exp_name='test_exp',
#         metric_name='metric1',
#         ticker='USD',
#         period='1 day',
#         tracking_uri='http://localhost:5000'
#     )
    
#     # Vérifier les résultats
#     assert result is None  # Aucune information sur le modèle ne doit être retournée
    
#     # Vérifier les appels aux mocks
#     mock_get_check_experiment.assert_called_once_with('test_exp', 'http://localhost:5000')
#     MockMlflowClient.assert_called_once_with(tracking_uri='http://localhost:5000')
#     mock_client.search_runs.assert_called_once_with('1', order_by=['metrics.metric1 ASC'])
 
 

@patch('evaluation.ml_flow.MlflowClient')
@patch('evaluation.ml_flow.get_check_experiment')
def test_get_best_model(mock_get_check_experiment, MockMlflowClient):
    # Mock get_check_experiment to return a mocked experiment
    mock_experiment = MagicMock()
    mock_experiment.experiment_id = '1'
    mock_get_check_experiment.return_value = mock_experiment
    
    # Mock MlflowClient and its search_runs method
    mock_client = MockMlflowClient.return_value
    mock_run = MagicMock()
    mock_run.info.run_id = 'run_123'
    mock_run.data.params = {'param1': 'value1'}
    mock_run.data.metrics = {'metric1': 0.95}
    mock_run.info.artifact_uri = 'http://path/to/model'
    mock_client.search_runs.return_value = [mock_run]
    
    # Call the function with test inputs
    result = get_best_model(
        experiment=mock_experiment,
        metric_name='metric1',
        ticker='USD',
        period='1 day',
        tracking_uri='http://localhost:5000'
    )
    
    # Assertions
    assert result is not None
    assert result['run_id'] == 'run_123'
    assert result['params'] == {'param1': 'value1'}
    assert result['metrics'] == {'metric1': 0.95}
    assert result['model_path'] == 'http://path/to/model/model'
    
    # Ensure the mocked methods were called as expected
    mock_get_check_experiment.assert_called_once_with('test_exp', 'http://localhost:5000')
    MockMlflowClient.assert_called_once_with(tracking_uri='http://localhost:5000')
    mock_client.search_runs.assert_called_once_with('1', order_by=['metrics.metric1 ASC'])


@patch('evaluation.ml_flow.MlflowClient')
@patch('evaluation.ml_flow.get_check_experiment')
def test_get_best_model_no_runs(mock_get_check_experiment, MockMlflowClient):
    # Mock get_check_experiment to return a mocked experiment
    mock_experiment = MagicMock()
    mock_experiment.experiment_id = '1'
    mock_get_check_experiment.return_value = mock_experiment
    
    # Mock MlflowClient to return no runs
    mock_client = MockMlflowClient.return_value
    mock_client.search_runs.return_value = []  # No runs found
    
    # Call the function with test inputs
    result = get_best_model(
        experiment=mock_experiment,
        metric_name='metric1',
        ticker='USD',
        period='1 day',
        tracking_uri='http://localhost:5000'
    )
    
    # Assert the result is None
    assert result is None
    
    # Ensure the mocked methods were called as expected
    mock_get_check_experiment.assert_called_once_with('test_exp', 'http://localhost:5000')
    MockMlflowClient.assert_called_once_with(tracking_uri='http://localhost:5000')
    mock_client.search_runs.assert_called_once_with('1', order_by=['metrics.metric1 ASC'])

 
   
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

@patch("mlflow.tensorflow.load_model")  # Assurez-vous que ce chemin correspond à l'endroit où la fonction est utilisée
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
    

@patch("evaluation.ml_flow.get_check_experiment")
@patch("evaluation.ml_flow.MlflowClient")
@patch("evaluation.ml_flow.mlflow.tensorflow.load_model")
def test_load_best_model_failure(mock_load_model, mock_MlflowClient, mock_get_check_experiment, mock_experiment):
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
    model_uri = f"models:/{model_name}/{model_version}"
    mock_load_model.assert_called_once_with(model_uri=model_uri)
    assert best_model is None
    
    
    