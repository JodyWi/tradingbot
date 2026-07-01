# backend/tests/tickers.py

import requests
import json
from datetime import datetime

def get_all_pairs_and_save():
    url = "https://api.luno.com/api/1/tickers"
    response = requests.get(url)

    if response.status_code == 200:
        raw_data = response.json()

        output = {
            "fetched_at": datetime.utcnow().isoformat() + "Z",
            "tickers": raw_data.get("tickers", [])
        }

        with open("tickers.json", "w") as f:
            json.dump(output, f, indent=2)

        print(f"✅ Saved to tickers.json in current folder ({len(output['tickers'])} tickers)")
    else:
        print("❌ Error:", response.status_code, response.text)

if __name__ == "__main__":
    get_all_pairs_and_save()

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