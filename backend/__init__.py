# backend/__init__.py
import os
import sys

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import important modules for easier access
from .database import connect_db, create_tables
from .luno_api_functions.luno_get_balance import get_balance
