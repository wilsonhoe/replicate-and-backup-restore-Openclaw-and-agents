#!/bin/bash
# Start Chrome with debugging for Lisa automation

# Kill existing Chrome debug instance
pkill -f "remote-debugging-port=9222" 2>/dev/null

# Wait for cleanup
sleep 2

# Start Chrome with persistent profile
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile" \
  --no-first-run \
  --disable-background-networking \
  https://x.com \
  https://linkedin.com &

echo "Chrome started on port 9222"
echo "Login to Twitter and LinkedIn in the browser window"