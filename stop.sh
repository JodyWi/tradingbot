#!/bin/bash

# Create logs folder if it doesn't exist
mkdir -p logs

# Ensure scripts are executable
chmod +x start.sh stop.sh

echo "🛑 Stopping Backend & Frontend..." | tee -a logs/backend.log logs/frontend.log

# Stop backend running on port 8001
if sudo lsof -t -i :8001 > /dev/null; then
    echo "⚠️ Stopping backend process on port 8001..." | tee -a logs/backend.log
    sudo kill -9 $(sudo lsof -t -i :8001)
    echo "✅ Backend stopped successfully at $(date)" | tee -a logs/backend.log
else
    echo "✅ No backend process found on port 8001." | tee -a logs/backend.log
fi

# Stop frontend running on port 3001
if sudo lsof -t -i :3001 > /dev/null; then
    echo "⚠️ Stopping frontend process on port 3001..." | tee -a logs/frontend.log
    sudo kill -9 $(sudo lsof -t -i :3001)
    echo "✅ Frontend stopped successfully at $(date)" | tee -a logs/frontend.log
else
    echo "✅ No frontend process found on port 3001." | tee -a logs/frontend.log
fi

echo "✅ All processes stopped!" | tee -a logs/backend.log logs/frontend.log
