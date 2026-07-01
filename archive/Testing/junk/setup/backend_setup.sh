#!/bin/bash

echo "🔧 Setting up the backend environment..."

# Navigate to backend folder
cd backend || exit

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed! Please install Python before running this script."
    exit 1
fi

# Create a virtual environment
if [ ! -d "venv" ]; then
    echo "📂 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists."
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Start the backend server
echo "🚀 Starting backend server..."
python server.py &

echo "✅ Backend setup complete!"
