import pandas as pd
import sys
import os
from psycopg2.extras import RealDictCursor

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.features.preprocess import normalize_data2
from src.data.database import get_db

def load_data_2(table, asset):
    """
    Récupère les données d'une table spécifique et retourne un DataFrame Pandas.
    """
    conn = get_db()  # Obtenir la connexion
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = f"SELECT * FROM {table} WHERE asset='{asset}' ORDER BY dtutc DESC"  # Construire la requête SQL
            df = pd.read_sql_query(query, conn)  # Charger les données dans un DataFrame Pandas
        return df  # Retourner le DataFrame
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    finally:
        conn.close()  # Toujours fermer la connexion à la base de données


