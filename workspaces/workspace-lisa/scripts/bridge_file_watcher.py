#!/usr/bin/env python3
"""
Bridge File Watcher - Monitors claude-outbox.md for changes
Part of Lisa-Claude Bridge Monitoring System
"""

import os
import sys
import time
import hashlib
import signal
from pathlib import Path

# Configuration
BRIDGE_DIR = "/home/wls/bridge"
OUTBOX_FILE = f"{BRIDGE_DIR}/claude-outbox.md"
LAST_SEEN_FILE = "/home/wls/.openclaw/workspace-lisa/memory/bridge-last-seen.txt"
TRIGGER_FILE = f"{BRIDGE_DIR}/.bridge_trigger"
LOG_FILE = "/home/wls/.openclaw/workspace-lisa/memory/bridge-watcher.log"
CHECK_INTERVAL = 5  # seconds

def log(msg):
    """Log with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {msg}"
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def get_file_hash(filepath):
    """Get MD5 hash of file content"""
    try:
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def get_last_seen_timestamp():
    """Read last seen timestamp from memory"""
    try:
        with open(LAST_SEEN_FILE, "r") as f:
            return f.read().strip()
    except Exception:
        return "1970-01-01T00:00:00Z"

def extract_latest_timestamp(filepath):
    """Extract the latest timestamp from bridge file"""
    try:
        with open(filepath, "r") as f:
            content = f.read()
        # Find timestamps like [2026-04-09T22:45:00Z]
        import re
        timestamps = re.findall(r'\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\]', content)
        if timestamps:
            return max(timestamps)  # Return most recent
    except Exception:
        pass
    return None

def create_trigger(new_timestamp):
    """Create trigger file for cron to pick up"""
    try:
        with open(TRIGGER_FILE, "w") as f:
            f.write(f"new_message={new_timestamp}\n")
        log(f"✅ Trigger created: {new_timestamp}")
    except Exception as e:
        log(f"❌ Failed to create trigger: {e}")

def watch():
    """Main watch loop"""
    log("🟢 Bridge watcher started")
    log(f"   Monitoring: {OUTBOX_FILE}")
    log(f"   Check interval: {CHECK_INTERVAL}s")
    
    last_hash = get_file_hash(OUTBOX_FILE)
    last_seen = get_last_seen_timestamp()
    
    log(f"   Last seen: {last_seen}")
    
    while True:
        time.sleep(CHECK_INTERVAL)
        
        # Check if file exists
        if not os.path.exists(OUTBOX_FILE):
            continue
        
        # Get current hash
        current_hash = get_file_hash(OUTBOX_FILE)
        
        # Check for changes
        if current_hash != last_hash:
            last_hash = current_hash
            
            # Extract latest timestamp from file
            latest_timestamp = extract_latest_timestamp(OUTBOX_FILE)
            
            if latest_timestamp and latest_timestamp > last_seen:
                log(f"🔔 New message detected: {latest_timestamp}")
                
                # Create trigger file (cron will notify)
                create_trigger(latest_timestamp)
                
                # Update last seen
                last_seen = latest_timestamp
            else:
                log("ℹ️ File changed but no new timestamp")

def stop_handler(signum, frame):
    """Handle shutdown gracefully"""
    log("🛑 Bridge watcher stopped")
    sys.exit(0)

if __name__ == "__main__":
    # Setup signal handlers
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    os.makedirs(BRIDGE_DIR, exist_ok=True)
    
    # Start watching
    watch()
