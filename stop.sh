#!/bin/bash

mkdir -p logs
chmod +x start.sh stop.sh

echo "🛑 Stopping Backend & Frontend..." | tee -a logs/backend.log logs/node_backend.log logs/frontend.log

# Stop Python backend on port 8001
if sudo lsof -t -i :8001 > /dev/null; then
    echo "⚠️ Stopping Python backend on port 8001..." | tee -a logs/backend.log
    sudo kill -9 $(sudo lsof -t -i :8001)
    echo "✅ Python backend stopped at $(date)" | tee -a logs/backend.log
else
    echo "✅ No Python backend process found on port 8001." | tee -a logs/backend.log
fi

# Stop Node backend on port 3002
if sudo lsof -t -i :3002 > /dev/null; then
    echo "⚠️ Stopping Node backend on port 3002..." | tee -a logs/node_backend.log
    sudo kill -9 $(sudo lsof -t -i :3002)
    echo "✅ Node backend stopped at $(date)" | tee -a logs/node_backend.log
else
    echo "✅ No Node backend process found on port 3002." | tee -a logs/node_backend.log
fi

# Stop frontend on port 3001
if sudo lsof -t -i :3001 > /dev/null; then
    echo "⚠️ Stopping frontend on port 3001..." | tee -a logs/frontend.log
    sudo kill -9 $(sudo lsof -t -i :3001)
    echo "✅ Frontend stopped at $(date)" | tee -a logs/frontend.log
else
    echo "✅ No frontend process found on port 3001." | tee -a logs/frontend.log
fi

echo "✅ All processes stopped!" | tee -a logs/backend.log logs/node_backend.log logs/frontend.log
