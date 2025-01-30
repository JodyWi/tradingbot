# place_link_order.py

import requests
import os
import base64
from luno_python.client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the Luno API endpoint for placing a limit order
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/postorder"

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# Check if API credentials are available
if API_KEY_ID is None or API_KEY_SECRET is None:
    print("Luno API credentials not found. Please check your environment variables.")
else:
    # Prepare authentication headers
    headers = {
        "Authorization": f"Basic {API_KEY_ID}:{API_KEY_SECRET}"
    }

    # Define order parameters for the LINK/ZAR trading pair
    pair = "LINKZAR"    # Currency pair (Chainlink to South African Rand)
    type = "BID"         # BID for a buy limit order, ASK for a sell limit order
    volume = "0.11"      # Adjusted volume to be more than 0.10 LINK
    price = "100"        # Limit price for the order in ZAR

    # Define payload for the request
    payload = {
        "pair": pair,
        "type": type,
        "volume": volume,
        "price": price
    }

    # Make a POST request to place the limit order
    response = requests.post(LUNO_API_ENDPOINT, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        order_id = response.json()["order_id"]
        print(f"Limit order for Chainlink successfully placed. Order ID: {order_id}")
    else:
        print(f"Failed to place limit order. Status code: {response.status_code}")
