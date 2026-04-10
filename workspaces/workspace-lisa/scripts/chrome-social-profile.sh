#!/bin/bash
# Persistent Chrome profile for social media automation
# Uses a dedicated user-data-dir so cookies/sessions persist

PROFILE_DIR="$HOME/.openclaw/workspace-lisa/browser-profiles/social-automation"
PORT=18801  # Different port from main OpenClaw browser

mkdir -p "$PROFILE_DIR"

# Kill any existing instance on this port
pkill -f "user-data-dir=$PROFILE_DIR" 2>/dev/null

# Launch Chrome with persistent profile
google-chrome-stable \
  --remote-debugging-port=$PORT \
  --user-data-dir="$PROFILE_DIR" \
  --no-first-run \
  --disable-default-apps \
  "$@" &

echo "Chrome launched with persistent profile on port $PORT"
echo "Profile dir: $PROFILE_DIR"
