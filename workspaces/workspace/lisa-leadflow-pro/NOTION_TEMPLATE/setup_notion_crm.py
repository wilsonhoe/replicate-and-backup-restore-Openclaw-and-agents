"""
LeadFlow Pro - Notion CRM Template Setup
Creates the complete Notion database structure for real estate lead management
"""

import os
import json
import requests
from datetime import datetime, timedelta

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
PARENT_PAGE_ID = os.environ.get('NOTION_PARENT_PAGE_ID')

if not NOTION_API_KEY:
    raise ValueError("Please set NOTION_API_KEY environment variable")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def create_database(parent_page_id, title, properties):
    """Create a Notion database"""
    url = "https://api.notion.com/v1/databases"
    payload = {
        "parent": {"page_id": parent_page_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"Error creating {title}: {response.text}")
        return None


def create_page(parent_id, title, icon=None):
    """Create a Notion page"""
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": [{"text": {"content": title}}]
        }
    }
    if icon:
        payload["icon"] = icon
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["id"]
    return None


def create_leads_database(parent_id):
    """Create the main Leads database"""
    properties = {
        "Name": {"title": {}},
        "Lead Source": {"select": {"options": [
            {"name": "Website", "color": "blue"},
            {"name": "Scraper", "color": "green"},
            {"name": "Referral", "color": "yellow"},
            {"name": "Social Media", "color": "purple"},
            {"name": "Cold Outreach", "color": "red"},
            {"name": "Other", "color": "gray"}
        ]}},
        "Status": {"select": {"options": [
            {"name": "New", "color": "gray"},
            {"name": "Contacted", "color": "yellow"},
            {"name": "Qualified", "color": "blue"},
            {"name": "Proposal Sent", "color": "purple"},
            {"name": "Negotiating", "color": "orange"},
            {"name": "Closed Won", "color": "green"},
            {"name": "Closed Lost", "color": "red"},
            {"name": "Nurture", "color": "brown"}
        ]}},
        "Priority": {"select": {"options": [
            {"name": "Hot", "color": "red"},
            {"name": "Warm", "color": "yellow"},
            {"name": "Cold", "color": "blue"}
        ]}},
        "Phone": {"phone_number": {}},
        "Email": {"email": {}},
        "Property Interest": {"relation": {"database_id": "PLACEHOLDER_PROPERTIES"}},
        "Budget": {"number": {"format": "dollar"}},
        "Follow-up Date": {"date": {}},
        "Last Contact": {"date": {}},
        "Next Action": {"rich_text": {}},
        "Assigned Agent": {"people": {}},
        "Notes": {"rich_text": {}},
        "Created Date": {"created_time": {}},
        "Last Modified": {"last_edited_time": {}}
    }
    return create_database(parent_id, "📊 Leads Database", properties)


def create_properties_database(parent_id):
    """Create the Properties database"""
    properties = {
        "Name": {"title": {}},
        "Property Type": {"select": {"options": [
            {"name": "House", "color": "blue"},
            {"name": "Condo", "color": "green"},
            {"name": "Apartment", "color": "yellow"},
            {"name": "Commercial", "color": "purple"},
            {"name": "Land", "color": "brown"}
        ]}},
        "Status": {"select": {"options": [
            {"name": "Available", "color": "green"},
            {"name": "Under Contract", "color": "yellow"},
            {"name": "Sold", "color": "red"},
            {"name": "Off Market", "color": "gray"}
        ]}},
        "Price": {"number": {"format": "dollar"}},
        "Address": {"rich_text": {}},
        "City": {"select": {}},
        "State": {"select": {}},
        "Zip Code": {"rich_text": {}},
        "Bedrooms": {"number": {}},
        "Bathrooms": {"number": {}},
        "Square Feet": {"number": {}},
        "Listing URL": {"url": {}},
        "Lead Interest": {"relation": {"database_id": "PLACEHOLDER_LEADS"}},
        "Description": {"rich_text": {}},
        "Images": {"files": {}},
        "Created Date": {"created_time": {}}
    }
    return create_database(parent_id, "🏠 Properties Database", properties)


def create_follow_ups_database(parent_id):
    """Create the Follow-ups database"""
    properties = {
        "Name": {"title": {}},
        "Lead": {"relation": {"database_id": "PLACEHOLDER_LEADS"}},
        "Type": {"select": {"options": [
            {"name": "Phone Call", "color": "blue"},
            {"name": "Email", "color": "green"},
            {"name": "Text", "color": "yellow"},
            {"name": "Meeting", "color": "purple"},
            {"name": "Tour", "color": "orange"}
        ]}},
        "Status": {"select": {"options": [
            {"name": "Scheduled", "color": "yellow"},
            {"name": "Completed", "color": "green"},
            {"name": "No Show", "color": "red"},
            {"name": "Rescheduled", "color": "blue"}
        ]}},
        "Due Date": {"date": {}},
        "Completed Date": {"date": {}},
        "Notes": {"rich_text": {}},
        "Assigned To": {"people": {}},
        "Created Date": {"created_time": {}}
    }
    return create_database(parent_id, "📅 Follow-ups", properties)


