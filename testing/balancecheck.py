import requests
import os
import base64
from dotenv import load_dotenv
from luno_python.client import Client

# Load environment variables from .env file
load_dotenv()

# Luno API endpoint for retrieving account balances
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance?assets=ETH"

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



    # save raw json split by account_id
    with open("balances_by_account_id.json", "w") as f:
        for balance in balances:
            account_id = balance["account_id"]
            account_balances = [b for b in balances if b["account_id"] == account_id]
            f.write(f"Account ID: {account_id}\n")
            f.write(f"Asset: {balance['asset']}\n")
            f.write(f"Balance: {balance['balance']}\n")
            f.write(f"reserved: {balance['reserved']}\n")
            f.write(f"unconfirmed: {balance['unconfirmed']}\n")

    with open("balances.json", "w") as f:
        f.write(response.text)


# main


