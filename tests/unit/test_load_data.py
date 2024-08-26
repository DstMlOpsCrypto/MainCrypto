import requests
import pytest
import os
import sys
import pandas as pd

#Ajout du repertoire de base au Path
# Récupérer le chemin d'accès du répertoire courant du dossier
current_dir = os.getcwd()
# Accéder au répertoire parent en utilisant os.pardir
parent_current_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
#ajout du chemin dans sys
sys.path.append(parent_current_dir)

from src.data.import_raw_data import load_data


@pytest.mark.parametrize("interval", ["1d", "5d"])
def test_load_data(interval):
    # Créez des valeurs factices pour les paramètres
    ticker = "AAPL"  # Utilisez un ticker réel comme exemple, par exemple "AAPL" pour Apple Inc.
    start = "2014-07-01"
    end = "2024-08-01"
    start_new_data = "2024-08-01"
    
    # Appeler la fonction load_data
    df = load_data(ticker, start=start, end=end, interval=interval, start_new_data=start_new_data)
    
    # Vérifiez que l'objet retourné est bien un DataFrame
    assert isinstance(df, pd.DataFrame), f"Le résultat doit être un DataFrame, mais il est {type(df)}"
    
    # Vérifiez que le DataFrame n'est pas vide
    assert not df.empty, "Le DataFrame ne doit pas être vide"
    
    # Vérifiez que le DataFrame contient au moins 100 entrées
    assert df.shape[0] > 100, f"Le DataFrame doit contenir plus de 100 lignes, mais il en contient {df.shape[0]}"

    # Optionnel: Vérifiez les colonnes attendues (par exemple, 'Open', 'Close', 'Volume', etc.)
    expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in expected_columns:
        assert col in df.columns, f"La colonne {col} est manquante dans le DataFrame"





    
#  print(f"la variable log vaut {os.environ.get('LOG')}")
            
# # # impression des logs dans un dossier log sue le container de test dans app/log
#         # if os.environ.get('LOG') == '1':
#         #     log_dir = 'app/log'
#         #     os.makedirs(log_dir, exist_ok=True)
#         #     log_file = os.path.join(log_dir, 'training_test.log')
#         #     with open(log_file, 'a') as file:
#         #             print(output, file=file)
