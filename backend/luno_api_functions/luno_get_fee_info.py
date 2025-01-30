# Luno API balance endpoint | tradingbot/Backend/luno_api_functions/luno_py

import os
import base64
import requests
import logging
import json
import datetime 
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Luno API endpoint
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/fee_info"

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")


def get_fee_info():
    if API_KEY_ID is None or API_KEY_SECRET is None:
        print("Luno API credentials not found. Please check your .env file.")
    else:
        # Prepare authentication headers
        credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_credentials}"
        }

        # Make a GET request
        response = requests.get(LUNO_API_ENDPOINT, headers=headers)

        if response.status_code == 200:
            # Parse JSON response
            fee_info = response.json().get("balance", [])

            # Prepare a JSON response 
            fees_list = []
            for fees in fee_info:
                fees_list.append({
                    "Maker Fees": fees['maker_fee'],
                    "Taker Fees": fees['taker_fee'],
                    "30 Day Volume": fees['thirty_day_volume']
                })

            # save raw json split with time stamp
            with open(f"Fee_Info_{datetime.datetime.now()}.json", "w") as f:
                for fees in fees_list:

                    # Save split lines in a json file
                    json.dump(fees, f)
                    f.write("\n")
        else:
            print(f"Failed to retrieve Fee Info. Status code: {response.status_code}")

        return response
    
if __name__ == "__main__":
    get_fee_info()


# Error Failed to retrieve Fee Info. Status code: 400