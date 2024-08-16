#!/bin/bash


# Get the operating system value
OS=$(hostnamectl | awk -F': ' '/Operating System/ {print $2}' | tr -d ' ')
# Check if the PostgreSQL Docker container is running
CONTAINER_ID=$(docker ps -aq --filter "name=postgres")

if [ -z "$CONTAINER_ID" ]; then
    echo "PostgreSQL Docker container is not running."
    exit 0
fi

# Stop and remove the PostgreSQL Docker container
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID

# Remove the PostgreSQL Docker image (optional)
# docker rmi postgres

echo "PostgreSQL has been uninstalled from the Docker container."