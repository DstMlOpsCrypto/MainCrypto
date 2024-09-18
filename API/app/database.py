import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://crypto:crypto@db/cryptoDb"

def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        yield cursor
        cursor.close()
    finally:
        conn.close()
