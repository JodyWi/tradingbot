#!/bin/bash

echo "🔍 Checking if port 8000 is in use..."

# Find and kill any process using port 8000
if sudo lsof -t -i :8000 > /dev/null; then
    echo "⚠️ Port 8000 is in use. Stopping process..."
    sudo kill -9 $(sudo lsof -t -i :8000)
    echo "✅ Port 8000 is now free."
else
    echo "✅ Port 8000 is free."
fi

echo "🚀 Starting Backend..."

# Navigate to backend folder
cd backend || exit

# Activate virtual environment
source venv/bin/activate

# Start the backend server
python server.py &

echo "✅ Backend is now running on port 8000!"
