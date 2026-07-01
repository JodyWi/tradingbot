import os
import base64
import requests
import logging
import json
import datetime
import pandas as pd
import streamlit as st
import ollama 
# from langchain.llms import Ollama
from langchain_community.llms import Ollama
import pyttsx3

import functions.luno_api_functions.luno_get_balance as luno_get_balance
#import functions.luno_api_functions.luno_get_order_book as luno_get_order_book
import functions.luno_api_functions.luno_get_fee_info as luno_get_fee_info
import functions.luno_api_functions.luno_get_transactions as luno_get_transactions

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Voice engine
# Initialize the engine
engine = pyttsx3.init()


# LLM settings


# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# List of account IDs
account_ids = [
    "8075122085411341746",
    "9119250031648298122",
    "8186407348185805061",
    "687412742627896300",
    "3784206532036387289",
    "8772730523187070049",
    "4754107407400490211",
    "3663503223668122216",
    "3731946183750833758",
    "4715269767296112715",
    "4044512054462273666",
    "7604837217064805551",
]

# List of assets
assets_list = [
    "ALL",
    "BCH",
    "XBT",
    "ETH",
    "LINK",
    "LTC",
    "UNI",
    "USDC",
    "XRP",
    "ZAR",
]

# Streamlit app UI
st.title("Trading App")

assets = st.selectbox("Select Asset for Balance", assets_list)

if st.button("Get Balance"):
    # If "ALL" is selected, pass an empty string to get all balances
    if assets == "ALL":
        balance_list = luno_get_balance.get_balance("")
    else:
        balance_list = luno_get_balance.get_balance(assets)
    
    # Display the balance
    if balance_list:
        st.write("Balance List:")
        # Display using pandas
        
        balance_df = pd.DataFrame(balance_list)
        st.dataframe(balance_df)
        #st.json(balance_list)
    else:
        st.write("No balance information available.")


# Button for getting fee info
st.button("Get Fee Info", on_click=luno_get_fee_info.get_fee_info)

# Select account ID using a dropdown
id = st.selectbox("Select Account ID", account_ids)

# Use lambda function to pass 'id' as argument to 'get_transactions'
st.button(f"Get Transactions for {id}", on_click=lambda: luno_get_transactions.get_transactions(id))

# Uncomment the following line if needed for order book
# st.button("Get Order Book", on_click=luno_get_order_book.get_order_book)

# Select Model
st.markdown("## Select Model")
model = st.selectbox("Select Model", ["llama3.1"])

# Text Input
st.markdown("## Text Input")
text_input = st.text_input("Enter your question:", "")

# Initialize LLM
llm = Ollama(model=model)

# Text output
st.markdown("## LLM Text Output")
text_output = st.empty()

# Get available voices
voices = engine.getProperty('voices')

# Handle user input and LLM prediction
if st.button("Ask LLM"):
    if text_input:  # Ensure there's user input
        response = llm.invoke(text_input)
        # Output the response using a text area to prevent horizontal scrolling
        text_output.text_area("Response", response, height=300)  # Multiline text box with wrapping
    
        # play the response using pyttsx3
        engine.say(response)
        engine.runAndWait()
    else:
        text_output.text("Please enter a question.")


# prompt = st.selectbox("Select Prompt", ["What is the price of BTC?"])

# # Handle user input and LLM prediction using the functions
# if st.button("Ask LLM to check balance"):
#     if text_input:  # Ensure there's user input
#         response = llm.invoke(text_input)
#         # Output the response using a text area to prevent horizontal scrolling
#         text_output.text_area("Response", response, height=300)  # Multiline text box with wrapping
    
#         # play the response using pyttsx3
#         engine.say(response)
#         engine.runAndWait()
#     else:
#         text_output.text("Please enter a question.")


## LLM functions adding all Luno functions

# trying to find a way to add all Luno functions to the llm
# try to get the llm to call functions
# list the functions
# balance function



# ollama balance function



