# tradingbot/backend/luno_api_functions/luno_tickers.py

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

def update_tickers():
    """Call Luno API for all tickers and store them"""
    response = requests.get(
        f"{LUNO_API_URL}/api/1/tickers",
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")

    data = response.json()
    store_db(data["tickers"])
    return {"status": "success", "count": len(data["tickers"])}

def store_db(tickers):
    """Store all ticker data as history (no overwrite)"""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Create table for ticker history with auto-increment ID
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticker_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT,
                timestamp INTEGER,
                bid TEXT,
                ask TEXT,
                last_trade TEXT,
                volume TEXT,
                status TEXT
            )
        """)

        # Insert all tickers as new rows (no conflict handling)
        for ticker in tickers:
            cursor.execute("""
                INSERT INTO ticker_history (pair, timestamp, bid, ask, last_trade, volume, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                ticker["pair"],
                ticker["timestamp"],
                ticker["bid"],
                ticker["ask"],
                ticker["last_trade"],
                ticker["rolling_24_hour_volume"],
                ticker["status"]
            ))
            print(f"✅ Stored history for: {ticker['pair']}")

        conn.commit()
    except Exception as e:
        print(f"❌ Error storing ticker history: {e}")
    finally:
        conn.close()


# "/api/1/tickers": {
#   "get": {
#     "description": "Returns the latest ticker indicators from all active Luno exchanges.\n\nPlease see the <a href=\"#tag/currency \">Currency list</a> for the complete list of supported currency pairs.",
#     "tags": [
#       "Market"
#     ],
#     "summary": "List tickers for all currency pairs",
#     "operationId": "GetTickers",
#     "parameters": [
#       {
#         "example": "XBTZAR",
#         "x-go-name": "Pair",
#         "description": "Return tickers for multiple markets (if not provided, all tickers will be returned).\nTo request tickers for multiple markets, pass the parameter multiple times,\ne.g. `pair=XBTZAR&pair=ETHZAR`.",
#         "name": "pair",
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
#               "$ref": "#/components/schemas/ListTickersResponse"
#             }
#           }
#         }
#       },
#       "default": {
#         "$ref": "#/components/responses/apiError"
#       }
#     }
#   }
# },