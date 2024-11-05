#!/bin/bash

# Nom ou partie du nom du conteneur (dans ton cas 'worker')
CONTAINER_NAME_KEYWORD="worker"

# Trouver le conteneur correspondant
CONTAINER_ID=$(docker ps --filter "name=$CONTAINER_NAME_KEYWORD" --format "{{.ID}}" | head -n 1)

# Vérifier si le conteneur est trouvé
if [ -z "$CONTAINER_ID" ]; then
    echo "Erreur : Aucun conteneur correspondant à '$CONTAINER_NAME_KEYWORD' trouvé."
    exit 1
fi

# Afficher un message d'information
echo "Conteneur trouvé : $CONTAINER_ID. Connexion au container..."

# Exécuter les commandes dans le conteneur trouvé
docker exec -it $CONTAINER_ID /bin/bash