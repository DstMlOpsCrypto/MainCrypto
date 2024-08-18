import requests
import streamlit as st
import socket
import os

def get_host_ip():
    try:
        # Créer une connexion socket vers un serveur externe (Google DNS dans cet exemple)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"  # Fallback to localhost if unable to get IP

#API_URL = f"http://{get_host_ip()}:3000"
API_URL = os.getenv('API_URL', 'http://localhost:3000')

def get_prediction(crypto):
    headers = {"Authorization": f"Bearer {st.session_state.get('token', '')}"}
    response = requests.get(f"{API_URL}/predict/{crypto}", headers=headers)
    return response.json()