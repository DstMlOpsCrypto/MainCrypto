import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from sklearn.preprocessing import MinMaxScaler

# Importation de la fonction normalize_data2 depuis le module src.features.preprocess
from src.features.preprocess import normalize_data2

@pytest.fixture
def mock_dataframe():
    """Fixture qui crée un DataFrame pour le test."""
    data = {
        'asset': ['A', 'B', 'C'],
        'dtutc': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'open': [100, 105, 110],
        'high': [110, 115, 120],
        'low': [95, 100, 105],
        'volume': [1000, 1100, 1200],
        'trades': [10, 15, 20],
        'feature1': [1.0, 2.0, 3.0],
        'feature2': [4.0, 5.0, 6.0]
    }
    return pd.DataFrame(data)

@patch('src.features.preprocess.MinMaxScaler')  # Patch MinMaxScaler dans le bon module
def test_normalize_data2(mock_scaler, mock_dataframe):
    # Créer un objet mock du scaler pour contrôler son comportement
    mock_scaler_instance = mock_scaler.return_value
    mock_scaler_instance.fit_transform.return_value = np.array([0.2, 0.5, 0.6])  # Valeur simulée de normalisation

    # Appeler la fonction à tester
    period = '1d'  # Utilisation d'un paramètre factice pour le test
    scaled_data, df_index, scaler = normalize_data2(mock_dataframe, period)
    
    # Assertions
    # Vérifier que les données ont été correctement normalisées
    np.testing.assert_array_equal(scaled_data, np.array([0.2, 0.5, 0.6]))
    # Vérifier que le scaler a été utilisé
    mock_scaler_instance.fit_transform.assert_called_once_with(np.array(mock_dataframe[['feature1', 'feature2']]))