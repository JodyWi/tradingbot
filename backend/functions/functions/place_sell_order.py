import requests
import os
import base64
from luno_python.client import Client
from dotenv import load_dotenv

load_dotenv()

# Define the Luno API endpoint for placing market orders
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/marketorder"

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

    # Construct the request payload
    payload = {
        "pair": "LINKZAR",  # Example pair, replace with your desired pair
        "type": "SELL",      # Type is set to SELL for a sell order
        "base_volume": "0.1" # Example volume, adjust as needed
    }

    # Make a POST request to place the market order
    response = requests.post(LUNO_API_ENDPOINT, headers=headers, json=payload)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        order_id = response.json()["order_id"]
        print(f"Market order placed successfully. Order ID: {order_id}")
    else:
        print(f"Failed to place market order. Status code: {response.status_code}")
