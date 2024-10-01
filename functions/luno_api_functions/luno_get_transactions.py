

import requests
import base64
import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")









def get_transactions(id):
    LUNO_API_ENDPOINT = f"https://api.luno.com/api/1/transactions?account_id={id}"

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
            transactions = response.json().get("transactions", [])

            if transactions is None:
                # If the API does not return a balance key, return an empty list

                logger.error("No transactions data returned.")
                return []

            else:
                return transactions
            

if __name__ == "__main__":
    print(get_transactions(""))