
import datetime
from datetime import date
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def normalize_data(df, period, duration=1000):
    """
    Standardise numerical features of a DataFrame and remove some columns
    :param df: pd.DataFrame
    :columns: list of non used columns for the price prediction, which are removed
    :return: np.Array with standardized values
    """ 
    #aRécupérer la valeur de la veille
    today = date.today()
    today_date = today.isoformat() # on va récupérer les données jusqu'à celle d'hier
    start_date = today - datetime.timedelta(days=duration)

    # recup√©ration de l'index (√† voir ensuite si utile)
    df_index = df.index
    
    #tf en tableau numpy
    df_array = np.array(df)
    
    #instanciation du Scaler et normalisation
    scaler=MinMaxScaler(feature_range=(0,1))    
    scaled_data = scaler.fit_transform (df_array)

    return scaled_data, df_index, scaler

def normalize_data2(df, period):
    """
    Standardise numerical features of a DataFrame and remove some columns
    :param df: pd.DataFrame
    :columns: list of non used columns for the price prediction, which are removed
    :return: np.Array with standardized values
    """ 
    
    # removal of useless columns 
    try:
        df =df.drop(columns= ['asset','dtutc','open','high','low','volume','trades'], axis=1)   

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