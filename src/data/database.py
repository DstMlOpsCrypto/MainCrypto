import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import asynccontextmanager


def get_db():
    conn = psycopg2.connect(
        dbname="cryptoDb",
        user="crypto",
        password="crypto",
        host="db",
        port="5432"
    )
    return conn