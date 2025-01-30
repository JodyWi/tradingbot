import websocket
import json
import os

# Define the WebSocket endpoint with the currency pair
pair = "XBTZAR"  # Example currency pair
ws_endpoint = f"wss://ws.luno.com/api/1/stream/{pair}"

# Define your API key credentials
api_key_id = os.getenv("LUNO_API_KEY_ID")
api_key_secret = os.getenv("LUNO_API_KEY_SECRET")

# Define the message to send containing API key credentials
auth_message = {
    "api_key_id": api_key_id,
    "api_key_secret": api_key_secret
}

# Convert the message to JSON format
auth_message_json = json.dumps(auth_message)

# Define the function to execute when a message is received
def on_message(ws, message):
    print("Received message:")
    print(message)

# Define the function to execute when an error occurs
def on_error(ws, error):
    print("Error:")
    print(error)

# Define the function to execute when the WebSocket connection is closed
def on_close(ws):
    print("WebSocket connection closed")

# Define the function to execute when the WebSocket connection is opened
def on_open(ws):
    print("WebSocket connection opened")
    # Send the authentication message
    ws.send(auth_message_json)

# Create a WebSocket connection
ws = websocket.WebSocketApp(ws_endpoint,
                             on_message=on_message,
                             on_error=on_error,
                             on_close=on_close,
                             on_open=on_open)

# Run the WebSocket connection
ws.run_forever()
