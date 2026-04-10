#!/usr/bin/env python3
"""
Singapore Real Estate Notion System Setup
Creates complete template system via Notion API
"""

import requests
import json
import os
import sys

NOTION_TOKEN = "REDACTED_SET_FROM_ENV"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Emoji mapping for visual consistency
ICONS = {
    "home": {"emoji": "🏠"},
    "dashboard": {"emoji": "📊"},
    "leads": {"emoji": "👥"},
    "properties": {"emoji": "🏢"},
    "activities": {"emoji": "📅"},
    "deals": {"emoji": "💼"},
    "knowledge": {"emoji": "📚"},
    "scripts": {"emoji": "📝"},
    "insights": {"emoji": "💡"},
    "lessons": {"emoji": "🎯"},
    "nel": {"emoji": "🚇"},
    "settings": {"emoji": "⚙️"}
}


def create_page(title, parent_id, icon=None, is_database=False, properties=None):
    """Create a Notion page or database"""
    url = "https://api.notion.com/v1/pages"

    data = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"text": {"content": title}}]}
        }
    }

    if icon:
        data["icon"] = icon

    if is_database and properties:
        data["properties"] = properties
        # For database creation, we need different endpoint
        url = "https://api.notion.com/v1/databases"
        data = {
            "parent": {"page_id": parent_id},
            "title": [{"text": {"content": title}}],
            "properties": properties
        }
        if icon:
            data["icon"] = icon

    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()


def create_database(parent_id, title, icon, properties):
    """Create a Notion database"""
    url = "https://api.notion.com/v1/databases"

    data = {
        "parent": {"page_id": parent_id},
        "title": [{"text": {"content": title}}],
        "properties": properties
    }

    if icon:
        data["icon"] = icon

    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()


def get_workspace_pages():
    """Get first available page to use as parent"""
    url = "https://api.notion.com/v1/search"
    data = {
        "query": "",
        "filter": {"value": "page", "property": "object"},
        "page_size": 10
    }

    response = requests.post(url, headers=HEADERS, json=data)
    results = response.json().get("results", [])

    # Return first page that isn't a database
    for page in results:
        if page.get("object") == "page":
            return page["id"]

    return None


def setup_leads_database(parent_id):
    """Create Leads database"""
    properties = {
        "Name": {"title": {}},
        "Contact": {"phone_number": {}},
        "Email": {"email": {}},
        "Source": {
            "select": {
                "options": [
                    {"name": "🚪 Door Knocking", "color": "brown"},
                    {"name": "👨‍👩‍👧 Referral", "color": "green"},
                    {"name": "💻 Online", "color": "blue"},
                    {"name": "📱 Social Media", "color": "purple"},
                    {"name": "🏢 Walk-in", "color": "yellow"}
                ]
            }
        },
        "Property Interest": {
            "multi_select": {
                "options": [
                    {"name": "🏢 HDB", "color": "blue"},
                    {"name": "🏠 Condo", "color": "green"},
                    {"name": "🏡 Landed", "color": "orange"},
                    {"name": "🏘️ EC", "color": "purple"}
                ]
            }
        },
        "Budget Range": {
            "select": {
                "options": [
                    {"name": "<$500K", "color": "gray"},
                    {"name": "$500K-$800K", "color": "green"},
                    {"name": "$800K-$1.2M", "color": "yellow"},
                    {"name": "$1.2M-$2M", "color": "orange"},
                    {"name": ">$2M", "color": "red"}
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "🆕 New", "color": "gray"},
                    {"name": "📞 Contacted", "color": "blue"},
                    {"name": "👀 Viewing Scheduled", "color": "yellow"},
                    {"name": "💰 Offer Made", "color": "orange"},
                    {"name": "✅ Closed", "color": "green"},
                    {"name": "❌ Lost", "color": "red"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "🔥 Hot", "color": "red"},
                    {"name": "⚡ Warm", "color": "yellow"},
                    {"name": "❄️ Cold", "color": "blue"}
                ]
            }
        },
        "Last Contact": {"date": {}},
        "Next Follow-up": {"date": {}},
        "Notes": {"rich_text": {}}
    }

    return create_database(parent_id, "👥 Leads Database", ICONS["leads"], properties)


