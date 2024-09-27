import os
import logging
import pandas as pd
import streamlit as st
from openai import OpenAI
import pyttsx3
import threading
# import functions.luno_api_functions.luno_get_balance as luno_get_balance
# import functions.luno_api_functions.luno_get_fee_info as luno_get_fee_info
# import functions.luno_api_functions.luno_get_transactions as luno_get_transactions
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# List of account IDs and assets
account_ids = ["8075122085411341746", "9119250031648298122", "8186407348185805061", "687412742627896300", 
               "3784206532036387289", "8772730523187070049", "4754107407400490211", "3663503223668122216", 
               "3731946183750833758", "4715269767296112715", "4044512054462273666", "7604837217064805551"]

assets_list = ["ALL", "BCH", "XBT", "ETH", "LINK", "LTC", "UNI", "USDC", "XRP", "ZAR"]

# Initialize the TTS engine (only once)
engine = pyttsx3.init()

# Run TTS engine once
def run_tts_once(text):
    """Run TTS engine once on app startup."""
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Stop after running once

# Run TTS with an initial message (optional)
run_tts_once("Welcome to the Trading App. Please make your selections.")

# Streamlit app UI
st.title("Trading App")

assets = st.selectbox("Select Asset for Balance", assets_list)

# if st.button("Get Balance"):
#     if assets == "ALL":
#         balance_list = luno_get_balance.get_balance("")
#     else:
#         balance_list = luno_get_balance.get_balance(assets)
    
#     if balance_list:
#         st.write("Balance List:")
#         balance_df = pd.DataFrame(balance_list)
#         st.dataframe(balance_df)
#     else:
#         st.write("No balance information available.")

# st.button("Get Fee Info", on_click=luno_get_fee_info.get_fee_info)

# id = st.selectbox("Select Account ID", account_ids)
# st.button(f"Get Transactions for {id}", on_click=lambda: luno_get_transactions.get_transactions(id))

# Select Model
st.markdown("## Select Model")
model = st.selectbox("Select Model", ["llama3.1"])

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Streamlit UI for LLM
text_input = st.text_input("Ask LLM:")
text_output = st.empty()  # Use an empty container for dynamic content

if st.button("Ask LLM"):
    if text_input:  # Ensure there's user input
        response = client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": "Please respond thoughtfully."},
                {"role": "user", "content": f"{text_input}"}
            ],
            temperature=0.7,
        )

        # Check if response has valid choices
        if response.choices and hasattr(response.choices[0], 'message'):
            output_text = response.choices[0].message.content
            text_output.text_area("Response", output_text, height=300)  # Display the response
        else:
            output_text = "No valid response generated."
            text_output.text_area("Response", output_text, height=300)
    else:
        text_output.text("Please enter a question.")
