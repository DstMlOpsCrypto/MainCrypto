import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

# Supposons que load_data_2 est dans le module 'my_module'
from src.data.import_raw_data import load_data_2

@pytest.fixture
def mock_db_connection():
    """Fixture qui simule une connexion à la base de données."""
    # Simuler une connexion à la base de données
    mock_conn = MagicMock()
    yield mock_conn  # Cette valeur sera utilisée dans le test
    mock_conn.close()  # Assurer que la connexion est fermée après le test

@patch('src.data.import_raw_data.pd.read_sql_query')  # Patch de pandas pour simuler le chargement des données
@patch('src.data.import_raw_data.get_db')  # Patch de get_db pour simuler la connexion à la base de données
def test_load_data_2(mock_get_db, mock_read_sql_query, mock_db_connection):
    
    # Configurer les mocks
    mock_get_db.return_value = mock_db_connection  # Retourner notre connexion simulée
    mock_df = pd.DataFrame({
        'column1': ['value1', 'value2'],
        'column2': ['value3', 'value4']
    })  # Exemple de DataFrame simulé
    mock_read_sql_query.return_value = mock_df  # Retourner le DataFrame simulé lors de l'appel de read_sql_query
    
    # Appeler la fonction à tester
    table = 'my_table'
    asset = 'my_asset'
    result = load_data_2(table, asset)
    
    # Assertions
    mock_get_db.assert_called_once()  # Vérifier que get_db a été appelé une seule fois
    mock_read_sql_query.assert_called_once_with(
        f"SELECT * FROM {table} WHERE asset='{asset}' ORDER BY dtutc DESC",
        mock_db_connection
    )  # Vérifier que read_sql_query a été appelé avec la requête correcte
    
    # Vérifier que le résultat est bien le DataFrame simulé
    assert result.equals(mock_df)  # Comparer les DataFrames