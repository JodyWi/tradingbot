import os
import requests
import uuid
from datetime import datetime

from dotenv import load_dotenv
from database.mongo import insert_many, upsert_unique

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
    """Store ticker snapshots in Mongo."""
    docs = []
    for ticker in ticker_data:
        docs.append({
            "uid": str(uuid.uuid4()),
            "pair": ticker["pair"],
            "timestamp": datetime.fromtimestamp(ticker["timestamp"] / 1000).isoformat(),
            "raw_timestamp": ticker["timestamp"],
            "bid": ticker["bid"],
            "ask": ticker["ask"],
            "last_trade": ticker["last_trade"],
            "rolling_24_hour_volume": ticker["rolling_24_hour_volume"],
            "status": ticker["status"],
        })
        upsert_unique("pairs_list", "pairs", ticker["pair"], {
            "uid": str(uuid.uuid4()),
            "pairs": ticker["pair"],
        })
        print(f"✅ Stored ticker: {ticker['pair']}")
    insert_many("ticker_history", docs)


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
