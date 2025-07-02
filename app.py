# app.py
import streamlit as st
from api import fetch_spending_data
from graph import render_sankey

st.set_page_config(layout="wide")
st.title("Federal Spending Visualization (FY2025 Q2)")

with st.spinner("Fetching and processing data..."):
    results = fetch_spending_data()

if results:
    fig = render_sankey(results)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("No data available.")
