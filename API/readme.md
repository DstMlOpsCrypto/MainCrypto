
1. Construire l'image Docker:
Dans votre terminal, à partir du répertoire API, exécutez la commande suivante:

```bash
docker build -t fastapi-app .
```

2. Exécuter le conteneur Docker:

Pour démarrer le conteneur avec votre application FastAPI:

```bash
docker run -d -p 3000:3000 fastapi-app
```

Cette commande va lancer le conteneur en arrière-plan et exposer votre application sur le port 3000 de votre machine hôte.

