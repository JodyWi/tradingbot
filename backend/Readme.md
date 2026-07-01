python3 -m venv ../.venv

source ../.venv/bin/activate

pip install -r ../requirements.txt

Run Server

cd ..
source .venv/bin/activate
python server.py

./startup.sh

Run Node Server

cd ..
node server.js

kill if needed

sudo lsof -i :8000
sudo kill -9 <PID>

### Update `requirements.txt`  
pip freeze > requirements.txt  
sudo kill -9 74811
