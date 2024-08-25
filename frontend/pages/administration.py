import streamlit as st
import requests
from utils.api_client import API_URL
from utils.auth import is_authenticated, is_admin

def show():
    if not is_authenticated() or not is_admin():
        st.error("You must be logged in as an admin to view this page.")
        return

    st.title("User Administration")

    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch all users
    response = requests.get(f"{API_URL}/auth/users", headers=headers)
    if response.status_code != 200:
        st.error("Failed to retrieve users.")
        return

    users = response.json()

    # Display users in a table
    st.table(
        [
            {
                "Username": user["username"],
                "Email": user["email"],
                "Role": user["role"],
                "Actions": f"{user['username']}|{user['role']}"
            }
            for user in users
        ]
    )

    # User actions
    st.subheader("User Actions")
    selected_user = st.selectbox("Select a user", [user["username"] for user in users])
    action = st.radio("Choose an action", ["Change Role", "Delete User"])

    if action == "Change Role":
        new_role = st.selectbox("Select new role", ["user", "admin"])
        if st.button("Change Role"):
            response = requests.put(
                f"{API_URL}/auth/users/{selected_user}/role",
                json={"role": new_role},
                headers=headers
            )
            if response.status_code == 200:
                st.success(f"Role updated for {selected_user}")
                st.experimental_rerun()
            else:
                st.error("Failed to update role")

    elif action == "Delete User":
        if st.button("Delete User"):
            response = requests.delete(
                f"{API_URL}/auth/users/{selected_user}",
                headers=headers
            )
            if response.status_code == 200:
                st.success(f"User {selected_user} deleted successfully")
                st.experimental_rerun()
            else:
                st.error("Failed to delete user")