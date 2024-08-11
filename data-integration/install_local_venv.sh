#!/bin/bash

# Remove existing virtual environment
if [ -d "$(pwd)/.venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$(pwd)/.venv"
    echo "Virtual environment removed."
fi

# Create new virtual environment
echo "Creating new virtual environment..."
python -m venv "$(pwd)/.venv"
echo "Virtual environment created."

# Activate the virtual environment
echo "Activating virtual environment..."
source ".venv/bin/activate"
echo "Virtual environment activated."

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r $(pwd)/requirements.txt
echo "Dependencies installed."

# activate python venv
source "$(pwd)/.venv/bin/activate"