import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from luno_api_functions.luno_get_balance import get_balance

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Route to get balance
@app.route('/balance', methods=['GET'])
def balance():
    assets = request.args.get("assets", "")  # Get asset from query params
    balances = get_balance(assets)  # Fetch balances

    if balances:
        return jsonify({"status": "success", "balances": balances})
    else:
        return jsonify({"status": "error", "message": "Failed to fetch balances"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)