def setup_properties_database(parent_id):
    """Create Properties database"""
    properties = {
        "Property Name": {"title": {}},
        "Address": {"rich_text": {}},
        "Type": {
            "select": {
                "options": [
                    {"name": "🏢 HDB", "color": "blue"},
                    {"name": "🏠 Condo", "color": "green"},
                    {"name": "🏡 Landed", "color": "orange"},
                    {"name": "🏘️ EC", "color": "purple"}
                ]
            }
        },
        "District": {
            "select": {
                "options": [
                    {"name": f"D{i}", "color": "gray"} for i in range(1, 29)
                ]
            }
        },
        "Area": {
            "select": {
                "options": [
                    {"name": "🚇 Punggol", "color": "purple"},
                    {"name": "🚇 Sengkang", "color": "pink"},
                    {"name": "🚇 Hougang", "color": "yellow"},
                    {"name": "🚇 Serangoon", "color": "orange"},
                    {"name": "Other NEL", "color": "gray"},
                    {"name": "CBD", "color": "blue"},
                    {"name": "Other", "color": "brown"}
                ]
            }
        },
        "Price": {"number": {"format": "dollar"}},
        "Size (sqft)": {"number": {"format": "number"}},
        "Bedrooms": {
            "select": {
                "options": [
                    {"name": "1", "color": "gray"},
                    {"name": "2", "color": "blue"},
                    {"name": "3", "color": "green"},
                    {"name": "4", "color": "yellow"},
                    {"name": "5+", "color": "red"}
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    {"name": "✅ Available", "color": "green"},
                    {"name": "📝 Under Offer", "color": "yellow"},
                    {"name": "❌ Sold", "color": "red"},
                    {"name": "🔒 Off Market", "color": "gray"}
                ]
            }
        },
        "Listing Date": {"date": {}},
        "Seller Contact": {"phone_number": {}},
        "Notes": {"rich_text": {}}
    }

    return create_database(parent_id, "🏢 Properties Database", ICONS["properties"], properties)


def setup_activities_database(parent_id):
    """Create Activities database"""
    properties = {
        "Activity Name": {"title": {}},
        "Date": {"date": {}},
        "Type": {
            "select": {
                "options": [
                    {"name": "🚪 Door Knocking", "color": "brown"},
                    {"name": "☎️ Cold Call", "color": "blue"},
                    {"name": "📧 Follow-up", "color": "purple"},
                    {"name": "👀 Viewing", "color": "green"},
                    {"name": "🤝 Meeting", "color": "yellow"},
                    {"name": "💻 Research", "color": "gray"},
                    {"name": "📝 Admin", "color": "orange"}
                ]
            }
        },
        "Area": {
            "select": {
                "options": [
                    {"name": "🚇 Punggol", "color": "purple"},
                    {"name": "🚇 Sengkang", "color": "pink"},
                    {"name": "🚇 Hougang", "color": "yellow"},
                    {"name": "🚇 Serangoon", "color": "orange"},
                    {"name": "Other NEL", "color": "gray"},
                    {"name": "CBD", "color": "blue"},
                    {"name": "Other", "color": "brown"}
                ]
            }
        },
        "Outcome": {
            "select": {
                "options": [
                    {"name": "✅ Lead Generated", "color": "green"},
                    {"name": "📞 Callback Scheduled", "color": "blue"},
                    {"name": "❌ No Answer", "color": "gray"},
                    {"name": "🚫 Not Interested", "color": "red"},
                    {"name": "📊 Market Intel", "color": "yellow"},
                    {"name": "✅ Completed", "color": "green"}
                ]
            }
        },
        "Leads Generated": {"number": {"format": "number"}},
        "Conversations": {"number": {"format": "number"}},
        "Duration (mins)": {"number": {"format": "number"}},
        "Notes": {"rich_text": {}},
        "Added to KB": {"checkbox": {}}
    }

    return create_database(parent_id, "📅 Activities Database", ICONS["activities"], properties)


