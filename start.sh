#!/bin/bash
# Start script for Financial Tracker application

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Personal Finance Tracker Startup     ${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: Node.js/npm is not installed${NC}"
    exit 1
fi

# Start backend
echo -e "\n${GREEN}Starting backend server...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
if [ ! -f "venv/bin/flask" ]; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
fi

# Start backend in background
export FLASK_ENV=development
python app.py &
BACKEND_PID=$!
echo -e "${GREEN}Backend started on http://localhost:5000 (PID: $BACKEND_PID)${NC}"

# Start frontend
cd ../frontend
echo -e "\n${GREEN}Starting frontend server...${NC}"

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start frontend
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend starting on http://localhost:5173 (PID: $FRONTEND_PID)${NC}"

# Trap to cleanup on exit
cleanup() {
    echo -e "\n${BLUE}Shutting down servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Servers stopped${NC}"
    exit 0
}

trap cleanup INT TERM

echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}Both servers are starting...${NC}"
echo -e "${GREEN}Backend: http://localhost:5000${NC}"
echo -e "${GREEN}Frontend: http://localhost:5173${NC}"
echo -e "${BLUE}Press Ctrl+C to stop${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Wait for processes
wait
