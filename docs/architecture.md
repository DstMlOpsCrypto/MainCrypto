# Architecture


## Capacity 

Our standard methodology has involved several key steps: 
- data collection
- data loading and preprocessing (normalization, transformation)
- model creation
- model training
- model prediction and evaluation
- model deployment. 


## Architecture layers

### Business


### Applicative

Basic scheme of the application :

Version 1 :

```mermaid
graph TB
    subgraph Public Network
        Streamlit[Streamlit Frontend]
        Gateway_Public[Gateway API]
    end
    
    subgraph Private Network
        Gateway_Private[Gateway API]
        PredictionAPI[Prediction API]
        PostgreSQL[(PostgreSQL)]
        Airflow[Airflow]
        MLflow[MLflow]
        
        subgraph Monitoring
            Prometheus[Prometheus]
            Grafana[Grafana]
        end
    end
    
    %% Public to Private connections
    Streamlit -->|HTTP| Gateway_Public
    Gateway_Public ===|Same Service| Gateway_Private
    
    %% Gateway API connections
    Gateway_Private -->|HTTP| PredictionAPI
    Gateway_Private -->|SQL| PostgreSQL
    Gateway_Private -->|HTTP| Airflow
    
    %% Prediction API connections
    PredictionAPI -->|SQL| PostgreSQL
    PredictionAPI -->|HTTP| Airflow
    PredictionAPI -->|HTTP| MLflow
    
    %% Airflow connections
    Airflow -->|SQL| PostgreSQL
    Airflow -->|HTTP| MLflow
    
    %% Monitoring connections
    Prometheus -->|Metrics| PredictionAPI
    Prometheus -->|Metrics| Airflow
    Prometheus -->|Metrics| MLflow
    Grafana -->|Query| Prometheus

    %% Styling
    classDef public fill:#f9f,stroke:#333,stroke-width:2px
    classDef private fill:#bbf,stroke:#333,stroke-width:2px
    classDef monitoring fill:#bfb,stroke:#333,stroke-width:2px
    
    class Streamlit,Gateway_Public public
    class Gateway_Private,PredictionAPI,PostgreSQL,Airflow,MLflow private
    class Prometheus,Grafana monitoring
```

Version 2 (Service-focused):

```mermaid
graph LR
    Streamlit[Streamlit Frontend]
    Gateway[Gateway API]
    PredictionAPI[Prediction API]
    PostgreSQL[(PostgreSQL)]
    Airflow[Airflow]
    MLflow[MLflow]
    Prometheus[Prometheus]
    Grafana[Grafana]
    
    %% Main application flow
    Streamlit -->|HTTP| Gateway
    Gateway -->|HTTP| PredictionAPI
    Gateway -->|SQL| PostgreSQL
    Gateway -->|HTTP| Airflow
    
    %% Prediction API connections
    PredictionAPI -->|SQL| PostgreSQL
    PredictionAPI -->|HTTP| Airflow
    PredictionAPI -->|HTTP| MLflow
    
    %% Airflow connections
    Airflow -->|SQL| PostgreSQL
    Airflow -->|HTTP| MLflow
    
    %% Monitoring
    Prometheus -->|Metrics| PredictionAPI
    Prometheus -->|Metrics| Airflow
    Prometheus -->|Metrics| MLflow
    Grafana -->|Query| Prometheus

    %% Styling
    classDef frontend fill:#f9f,stroke:#333,stroke-width:2px
    classDef api fill:#bbf,stroke:#333,stroke-width:2px
    classDef storage fill:#fbb,stroke:#333,stroke-width:2px
    classDef monitoring fill:#bfb,stroke:#333,stroke-width:2px
    
    class Streamlit frontend
    class Gateway,PredictionAPI,Airflow,MLflow api
    class PostgreSQL storage
    class Prometheus,Grafana monitoring
```

### Technologique

