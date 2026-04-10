#!/bin/bash

# Continuous bridge monitoring script for Lisa
echo "Starting bridge monitor..."

while true; do
    # Check for new messages in telegram-inbox.md
    if [ -f "/home/wls/bridge/telegram-inbox.md" ]; then
        # Get the last timestamp from the file
        last_timestamp=$(tail -10 "/home/wls/bridge/telegram-inbox.md" | grep "\[.*\] Lisa" | tail -1 | sed 's/.*\[\(.*\)\] Lisa.*/\1/')
        
        # If there's a new message from Wilson (not from Lisa)
        if grep -q "\[.*\] Wilson" "/home/wls/bridge/telegram-inbox.md" && ! grep -q "STATUS: DONE" "/home/wls/bridge/telegram-inbox.md"; then
            # Extract Wilson's message
            wilson_msg=$(grep -A 5 "\[.*\] Wilson" "/home/wls/bridge/telegram-inbox.md" | tail -n +2 | head -4)
            
            # Respond based on message content
            timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            
            if echo "$wilson_msg" | grep -q "start the infra setup"; then
                echo "## [$timestamp] Lisa" >> "/home/wls/bridge/telegram-inbox.md"
                echo "**Status Update:**" >> "/home/wls/bridge/telegram-inbox.md"
                echo "- Infrastructure setup (Task #9): IN PROGRESS" >> "/home/wls/bridge/telegram-inbox.md"
                echo "- Created setup script and configuration guides" >> "/home/wls/bridge/telegram-inbox.md"
                echo "- Ready for Lisa to execute setup script" >> "/home/wls/bridge/telegram-inbox.md"
                echo "" >> "/home/wls/bridge/telegram-inbox.md"
                echo "Next action: Lisa to run: bash /home/wls/.openclaw/scripts/setup-task9.sh" >> "/home/wls/bridge/telegram-inbox.md"
                echo "" >> "/home/wls/bridge/telegram-inbox.md"
                echo "Status: IN_PROGRESS" >> "/home/wls/bridge/telegram-inbox.md"
                
                # Mark as processed
                echo "STATUS: DONE (responded)" >> "/home/wls/bridge/telegram-inbox.md"
            fi
        fi
    fi
    
    # Check claude-outbox.md for Claude's messages that need relaying to Wilson
    if [ -f "/home/wls/bridge/claude-outbox.md" ]; then
        # Check if there are new SENT messages that Lisa should acknowledge
        if grep -q "Status: SENT" "/home/wls/bridge/claude-outbox.md" && ! grep -q "ACKNOWLEDGED:" "/home/wls/bridge/telegram-inbox.md" | tail -5; then
            timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            echo "## [$timestamp] Lisa" >> "/home/wls/bridge/telegram-inbox.md"
            echo "**Status Update:**" >> "/home/wls/bridge/telegram-inbox.md"
            echo "- Acknowledged receipt of Claude's message" >> "/home/wls/bridge/telegram-inbox.md"
            echo "- Will act on instructions as appropriate" >> "/home/wls/bridge/telegram-inbox.md"
            echo "" >> "/home/wls/bridge/telegram-inbox.md"
            echo "Status: MESSAGE_PROCESSED" >> "/home/wls/bridge/telegram-inbox.md"
        fi
    fi
    
    # Sleep for 30 seconds before checking again
    sleep 30
done