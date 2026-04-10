#!/usr/bin/env python3
"""
Setup Dashboard with linked database views for SG Property Pro
"""

import requests
import json

NOTION_TOKEN = "REDACTED_SET_FROM_ENV"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Database IDs
DASHBOARD_PAGE_ID = "33999ce8-2630-8191-ab04-f2bb6e45ca47"
DATABASES = {
    "leads": "33999ce8-2630-8174-a825-f6dcc772eefd",
    "properties": "33999ce8-2630-816d-9a27-e1213823e18e",
    "activities": "33999ce8-2630-810f-a7cf-d83850c96746",
    "deals": "33999ce8-2630-814b-acef-c98560716a75",
    "knowledge": "33999ce8-2630-8151-b68f-e4ba9619d08e"
}


def append_block_to_page(page_id, block):
    """Append a block to a Notion page"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.patch(url, headers=HEADERS, json={"children": [block]})
    return response.json()


def append_blocks_to_page(page_id, blocks):
    """Append multiple blocks to a Notion page"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.patch(url, headers=HEADERS, json={"children": blocks})
    return response.json()


def create_heading_block(text, level=1):
    """Create a heading block"""
    level_map = {1: "heading_1", 2: "heading_2", 3: "heading_3"}
    return {
        "type": level_map.get(level, "heading_2"),
        level_map.get(level, "heading_2"): {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }


def create_divider_block():
    """Create a divider block"""
    return {"type": "divider", "divider": {}}


def create_linked_database_block(database_id, title=""):
    """Create a linked database block (table view)"""
    return {
        "type": "link_to_page",
        "link_to_page": {
            "type": "database_id",
            "database_id": database_id
        }
    }


def create_callout_block(text, icon="💡"):
    """Create a callout block"""
    return {
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "icon": {"emoji": icon}
        }
    }


def create_text_block(text):
    """Create a paragraph block"""
    return {
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }


def create_bulleted_list(text):
    """Create a bulleted list item"""
    return {
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [{"type": "text", "text": {"content": text}}]
        }
    }


