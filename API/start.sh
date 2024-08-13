#! /usr/bin/env sh
# arrête le script immédiatement si une erreur se produit
set -e

# Ajoute le répertoire actuel au chemin Python
export PYTHONPATH=$PYTHONPATH:/:/app

# Détecte l'emplacement du fichier principal de l'application
if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi

# Définit le nom du module et de la variable principale de l'application
# Si MODULE_NAME n'est pas défini, utilise DEFAULT_MODULE_NAME
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}

# Définit le nom de l'application
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

# Récupère la configuration de Gunicorn
if [ -f /app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
elif [ -f /app/app/gunicorn_conf.py ]; then
    DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
else
    DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
fi
# Exporte le chemin du fichier de configuration de Gunicorn
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"

if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else 
    echo "There is no script $PRE_START_PATH"
fi

# Démarre Gunicorn avec Uvicorn comme worker
# -k spécifie le type de worker (ici, UvicornWorker)
# -c spécifie le fichier de configuration
# Le dernier argument est le module et la variable de l'application à exécuter
exec gunicorn -k uvicorn.workers.UvicornWorker -c "$GUNICORN_CONF" "$APP_MODULE"
