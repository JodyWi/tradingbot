import os
import requests
import uuid
import time
from database import financial_db
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def get_candles(pair, duration, since): 
    """Get candles from Luno API"""
    response = requests.get(
        f"{LUNO_API_URL}/api/exchange/1/candles",
        params={
            "pair": pair,
            "duration": duration,
            "since": since
            },
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")

    data = response.json()
    # print(data)
    # financial_db(data["candles"])
    return data["candles"]
    # return {"status": "success", "count": len(data["candles"])}


if __name__ == "__main__":
    pair = "XBTZAR"
    duration = 60  # 5-min candles

    now_ms = int(time.time() * 1000)
    since_24h = now_ms - (24 * 60 * 60 * 1000)  # Last 24h
    since_1h = now_ms - (1 * 60 * 60 * 1000)

    print(since_1h)

    try:
        candles = get_candles(pair, duration, since_1h)
        print(candles)
        # for candle in candles[:5]:  # show first 5 for sanity check
        #     print(candle)
    except Exception as e:
        print(f"❌ Error: {e}")


# Testing the Api
# if __name__ == "__main__":
#     pair = "XBTZAR"  # Example: Bitcoin/Rand market
#     try:
#         result = get_fee_info(pair)
#         print("✅ Fee info fetched successfully:")
#         print(result)
#     except Exception as e:
#         print(f"❌ Error: {e}")

# {
#   "candles": [
#     {
#       "close": "string",
#       "high": "string",
#       "low": "string",
#       "open": "string",
#       "timestamp": 0,
#       "volume": "string"
#     }
#   ],
#   "duration": 0,
#   "pair": "string"
# }