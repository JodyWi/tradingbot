# tests/luno_get_balance.py

import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# def get_balance(assets=""):
#     LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"
#     if assets:
#         LUNO_API_ENDPOINT += f"?assets={assets}"

#     if not API_KEY_ID or not API_KEY_SECRET:
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
#             results.append({
#                 "Asset": asset,
#                 "Balance": float(value) if value.replace('.', '', 1).isdigit() else 0.0
#             })
#         print("✅ Balances:", results)
#         return {"status": "success", "balances": results}
#     else:
#         print("❌ API error:", response.text)
#         return {"status": "error", "message": "API request failed"}


def get_balance(assets=""):
    LUNO_API_ENDPOINT = "https://api.luno.com/api/1/balance"
    if assets:
        LUNO_API_ENDPOINT += f"?assets={assets}"

    if not API_KEY_ID or not API_KEY_SECRET:
        return {"status": "error", "message": "Missing API credentials"}

    credentials = f"{API_KEY_ID}:{API_KEY_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = requests.get(LUNO_API_ENDPOINT, headers=headers)

    if response.status_code == 200:
        raw_data = response.json()  # ← raw untouched JSON from Luno
        print("✅ RAW API Response:")
        print(raw_data)
        return {"status": "success", "data": raw_data}
    else:
        print("❌ Error:", response.text)
        return {"status": "error", "message": "API request failed"}


# 👇 Call the function only if this is the main script
if __name__ == "__main__":
    get_balance()
