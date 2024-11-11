# CryptoPredict
![Bitcoin](https://upload.wikimedia.org/wikipedia/commons/5/5a/Bitcoin_Crypto_Sustainability.jpg){ align=center }

This project represent the final project of DataScientest MLOps exam.
This project start in July 2024 to mid November 2024

## Rational 

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
    * Yann

=== "Project management"

    Github have been used for : 

    * Code repository
    * Project management
    * Testing and deployment through Github actions


## Getting started

### Prerequisites

The following prerequisites are minimal requirements to make this repository work:

- VM with proper network configuration to allow internal external flow
- Access to [Github Actions](https://github.com/features/actions)
- Set [github secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) for target repo
    - PRIVATE_KEY : SSH private key
    - EC2_HOST: VM host
    - EC2_USER: VM user
    - GIT_PAT: user token
- VS Code or any IDE
- python environnement setup
- git setup

### Launch apps locally

- clone repo

```python
git clone https://github.com/DstMlOpsCrypto/MainCrypto.git
cd MainCrypto.git
```

- chmod +x 'setup.sh' file

You are ready to go !

The installation process is straightforward and simple, you just need to execute 'setup.sh'

```bash
sh setup.sh
```

??? Tasks-workflow

    ```mermaid
    flowchart
        subgraph install-docker-env;
            local_docker_install.sh;
        end;
        subgraph refresh-containers;
            clean-env --> init-airflow;
            init-airflow --> launch-docker-app;
        end;

        install-docker-env --> refresh-containers
    ```

    **1. Install-docker-env**

        - Prepare an environnement for linux (Debian, Fedora, CentOS, RedHat Entreprise, OpenSUSE, ArchLinux)
        - Add current user to the docker group
    **2. Refresh-containerized-apps-installation**

        - stop all containers
        - remove all stopped containers
        - remove all images
        - remove any volumes
        - remove any networks
        - remove all unused data
        - remove ./plugins folder (mapped)
        - remove ./dags folder (mapped)
    **3. Install apps from docker-compose.yml**

        - init airflow
        - launch containers


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
    prom/                   # TODO: Monitoring Service including Prometheus annd Grafana
        alertmanager/
        statsd/
    scripts/                # TODO: Models scripts for training, predicting and evaluating model 
    src/                    # TODO: Ressources and modules useful for model scripts 
        data/
        deployment/
        evaluation/
        features/
        models/
        utils/
        vizualisation/
    tests/                  # TODO: Tests repository for dev, including api, crypto datbase and modelling
        api/
        crypto/
        model/
    setup.sh                # bash script to install complete application
    local_docker_clean.sh   # Bash script to clean docker
    docker-compose.yml      # Production compose (see XX)
    docker-compose-dev.yml  # Development compose (see XX)
```

## Down the rabbit hole
![Down the Rabbit Hole](https://insatpress.tn/wp-content/uploads/2018/08/down-the-rabbit-hole-1.jpg){ align=center }

We encourage anyone to take time to refer to dedicated pages listed on header.

