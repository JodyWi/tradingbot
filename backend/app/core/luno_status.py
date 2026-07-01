import os
from requests import get, RequestException

from dotenv import load_dotenv

load_dotenv()


def get_luno_status():
    api_url = os.getenv("LUNO_API_URL", "").strip()
    api_key = os.getenv("API_KEY", "").strip() or os.getenv("LUNO_API_KEY_ID", "").strip()
    api_secret = os.getenv("API_SECRET", "").strip() or os.getenv("LUNO_API_KEY_SECRET", "").strip()
    configured = bool(api_url and api_key and api_secret)
    connected = False
    message = "Luno API credentials are missing."

    if configured:
        try:
            response = get(
                f"{api_url}/api/1/tickers",
                auth=(api_key, api_secret),
                timeout=3,
            )
            connected = response.ok
            message = "Luno API is connected." if connected else f"Luno API returned {response.status_code}."
        except RequestException as exc:
            message = f"Luno API check failed: {exc.__class__.__name__}"

    return {
        "configured": configured,
        "connected": connected,
        "apiUrl": api_url,
        "message": message,
    }
