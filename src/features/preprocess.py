import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def normalize_data2(df, period):
    """
    Standardise numerical features of a DataFrame and remove some columns
    :param df: pd.DataFrame
    :columns: list of non used columns for the price prediction, which are removed
    :return: np.Array with standardized values
    """ 
    
    # removal of useless columns 
    try:
        df.drop(columns= ['asset','dtutc','open','high','low','volume','trades'], axis=1, inplace =True)   

        # recuperation de l'index
        df_index = df.index
        
        #tf en tableau numpy
        df_array = np.array(df)
        
        #instanciation du Scaler et normalisation
        scaler=MinMaxScaler(feature_range=(0,1))    
        scaled_data = scaler.fit_transform (df_array)
        
        return scaled_data, df_index, scaler
    
    except Exception as e:
        print(f"Error normalizing data: {e}")
        return None