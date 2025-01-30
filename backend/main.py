import os
import base64
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Add this to enable CORS for all routes

# Luno API endpoint for retrieving account balances
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")


@app.route("/api/1/balance", methods=["GET"])
def get_balance():
    asset = request.args.get('assets')  # Fetch query parameter
    if asset is None:
        return jsonify({"error": "No asset provided"}), 400

    # Check if API credentials are available
    if API_KEY_ID is None or API_KEY_SECRET is None:
        return jsonify({"error": "API credentials not found. Check your .env file."}), 500

    # Prepare authentication headers
    credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    # Add the asset parameter to the URL
    response = requests.get(f"{LUNO_API_ENDPOINT}?assets={asset}", headers=headers)

    if response.status_code == 200:
        balances = response.json().get("balance", [])
        return jsonify({"balances": balances}), 200
    else:
        return jsonify({"error": f"Failed to retrieve account balances. Status code: {response.status_code}"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
