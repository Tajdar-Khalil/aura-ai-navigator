import streamlit as st
import streamlit.components.v1 as components

# Configure full-screen layout
st.set_page_config(
    page_title="AuraAI | AI Career & Skills Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Strip default Streamlit margins and bars
st.markdown("""
<style>
    #MainMenu, header, footer { visibility: hidden; }
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Read and render the responsive unified canvas
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=950, scrolling=True)
