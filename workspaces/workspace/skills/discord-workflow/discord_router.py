#!/usr/bin/env python3
"""
Discord Message Router for OpenClaw Multi-Agent System
Implements SOUL-defined flow: Nyx → Lisa → Kael → Logs → Lisa
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Discord Configuration - From discord_coordinator.py (ControlCenter Guild)
CHANNELS = {
    "research": "1489884494935752784",
    "command_center": "1489884533191872603",
    "execution": "1489884515886301335",
    "logs": "1489884548383641642"
}

AGENT_TOKENS = {
    "nyx": "REDACTED_SET_FROM_ENV",
    "lisa": "REDACTED_SET_FROM_ENV",
    "kael": "REDACTED_SET_FROM_ENV"
}

# Workspace paths
WORKSPACES = {
    "lisa": "/home/wls/.openclaw/workspace-lisa",
    "nyx": "/home/wls/.openclaw/workspace-nyx",
    "kael": "/home/wls/.openclaw/workspace-kael"
}


@dataclass
class DiscordMessage:
    id: str
    content: str
    author: str
    author_id: str
    timestamp: str
    channel_id: str
    mentions: List[Dict]


class DiscordRouter:
    """Routes Discord messages to agent INBOX files per SOUL specifications"""

    def __init__(self):
        self.state_file = Path("/home/wls/.openclaw/workspace/skills/discord-workflow/router_state.json")
        self.last_message_ids = self._load_state()

    def _load_state(self) -> Dict:
        """Load last seen message IDs"""
        if self.state_file.exists():
            with open(self.state_file) as f:
                return json.load(f)
        return {}

    def _save_state(self):
        """Save last seen message IDs"""
        with open(self.state_file, 'w') as f:
            json.dump(self.last_message_ids, f, indent=2)

    def fetch_messages(self, channel_id: str, limit: int = 20) -> List[DiscordMessage]:
        """Fetch messages from Discord API"""
        token = AGENT_TOKENS["lisa"]  # Lisa token can read all channels

        try:
            response = requests.get(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                headers={"Authorization": f"Bot {token}"},
                params={"limit": limit},
                timeout=15
            )

            if response.status_code != 200:
                print(f"❌ Discord API error: {response.status_code}")
                return []

            messages = []
            for msg in response.json():
                # Skip bot messages to avoid loops
                if msg["author"].get("bot", False):
                    continue

                messages.append(DiscordMessage(
                    id=msg["id"],
                    content=msg["content"],
                    author=msg["author"]["username"],
                    author_id=msg["author"]["id"],
                    timestamp=msg["timestamp"],
                    channel_id=channel_id,
                    mentions=msg.get("mentions", [])
                ))
            return messages

        except Exception as e:
            print(f"❌ Error fetching messages: {e}")
            return []

    def write_to_inbox(self, agent: str, content: str):
        """Write notification to agent's INBOX.md"""
        inbox_path = Path(f"{WORKSPACES[agent]}/INBOX.md")

        # Ensure directory exists
        inbox_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().isoformat()
        message = f"""
## [{timestamp}] Discord Alert

{content}

**Action Required**: Check Discord and respond according to SOUL protocol.

---
"""

        try:
            with open(inbox_path, 'a') as f:
                f.write(message)
            print(f"   ✅ Routed to {agent}'s INBOX")
        except Exception as e:
            print(f"   ❌ Failed to write to {agent}'s INBOX: {e}")

    def route_research_to_lisa(self, msg: DiscordMessage):
        """Route [OPPORTUNITY] from #research to Lisa"""
        if "[OPPORTUNITY]" in msg.content:
            print(f"   🎯 Found OPPORTUNITY from {msg.author}")
            self.write_to_inbox("lisa", f"""**New Opportunity Posted in #research**

From: {msg.author}
Content: {msg.content[:500]}...

**Your Action**: Review and post [APPROVED] or [REJECTED] in #command-center""")

    def route_command_to_kael(self, msg: DiscordMessage):
        """Route [APPROVED] from #command-center to Kael"""
        if "[APPROVED]" in msg.content:
            # Check if Kael is mentioned or assigned
            content_lower = msg.content.lower()
            if "kael" in content_lower or msg.author == "lisa":
                print(f"   ✅ Found APPROVED task for Kael")
                self.write_to_inbox("kael", f"""**New Assignment from Lisa**

From: {msg.author}
Content: {msg.content[:500]}...

**Your Action**: Post [EXECUTING] in #execution, then execute and report [SUCCESS]/[FAIL] in #logs""")

    def route_command_to_nyx(self, msg: DiscordMessage):
        """Route [REJECTED] feedback from #command-center to Nyx"""
        if "[REJECTED]" in msg.content:
            content_lower = msg.content.lower()
            # Check if this was Nyx's opportunity
            if "opportunity" in content_lower:
                print(f"   🔄 Found REJECTED feedback for Nyx")
                self.write_to_inbox("nyx", f"""**Opportunity Rejected - Feedback from Lisa**

From: {msg.author}
Content: {msg.content[:500]}...

**Your Action**: Review feedback, adjust research, post new [OPPORTUNITY]""")

    def route_logs_to_lisa(self, msg: DiscordMessage):
        """Route [SUCCESS]/[FAIL] from #logs to Lisa"""
        if "[SUCCESS]" in msg.content or "[FAIL]" in msg.content:
            print(f"   📊 Found execution result from {msg.author}")
            self.write_to_inbox("lisa", f"""**Execution Report in #logs**

From: {msg.author}
Content: {msg.content[:500]}...

**Your Action**: Review and post [SCALE], [OPTIMIZE], or [TERMINATE] in #command-center""")

    def route_execution_status(self, msg: DiscordMessage):
        """Route [EXECUTING] status from #execution to Lisa"""
        if "[EXECUTING]" in msg.content:
            print(f"   🚀 Found EXECUTING status from {msg.author}")
            # Just log this, Lisa monitors execution channel
            self.write_to_inbox("lisa", f"""**Execution Started - Status Update**

From: {msg.author}
Content: {msg.content[:300]}...

**Status**: Task in progress. Check #execution for updates.""")

    def process_channel(self, channel_name: str):
        """Process messages from a specific channel"""
        channel_id = CHANNELS.get(channel_name)
        if not channel_id:
            return

        print(f"\n📡 Checking #{channel_name}...")

        messages = self.fetch_messages(channel_id)
        if not messages:
            print("   No messages found")
            return

        last_id = self.last_message_ids.get(channel_name)
        new_messages = []

        for msg in messages:
            # Skip if already seen
            if last_id and int(msg.id) <= int(last_id):
                continue
            new_messages.append(msg)

        if not new_messages:
            print("   No new messages")
            return

        print(f"   📬 {len(new_messages)} new messages")

        # Update last seen
        self.last_message_ids[channel_name] = messages[0].id
        self._save_state()

        # Route each message
        for msg in new_messages:
            self.route_message(msg, channel_name)

    def route_message(self, msg: DiscordMessage, channel_name: str):
        """Route a message based on channel and content"""
        print(f"\n   📝 From {msg.author}: {msg.content[:100]}...")

        if channel_name == "research":
            self.route_research_to_lisa(msg)
        elif channel_name == "command_center":
            self.route_command_to_kael(msg)
            self.route_command_to_nyx(msg)
        elif channel_name == "execution":
            self.route_execution_status(msg)
        elif channel_name == "logs":
            self.route_logs_to_lisa(msg)

    def run(self):
        """Check all channels and route messages"""
        print("=" * 60)
        print("Discord Message Router")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 60)

        for channel_name in ["research", "command_center", "execution", "logs"]:
            self.process_channel(channel_name)

        print("\n" + "=" * 60)
        print("Router complete")
        print("=" * 60)


def main():
    router = DiscordRouter()
    router.run()


if __name__ == "__main__":
    main()
