import streamlit as st

st.set_page_config(page_title="AI Trading Bot", layout="wide")

st.title("🚀 AI Trading Bot Dashboard")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Balance", "Trading", "Settings", "Logs"])

# Placeholder for different sections
if page == "Home":
    st.header("📊 Overview")
    st.write("Welcome to your AI Trading Bot dashboard. Monitor performance and control trades.")

    # Placeholder Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Balance", "Loading...", "0%")
    col2.metric("Open Trades", "Loading...", "0")
    col3.metric("Profit/Loss", "Loading...", "0%")

    # Quick Actions
    st.subheader("⚡ Quick Actions")
    colA, colB = st.columns(2)
    colA.button("🔄 Refresh Data", key="refresh")
    colB.button("🛑 Stop Bot", key="stop_bot")

elif page == "Balance":
    st.header("💰 Account Balance")
    st.write("Check your account balances from LUNO.")
    # Add button to navigate to the Balance page
    if st.button("🔍 View Balances"):
        st.session_state["page"] = "Balance"  # Set session state to navigate

    # Auto-refresh workaround (Temporary)
    if "page" in st.session_state and st.session_state["page"] == "Balance":
        st.switch_page("pages/balance.py")  # Navigate to balance page

elif page == "Trading":
    st.header("📈 Trading Panel")
    st.write("Place and manage trades.")

    # Placeholder for trading actions
    col1, col2 = st.columns(2)
    col1.button("📊 Place Market Order", key="market_order")
    col2.button("📉 Cancel Open Order", key="cancel_order")

elif page == "Settings":
    st.header("⚙️ Settings")
    st.write("Configure API keys, AI models, and bot preferences.")

    # AI Model Selection Placeholder
    model = st.radio("Select AI Model", ["OpenAI", "Grok", "Local LLM"])
    st.button("💾 Save Settings", key="save_settings")

elif page == "Logs":
    st.header("📜 Trade Logs")
    st.write("View past trades and bot actions.")
    st.button("🔄 Refresh Logs", key="refresh_logs")
