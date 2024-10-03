FROM postgres:13

# Copie du script d'initialisation
COPY ./mlflow/init-db.sh /docker-entrypoint-initdb.d/init-db.sh

# Rendre le script exécutable
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

# Expose le port PostgreSQL
EXPOSE 5432