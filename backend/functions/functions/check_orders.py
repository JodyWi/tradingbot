#check_orders.py
import requests
import os
import base64
from luno_python.client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the Luno API endpoint for listing orders
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/listorders"


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

    # Make a GET request to retrieve the most recent orders
    response = requests.get(LUNO_API_ENDPOINT, headers=headers)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse JSON response
        orders = response.json()["orders"]

        # Check if orders exist
        if orders:
            # Print order details
            for order in orders:
                print(f"Order ID: {order['order_id']}")
                print(f"Pair: {order['pair']}")
                print(f"Type: {order['type']}")
                print(f"Volume: {order['limit_volume']}")
                print(f"Price: {order['limit_price']}")
                print(f"State: {order['state']}")
                print("-" * 30)
        else:
            print("No orders found.")
    else:
        print(f"Failed to retrieve orders. Status code: {response.status_code}")