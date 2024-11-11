import requests
import pytest
import mlflow
from unittest.mock import Mock, MagicMock, patch

#a mettre dans __init__ si possible
import os
import sys

from evaluation.ml_flow import init_mlflow_experiment, get_best_model, get_check_experiment, load_best_model

@patch('evaluation.ml_flow.MlflowClient')
def test_get_best_model(MockMlflowClient): 
    
    # Mock MlflowClient and its search_runs method
    mock_client = MockMlflowClient.return_value
    mock_run = MagicMock()
    mock_run.info.run_id = 'run_123'
    mock_run.data.params = {'param1': 'value1'}
    mock_run.data.metrics = {'metric1': 0.95}
    mock_run.info.artifact_uri = "http://path/to"
    mock_client.search_runs.return_value = [mock_run]
    
    result = get_best_model(
        experiment_id='1',  # Pass experiment_id directly
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
    assert result['model_path'] == "http://path/to/model"
    
    # Ensure the mocked methods were called as expected
    MockMlflowClient.assert_called_once_with(tracking_uri='http://localhost:5000')
    mock_client.search_runs.assert_called_once_with(experiment_ids = ['1'], order_by=['metrics.metric1 ASC'])
