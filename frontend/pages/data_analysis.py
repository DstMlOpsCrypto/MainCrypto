import streamlit as st
import pandas as pd

def show():
    st.title("Data Analysis")
    st.write("Here you can analyze crypto data.")
    
    # Placeholder for data loading and visualization
    data = pd.DataFrame({'Crypto': ['Bitcoin', 'Ethereum', 'Dogecoin'],
                         'Price': [50000, 3000, 0.5]})
    st.dataframe(data)