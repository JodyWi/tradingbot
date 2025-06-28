# backend/tests/get_trades.py

import os
import base64
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("LUNO_API_KEY_ID")
API_SECRET = os.getenv("LUNO_API_KEY_SECRET")

def get_my_trades(pair="XBTZAR", limit=10):


    url = "https://api.luno.com/api/1/listtrades"
    params = {
        "pair": pair,
        "limit": limit,
        "sort_desc": "true"
    }

    auth = f"{API_KEY}:{API_SECRET}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(auth.encode()).decode()}"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        raw_data = response.json()  # ← raw untouched JSON from Luno
        print("✅ RAW API Response:")
        print(raw_data)
        return {"status": "success", "data": raw_data}
    else:
        print("❌ Error:", response.status_code, response.text)
        return {"status": "error", "message": "API request failed"}


if __name__ == "__main__":

    get_my_trades()
