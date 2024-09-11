# Introduction
Cryptocurrency markets are highly volatile, making price prediction a challenging task. This project leverages machine learning models to predict future prices of cryptocurrencies. 


## Index

- [Introduction](#Introduction)
- [Purpose](#purpose)
- [Project-structure](#project-structure)
- [Pre-Requisites](#pre-requisites)
- [Installation](#installation)
  - [Development-Environment](#development-environment)
    - [Data-Processing](#data-processing)
    - [fastAPI](#fastapi)
    - [MLFlow](#mlflow)  
  - [Build](#build)  
- [Deployment](#deployment)
- [Usage](#usage)
- [Contribution](#contribution)
- [Resources](#resources)
- [Gallery](#gallery)
- [Credit/Acknowledgment](#creditacknowledgment)
- [License](#license)


# Purpose 

This project is made available to everyone for educational purposes, it cannot be used in production.
Architecture is based on 3 VM (EC2) spread on 3 different AWS unmanaged accounts.

Meanwhile this light architecture, this project aimed to implement a (almost) full CI/CD based on Github Actions, docker, MLflow, fastAPI, graphical UI.
Trunk branching strategy is used.

# Project-Structure

This project is composed of 4 directories (app)
- db : oHCLVT data are stored in postgreSQL 
- mlflow : MLflow components
- fastapi : API used by external users for inference

For local test, for each app, bash scripts allowed developer to facilitate requiired components. A requirements.txt file is present for python

TO COMPLETE

# Pre-Requisites
List all the pre-requisites the system needs to develop this project.
This project is adapted to a Linux environment and as been tested on 
- Arch Linux - Linux 6.10.3
- Ubuntu|Debian

# Installation

- clone the repo

```
git clone https://github.com/DstMlOpsCrypto/MainCrypto.git
cd MainCrypto.git
```

## Development-Environment
To set up a local environment with Docker, PostgreSQL on Docker, and Python, follow these steps: 

### install Docker and Docker compose on your linux machine. 

Script : local_docker_install.sh file

The script follow these steps:

- update system
- install docker
- install docker-compose

### Install environnement

```bash
docker-compose up airflow-init

docker-compose up -d
```

### Airflow

DAG refer to connection id set withing airflow.
Setting this connection to "Data server" is mandatory to run DAG

#### Launch Airflow

- Point to '0.0.0.0:8080' on your browser
- login: airflow
- password: airflow

#### Setting connection

- goto /administration
- goto /connection
  - name: postgres_crypto
  - type : Postgres
  - service/host: db
  - database: cryptoDb
  - user: crypto
  - pw: crypto
  - port: 5432
- save

#### Run DAG

Current DAG "crypto_ohcl_dag.py" do following actions
- get all assets (list) from table "assets" withing CryptoDb database
- for each assets, get current crypto price

The DAG is forcast to run every 1 mn (for dev purpose)
By default the DAG is on standby. Just toggle it and wait

### Pgadmin

#### Launch pgadmin

- Point to '0.0.0.0:8888' on your browser
- login : admin@admin.com
- password : admin

#### Connect to Servers (containers)

- **Airflow server**
  - host(service): postgres
  - user: airflow
  - pw: airflow
- **Data server**
  - host(service): db
  - user: crypto
  - pw: crypto

Goto Public to see shemas

### Remove Docker, Docker compose and containers cache

Script : local_docker_clean.sh file

The script follow these steps:

- Stop all running containers
- Remove all stopped containers
- Remove all images
- Remove any  volumes
- Remove any  networks
- Remove all unused data

The script "local_dockercompose_remove.sh" uninstall docker and docker-compose.

### Usefull Commands

```bash
# check compose version
docker compose version

# check if docker is running
sudo systemctl status docker

# check containers
docker-compose ps
docker ps

# check the connection to a PostgreSQL database
docker exec -it {container-id or container-name} -U postgres

# List all databases
docker exec -it "$CONTAINER_NAME" psql -U postgres -c "\l"
docker exec -it 2c356056a66b psql -U postgres -c "\l"

# list all table commend sql \dt+
docker exec -it {container-id or container-name} psql -U "{user}" -d "{db_name}" -c "\dt+"
docker exec -it cpostgres psql -U postgres -d ohlcvt -c "\dt+"

# List all columns properties for specific table
docker exec -it {container-id or container-name} psql -U "{user}" -d "{db_name}" -c "\d+ {table_name}"

# view data from a PostgreSQL table
docker exec -it {container-id or container-name} psql -U "{user}" -d "{db_name}" -c "SELECT * FROM {table_name};"
```

## fastAPI


## MLFlow


## Build
Write the build Instruction here.



## Deployment
Write the deployment instruction here.

# Usage
TBD

# Contribution

 Your contributions are always welcome and appreciated. Following are the things you can do to contribute to this project.

##  Resources
Add important resources here

##  Gallery
Pictures of your project.

## Credit/Acknowledgment
Credit the authors here.

##  License
Add a license here, or a link to it.



The coordination and automation of data flow across various tools and systems to deliver quality data products and analytics.

Manual and error-prone processes
Lack of standards around data formats, processes, and processing techniques

Time-based scheduling tools (e.g., Cron)
 Rise of proprietary scheduling and workload management tools (e.g., AutoSys)


*An increase in data size and complexity of scheduling and workloads
 *Tools that were designed for specific ecosystems (e.g., Hadoop)



# airflow https://www.youtube.com/watch?v=In7zwp0FDX4