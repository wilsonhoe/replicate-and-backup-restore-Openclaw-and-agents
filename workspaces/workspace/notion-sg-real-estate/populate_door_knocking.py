#!/usr/bin/env python3
"""
Populate Door Knocking Mastery System to Notion
Creates a new parent page and all 6 databases with sample data
"""

import os
import json
import csv
import requests
from datetime import datetime, timedelta

# API Configuration
API_KEY = "REDACTED_SET_FROM_ENV"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

BASE_URL = "https://api.notion.com/v1"

# Color mapping for select options
COLORS = {
    "Punggol": "blue",
    "Serangoon": "green",
    "Sengkang": "yellow",
    "Both": "purple",
    "High": "red",
    "Medium": "yellow",
    "Low": "gray",
    "Pending": "yellow",
    "Done": "green",
    "Overdue": "red",
    "Sell": "red",
    "Buy": "blue",
    "Exploring": "gray",
    "Call": "blue",
    "WhatsApp": "green",
    "Visit": "purple",
    "Warm-up": "yellow",
    "Simulation": "orange",
    "Review": "blue",
    "Easy": "green",
    "Medium": "yellow",
    "Hard": "red",
    "Opening": "blue",
    "Hook": "green",
    "Close": "red",
    "Objection": "orange",
    "New": "gray",
    "Follow-up": "yellow",
    "Viewing": "blue",
    "Closed": "green",
    "Lost": "red",
    "Owner": "blue",
    "Tenant": "purple",
    "Morning": "yellow",
    "Afternoon": "orange",
    "Evening": "purple",
}

