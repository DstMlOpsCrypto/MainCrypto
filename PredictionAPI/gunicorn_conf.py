import json
import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "3001")  # Changed to 3001

use_loglevel = os.getenv("LOG_LEVEL", "debug")

bind_env = os.getenv("BIND", None)

if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores

if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)

loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
keepalive = 120
timeout = 1800 # 30 minutes timeout
errorlog = "-"

log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "workers_per_core": workers_per_core,
    "host": host,
    "port": port,
}

print(json.dumps(log_data))

forwarded_allow_ips = '*'
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}