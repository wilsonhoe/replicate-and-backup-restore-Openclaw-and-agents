#!/usr/bin/env python3
"""
OpenClaw Discord Message Router
Routes messages via file-based queue since OpenClaw handles Discord directly
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Agent workspaces
WORKSPACES = {
    "lisa": "/home/wls/.openclaw/workspace-lisa",
    "nyx": "/home/wls/.openclaw/workspace-nyx",
    "kael": "/home/wls/.openclaw/workspace-kael"
}

# Message queue directory
QUEUE_DIR = Path("/home/wls/.openclaw/workspace/skills/discord-workflow/queue")
QUEUE_DIR.mkdir(exist_ok=True)


@dataclass
class RoutedMessage:
    """A message to be routed to an agent"""
    id: str
    source: str  # discord, system, etc.
    channel: str  # research, command_center, execution, logs
    author: str
    content: str
    tags: List[str]  # [OPPORTUNITY], [APPROVED], etc.
    timestamp: str
    processed: bool = False


def generate_id() -> str:
    """Generate unique message ID"""
    return f"msg_{int(time.time() * 1000)}"


def write_to_inbox(agent: str, message: RoutedMessage):
    """Write notification to agent's INBOX.md"""
    inbox_path = Path(f"{WORKSPACES[agent]}/INBOX.md")
    inbox_path.parent.mkdir(parents=True, exist_ok=True)

    notification = f"""
## [{message.timestamp}] Discord Workflow Alert

**Channel**: #{message.channel}
**From**: {message.author}
**Tags**: {', '.join(message.tags)}

**Content**:
{message.content[:500]}{'...' if len(message.content) > 500 else ''}

**Action Required**: Respond according to SOUL protocol.

---
"""

    try:
        with open(inbox_path, 'a') as f:
            f.write(notification)
        print(f"   ✅ Routed to {agent}'s INBOX")
        return True
    except Exception as e:
        print(f"   ❌ Failed to write to {agent}'s INBOX: {e}")
        return False


def save_message_to_queue(msg: RoutedMessage):
    """Save message to queue for processing"""
    queue_file = QUEUE_DIR / f"{msg.id}.json"
    with open(queue_file, 'w') as f:
        json.dump(asdict(msg), f, indent=2)


def process_queue():
    """Process all pending messages in queue"""
    queue_files = sorted(QUEUE_DIR.glob("msg_*.json"))

    if not queue_files:
        return

    print(f"\n📬 Processing {len(queue_files)} queued messages...")

    for queue_file in queue_files:
        try:
            with open(queue_file) as f:
                data = json.load(f)
            msg = RoutedMessage(**data)

            if msg.processed:
                queue_file.unlink()
                continue

            route_message(msg)

            # Mark as processed
            msg.processed = True
            save_message_to_queue(msg)
            queue_file.unlink()  # Remove processed message

        except Exception as e:
            print(f"   ❌ Error processing {queue_file.name}: {e}")


def route_message(msg: RoutedMessage):
    """Route a message to the appropriate agent based on content tags"""
    print(f"\n   📝 From {msg.author} in #{msg.channel}")
    print(f"   Tags: {', '.join(msg.tags)}")

    # Route based on tags and channel
    if "[OPPORTUNITY]" in msg.tags and msg.channel == "research":
        # Nyx posts opportunity → Route to Lisa
        print("   → Routing to Lisa (Authority Layer)")
        write_to_inbox("lisa", msg)

    elif "[APPROVED]" in msg.tags and msg.channel == "command_center":
        # Lisa approves → Route to Kael
        print("   → Routing to Kael (Execution Layer)")
        write_to_inbox("kael", msg)

    elif "[REJECTED]" in msg.tags and msg.channel == "command_center":
        # Lisa rejects → Route back to Nyx
        print("   → Routing to Nyx (Intelligence Layer)")
        write_to_inbox("nyx", msg)

    elif "[EXECUTING]" in msg.tags and msg.channel == "execution":
        # Kael starts execution → Notify Lisa
        print("   → Notifying Lisa of execution start")
        write_to_inbox("lisa", msg)

    elif "[SUCCESS]" in msg.tags or "[FAIL]" in msg.tags:
        if msg.channel == "logs":
            # Kael reports result → Route to Lisa for decision
            print("   → Routing execution result to Lisa")
            write_to_inbox("lisa", msg)

    elif "[SCALE]" in msg.tags or "[OPTIMIZE]" in msg.tags or "[TERMINATE]" in msg.tags:
        if msg.channel == "command_center":
            # Lisa's final decision → Notify all
            print("   → Broadcasting final decision")
            write_to_inbox("kael", msg)
            write_to_inbox("nyx", msg)


