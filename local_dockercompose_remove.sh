#!/bin/bash

# Function to check if Docker is installed
is_docker_installed() {
    if command -v docker >/dev/null 2>&1; then
        return 0  # Docker is installed
    else
        return 1  # Docker is not installed
    fi
}

# Function to check if Docker Compose is installed
is_docker_compose_installed() {
    if command -v docker-compose >/dev/null 2>&1; then
        # Stop all running containers:
        docker-compose down
        # Remove any stopped containers:
        docker-compose rm -f
        # Remove any unused Docker images:
        docker image prune
        # Remove any unused volumes:
        docker volume prune
        # Remove any unused networks:
        docker network prune
        return 0  # Docker Compose is installed
    else
        return 1  # Docker Compose is not installed
    fi
}

# Function to uninstall Docker
uninstall_docker() {
    echo "Uninstalling Docker..."
    OS=$(hostnamectl | awk -F': ' '/Operating System/ {print $2}' | tr -d ' ')
# ================

    case "$OS" in
        Ubuntu|Debian)
            sudo apt-get remove -y docker docker-engine docker.io containerd runc
            ;;
        CentOS|Fedora|"RedHatEnterprise")
            sudo yum remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
            ;;
        openSUSE)
            sudo zypper remove -y docker docker-compose
            ;;
        ArchLinux|Manjaro)
            sudo pacman -Rns --noconfirm docker docker-compose
            ;;
        Alpine)
            sudo apk del docker docker-compose
            ;;
        *)
            echo "Unsupported distribution: $OS"
            exit 1
            ;;
    esac
    echo "...done"
}

# Function to uninstall Docker Compose
uninstall_docker_compose() {
    echo "Uninstalling Docker Compose..."
    sudo rm -rf /usr/local/bin/docker-compose
    echo "...done"

}

# Check if Docker is installed
if is_docker_installed; then
    uninstall_docker
else
    echo "Docker is not installed."
fi

# Check if Docker Compose is installed
if is_docker_compose_installed; then
    uninstall_docker_compose
else
    echo "Docker Compose is not installed."
fi
