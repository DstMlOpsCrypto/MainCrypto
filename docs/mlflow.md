# MLFlow 

This part presents an overview of MLflow tool for educational purposes.

## Overview 

=== "Creator"

    * **Name**: Developed by a team of engineers and data scientists at Databricks with significant contributions from the open-source community
    * **Background**: Databricks is a company founded by the creators of Apache Spark, and it focuses on providing a unified analytics platform for big data and machine learning.
    * **Contribution**: The team at Databricks developed MLflow to address the complexities of managing the machine learning lifecycle, from experimentation to deployment.

=== "Use Cases"

    * **Experiment Tracking**
    
        * Logging Parameters and Metrics: Track and compare different runs of experiments by logging parameters, metrics, and artifacts.

        * Experiment Visualization: Use the MLflow UI to visualize and compare experiments, making it easier to identify the best-performing models.

    * **Model Management**
        * Model Registry: Manage different versions of models, including their lineage, versioning, aliasing, tagging, and annotations.

        * Model Deployment: Deploy models to various environments, such as real-time serving through REST APIs and batch inference on Apache Spark.

    * **Reproducibility**
        * Packaging Code: Package data science work into reusable and reproducible formats using MLflow Projects.

        * Reproducible Runs: Ensure that experiments can be reproduced and shared easily, promoting collaboration and verification of results.

    * **Model Deployment**
        * Standardized Packaging: Package machine learning models in a standard format that can be used in various downstream tools.

        * Deployment to Different Environments: Deploy models to different environments, including Docker, Apache Spark, Azure ML, and AWS SageMaker.

    * **Model Evaluation**
        * Objective Comparison: Facilitate objective model comparison, whether working with traditional machine learning algorithms or advanced LLMs.

        * Evaluation Tools: Provide tools for evaluating model performance and making informed decisions.

    * **Structuring ML Projects**
        * MLflow Recipes: Offer recommendations for structuring ML projects to ensure functional end results optimized for real-world deployment scenarios.

## Main Characteristics of MLflow

### Tracking

#### Logging

MLflow Tracking provides a simple API and UI for logging various aspects of your machine learning process, such as parameters, metrics, code versions, and output files. 

This enables users to keep track of different experiments and their results, ensuring that the development and evaluation process is well-documented and reproducible.

#### Centralized Repository

All logged data is stored in a centralized repository, which captures essential details such as parameters, metrics, artifacts, data, and environment configurations. 

This centralization allows teams to gain insights into their models' evolution over time and compare different runs effectively.

### Model Registry

#### Model Management

MLflow Model Registry helps in handling different versions of models, managing their current state (e.g., staging, production), and ensuring smooth productionization. 

It provides a comprehensive platform to manage the lifecycle of machine learning models.

#### Lifecycle Management

The model registry offers APIs and a user interface to manage the full lifecycle of MLflow Models, including model lineage, versioning, aliasing, tagging, and annotations. 

This promotes collaboration and efficient model management within teams.

## Projects

### Packaging

MLflow Projects allow you to package your data science work in a reusable and reproducible format. 

A project is defined by a directory of files or a Git repository containing your code, dependencies, and entry points for running the code.

### Reproducibility

By packaging your work as an MLflow Project, you ensure that experiments can be reproduced and shared easily. This is crucial for collaboration and for verifying the results of experiments.

## Deployments

### Standardization

MLflow provides a standard format for packaging machine learning models, enabling them to be used in various downstream tools and deployment scenarios.

### Deployment

MLflow supports deploying models to different environments, including real-time serving through REST APIs and batch inference on Apache Spark. 

This versatility ensures that models can be deployed and scaled effectively across different platforms.

## Evaluate

### Model Analysis

MLflow Evaluate facilitates objective model comparison, whether you're working with traditional machine learning algorithms or advanced LLMs (large language models). It provides tools for evaluating model performance and making informed decisions.

### Evaluation Tools

