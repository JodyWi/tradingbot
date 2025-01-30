# Luno API balance endpoint | tradingbot/Backend/luno_api_functions/luno_py

import os
from flask import request, jsonify
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Luno API base URL
LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Check for required environment variables
if not all([LUNO_API_URL, API_KEY, API_SECRET]):
    logger.error("Missing required Luno API environment variables.")
    raise EnvironmentError("API credentials or URL are not set in the environment.")

# API route function for Luno 

@app.route("/api/1/withdrawal", methods=["POST"])
def create_withdrawal():
    data = request.json
    amount = data.get('amount')
    currency = data.get('currency')
    address = data.get('address')

    if not all([amount, currency, address]):
        return jsonify({"error": "amount, currency, and address are required"}), 400

    response = requests.post(
        f"{LUNO_API_URL}/api/1/withdrawal",
        json={"amount": amount, "currency": currency, "address": address},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code