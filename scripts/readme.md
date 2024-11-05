

# Construction des images Dockerfile
## Worker
Créer une image nommée "worker" :
docker build -f scripts/Dockerfile -t worker:latest .

## Tests unitaires ML
Créer une image nommée "tests-scripts-ml" :
docker build -f scripts/Dockerfile.tests -t tests-scripts-ml:latest .

## Lancement seul des tests du scripts d'entrainement et de prédiction
docker-compose up --no-deps tests-ml

# procedure en local
Install Python version 3.12.4, virtualenv

# Dépendances
apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && pip3 install --upgrade pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# training
Go into scripts repo :
cd scripts
Script are launched with avec two compulsory parameters :
python3 train.py --currency= <currency> --period = <period>

2 options for currency : 'BCT-EUR' or 'BTC-USD', represent the currenct : Euro or US dollar
# 2 options for period : '1d' or '5d' : represents the period chosen for the prediction, 1 day or 5 days.   ## removed
# exemple : python3 train.py --currency='BTC-EUR' --period='1d' # removed
exemple : python3 train.py --currency='BTC-EUR'

# Prediction
cd scripts
Script are launched with avec two compulsory parameters :
python3 predict.py --currency= <currency> --period = <period>

2 options for currency : 'BCT-EUR' or 'BTC-USD', represent the currenct : Euro or US dollar
2 options for period : '1d' or '5d' : represents the period chosen for the prediction, 1 day or 5 days.

# Unit testing
Run pytest in tests/unit