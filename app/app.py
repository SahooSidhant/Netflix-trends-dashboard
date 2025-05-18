# app/app.py

import streamlit as st
from PIL import Image
import home
import eda_charts
import powerbi

# Streamlit page configuration
st.set_page_config(page_title="Netflix Trends App", layout="wide")

# Try loading Netflix logo
try:
    logo = Image.open("app/Netflix-Logo.png")
except FileNotFoundError:
    st.warning("Netflix logo not found. Please ensure 'Netflix-logo.png' is in the same folder as app.py.")
    logo = None

# Inject custom CSS for navbar styling
st.markdown("""
<style>
body {
    margin: 0;
    background-color: #141414;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.navbar {
    background-color: #e50914;
    padding: 10px 40px;
    display: flex;
    align-items: center;
    gap: 60px;
    border-radius: 0 0 12px 12px;
}
div[data-baseweb="radio"] > div {
    display: flex !important;
    gap: 25px !important;
}
div[data-baseweb="radio"] label {
    background-color: #e50914 !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 18px !important;
    padding: 12px 25px !important;
    border-radius: 6px !important;
    cursor: pointer !important;
    border: 2px solid transparent !important;
    transition: background-color 0.3s ease !important;
}
div[data-baseweb="radio"] label[data-selected="true"] {
    background-color: #8b050c !important;
    border-color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Navbar container
with st.container():
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    if logo:
        st.image(logo, width=110)
    page = st.radio(
        "", ["Home", "EDA Charts", "Power BI"],
        horizontal=True,
        key="page",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Route to selected page
if page == "Home":
    home.show()
elif page == "EDA Charts":
    eda_charts.show()
elif page == "Power BI":
    powerbi.show()
