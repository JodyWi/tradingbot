# tradingbot/backend/luno_api_functions/luno_ticker.py
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


def get_ticker(pair):
    """Call Luno API for a single pair"""
    if not pair:
        raise ValueError("pair is required")

    response = requests.get(
        f"{LUNO_API_URL}/api/1/ticker",
        params={"pair": pair},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code == 200:
        data = response.json()
        store_db(data)
        return data
    else:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")


def store_db(ticker_data):
    """Store or update ticker data in the database"""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickers (
                pair TEXT PRIMARY KEY,
                timestamp INTEGER,
                bid TEXT,
                ask TEXT,
                last_trade TEXT,
                volume TEXT,
                status TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO tickers (pair, timestamp, bid, ask, last_trade, volume, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(pair) DO UPDATE SET
                timestamp=excluded.timestamp,
                bid=excluded.bid,
                ask=excluded.ask,
                last_trade=excluded.last_trade,
                volume=excluded.volume,
                status=excluded.status
        """, (
            ticker_data["pair"],
            ticker_data["timestamp"],
            ticker_data["bid"],
            ticker_data["ask"],
            ticker_data["last_trade"],
            ticker_data["rolling_24_hour_volume"],
            ticker_data["status"]
        ))

        conn.commit()
        print(f"✅ Stored ticker: {ticker_data['pair']}")
    except Exception as e:
        print(f"❌ Error storing ticker: {e}")
    finally:
        conn.close()

# "/api/1/ticker": {
#   "get": {
#     "description": "Returns the latest ticker indicators for the specified currency pair.\n\nPlease see the <a href=\"#tag/currency \">Currency list</a> for the complete list of supported currency pairs.",
#     "tags": [
#       "Market"
#     ],
#     "summary": "Get ticker for currency pair",
#     "operationId": "GetTicker",
#     "parameters": [
#       {
#         "example": "XBTZAR",
#         "x-go-name": "Pair",
#         "description": "Currency pair",
#         "name": "pair",
#         "in": "query",
#         "required": true,
#         "schema": {
#           "type": "string"
#         }
#       }
#     ],
#     "responses": {
#       "200": {
#         "description": "OK",
#         "content": {
#           "application/json": {
#             "schema": {
#               "$ref": "#/components/schemas/GetTickerResponse"
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