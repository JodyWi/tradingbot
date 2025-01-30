import os
import sys

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import core functionality
from .database import connect_db, create_tables
from .config import load_env
from .luno_api_functions import (
    get_balance,
    # get_addresses,
    # get_transactions,
    # get_fee_info,
)

# Expose these modules when `backend` is imported
__all__ = ["connect_db", "create_tables", "load_env", "get_balance"]
