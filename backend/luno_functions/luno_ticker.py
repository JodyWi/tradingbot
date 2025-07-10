import os
import requests
import uuid
from database import financial_db
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def get_ticker(pair):
    """Call Luno API for a single pair"""
    if not pair:
        print("pair is required")
        raise ValueError("pair is required")

    response = requests.get(
        f"{LUNO_API_URL}/api/1/ticker",
        params={"pair": pair},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")
    
    data = response.json()
    # print(data)
    store_db([data])
    return {"status": "success", "pair": data["pair"]}

def get_tickers():
    """Call Luno API for all tickers and store them"""
    response = requests.get(
        f"{LUNO_API_URL}/api/1/tickers",
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")

    data = response.json()
    # print(data)
    store_db(data["tickers"])
    return {"status": "success", "pair": data["tickers"]}

def store_db(ticker_data):
    """Store or update ticker data in the database"""
    conn = financial_db()
    cursor = conn.cursor()

    try:
        # Create tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticker_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                pair TEXT,
                timestamp TEXT,
                raw_timestamp INTEGER,
                bid TEXT,
                ask TEXT,
                last_trade TEXT,
                rolling_24_hour_volume TEXT,
                status TEXT
            )
        """)
        # Create table for Pairs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pairs_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                pairs TEXT UNIQUE
            )
        """)
        
        # Insert into tickers table
        for ticker in ticker_data:
            cursor.execute("""
                INSERT INTO ticker_history (
                    uid,
                    pair,
                    timestamp,
                    raw_timestamp,
                    bid,
                    ask,
                    last_trade,
                    rolling_24_hour_volume,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                ticker["pair"],
                datetime.fromtimestamp(ticker["timestamp"] / 1000).isoformat(),
                ticker["timestamp"],
                ticker["bid"],
                ticker["ask"],
                ticker["last_trade"],
                ticker["rolling_24_hour_volume"],
                ticker["status"]
            ))
            print(f"✅ Stored ticker: {ticker['pair']}")

            # Insert into pairs_list with debug
            cursor.execute("""
                INSERT OR IGNORE INTO pairs_list (
                    uid,
                    pairs
                )
                VALUES (?, ?)
            """, (
                str(uuid.uuid4()),
                ticker["pair"]
            ))

        conn.commit()
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