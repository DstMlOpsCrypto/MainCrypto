# CryptoPredict

This project represent the final project of DataScientest MLOps exam.
This project start in _XXX_ 2024 to mid November 2024

The purpose of this project have 1 Objectives : Develop a fully functional Bitcoin price prediction application 'CryptoPredict'


=== "Contraints"

    Some constraints have been listed by DataSciencetest Team :

    * Use only 1 VM on AWS EC2 (TODO: flavors)
    * Required tools to use
        * MLFlow
        * Airflow
        * Docker and Docker Compose
        * Prometheus and Kibana
        * Web Framework (we took Streamlit)
        * FastAPI
        * Github with Github Actions
    * 1 Deep Learning model with re trained mecanism
    * logging mecanism

=== "Team members"

    * Frederic
    * Tristan
    * Yann :robot:

=== "Project management"

    Github have been used for : 

    * Code repository
    * Project management
    * Testing and deployment through Github actions

# Quickstart

_[list all preliminary actions to do for any users]_

## Project Plan

Tasks have been listed in specific page.

[Readmore](project-plan.md)

## Project layout

```bash
    README.md               # TODO: details instalation instruction 
    API/                    # TODO: Main API service
    PredictionAPI/          # Prediction API (see API)
    airflow/                # TODO: Data flow orchestration
        dags/
    db/                     # TODO: Database (crypto data, assets, users)
    frontend/               # TODO: Frontend (Streamlit)
        components/
        pages/
        utils/
    mlflow/                 # TODO: Models Lifecycle management (See modeling)
    notebooks/              # TODO: Models scripts (See modeling)
        exploration/
        modeling/
    prom/                   # TODO: Check with frederic/tristan
        alertmanager/
        statsd/
    scripts/                # TODO: Check with frederic/tristan 
    src/                    # TODO: Check with frederic/tristan 
        data/
        deployment/
        evaluation/
        features/
        models/
        utils/
        vizualisation/
    tests/                  # TODO: Tests repository for dev 
        api/
        crypto/
        model/
    setup.sh                # bash script to install application
    local_docker_clean.sh   # Bash script to clean docker
    docker-compose.yml      # Production compose (see XX)
    docker-compose-dev.yml  # Development compose (see XX)
```

