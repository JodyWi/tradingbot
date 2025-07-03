import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def connect_db():
    """Local DB connection just for this script"""
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DB_PATH = os.path.join(BASE_DIR, "database", "tradingbot.db")
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def get_balance():
    """Call Luno API for balance and store them"""
    response = requests.get(
        f"{LUNO_API_URL}/api/1/balance",
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")

    data = response.json()
    print(response)
    # store_db(data["balances"])
    return {"status": "success", "count": len(data["balances"])}

# def clean_balance(value):
#     """Ensure the balance is a valid number."""
#     try:
#         return float(value)  # Convert to float if possible
#     except ValueError:
#         logger.error(f"❌ Invalid balance value received: {value}. Storing as 0.0")
#         return 0.0  # Default to 0.0 if conversion fails

# def store_db(balances):
#     """Store all balance data as history (no overwrite)"""
#     conn = connect_db()
#     cursor = conn.cursor()

#     try:
#         # Create table for balance history with auto-increment ID
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS balance_history (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 pair TEXT,
#                 timestamp INTEGER,
#                 bid TEXT,
#                 ask TEXT,
#                 last_trade TEXT,
#                 volume TEXT,
#                 status TEXT
#             )
#         """)

#         # Insert all balances as new rows (no conflict handling)
#         for balance in balances:
#             cursor.execute("""
#                 INSERT INTO balance_history (pair, timestamp, bid, ask, last_trade, volume, status)
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 balance["pair"],
#                 balance["timestamp"],
#                 balance["bid"],
#                 balance["ask"],
#                 balance["last_trade"],
#                 balance["rolling_24_hour_volume"],
#                 balance["status"]
#             ))
#             print(f"✅ Stored history for: {balance['pair']}")

#         conn.commit()
#     except Exception as e:
#         print(f"❌ Error storing balance history: {e}")
#     finally:
#         conn.close()



# def store_balance(asset, balance):
#     """ Store or update balance in the database safely """
#     conn = connect_db()
#     cursor = conn.cursor()

#     try:
#         # ✅ Ensure balance is always a number
#         try:
#             clean_balance = float(balance) if balance and balance.replace('.', '', 1).isdigit() else 0.0
#         except ValueError:
#             clean_balance = 0.0  # If conversion fails, default to 0.0

#         # ✅ Check if asset exists
#         cursor.execute("SELECT id FROM balances WHERE asset = ?", (asset,))
#         existing_entry = cursor.fetchone()

#         if existing_entry:
#             cursor.execute(
#                 "UPDATE balances SET balance = ?, timestamp = CURRENT_TIMESTAMP WHERE asset = ?",
#                 (clean_balance, asset)
#             )
#         else:
#             cursor.execute(
#                 "INSERT INTO balances (asset, balance) VALUES (?, ?)",
#                 (asset, clean_balance)
#             )

#         conn.commit()
#     except Exception as e:
#         print(f"❌ Error storing balance for {asset}: {e}")
#     finally:
#         conn.close()

# def get_balance(assets=""):
#     """ Fetch balance from Luno API and store in database """
#     LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"
#     if assets:
#         LUNO_API_ENDPOINT += f"?assets={assets}"

#     if not API_KEY_ID or not API_KEY_SECRET:
#         logger.error("Luno API credentials not found.")
#         return {"status": "error", "message": "Missing API credentials"}

#     credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
#     encoded_credentials = base64.b64encode(credentials.encode()).decode()
#     headers = {"Authorization": f"Basic {encoded_credentials}"}

#     response = requests.get(LUNO_API_ENDPOINT, headers=headers)

#     if response.status_code == 200:
#         balances = response.json().get("balance", [])
        
#         results = []
#         for balance in balances:
#             asset = balance.get('asset', 'UNKNOWN')
#             value = balance.get('balance', '0.0')

#             store_balance(asset, value)  # ✅ Save to DB
            
#             results.append({
#                 "Asset": asset,
#                 "Balance": float(value) if value.replace('.', '', 1).isdigit() else 0.0
#             })

#         return {"status": "success", "balances": results}
#     else:
#         logger.error(f"Failed to retrieve balances. Status code: {response.status_code}")
#         return {"status": "error", "message": "API request failed"}

# "/api/1/balance": {
#   "get": {
#     "description": "The list of all Accounts and their respective balances for the requesting user.\n\nPermissions required: <code>Perm_R_Balance</code>",
#     "tags": [
#       "Accounts"
#     ],
#     "summary": "List account balances",
#     "operationId": "getBalances",
#     "parameters": [
#       {
#         "example": "XBT",
#         "x-go-name": "Assets",
#         "description": "Only return balances for wallets with these currencies (if not provided,\nall balances will be returned). To request balances for multiple currencies,\npass the parameter multiple times,\ne.g. `assets=XBT&assets=ETH`.",
#         "name": "assets",
#         "in": "query",
#         "style": "form",
#         "explode": false,
#         "schema": {
#           "type": "array",
#           "items": {
#             "type": "string"
#           }
#         }
#       }
#     ],
#     "responses": {
#       "200": {
#         "description": "OK",
#         "content": {
#           "application/json": {
#             "schema": {
#               "$ref": "#/components/schemas/getBalancesResponse"
#             }
#           }
#         }
#       }
#     }
#   }
# },