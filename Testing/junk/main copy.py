import os
import sys
import logging
import requests
from dotenv import load_dotenv
from flask_cors import CORS
from flask import Flask, request, jsonify, send_from_directory

from luno_api_functions.luno_get_balance import get_balance

# Load environment variables
load_dotenv("../.env")
# Check if all required environment variables are set
# This must happen before importing video which uses API keys without checking
# check_env_vars()

API_KEY_ID = os.getenv("LUNO_API_KEY_ID")
API_KEY_SECRET = os.getenv("LUNO_API_KEY_SECRET")

# Initialize Flask
app = Flask(__name__, static_folder='../Frontend')
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'storage')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r"/*": {"origins": "*"}})  # Adjust if needed

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
HOST = "0.0.0.0"
PORT = 8095

# Route to serve the main HTML page
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Route to serve other HTML files
@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(app.static_folder, path)

# # Route to get balance from Luno API
# @app.route("/api/1/balance", methods=["GET"])
# def get_balance_route():
#     try:
#         assets = request.args.getlist('assets')
#         result = get_balance(API_KEY_ID, API_KEY_SECRET, assets)
#         return jsonify(result)
#     except Exception as e:
#         logger.error(f"Error getting balance: {str(e)}")
#         return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
