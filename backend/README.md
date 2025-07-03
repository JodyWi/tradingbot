sudo apt install sqlitebrowser


cd database
sqlitebrowser tradingbot.db

sqlitebrowser ~/projects/tradingbot/database/tradingbot.db

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

Run Server

cd backend
source venv/bin/activate
python server.py

chmod +x run_backend.sh
./run_backend.sh

Run Node Server

cd backend
node server.js

kill if needed

sudo lsof -i :8000
sudo kill -9 <PID>

### Update `requirements.txt`  
pip freeze > requirements.txt  


