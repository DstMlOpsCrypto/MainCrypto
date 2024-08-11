#!/bin/bash


# Get the operating system value
OS=$(hostnamectl | awk -F': ' '/Operating System/ {print $2}' | tr -d ' ')

# Uninstall Docker based on the distribution
case "$OS" in
    Ubuntu|Debian)
        # Stop Docker service
        sudo systemctl stop docker
        # Remove Docker packages
        sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        # Remove Docker images, containers, volumes, and networks
        sudo rm -rf /var/lib/docker
        sudo rm -rf /etc/docker
        # Remove Docker repository
        sudo rm /etc/apt/sources.list.d/docker.list
        # Update package index
        sudo apt-get update
        # Remove any remaining dependencies
        sudo apt-get autoremove -y --purge docker-ce
        # Remove Docker GPG key
        sudo rm -rf /etc/apt/keyrings/docker.gpg        
        ;;
    CentOS|Fedora|"RedHatEnterprise")
        # Stop Docker service
        sudo systemctl stop docker
        # Remove Docker packages
        sudo yum remove -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        # Remove Docker images, containers, volumes, and networks
        sudo rm -rf /var/lib/docker
        sudo rm -rf /etc/docker
        # Remove Docker repository
        sudo rm /etc/yum.repos.d/docker-ce.repo
        # Remove any remaining dependencies
        sudo yum autoremove -y
        ;;
    openSUSE)
        # Stop Docker service
        sudo systemctl stop docker

        # Remove Docker packages
        sudo zypper remove -y docker docker-compose

        # Remove Docker images, containers, volumes, and networks
        sudo rm -rf /var/lib/docker
        sudo rm -rf /etc/docker
        ;;
    ArchLinux|Manjaro)
        # Stop Docker service
        sudo systemctl stop docker
        # Remove Docker packages
        sudo pacman -Rs -n --noconfirm docker docker-compose
        # Remove Docker images, containers, volumes, and networks
        sudo rm -rf /var/lib/docker
        sudo rm -rf /etc/docker
        ;;
    Alpine)
        # Stop Docker service
        sudo rc-service docker stop
        # Remove Docker packages
        sudo apk del docker docker-compose
        # Remove Docker images, containers, volumes, and networks
        sudo rm -rf /var/lib/docker
        sudo rm -rf /etc/docker
        ;;
esac

echo "Docker installation completed successfully!"

