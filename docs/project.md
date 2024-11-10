# Project

All project has been manage through github

- project plan + roadmap
- issues

We use a flavor of XP programming to enhanced collaboration and communication (3 meetings per week included 1 to 1 dedicated meeting if necessary). 

We were focused on delivery through short delivery cycle  (more than 5 times per week) to get rapid feedback, and to keep motivation up ! 

???+ note
    [See github statistics](https://github.com/DstMlOpsCrypto/MainCrypto/pulse)


The following part sumup the setup

## Project Setup and Environment Configuration

### Tasks

* Set up the development environment (Docker, virtual environments, etc.).
* Install necessary libraries and frameworks (Airflow, MLflow, etc.).
* Set up GitHub repository for version control.

### Deliverables

* Dockerfile and docker-compose.yml for each services
* Environment configuration files
* Initial commit to GitHub

## Data Collection and Preprocessing

### Tasks

* Create Airflow DAG for data extraction from Kaggle.
* Preprocess the data (cleaning, normalization, etc.).
* Store processed data in PostgreSQL database.

### Deliverables

* Airflow DAG script for data collection
* Data preprocessing scripts
* PostgreSQL schema and data

## Model Development

### Tasks

* Develop the LSTM model for Bitcoin price prediction.
* Split data into training, validation, and test sets.
* Train the LSTM model and evaluate its performance.

### Deliverables

* LSTM model script
* Trained model artifacts
* Model evaluation metrics

## Model Tracking and Versioning

### Tasks

* Integrate MLflow for model tracking and versioning.
* Log model parameters, metrics, and artifacts in MLflow.

### Deliverables

* MLflow integration script
* MLflow server setup
* Model version tracking in MLflow

## API Development

### Tasks

* Develop a private API for sensitive operations (training, etc.)
* Develop a bridge API for communication with the frontend, the private API and other services
* Create endpoints for data input and output.

### Deliverables

* FastAPI application for model management (prédiction, training, etc.)
* FastAPI application for authentication and communication with the frontend
* API documentation

## Monitoring and Logging

### Tasks

* Set up Prometheus for monitoring logs and metrics.
* Configure Prometheus to trigger Airflow DAGs based on log metrics.
* Integrate Kibana for log visualization.

### Deliverables

* Prometheus configuration files
* Kibana dashboards
* Alerts and triggers configuration

## Visualization Dashboard

### Tasks

* Develop Streamlit dashboard for visualizing model predictions and metrics, manage users and assets.
* Integrate Streamlit with Gateway API to access backend services.

### Deliverables

* Streamlit application.

## Testing and Validation

### Tasks

* Perform end-to-end testing of the MLOps pipeline.
* Validate the accuracy and reliability of predictions.
* Gather feedback from stakeholders and make necessary adjustments.

### Deliverables

* Test cases and results
* Validation report

## Deployment

### Tasks

* Deploy the entire MLOps pipeline to a developement environment included unit tests
* Deploy the entire MLOps pipeline to a production environment (VM EC2 DataScientest).
* Ensure all components are correctly integrated and functional.

### Deliverables

* Deployment scripts under Githhub Actions
* Live development system with test
* Live production system

## Documentation

### Tasks:

* Document the entire project, including setup instructions, usage guidelines, and technical details.
* Prepare a presentation for the jury explaining the project objectives, process, and outcomes.

### Deliverables

* Comprehensive project documentation
* Presentation document under [MkDocs](https://www.mkdocs.org/)


# Project Timeline 

* Week 1-2: Project Setup and Environment Configuration
* Week 3-4: Data Collection and Preprocessing
* Week 5-6: Model Development
* Week 7-8: Model Tracking and Versioning
* Week 9: API Development
* Week 10-11: Monitoring and Logging
* Week 12: Visualization Dashboard
* Week 13-14: Testing and Validation
* Week 15: Deployment :rocket:
* Week 16: Documentation 

???+ note
    [Github project](https://github.com/orgs/DstMlOpsCrypto/projects/1)
