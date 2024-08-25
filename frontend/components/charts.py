import streamlit as st
import pandas as pd
import plotly.express as px

def line_chart(data, x, y, title):
    fig = px.line(data, x=x, y=y, title=title)
    st.plotly_chart(fig)