# Utiliser une image de base Airflow
FROM apache/airflow:2.10.0

# Passer à l'utilisateur root pour les installations
USER root

# Mettre à jour le système et installer Python, pip, et les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && pip3 install --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installer les packages Python nécessaires
RUN pip3 install tensorflow mlflow yfinance --upgrade typing_extensions pytest

# Revenir à l'utilisateur airflow
USER airflow