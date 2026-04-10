#!/usr/bin/env python3
"""
Discord Channel Monitor for OpenClaw Agents
Monitors channels and routes messages to appropriate agents
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from pathlib import Path

# Channel IDs
CHANNELS = {
    "research": "1359104387158147162",
    "command_center": "1359104415419138109",
    "execution": "1359104434668875782",
    "logs": "1359104454165961909"
}

AGENT_TOKENS = {
    "nyx": "REDACTED_SET_FROM_ENV",
    "lisa": "REDACTED_SET_FROM_ENV",
    "kael": "REDACTED_SET_FROM_ENV"
}

@dataclass
class DiscordMessage:
    """Represents a Discord message"""
    id: str
    content: str
    author: str
    timestamp: str
    channel: str
    mentions: List[str]


class ChannelMonitor:
    """Monitors Discord channels and routes to agents"""

    def __init__(self):
        self.last_message_ids = {}
        self.handlers: Dict[str, List[Callable]] = {}
        self.load_state()

    def load_state(self):
        """Load last seen message IDs"""
        state_file = Path("/home/wls/.openclaw/workspace/skills/discord-workflow/monitor_state.json")
        if state_file.exists():
            with open(state_file) as f:
                self.last_message_ids = json.load(f)

    def save_state(self):
        """Save last seen message IDs"""
        state_file = Path("/home/wls/.openclaw/workspace/skills/discord-workflow/monitor_state.json")
        with open(state_file, 'w') as f:
            json.dump(self.last_message_ids, f)

    def fetch_messages(self, channel_id: str, limit: int = 10) -> List[DiscordMessage]:
        """Fetch recent messages from a channel"""
        # Use Lisa's token to read all channels
        token = AGENT_TOKENS["lisa"]

        try:
            response = requests.get(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                headers={"Authorization": f"Bot {token}"},
                params={"limit": limit},
                timeout=10
            )

            if response.status_code != 200:
                print(f"❌ Failed to fetch messages: {response.status_code}")
                return []

            messages = []
            for msg in response.json():
                messages.append(DiscordMessage(
                    id=msg["id"],
                    content=msg["content"],
                    author=msg["author"]["username"],
                    timestamp=msg["timestamp"],
                    channel=channel_id,
                    mentions=[m["username"] for m in msg.get("mentions", [])]
                ))
            return messages

        except Exception as e:
            print(f"❌ Error fetching messages: {e}")
            return []

    def check_new_messages(self, channel_name: str) -> List[DiscordMessage]:
        """Check for new messages in a channel"""
        channel_id = CHANNELS.get(channel_name)
        if not channel_id:
            return []

        messages = self.fetch_messages(channel_id)
        last_id = self.last_message_ids.get(channel_name)

        # Filter to only new messages
        new_messages = []
        for msg in messages:
            if last_id and int(msg.id) <= int(last_id):
                continue
            new_messages.append(msg)

        # Update last seen
        if messages:
            self.last_message_ids[channel_name] = messages[0].id
            self.save_state()

        return new_messages

    def process_message(self, msg: DiscordMessage):
        """Process a message and route to appropriate agent"""
        print(f"\n📨 New message in #{msg.channel}")
        print(f"   From: {msg.author}")
        print(f"   Content: {msg.content[:100]}...")

        # Parse tags
        if "[OPPORTUNITY]" in msg.content:
            print("   → Routing to Lisa for review")
            self.notify_agent("lisa", f"New opportunity from {msg.author}: {msg.content[:200]}")

        elif "[APPROVED]" in msg.content:
            print("   → Routing to Kael for execution")
            self.notify_agent("kael", f"Approved task: {msg.content[:200]}")

        elif "[SUCCESS]" in msg.content or "[FAIL]" in msg.content:
            print("   → Routing to Lisa for review")
            self.notify_agent("lisa", f"Execution result: {msg.content[:200]}")

    def notify_agent(self, agent: str, message: str):
        """Write to agent's INBOX"""
        inbox_path = f"/home/wls/.openclaw/workspace-{agent}/INBOX.md"

        notification = f"""
[{datetime.now().isoformat()}] Discord Notification

{message}

---
"""

        try:
            with open(inbox_path, 'a') as f:
                f.write(notification)
            print(f"   ✅ Notification written to {agent}'s INBOX")
        except Exception as e:
            print(f"   ❌ Failed to write notification: {e}")

    def monitor_all(self):
        """Monitor all channels once"""
        print(f"\n🔍 Monitoring Discord channels at {datetime.now().isoformat()}")

        for channel_name in ["research", "command_center", "execution", "logs"]:
            new_messages = self.check_new_messages(channel_name)
            if new_messages:
                print(f"\n📬 {len(new_messages)} new messages in #{channel_name}")
                for msg in new_messages:
                    self.process_message(msg)
            else:
                print(f"   No new messages in #{channel_name}")


def run_monitor_loop(interval_minutes: int = 5):
    """Run the monitor in a loop"""
    monitor = ChannelMonitor()

    print("=" * 60)
    print("Discord Channel Monitor Started")
    print(f"Checking every {interval_minutes} minutes")
    print("=" * 60)

    while True:
        try:
            monitor.monitor_all()
            print(f"\n⏰ Sleeping for {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)
        except KeyboardInterrupt:
            print("\n👋 Monitor stopped")
            break
        except Exception as e:
            print(f"\n❌ Error in monitor loop: {e}")
            time.sleep(60)


def run_once():
    """Run monitor once (for cron)"""
    monitor = ChannelMonitor()
    monitor.monitor_all()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        run_monitor_loop()
    else:
        run_once()
