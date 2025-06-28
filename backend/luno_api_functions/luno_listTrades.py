



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