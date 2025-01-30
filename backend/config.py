import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Read API keys from environment variables
LUNO_API_KEY = os.getenv("LUNO_API_KEY")
LUNO_API_SECRET = os.getenv("LUNO_API_SECRET")

# Check if keys are loaded (optional: remove this in production)
if not LUNO_API_KEY or not LUNO_API_SECRET:
    raise ValueError("❌ API Keys not found! Check your .env file.")

print("✅ API keys loaded successfully.")
