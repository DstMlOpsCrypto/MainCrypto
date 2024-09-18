from sklearn.metrics import mean_squared_error,r2_score


def scaling (train_predict, test_predict, y_train, y_test, scaler):
    """
    Calcule le score du modèle sur les données de test.
    """        
    #Remise à l'échelle Xtrain, Xtest
    train_predict = train_predict/scaler.scale_[0]
    test_predict = test_predict/scaler.scale_[0]
        
    # remise à l'échelle y
    y_train = y_train.reshape(-1,1)
    y_train = y_train /scaler.scale_[0]
            
    y_test = y_test.reshape(-1,1)
    y_test = y_test/scaler.scale_[0] 
                        
    return train_predict, test_predict, y_train, y_test


def score(train_predict, test_predict, y_train, y_test):
            
    #train
    mse_train = mean_squared_error(y_train, train_predict)
    r2_score_train = r2_score(y_train, train_predict)
       
    #test
    mse_test = mean_squared_error(y_test, test_predict)
    r2_score_test = r2_score(y_test, test_predict)
        
    return mse_train, r2_score_train, mse_test, r2_score_test
