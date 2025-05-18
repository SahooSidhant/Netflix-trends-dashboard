# app/home.py

import streamlit as st
from PIL import Image

def show():
    # Page title
    st.markdown("<h1 style='color:#E50914;'>🎬 Netflix Trends Dashboard App</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:white;'>Unlocking Global Insights from Netflix Titles Over Time</h4>", unsafe_allow_html=True)
    st.markdown("---")

    # Netflix-style banner image
    st.image("banner1.png", use_container_width=True)

    # Project authors
    st.markdown("<h4 style='color:red;'>👥 Project Team</h4>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.image("4140052.png", width=60)
        st.markdown("<p style='color:white; font-size:18px;'><b>Sidhanta Sahoo</b></p>", unsafe_allow_html=True)

    with col2:
        st.image("6997674.png", width=60)
        st.markdown("<p style='color:white; font-size:18px;'><b>Somen Mandal</b></p>", unsafe_allow_html=True)

    st.markdown("---")

    # Welcome message
    st.markdown("""
    <div style='background-color:#1c1c1c; padding: 20px; border-radius: 10px;'>
        <p style='font-size: 18px; color:white;'>
            👋 Welcome to our interactive Netflix dashboard! <br><br>
            This app helps you explore how Netflix content trends have evolved over time across countries and formats. 
            Use the top navigation bar to view detailed EDA visualizations or explore our Power BI insights.
        </p>
    </div>
    """, unsafe_allow_html=True)
