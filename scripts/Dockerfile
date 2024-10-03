# Utiliser une image de base Airflow
FROM apache/airflow:2.10.0

USER root

# RUN apt-get update --fix-missing --allow-releaseinfo-change-suite --yes --no-install-recommends

RUN apt-get update

RUN apt-get install -y --no-install-recommends --fix-missing\
    python3 \
    python3-pip \
    python3-venv \
    git

USER airflow

RUN pip3 install --upgrade pip \
    && pip install tensorflow \
    && pip install mlflow \
    && pip install yfinance \
    && pip install pytest \
    && pip install psycopg2-binary \
    && pip install SQLAlchemy \
    && pip install --upgrade typing_extensions

USER root

RUN apt-get clean

USER airflow
