# #!/bin/bash
# set -e

# # Only create the user, the database is already created by the environment variable
# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
#     CREATE USER mlflow WITH PASSWORD 'mlflow';
# EOSQL


#!/bin/bash

set -e

# Vérifier si le rôle existe déjà
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    DO
    \$\$
    BEGIN
        IF NOT EXISTS (
            SELECT 1
            FROM pg_roles
            WHERE rolname = 'mlflow') THEN
            CREATE ROLE mlflow WITH LOGIN PASSWORD 'mlflow';
        END IF;
    END
    \$\$;
EOSQL
