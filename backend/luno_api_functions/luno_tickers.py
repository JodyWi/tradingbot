

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