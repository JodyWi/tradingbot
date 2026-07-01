import streamlit as st

st.set_page_config(page_title="Trading Bot", layout="wide")

# 🔥 Remove "Main" from Streamlit's sidebar if it still exists
hide_menu_style = """
    <style>
        [data-testid="stSidebarNav"] ul li:first-child {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("🚀 AI Trading Bot")
st.sidebar.success("Select a page from the sidebar.")
