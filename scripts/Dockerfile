# # Utiliser une image de base Airflow
# FROM apache/airflow:2.10.0

# USER root

# # RUN apt-get update --fix-missing --allow-releaseinfo-change-suite --yes --no-install-recommends

# RUN apt-get update

# RUN apt-get install -y --no-install-recommends --fix-missing\
#     python3 \
#     python3-pip \
#     python3-venv \
#     git

# USER airflow

# RUN pip3 install --upgrade pip \
#     && pip install tensorflow \
#     && pip install mlflow \
#     && pip install yfinance \
#     && pip install pytest \
#     && pip install psycopg2-binary \
#     && pip install SQLAlchemy \
#     && pip install --upgrade typing_extensions

# USER root

# RUN apt-get clean

# USER airflow

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
    
# Mise à jour et installation de Python et des utilitaires requis
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     python3 \
#     python3-pip \
#     python3-venv \
#     git \
#     && apt-get clean

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

# # Mettre à jour pip pour l'utilisateur airflow et installer les packages requis
# RUN /home/airflow/.local/bin/pip install --upgrade pip \
#     && /home/airflow/.local/bin/pip install \
#     tensorflow \
#     mlflow \
#     yfinance \
#     pytest \
#     psycopg2-binary \
#     requests\
#     uvicorn\
#     gunicorn\ 
#     --upgrade typing_extensions

# RUN /home/airflow/.local/bin/pip install --upgrade "sqlalchemy>=2.0"

# # Ajouter le chemin d'accès à /home/airflow/.local/lib/python3.12/site-packages/ à la variable d'environnement PYTHONPATH
# ENV PYTHONPATH=/home/airflow/.local/lib/python3.12/site-packages:$PYTHONPATH

# # Vérifier que les packages sont bien installés
# RUN /home/airflow/.local/bin/pip show mlflow && /home/airflow/.local/bin/pip show yfinance

# # Set the PYTHONPATH environment variable to the root directory and app directory
# ENV PYTHONPATH=/app