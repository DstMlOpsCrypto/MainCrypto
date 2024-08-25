FROM postgres:latest


# TODO : create cron job to combine and upload data, then remove files

ARG POSTGRES_PORT

# Copy the SQL script into the Docker image
COPY .db/create_tables.sql /docker-entrypoint-initdb.d/

# Create folder 'historical_ohlcvt'
RUN mkdir -p /var/lib/postgresql/data/historical_ohlcvt

# Expose the PostgreSQL port
EXPOSE ${POSTGRES_USER}/tcp

