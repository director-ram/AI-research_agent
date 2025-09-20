#!/bin/bash

echo "🚀 Starting AI Research Agent"
echo "============================"

echo ""
echo "Starting backend..."
gnome-terminal -- bash -c "source venv/bin/activate && python main.py; exec bash" 2>/dev/null || \
xterm -e "source venv/bin/activate && python main.py; bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)' && source venv/bin/activate && python main.py"' 2>/dev/null || \
echo "Please start backend manually: source venv/bin/activate && python main.py"

echo ""
echo "Waiting 5 seconds for backend to start..."
sleep 5

echo ""
echo "Starting frontend..."
gnome-terminal -- bash -c "cd frontend && npm run dev; exec bash" 2>/dev/null || \
xterm -e "cd frontend && npm run dev; bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/frontend && npm run dev"' 2>/dev/null || \
echo "Please start frontend manually: cd frontend && npm run dev"

echo ""
echo "✅ Both services starting..."
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop this script..."
wait
