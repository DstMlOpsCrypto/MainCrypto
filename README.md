# Introduction
Cryptocurrency markets are highly volatile, making price prediction a challenging task. This project leverages machine learning models to predict future prices of cryptocurrencies. 


## Index

- [Introduction](#Introduction)
- [Usage](#usage)
  - [Installation](#installation)
  - [Commands](#commands)
- [Development](#development)
  - [Pre-Requisites](#pre-requisites)
  - [Developmen Environment](#development-environment)
  - [File Structure](#file-structure)
  - [Build](#build)  
  - [Deployment](#deployment)  
- [Community](#community)
  - [Contribution](#contribution)
  - [Branches](#branches)
  - [Guideline](guideline)  
- [FAQ](#faq)
- [Resources](#resources)
- [Gallery](#gallery)
- [Credit/Acknowledgment](#creditacknowledgment)
- [License](#license)


# Purpose 

This project is made available to everyone for educational purposes, it cannot be used in production.
Architecture is based on 3 VM (EC2) spread on 3 different AWS unmanaged accounts.

Meanwhile this light architecture, this project aimed to implement a (almost) full CI/CD based on Github Actions, docker, MLflow, fastAPI, graphical UI.
Trunk branching strategy is used.

# Project structure

This project is composed of 4 directories (app)
- db : oHCLVT data are stored in postgreSQL 
- mlflow : MLflow components
- fastapi : API used by external users for inference

For local test, for each app, bash scripts allowed developer to facilitate requiired components. A requirements.txt file is present for python

TO COMPLETE

### Pre-Requisites
List all the pre-requisites the system needs to develop this project.
This project is adapted to a Linux environment and as been tested on 
- Arch Linux - Linux 6.10.3
- xxx

# Installation


- clone the repo

```
git clone https://github.com/DstMlOpsCrypto/MainCrypto.git
cd MainCrypto.git
```

## Development Environment
To set up a local environment with Docker, PostgreSQL on Docker, and Python, follow these steps: 

- install Docker on your linux machine. Use local_docker_install.sh file
- pull the PostgreSQL image by running docker pull postgres in your terminal by using local_postgrSQL_install.sh
- install python virtualenv and dependencies by using se local_venv_install.sh

### Data processing process

- launch test to ensure everything is operational. Tests are located in /{app}/tests
- load historical (extract) ohclvt data file in db by using  TODO
```python
pytest {app}/tests/
```
### fastAPI


*
Next, create and run a PostgreSQL container using the command docker run --name my_postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres. Ensure you have Python installed on your machine; if not, download and install it from the official Python website. You can then use pip to install any necessary Python packages. Finally, connect your Python application to the PostgreSQL database by using a library like psycopg2 and configuring the connection parameters to match those of your Docker container. This setup will provide a robust local development environment with all the necessary components.


## Build
Write the build Instruction here.

## Deployment
Write the deployment instruction here.

# Usage
TBD

## Historical Data ingestion
TBD

## Real Time data ingestion
TBD

# Model Training
TBD

# Prediction
TBD


# Monitoring and Maintenance
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
