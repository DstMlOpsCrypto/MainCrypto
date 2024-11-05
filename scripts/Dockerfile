# Utiliser l'image de base Airflow
FROM apache/airflow:2.10.0

# Basculer en mode root pour installer des dépendances système
USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libpq-dev \
        gcc \
        g++ \
        python3 \
        python3-pip \
        python3-venv \
        git
    
# Revenir à l'utilisateur airflow
USER airflow

RUN pip3 install --upgrade pip

RUN pip install --no-cache-dir \
tensorflow \
mlflow \
yfinance \
pytest \
psycopg2-binary \
apache-airflow \
requests

USER root

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