def setup_deals_database(parent_id):
    """Create Deals Pipeline database"""
    properties = {
        "Deal Name": {"title": {}},
        "Stage": {
            "select": {
                "options": [
                    {"name": "🆕 New", "color": "gray"},
                    {"name": "👀 Viewing", "color": "blue"},
                    {"name": "💰 Offer Made", "color": "yellow"},
                    {"name": "📝 OTP Issued", "color": "orange"},
                    {"name": "✅ OTP Exercised", "color": "green"},
                    {"name": "📋 Resale Application", "color": "purple"},
                    {"name": "🏛️ HDB Acceptance", "color": "blue"},
                    {"name": "🔨 Legal Completion", "color": "yellow"},
                    {"name": "✅ Closed", "color": "green"},
                    {"name": "❌ Lost", "color": "red"}
                ]
            }
        },
        "Deal Type": {
            "select": {
                "options": [
                    {"name": "🏢 HDB → HDB", "color": "blue"},
                    {"name": "🏢 HDB → 🏠 Private", "color": "purple"},
                    {"name": "🏠 Private → 🏠 Private", "color": "green"},
                    {"name": "🏠 Private → 🏢 HDB", "color": "orange"}
                ]
            }
        },
        "Price": {"number": {"format": "dollar"}},
        "Commission %": {"number": {"format": "percent"}},
        "Expected Close": {"date": {}},
        "OTP Date": {"date": {}},
        "OTP Exercise Date": {"date": {}},
        "Resale Application Date": {"date": {}},
        "HDB Acceptance Date": {"date": {}},
        "Legal Completion Date": {"date": {}},
        "Probability": {
            "select": {
                "options": [
                    {"name": "10%", "color": "gray"},
                    {"name": "25%", "color": "red"},
                    {"name": "50%", "color": "yellow"},
                    {"name": "75%", "color": "blue"},
                    {"name": "90%", "color": "green"},
                    {"name": "100%", "color": "green"}
                ]
            }
        },
        "Next Action": {"rich_text": {}},
        "Next Action Due": {"date": {}},
        "Notes": {"rich_text": {}}
    }

    return create_database(parent_id, "💼 Deals Pipeline", ICONS["deals"], properties)


def setup_knowledge_base(parent_id):
    """Create Knowledge Base with sub-databases"""
    # Main KB page
    kb_page = create_page("📚 Knowledge Base", parent_id, ICONS["knowledge"])
    kb_id = kb_page.get("id")

    if not kb_id:
        print("Failed to create Knowledge Base page")
        return None

    # Scripts Library
    scripts_props = {
        "Script Name": {"title": {}},
        "Type": {
            "select": {
                "options": [
                    {"name": "🚪 Door Knocking", "color": "brown"},
                    {"name": "☎️ Cold Call", "color": "blue"},
                    {"name": "📧 Follow-up", "color": "purple"},
                    {"name": "❌ Objection Handling", "color": "red"},
                    {"name": "🤝 Closing", "color": "green"},
                    {"name": "📊 CMA Presentation", "color": "yellow"}
                ]
            }
        },
        "Best For": {
            "multi_select": {
                "options": [
                    {"name": "HDB", "color": "blue"},
                    {"name": "Condo", "color": "green"},
                    {"name": "Landed", "color": "orange"},
                    {"name": "First-time buyer", "color": "yellow"},
                    {"name": "Investor", "color": "purple"}
                ]
            }
        },
        "Content": {"rich_text": {}},
        "Success Rate": {
            "select": {
                "options": [
                    {"name": "High", "color": "green"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "red"},
                    {"name": "Untested", "color": "gray"}
                ]
            }
        },
        "Last Used": {"date": {}}
    }

    scripts_db = create_database(kb_id, "📝 Scripts Library", ICONS["scripts"], scripts_props)

    # Market Insights
    insights_props = {
        "Insight": {"title": {}},
        "Area": {
            "select": {
                "options": [
                    {"name": "🚇 Punggol", "color": "purple"},
                    {"name": "🚇 Sengkang", "color": "pink"},
                    {"name": "🚇 Hougang", "color": "yellow"},
                    {"name": "🚇 Serangoon", "color": "orange"},
                    {"name": "Other", "color": "gray"}
                ]
            }
        },
        "Type": {
            "select": {
                "options": [
                    {"name": "📈 Price Trend", "color": "green"},
                    {"name": "🏗️ New Launch", "color": "blue"},
                    {"name": "📊 Transaction Volume", "color": "yellow"},
                    {"name": "📝 Policy Change", "color": "red"}
                ]
            }
        },
        "Date": {"date": {}},
        "Source": {"rich_text": {}},
        "Impact": {
            "select": {
                "options": [
                    {"name": "High", "color": "red"},
                    {"name": "Medium", "color": "yellow"},
                    {"name": "Low", "color": "blue"}
                ]
            }
        }
    }

    insights_db = create_database(kb_id, "💡 Market Insights", ICONS["insights"], insights_props)

    # Lessons Learned
    lessons_props = {
        "Lesson": {"title": {}},
        "Context": {
            "select": {
                "options": [
                    {"name": "✅ What Worked", "color": "green"},
                    {"name": "❌ What Didn't", "color": "red"},
                    {"name": "💡 Insight", "color": "yellow"},
                    {"name": "🔧 System Improvement", "color": "blue"}
                ]
            }
        },
        "Date": {"date": {}},
        "Action Item": {"rich_text": {}}
    }

    lessons_db = create_database(kb_id, "🎯 Lessons Learned", ICONS["lessons"], lessons_props)

    return {
        "kb_page": kb_page,
        "scripts": scripts_db,
        "insights": insights_db,
        "lessons": lessons_db
    }


