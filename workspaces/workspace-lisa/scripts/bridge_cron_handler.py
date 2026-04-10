#!/usr/bin/env python3
"""
Bridge Cron Handler - Processes trigger files and notifies Lisa
Part of Lisa-Claude Bridge Monitoring System
"""

import os
import sys

# Configuration
BRIDGE_DIR = "/home/wls/bridge"
OUTBOX_FILE = f"{BRIDGE_DIR}/claude-outbox.md"
TRIGGER_FILE = f"{BRIDGE_DIR}/.bridge_trigger"
LAST_SEEN_FILE = "/home/wls/.openclaw/workspace-lisa/memory/bridge-last-seen.txt"

def process_trigger():
    """Process trigger file and return notification message"""
    
    if not os.path.exists(TRIGGER_FILE):
        return None
    
    try:
        # Read trigger content
        with open(TRIGGER_FILE, "r") as f:
            content = f.read().strip()
        
        # Parse timestamp
        timestamp = None
        for line in content.split("\n"):
            if line.startswith("new_message="):
                timestamp = line.split("=", 1)[1]
                break
        
        # Read message preview from bridge
        preview = ""
        try:
            with open(OUTBOX_FILE, "r") as f:
                lines = f.readlines()
                # Find the latest message
                for i, line in enumerate(lines):
                    if timestamp and timestamp in line:
                        # Get next few non-empty lines as preview
                        for j in range(i+1, min(i+5, len(lines))):
                            if lines[j].strip() and not lines[j].startswith("---"):
                                preview = lines[j].strip()[:100]
                                break
                        break
        except Exception:
            pass
        
        # Update last seen timestamp
        if timestamp:
            with open(LAST_SEEN_FILE, "w") as f:
                f.write(timestamp)
        
        # Delete trigger file
        os.remove(TRIGGER_FILE)
        
        # Build notification
        msg = f"""🔔 **New Message from Claude**

Timestamp: {timestamp}

Preview: {preview}{'...' if len(preview) >= 100 else ''}

📄 Full message: /home/wls/bridge/claude-outbox.md

Reply to this message to respond."""
        
        return msg
        
    except Exception as e:
        return f"❌ Error processing trigger: {e}"

if __name__ == "__main__":
    result = process_trigger()
    if result:
        print(result)
        sys.exit(0)
    else:
        # No trigger found - silent exit
        sys.exit(0)
