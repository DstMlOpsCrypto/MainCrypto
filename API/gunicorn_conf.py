# Ce fichier est utilisé pour configurer Gunicorn, le serveur web utilisé par FastAPI
# Il utilise Uvicorn comme worker (gestionnaire de requêtes)
import json
import multiprocessing
import os

# Récupération des variables ou valeurs par défaut
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "3000")

use_loglevel = os.getenv("LOG_LEVEL", "debug") # du moins détaillé au plus détaillé : ERROR, WARNING, INFO, DEBUG

# Récupération de l'adresse de liaison depuis une variable d'environnement, par défaut None
bind_env = os.getenv("BIND", None)

# Si une adresse de liaison est spécifiée, l'utiliser, sinon utiliser host:port
if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

# Détermination du nombre de cœurs CPU et calcul du nombre total de workers par défaut
cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores

# Si un nombre total de workers est spécifié, l'utiliser (doit être > 0)
# Sinon, utiliser le maximum entre le nombre calculé et 2
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
keepalive = 120
errorlog = "-" # "-" signifie que les erreurs seront envoyées sur la sortie standard

# Création d'un dictionnaire pour le débogage et les tests
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
}

# Affichage des données de configuration au format JSON
print(json.dumps(log_data))

forwarded_allow_ips = '*'
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}
