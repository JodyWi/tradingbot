import os
import base64
import requests
import logging
import json
import datetime
import streamlit as st
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# Print env path
logger.info(f"API_KEY_ID: {API_KEY_ID}")
logger.info(f"API_KEY_SECRET: {API_KEY_SECRET}")

def get_balance(assets):
    # If "ALL" is selected, do not append the assets query parameter
    if assets == "":
        LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"
    else:
        LUNO_API_ENDPOINT = f"https://api.luno.com/api/1/balance?assets={assets}"

    # Check if API credentials are available
    if API_KEY_ID is None or API_KEY_SECRET is None:
        print("Luno API credentials not found. Please check your .env file.")
        return None
    else:
        # Prepare authentication headers
        credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        # Make a GET request to retrieve account balances
        response = requests.get(LUNO_API_ENDPOINT, headers=headers)

        if response.status_code == 200:
            # Parse JSON response
            balances = response.json().get("balance", [])

            if balances is None:
                # If the API does not return a balance key, return an empty list
                logger.error("No balance data returned.")
                return []

            # Prepare a list of balances to return
            balance_list = []
            for balance in balances:
                balance_list.append({
                    "Asset": balance['asset'],
                    "Account ID": balance['account_id'],
                    "Balance": balance['balance'],
                    "Reserved": balance['reserved'],
                    "Unconfirmed": balance['unconfirmed']
                })

            return balance_list
        else:
            logger.error(f"Failed to retrieve account balances. Status code: {response.status_code}")
            return []
















if __name__ == "__main__":
    print(get_balance(""))

