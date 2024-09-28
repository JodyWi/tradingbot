
import os
import logging
import pyttsx3
import threading
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


import functions.luno_api_functions.luno_get_balance as luno_get_balance
# import functions.luno_api_functions.luno_get_fee_info as luno_get_fee_info
# import functions.luno_api_functions.luno_get_transactions as luno_get_transactions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Select Model
st.markdown("## Select Model")
model = st.selectbox("Select Model", ["llama3.1"])

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# List of account IDs and assets
account_ids = ["8075122085411341746", "9119250031648298122", "8186407348185805061", "687412742627896300", 
               "3784206532036387289", "8772730523187070049", "4754107407400490211", "3663503223668122216", 
               "3731946183750833758", "4715269767296112715", "4044512054462273666", "7604837217064805551"]

assets_list = ["ALL", "BCH", "XBT", "ETH", "LINK", "LTC", "UNI", "USDC", "XRP", "ZAR"]



# Run TTS engine once
def run_tts(text):
    """Run TTS engine once on app startup."""

    # Initialize the TTS engine (only once)
    engine = pyttsx3.init()

    # Select the voice index
    engine.setProperty("voice", "english")
    engine.setProperty("rate", 150)

    # Run TTS engine once
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Stop after running once

# # Run TTS with an initial message (optional)
# run_tts_once("Welcome to the Trading App. Please make your selections.")

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


from pathlib import Path
import autogen
from autogen.cache import Cache
from autogen.coding import CodeBlock, LocalCommandLineCodeExecutor



def create_code_blocks():
    
    work_dir = Path("coding")
    work_dir.mkdir(exist_ok=True)

    executor = LocalCommandLineCodeExecutor(work_dir=work_dir)
    print(
        executor.execute_code_blocks(
            code_blocks=[
                CodeBlock(language="python", code="print('Hello, Wdddrorld!')"),
            ]
        )
    )

    print(executor.functions)


import httpx


class MyHttpClient(httpx.Client):
    def __deepcopy__(self, memo):
        return self


config_list = [
    {
        "model": "my-gpt-4-deployment",
        "api_key": "",
        "http_client": MyHttpClient(proxy="http://localhost:1234/v1"),
    }
]

# config_list = client
# config_list = [
#     {
#         'model': 'gpt-3.5-turbo',
#         'api_key': '<your OpenAI API key here>',
#         'tags': ['tool', '3.5-tool'],
#     },
#     {
#         'model': 'gpt-3.5-turbo',
#         'api_key': '<your Azure OpenAI API key here>',
#         'base_url': '<your Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-02-01',
#         'tags': ['tool', '3.5-tool'],
#     },
#     {
#         'model': 'gpt-3.5-turbo-16k',
#         'api_key': '<your Azure OpenAI API key here>',
#         'base_url': '<your Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-02-01',
#         'tags': ['tool', '3.5-tool'],
#     },
# ]

def balance_check():
    llm_config = {
        "config_list": config_list,
        "timeout": 120,
    }

    balancebot = autogen.AssistantAgent(
        name="chatbot",
        system_message="For Checking balance tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
        llm_config=llm_config,
    )

    # create a UserProxyAgent instance named "user_proxy"
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
    )

    # Register the get_balance function in function_map
    user_proxy.function_map["get_balance"] = luno_get_balance.get_balance

    # Assert the correct origin
    assert user_proxy.function_map["get_balance"] == luno_get_balance.get_balance

    with Cache.disk() as cache:
        # start the conversation
        res = user_proxy.initiate_chat(
            balancebot, message="How much the balances?", summary_method="reflection_with_llm", cache=cache
        )

        # print the summary message
        print("Chat summary:", res.summary)
        return res.summary


if st.button("Balance Check"):
    summary = balance_check()
    st.write(summary)
    run_tts(summary)
    


# Streamlit UI for Coder
st.markdown("## Coder")

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


if st.button("Run Code"):
    create_code_blocks()






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
            run_tts(output_text)
        else:
            output_text = "No valid response generated."
            text_output.text_area("Response", output_text, height=300)
    else:
        text_output.text("Please enter a question.")
