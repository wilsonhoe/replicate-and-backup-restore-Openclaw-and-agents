#!/usr/bin/env python3
"""
Discord Coordinator for OpenClaw Multi-Agent System
Implements SOUL-defined flow:
  Nyx → Lisa → Kael → Logs → Lisa

Fetches Discord messages and routes to agent INBOX files.
Only processes CRITICAL decision tags, ignores status messages.
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Discord Configuration (ControlCenter Guild: 1489520250515886110)
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

# Workspaces
WORKSPACES = {
    "lisa": "/home/wls/.openclaw/workspace-lisa",
    "nyx": "/home/wls/.openclaw/workspace-nyx",
    "kael": "/home/wls/.openclaw/workspace-kael"
}

# State file for tracking last seen messages
STATE_FILE = Path("/home/wls/.openclaw/workspace/skills/discord-workflow/coordinator_state.json")

# CRITICAL TAGS ONLY (per SOUL: no status messages like [IDLE], [WAIT], [MONITOR])
CRITICAL_TAGS = {
    # Nyx → Lisa
    "[OPPORTUNITY]": {"from": "nyx", "to": "lisa", "channel": "research"},
    # Lisa → Kael
    "[APPROVED]": {"from": "lisa", "to": "kael", "channel": "command_center"},
    # Lisa → Nyx (rejection feedback)
    "[REJECTED]": {"from": "lisa", "to": "nyx", "channel": "command_center"},
    # Kael → Lisa (execution status)
    "[EXECUTING]": {"from": "kael", "to": "lisa", "channel": "execution"},
    # Kael → Lisa (results)
    "[SUCCESS]": {"from": "kael", "to": "lisa", "channel": "logs"},
    "[FAIL]": {"from": "kael", "to": "lisa", "channel": "logs"},
    "[BLOCKED]": {"from": "kael", "to": "lisa", "channel": "logs"},
    # Lisa → All (final decisions)
    "[SCALE]": {"from": "lisa", "to": ["kael", "nyx"], "channel": "command_center"},
    "[OPTIMIZE]": {"from": "lisa", "to": ["kael", "nyx"], "channel": "command_center"},
    "[TERMINATE]": {"from": "lisa", "to": ["kael", "nyx"], "channel": "command_center"},
}

# IGNORED TAGS (status messages - do NOT route)
IGNORED_TAGS = ["[IDLE]", "[WAIT]", "[MONITOR]", "[STANDBY]", "[OBSERVE]", "[ACTIVE]"]


@dataclass
class DiscordMessage:
    id: str
    content: str
    author: str
    author_id: str
    timestamp: str
    channel_id: str
    channel_name: str
    mentions: List[Dict]


class DiscordCoordinator:
    """
    Coordinates multi-agent Discord workflow per SOUL specifications.
    Only processes CRITICAL decision tags, ignores status spam.
    """

    def __init__(self):
        self.state = self._load_state()
        self.processed_count = 0
        self.ignored_count = 0
        self.discord_available = True

    def _load_state(self) -> Dict:
        """Load last seen message IDs"""
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
        return {}

    def _save_state(self):
        """Save last seen message IDs"""
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)

    def fetch_messages(self, channel_id: str, limit: int = 50) -> Optional[List[DiscordMessage]]:
        """Fetch messages from Discord API using Lisa's token"""
        if not self.discord_available:
            return None

        token = AGENT_TOKENS["kael"]  # Use Kael's valid token for reading

        try:
            response = requests.get(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                headers={"Authorization": f"Bot {token}"},
                params={"limit": limit},
                timeout=15
            )

            if response.status_code == 401:
                print("  ❌ Discord authentication failed - tokens invalid")
                self.discord_available = False
                return None
            if response.status_code == 404:
                print("  ❌ Discord channel not found")
                return []
            if response.status_code != 200:
                print(f"  ❌ Discord API error: {response.status_code}")
                return []

            data = response.json()
            if not isinstance(data, list):
                return []

            messages = []
            for msg in data:
                if msg.get("author", {}).get("bot", False):
                    continue

                channel_name = "unknown"
                for name, cid in CHANNELS.items():
                    if cid == channel_id:
                        channel_name = name
                        break

                messages.append(DiscordMessage(
                    id=msg["id"],
                    content=msg.get("content", ""),
                    author=msg["author"]["username"],
                    author_id=msg["author"]["id"],
                    timestamp=msg["timestamp"],
                    channel_id=channel_id,
                    channel_name=channel_name,
                    mentions=msg.get("mentions", [])
                ))
            return messages

        except Exception as e:
            print(f"  ❌ Error: {e}")
            return []

    def extract_critical_tags(self, content: str) -> List[str]:
        """Extract only CRITICAL tags from message content"""
        found_tags = []
        content_upper = content.upper()
        for tag in CRITICAL_TAGS.keys():
            if tag.upper() in content_upper:
                found_tags.append(tag)
        return found_tags

    def has_ignored_tags(self, content: str) -> bool:
        """Check if message has ignored status tags"""
        content_upper = content.upper()
        for tag in IGNORED_TAGS:
            if tag.upper() in content_upper:
                return True
        return False

    def write_to_inbox(self, agent: str, msg: DiscordMessage, tags: List[str]):
        """Write notification to agent's INBOX.md"""
        inbox_path = Path(f"{WORKSPACES[agent]}/INBOX.md")
        inbox_path.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().isoformat()

        action_map = {
            "[OPPORTUNITY]": "New opportunity in #research. Review and post [APPROVED] or [REJECTED].",
            "[APPROVED]": "Lisa APPROVED an opportunity. Check #command-center for assignment.",
            "[REJECTED]": "Opportunity rejected. Review Lisa's feedback in #command-center.",
            "[EXECUTING]": "Execution started by Kael. Monitor #execution for progress.",
            "[SUCCESS]": "Task completed. Review results and post [SCALE], [OPTIMIZE], or [TERMINATE].",
            "[FAIL]": "Task failed. Review error details and decide [TERMINATE] or [OPTIMIZE].",
            "[BLOCKED]": "Execution BLOCKED. Review blocker details and provide guidance.",
            "[SCALE]": "Lisa ordered SCALE. Expand the successful system.",
            "[OPTIMIZE]": "Lisa ordered OPTIMIZE. Fix issues and retry.",
            "[TERMINATE]": "Mission TERMINATED. Archive and move to next opportunity.",
        }

        action_text = action_map.get(tags[0], "Review and respond per SOUL protocol.")

        notification = f"""
## [{timestamp}] Discord Alert | #{msg.channel_name} | Tags: {', '.join(tags)}

**From**: {msg.author}
**Content**:
{msg.content[:800]}{'...' if len(msg.content) > 800 else ''}

**Action Required**: {action_text}

---
"""
        try:
            with open(inbox_path, 'a') as f:
                f.write(notification)
            print(f"    ✅ Routed to {agent}'s INBOX")
            return True
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            return False

    def route_message(self, msg: DiscordMessage):
        """Route a message based on critical tags"""
        if self.has_ignored_tags(msg.content):
            self.ignored_count += 1
            return

        critical_tags = self.extract_critical_tags(msg.content)
        if not critical_tags:
            return

        print(f"\n  📨 [{msg.channel_name}] {msg.author}: {msg.content[:80]}...")
        print(f"    Critical tags: {', '.join(critical_tags)}")

        for tag in critical_tags:
            config = CRITICAL_TAGS.get(tag)
            if not config:
                continue
            recipients = config["to"]
            if isinstance(recipients, str):
                recipients = [recipients]
            for recipient in recipients:
                self.write_to_inbox(recipient, msg, [tag])

        self.processed_count += 1

    def process_channel(self, channel_name: str):
        """Process messages from a specific channel"""
        channel_id = CHANNELS.get(channel_name)
        if not channel_id:
            return

        print(f"\n📡 Checking #{channel_name}...")
        messages = self.fetch_messages(channel_id)

        if messages is None:
            print("  ⚠️  Discord unavailable - use file-based bridge")
            return

        if not messages:
            print("  No messages")
            return

        last_id = self.state.get(channel_name)
        new_messages = [m for m in messages if not last_id or int(m.id) > int(last_id)]

        if not new_messages:
            print("  No new messages")
            return

        print(f"  {len(new_messages)} new messages")
        self.state[channel_name] = messages[0].id
        self._save_state()

        for msg in new_messages:
            self.route_message(msg)

    def run(self):
        """Check all channels and route messages"""
        print("=" * 70)
        print("Discord Coordinator - Multi-Agent Workflow")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 70)
        print("\nProcessing CRITICAL tags only:")
        for tag, config in CRITICAL_TAGS.items():
            to_str = config["to"] if isinstance(config["to"], str) else ", ".join(config["to"])
            print(f"  {tag} → {to_str}")
        print("\nIgnoring:", ", ".join(IGNORED_TAGS))

        for channel_name in ["research", "command_center", "execution", "logs"]:
            self.process_channel(channel_name)
            if not self.discord_available:
                break

        print("\n" + "=" * 70)
        print(f"Complete: {self.processed_count} routed, {self.ignored_count} ignored")
        if not self.discord_available:
            print("⚠️  Discord unavailable - using file-based bridge mode")
        print("=" * 70)


def main():
    coordinator = DiscordCoordinator()
    coordinator.run()


if __name__ == "__main__":
    main()
