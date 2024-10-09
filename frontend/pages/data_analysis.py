import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.api_client import API_URL
from utils.auth import is_authenticated

def show():
    st.title("Data Analysis")

    if not is_authenticated():
        st.warning("Please log in to view the data analysis.")
        return

    token = st.session_state.get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch available assets
    try:
        response = requests.get(f"{API_URL}/crypto/assets", headers=headers)
        if response.status_code == 200:
            assets = response.json()
            asset_options = [f"{asset['symbol']} ({asset['asset']})" for asset in assets]
            asset_map = {f"{asset['symbol']} ({asset['asset']})": asset['asset'] for asset in assets}
        else:
            st.error("Failed to fetch assets.")
            return
    except requests.RequestException as e:
        st.error(f"An error occurred while fetching assets: {str(e)}")
        return

    # Let user select an asset
    selected_asset_option = st.selectbox("Select an asset", asset_options)
    selected_asset = asset_map[selected_asset_option]

    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End date", datetime.now())

        if st.button("Load Data"):
            # Fetch asset history
            try:
                response = requests.get(
                    f"{API_URL}/crypto/asset_history/{selected_asset}",
                    params={
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "limit": 1000
                    },
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    #st.write("API Response:", data[:5])  # Display first 5 items for debugging
                    
                    if not data:
                        st.warning("No data returned from the API.")
                        return
                    
                    df = pd.DataFrame(data)
                    #st.write("DataFrame columns:", df.columns)  # Display column names
                    
                    if 'dtutc' not in df.columns:
                        st.error("'dtutc' column not found in the data.")
                        return
                    
                    df['dtutc'] = pd.to_datetime(df['dtutc'])
                    df = df.sort_values('dtutc')

                    # Create candlestick chart
                    fig = go.Figure(data=[go.Candlestick(
                        x=df['dtutc'],
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close']
                    )])

                    fig.update_layout(
                        title=f"{selected_asset} Price Chart",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        xaxis_rangeslider_visible=False
                    )

                    st.plotly_chart(fig)

                    # Display summary statistics
                    st.subheader("Summary Statistics")
                    st.write(df[['open', 'high', 'low', 'close']].describe())

                else:
                    st.error(f"Failed to fetch asset history. Status code: {response.status_code}")
                    st.write("Response content:", response.text)
            except requests.RequestException as e:
                st.error(f"An error occurred while fetching asset history: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")