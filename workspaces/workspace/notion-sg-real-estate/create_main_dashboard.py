#!/usr/bin/env python3
"""
Create Main Dashboard for Real Estate Systems
Links to Door Knocking Mastery and other systems
"""

import requests

API_KEY = "REDACTED_SET_FROM_ENV"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

BASE_URL = "https://api.notion.com/v1"

def create_dashboard():
    """Create the main dashboard page"""
    print("Creating Main Real Estate Dashboard...")

    # Use the first accessible page as parent (SG Property Pro workspace)
    response = requests.post(f"{BASE_URL}/search", headers=HEADERS, json={"page_size": 1})
    if response.status_code != 200:
        print("Failed to search workspace")
        return None

    results = response.json().get("results", [])
    if not results:
        print("No accessible pages found")
        return None

    # Create dashboard as a standalone top-level page
    data = {
        "parent": {"page_id": results[0]["id"]},
        "properties": {
            "title": {
                "title": [{"text": {"content": "🏠 Singapore Real Estate Command Center"}}]
            }
        },
        "icon": {"emoji": "🏠"},
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"text": {"content": "Singapore Real Estate Command Center"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "Your complete real estate management hub. Access all systems from one place."}}]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "🎯 Active Systems"}}]
                }
            },
            {
                "object": "block",
                "type": "link_to_page",
                "link_to_page": {
                    "type": "page_id",
                    "page_id": "33999ce8-2630-813e-b316-f79788a49622"  # Door Knocking
                }
            },
            {
                "object": "block",
                "type": "link_to_page",
                "link_to_page": {
                    "type": "page_id",
                    "page_id": "33999ce8-2630-8191-ab04-f2bb6e45ca47"  # SG Property Pro
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "📊 Quick Stats"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Door Knocking Sessions: 10+ logged"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Active Leads: 15+ tracked"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Sales Scripts: 11+ optimized"}}]
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "🚀 Quick Actions"}}]
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"text": {"content": "Check today's follow-ups"}}],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"text": {"content": "Review hot leads"}}],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"text": {"content": "Practice scripts (10 min)"}}],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"text": {"content": "Plan today's door knocking route"}}],
                    "checked": False
                }
            },
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": "💡 Tip: Use the Door Knocking system for field execution and SG Property Pro for CRM/deal tracking. Both systems work together!"}}],
                    "icon": {"emoji": "💡"}
                }
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=data)
    if response.status_code == 200:
        page = response.json()
        print(f"✓ Created Main Dashboard: {page['url']}")
        return page["id"]
    else:
        print(f"✗ Failed to create dashboard: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("CREATING MAIN DASHBOARD")
    print("=" * 60)
    dashboard_id = create_dashboard()
    if dashboard_id:
        print(f"\n✓ Dashboard created successfully!")
        print(f"The Door Knocking system remains standalone as requested.")
    else:
        print("\n✗ Failed to create dashboard")
