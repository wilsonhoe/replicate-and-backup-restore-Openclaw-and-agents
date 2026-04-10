#!/usr/bin/env python3
"""
Discord Webhook Handler for OpenClaw
Receives Discord messages from OpenClaw plugin and routes to agents
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from message_router import RoutedMessage, generate_id, save_message_to_queue, process_queue


def parse_discord_message(content: str, author: str, channel: str) -> RoutedMessage:
    """Parse a Discord message and extract tags"""
    tags = []

    # Extract tags from content
    tag_patterns = [
        "[OPPORTUNITY]", "[APPROVED]", "[REJECTED]",
        "[EXECUTING]", "[SUCCESS]", "[FAIL]",
        "[SCALE]", "[OPTIMIZE]", "[TERMINATE]"
    ]

    for tag in tag_patterns:
        if tag in content:
            tags.append(tag)

    return RoutedMessage(
        id=generate_id(),
        source="discord",
        channel=channel,
        author=author,
        content=content,
        tags=tags,
        timestamp=datetime.now().isoformat()
    )


def receive_message(content: str, author: str, channel: str) -> bool:
    """Receive a message from Discord and queue it for routing"""
    try:
        msg = parse_discord_message(content, author, channel)

        if msg.tags:  # Only queue messages with workflow tags
            save_message_to_queue(msg)
            print(f"✅ Queued message from {author} in #{channel} with tags: {msg.tags}")
            return True
        else:
            print(f"   Skipped message from {author} (no workflow tags)")
            return False

    except Exception as e:
        print(f"❌ Error receiving message: {e}")
        return False


def main():
    """Process any queued messages"""
    print("Discord Webhook Handler")
    print("=" * 40)
    process_queue()


if __name__ == "__main__":
    main()
