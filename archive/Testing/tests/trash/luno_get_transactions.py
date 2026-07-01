# Luno API balance endpoint | tradingbot/Backend/luno_api_functions/luno_get_transactions.py

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

# To be Returned
# {
#   "id": "string",
#   "transactions": [
#     {
#       "account_id": "string",
#       "available": "string",
#       "available_delta": "string",
#       "balance": "string",
#       "balance_delta": "string",
#       "currency": "string",
#       "description": "string",
#       "detail_fields": {
#         "crypto_details": {
#           "address": "string",
#           "txid": "string"
#         },
#         "trade_details": {
#           "pair": "string",
#           "price": "string",
#           "sequence": 0,
#           "volume": "string"
#         }
#       },
#       "details": {
#         "property1": "string",
#         "property2": "string"
#       },
#       "kind": "FEE",
#       "reference": "string",
#       "row_index": 0,
#       "timestamp": 0
#     }
#   ]
# }

#
def get_transactions(id):
    # Luno API endpoint
    LUNO_API_ENDPOINT = f"https://api.luno.com/api/1/accounts/{id}/transactions"

    if API_KEY_ID is None or API_KEY_SECRET is None:
        print("Luno API credentials not found. Please check your .env file.")
        return None

    # Prepare authentication headers
    credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Make a GET request
    response = requests.get(LUNO_API_ENDPOINT, headers=headers)

    if response.status_code == 200:
        # Log the entire response to troubleshoot
        full_response = response.json()
        logger.info(f"Full response: {full_response}")

        # Check if transactions are present
        transactions = full_response.get("transactions", None)

        if transactions is None:
            st.error(f"No transactions found for account ID {id}.")
            logger.error(f"No transactions in response for account {id}")
            return []

        # Prepare transactions list
        transactions_list = []
        for transaction in transactions:
            transactions_list.append({
                "id": transaction['id'],
                "account_id": transaction['account_id'],
                "available": transaction['available'],
                "available_delta": transaction['available_delta'],
                "balance": transaction['balance'],
                "balance_delta": transaction['balance_delta'],
                "currency": transaction['currency'],
                "description": transaction['description'],
                "detail_fields": transaction['detail_fields'],
                "details": transaction['details'],
                "kind": transaction['kind'],
                "reference": transaction['reference'],
                "row_index": transaction['row_index'],
                "timestamp": transaction['timestamp']
            })

        # Save transactions to a file
        with open(f"Transactions_{id}_{datetime.datetime.now()}.json", "w") as f:
            for transaction in transactions_list:
                json.dump(transaction, f)
                f.write('\n')

        # Return the transactions list
        return transactions_list

    else:
        # Handle API errors
        logger.error(f"Failed to fetch transactions. Status code: {response.status_code}")
        logger.error(f"Response: {response.text}")
        st.error(f"Failed to fetch transactions for account ID {id}.")
        return []
