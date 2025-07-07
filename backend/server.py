# server.py
import os
import sys
import base64
import sqlite3
import requests

# Ensure the backend directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


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
# Ticker Api's
#############################
from luno_functions.luno_ticker import get_ticker, get_tickers
# curl -X POST http://localhost:8001/api/1/tickers
# curl -X POST "http://localhost:8001/api/1/ticker?pair=LTCZAR"
@app.route("/api/1/ticker", methods=["POST"])
def get_ticker_api():
    pair = request.args.get("pair", default="")
    if not pair:
        return jsonify({"error": "pair is required"}), 400
    try:
        result = get_ticker(pair=pair)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/api/1/tickers", methods=["POST"])
def get_tickers_api():
    try:
        result = get_tickers()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#############################
# Balance Api's
#############################
from luno_functions.luno_balance import get_balance, get_balances
# curl -X POST http://localhost:8001/api/1/balances
# curl -X POST "http://localhost:8001/api/1/balance?assets=ZAR"
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
# Trade Api's
#############################
# curl -X POST http://localhost:8001/api/1/trades
# curl -X POST "http://localhost:8001/api/1/trade?pair=LTCZAR"
from luno_functions.luno_listTrades import get_trade
@app.route("/api/1/trade", methods=["POST"])
def get_trade_api():
    try:
        pair = request.args.get("pair", default="LTCZAR")
        result = get_trade(pair=pair)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#############################
# Get Fees Api's
#############################

from luno_functions.luno_feeInfo import get_fee_info
# curl -X POST http://localhost:8001/api/1/fee_info
# curl -X POST "http://localhost:8001/api/1/fee_info?pair=LTCZAR"
@app.route("/api/1/fee_info", methods=["POST"])
def get_fee_info_api():
    try:
        pair = request.args.get("pair", default="LTCZAR")
        result = get_fee_info(pair=pair)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#############################
# Get Markets Info Api's
#############################

from luno_functions.luno_marketsInfo import get_markets_info
# curl -X POST http://localhost:8001/api/1/markets_info
# curl -X POST "http://localhost:8001/api/1/markets_info?pair=LTCZAR"
@app.route("/api/1/markets_info", methods=["POST"])
def get_markets_info_api():    
    try:
        pair = request.args.get("pair", default="LTCZAR")
        result = get_markets_info(pair=pair)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



#############################
# Entry Point
#############################
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)
