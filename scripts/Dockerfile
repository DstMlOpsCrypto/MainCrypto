# Utilisez l'image Python 3.12.4 basée sur Ubuntu 22.04
FROM python:3.12.4-slim-bullseye

#pip
RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copiez le script Python dans l'image Docker
COPY start_mlflow_server.py start_mlflow_server.py 
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Démarrez le serveur en exécutant le script Python
CMD ["python3", "start_mlflow_server.py"]


# Run the MLflow tracking server when the container launches
# CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]