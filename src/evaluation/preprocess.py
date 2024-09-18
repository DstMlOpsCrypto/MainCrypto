
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def normalize_data(df, period):
    """
    Standardise numerical features of a DataFrame and remove some columns
    :param df: pd.DataFrame
    :columns: list of non used columns for the price prediction, which are removed
    :return: np.Array with standardized values
    """ 
    
    # removal of useless columns 
    if period == '1d':
        df =df.drop(columns= ['Open','High','Low','Dividends','Stock Splits','Volume'], axis=1)
    else :
        df =df.drop(columns=['Open','High','Low','Volume'], axis=1)    
    
    # recupération de l'index (à voir ensuite si utile)
    df_index = df.index
    
    #tf en tableau numpy
    df_array = np.array(df)
    
    #instanciation du Scaler et normalisation
    scaler=MinMaxScaler(feature_range=(0,1))    
    scaled_data = scaler.fit_transform (df_array)

    return scaled_data, df_index, scaler