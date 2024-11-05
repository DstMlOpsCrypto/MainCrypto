import pytest
import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


#Ajout du repertoire de base au Path
# Récupérer le chemin d'accès du répertoire courant du dossier
current_dir = os.getcwd()
# Accéder au répertoire parent en utilisant os.pardir
parent_current_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
#ajout du chemin dans sys
sys.path.append(parent_current_dir)

from src.features.preprocess import normalize_data


@pytest.mark.parametrize("df, expect, index", [
    (
        pd.DataFrame({
            'Open': [400, 500, 600, 700, 800, 250],
            'High': [400, 355, 520, 700, 800, 900],
            'Low': [350, 450, 390, 700, 560, 650],
            'Close': [410, 789, 589, 700, 800, 900],
            'Volume': [1000, 1200, 1500, 700, 800, 900],
            'Dividends': [0, 0, 0, 0, 1, 0],
            'Stock Splits': [0, 0, 0, 0, 0, 1]
        }),
        (6, 1),  # Shape of the scaled data
        [0, 1, 2, 3, 4, 5]  # Expected index
    )
])
                         
def test_normalize_data_1d(df, expect, index):     
    # Appel de la fonction
    scaled_data, df_index, scaler = normalize_data(df=df, period='1d')

    # Assertions
    assert scaled_data.shape == expect    
    assert np.all((scaled_data >= 0) & (scaled_data <= 1.00000001)) # Vérifie que les données sont bien normalisées
    assert list(df_index) ==  index  # Vérifie que les index sont bien retournés


@pytest.mark.parametrize("df, expect, index", [
    (
    pd.DataFrame({'Open': [400, 500, 600, 700],
        'High': [4200, 355, 520, 700],
        'Low': [350,450,390, 700],
        'Close': [410, 789, 589, 700],
        'Volume': [1000, 1200, 1500, 700]
        }),    
        (4,1),
        [0,1,2,3]
    )
])
def test_normalize_data_5d(df, expect, index):
    # Appel de la fonction
    scaled_data, df_index, scaler = normalize_data(df=df, period='5d')

    # Assertions
    assert scaled_data.shape == expect            
    assert np.all((scaled_data >= 0) & (scaled_data <= 1.000000001))  # Vérifie que les données sont bien normalisées
    assert list(df_index) == index  # Vérifie que les index sont bien retournés
    
