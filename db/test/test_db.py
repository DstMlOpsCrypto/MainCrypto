import pytest
import psycopg2
import os
from datetime import datetime


def test_postgres_cryptodb_connection():
    # Establish a connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'cryptoDb'),
            user=os.environ.get('POSTGRES_USER', 'crypto'),
            password=os.environ.get('POSTGRES_PASSWORD', 'crypto'),
            host=os.environ.get('POSTGRES_HOST', 'db'),
            port=os.environ.get('POSTGRES_PORT', '5450')
        )
        cur = conn.cursor()
        cur.execute("SELECT asset FROM public.assets")
        records = cur.fetchall()
        assert len(records) > 0
        conn.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to PostgreSQL: {e}")

def test_postgres_airflow_tables():
    # Add assertions to check if the database connection is established
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'airflow'),
            user=os.environ.get('POSTGRES_USER', 'airflow'),
            password=os.environ.get('POSTGRES_PASSWORD', 'airflow'),
            host=os.environ.get('POSTGRES_HOST', 'postgres'),
            port=os.environ.get('POSTGRES_PORT', '5432')
        )
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        records = cur.fetchall()
        assert len(records) > 0
        conn.close()
    except Exception as e:
        pytest.fail(f"Failed to query PostgreSQL airflow: {e}")
