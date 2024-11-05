# Proposition de projet : prévision des prix des crypto-monnaies à l'aide de MLOps

## Introduction

 Les crypto-monnaies sont devenues une part importante du marché financier mondial.  Prédire leurs prix peut fournir des informations précieuses aux investisseurs et aux traders.  Ce projet vise à développer un pipeline MLOps robuste pour prévoir les prix des cryptomonnaies à l'aide de modèles d'apprentissage automatique.

## Objectifs

 Développez un pipeline MLOps de bout en bout pour la prévision des prix des cryptomonnaies.

 Implémentez et comparez différents modèles d'apprentissage automatique pour la prévision des prix.( a voir tout de même la faisabilité sur le temps imparti !!)

 Automatisez le déploiement, la surveillance et le recyclage des modèles.
 
 ## Portée du projet

 - Collecte de données : rassembler des données historiques sur les prix de diverses crypto-monnaies à partir de sources fiables.

 - Prétraitement des données : nettoyer et prétraiter les données pour les rendre adaptées à la formation du modèle.

 - Développement de modèles : mettre en œuvre plusieurs modèles d'apprentissage automatique (a completer) pour prévoir les prix.

 - Configuration du pipeline : configurer un pipeline MLOps à l'aide d'outils tels que les plates-formes Docker, Kubernetes et CI/CD, et le frameworks ML Flow.

 - Déploiement de modèles : déployer les modèles sur la VM mise a disposition de DataSciencTest.

 - Surveillance et recyclage : mettre en œuvre une surveillance pour suivre les performances du modèle et automatiser le re entraînement si nécessaire.

## Méthodologie

 #### Collecte de données:

 - Utilisation des API des échanges de crypto-monnaie (par exemple, Binance, Coinbase) pour collecter des données historiques sur les prix.

 - Stockez les données dans une base de données OpenSource.

 ### Prétraitement des données :

 - Géstion des valeurs manquantes et des valeurs aberrantes.

 - Normaliser les données pour de meilleures performances du modèle

 ### Développement d'un modèle:

 - Implémenter et former différents modèles ( exemple) :

      - LSTM (Long Short-Term Memory) : pour capturer les dépendances temporelles.

      - ARIMA (AutoRegressive Integrated Moving Average) : pour la prévision de séries chronologiques.

      - Prophet : Pour gérer les composants de saisonnalité et de tendance.

 - Évaluez les modèles à l'aide de métriques telles que RMSE (Root Mean Squared Error) et MAE (Mean Absolute Error).

 ### Configuration du pipeline :

 - Conteneurisez les modèles à l'aide de Docker.

 - Utilisez Kubernetes pour l'orchestration et la mise à l'échelle.( a voir) 

 - Implémentez des pipelines CI/CD à l'aide d'outils tels que Jenkins ou GitHub Actions.( voir si ML Flow peut nous aider dessus)

 ### Déploiement du modèle :

 - Déployer les modèles ( VM DataScienceTest ?)

 - Configurer les API REST pour l'inférence de modèle.

 ### Suivi et re entraînement :

- Utilisation des outils de surveillance (par exemple, Prometheus, Grafana) pour suivre les performances du modèle.

 - Automatiser les pipelines de re entrainement pour mettre à jour les modèles avec de nouvelles données.

## Outils et technologies

 - Langages de programmation : Python, SQL

 - Bibliothèques : TensorFlow, Keras, Scikit-learn, Statsmodels, Prophet

 - Stockage des données : PostgreSQL, MongoDB ( autre )

 - Conteneurisation : Docker

 - Orchestration : Kubernetes ( a voir )

 - CI/CD : GitHub actions

 - Plateformes cloud : a voir

 - Suivi : Prometheus, Grafana

## Chronologie

 - Semaine 1-2 : Collecte et prétraitement des données.

 - Semaine 3-4 : Développement et évaluation du modèle.

 - Semaine 5-6 : Configuration du pipeline et conteneurisation.

 - Semaine 7-8 : Déploiement du modèle et configuration de l'API.

 - Semaine 9-10 : Automatisation du suivi et du recyclage.

 - Semaine 11-12 : Tests, documentation et présentation finale.

## Résultats attendus

 - Un pipeline MLOps entièrement fonctionnel pour la prévision des prix des cryptomonnaies.

 - Analyse comparative de différents modèles d'apprentissage automatique.

 - Processus automatisés de déploiement, de surveillance et de recyclage.

## Conclusion

 Ce projet fournira une expérience pratique dans la mise en place d'un pipeline MLOps et l'application de modèles d'apprentissage automatique à un problème du monde réel.  
