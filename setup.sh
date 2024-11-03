 #!/bin/bash

### clean docker
bash local_docker_clean.sh

### Install environnement with
docker-compose build --no-cache airflow-init
docker-compose --verbose up airflow-init

### Launch tests
docker-compose --verbose up -d

#wait 65s for containers to get ready
sleep 65
docker container ls