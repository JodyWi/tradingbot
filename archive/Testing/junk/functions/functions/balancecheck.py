import requests
import os
import base64
from dotenv import load_dotenv
from luno_python.client import Client

# Load environment variables from .env file
load_dotenv()

# Luno API endpoint for retrieving account balances
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# Check if API credentials are available
if API_KEY_ID is None or API_KEY_SECRET is None:
    print("Luno API credentials not found. Please check your .env file.")
else:
    # Prepare authentication headers
    credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Make a GET request to retrieve account balances
    response = requests.get(LUNO_API_ENDPOINT, headers=headers)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse JSON response
        balances = response.json()["balance"]

        # Print account balances
        for balance in balances:
            print(f"Asset: {balance['asset']}")
            print(f"Account ID: {balance['account_id']}")
            print(f"Balance: {balance['balance']}")
            print("-" * 30)
    else:
        print(f"Failed to retrieve account balances. Status code: {response.status_code}")