def setup_nel_tracker(parent_id):
    """Create NEL Zone Tracker page"""
    return create_page("🚇 NEL Zone Tracker", parent_id, ICONS["nel"])


def setup_dashboard(parent_id):
    """Create main dashboard page"""
    dashboard = create_page("📊 Dashboard", parent_id, ICONS["dashboard"])

    if dashboard.get("id"):
        # Add content to dashboard with linked database views
        content = """
# 🏠 SG Property Pro — Agent Command Center

## 📊 KPI Overview
*Track your key metrics at a glance*

→ [[Insert linked view of Leads]]
→ [[Insert linked view of Deals]]
→ [[Insert linked view of Activities]]

---

## 🔥 Quick Actions
- [🆕 New Lead](link to Leads)
- [📅 Log Activity](link to Activities)
- [🏢 Add Property](link to Properties)
- [💼 New Deal](link to Deals)

---

## 📅 This Week's Focus
→ [[Insert filtered view: Activities this week]]

## 🔥 Hot Leads
→ [[Insert filtered view: Leads with Priority = Hot]]

## 💼 Active Deals
→ [[Insert filtered view: Deals not Closed/Lost]]

---

## 🚇 NEL Zone Tracker
- 🚇 Punggol
- 🚇 Sengkang
- 🚇 Hougang
- 🚇 Serangoon

---

**Last updated:** Today
        """

        # Note: Adding content requires block API calls
        # For now, page structure is created
        pass

    return dashboard


def main():
    """Main setup function"""
    print("🏠 Singapore Real Estate Notion System Setup")
    print("=" * 50)

    # Get parent page
    parent_id = get_workspace_pages()
    if not parent_id:
        print("❌ No workspace page found. Please create a page in Notion first.")
        sys.exit(1)

    print(f"✅ Found workspace page: {parent_id}")
    print()

    # Create main system page
    print("Creating main system page...")
    main_page = create_page("🏠 SG Property Pro", parent_id, ICONS["home"])
    main_id = main_page.get("id")

    if not main_id:
        print("❌ Failed to create main page")
        print(json.dumps(main_page, indent=2))
        sys.exit(1)

    print(f"✅ Main page created: {main_id}")
    print()

    # Setup components
    components = []

    print("📊 Creating Dashboard...")
    dashboard = setup_dashboard(main_id)
    components.append(("Dashboard", dashboard))
    print("✅ Dashboard created")
    print()

    print("👥 Creating Leads Database...")
    leads = setup_leads_database(main_id)
    components.append(("Leads", leads))
    print(f"✅ Leads Database: {leads.get('id', 'FAILED')}")
    print()

    print("🏢 Creating Properties Database...")
    properties = setup_properties_database(main_id)
    components.append(("Properties", properties))
    print(f"✅ Properties Database: {properties.get('id', 'FAILED')}")
    print()

    print("📅 Creating Activities Database...")
    activities = setup_activities_database(main_id)
    components.append(("Activities", activities))
    print(f"✅ Activities Database: {activities.get('id', 'FAILED')}")
    print()

    print("💼 Creating Deals Pipeline...")
    deals = setup_deals_database(main_id)
    components.append(("Deals", deals))
    print(f"✅ Deals Pipeline: {deals.get('id', 'FAILED')}")
    print()

    print("📚 Creating Knowledge Base...")
    kb = setup_knowledge_base(main_id)
    components.append(("Knowledge Base", kb))
    print(f"✅ Knowledge Base: {kb.get('kb_page', {}).get('id', 'FAILED') if kb else 'FAILED'}")
    print()

    print("🚇 Creating NEL Zone Tracker...")
    nel = setup_nel_tracker(main_id)
    components.append(("NEL Tracker", nel))
    print(f"✅ NEL Tracker: {nel.get('id', 'FAILED')}")
    print()

    # Summary
    print("=" * 50)
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    print()
    print("📋 Created Components:")
    for name, result in components:
        status = "✅" if result and (result.get('id') or (isinstance(result, dict) and result.get('kb_page'))) else "❌"
        print(f"  {status} {name}")
    print()
    print(f"🔗 Main Page URL: https://notion.so/{main_id.replace('-', '')}")
    print()
    print("⚠️  Next Steps:")
    print("  1. Open the main page in Notion")
    print("  2. Set up database relations manually (Lead ↔ Property ↔ Deal)")
    print("  3. Create filtered views in each database")
    print("  4. Add formulas for rollups (PSF, Commission, etc.)")
    print("  5. Customize the dashboard with linked database views")


if __name__ == "__main__":
    main()
