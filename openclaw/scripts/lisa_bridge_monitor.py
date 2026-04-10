#!/usr/bin/env python3
"""
Lisa Bridge Monitor - Real-time bridge watcher for Claude <-> Lisa communication
Triggers Lisa agent when Claude sends a message
"""

import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Configuration
BRIDGE_FILE = Path("/home/wls/.openclaw/workspace-lisa/BRIDGE_LISA.md")
TRIGGER_FILE = Path("/home/wls/.openclaw/workspace-lisa/.lisa_trigger")
LOG_FILE = Path("/home/wls/.openclaw/workspace-lisa/.bridge_lisa.log")
STATE_FILE = Path("/home/wls/.openclaw/workspace-lisa/.lisa_bridge_state.json")
POLL_INTERVAL = 5  # seconds

def log(message: str):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\n")

def get_file_hash(filepath: Path) -> str:
    """Calculate MD5 hash of file"""
    if not filepath.exists():
        return ""
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def save_state(state: dict):
    """Save monitoring state"""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def load_state() -> dict:
    """Load monitoring state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_hash": "", "last_message_from": None}

def check_for_claude_message(filepath: Path) -> dict:
    """Check if last message in bridge is from Claude"""
    if not filepath.exists():
        return {"found": False}

    content = filepath.read_text()

    # Look for Claude message headers (## [timestamp] Claude)
    lines = content.split("\n")
    claude_entries = []
    current_entry = None

    for i, line in enumerate(lines):
        if line.strip().startswith("## [") and "Claude" in line:
            # Found a Claude message header
            timestamp_match = line[line.find("[")+1:line.find("]")]
            current_entry = {
                "timestamp": timestamp_match,
                "line_number": i,
                "content": line + "\n"
            }
            claude_entries.append(current_entry)
        elif current_entry and line.strip().startswith("## ["):
            # New entry starts, stop collecting
            current_entry = None
        elif current_entry:
            current_entry["content"] += line + "\n"

    if claude_entries:
        # Get the last Claude message
        last_entry = claude_entries[-1]
        return {
            "found": True,
            "timestamp": last_entry["timestamp"],
            "line": last_entry["line_number"],
            "preview": last_entry["content"][:200]
        }

    return {"found": False}

def create_lisa_trigger(message_info: dict):
    """Create trigger file for Lisa agent"""
    trigger_data = {
        "triggered_at": datetime.now().isoformat(),
        "source": "bridge_monitor",
        "action": "READ_AND_RESPOND",
        "message_from": "claude",
        "message_timestamp": message_info.get("timestamp"),
        "message_preview": message_info.get("preview", "")[:100],
        "bridge_file": str(BRIDGE_FILE)
    }

    with open(TRIGGER_FILE, "w") as f:
        json.dump(trigger_data, f, indent=2)

    log(f"🟢 Created trigger for Lisa: {message_info.get('timestamp')}")

def main():
    """Main monitoring loop"""
    log("=" * 50)
    log("Lisa Bridge Monitor Started")
    log(f"Monitoring: {BRIDGE_FILE}")
    log(f"Trigger: {TRIGGER_FILE}")
    log(f"Poll interval: {POLL_INTERVAL}s")
    log("=" * 50)

    # Load or initialize state
    state = load_state()
    last_hash = state.get("last_hash", "")

    # Get initial hash
    current_hash = get_file_hash(BRIDGE_FILE)
    if current_hash:
        if not last_hash:
            last_hash = current_hash
            state["last_hash"] = last_hash
            save_state(state)
        log(f"Initial hash: {last_hash[:16]}...")
    else:
        log("Bridge file not found, waiting for creation...")

    try:
        while True:
            time.sleep(POLL_INTERVAL)

            # Check if bridge file exists
            if not BRIDGE_FILE.exists():
                continue

            # Calculate current hash
            current_hash = get_file_hash(BRIDGE_FILE)

            # Check if file changed
            if current_hash != last_hash:
                log(f"🔴 BRIDGE CHANGED - Hash: {current_hash[:16]}...")

                # Check if last message is from Claude
                message_info = check_for_claude_message(BRIDGE_FILE)

                if message_info["found"]:
                    last_from = state.get("last_message_from")
                    current_from = message_info["timestamp"]

                    # Only trigger if this is a new Claude message
                    if last_from != current_from:
                        log(f"📨 New message from Claude detected")
                        log(f"   Timestamp: {message_info['timestamp']}")
                        log(f"   Preview: {message_info['preview'][:80]}...")

                        create_lisa_trigger(message_info)

                        # Update state
                        state["last_message_from"] = current_from
                    else:
                        log("   (Already responded to this message)")
                else:
                    log("   (No Claude message found - Lisa may have responded)")

                # Update hash and save state
                last_hash = current_hash
                state["last_hash"] = last_hash
                save_state(state)

    except KeyboardInterrupt:
        log("\nMonitor stopped by user")
        save_state(state)
        sys.exit(0)
    except Exception as e:
        log(f"❌ ERROR: {e}")
        save_state(state)
        sys.exit(1)

if __name__ == "__main__":
    main()
