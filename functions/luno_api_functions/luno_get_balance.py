import httpx
import json


def get_balance(assets):
    url = "https://api.luno.com/api/v1/balances"    

    if assets:
        url = url + "?asset=" + assets

    response = httpx.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None















if __name__ == "__main__":
    print(get_balance(""))

