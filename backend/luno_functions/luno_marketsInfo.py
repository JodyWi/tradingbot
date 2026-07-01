import os
import requests
import uuid
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from database.mongo import insert_many

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def get_markets_info(pair):
    """ List all supported markets parameter information like price scale, min and\nmax order volumes and market ID. """
    if not pair:
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
    store_db(data["markets"], pair)
    return {"status": "success"}

def store_db(market_data, pair):
    """Store market snapshots in Mongo."""
    utc_time = datetime.now(timezone.utc)
    sa_time = utc_time + timedelta(hours=2)
    timestamp_str = sa_time.isoformat(timespec='microseconds').split('+')[0]
    docs = []
    for markets in market_data:
        docs.append({
            "uid": str(uuid.uuid4()),
            "pair": pair,
            "base_currency": markets["base_currency"],
            "counter_currency": markets["counter_currency"],
            "fee_scale": markets["fee_scale"],
            "market_id": markets["market_id"],
            "max_price": markets["max_price"],
            "max_volume": markets["max_volume"],
            "min_price": markets["min_price"],
            "min_volume": markets["min_volume"],
            "price_scale": markets["price_scale"],
            "trading_status": markets["trading_status"],
            "volume_scale": markets["volume_scale"],
            "timestamp": timestamp_str,
        })
    insert_many("market_history", docs)

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
