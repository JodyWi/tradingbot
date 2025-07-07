import os
import sqlite3
import requests
import uuid
from datetime import datetime, timezone, timedelta
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

# ✅ All assets working
def get_balances():
    """Call Luno API for all balances and store them"""
    response = requests.get(
        f"{LUNO_API_URL}/api/1/balance",
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")

    data = response.json()
    # print(data)
    store_db(data["balance"])
    return {"status": "success", "count": len(data["balance"])}

# ✅ Single asset or filtered assets
def get_balance(assets=""):
    """Call Luno API for one balance and store it"""
    if not assets:
        print("assets is required")
        raise ValueError("assets is required")
    
    response = requests.get(
        f"{LUNO_API_URL}/api/1/balance",
        params={"assets": assets},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")

    data = response.json()
    # print(data)
    store_db(data["balance"])
    return {"status": "success", "count": len(data["balance"])}

def store_db(balance_data):
    """Store all balance data as history (no overwrite)"""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Create table for balance history with auto-increment ID
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS balance_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                account_id TEXT,
                asset TEXT,
                balance TEXT,
                reserved TEXT,
                unconfirmed TEXT,
                timestamp TEXT
            )
        """)
        # Create table for Assets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                assets TEXT UNIQUE
            )
        """)

        # Insert all balances as new rows (no conflict handling for now)
        for balance in balance_data:
            # get local SA time eg 2025-07-05T18:48:49.552722
            utc_time = datetime.now(timezone.utc)
            sa_time = utc_time + timedelta(hours=2)
            timestamp_str = sa_time.isoformat(timespec='microseconds')
            if sa_time.tzinfo:
                timestamp_str = timestamp_str.split('+')[0]

            # Insert balance
            cursor.execute("""
                INSERT INTO balance_history (
                    uid, 
                    account_id, 
                    asset, 
                    balance, 
                    reserved, 
                    unconfirmed, 
                    timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                balance["account_id"],
                balance["asset"],
                balance["balance"],
                balance["reserved"],
                balance["unconfirmed"],
                timestamp_str
            ))
            print(f"✅ Stored history for: {balance['asset']}")

            # Insert asset if it doesn't exist
            cursor.execute("""
                INSERT OR IGNORE INTO assets_list (
                    uid,
                    assets
                )
                VALUES (?, ?)
            """, (
                str(uuid.uuid4()),
                balance["asset"]
            ))

        conn.commit()
    except Exception as e:
        print(f"❌ Error storing balance history: {e}")
    finally:
        conn.close()

# api returns
# {
# 'balance': 
# [{
# 'account_id': '6594336665814305622', 
# 'asset': 'ANKR', 
# 'balance': '38.49635914', 
# 'reserved': '0.00', 
# 'unconfirmed': '0'}, 
# {
# 'account_id': '8075122085411341746', 
# 'asset': 'BCH', 
# 'balance': '0.00009598', 
# 'reserved': '0.00', 
# 'unconfirmed': '0'}, 
# {
# 'account_id': '9119250031648298122', 'asset': 'XBT', 'balance': '0.0000016', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '8186407348185805061', 'asset': 'XBT', 'balance': '0.00', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '4184165031902329194', 'asset': 'DOGE', 'balance': '9.94', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '687412742627896300', 'asset': 'ETH', 'balance': '0.00002046', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '3784206532036387289', 'asset': 'ETH', 'balance': '0.00', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '8772730523187070049', 'asset': 'LINK', 'balance': '0.00', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '4754107407400490211', 'asset': 'LTC', 'balance': '0.00124241', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '2989982922454700085', 'asset': 'MATIC', 'balance': '1.00', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '2347604736617963376', 'asset': 'PYTH', 'balance': '5.11677744', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '5204714511829279333', 'asset': 'SAND', 'balance': '5.65876562', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '3663503223668122216', 'asset': 'UNI', 'balance': '0.00', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '3731946183750833758', 'asset': 'USDC', 'balance': '0.083021', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '4715269767296112715', 'asset': 'USDC', 'balance': '0.00', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '4044512054462273666', 'asset': 'XRP', 'balance': '0.017716', 'reserved': '0.00', 'unconfirmed': '0'}, {'account_id': '7604837217064805551', 'asset': 'ZAR', 'balance': '20.910572', 'reserved': '0.00', 'unconfirmed': '0'}]}

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