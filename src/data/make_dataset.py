
import numpy as np


def prepare_sequential_data(data, pas_temps):
    """
    Create an Array with adequate train and target sequences on the basis of original data.
    :param pas_temps: number of previous days used for LSTM prediction
    :param data: Standardized np.array
    """
    # Emply lists creation
    X = []  
    y = []
    
    #filling lists
    for i in range(data.shape[0]-pas_temps):
        a = data[i:(i+pas_temps), 0]   
        X.append(a)                             
        y.append(data[i+pas_temps, 0])
              
    return np.array(X),np.array(y) 

def split(data, test_size):
    """.git/
    Split data into train and test data.
    args:
    - data: np.array
    - test_size: fraction size of the data used for testing
    return:
    train_data, test_data
    """
    size = int(len(data)*(1-test_size))    
    train_data, test_data = data[:size,:], data[size:,:]
    
    return train_data, test_data 
    
def make_dataset(data, pas_temps, test_size=0.3):
    """
    Create sequencial data for training LSTM model, with parameter pas_temps.
    :param data: np.array
    :param test_size: fraction size of the test data
    :param pas_temps: number of previous days to incorporate in the training sequence
    :return: np.Array with standardized values
    """
    #Train and test data split
    train_data, test_data = split(data, test_size)
    
    # Train and test datasets creation with sequencing
    X_train, y_train = prepare_sequential_data(data=train_data,pas_temps=pas_temps)
    X_test, y_test = prepare_sequential_data(data=test_data,pas_temps=pas_temps)
    
    #mise en forme des données pour le réseau LSTM
    X_train = X_train.reshape(X_train.shape[0],X_train.shape[1],1)
    X_test = X_test.reshape(X_test.shape[0],X_test.shape[1],1)
    
    return X_train, X_test, y_train, y_test

def make_dataset_for_testing(data, pas_temps):
    """
    Create sequencial data for testing LSTM model, with parameter pas_temps.
    :param data: np.array
    :param test_size: fraction size of the test data
    :param pas_temps: number of previous days to incorporate in the training sequence
    :return: np.Array with standardized values
    """
    
    # Empty X list creation
    X = []  
    
    #filling X
    a = data[-pas_temps:-1, 0]   
    X.append(a)                             
    
    X = np.array(X)
         
    #mise en forme des données pour le réseau LSTM
    X = X.reshape(X.shape[0],X.shape[1],1)

    return X
    