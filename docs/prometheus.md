# Prometheus

## Introduction to Prometheus

### Overview

Prometheus is an open-source monitoring and alerting toolkit designed to be highly reliable and scalable. Originally developed at SoundCloud, Prometheus has become a leading tool for monitoring systems and applications.

Its ability to collect and store metrics as time series data, query it using PromQL, and alert on specified conditions has made it an indispensable tool in the industry.

In 2016, Prometheus joined the Cloud Native Computing Foundation (CNCF), further solidifying its place in the ecosystem of cloud-native tools.

=== "Creator"

    * **Name**: Created in 2012 by engineers at SoundCloud to address their monitoring needs
    * **Background**: Sebastián is a software developer from Colombia who currently resides in Berlin, Germany
    * **Contribution**: He is the creator of several popular open-source projects, including FastAPI, Typer, SQLModel, and Asyncer

=== "Use Cases"

    * **Infrastructure Monitoring**

        * Servers: Monitor CPU, memory, disk usage, and network traffic of physical and virtual servers.
        * Containers: Track resource usage and performance metrics of Docker containers and Kubernetes pods.
        * Databases: Monitor performance metrics of databases like PostgreSQL, MySQL, and MongoDB.
        * Network Devices: Collect metrics from switches, routers, and firewalls to monitor network performance.

    * **Application Performance Monitoring (APM)**

        * Web Applications: Measure response times, error rates, and request rates for web applications.
        * Microservices: Track metrics for individual microservices to monitor their performance and health.
        * APIs: Monitor API endpoints for latency, throughput, and error rates.

    * **DevOps and Continuous Integration/Continuous Deployment (CI/CD)**

        * Build Pipelines: Monitor the status and performance of CI/CD pipelines, including build times and failure rates.
        * Deployment Monitoring: Track the deployment status and measure the impact of new releases on application performance.

    * **Custom Business Metrics**

        * E-commerce: Monitor transaction rates, shopping cart abandonment, and user activity on e-commerce platforms.
        * Finance: Track trading volumes, transaction processing times, and system availability for financial services.
        * Healthcare: Monitor patient data processing, system uptime, and resource utilization in healthcare applications.

    * **Security Monitoring**

        * Intrusion Detection: Collect and analyze logs from intrusion detection systems (IDS) for security threats.
        * Access Logs: Monitor access logs to detect unauthorized access attempts and security breaches.
        * Compliance: Track compliance-related metrics to ensure adherence to security standards and regulations.

    * **Real-time Analytics**

        * User Behavior: Monitor real-time user activity and behavior on websites and applications.
        * Social Media: Track metrics from social media platforms to analyze engagement and reach.
        * IoT Devices: Collect and analyze data from Internet of Things (IoT) devices for real-time insights.

    * **Alerting and Incident Management**

        * Service Level Objectives (SLOs): Monitor SLOs and alert on breaches to maintain service reliability.
        * Incident Response: Trigger alerts for critical incidents and integrate with alerting systems like PagerDuty or Slack.
        * Automated Remediation: Use metrics to automate responses to incidents and reduce downtime.


## Main Characteristics of Prometheus

### Multi-Dimensional Data Model

Prometheus utilizes a multi-dimensional data model where time series data is identified by a combination of a metric name and key-value pairs. 

This approach allows for the collection and storage of high-dimensional data, making it easier to query and analyze performance metrics across various dimensions like instance, job, and region.

### PromQL 

PromQL (Prometheus Query Language) is a powerful and flexible query language designed specifically for Prometheus. It allows users to select and aggregate time series data using a rich set of operators and functions. 

PromQL leverages the multi-dimensional data model to enable complex queries that can slice and dice the data in numerous ways, providing deep insights into system performance and behavior.

### No Distributed Storage

Prometheus is designed to operate without distributed storage. Each Prometheus server node functions independently, storing its time series data locally. 

This approach simplifies the architecture and ensures that each node is autonomous, providing resilience and ease of management.

### Pull Model 

Prometheus employs a pull model for time series data collection. It scrapes metrics over HTTP from instrumented services at regular intervals. 

This pull-based approach allows Prometheus to control the data collection process, ensuring consistency and reliability in the metrics gathered.

### Push Gateway

The Push Gateway supports scenarios where the pull model is not feasible, such as short-lived jobs. It acts as an intermediary gateway, allowing clients to push metrics to it, which are then scraped by Prometheus. 

This ensures that even ephemeral tasks can be monitored effectively.

### Service Discovery

Service discovery in Prometheus automates the process of finding and scraping targets. It supports various service discovery mechanisms like Kubernetes, Consul, and static configuration. 

This flexibility ensures that Prometheus can dynamically adapt to changes in the infrastructure, such as scaling up or down.

### Graphing and Dashboarding 

Prometheus offers robust support for graphing and dashboarding, enabling users to visualize metrics in multiple ways. 

It integrates seamlessly with Grafana, a popular open-source dashboard tool, allowing for the creation of interactive and customizable dashboards that provide real-time insights into system performance.

## Prometheus Architecture

### Prometheus Server

The Prometheus server is the core component responsible for scraping and storing time series data. It retrieves metrics from configured targets, stores them in the local time series database (TSDB), and makes the data available for querying and analysis using PromQL.

### Time-Series Database (TSDB)

The TSDB in Prometheus is optimized for handling time series data. It stores all scraped samples locally, providing efficient data storage and retrieval. 

The TSDB ensures high performance and scalability, allowing Prometheus to handle large volumes of metrics data.

### Targets

Targets are the endpoints from which Prometheus scrapes metrics. 

These can be application servers, databases, or any other instrumented services that expose metrics in a format understood by Prometheus.

### Exporters

Exporters are special-purpose components that expose metrics for various services. Examples include HAProxy, StatsD, Graphite, and many others. 

Exporters convert metrics from these services into a format that Prometheus can scrape and store.

### Alertmanager

The Alertmanager handles alerts generated by Prometheus. It manages the routing and notification of alerts to various channels like email, Slack, PagerDuty, and more. 

Alertmanager also supports silencing, inhibition, and grouping of alerts to reduce noise and improve incident management

### Client Libraries

Client libraries are available for various programming languages (e.g., Go, Python, Java, Ruby) to instrument application code. 
These libraries facilitate the collection and exposure of custom application metrics that Prometheus can scrape.

### Push Gateway

The Push Gateway allows for pushing metrics from short-lived jobs. It serves as an intermediary that receives and temporarily stores metrics, which Prometheus then scrapes. 

This ensures that metrics from transient tasks are not lost.

### PromQL: 

PromQL is essential for querying and analyzing metrics in Prometheus. It allows users to perform complex queries, aggregations, and transformations on the collected time series data, providing valuable insights into system performance.

## Use Cases and Benefits

### Monitoring Use Cases

* **Web Servers**: Monitor HTTP request rates, response times, and error rates.
* **Databases**: Track query performance, connection counts, and resource usage.
* **Kubernetes Clusters**: Observe pod health, resource utilization, and cluster events.

For more use cases see [Overview](prometheus.md#__tabbed_1_2) 

### Benefits 

* **Reliability**: Prometheus is designed for high availability and resilience.
* **Scalability**: Handles large volumes of metrics data and scales with the infrastructure.
* **Ease of Integration**: Seamlessly integrates with a wide range of third-party tools and services.


