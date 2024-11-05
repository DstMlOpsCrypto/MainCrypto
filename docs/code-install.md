An exemple of codeblock 

```bash title="install..." linenums="1" hl_lines="13"
 #!/bin/bash

### clean docker
bash local_docker_clean.sh

### Install environnement
docker-compose --verbose up airflow-init

### Launch docker compose
docker-compose --verbose up -d

#wait 65s for containers to get ready
sleep 65
docker container ls

```