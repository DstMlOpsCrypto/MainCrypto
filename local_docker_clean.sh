#!/bin/bash      

is_docker_installed() {
    if command -v docker >/dev/null 2>&1; then
        return 0  # Docker is installed
    else
        return 1  # Docker is not installed
    fi
}

if is_docker_installed; then
    echo "Docker is installed. Let's wipe out all stuff ! "

    echo "\n #Stop all running containers..."
    docker stop $(docker ps -a -q)

    echo "\n #Remove all stopped containers..."
    docker rm $(docker ps -a -q)

    echo "\n #Remove all images..."
    docker rmi $(docker images -q)   

    echo "\n #Remove any  volumes..."
    docker volume rm $(docker volume ls -q)

    echo "\n #Remove any  networks..."
    docker network prune -f
    docker network rm $(docker network ls -q)

    echo "\n #Prune the system (this will remove all unused data..."
    docker system prune -f -a --volumes

    echo "\n Docker is cleaned."
else
    echo "Docker is not installed. What are you waiting to use docker ;-)"
fi