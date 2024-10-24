```bash
#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i:"$1" >/dev/null 2>&1
}

# Check for required commands
if ! command_exists python; then
    echo "Error: Python is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "Error: Node.js is not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "Error: npm is not installed"
    exit 1
fi

# Check if ports are available
if port_in_use 8000; then
    echo "Error: Port 8000 is already in use"
    exit 1
fi

if port_in_use 3000; then
    echo "Error: Port 3000 is already in use"
    exit 1
fi

# Create log directory if it doesn't exist
mkdir -p logs

echo "Starting MAX POD application..."

# Start the backend server
echo "Starting backend server..."
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Check if backend started successfully
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "Error: Backend failed to start. Check logs/backend.log for details"
    kill $BACKEND_PID
    exit 1
fi

# Start the frontend development server
echo "Starting frontend server..."
npm start > logs/frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo "Waiting for frontend to start..."
sleep 10

# Check if frontend started successfully
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "Error: Frontend failed to start. Check logs/frontend.log for details"
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 1
fi

echo "Application started successfully!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the application"

# Function to cleanup processes on exit
cleanup() {
    echo "Stopping application..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Register cleanup function
trap cleanup INT TERM

# Keep script running
while true; do
    sleep 1
done