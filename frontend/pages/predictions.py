# prediction.py

import streamlit as st
import pandas as pd
import requests
from utils.api_client import API_URL
from utils.auth import is_authenticated
import plotly.graph_objects as go
from datetime import timedelta

def show():
    st.title("Prédictions Crypto")

    if not is_authenticated():
        st.warning("Veuillez vous connecter pour voir les prédictions.")
        return

    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Sélection de l'actif
    asset = "XXBTZUSD"  # Actif pour le Bitcoin
    st.subheader(f"Données pour l'actif : {asset}")

    # Récupérer les 14 dernières valeurs
    try:
        response = requests.get(
            f"{API_URL}/crypto/asset_latest/{asset}",
            headers=headers,
            params={"limit": 14}
        )
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df['dtutc'] = pd.to_datetime(df['dtutc'], utc=True) 
            df = df.sort_values('dtutc')
        else:
            st.error(f"Échec de la récupération des données historiques. Code de statut : {response.status_code}")
            return
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la récupération des données historiques : {str(e)}")
        return

    # Récupérer la dernière prédiction
    try:
        response = requests.get(f"{API_URL}/prediction/latest-prediction", headers=headers)
        if response.status_code == 200:
            prediction_data = response.json()
            prediction_value = prediction_data['prediction_value']
            prediction_date = pd.to_datetime(prediction_data['prediction_date'], utc=True)
            prediction_date += timedelta(days=1)
            st.write(f"**Date de Prédiction** : {prediction_date}")
            st.write(f"**Valeur Prédite** : {prediction_value}")
        else:
            st.error(f"Échec de la récupération de la dernière prédiction. Code de statut : {response.status_code}")
            return
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la récupération de la prédiction : {str(e)}")
        return

    # Ajouter la prédiction aux données
    prediction_df = pd.DataFrame([{
        'dtutc': prediction_date,
        'close': prediction_value
    }])
    df = pd.concat([df, prediction_df], ignore_index=True)
    df = df.sort_values('dtutc')

    # Créer le graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['dtutc'], y=df['close'], mode='lines+markers', name='Prix de Clôture'))

    fig.update_layout(
        title=f"Prix de Clôture et Prédiction pour {asset}",
        xaxis_title="Date",
        yaxis_title="Prix",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig)
