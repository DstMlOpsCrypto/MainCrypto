#!/bin/bash

# Nom ou partie du nom du conteneur PostgreSQL
CONTAINER_NAME_KEYWORD="mlflow_db"

# Identifiants PostgreSQL
DB_USER="mlflow"
DB_NAME="mlflow"

# Commande SQL à exécuter
SQL_COMMAND="ALTER TABLE runs ALTER COLUMN experiment_id TYPE BIGINT USING experiment_id::BIGINT;"

# Trouver le conteneur PostgreSQL en fonction du nom ou d'un mot-clé
CONTAINER_ID=$(docker ps --filter "name=$CONTAINER_NAME_KEYWORD" --format "{{.ID}}" | head -n 1)

# Vérifier si le conteneur est trouvé
if [ -z "$CONTAINER_ID" ]; then
    echo "Erreur : Aucun conteneur correspondant à '$CONTAINER_NAME_KEYWORD' trouvé."
    exit 1
fi

# Afficher un message d'information
echo "Conteneur trouvé : $CONTAINER_ID. Connexion et exécution de la commande SQL..."

# Exécuter la commande SQL à l'intérieur du conteneur trouvé
docker exec -i $CONTAINER_ID psql -U $DB_USER -d $DB_NAME -c "$SQL_COMMAND"

# Vérification du succès de la commande
if [ $? -eq 0 ]; then
    echo "Commande SQL exécutée avec succès."
else
    echo "Échec de l'exécution de la commande SQL."
fi
