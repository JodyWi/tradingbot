import streamlit as st

st.set_page_config(page_title="💰 Account Balance", layout="wide")

# 🔥 Hide sidebar navigation on Balance page
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💰 Account Balance")

# Back to Dashboard Button
if st.button("⬅️ Back to Dashboard"):
    st.switch_page("main.py")  # Navigate back