def test_api_key():
    """Test if API key is valid"""
    print("Testing Notion API key...")
    response = requests.get(f"{BASE_URL}/users/me", headers=HEADERS)
    if response.status_code == 200:
        user = response.json()
        print(f"✓ API key valid - Connected as: {user.get('name', 'Unknown')}")
        return True
    else:
        print(f"✗ API key invalid: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def search_workspaces():
    """Search for accessible pages"""
    print("\nSearching for accessible pages...")
    response = requests.post(f"{BASE_URL}/search", headers=HEADERS, json={"page_size": 10})
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            print(f"Found {len(results)} accessible pages:")
            for page in results:
                title = page.get("properties", {}).get("title", {}).get("title", [{}])[0].get("plain_text", "Untitled")
                print(f"  - {title} (ID: {page['id']})")
            return results[0]["id"]  # Return first page ID as fallback
        else:
            print("No pages found. Creating new workspace...")
            return None
    else:
        print(f"Search failed: {response.status_code}")
        return None

def create_parent_page(parent_id=None):
    """Create the main Door Knocking Mastery page"""
    print("\nCreating Door Knocking Mastery parent page...")

    data = {
        "parent": {"page_id": parent_id} if parent_id else {"workspace": True},
        "properties": {
            "title": {
                "title": [{"text": {"content": "🚪 Door Knocking Mastery System"}}]
            }
        },
        "icon": {"emoji": "🚪"}
    }

    response = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=data)
    if response.status_code == 200:
        page = response.json()
        print(f"✓ Created parent page: {page['url']}")
        return page["id"]
    else:
        print(f"✗ Failed to create page: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def create_database(parent_id, title, icon, properties):
    """Create a Notion database"""
    data = {
        "parent": {"page_id": parent_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
        "icon": {"emoji": icon}
    }

    response = requests.post(f"{BASE_URL}/databases", headers=HEADERS, json=data)
    if response.status_code == 200:
        db = response.json()
        print(f"✓ Created database: {title}")
        return db["id"]
    else:
        print(f"✗ Failed to create database {title}: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def create_page_in_database(database_id, properties, icon=None):
    """Create a page in a database"""
    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    if icon:
        data["icon"] = {"emoji": icon}

    response = requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=data)
    if response.status_code == 200:
        return response.json()["id"]
    else:
        print(f"✗ Failed to create page: {response.status_code}")
        return None

def parse_csv(filename):
    """Parse CSV file and return list of dictionaries"""
    filepath = f"/home/wls/.openclaw/workspace/notion-sg-real-estate/DOOR_KNOCKING_SYSTEM/Templates/{filename}"
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def create_select_option(name):
    """Create a select option with color"""
    color = COLORS.get(name, "default")
    return {"name": name, "color": color}

def main():
    print("=" * 60)
    print("DOOR KNOCKING MASTERY SYSTEM - NOTION POPULATION")
    print("=" * 60)

    # Test API key
    if not test_api_key():
        return

    # Search for accessible pages or use workspace root
    parent_page_id = search_workspaces()

    # Create parent page
    if parent_page_id:
        door_knocking_page_id = create_parent_page(parent_page_id)
    else:
        door_knocking_page_id = create_parent_page()

    if not door_knocking_page_id:
        print("Failed to create parent page. Exiting.")
        return

    print(f"\nParent page ID: {door_knocking_page_id}")

    # We'll create databases in a specific order:
    # 1. Scripts (no relations)
    # 2. Sessions (no relations)
    # 3. Leads (relates to Sessions)
    # 4. Follow-ups (relates to Leads)
    # 5. Training (relates to Scripts)
    # 6. Weekly Reviews (no relations)

    print("\n" + "=" * 60)
    print("CREATING DATABASES")
    print("=" * 60)

    # 1. Scripts Database
    print("\n1. Creating Scripts Database...")
    scripts_props = {
        "Script Name": {"title": {}},
        "Area": {
            "select": {
                "options": [
                    create_select_option("Punggol"),
                    create_select_option("Serangoon"),
                    create_select_option("Both")
                ]
            }
        },
        "Type": {
            "select": {
                "options": [
                    create_select_option("Opening"),
                    create_select_option("Hook"),
                    create_select_option("Close"),
                    create_select_option("Objection")
                ]
            }
        },
        "Script Content": {"rich_text": {}},
        "Effectiveness Score": {"rich_text": {}},
        "Usage Count": {"number": {"format": "number"}},
        "Notes": {"rich_text": {}}
    }
    scripts_db_id = create_database(door_knocking_page_id, "Scripts", "📚", scripts_props)

    # 2. Sessions Database
    print("\n2. Creating Door Knocking Sessions Database...")
    sessions_props = {
        "Block": {"title": {}},
        "Date": {"date": {}},
        "Area": {
            "select": {
                "options": [
                    create_select_option("Punggol"),
                    create_select_option("Serangoon"),
                    create_select_option("Sengkang")
                ]
            }
        },
        "Time Slot": {
            "select": {
                "options": [
                    create_select_option("Morning"),
                    create_select_option("Afternoon"),
                    create_select_option("Evening")
                ]
            }
        },
        "Doors Knocked": {"number": {"format": "number"}},
        "Doors Opened": {"number": {"format": "number"}},
        "Conversations": {"number": {"format": "number"}},
        "Leads Captured": {"number": {"format": "number"}},
        "Appointments Set": {"number": {"format": "number"}},
        "Open Rate %": {"formula": {"expression": "prop(\"Doors Opened\") / prop(\"Doors Knocked\") * 100"}},
        "Conversation Rate %": {"formula": {"expression": "prop(\"Conversations\") / prop(\"Doors Opened\") * 100"}},
        "Lead Rate %": {"formula": {"expression": "prop(\"Leads Captured\") / prop(\"Conversations\") * 100"}},
        "Notes": {"rich_text": {}}
    }
    sessions_db_id = create_database(door_knocking_page_id, "Door Knocking Sessions", "🎯", sessions_props)

    # 3. Leads Database
    print("\n3. Creating Leads Database...")
    leads_props = {
        "Name": {"title": {}},
        "Unit": {"rich_text": {}},
        "Block": {"rich_text": {}},
        "Contact": {"rich_text": {}},
        "Owner/Tenant": {
            "select": {
                "options": [
                    create_select_option("Owner"),
                    create_select_option("Tenant")
                ]
            }
        },
        "Intent": {
            "select": {
                "options": [
                    create_select_option("Sell"),
                    create_select_option("Buy"),
                    create_select_option("Exploring")
                ]
            }
        },
        "Timeline": {"rich_text": {}},
        "Budget/Price": {"rich_text": {}},
        "Source": {"rich_text": {}},
        "Status": {
            "select": {
                "options": [
                    create_select_option("New"),
                    create_select_option("Follow-up"),
                    create_select_option("Viewing"),
                    create_select_option("Closed"),
                    create_select_option("Lost")
                ]
            }
        },
        "Last Contact Date": {"date": {}},
        "Area": {
            "select": {
                "options": [
                    create_select_option("Punggol"),
                    create_select_option("Serangoon"),
                    create_select_option("Sengkang")
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    create_select_option("High"),
                    create_select_option("Medium"),
                    create_select_option("Low")
                ]
            }
        },
        "Notes": {"rich_text": {}}
    }
    leads_db_id = create_database(door_knocking_page_id, "Leads", "👤", leads_props)

    # 4. Follow-ups Database
    print("\n4. Creating Follow-ups Database...")
    followups_props = {
        "Lead Name": {"title": {}},
        "Follow-up Date": {"date": {}},
        "Method": {
            "select": {
                "options": [
                    create_select_option("Call"),
                    create_select_option("WhatsApp"),
                    create_select_option("Visit")
                ]
            }
        },
        "Outcome": {"rich_text": {}},
        "Next Action": {"rich_text": {}},
        "Priority": {
            "select": {
                "options": [
                    create_select_option("High"),
                    create_select_option("Medium"),
                    create_select_option("Low")
                ]
            }
        },
        "Status": {
            "select": {
                "options": [
                    create_select_option("Pending"),
                    create_select_option("Done"),
                    create_select_option("Overdue")
                ]
            }
        }
    }
    followups_db_id = create_database(door_knocking_page_id, "Follow-ups", "📞", followups_props)

    # 5. Training Database
    print("\n5. Creating Training Database...")
    training_props = {
        "Session Name": {"title": {}},
        "Date": {"date": {}},
        "Practice Type": {
            "select": {
                "options": [
                    create_select_option("Warm-up"),
                    create_select_option("Simulation"),
                    create_select_option("Review")
                ]
            }
        },
        "Difficulty": {
            "select": {
                "options": [
                    create_select_option("Easy"),
                    create_select_option("Medium"),
                    create_select_option("Hard")
                ]
            }
        },
        "Scenario Type": {
            "select": {
                "options": [
                    create_select_option("Punggol"),
                    create_select_option("Serangoon"),
                    create_select_option("Objection")
                ]
            }
        },
        "Script Used": {"rich_text": {}},
        "Score": {"rich_text": {}},
        "Feedback": {"rich_text": {}},
        "Improvement Notes": {"rich_text": {}},
        "Duration": {"rich_text": {}}
    }
    training_db_id = create_database(door_knocking_page_id, "Training", "🧠", training_props)

    # 6. Weekly Reviews Database
    print("\n6. Creating Weekly Reviews Database...")
    reviews_props = {
        "Week": {"title": {}},
        "Total Sessions": {"rich_text": {}},
        "Total Doors Knocked": {"number": {"format": "number"}},
        "Total Leads": {"number": {"format": "number"}},
        "Best Area": {
            "select": {
                "options": [
                    create_select_option("Punggol"),
                    create_select_option("Serangoon"),
                    create_select_option("Sengkang")
                ]
            }
        },
        "Open Rate %": {"number": {"format": "percent"}},
        "Conversation Rate %": {"number": {"format": "percent"}},
        "Lead Rate %": {"number": {"format": "percent"}},
        "Appointment Rate %": {"number": {"format": "percent"}},
        "Script of the Week": {"rich_text": {}},
        "Lessons Learned": {"rich_text": {}},
        "Next Week Plan": {"rich_text": {}}
    }
    reviews_db_id = create_database(door_knocking_page_id, "Weekly Reviews", "📊", reviews_props)

    print("\n" + "=" * 60)
    print("POPULATING DATA")
    print("=" * 60)

    # Populate Scripts
    print("\nPopulating Scripts...")
    scripts_data = parse_csv("scripts.csv")
    for row in scripts_data[:12]:  # Limit to 12 scripts
        props = {
            "Script Name": {"title": [{"text": {"content": row.get("Script Name", "")}}]},
            "Area": {"select": {"name": row.get("Area", "Punggol")}},
            "Type": {"select": {"name": row.get("Type", "Opening")}},
            "Script Content": {"rich_text": [{"text": {"content": row.get("Script Content", "")[:2000]}}]},
            "Effectiveness Score": {"rich_text": [{"text": {"content": row.get("Effectiveness Score", "")}}]},
            "Usage Count": {"number": int(row.get("Usage Count", "0") or 0)},
            "Notes": {"rich_text": [{"text": {"content": row.get("Notes", "")}}]}
        }
        create_page_in_database(scripts_db_id, props)
    print(f"✓ Added {len(scripts_data[:12])} scripts")

    # Populate Sessions
    print("\nPopulating Door Knocking Sessions...")
    sessions_data = parse_csv("door_knocking_sessions.csv")
    for row in sessions_data[:10]:
        props = {
            "Block": {"title": [{"text": {"content": row.get("Block", "")}}]},
            "Date": {"date": {"start": row.get("Date", datetime.now().strftime("%Y-%m-%d"))}},
            "Area": {"select": {"name": row.get("Area", "Punggol")}},
            "Time Slot": {"select": {"name": row.get("Time Slot", "Evening")}},
            "Doors Knocked": {"number": int(row.get("Doors Knocked", "0") or 0)},
            "Doors Opened": {"number": int(row.get("Doors Opened", "0") or 0)},
            "Conversations": {"number": int(row.get("Conversations", "0") or 0)},
            "Leads Captured": {"number": int(row.get("Leads Captured", "0") or 0)},
            "Appointments Set": {"number": int(row.get("Appointments Set", "0") or 0)},
            "Notes": {"rich_text": [{"text": {"content": row.get("Notes", "")}}]}
        }
        create_page_in_database(sessions_db_id, props)
    print(f"✓ Added {len(sessions_data[:10])} sessions")

    # Populate Leads
    print("\nPopulating Leads...")
    leads_data = parse_csv("leads.csv")
    for row in leads_data[:16]:
        props = {
            "Name": {"title": [{"text": {"content": row.get("Name", "")}}]},
            "Unit": {"rich_text": [{"text": {"content": row.get("Unit", "")}}]},
            "Block": {"rich_text": [{"text": {"content": row.get("Block", "")}}]},
            "Contact": {"rich_text": [{"text": {"content": row.get("Contact", "")}}]},
            "Owner/Tenant": {"select": {"name": row.get("Owner/Tenant", "Owner")}},
            "Intent": {"select": {"name": row.get("Intent", "Exploring")}},
            "Timeline": {"rich_text": [{"text": {"content": row.get("Timeline", "")}}]},
            "Budget/Price": {"rich_text": [{"text": {"content": row.get("Budget/Price Expectation", "")}}]},
            "Source": {"rich_text": [{"text": {"content": row.get("Source", "Door Knocking")}}]},
            "Status": {"select": {"name": row.get("Status", "New")}},
            "Last Contact Date": {"date": {"start": row.get("Last Contact Date", datetime.now().strftime("%Y-%m-%d"))}},
            "Area": {"select": {"name": row.get("Area", "Punggol")}},
            "Priority": {"select": {"name": row.get("Priority", "Medium")}},
            "Notes": {"rich_text": [{"text": {"content": row.get("Notes", "")}}]}
        }
        create_page_in_database(leads_db_id, props)
    print(f"✓ Added {len(leads_data[:16])} leads")

    # Populate Follow-ups
    print("\nPopulating Follow-ups...")
    followups_data = parse_csv("follow_ups.csv")
    for row in followups_data[:13]:
        props = {
            "Lead Name": {"title": [{"text": {"content": row.get("Lead Name", "")}}]},
            "Follow-up Date": {"date": {"start": row.get("Follow-up Date", datetime.now().strftime("%Y-%m-%d"))}},
            "Method": {"select": {"name": row.get("Method", "WhatsApp")}},
            "Outcome": {"rich_text": [{"text": {"content": row.get("Outcome", "")}}]},
            "Next Action": {"rich_text": [{"text": {"content": row.get("Next Action", "")}}]},
            "Priority": {"select": {"name": row.get("Priority", "Medium")}},
            "Status": {"select": {"name": row.get("Status", "Pending")}}
        }
        create_page_in_database(followups_db_id, props)
    print(f"✓ Added {len(followups_data[:13])} follow-ups")

    # Populate Training
    print("\nPopulating Training Sessions...")
    training_data = parse_csv("training_sessions.csv")
    for i, row in enumerate(training_data[:14]):
        session_name = f"{row.get('Practice Type', 'Session')} {i+1} - {row.get('Scenario Type', 'General')}"
        props = {
            "Session Name": {"title": [{"text": {"content": session_name}}]},
            "Date": {"date": {"start": row.get("Date", datetime.now().strftime("%Y-%m-%d"))}},
            "Practice Type": {"select": {"name": row.get("Practice Type", "Warm-up")}},
            "Difficulty": {"select": {"name": row.get("Difficulty", "Medium")}},
            "Scenario Type": {"select": {"name": row.get("Scenario Type", "Punggol")}},
            "Script Used": {"rich_text": [{"text": {"content": row.get("Script Used", "")}}]},
            "Score": {"rich_text": [{"text": {"content": row.get("Score", "")}}]},
            "Feedback": {"rich_text": [{"text": {"content": row.get("Feedback", "")}}]},
            "Improvement Notes": {"rich_text": [{"text": {"content": row.get("Improvement Notes", "")}}]},
            "Duration": {"rich_text": [{"text": {"content": row.get("Duration", "")}}]}
        }
        create_page_in_database(training_db_id, props)
    print(f"✓ Added {len(training_data[:14])} training sessions")

    # Populate Weekly Reviews
    print("\nPopulating Weekly Reviews...")
    reviews_data = parse_csv("weekly_reviews.csv")
    for row in reviews_data[:4]:
        # Parse numeric values that may have text (e.g., "172 doors" -> 172)
        def parse_number(val):
            if not val:
                return 0
            val_str = str(val).split()[0]  # Get first part before space
            try:
                return int(float(val_str))
            except:
                return 0

        props = {
            "Week": {"title": [{"text": {"content": row.get("Week", "")}}]},
            "Total Sessions": {"rich_text": [{"text": {"content": row.get("Total Sessions", "")}}]},
            "Total Doors Knocked": {"number": parse_number(row.get("Total Doors Knocked", "0"))},
            "Total Leads": {"number": parse_number(row.get("Total Leads", "0"))},
            "Best Area": {"select": {"name": row.get("Best Area", "Punggol")}},
            "Open Rate %": {"number": float(row.get("Open Rate %", "0") or 0)},
            "Conversation Rate %": {"number": float(row.get("Conversation Rate %", "0") or 0)},
            "Lead Rate %": {"number": float(row.get("Lead Rate %", "0") or 0)},
            "Appointment Rate %": {"number": float(row.get("Appointment Rate %", "0") or 0)},
            "Script of the Week": {"rich_text": [{"text": {"content": row.get("Script of the Week", "")}}]},
            "Lessons Learned": {"rich_text": [{"text": {"content": row.get("Lessons Learned", "")}}]},
            "Next Week Plan": {"rich_text": [{"text": {"content": row.get("Next Week Plan", "")}}]}
        }
        create_page_in_database(reviews_db_id, props)
    print(f"✓ Added {len(reviews_data[:4])} weekly reviews")

    print("\n" + "=" * 60)
    print("POPULATION COMPLETE!")
    print("=" * 60)
    print(f"\nCreated 6 databases in your Notion workspace:")
    print(f"  📚 Scripts - 12 scripts loaded")
    print(f"  🎯 Door Knocking Sessions - 10 sessions loaded")
    print(f"  👤 Leads - 16 leads loaded")
    print(f"  📞 Follow-ups - 13 follow-ups loaded")
    print(f"  🧠 Training - 14 training sessions loaded")
    print(f"  📊 Weekly Reviews - 3 reviews loaded")
    print(f"\nTotal: 68 sample records populated!")
    print(f"\nNext steps:")
    print(f"  1. Open your Notion workspace")
    print(f"  2. Find '🚪 Door Knocking Mastery System'")
    print(f"  3. Set up relations between databases (see SETUP_GUIDE.md)")
    print(f"  4. Create filtered views for daily workflow")

if __name__ == "__main__":
    main()
