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

# #############################
# # Get Fees Api's in the server.py
# #############################
# from luno_functions.luno_feeInfo import get_fee_info
# # curl -X POST http://localhost:8001/api/1/fee_info
# # curl -X POST "http://localhost:8001/api/1/fee_info?pair=LTCZAR"
# @app.route("/api/1/fee_info", methods=["POST"])
# def get_fee_info_api():
#     try:
#         pair = request.args.get("pair", default="LTCZAR")
#         result = get_fee_info(pair=pair)
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    



def get_fee_info(pair):
    """Returns the fees and 30 day trading volume (as of midnight) for a given currency pair"""

    if not pair:
        print("pair is required")
        raise ValueError("pair is required")
    
    response = requests.get(
        f"{LUNO_API_URL}/api/1/fee_info",
        params={"pair": pair},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")
    
    data = response.json()
    # print(data)
    store_db([data], pair)
    return {"status": "success"}

def store_db(fee_data, pair):
    """Store fee snapshots in Mongo."""
    utc_time = datetime.now(timezone.utc)
    sa_time = utc_time + timedelta(hours=2)
    timestamp_str = sa_time.isoformat(timespec='microseconds').split('+')[0]
    docs = [{
        "uid": str(uuid.uuid4()),
        "pair": pair,
        "maker_fee": fee["maker_fee"],
        "taker_fee": fee["taker_fee"],
        "thirty_day_volume": fee["thirty_day_volume"],
        "timestamp": timestamp_str,
    } for fee in fee_data]
    insert_many("fee_history", docs)

# Testing the Api
# if __name__ == "__main__":
#     pair = "XBTZAR"  # Example: Bitcoin/Rand market
#     try:
#         result = get_fee_info(pair)
#         print("✅ Fee info fetched successfully:")
#         print(result)
#     except Exception as e:
#         print(f"❌ Error: {e}")


# Api Returns
# {
#   "maker_fee": "string",
#   "taker_fee": "string",
#   "thirty_day_volume": "string"
# }

# "/api/1/fee_info": {
#   "get": {
#     "description": "Returns the fees and 30 day trading volume (as of midnight) for a given currency pair.  For complete details, please see <a href=\"en/countries\">Fees & Features</a>.\n\nPermissions required: <code>Perm_R_Orders</code>",
#     "tags": [
#       "Orders"
#     ],
#     "summary": "Get fee information",
#     "operationId": "getFeeInfo",
#     "parameters": [
#       {
#         "example": "XBTZAR",
#         "x-go-name": "Pair",
#         "description": "Get fee information about this pair.",
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
#               "$ref": "#/components/schemas/getFeeInfoResponse"
#             }
#           }
#         }
#       }
#     }
#   }
# },