def create_test_opportunity():
    """Create a test opportunity from Nyx"""
    msg = RoutedMessage(
        id=generate_id(),
        source="system",
        channel="research",
        author="nyx",
        content="""[OPPORTUNITY]
Name: Real Estate Lead Bot
Potential: $500-1000/month
Effort: 2 days setup, 1hr/week maintenance
Automation: 90%
First Step: Set up scraping for local listings
Confidence: High

Awaiting [APPROVED]/[REJECTED] from Lisa""",
        tags=["[OPPORTUNITY]"],
        timestamp=datetime.now().isoformat()
    )
    save_message_to_queue(msg)
    print("✅ Test opportunity created")


def create_test_decision(approved: bool = True):
    """Create a test decision from Lisa"""
    decision = "APPROVED" if approved else "REJECTED"
    msg = RoutedMessage(
        id=generate_id(),
        source="system",
        channel="command_center",
        author="lisa",
        content=f"""[{decision}]
Opportunity: Real Estate Lead Bot
Assigned to: @kael
Priority: High
Notes: Start immediately with full resources

@kael - Awaiting [EXECUTING] confirmation""",
        tags=[f"[{decision}]"],
        timestamp=datetime.now().isoformat()
    )
    save_message_to_queue(msg)
    print(f"✅ Test {decision} decision created")


def create_test_execution():
    """Create a test execution from Kael"""
    msg = RoutedMessage(
        id=generate_id(),
        source="system",
        channel="logs",
        author="kael",
        content="""[SUCCESS]
Task: Setup real estate scraper
Completed: 2026-04-05T02:30:00
Result: Scraper configured for 3 cities, output to CSV
Details:
- Python scraper with BeautifulSoup
- Scheduled to run every 6 hours
- Data exported to Google Sheets
- Error handling implemented

@lisa - Review for [SCALE]/[OPTIMIZE]/[TERMINATE]""",
        tags=["[SUCCESS]"],
        timestamp=datetime.now().isoformat()
    )
    save_message_to_queue(msg)
    print("✅ Test execution result created")


def run_test():
    """Run full workflow test"""
    print("=" * 60)
    print("Discord Workflow Test")
    print("=" * 60)

    print("\n1. Creating test opportunity from Nyx...")
    create_test_opportunity()

    print("\n2. Creating test approval from Lisa...")
    create_test_decision(approved=True)

    print("\n3. Creating test execution result from Kael...")
    create_test_execution()

    print("\n4. Processing queue...")
    process_queue()

    print("\n" + "=" * 60)
    print("Test complete - Check agent INBOX files")
    print("=" * 60)


def run_daemon(interval_seconds: int = 300):
    """Run as daemon, checking queue periodically"""
    print("=" * 60)
    print(f"Message Router Daemon (checking every {interval_seconds}s)")
    print("=" * 60)

    while True:
        try:
            process_queue()
            time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n👋 Daemon stopped")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            time.sleep(60)


def main():
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            run_test()
        elif sys.argv[1] == "--daemon":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
            run_daemon(interval)
        elif sys.argv[1] == "--once":
            process_queue()
        else:
            print("Usage: python3 message_router.py [--test|--daemon|--once]")
    else:
        # Default: process once
        process_queue()


if __name__ == "__main__":
    main()
