#!/bin/bash

# Create logs folder if it doesn't exist
mkdir -p logs

# Ensure scripts are executable
chmod +x start.sh stop.sh

echo "🔍 Checking if port 8001 (backend) is in use..."
if sudo lsof -t -i :8001 > /dev/null; then
    echo "⚠️ Port 8001 is in use. Stopping process..."
    sudo kill -9 $(sudo lsof -t -i :8001)
    echo "✅ Port 8001 is now free."
else
    echo "✅ Port 8001 is free."
fi

echo "🔍 Checking if port 3001 (frontend) is in use..."
if sudo lsof -t -i :3001 > /dev/null; then
    echo "⚠️ Port 3001 is in use. Stopping process..."
    sudo kill -9 $(sudo lsof -t -i :3001)
    echo "✅ Port 3001 is now free."
else
    echo "✅ Port 3001 is free."
fi

echo "🚀 Starting Backend..."
cd backend || exit
source venv/bin/activate

# Append logs instead of overwriting
python server.py >> ../logs/backend.log 2>&1 &

echo "✅ Backend is running on port 8001!"

echo "🚀 Starting Frontend..."
cd .. || exit

# Append logs instead of overwriting
npm start >> logs/frontend.log 2>&1 &

echo "✅ Both Backend & Frontend are running! Logs are being written to /logs/."
