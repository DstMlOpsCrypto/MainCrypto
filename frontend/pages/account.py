import streamlit as st
import requests
from utils.api_client import API_URL
from utils.auth import logout, is_admin

def show():
    st.title("Account Settings")

    token = st.session_state.get("token")
    if not token:
        st.error("You must be logged in to view this page.")
        return

    # Récupérer les informations de l'utilisateur
    response = requests.get(f"{API_URL}/auth/users/me", headers={"Authorization": f"Bearer {token}"})
    if response.status_code != 200:
        st.error("Failed to retrieve user information.")
        return

    user_info = response.json()

    # Formulaire de mise à jour des informations
    st.subheader("Update Information")
    with st.form("update_form"):
        new_username = st.text_input("New Username", value=user_info['username'])
        new_email = st.text_input("New Email", value=user_info['email'])
        new_password = st.text_input("New Password", type="password")
        update_button = st.form_submit_button("Update")

    if update_button:
        update_data = {}
        if new_username != user_info['username']:
            update_data["username"] = new_username
        if new_email != user_info['email']:
            update_data["email"] = new_email
        if new_password:
            update_data["password"] = new_password

        if update_data:
            response = requests.put(
                f"{API_URL}/auth/users/me",
                json=update_data,
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                st.success("Information updated successfully!")
                st.experimental_rerun()
            else:
                st.error(f"Failed to update information: {response.text}")

    # Bouton de suppression du compte
    st.subheader("Delete Account")
    if st.button("Delete My Account"):
        if st.checkbox("I understand this action is irreversible"):
            response = requests.delete(
                f"{API_URL}/auth/users/{user_info['username']}",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code == 200:
                st.success("Account deleted successfully.")
                logout()
                st.experimental_rerun()
            else:
                st.error(f"Failed to delete account: {response.text}")
