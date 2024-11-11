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