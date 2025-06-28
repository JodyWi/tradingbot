# 🏦 TradingBot_ST  
A Work-in-Progress AI-Powered Trading Bot that integrates **Python for backend processing**. The bot interacts with the **LUNO API** and can be extended with **LLM models** for advanced trading strategies.  

## 📌 Project Setup  
### Update `requirements.txt`  
pip freeze > requirements.txt  

### Generate Project Directory Structure  
tree -a -I 'node_modules|objects|build|venv|__pycache__|venvtest|junk|.git' > directory_structure.txt  

## 📌 Backend Setup 🖥️  
⚙️ Backend is a Work-in-Progress (WIP)  

### Setting Up Python in Backend  
Run the following commands to set up the Python environment inside the backend folder:  
cd backend  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  

**Possible Issue:**  
If you encounter the following error:  
error: externally-managed-environment  
× This environment is externally managed  

Run the following fix:  
pip install --break-system-packages -r requirements.txt  
This will **bypass the restriction** and allow package installation.  

### Starting the Backend  
cd ~/projects/tradingbot/backend  
source venv/bin/activate  
python3 main.py  

## 📌 Running the Standalone Bot  
cd ~/projects/tradingbot  
python3 run_standalone.py  
cd ~/projects/tradingbot  
python3 run.py  

## 📌 LLM Integration 🤖  
The bot can integrate with **Ollama LLM models** to assist with decision-making.  

### Set Up Ollama API  
export OLLAMA_API_BASE=http://127.0.0.1:11434  

### Running Aider with Llama Models  
aider --model ollama/llama3.1  
aider --model ollama/codellama --edit-format whole  
aider --model ollama/llama3.1 --edit-format whole  

## 📌 LUNO API Configuration 🔑  
⚠️ Ensure API keys are stored securely. Do NOT hardcode them in the project. Use `.env` file instead.  

### Example `.env` File  


## 📌 Notes & Additional Commands  
### Activate Virtual Environment  
source ~/projects/tradingbot/backend/venv/bin/activate  

### Start Backend  
cd ~/projects/tradingbot/backend  
python3 main.py  

## 📌 Next Steps 🚀  
- [ ] Complete Backend API  
- [ ] Enhance Trading Strategies  
- [ ] Implement Logging & Monitoring  
- [ ] Deploy for Automated Trading  

## DB
sudo apt install sqlite3


## 📌 About  
This project is an AI-powered trading bot designed to execute **LUNO API trades** automatically. It leverages **LLMs for smarter decision-making** and aims to be fully **autonomous in future iterations**.  


tree -I 'node_modules|.git|dist|build|.next|.cache|logs' -L 4



Rate Limiting
APIs are rate limited to 300 calls per minute. Calls made in excess of this limit will receive a HTTP error Code 429 response.

The streaming API is limited to 50 sessions open simultaneously. Calls in excess of this limit will receive a session limit exceeded message.


Security
Always use HTTPS when calling the API. Non-TLS HTTP requests cause error 403 to be returned. Using non-TLS requests can leak your authentication credentials.

Verify that your client validates the server's SSL certificate. Many libraries (e.g. urllib2 in Python2) do not validate server certificates by default. Failing to verify the server certificate makes your application vulnerable to man-in-the-middle attack.

Minimum withdrawal amount
When you’re withdrawing funds from your local currency wallet, here’s the minimum withdrawal amount for your country:

COUNTRY	MINIMUM WITHDRAWAL AMOUNT

South Africa	R10
