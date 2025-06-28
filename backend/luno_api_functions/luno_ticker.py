# Luno API balance endpoint | tradingbot/Backend/luno_api_functions/luno_py
# luno_get_ticker.py

import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from database import connect_db

app = Flask(__name__)

load_dotenv()

LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


@app.route("/api/1/ticker", methods=["GET"])
def get_ticker():
    pair = request.args.get('pair')
    if not pair:
        return jsonify({"error": "pair is required"}), 400

    response = requests.get(
        f"{LUNO_API_URL}/api/1/ticker",
        params={"pair": pair},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code


    # {
    #   "pair": "AAVEMYR",
    #   "timestamp": 1750881878718,
    #   "bid": "1093.87",
    #   "ask": "1103.40",
    #   "last_trade": "1096.67",
    #   "rolling_24_hour_volume": "395.3898",
    #   "status": "ACTIVE"
    # },
# the db need to store something like this
def store_db(ticker_data):
    """Store or update ticker data in the database safely"""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickers (
                pair TEXT PRIMARY KEY,
                timestamp INTEGER,
                bid TEXT,
                ask TEXT,
                last_trade TEXT,
                volume TEXT,
                status TEXT
            )
        """)

        cursor.execute("""
            INSERT INTO tickers (pair, timestamp, bid, ask, last_trade, volume, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(pair) DO UPDATE SET
                timestamp=excluded.timestamp,
                bid=excluded.bid,
                ask=excluded.ask,
                last_trade=excluded.last_trade,
                volume=excluded.volume,
                status=excluded.status
        """, (
            ticker_data["pair"],
            ticker_data["timestamp"],
            ticker_data["bid"],
            ticker_data["ask"],
            ticker_data["last_trade"],
            ticker_data["rolling_24_hour_volume"],
            ticker_data["status"]
        ))

        conn.commit()
        print(f"✅ Stored ticker: {ticker_data['pair']}")
    except Exception as e:
        print(f"❌ Error storing ticker: {e}")
    finally:
        conn.close()



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