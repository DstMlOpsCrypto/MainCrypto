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
echo "Conteneur trouvé : $CONTAINER_ID. Connexion et lancement de la prédiction..."

# Exécuter les commandes dans le conteneur trouvé
docker exec -i $CONTAINER_ID /bin/bash -c "
    cd /app/scripts && \
    echo 'Dossier de scripts atteint, lancement de la prédiction...' && \
    python3 predict.py --currency='BTC-EUR'
"

# Vérification du succès de la commande
if [ $? -eq 0 ]; then
    echo "Entrainement lancé avec succès."
else
    echo "Échec de l'exécution de la commande."
fi