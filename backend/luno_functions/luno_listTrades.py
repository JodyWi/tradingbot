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

# def get_trades(pair="DOGEZAR", since=None, before=None, after_seq=None, before_seq=None, sort_desc=False, limit=100):
def get_trade(pair):
    """Call Luno API for trades for a given pair"""
    if not pair:
        print("pair is required")
        raise ValueError("pair is required")

    response = requests.get(
        f"{LUNO_API_URL}/api/1/listtrades",
        params={"pair": pair},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code != 200:
        raise Exception(f"Luno API error: {response.status_code} {response.text}")

    data = response.json()
    # print(data)
    store_db(data["trades"])
    return {"status": "success", "count": len(data["trades"])}

def store_db(trade_data):
    """Store all trade data as history (no overwrite)"""
    conn = financial_db()
    cursor = conn.cursor()

    try:
        # Create table for trade history with auto-increment ID
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE,
                pair TEXT,
                sequence TEXT,
                order_id TEXT,
                type TEXT,
                price TEXT,
                timestamp TEXT,
                raw_timestamp INTEGER,
                volume TEXT,
                base TEXT,
                counter TEXT,
                fee_base TEXT,
                fee_counter TEXT,
                is_buy BOOLEAN,
                client_order_id TEXT
            )
        """)

        # Insert all trades as new rows (no conflict handling for now)
        for trade in trade_data:
            cursor.execute("""
                INSERT INTO trade_history (
                    uid, 
                    pair, 
                    sequence, 
                    order_id, 
                    type, 
                    price, 
                    timestamp,
                    raw_timestamp, 
                    volume,
                    base, 
                    counter, 
                    fee_base, 
                    fee_counter, 
                    is_buy,
                    client_order_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()),  # unique ID for each record
                trade["pair"],
                trade["sequence"],
                trade["order_id"],
                trade["type"],
                trade["price"],
                datetime.fromtimestamp(trade["timestamp"] / 1000).isoformat(),
                trade["timestamp"],
                trade["volume"],
                trade["base"],
                trade["counter"],
                trade["fee_base"],
                trade["fee_counter"],
                trade["is_buy"],
                trade["client_order_id"]

            ))
            print(f"✅ Stored history for: {trade['pair']}")

        conn.commit()
    except Exception as e:
        print(f"❌ Error storing trade history: {e}")
    finally:
        conn.close()

# Api returns
# {
#   'trades': [
#   { 
#     'pair': 'XBTZAR', 
#     'sequence': 20978178, 
#     'order_id': 'BXX678PNCWFSQ4', 
#     'type': 'ASK', 
#     'timestamp': 1659118430072, 
#     'price': '406347.000000000000000000', 
#     'volume': '0.000698000000000000', 
#     'base': '0.000698000000000000', 
#     'counter': '283.630206000000000000', 
#     'fee_base': '0.000000690000000000', 
#     'fee_counter': '0.000000000000000000', 
#     'is_buy': False, 
#     'client_order_id': ''
#   }, 
#     
#   {
#     'pair': 'XBTZAR', 
#     'sequence': 20978211, 
#     'order_id': 'BXMM3M72QGDXH9N', 
#     'type': 'BID', 
#     'timestamp': 1659118561650, 
#     'price': '406022.000000000000000000', 
#     'volume': '0.000697000000000000', 
#     'base': '0.000697000000000000', 
#     'counter': '282.997334000000000000', 
#     'fee_base': '0.000000690000000000', 
#     'fee_counter': '0.000000000000000000', 
#     'is_buy': True, 
#     'client_order_id': ''
#   }
#  ]
# }
# "/api/1/listtrades": {
#   "get": {
#     "description": "Returns a list of the recent Trades for a given currency pair for this user, sorted by oldest first.\nIf <code>before</code> is specified, then Trades are returned sorted by most-recent first.\n\n<code>type</code> in the response indicates the type of Order that was placed to participate in the trade.\nPossible types: <code>BID</code>, <code>ASK</code>.\n\nIf <code>is_buy</code> in the response is true, then the Order which completed the trade (market taker) was a Bid Order.\n\nResults of this query may lag behind the latest data.\n\nPermissions required: <code>Perm_R_Orders</code>",
#     "tags": [
#       "Orders"
#     ],
#     "summary": "List trades",
#     "operationId": "ListUserTrades",
#     "parameters": [
#       {
#         "example": "XBTZAR",
#         "x-go-name": "Pair",
#         "description": "Filter to trades of this currency pair.",
#         "name": "pair",
#         "in": "query",
#         "required": true,
#         "schema": {
#           "type": "string"
#         }
#       },
#       {
#         "x-go-name": "Since",
#         "description": "Filter to trades on or after this timestamp (Unix milliseconds).",
#         "name": "since",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "timestamp"
#         }
#       },
#       {
#         "x-go-name": "Before",
#         "description": "Filter to trades before this timestamp (Unix milliseconds).",
#         "name": "before",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "timestamp"
#         }
#       },
#       {
#         "example": 10,
#         "x-go-name": "AfterSeq",
#         "description": "Filter to trades from (including) this sequence number.\nDefault behaviour is not to include this filter.",
#         "name": "after_seq",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       },
#       {
#         "example": 1,
#         "x-go-name": "BeforeSeq",
#         "description": "Filter to trades before (excluding) this sequence number.\nDefault behaviour is not to include this filter.",
#         "name": "before_seq",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       },
#       {
#         "example": true,
#         "x-go-name": "SortDesc",
#         "description": "If set to true, sorts trades in descending order, otherwise ascending\norder will be assumed.",
#         "name": "sort_desc",
#         "in": "query",
#         "schema": {
#           "type": "boolean"
#         }
#       },
#       {
#         "example": 100,
#         "x-go-name": "Limit",
#         "description": "Limit to this number of trades (default 100).",
#         "name": "limit",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64",
#           "minimum": 1,
#           "maximum": 1000
#         }
#       }
#     ],
#     "responses": {
#       "200": {
#         "description": "OK",
#         "content": {
#           "application/json": {
#             "schema": {
#               "$ref": "#/components/schemas/ListUserTradesResponse"
#             }
#           }
#         }
#       }
#     }
#   }
# },