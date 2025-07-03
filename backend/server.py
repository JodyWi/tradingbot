import os
import base64
import sqlite3
import requests

from flask import Flask, jsonify, request
from flask_cors import CORS

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)
CORS(app)

#############################
# Routes
#############################

#############################
# Ticker Point
#############################
from luno_api_functions.luno_ticker import get_ticker

@app.route("/api/1/ticker")
def api_get_ticker():
    pair = request.args.get('pair')
    if not pair:
        return jsonify({"error": "pair is required"}), 400
    try:
        result = get_ticker(pair)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#############################
# All Ticker Point
#############################
from luno_api_functions.luno_tickers import update_tickers

#@app.route("/api/1/tickers")
@app.route("/api/1/tickers/update", methods=["POST"])
def update_tickers_api():
    try:
        result = update_tickers()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#############################
# All Balance
#############################
from luno_api_functions.luno_balance import get_balances, get_balance

@app.route("/api/1/balance", methods=["POST"])
def get_balance_api():
    try:
        # Read the 'assets' query parameter from the request
        assets = request.args.get("assets", default="", type=str)
        result = get_balance(assets=assets)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/1/balances", methods=["POST"])
def get_balances_api():
    try:
        result = get_balances()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




#############################
# Entry Point
#############################
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)
