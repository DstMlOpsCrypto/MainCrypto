import streamlit as st

def show():
    st.title("Crypto Predictions")
    st.write("Here you can see predictions for various cryptocurrencies.")
    
    # Placeholder for prediction functionality
    crypto = st.selectbox("Select a cryptocurrency", ["Bitcoin", "Ethereum", "Dogecoin"])
    if st.button("Predict"):
        st.write(f"Prediction for {crypto}: $XX,XXX")