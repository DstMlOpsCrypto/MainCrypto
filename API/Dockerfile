FROM python:3.8-alpine
# python:3.8-alpine is an image of a light version of python based on Alpine Linux
# Based on tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip
# Installing base packages
RUN apk add --no-cache --virtual .build-deps gcc libc-dev make libffi-dev postgresql-dev \
    && pip install --no-cache-dir uvicorn gunicorn fastapi python-jose[cryptography] passlib python-multipart pytest httpx email-validator slowapi psycopg2-binary \
    && apk del .build-deps gcc libc-dev make libffi-dev postgresql-dev

# Copy the start.sh script to the container
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

# Copy the gunicorn_conf.py script to the container
COPY ./gunicorn_conf.py /gunicorn_conf.py

# Copy the start-reload.sh script to the container
COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

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