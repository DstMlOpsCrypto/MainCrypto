#!/bin/bash


# Get the operating system value
OS=$(hostnamectl | awk -F': ' '/Operating System/ {print $2}' | tr -d ' ')

# install Docker based on the distribution
case "$OS" in
    Ubuntu|Debian)
        docker run -d --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres
        ;;
    CentOS|Fedora|"RedHatEnterprise")
        docker run -d --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres
        ;;
    openSUSE)
        docker run -d --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres
        ;;
    ArchLinux|Manjaro)
        docker run -d --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres
        ;;
    Alpine)
        docker run -d --name postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres
        ;;
    *)
        echo "Unsupported distribution: $OS"
        exit 1
        ;;
esac

echo "posgreSQL installation completed successfully!"