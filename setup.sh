 #!/bin/bash

### clean docker
bash local_docker_clean.sh

### build images
docker build -f scripts/Dockerfile -t worker:latest .
#docker build -f scripts/Dockerfile.tests -t tests-scripts-ml:latest .


### Install environnement
bash docker-compose up airflow-init

### Launch tests
docker-compose up -d
#docker-compose up --no-deps tests-ml

# Attendre ....
wait 600

# # launch training
bash scripts/launch_training.sh

# # Attendre ....
# wait 500

# # #lauch prediction
# bash scripts/launch_prediction.sh
