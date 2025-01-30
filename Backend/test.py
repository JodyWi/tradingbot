from dotenv import load_dotenv
import os
import requests

# load_dotenv()  # Load from .env file

# API_KEY = os.getenv('API_KEY')
# API_SECRET = os.getenv('API_SECRET')


# Luno API base URL
LUNO_API_URL = "https://api.luno.com/api/1/"
API_KEY = "h93eqa9ztt8ug"
API_SECRET = "NxUDUIWlW_anHo882hetrj36rCoH7xNzjW9JMGTG-Ww"


response = requests.get(
    f"{LUNO_API_URL}/balance",
    auth=(API_KEY, API_SECRET)
)


print(response.json())