The evaluation tools in MLflow help assess model accuracy, precision, recall, and other performance metrics, ensuring that the best models are selected for deployment.

### Recipes

#### Guidance

MLflow Recipes offers recommendations for structuring ML projects, ensuring that they are functional and optimized for real-world deployment scenarios. 

This guidance helps maintain consistency and best practices across different projects.

# MLflow Architecture

## MLflow Tracking

### Core Component

The MLflow Tracking component is the core of the MLflow architecture. It logs, organizes, and visualizes machine learning experiments, providing a comprehensive view of all runs and their results.

### Experiments and Runs

MLflow organizes machine learning projects into experiments, which are groups of related runs. 

Each run captures the details of a single execution of the project, including parameters, metrics, and artifacts.

### Artifacts Store

The artifacts store is where all outputs of the experiments, such as models and figures, are stored. 

This ensures traceability and easy access to all related files.

### Metrics and Parameters

MLflow logs metrics and parameters for each run, allowing users to compare different runs and optimize their models.

### Dependencies and Environment

MLflow captures the computational environment, including dependencies and configurations, to ensure reproducibility of the experiments.

### UI Integration

The integrated UI allows users to visualize and compare runs, facilitating better decision-making and analysis.

### APIs

MLflow provides APIs for interacting programmatically with the tracking system, enabling seamless integration with other tools and workflows.

### tracking Server

MLflow Tracking Server can be configured with an artifacts HTTP proxy, passing artifact requests through the tracking server to store and retrieve artifacts without having to interact with underlying object store services. This is particularly useful for team development scenarios where you want to store artifacts and experiment metadata in a shared location with proper access control.

Here a scheme of MLFflow Tracking in Team development as we used it :

![MLFLOW Tracking Server Schema](images/tracking-setup-overview.png)


## MLflow Projects

### Project Definition

An MLflow Project is defined by a directory of files or a Git repository that contains the project code. This makes it easy to share and reproduce the project.

### Entry Points

Projects include entry points, which are commands that can be executed within the project, along with their parameters. This makes running experiments straightforward and standardized.

### Environment Specification

MLflow Projects specify execution environments, including Conda environments and Docker files. This ensures that the code runs in the correct environment, further promoting reproducibility.

### MLflow Models

### Standard Format

MLflow Models are packaged in a standard format that includes metadata, such as dependencies and inference schema. This standardization makes it easy to deploy models across different platforms.

### Flavors

MLflow Models support multiple formats, known as flavors, making them compatible with various downstream tools and environments. For example, a model can be saved in a format that is compatible with TensorFlow, PyTorch, or scikit-learn.

### MLflow Deployments

### Unified Interface

MLflow provides a unified interface for deploying models to various platforms, including SaaS and open-source solutions. This simplifies the deployment process and ensures consistency.

### Security

MLflow bolsters security through authenticated access to models, ensuring that only authorized users can deploy and manage models.

### APIs

The deployment APIs provide a common set of functions for deploying models to different environments, making the process seamless and efficient.


## Use Cases and Benefits

### Use cases

* **Monitoring Use Cases**
    * Web Servers: Monitor HTTP request rates, response times, and error rates to ensure the performance and reliability of web applications.

    * Databases: Track query performance, connection counts, and resource usage for databases like PostgreSQL, MySQL, and MongoDB.

    * Kubernetes Clusters: Observe pod health, resource utilization, and cluster events to maintain the health and efficiency of Kubernetes clusters.

For more use cases see [Overview](mlflow.md#__tabbed_1_2)     

### Benefits

* **Reliability**: Prometheus is designed for high availability and resilience, ensuring that monitoring and alerting are reliable.

* **Scalability**: Prometheus handles large volumes of metrics data and scales with the infrastructure, making it suitable for growing environments.

* **Ease of Integration**: Prometheus seamlessly integrates with a wide range of third-party tools and services, providing a flexible and powerful monitoring solution.