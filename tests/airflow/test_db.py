import pytest
import psycopg2
import os


def test_postgres_airflow_tables():
    # Add assertions to check if the database connection is established
    try:
        conn = psycopg2.connect(
            host=os.environ.get('AIRFLOW_DB_HOST'),
            port=os.environ.get('AIRFLOW_DB_PORT'),
            dbname=os.environ.get('AIRFLOW_DB_NAME'),
            user=os.environ.get('AIRFLOW_DB_USER'),
            password=os.environ.get('AIRFLOW_DB_PASSWORD')
        )
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        records = cur.fetchall()
        assert len(records) > 0
        conn.close()
    except Exception as e:
        pytest.fail(f"Failed to query PostgreSQL airflow: {e}")
