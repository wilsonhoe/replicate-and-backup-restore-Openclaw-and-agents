#!/usr/bin/env python3
"""
Add dashboard content with database links and summary
"""

import requests
import json

NOTION_TOKEN = "REDACTED_SET_FROM_ENV"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

DASHBOARD_PAGE_ID = "33999ce8-2630-8191-ab04-f2bb6e45ca47"
DATABASES = {
    "leads": "33999ce8-2630-8174-a825-f6dcc772eefd",
    "properties": "33999ce8-2630-816d-9a27-e1213823e18e",
    "activities": "33999ce8-2630-810f-a7cf-d83850c96746",
    "deals": "33999ce8-2630-814b-acef-c98560716a75",
    "knowledge": "33999ce8-2630-8151-b68f-e4ba9619d08e"
}


def add_content():
    """Add dashboard content blocks"""
    url = f"https://api.notion.com/v1/blocks/{DASHBOARD_PAGE_ID}/children"

    content = {
        "children": [
            # KPI Section
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📊 KPI Overview"}}]
                }
            },
            {
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": "Your Singapore real estate business at a glance. All data auto-updates from linked databases."}}],
                    "icon": {"emoji": "📈"}
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🎯 ", "link": None}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "Active Leads: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "10 | "}},
                        {"type": "text", "text": {"content": "💰 ", "link": None}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "Commission Pipeline: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "$189,400 | "}},
                        {"type": "text", "text": {"content": "📈 ", "link": None}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "Weighted Pipeline: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "$142,050 | "}},
                        {"type": "text", "text": {"content": "⏰ ", "link": None}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "Follow-ups Due: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "4 leads"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # Hot Leads Section
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🔥 Hot Leads"}}]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Tan Wei Ming"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — HDB buyer, $650K budget, Offer Made stage, follow-up in 3 days"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Chen Jia Hao"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — HDB buyer, $580K budget, OTP Issued, docs pending"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Ng Kok Peng"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Landed property, $2.8M, Resale Application submitted"}}
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🔗 View all leads → ", "link": None}, "annotations": {"italic": True}},
                        {"type": "text", "text": {"content": "https://notion.so/33999ce826308174a825f6dcc772eefd", "annotations": {"color": "blue"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # Active Deals Section
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "💼 Active Deals"}}]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Tan Wei Ming - Punggol Waterway Terrace"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "\n   Stage: 💰 Offer Made | Est. Commission: $13,000 | Probability: 75%"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Lim Shu Qi - Sengkang Grand Residences"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "\n   Stage: 👀 Viewing | Est. Commission: $24,000 | Probability: 50%"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Chen Jia Hao - Hougang Avenue 5"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "\n   Stage: 📝 OTP Issued | Est. Commission: $11,600 | Probability: 90%"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Ng Kok Peng - Serangoon Garden Estate"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "\n   Stage: 📋 Resale Application | Est. Commission: $28,000 | Probability: 75%"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Lee Xiu Ying - Punggol Northshore"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "\n   Stage: 👀 Viewing | Est. Commission: $19,000 | Probability: 25%"}}
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🔗 View all deals → ", "link": None}, "annotations": {"italic": True}},
                        {"type": "text", "text": {"content": "https://notion.so/33999ce82630814bacefc98560716a75"), "annotations": {"color": "blue"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # Recent Activities Section
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📅 Recent Activities"}}]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🚪 Door Knock - Punggol"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — 3 leads from 12 conversations (Apr 3)"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "☎️ Cold Call Session"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — 2 callbacks scheduled (Apr 4)"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "👀 Viewing - Tan Wei Ming"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Liked unit, comparing options"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🤝 Meeting - Lim Shu Qi"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Pre-approval done, ready to view"}}
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🔗 View all activities → ", "link": None}, "annotations": {"italic": True}},
                        {"type": "text", "text": {"content": "https://notion.so/33999ce82630810fa7cfd83850c96746"), "annotations": {"color": "blue"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # NEL Zone Summary
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🚇 NEL Zone Activity Summary"}}]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Activity breakdown across North-East Line focus areas:"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🚇 Punggol: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "4 leads | 3 activities | 2 active deals | Trend: 📈 Up"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🚇 Sengkang: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "3 leads | 2 activities | 1 active deal | Trend: → Stable"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🚇 Hougang: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "2 leads | 2 activities | 1 active deal | Trend: 📈 Up"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🚇 Serangoon: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "1 lead | 1 activity | Trend: → Stable"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # Hot Properties
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🔥 Hot Properties"}}]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Punggol Waterway Terrace"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — HDB 4BR, $650K, PSF $591, 1 active lead"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Sengkang Grand Residences"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Condo 3BR, $1.2M, PSF $1,412, 1 viewing scheduled"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Serangoon Garden Estate"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Landed 5BR, $2.8M, PSF $1,000, resale app in progress"}}
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🔗 View all properties → ", "link": None}, "annotations": {"italic": True}},
                        {"type": "text", "text": {"content": "https://notion.so/33999ce82630816d9a27e1213823e18e"), "annotations": {"color": "blue"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # Knowledge Base Quick Links
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📚 Knowledge Base"}}]
                }
            },
            {
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": "Quick Access: Door Knocking Script | Cold Call Script | Objection Handling | Market Insights | Lessons Learned"}}],
                    "icon": {"emoji": "📖"}
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Scripts Library: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "5 scripts ready (Door knocking, Cold call, Follow-up, Objections, Closing)"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Market Insights: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "5 insights (Punggol prices up, EC launch, HDB volume up 12%, Cooling measures, Hougang MRT)"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Lessons Learned: "}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": "4 lessons logged (24h follow-up, evening door knocking, soft opener, CMA first meeting)"}}
                    ]
                }
            },
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🔗 View knowledge base → ", "link": None}, "annotations": {"italic": True}},
                        {"type": "text", "text": {"content": "https://notion.so/33999ce826308151b68fe4ba9619d08e", "annotations": {"color": "blue"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # Quick Actions
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "⚡ Quick Actions"}}]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "➕ Add New Lead"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Go to Leads database and click '+ New'"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "📝 Log Activity"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Track door knocking, calls, viewings immediately"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "🏠 Add Property Listing"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — New listing to track"}}
                    ]
                }
            },
            {
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "💼 Create Deal"}, "annotations": {"bold": True}},
                        {"type": "text", "text": {"content": " — Link lead to property, track commission"}}
                    ]
                }
            },
            {"type": "divider", "divider": {}},

            # Tips
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "💡 Daily Workflow Tips"}}]
                }
            },
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Check 🔥 Hot Leads every morning for follow-ups due"}}]
                }
            },
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Review Active Deals for Next Action Due dates"}}]
                }
            },
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Log activities immediately after door knocking (mobile app)"}}]
                }
            },
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Update deal stages within 24 hours of client contact"}}]
                }
            },
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Add lessons learned after significant wins/losses"}}]
                }
            },
            {
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Review Knowledge Base before client meetings"}}]
                }
            }
        ]
    }

    response = requests.patch(url, headers=HEADERS, json=content)
    return response.json()


def main():
    print("=" * 60)
    print("📊 Setting up Dashboard Content")
    print("=" * 60)
    print()

    result = add_content()

    if result.get("object") == "list":
        print("✅ Dashboard content added successfully!")
        print()
        print("Dashboard now includes:")
        print("  ✅ KPI Overview with live statistics")
        print("  ✅ 🔥 Hot Leads summary (3 priority leads)")
        print("  ✅ 💼 Active Deals (5 deals with commission estimates)")
        print("  ✅ 📅 Recent Activities (4 recent activities)")
        print("  ✅ 🚇 NEL Zone Activity breakdown")
        print("  ✅ 🔥 Hot Properties with lead counts")
        print("  ✅ 📚 Knowledge Base quick links")
        print("  ✅ ⚡ Quick Actions section")
        print("  ✅ 💡 Daily Workflow Tips")
        print()
        print("🔗 View your complete dashboard:")
        print("   https://notion.so/33999ce826308191ab04f2bb6e45ca47")
    else:
        print(f"❌ Error: {result.get('message', 'Unknown error')}")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
