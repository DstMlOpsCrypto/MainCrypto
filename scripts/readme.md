
# procedure en local
Install Python version 3.12.4
Use gestionnaire de dépendance comme virtualenv :
pip install virtualenv

## Installer les dépendances :
pip install --no-cache-dir -r scripts/requirements.txt

# Entrainement
cd scripts
Script are launched with avec two compulsory parameters :
python3 train.py --currency= <currency> --period = <period>

2 options for currency : 'BCT-EUR' or 'BTC-USD', represent the currenct : Euro or US dollar
2 options for period : '1d' or '5d' : represents the period chosen for the prediction, 1 day or 5 days.

# Prévision
cd scripts
Script are launched with avec two compulsory parameters :
python3 predict.py --currency= <currency> --period = <period>

2 options for currency : 'BCT-EUR' or 'BTC-USD', represent the currenct : Euro or US dollar
2 options for period : '1d' or '5d' : represents the period chosen for the prediction, 1 day or 5 days.

# Unit testing
Run pytest in tests/unit
