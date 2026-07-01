# luno_api_wrapper.py

# In luno_api_wrapper.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'luno_api_functions')))

from luno_api_functions.luno_get_balance import get_balance  # or whatever functions you need
from luno_api_functions.luno_get_transactions import get_transactions
from luno_api_functions.luno_place_order import place_order
def get_balance_wrapper(api_url, api_key, api_secret, assets=None):
    return get_balance(api_url, api_key, api_secret, assets)

def get_transactions_wrapper(api_url, api_key, api_secret, params):
    return get_transactions(api_url, api_key, api_secret, params)

def place_order_wrapper(api_url, api_key, api_secret, order_data):
    return place_order(api_url, api_key, api_secret, order_data)
