#!/bin/bash
# Twitter Automation Runner
# Usage: ./run_twitter.sh [tweet_number]

cd "$(dirname "$0")"

# Check if playwright is available
if ! command -v node >/dev/null 2>&1; then
    echo "[ERROR] Node.js not found"
    exit 1
fi

# Default tweets from session
TWEET1="The AI agent economy is accelerating—fast. Companies aren't just using AI anymore. They're hiring AI agents. The shift from tool to teammate is happening now. Are you building agent-first workflows? #AI #Automation #BusinessGrowth"

TWEET2="Algorithmic trading isn't just for hedge funds anymore. AI-powered retail trading systems are matching institutional precision. Speed + Data + Automation = The new edge. You don't need a Bloomberg terminal. You need the right agents. #AITrading #FinTech #PassiveIncome"

TWEET3="The $1K/month passive income baseline is becoming table stakes. The new target? $10K/month with 90% automation. AI agents handling: Lead gen, Content creation, Customer support, Trading execution. Systems scale. Effort doesn't. #AIAgents #OnlineBusiness #Scalability"

# Select tweet
if [ "$1" == "1" ]; then
    TWEET="$TWEET1"
elif [ "$1" == "2" ]; then
    TWEET="$TWEET2"
elif [ "$1" == "3" ]; then
    TWEET="$TWEET3"
else
    TWEET="$TWEET1"
fi

# Create temp file with tweet
echo "$TWEET" > /tmp/tweet_text.txt

echo "[INFO] Running Twitter automation..."
echo "[INFO] Tweet length: ${#TWEET} characters"
echo "[INFO] Tweet preview: ${TWEET:0:60}..."
echo ""

# Run the automation
node twitter_automation.js /tmp/tweet_text.txt

# Cleanup
rm -f /tmp/tweet_text.txt
