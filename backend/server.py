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

# Constants
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "tradingbot.db")
LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")


#############################
# DB Helpers
#############################

def connect_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            asset TEXT NOT NULL,
            trade_type TEXT NOT NULL,
            amount REAL NOT NULL,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            asset TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def insert_trade(asset, trade_type, amount, price):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO trades (asset, trade_type, amount, price)
            VALUES (?, ?, ?, ?)
        ''', (asset, trade_type, float(amount), float(price)))
        conn.commit()
        print(f"✅ Trade recorded: {asset} {trade_type} {amount} @ {price}")
    except Exception as e:
        print(f"❌ Error inserting trade: {e}")
    finally:
        conn.close()

def update_balance(asset, balance):
    try:
        balance = float(balance)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO balances (asset, balance) 
            VALUES (?, ?)
            ON CONFLICT(asset) DO UPDATE SET balance = excluded.balance
        ''', (asset, balance))
        conn.commit()
        print(f"✅ Balance updated: {asset} => {balance}")
    except Exception as e:
        print(f"❌ Error updating balance: {e}")
    finally:
        conn.close()

#############################
# Routes
#############################

@app.route('/balance', methods=['GET'])
def local_balance():
    assets = request.args.get("assets", "")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT asset, balance FROM balances WHERE asset = ?", (assets,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({"status": "success", "balances": {row[0]: row[1]}})
    else:
        return jsonify({"status": "error", "message": "Balance not found"}), 404

@app.route("/api/1/balance", methods=["GET"])
def get_luno_balance():
    asset = request.args.get('assets')
    if not asset:
        return jsonify({"error": "No asset provided"}), 400

    if not API_KEY_ID or not API_KEY_SECRET:
        return jsonify({"error": "Missing API credentials"}), 500

    credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = { "Authorization": f"Basic {encoded_credentials}" }

    response = requests.get(f"{LUNO_API_ENDPOINT}?assets={asset}", headers=headers)

    if response.status_code == 200:
        balances = response.json().get("balance", [])
        return jsonify({"balances": balances}), 200
    else:
        return jsonify({"error": "Failed to retrieve balances"}), response.status_code

@app.route('/api/trades', methods=['GET'])
def get_trades():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trades")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()
    return jsonify({"status": "success", "trades": [dict(zip(column_names, row)) for row in rows]})

@app.route('/api/balances', methods=['GET'])
def get_balances():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM balances")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()
    return jsonify({"status": "success", "balances": [dict(zip(column_names, row)) for row in rows]})


#############################
# Entry Point
#############################
if __name__ == '__main__':
    create_tables()  # Optional: Auto-create tables if they don't exist
    app.run(host="0.0.0.0", port=8001, debug=True)