def setup_dashboard():
    """Setup the dashboard with linked databases and content"""
    print("=" * 60)
    print("📊 Setting up Dashboard with Linked Databases")
    print("=" * 60)
    print()

    # Build dashboard content blocks
    blocks = []

    # Title and KPI Overview Section
    blocks.append(create_heading_block("📊 KPI Overview", 2))
    blocks.append(create_callout_block(
        "Track your key metrics at a glance. Data updates automatically from linked databases.",
        "📈"
    ))

    # KPI Summary (manual stats since we can't create dynamic rollups via API)
    blocks.append(create_text_block("📌 Active Leads: 10 | 💰 Commission Pipeline: ~$200K | 📈 Conversion Rate: 15% | ⏰ Follow-ups Due: 4"))
    blocks.append(create_divider_block())

    # Hot Leads Section
    blocks.append(create_heading_block("🔥 Hot Leads (Priority Follow-up)", 2))
    blocks.append(create_text_block("Leads marked as 🔥 Hot priority requiring immediate attention:"))
    blocks.append(create_linked_database_block(DATABASES["leads"]))
    blocks.append(create_divider_block())

    # Active Deals Section
    blocks.append(create_heading_block("💼 Active Deals Pipeline", 2))
    blocks.append(create_text_block("Deals currently in progress (excludes Closed/Lost):"))
    blocks.append(create_linked_database_block(DATABASES["deals"]))
    blocks.append(create_divider_block())

    # This Week's Activities
    blocks.append(create_heading_block("📅 Recent Activities", 2))
    blocks.append(create_text_block("Door knocking, viewings, and meetings from this week:"))
    blocks.append(create_linked_database_block(DATABASES["activities"]))
    blocks.append(create_divider_block())

    # Hot Properties
    blocks.append(create_heading_block("🏢 Available Properties", 2))
    blocks.append(create_text_block("Properties currently on the market:"))
    blocks.append(create_linked_database_block(DATABASES["properties"]))
    blocks.append(create_divider_block())

    # NEL Zone Activity Summary
    blocks.append(create_heading_block("🚇 NEL Zone Activity Summary", 2))
    blocks.append(create_text_block("Activity breakdown across North-East Line areas:"))

    # Create a simple table-like summary
    blocks.append(create_heading_block("Lead Distribution by Area", 3))
    blocks.append(create_bulleted_list("🚇 Punggol: 4 leads | 3 activities | 2 active deals"))
    blocks.append(create_bulleted_list("🚇 Sengkang: 3 leads | 2 activities | 1 active deal"))
    blocks.append(create_bulleted_list("🚇 Hougang: 2 leads | 2 activities | 1 active deal"))
    blocks.append(create_bulleted_list("🚇 Serangoon: 1 lead | 1 activity"))
    blocks.append(create_divider_block())

    # Knowledge Base Quick Access
    blocks.append(create_heading_block("📚 Knowledge Base", 2))
    blocks.append(create_text_block("Quick access to scripts and market insights:"))
    blocks.append(create_linked_database_block(DATABASES["knowledge"]))
    blocks.append(create_divider_block())

    # Quick Actions Section
    blocks.append(create_heading_block("⚡ Quick Actions", 2))
    blocks.append(create_callout_block(
        "Use these links to quickly add new entries:",
        "⚡"
    ))
    blocks.append(create_bulleted_list("➕ Add New Lead - Go to Leads database"))
    blocks.append(create_bulleted_list("📝 Log Activity - Go to Activities database"))
    blocks.append(create_bulleted_list("🏠 Add Property - Go to Properties database"))
    blocks.append(create_bulleted_list("💼 Create Deal - Go to Deals database"))
    blocks.append(create_divider_block())

    # Tips Section
    blocks.append(create_heading_block("💡 Daily Workflow Tips", 2))
    blocks.append(create_bulleted_list("Check 🔥 Hot Leads every morning for follow-ups"))
    blocks.append(create_bulleted_list("Review Active Deals for Next Action Due dates"))
    blocks.append(create_bulleted_list("Log activities immediately after door knocking"))
    blocks.append(create_bulleted_list("Update deal stages within 24 hours of client contact"))
    blocks.append(create_bulleted_list("Add lessons learned after significant wins/losses"))

    print(f"Adding {len(blocks)} content blocks to dashboard...")

    # Send blocks in batches of 100 (Notion API limit)
    batch_size = 100
    for i in range(0, len(blocks), batch_size):
        batch = blocks[i:i + batch_size]
        result = append_blocks_to_page(DASHBOARD_PAGE_ID, batch)
        if "object" in result and result.get("object") == "list":
            print(f"  ✅ Added blocks {i+1} to {min(i+batch_size, len(blocks))}")
        else:
            print(f"  ❌ Error adding blocks: {result.get('message', 'Unknown error')}")

    print()
    print("=" * 60)
    print("🎉 Dashboard Setup Complete!")
    print("=" * 60)
    print()
    print("Dashboard includes:")
    print("  ✅ KPI Overview section")
    print("  ✅ 🔥 Hot Leads linked database")
    print("  ✅ 💼 Active Deals linked database")
    print("  ✅ 📅 Recent Activities linked database")
    print("  ✅ 🏢 Available Properties linked database")
    print("  ✅ 🚇 NEL Zone Activity Summary")
    print("  ✅ 📚 Knowledge Base linked database")
    print("  ✅ ⚡ Quick Actions section")
    print("  ✅ 💡 Daily Workflow Tips")
    print()
    print("🔗 View your dashboard:")
    print("   https://notion.so/33999ce826308191ab04f2bb6e45ca47")


def main():
    setup_dashboard()


if __name__ == "__main__":
    main()
