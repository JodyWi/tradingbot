import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

from dotenv import load_dotenv
from luno_api_functions.luno_get_balance import get_balance


# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)


# Route to get balance
@app.route('/balance', methods=['GET'])
def balance():
    assets = request.args.get("assets", "")  # Get asset from query params
    balances = get_balance(assets)  # Fetch balances

    if balances:
        return jsonify({"status": "success", "balances": balances})
    else:
        return jsonify({"status": "error", "message": "Failed to fetch balances"}), 500
    

@app.route('/api/trades', methods=['GET'])
def get_trades():
    conn = sqlite3.connect('../database/tradingbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades")
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]
    trades = [dict(zip(column_names, row)) for row in rows]

    conn.close()
    return jsonify({"status": "success", "trades": trades})

@app.route('/api/balances', methods=['GET'])
def get_balances():
    conn = sqlite3.connect('../database/tradingbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balances")
    rows = cursor.fetchall()

    column_names = [description[0] for description in cursor.description]
    balances = [dict(zip(column_names, row)) for row in rows]

    conn.close()
    return jsonify({"status": "success", "balances": balances})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)
