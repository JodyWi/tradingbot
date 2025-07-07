

# "/api/1/marketorder": {
#   "post": {
#     "description": "A Market Order executes immediately, and either buys as much of the asset that can be bought for a set amount of fiat currency, or sells a set amount of the asset for as much as possible.\n\n<b>Warning!</b> Orders cannot be reversed once they have executed.\nPlease ensure your program has been thoroughly tested before submitting Orders.\n\nIf no <code>base_account_id</code> or <code>counter_account_id</code> are specified, the default base currency or counter currency account will be used.\nUsers can find their account IDs by calling the <a href=\"#operation/getBalances\">Balances</a> request.\n\nPermissions required: <code>Perm_W_Orders</code>",
#     "tags": [
#       "Orders"
#     ],
#     "summary": "Post Market Order",
#     "operationId": "PostMarketOrder",
#     "parameters": [
#       {
#         "example": "XBTZAR",
#         "x-go-name": "Pair",
#         "description": "The currency pair to trade.",
#         "name": "pair",
#         "in": "query",
#         "required": true,
#         "schema": {
#           "type": "string"
#         }
#       },
#       {
#         "example": "BUY",
#         "x-go-name": "OrderType",
#         "description": "<code>BUY</code> to buy an asset<br>\n<code>SELL</code> to sell an asset",
#         "name": "type",
#         "in": "query",
#         "required": true,
#         "schema": {
#           "type": "string",
#           "enum": [
#             "BUY",
#             "SELL"
#           ]
#         }
#       },
#       {
#         "example": "100.50",
#         "x-go-name": "CounterVolume",
#         "description": "For a <code>BUY</code> order: amount of the counter currency to use (e.g. how much EUR to use to buy BTC in the BTC/EUR market)",
#         "name": "counter_volume",
#         "in": "query",
#         "schema": {
#           "type": "string",
#           "format": "amount"
#         }
#       },
#       {
#         "example": "1.423",
#         "x-go-name": "BaseVolume",
#         "description": "For a <code>SELL</code> order: amount of the base currency to use (e.g. how much BTC to sell for EUR in the BTC/EUR market)",
#         "name": "base_volume",
#         "in": "query",
#         "schema": {
#           "type": "string",
#           "format": "amount"
#         }
#       },
#       {
#         "example": 12345,
#         "x-go-name": "BaseAccountID",
#         "description": "The base currency account to use in the trade.",
#         "name": "base_account_id",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       },
#       {
#         "example": 12345,
#         "x-go-name": "CounterAccountID",
#         "description": "The counter currency account to use in the trade.",
#         "name": "counter_account_id",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       },
#       {
#         "x-go-name": "Timestamp",
#         "description": "Unix timestamp in milliseconds of when the request was created and sent.",
#         "name": "timestamp",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64"
#         }
#       },
#       {
#         "example": 5000,
#         "x-go-name": "TTL",
#         "description": "Specifies the number of milliseconds after timestamp the request is valid for.\nIf `timestamp` is not specified, `ttl` will not be used.",
#         "name": "ttl",
#         "in": "query",
#         "schema": {
#           "type": "integer",
#           "format": "int64",
#           "minimum": 1,
#           "maximum": 10000,
#           "default": 10000
#         }
#       },
#       {
#         "example": "mkt-53960812",
#         "x-go-name": "ClientOrderID",
#         "description": "Client order ID.\nMay only contain alphanumeric (0-9, a-z, or A-Z) and special characters (_ ; , . -). Maximum length: 255.\nIt will be available in read endpoints, so you can use it to reconcile Luno with your internal system.\nValues must be unique across all your successful order creation endpoint calls; trying to create an order\nwith the same `client_order_id` as one of your past orders will result in a HTTP 409 Conflict response.",
#         "name": "client_order_id",
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
#               "$ref": "#/components/schemas/PostMarketOrderResponse"
#             }
#           }
#         }
#       }
#     }
#   }
# },