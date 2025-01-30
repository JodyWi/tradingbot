# backend/luno_api_functions/luno_get_balance.py
import os
import base64
import requests
import sqlite3
import logging
from dotenv import load_dotenv
from database import connect_db  # Ensure database connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Luno API credentials
API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

def store_balance(asset, balance):
    """ Store or update balance in the database """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Check if asset exists
    cursor.execute("SELECT * FROM balances WHERE asset = ?", (asset,))
    existing_entry = cursor.fetchone()
    
    if existing_entry:
        # Update balance
        cursor.execute(
            "UPDATE balances SET balance = ?, timestamp = CURRENT_TIMESTAMP WHERE asset = ?",
            (balance, asset)
        )
    else:
        # Insert new balance entry
        cursor.execute(
            "INSERT INTO balances (asset, balance) VALUES (?, ?)",
            (asset, balance)
        )
    
    conn.commit()
    conn.close()

def get_balance(assets=""):
    """ Fetch balance from Luno API and store in database """
    LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"
    if assets:
        LUNO_API_ENDPOINT += f"?assets={assets}"

    if not API_KEY_ID or not API_KEY_SECRET:
        logger.error("Luno API credentials not found.")
        return None

    credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = requests.get(LUNO_API_ENDPOINT, headers=headers)

    if response.status_code == 200:
        balances = response.json().get("balance", [])
        
        # Store balances in DB
        for balance in balances:
            store_balance(balance['asset'], balance['balance'])

        return balances
    else:
        logger.error(f"Failed to retrieve balances. Status code: {response.status_code}")
        return []
