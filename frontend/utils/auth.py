import streamlit as st
import requests
from .api_client import API_URL

def login(username: str, password: str) -> bool:
    try:
        response = requests.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            st.session_state["username"] = username
            st.session_state["role"] = data["role"]
            st.session_state["token"] = data["access_token"]
            return True
        return False
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def is_authenticated():
    token = st.session_state.get("token")
    if token:
        try:
            response = requests.post(
                f"{API_URL}/auth/validate",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("valid"):
                    return True
            # Si le token n'est pas valide, on déconnecte l'utilisateur
            logout()
        except requests.RequestException:
            pass
    return False

def logout():
    for key in ["username", "role", "token"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

def is_admin():
    return st.session_state.get('role') == 'admin' and is_authenticated()