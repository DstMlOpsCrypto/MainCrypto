 #!/bin/bash

### clean docker
bash local_docker_clean.sh

# Que je dois executer avant de lancer le script / à résoudre pour la suite et éviter de devoir faire ces manips
# sudo chown -R 50000:0 airflow/logs/
# sudo chmod -R 777 airflow/logs/
# sudo chown -R ubuntu:ubuntu mlflow-artifacts/
# sudo chmod -R 777 mlflow-artifacts/
# export AIRFLOW_UID=50000

bash se### Launch docker compose stats-exporter, model-score-sender and p airflow-init
docker-compose up stats-exporter model-score-sender

docker-compose up airflow-init

### Launch docker compose
docker-compose up -d

#wait 65s for all containers to get ready
sleep 65
docker container ls