def create_agent_dashboard(parent_id):
    """Create the main agent dashboard page"""
    dashboard_id = create_page(parent_id, "🎯 Agent Dashboard", {"emoji": "🎯"})
    if dashboard_id:
        # Add content to dashboard
        url = "https://api.notion.com/v1/blocks/children"
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"text": {"content": "LeadFlow Pro - Dashboard"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "Welcome to your LeadFlow Pro system! This dashboard gives you a quick overview of your leads and activities."}}]
                }
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
                    "rich_text": [{"text": {"content": "New Leads This Week: [Add linked database view]"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Hot Leads: [Add linked database view]"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Follow-ups Today: [Add linked database view]"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "🔗 Quick Links"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Add New Lead"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "View All Properties"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Today's Follow-ups"}}]
                }
            }
        ]
        requests.patch(f"{url}/{dashboard_id}/children", headers=headers, json={"children": blocks})
    return dashboard_id


def setup_complete_system():
    """Set up the complete LeadFlow Pro Notion system"""
    if not PARENT_PAGE_ID:
        print("Please set NOTION_PARENT_PAGE_ID environment variable")
        print("Create a parent page in Notion and copy its page ID")
        return

    print("🚀 Setting up LeadFlow Pro Notion System...")
    print("=" * 50)

    # Create main workspace page
    workspace_id = create_page(PARENT_PAGE_ID, "LeadFlow Pro - Real Estate CRM", {"emoji": "🏢"})
    if not workspace_id:
        print("❌ Failed to create workspace")
        return

    print(f"✅ Created workspace: {workspace_id}")

    # Create Agent Dashboard
    dashboard_id = create_agent_dashboard(workspace_id)
    print(f"✅ Created Agent Dashboard")

    # Create Properties Database
    properties_db_id = create_properties_database(workspace_id)
    print(f"✅ Created Properties Database: {properties_db_id}")

    # Create Leads Database (with relation to Properties)
    # Note: We'll need to update relations after all databases are created
    leads_properties = {
        "Name": {"title": {}},
        "Lead Source": {"select": {"options": [
            {"name": "Website", "color": "blue"},
            {"name": "Scraper", "color": "green"},
            {"name": "Referral", "color": "yellow"},
            {"name": "Social Media", "color": "purple"},
            {"name": "Cold Outreach", "color": "red"},
            {"name": "Other", "color": "gray"}
        ]}},
        "Status": {"select": {"options": [
            {"name": "New", "color": "gray"},
            {"name": "Contacted", "color": "yellow"},
            {"name": "Qualified", "color": "blue"},
            {"name": "Proposal Sent", "color": "purple"},
            {"name": "Negotiating", "color": "orange"},
            {"name": "Closed Won", "color": "green"},
            {"name": "Closed Lost", "color": "red"},
            {"name": "Nurture", "color": "brown"}
        ]}},
        "Priority": {"select": {"options": [
            {"name": "Hot", "color": "red"},
            {"name": "Warm", "color": "yellow"},
            {"name": "Cold", "color": "blue"}
        ]}},
        "Phone": {"phone_number": {}},
        "Email": {"email": {}},
        "Budget": {"number": {"format": "dollar"}},
        "Follow-up Date": {"date": {}},
        "Last Contact": {"date": {}},
        "Next Action": {"rich_text": {}},
        "Notes": {"rich_text": {}},
        "Created Date": {"created_time": {}},
        "Last Modified": {"last_edited_time": {}}
    }

    leads_db_id = create_database(workspace_id, "📊 Leads Database", leads_properties)
    print(f"✅ Created Leads Database: {leads_db_id}")

    # Create Follow-ups Database
    follow_ups_properties = {
        "Name": {"title": {}},
        "Type": {"select": {"options": [
            {"name": "Phone Call", "color": "blue"},
            {"name": "Email", "color": "green"},
            {"name": "Text", "color": "yellow"},
            {"name": "Meeting", "color": "purple"},
            {"name": "Tour", "color": "orange"}
        ]}},
        "Status": {"select": {"options": [
            {"name": "Scheduled", "color": "yellow"},
            {"name": "Completed", "color": "green"},
            {"name": "No Show", "color": "red"},
            {"name": "Rescheduled", "color": "blue"}
        ]}},
        "Due Date": {"date": {}},
        "Completed Date": {"date": {}},
        "Notes": {"rich_text": {}},
        "Created Date": {"created_time": {}}
    }

    follow_ups_db_id = create_database(workspace_id, "📅 Follow-ups", follow_ups_properties)
    print(f"✅ Created Follow-ups Database: {follow_ups_db_id}")

    print("\n" + "=" * 50)
    print("🎉 LeadFlow Pro Setup Complete!")
    print("=" * 50)
    print(f"\nWorkspace ID: {workspace_id}")
    print(f"Dashboard ID: {dashboard_id}")
    print(f"Leads DB ID: {leads_db_id}")
    print(f"Properties DB ID: {properties_db_id}")
    print(f"Follow-ups DB ID: {follow_ups_db_id}")
    print("\nNext steps:")
    print("1. Save these IDs for the scraper configuration")
    print("2. Add linked database views to your dashboard")
    print("3. Import your first leads!")


if __name__ == "__main__":
    setup_complete_system()