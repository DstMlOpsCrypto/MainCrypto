
import datetime
import yfinance as yf
from datetime import date
import pandas as pd
import numpy as np

from src.features.preprocess import normalize_data

def load_data(ticker, start = "2014-07-01", end = "2024-08-01", interval = "1d", start_new_data = "2024-08-01"):
    """
    
    """
    try:       
        #Teléchargement via l'API yfinance
        #données dentrainement
        currency= yf.Ticker(ticker)       
        currency_historical = currency.history(start=start, end = end, interval = interval, auto_adjust = True)
        
        #ajouter nouvelles données
        today = date.today()
        today_date = today.isoformat() # on va récupérer les données jusqu'à celle d'hier
        yesterday = today - datetime.timedelta(days=1)

        currency_new_data = currency.history(start=start_new_data, end =  yesterday, interval = interval, auto_adjust = True)
      
        return pd.concat([currency_historical, currency_new_data], ignore_index=True) # new_data is appended to reference_data without Outcome
    
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()   # df concaténé
    


def load_transform_data(period,ticker): 
       
    df = load_data(ticker=ticker, start = "2014-07-01", end = "2024-08-01", interval = period, start_new_data = "2024-08-01")
    print("Chargement des données effectué")
    
    # Data Normalization
    df_array, df_index, scaler = normalize_data(df= df, period=period)
    print("Normalisation des données effectuée")
    
    return df_array, df.index, scaler

