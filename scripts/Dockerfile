# Utilisez l'image Python 3.12.4 basée sur Ubuntu 22.04
FROM python:3.12.4-slim-bullseye

# mISE À JOUR ET INSTALLATION pip
RUN apt-get update && pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install tensorflow && pip install mlflow && pip install yfinance && pip install --upgrade typing_extensions


# Create repos
RUN mkdir -p /src /scripts /tests /mlruns

# Copiez les dossiers dans l'image Docker depuis le répertoire parent
COPY ../src /src
COPY ../scripts /scripts
COPY ../tests /tests

# Set the working directory in the container
WORKDIR /scripts

VOLUME /scripts/mlruns

#RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Start mlflow tracking server, port 5000
CMD ["python3", "start_mlflow_server.py"]

#train model inside container
#CMD ["python3", "train.py", "--currency=BTC-EUR","--period=1d"]

#predict inside container
#CMD ["python3", "predict.py", "--currency=BTC-EUR","--period=1d"]

#construit avec : docker build -f scripts/Dockerfile -t model:latest . depuis le repo MainCrypto
# lancé avec docker container run -it -p 5000:5000 -v /scripts/mlruns:/scripts/mlruns model