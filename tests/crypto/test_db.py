import pytest
import psycopg2
import os

def test_postgres_cryptodb_connection():
    # Establish a connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            host=os.environ.get('CRYPTO_DB_HOST'),
            port=os.environ.get('CRYPTO_DB_PORT'),
            dbname=os.environ.get('CRYPTO_DB_NAME'),
            user=os.environ.get('CRYPTO_DB_USER'),
            password=os.environ.get('CRYPTO_DB_PASSWORD')
        )
        print(
            os.environ.get('CRYPTO_DB_HOST'),
            os.environ.get('CRYPTO_DB_PORT'),
            os.environ.get('CRYPTO_DB_NAME'),
            os.environ.get('CRYPTO_DB_USER'),
            os.environ.get('CRYPTO_DB_PASSWORD')
        )
        cur = conn.cursor()
        cur.execute("SELECT asset FROM public.assets")
        records = cur.fetchall()
        assert len(records) > 0
        conn.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to PostgreSQL: {e}")