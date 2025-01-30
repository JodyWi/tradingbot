import requests
import time
import os
import base64
from dotenv import load_dotenv
from luno_python.client import Client
import autogen
from autogen import AssistantAgent
from autogen import UserProxyAgent
from autogen import code_utils
from autogen.code_utils import *
from autogen import retrieve_utils

#Model Config / API
config_list = {
        "model": "vicuna-7b-v1.5-16k",
        "api_base": "http://localhost:8000/v1",
        "api_type": "open_ai",
        "api_key": "YOUR_OPENAI_API_KEY",  # Replace with your OpenAI API key
}

#Model Settings
llm_config = {
    "request_timeout": 2000,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "max_tokens": 16000
}


#load_dotenv()# Load environment variables from .env file


# Luno API endpoint for retrieving account balances
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

if __name__ == '__main__':
    user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    llm_config=llm_config,
    system_message="Welcome, I'm your dedicated User Proxy Agent, designed to assist you with a human touch.",
    code_execution_config={"last_n_messages": 2, "work_dir": "Projects", "use_docker": False,},
    human_input_mode="TERMINATE",
    is_termination_msg={"content", 
                        "role" "Manager", 
                        "name", 
                        "function_call"},
    #role="Project Manager",
    #backstory="Meet the Project Manager, your guide in the realm of innovation. With years of experience in navigating complex projects, the Project Manager is here to ensure your endeavors within the Projects folder are streamlined and successful. They bring a wealth of knowledge, a keen eye for opportunities, and a knack for turning challenges into triumphs. Trust in their expertise, and let them lead you towards unparalleled project excellence."
    )

    pm = autogen.AssistantAgent(
    name="Project_manager",
    system_message="""fghdghjfg""",
    llm_config=llm_config,
    code_execution_config={"work_dir": "Projects",
                            "use_docker": False,  },# Set to True to use Docker                           
    )
    user_proxy.initiate_chat( 
    pm,
    message="do you have access to luno?"
)


