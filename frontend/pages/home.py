import streamlit as st
import requests
import pandas as pd
from utils.api_client import API_URL
from utils.auth import is_authenticated

def show():
    st.title("Welcome to DstMlOpsCrypto")
    st.write("This is the home page of our crypto analysis application.")

    if not is_authenticated():
        st.warning("Please log in to view available crypto pairs.")
        return

    token = st.session_state.get("token")
    if not token:
        st.error("Authentication token not found. Please log in again.")
        return

    st.subheader("Available Crypto Pairs")

    try:
        response = requests.get(
            f"{API_URL}/crypto/assets",
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 200:
            assets = response.json()
            if assets:
                df = pd.DataFrame(assets)
                st.dataframe(df)
            else:
                st.info("No crypto pairs available at the moment.")
        else:
            st.error(f"Failed to fetch crypto pairs. Status code: {response.status_code}")
            st.error(f"Error message: {response.text}")

    except requests.RequestException as e:
        st.error(f"An error occurred while fetching crypto pairs: {str(e)}")