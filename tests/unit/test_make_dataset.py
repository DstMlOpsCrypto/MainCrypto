import numpy as np
import pytest
from  src.data.make_dataset import prepare_sequential_data, split  


#test prepare_sequential_data

def test_prepare_sequential_data_basic():
    data = np.array([[1], [2], [3], [4], [5], [6]])  # Un petit ensemble de données pour les tests
    pas_temps = 2

    X, y = prepare_sequential_data(data, pas_temps)
    
    # Les séquences d'entrée attendues
    expected_X = np.array([[1, 2],
        [2, 3],
        [3, 4],
        [4, 5]])
    
    # Les cibles attendues
    expected_y = np.array([3, 4, 5, 6])
        
    # Vérifier que les résultats sont corrects
    np.testing.assert_array_equal(X, expected_X)
    np.testing.assert_array_equal(y, expected_y)

def test_prepare_sequential_data_single_step():
    data = np.array([[10], [20], [30], [40], [50]])
    pas_temps = 1

    X, y = prepare_sequential_data(data, pas_temps)
    
    expected_X = np.array([[10], [20], [30], [40]])
    expected_y = np.array([20, 30, 40, 50])
    
    np.testing.assert_array_equal(X, expected_X)
    np.testing.assert_array_equal(y, expected_y)

def test_prepare_sequential_data_large_step():
    data = np.array([[100], [200], [300], [400], [500], [600], [700], [600], [400], [1000], [600], [700]])
    pas_temps = 5

    X, y = prepare_sequential_data(data, pas_temps)
    
    expected_X = np.array(
        [
        [100, 200, 300, 400, 500],
        [200, 300, 400, 500, 600],
        [300, 400, 500, 600, 700],
        [400, 500, 600, 700, 600],
        [500, 600, 700, 600, 400],
        [600, 700, 600, 400, 1000],
        [700, 600, 400, 1000, 600]
        ])
                              
    expected_y = np.array([ 600,  700,  600,  400, 1000,  600,  700])
    
    np.testing.assert_array_equal(X, expected_X)
    np.testing.assert_array_equal(y, expected_y)

def test_prepare_sequential_data_empty():
    data = np.array([])
    pas_temps = 2

    X, y = prepare_sequential_data(data, pas_temps)
    
    # Avec des données vides, les résultats doivent être des tableaux vides
    assert X.size == 0
    assert y.size == 0

def test_prepare_sequential_data_insufficient_data():
    data = np.array([[5], [10]])
    pas_temps = 3

    X, y = prepare_sequential_data(data, pas_temps)
    
    # Avec des données insuffisantes, les résultats doivent être des tableaux vides
    assert X.size == 0
    assert y.size == 0



def test_split():
    # Créer des données factices
    data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    
    # Taille du test définie à 40% (donc 60% pour le train)
    test_size = 0.4
    
    # Appeler la fonction `split`
    train_data, test_data = split(data, test_size)
    
    # Vérifications
    # Vérifier la taille des ensembles de train et de test
    assert train_data.shape[0] == 3  # 60% de 5 (le nombre total de lignes) est 3
    assert test_data.shape[0] == 2   # 40% de 5 est 2
    
    # Vérifier que les données sont bien divisées
    np.testing.assert_array_equal(train_data, np.array([[1, 2], [3, 4], [5, 6]]))
    np.testing.assert_array_equal(test_data, np.array([[7, 8], [9, 10]]))
    
    # Vérifier avec une autre taille de test
    test_size = 0.2
    train_data, test_data = split(data, test_size)
    
    assert train_data.shape[0] == 4  # 80% de 5 est 4
    assert test_data.shape[0] == 1   # 20% de 5 est 1
    
    np.testing.assert_array_equal(train_data, np.array([[1, 2], [3, 4], [5, 6], [7, 8]]))
    np.testing.assert_array_equal(test_data, np.array([[9, 10]]))