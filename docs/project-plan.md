# Project Plan

## Project Setup and Environment Configuration

### Tasks

* Set up the development environment (Docker, virtual environments, etc.).
* Install necessary libraries and frameworks (TensorFlow, Airflow, MLflow, etc.).
* Set up GitHub repository for version control.

### Deliverables

* Dockerfile and docker-compose.yml
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

* Develop FastAPI endpoints for model predictions.
* Create endpoints for data input and output.

### Deliverables

* FastAPI application script
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

* Develop Streamlit dashboard for visualizing model predictions and metrics.
* Integrate Streamlit with PostgreSQL to fetch data and display results.

### Deliverables

* Streamlit dashboard script
* Dashboard components and features

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

* Deploy the entire MLOps pipeline to a production environment.
* Ensure all components are correctly integrated and functional.

### Deliverables

* Deployment scripts
* Live production system

## Documentation

### Tasks:

* Document the entire project, including setup instructions, usage guidelines, and technical details.
* Prepare a presentation for the jury explaining the project objectives, process, and outcomes.

### Deliverables

* Comprehensive project documentation
* Presentation slides


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
