#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
import requests


def pick_credentials() -> tuple[str, str, str]:
    api_url = os.getenv("LUNO_API_URL", "").strip()
    api_key = os.getenv("API_KEY", "").strip()
    api_secret = os.getenv("API_SECRET", "").strip()
    if api_url and api_key and api_secret:
        return api_url, api_key, api_secret

    alt_key = os.getenv("LUNO_API_KEY_ID", "").strip()
    alt_secret = os.getenv("LUNO_API_KEY_SECRET", "").strip()
    if api_url and alt_key and alt_secret:
        return api_url, alt_key, alt_secret

    return api_url, "", ""


def main() -> int:
    load_dotenv()

    api_url, api_key, api_secret = pick_credentials()
    if not api_url or not api_key or not api_secret:
        print("configured=false connected=false")
        print("message=Luno API credentials are missing.")
        print(f"api_url={api_url or 'missing'}")
        return 1

    try:
        response = requests.get(
            f"{api_url}/api/1/tickers",
            auth=(api_key, api_secret),
            timeout=3,
        )
        connected = response.ok
        print(f"configured=true connected={str(connected).lower()}")
        print(f"status_code={response.status_code}")
        print(
            "message="
            + (
                "Luno API is connected."
                if connected
                else f"Luno API returned {response.status_code}."
            )
        )
        return 0 if connected else 2
    except requests.RequestException as exc:
        print("configured=true connected=false")
        print(f"message=Luno API check failed: {exc.__class__.__name__}")
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
