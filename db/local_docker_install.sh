#!/bin/bash

# Get the operating system value
OS=$(hostnamectl | awk -F': ' '/Operating System/ {print $2}' | tr -d ' ')

# Update the system based on the distribution
case "$OS" in
    Ubuntu|Debian)
        sudo apt-get update
        sudo apt-get upgrade -y
        ;;
    CentOS|Fedora|"RedHatEnterprise")
        sudo yum update -y
        ;;
    openSUSE)
        sudo zypper update -y
        ;;
    ArchLinux|Manjaro)
        sudo pacman -Syu --noconfirm
        ;;
    Alpine)
        sudo apk update
        sudo apk upgrade
        ;;
    *)
        echo "Unsupported distribution: $OS"
        exit 1
        ;;
esac

# Install Docker based on the distribution
case "$OS" in
    Ubuntu|Debian)
        sudo apt-get install -y ca-certificates curl gnupg lsb-release
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$OS $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        ;;
    CentOS|Fedora|"RedHatEnterprise")
        sudo yum install -y yum-utils
        sudo yum-config-manager --add-repo https://download.docker.com/linux/$OS/docker-ce.repo
        sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
        ;;
    openSUSE)
        sudo zypper install -y docker docker-compose
        ;;
    ArchLinux|Manjaro)
        sudo pacman -S --noconfirm docker docker-compose
        ;;
    Alpine)
        sudo apk add docker docker-compose
        ;;
    *)
        echo "Unsupported distribution: $OS"
        exit 1
        ;;
esac

echo "Docker installation completed successfully!"
