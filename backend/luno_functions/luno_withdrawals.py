# Luno API balance endpoint | tradingbot/Backend/luno_api_functions/luno_py

import os
from flask import request, jsonify
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Luno API base URL
LUNO_API_URL = os.getenv("LUNO_API_URL")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Check for required environment variables
if not all([LUNO_API_URL, API_KEY, API_SECRET]):
    logger.error("Missing required Luno API environment variables.")
    raise EnvironmentError("API credentials or URL are not set in the environment.")

# API route function for Luno 

@app.route("/api/1/withdrawal", methods=["POST"])
def create_withdrawal():
    data = request.json
    amount = data.get('amount')
    currency = data.get('currency')
    address = data.get('address')

    if not all([amount, currency, address]):
        return jsonify({"error": "amount, currency, and address are required"}), 400

    response = requests.post(
        f"{LUNO_API_URL}/api/1/withdrawal",
        json={"amount": amount, "currency": currency, "address": address},
        auth=(API_KEY, API_SECRET)
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text}), response.status_code
    


# "/api/1/withdrawals": {
#   "get": {
#     "description": "Returns a list of withdrawal requests.\n\nPermissions required: <code>Perm_R_Withdrawals</code>",
#     "tags": [
#       "Transfers"
#     ],
#     "summary": "List withdrawal requests",
#     "operationId": "ListWithdrawals",
#     "parameters": [
#       {
#         "example": 12345,
#         "x-go-name": "BeforeID",
#         "description": "Filter to withdrawals requested on or before the withdrawal with this ID.\nCan be used for pagination.",
#         "name": "before_id",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       },
#       {
#         "example": 986,
#         "x-go-name": "Limit",
#         "description": "Limit to this many withdrawals",
#         "name": "limit",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64",
#           "minimum": 1,
#           "maximum": 1000,
#           "default": 100
#         }
#       }
#     ],
#     "responses": {
#       "200": {
#         "description": "OK",
#         "content": {
#           "application/json": {
#             "schema": {
#               "$ref": "#/components/schemas/ListWithdrawalsResponse"
#             }
#           }
#         }
#       }
#     }
#   },
#   "post": {
#     "description": "Creates a new withdrawal request to the specified beneficiary.\n\nPermissions required: <code>Perm_W_Withdrawals</code>",
#     "tags": [
#       "Transfers"
#     ],
#     "summary": "Request a withdrawal",
#     "operationId": "CreateWithdrawal",
#     "parameters": [
#       {
#         "example": "ZAR_EFT",
#         "x-go-name": "Type",
#         "description": "Withdrawal method.",
#         "name": "type",
#         "in": "query",
#         "required": true,
#         "schema": {
#           "type": "string"
#         }
#       },
#       {
#         "example": "10000.00",
#         "x-go-name": "Amount",
#         "description": "Amount to withdraw. The currency withdrawn depends on the type setting.",
#         "name": "amount",
#         "in": "query",
#         "required": true,
#         "schema": {
#           "type": "string",
#           "format": "amount"
#         }
#       },
#       {
#         "example": 12345,
#         "x-go-name": "BeneficiaryID",
#         "description": "The beneficiary ID of the bank account the withdrawal will be paid out to.\nThis parameter is required if the user has set up multiple beneficiaries.\nThe beneficiary ID can be found by selecting on the beneficiary name on the user’s <a href=\"/wallet/beneficiaries\">Beneficiaries</a> page.",
#         "name": "beneficiary_id",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       },
#       {
#         "example": true,
#         "x-go-name": "Fast",
#         "description": "If true, it will be a fast withdrawal if possible. Fast withdrawals come with a fee.\nCurrently fast withdrawals are only available for `type=ZAR_EFT`; for other types, an error is returned.\nFast withdrawals are not possible for Bank of Baroda, Deutsche Bank, Merrill Lynch South Africa, UBS, Postbank and Tyme Bank.\nThe fee to be charged is the same as when withdrawing from the UI.",
#         "name": "fast",
#         "in": "query",
#         "schema": {
#           "type": "boolean",
#           "default": false
#         }
#       },
#       {
#         "x-go-name": "Reference",
#         "description": "For internal use.\nDeprecated: We don't allow custom references and will remove this soon.",
#         "name": "reference",
#         "in": "query",
#         "schema": {
#           "type": "string"
#         }
#       },
#       {
#         "example": "123e4567-e89b-12d3-a456-426655440000",
#         "x-go-name": "ExternalID",
#         "description": "Optional unique ID to associate with this withdrawal.\nUseful to prevent duplicate sends.\nThis field supports all alphanumeric characters including \"-\" and \"_\".",
#         "name": "external_id",
#         "in": "query",
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
#               "$ref": "#/components/schemas/CreateWithdrawalResponse"
#             }
#           }
#         }
#       }
#     }
#   }
# },
# "/api/1/withdrawals/{id}": {
#   "get": {
#     "description": "Returns the status of a particular withdrawal request.\n\nPermissions required: <code>Perm_R_Withdrawals</code>",
#     "tags": [
#       "Transfers"
#     ],
#     "summary": "Get withdrawal request",
#     "operationId": "GetWithdrawal",
#     "parameters": [
#       {
#         "example": 12345,
#         "x-go-name": "ID",
#         "description": "Withdrawal ID to retrieve.",
#         "name": "id",
#         "in": "path",
#         "required": true,
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       }
#     ],
#     "responses": {
#       "200": {
#         "description": "OK",
#         "content": {
#           "application/json": {
#             "schema": {
#               "$ref": "#/components/schemas/GetWithdrawalResponse"
#             }
#           }
#         }
#       }
#     }
#   },
#   "delete": {
#     "description": "Cancels a withdrawal request.\nThis can only be done if the request is still in state <code>PENDING</code>.\n\nPermissions required: <code>Perm_W_Withdrawals</code>",
#     "tags": [
#       "Transfers"
#     ],
#     "summary": "Cancel withdrawal request",
#     "operationId": "CancelWithdrawal",
#     "parameters": [
#       {
#         "example": 12345,
#         "x-go-name": "ID",
#         "description": "ID of the withdrawal to cancel.",
#         "name": "id",
#         "in": "path",
#         "required": true,
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       }
#     ],
#     "responses": {
#       "200": {
#         "description": "OK",
#         "content": {
#           "application/json": {
#             "schema": {
#               "$ref": "#/components/schemas/CancelWithdrawalResponse"
#             }
#           }
#         }
#       }
#     }
#   }
# },