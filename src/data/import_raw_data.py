import datetime
import yfinance as yf
from datetime import date
import pandas as pd
import numpy as np
import sys
import os
from psycopg2.extras import RealDictCursor
from sklearn.preprocessing import MinMaxScaler

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.features.preprocess import normalize_data, normalize_data2
from src.data.database import get_db

def load_data(ticker, start = "2014-07-01", end = "2024-08-01", interval = "1d", start_new_data = "2024-08-01"):
    """
    Load historical and new data for a given ticker symbol from Yahoo Finance using the yfinance library.
    Args:
        ticker (str): The ticker symbol for the financial instrument.
        start (str, optional): The start date for the historical data in the format "YYYY-MM-DD". Defaults to "2014-07-01".
        end (str, optional): The end date for the historical data in the format "YYYY-MM-DD". Defaults to "2024-08-01".
        interval (str, optional): The interval for the historical data. Defaults to "1d".
        start_new_data (str, optional): The start date for the new data in the format "YYYY-MM-DD". Defaults to "2024-08-01".
    Returns:
        pandas.DataFrame: A DataFrame containing the concatenated historical and new data.

    Raises:
        Exception: If there is an error loading the data.
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

def load_data_2(table):
    """
    """
    try:
        conn = get_db()
        with get_db() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"SELECT * FROM {table}"
            df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

#old way
def load_transform_data(period, ticker): 
    """
    """
    # Loading
    df = load_data (ticker=ticker, start = "2014-07-01", end = "2024-08-01", interval = period, start_new_data = "2024-08-01")
    print("Chargement des données effectué")

    print(df)

    #Transformation
    # removal of useless columns 
    if period == '1d':
        df = df.drop(columns= ['Open','High','Low','Dividends','Stock Splits','Volume'], axis=1)
    else :
        df = df.drop(columns=['Open','High','Low','Volume'], axis=1) 
    
    # tf en tableau numpy
    df_array = np.array(df)
    
    # Data Normalization
    df_array, df_index, scaler = normalize_data(df= df, period=period)
    print(df_array)
    print("Normalisation des données effectuée")
    
    return df_array, df.index, scaler


#new_way
def load_data_2(table):
    """
    Récupère les données d'une table spécifique et retourne un DataFrame Pandas.
    """
    conn = get_db()  # Obtenir la connexion
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = f"SELECT * FROM {table}"  # Construire la requête SQL
            df = pd.read_sql_query(query, conn)  # Charger les données dans un DataFrame Pandas
        return df  # Retourner le DataFrame
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    finally:
        conn.close()  # Toujours fermer la connexion à la base de données
    
def load_transform_data2(table,period):
    """
    Récupère les données d'une table spécifique, retourne un DataFrame Pandas après l'avoir normalisé.
    """
    conn = get_db()  # Obtenir la connexion
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = f"SELECT * FROM {table}"  # Construire la requête SQL
            df = pd.read_sql_query(query, conn)  # Charger les données dans un DataFrame Pandas
            df_array, df_index, scaler = normalize_data2(df= df, period=period)
            print("Normalisation des données effectuée")            
        return df_array, df.index, scaler # Retourner le DataFrame
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    finally:
        conn.close()  # Toujours fermer la connexion à la base de données
        
