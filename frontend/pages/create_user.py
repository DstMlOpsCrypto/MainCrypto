import streamlit as st
import requests
from utils.api_client import API_URL
from utils.auth import is_authenticated, is_admin

def show():
    st.title("Create New User")
    
    with st.form("create_user_form"):
        username = st.text_input("New Username")
        email = st.text_input("Email")
        password = st.text_input("New Password", type="password")
        role = st.selectbox("Role", ["admin", "user"])
        submit_button = st.form_submit_button("Create User")

    if submit_button:
        token = st.session_state.get("token")
        if not is_authenticated() or not is_admin():
            st.error("You must be logged in as an admin to create a new user.")
            return

        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }

        try:
            response = requests.post(
                f"{API_URL}/auth/signup",
                json=user_data,
                headers={"Authorization": f"Bearer {token}"}
            )

            if response.status_code == 200 or response.status_code == 201:
                response_data = response.json()
                st.success(response_data["message"])
                st.json(response_data["user"])
            elif response.status_code == 403:
                st.error("Only admins can create new accounts.")
            elif response.status_code == 400:
                st.error("Username already registered.")
            else:
                st.error(f"An error occurred: {response.text}")
        except requests.RequestException as e:
            st.error(f"An error occurred: {str(e)}")