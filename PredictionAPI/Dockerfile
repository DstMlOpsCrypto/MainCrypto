#FROM python:3.8-slim
FROM python:3.12.4-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libpq-dev \
        gcc \
        g++ \
        python3 \
        python3-pip \
        python3-venv \
        git
    
 RUN pip3 install --upgrade pip

 RUN pip install --no-cache-dir \
 tensorflow \
 mlflow \
 yfinance \
 uvicorn \
 gunicorn \
 fastapi \
 python-jose[cryptography] \
 passlib[argon2] \
 python-multipart \
 pytest \
 httpx \
 email-validator \
 slowapi \
 psycopg2-binary \
 apache-airflow \
 requests

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*


# Copy the start.sh script to the container
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Copy the gunicorn_conf.py script to the container
COPY ./gunicorn_conf.py /gunicorn_conf.py

# Copy the start-reload.sh script to the container
COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

# # Copy the predict.py script to the container, # not sure necessary here because of docker compose
# COPY ../scripts app/scripts
# COPY ./src app/src

# Copy the app directory to the container
COPY ./app /app
WORKDIR /app/

# Set the PYTHONPATH environment variable to the root directory and app directory
ENV PYTHONPATH=/app

# Expose the port 3000
EXPOSE 3000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start-reload.sh"] 
# we can use it with start.sh or with start-reload.sh for hot reloading