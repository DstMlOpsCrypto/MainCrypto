from src.models.model_LSTM import*
from keras.models import Sequential
import datetime
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


# callbacks
def create_callbacks():
    """
    Creates two training callbacks:
    
    - EarlyStopping: Stops training if "val_loss" doesn't improve by at least 0.0001 after 8 epochs, restoring the best model weights.
    - ReduceLROnPlateau: Reduces the learning rate by a factor of 0.0001 if "val_loss" plateaus for 5 epochs, with a cooldown period of 3 epochs and a minimum learning rate of 1e-6.
    
    Returns:
        tuple: (early_stopping, reduce_learning_rate)
    """
    early_stopping = EarlyStopping(monitor="val_loss",
                                min_delta = 0.0001,
                                patience = 8,
                                verbose=1,
                                restore_best_weights = True)

    reduce_learning_rate = ReduceLROnPlateau(monitor="val_loss",
                                                patience = 5,
                                                factor = 0.0001,
                                                cooldown = 3,
                                                verbose=1,min_lr = 1e-6)
    return early_stopping,reduce_learning_rate


def train(X_train, y_train, X_test, y_test, model, batch_size = 5):
    """
    Fit the model acccording to the data and measure duration of the training process.
    Args:
    :param X_train, y_train, X_test, y_test: Train and test data
    :param batch_size: batch size during training, value 5 by defaut
    :param model: Sequential ML model
    Return: history object, fitted model and duration of the traing step in seconds
    """    
    
    #callbacks
    early_stopping,reduce_learning_rate = create_callbacks()
       
    #entrainement
    history, model, duration_seconds = model.fit(X_train, y_train, X_test, y_test, early_stopping, reduce_learning_rate, batch_size= batch_size)
    
    return history, model, duration_seconds


