

# Construction des images Dockerfile
## creation initiation bdd

## Worker
Créer une image nommée "worker" :
docker build -f scripts/Dockerfile -t worker:latest .

## Tests
Créer une image nommée "tests-scripts-ml" :
docker build -f scripts/Dockerfile.tests -t tests-scripts-ml:latest .

## Lancement des tests du scripts d'entrainement et de prédiction
docker compose --

## Lancement des tests du scripts d'entrainement et de prédiction
docker-compose up --no-deps tests-ml
### attention test-db exlcus des tests en attendant sa finalisation


