#!/bin/bash

# Create logs folder if it doesn't exist
mkdir -p logs

# Ensure scripts are executable
chmod +x start.sh stop.sh

# Function to free a port if in use
free_port() {
  local port=$1
  echo "🔍 Checking if port $port is in use..."
  if sudo lsof -t -i :$port > /dev/null; then
    echo "⚠️ Port $port is in use. Stopping process..."
    sudo kill -9 $(sudo lsof -t -i :$port)
    echo "✅ Port $port is now free."
  else
    echo "✅ Port $port is free."
  fi
}

# Free backend (Python) port 8001
free_port 8001

# Free React frontend port 3001
free_port 3001

# Free Node backend port 3002
free_port 3002

echo "🚀 Starting Backend (Python)..."
cd backend || exit
source venv/bin/activate

# Append logs instead of overwriting
python server.py >> ../logs/backend.log 2>&1 &

echo "✅ Python Backend is running on port 8001!"

echo "🚀 Starting Backend (Node)..."
# Start Node backend (assumes server.js in backend folder)
node server.js >> ../logs/node_backend.log 2>&1 &

echo "✅ Node Backend is running on port 3002!"

echo "🚀 Starting Frontend..."
cd .. || exit

# Append logs instead of overwriting
npm start >> logs/frontend.log 2>&1 &

echo "✅ Frontend is running! Logs are being written to /logs/"
