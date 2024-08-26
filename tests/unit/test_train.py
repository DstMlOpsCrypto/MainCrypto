from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from src.models.train_model import create_callbacks, train
from unittest.mock import MagicMock, patch

def test_create_callbacks():
    early_stopping, reduce_learning_rate = create_callbacks()

    # Test EarlyStopping callback
    assert isinstance(early_stopping, EarlyStopping)
    assert early_stopping.monitor == "val_loss"
    assert early_stopping.min_delta == 0.0001
    assert early_stopping.patience == 8
    assert early_stopping.verbose == 1
    assert early_stopping.restore_best_weights == True

    # Test ReduceLROnPlateau callback
    assert isinstance(reduce_learning_rate, ReduceLROnPlateau)
    assert reduce_learning_rate.monitor == "val_loss"
    assert reduce_learning_rate.patience == 5
    assert reduce_learning_rate.factor == 0.0001
    assert reduce_learning_rate.cooldown == 3
    assert reduce_learning_rate.min_lr == 1e-6
    assert reduce_learning_rate.verbose == 1
    

@patch('src.models.train_model.create_callbacks')
def test_train(mock_create_callbacks):
    # Mocking the callbacks
    mock_early_stopping = MagicMock()
    mock_reduce_learning_rate = MagicMock()
    mock_create_callbacks.return_value = (mock_early_stopping, mock_reduce_learning_rate)
    
    # Mocking the model and its fit method
    mock_model = MagicMock()
    mock_history = MagicMock()
    mock_model.fit.return_value = (mock_history, mock_model, 100)  # Example duration in seconds

    # Dummy data
    X_train = MagicMock()
    y_train = MagicMock()
    X_test = MagicMock()
    y_test = MagicMock()
    batch_size = 10

    # Call the train function
    history, trained_model, duration = train(X_train, y_train, X_test, y_test, mock_model, batch_size)

    # Assertions
    mock_create_callbacks.assert_called_once()
    mock_model.fit.assert_called_once_with(X_train, y_train, X_test, y_test, mock_early_stopping, mock_reduce_learning_rate, batch_size=batch_size)
    
    assert history == mock_history
    assert trained_model == mock_model
    assert duration == 100  # Example duration