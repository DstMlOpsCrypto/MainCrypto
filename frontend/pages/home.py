import streamlit as st
import requests
import pandas as pd
from utils.api_client import API_URL
from utils.auth import is_authenticated

def show():
    st.title("Welcome to DstMlOpsCrypto")
    st.write("This is the home page of our crypto analysis application.")

    if not is_authenticated():
        st.warning("Please log in to view and manage crypto pairs.")
        return

    token = st.session_state.get("token")
    if not token:
        st.error("Authentication token not found. Please log in again.")
        return

    st.subheader("Available Crypto Pairs")

    # Fetch and display existing assets
    existing_assets = fetch_existing_assets(token)
    if existing_assets is not None:
        st.dataframe(existing_assets)

        # Add delete functionality
        if not existing_assets.empty:
            # Create a mapping from asset names to IDs
            asset_names = existing_assets['asset'].tolist()
            asset_id_mapping = dict(zip(existing_assets['asset'], existing_assets['id']))

            # Let the user select an asset by name
            asset_to_delete = st.selectbox("Select an asset to delete", asset_names)
            if st.button("Delete Selected Asset"):
                # Get the corresponding asset ID
                asset_id = asset_id_mapping[asset_to_delete]
                delete_asset(token, asset_id)
                st.experimental_rerun()

    # Add new asset functionality
    st.subheader("Add New Crypto Pair")
    kraken_assets = fetch_kraken_assets(token)
    if kraken_assets is not None:
        new_asset = st.selectbox("Select a new asset to add", kraken_assets['asset'])
        if st.button("Add Selected Asset"):
            add_new_asset(token, kraken_assets[kraken_assets['asset'] == new_asset].iloc[0])
            st.experimental_rerun()

def fetch_existing_assets(token):
    try:
        response = requests.get(
            f"{API_URL}/crypto/assets",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            assets = response.json()
            if assets:
                return pd.DataFrame(assets)
            else:
                st.info("No crypto pairs available at the moment.")
        else:
            st.error(f"Failed to fetch crypto pairs. Status code: {response.status_code}")
            st.error(f"Error message: {response.text}")
    except requests.RequestException as e:
        st.error(f"An error occurred while fetching crypto pairs: {str(e)}")
    return None

def fetch_kraken_assets(token):
    try:
        response = requests.get(
            f"{API_URL}/crypto/kraken_assets",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            assets = response.json()
            if assets:
                return pd.DataFrame(assets)
            else:
                st.info("No Kraken assets available at the moment.")
        else:
            st.error(f"Failed to fetch Kraken assets. Status code: {response.status_code}")
            st.error(f"Error message: {response.text}")
    except requests.RequestException as e:
        st.error(f"An error occurred while fetching Kraken assets: {str(e)}")
    return None

def add_new_asset(token, asset_data):
    try:
        response = requests.post(
            f"{API_URL}/crypto/assets",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "asset": asset_data['asset'],
                "symbol": asset_data['symbol'],
                "exchange": asset_data['exchange']
            }
        )
        if response.status_code == 201:
            st.success(f"Successfully added new asset: {asset_data['asset']}")
        else:
            st.error(f"Failed to add new asset. Status code: {response.status_code}")
            st.error(f"Error message: {response.text}")
    except requests.RequestException as e:
        st.error(f"An error occurred while adding new asset: {str(e)}")

def delete_asset(token, asset_id):
    try:
        response = requests.delete(
            f"{API_URL}/crypto/assets/{asset_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 204:
            st.success(f"Successfully deleted asset: {asset_id}")
        else:
            st.error(f"Failed to delete asset. Status code: {response.status_code}")
            st.error(f"Error message: {response.text}")
    except requests.RequestException as e:
        st.error(f"An error occurred while deleting asset: {str(e)}")