 #!/bin/bash

### clean docker
bash local_docker_clean.sh

### Install environnement
docker-compose up stats-exporter model-score-sender

docker-compose up airflow-init

### Launch docker compose
docker-compose up -d

#wait 65s for containers to get ready
sleep 65
docker container ls