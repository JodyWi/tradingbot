import os
import requests
import uuid
from database import financial_db
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def get_fee_info(pair):
    """Returns the fees and 30 day trading volume (as of midnight) for a given currency pair"""

    if pair is None:
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
    """Store fee data in the database"""
    conn = financial_db()
    cursor = conn.cursor()

    try:
        # Create table for fee history with auto-increment ID
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fee_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                pair TEXT,
                maker_fee TEXT,
                taker_fee TEXT,
                thirty_day_volume TEXT,
                timestamp TEXT
            )
        """)

        for fee in fee_data:
            # get local SA time
            utc_time = datetime.now(timezone.utc)
            sa_time = utc_time + timedelta(hours=2)
            timestamp_str = sa_time.isoformat(timespec='microseconds')
            if sa_time.tzinfo:
                timestamp_str = timestamp_str.split('+')[0]

            # Insert the fee data into the database
            cursor.execute("""
                INSERT INTO fee_history (
                    uid,
                    pair, 
                    maker_fee, 
                    taker_fee, 
                    thirty_day_volume,
                    timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),
                pair,
                fee["maker_fee"],
                fee["taker_fee"],
                fee["thirty_day_volume"],
                timestamp_str
            ))

        conn.commit()
    except Exception as e:
        print(f"❌ Error storing trade history: {e}")
    finally:
        conn.close()

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