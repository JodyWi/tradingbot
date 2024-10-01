
import os
import shutil
import time
import logging
import pyttsx3
import threading
import datetime
from pathlib import Path
import httpx
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


from functions.luno_api_functions.luno_get_balance import get_balance
# import functions.luno_api_functions.luno_get_fee_info as luno_get_fee_info
# import functions.luno_api_functions.luno_get_transactions as luno_get_transactions

# LLM Functions
from functions.function_llm_balance import llm_balance_check



from functions.function_tts import run_tts_tts
from functions.function_tts_pyttsx3 import run_tts_pyttsx3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Directory to save the generated audio file
tts_directory = "data\\tts_data"
# C:\Users\jodyk\Desktop\GitHub\tradingbot_st\data\tts_data
os.makedirs(tts_directory, exist_ok=True)  # Ensure the directory exists


# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# Streamlit app UI
st.title("Trading App")


# Select Model
st.markdown("Select Model")
model = st.selectbox("Select Model", ["llama3.1"])

# List of account IDs and assets
account_ids = ["8075122085411341746", "9119250031648298122", "8186407348185805061", "687412742627896300", 
               "3784206532036387289", "8772730523187070049", "4754107407400490211", "3663503223668122216", 
               "3731946183750833758", "4715269767296112715", "4044512054462273666", "7604837217064805551"]

assets_list = ["ALL", "BCH", "XBT", "ETH", "LINK", "LTC", "UNI", "USDC", "XRP", "ZAR"]


assets = st.selectbox("Select Asset for Balance", assets_list)

if st.button("Get Balance"):
    if assets == "ALL":
        balance_list = get_balance("")
    else:
        balance_list = get_balance(assets)
    
    if balance_list:
        st.write("Balance List:")
        balance_df = pd.DataFrame(balance_list)
        st.dataframe(balance_df)
    else:
        st.write("No balance information available.")

# st.button("Get Fee Info", on_click=luno_get_fee_info.get_fee_info)

# id = st.selectbox("Select Account ID", account_ids)
# st.button(f"Get Transactions for {id}", on_click=lambda: luno_get_transactions.get_transactions(id))


if st.button("Balance Check using LLM"):
    summary = llm_balance_check()
    st.write(summary)
    run_tts_pyttsx3(summary)
    

# text_input = st.text_input("Code:")
# text_output = st.empty()  # Use an empty container for dynamic content

# if st.button("Run Code"):
#     if text_input:  # Ensure there's user input
#         output = executor.execute_code_blocks(
#             code_blocks=[
#                 CodeBlock(language="python", code=text_input),
#             ]
#         )
#         text_output.text_area("Output", output, height=300)  # Display the output
#     else:
#         text_output.text("Please enter some code.")





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
            #run_tts_pyttsx3(output_text)
            run_tts_tts(output_text)
        else:
            output_text = "No valid response generated."
            text_output.text_area("Response", output_text, height=300)
    else:
        text_output.text("Please enter a question.")





# C:\Users\jodyk\Desktop\GitHub\tradingbot_st\data\tts_data
# Clear audio cache directory
def clear_audio_cache(tts_directory):
    # Ensure pygame has stopped using the files
    time.sleep(1)  # Small delay to ensure file is released

    try:
        # Attempt to delete the directory and its contents
        shutil.rmtree(tts_directory)
        print(f"Successfully deleted {tts_directory}")
    except PermissionError as e:
        print(f"PermissionError: {e} - File is still in use.")
    except Exception as e:
        print(f"An error occurred: {e}")

if st.button("Clear Audio Cache"):
    clear_audio_cache(tts_directory)
    st.write("Audio cache cleared.")
    run_tts_pyttsx3(text="Audio cache cleared.")



