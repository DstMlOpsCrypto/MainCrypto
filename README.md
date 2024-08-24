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
- launch docker-compose.yml

The script "local_dockercompose_remove.sh" uninstall docker and docker-compose.

### Command

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

## Data-Processing

- TODO :
  - cronjob feed historical data by user manuel upload (csv)
  - cronjob feed realtime data from currency list (csv)
  - (option : install airflow)
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
