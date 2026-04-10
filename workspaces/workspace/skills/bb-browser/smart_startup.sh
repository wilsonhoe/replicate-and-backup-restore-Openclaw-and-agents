#!/bin/bash
# Smart Chrome startup for bb-browser with login preservation

echo "🚀 Smart Chrome Startup for bb-browser"
echo "======================================"

# Kill existing Chrome processes
echo "1. Stopping existing Chrome processes..."
pkill chrome 2>/dev/null
pkill chromium 2>/dev/null
sleep 2

# Find Chrome executable
if command -v chromium-browser &> /dev/null; then
    CHROME_CMD="chromium-browser"
elif command -v google-chrome &> /dev/null; then
    CHROME_CMD="google-chrome"
elif command -v chromium &> /dev/null; then
    CHROME_CMD="chromium"
else
    echo "❌ No Chrome/Chromium found!"
    exit 1
fi

echo "2. Using Chrome: $CHROME_CMD"

# Method 1: Use existing profile (recommended)
echo "3. Starting Chrome with existing profile..."
echo "   Open your accounts in this Chrome window, then press Ctrl+C to continue..."

# Start Chrome normally first
$CHROME_CMD &
CHROME_PID=$!
echo "   Chrome PID: $CHROME_PID"
echo ""
echo "   📝 NOW: Log into your accounts (Twitter, Reddit, LinkedIn, etc.)"
echo "   📝 When done logging in, press Ctrl+C to continue..."
echo ""

# Wait for user to log in
wait $CHROME_PID

echo ""
echo "4. Restarting Chrome with debugging port..."

# Now restart with debugging, preserving the profile
$CHROME_CMD --remote-debugging-port=9222 &
NEW_PID=$!

echo "   Chrome with debugging PID: $NEW_PID"
echo "   Debugging port: 9222"
echo ""
echo "✅ Chrome is ready for bb-browser!"
echo ""
echo "Test commands:"
echo "  bb-browser site twitter/search 'AI agent' 5"
echo "  bb-browser site reddit/hot 10"
echo "  bb-browser site arxiv/search 'machine learning' 3"
