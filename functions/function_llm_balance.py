import os
import httpx
import torch
import base64
import requests
import logging
import json
import datetime
from openai import OpenAI
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

import autogen
from autogen.cache import Cache
from autogen.coding import CodeBlock, LocalCommandLineCodeExecutor


from functions.luno_api_functions.luno_get_balance import get_balance


from functions.function_tts import run_tts_tts 
from functions.function_tts_pyttsx3 import run_tts_pyttsx3

# Run run_tts_tts for Agent balancebot
# Run run_tts_pyttsx3 for Agent user_proxy

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

import httpx


# class MyHttpClient(httpx.Client):
#     def __deepcopy__(self, memo):
#         return self


config_list = [
    {
        "model": "TheBloke/vicuna-7B-v1.5-16K-GGUF",
        "base_url": "http://localhost:1234/v1",
        "api_key": "",
        # "http_client": MyHttpClient(proxy="http://localhost:1234/v1"),
    }
]

# llm_config = {
#     "config_list": config_list,
#     "timeout": 120,
# }


def llm_balance_check():
    

    # create an AssistantAgent named "assistant"
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={
            "cache_seed": 41,  # seed for caching and reproducibility
            "config_list": config_list,  # a list of OpenAI API configurations
            "temperature": 0,  # temperature for sampling
        },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
    )

    # create a UserProxyAgent instance named "user_proxy"
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            # the executor to run the generated code
            "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
        },
    )
    # the assistant receives a message from the user_proxy, which contains the task description
    chat_res = user_proxy.initiate_chat(
        assistant,
        message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
        summary_method="reflection_with_llm",
    )

    return chat_res 