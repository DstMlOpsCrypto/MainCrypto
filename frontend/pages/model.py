# model.py

import streamlit as st
import requests
from utils.api_client import API_URL
from utils.auth import is_authenticated

def show():
    st.title("Gestion des Modèles")

    if not is_authenticated():
        st.warning("Veuillez vous connecter pour gérer les modèles.")
        return

    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Afficher les modèles disponibles
    st.subheader("Modèles Disponibles")
    if st.button("Actualiser la liste des modèles"):
        try:
            response = requests.get(f"{API_URL}/prediction/models", headers=headers)
            if response.status_code == 200:
                models = response.json().get("models", [])
                if models:
                    for model in models:
                        st.write(f"**Nom du Modèle** : {model['name']}")
                        for version in model['latest_versions']:
                            st.write(f"- **Version** : {version['version']}, **Stage** : {version['stage']}, **Run ID** : {version['run_id']}")
                else:
                    st.info("Aucun modèle trouvé.")
            else:
                st.error(f"Échec de la récupération des modèles. Code de statut : {response.status_code}")
        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")

    # Déclencher l'entraînement d'un nouveau modèle
    st.subheader("Entraîner un Nouveau Modèle")
    if st.button("Lancer l'entraînement"):
        try:
            response = requests.post(f"{API_URL}/prediction/train", headers=headers)
            if response.status_code == 202:
                st.success("Le DAG d'entraînement a été déclenché avec succès.")
            else:
                st.error(f"Échec du déclenchement de l'entraînement. Code de statut : {response.status_code}")
        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")

    # Afficher les métriques d'évaluation du modèle
    st.subheader("Métriques d'Évaluation du Modèle")
    if st.button("Obtenir les dernières métriques d'évaluation"):
        try:
            response = requests.get(f"{API_URL}/prediction/model-evaluation", headers=headers)
            if response.status_code == 200:
                metrics = response.json()
                st.write(metrics)
            else:
                st.error(f"Échec de la récupération des métriques. Code de statut : {response.status_code}")
        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")

    # Afficher le meilleur modèle
    st.subheader("Meilleur Modèle")
    if st.button("Obtenir le meilleur modèle"):
        try:
            response = requests.get(f"{API_URL}/prediction/best-model", headers=headers)
            if response.status_code == 200:
                best_model = response.json()
                st.write(best_model)
            else:
                st.error(f"Échec de la récupération du meilleur modèle. Code de statut : {response.status_code}")
        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")
