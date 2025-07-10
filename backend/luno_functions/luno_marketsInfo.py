import os
import sqlite3
import requests
import uuid
from database import financial_db
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def get_markets_info(pair):
    """ List all supported markets parameter information like price scale, min and\nmax order volumes and market ID. """
    if pair is None:
        print("pair is required")
        raise ValueError("pair is required")

    response = requests.get(
        f"{LUNO_API_URL}/api/exchange/1/markets",
        params={"pair": pair},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")
    
    data = response.json()
    # print(data)
    financial_db(data["markets"], pair)
    return {"status": "success"}

def financial_db(market_data, pair):
    """Store the market data in the database"""
    conn = financial_db()
    cursor = conn.cursor()

    try:
        # Create table for market history with auto-increment ID
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                pair TEXT,
                base_currency TEXT,
                counter_currency TEXT,
                fee_scale TEXT,
                market_id TEXT,
                max_price TEXT,
                max_volume TEXT,
                min_price TEXT,
                min_volume TEXT,
                price_scale TEXT,
                trading_status TEXT,
                volume_scale TEXT,
                timestamp TEXT
            )
        """)
        for markets in market_data:
            # get local SA time eg 2025-07-05T18:48:49.552722
            utc_time = datetime.now(timezone.utc)
            sa_time = utc_time + timedelta(hours=2)
            timestamp_str = sa_time.isoformat(timespec='microseconds')
            if sa_time.tzinfo:
                timestamp_str = timestamp_str.split('+')[0]

            # Insert the market data into the database
            cursor.execute("""
                INSERT INTO market_history (
                    uid,
                    pair,
                    base_currency,
                    counter_currency,
                    fee_scale,
                    market_id,
                    max_price,
                    max_volume,
                    min_price,
                    min_volume,
                    price_scale,
                    trading_status,
                    volume_scale,
                    timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                pair,
                markets["base_currency"],
                markets["counter_currency"],
                markets["fee_scale"],
                markets["market_id"],
                markets["max_price"],
                markets["max_volume"],
                markets["min_price"],
                markets["min_volume"],
                markets["price_scale"],
                markets["trading_status"],
                markets["volume_scale"],
                timestamp_str
            ))
        conn.commit()
    except Exception as e:
        print(f"❌ Error storing balance history: {e}")
    finally:
        conn.close()

# # Testing the Api
# if __name__ == "__main__":
#     pair = "XBTZAR"  # Example: Bitcoin/Rand market
#     try:
#         result = get_markets_info(pair)
#         print("✅ Fee info fetched successfully:")
#         print(result)
#     except Exception as e:
#         print(f"❌ Error: {e}")

#  Api Returns 
# {
#   "markets": [
#     {
#       "base_currency": "XBT",
#       "counter_currency": "EUR",
#       "fee_scale": 0,
#       "market_id": "XBTEUR",
#       "max_price": "100000.00",
#       "max_volume": "100.0",
#       "min_price": "100.00",
#       "min_volume": "0.0005",
#       "price_scale": 2,
#       "trading_status": "POST_ONLY",
#       "volume_scale": 4
#     }
#   ]
# }
# "/api/exchange/1/markets": {
#   "get": {
#     "description": "List all supported markets parameter information like price scale, min and\nmax order volumes and market ID.",
#     "tags": [
#       "Market"
#     ],
#     "summary": "Get markets info",
#     "operationId": "Markets",
#     "parameters": [
#       {
#         "example": "XBTZAR",
#         "x-go-name": "Markets",
#         "description": "List of market pairs to return. Requesting only the required pairs will improve response times.",
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
#               "$ref": "#/components/schemas/MarketsInfoResponse"
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