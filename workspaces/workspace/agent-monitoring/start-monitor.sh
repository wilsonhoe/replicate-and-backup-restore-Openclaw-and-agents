#!/bin/bash

# Agent Activity Monitor Startup Script
# Starts the real-time monitoring system with dashboard

echo "Starting OpenClaw Agent Activity Monitor..."
echo "========================================"

# Change to the monitoring directory
cd "$(dirname "$0")"

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed or not in PATH"
    echo "Please install Node.js to run the monitoring system"
    exit 1
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed or not in PATH"
    echo "Please install npm to run the monitoring system"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the monitoring system
echo "Starting monitoring system..."
echo "Dashboard will be available at: http://localhost:3001"
echo "Press Ctrl+C to stop the monitor"
echo "========================================"

npm start