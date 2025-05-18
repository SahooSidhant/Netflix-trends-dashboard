import streamlit as st

def show():
    st.title("📊 Power BI Dashboard - Netflix Trends")

    st.markdown("This dashboard provides deep insights using Power BI visualization tools embedded below.")

    powerbi_embed_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZmY2ZhZjktYzg2Ny00MzY5LTljZmMtNDBhZDZlM2NlMmVlIiwidCI6ImUwMWI2ZDg3LTRhNGEtNGQ1YS1hMjc0LTVjMGIyMDI3MGVhZiJ9"

    st.markdown(
        f"""
        <iframe title="Power BI Dashboard" width="100%" height="800" 
        src="{powerbi_embed_url}" frameborder="0" allowFullScreen="true"></iframe>
        """,
        unsafe_allow_html=True,
    )
