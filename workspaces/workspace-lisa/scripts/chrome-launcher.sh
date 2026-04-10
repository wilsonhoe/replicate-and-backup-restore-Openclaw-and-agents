#!/bin/bash
# Chrome Pre-Launch Script for OpenClaw Browser Automation
# Date: April 8, 2026
# Purpose: Launch Chrome on port 18800 for stable agent browser access

CHROME_PATH="$HOME/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"
LOG_FILE="/tmp/chrome-cdp.log"
PORT=18800

echo "=== OpenClaw Chrome Launcher ==="
echo "Date: $(date)"
echo "Port: $PORT"
echo "Log: $LOG_FILE"
echo ""

# Check if Chrome is already running on port 18800
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✓ Chrome is already running on port $PORT"
    echo "Process: $(lsof -Pi :$PORT -sTCP:LISTEN -t)"
    exit 0
fi

# Check if Chrome binary exists
if [ ! -f "$CHROME_PATH" ]; then
    echo "✗ Chrome not found at: $CHROME_PATH"
    echo "Searching for Playwright Chrome..."
    
    # Try to find Chrome in common locations
    CHROME_PATH=$(find ~/.cache/ms-playwright -name "chrome-linux64" -type d 2>/dev/null | head -1)
    
    if [ -z "$CHROME_PATH" ]; then
        echo "✗ Chrome not found. Install Playwright:"
        echo "  npx playwright install chromium"
        exit 1
    fi
    
    CHROME_PATH="$CHROME_PATH/chrome"
fi

echo "✓ Found Chrome at: $CHROME_PATH"
echo "Launching Chrome on port $PORT..."

# Launch Chrome in headless mode with remote debugging
nohup "$CHROME_PATH" \
    --headless=new \
    --no-sandbox \
    --remote-debugging-port=$PORT \
    --disable-gpu \
    --disable-dev-shm-usage \
    --disable-setuid-sandbox \
    --disable-web-security \
    --disable-features=IsolateOrigins,site-per-process \
    > "$LOG_FILE" 2>&1 &

CHROME_PID=$!
disown $CHROME_PID 2>/dev/null

echo ""
echo "✓ Chrome launched with PID: $CHROME_PID"
echo "  Port: $PORT"
echo "  Log: $LOG_FILE"
echo ""

# Wait a moment for Chrome to start
sleep 2

# Verify Chrome is listening
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✓ Chrome is now listening on port $PORT"
    echo "✓ Browser automation should now work with agents"
else
    echo "✗ Chrome failed to start. Check log: $LOG_FILE"
    exit 1
fi

echo ""
echo "To stop Chrome: kill $CHROME_PID"
echo "To view logs: tail -f $LOG_FILE"
