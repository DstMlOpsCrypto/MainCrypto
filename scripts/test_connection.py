# test_db_connection.py

from sqlalchemy import create_engine

# Connection string format for PostgreSQL
engine = create_engine("postgresql+psycopg2://crypto:crypto@db:5432/cryptoDb")

# Test the connection
try:
    connection = engine.connect()
    print("Connection to the database was successful!")
except Exception as e:
    print(f"Failed to connect to the database: {e}")
finally:
    connection.close()
