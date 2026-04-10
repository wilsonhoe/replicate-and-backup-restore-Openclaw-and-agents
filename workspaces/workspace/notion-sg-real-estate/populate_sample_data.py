#!/usr/bin/env python3
"""
Populate SG Real Estate Notion System with realistic sample data
"""

import requests
import json
import random
from datetime import datetime, timedelta

NOTION_TOKEN = "REDACTED_SET_FROM_ENV"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Database IDs
DATABASES = {
    "leads": "33999ce8-2630-8174-a825-f6dcc772eefd",
    "properties": "33999ce8-2630-816d-9a27-e1213823e18e",
    "activities": "33999ce8-2630-810f-a7cf-d83850c96746",
    "deals": "33999ce8-2630-814b-acef-c98560716a75",
    "knowledge": "33999ce8-2630-8151-b68f-e4ba9619d08e",
    "nel_tracker": "33999ce8-2630-8140-864c-f5fe6c850493"
}

# Sample data generators
SINGAPORE_NAMES = [
    "Tan Wei Ming", "Lim Shu Qi", "Chen Jia Hao", "Wong Mei Ling",
    "Ng Kok Peng", "Lee Xiu Ying", "Goh Zhi Xiang", "Chua Pei Shan",
    "Koh Jun Wei", "Ong Li Na", "Teo Han Ming", "Yeo Xin Yi",
    "Low Kar Wai", "Sim Ai Ling", "Poh Boon Keng"
]

SINGAPORE_ADDRESSES = [
    "123 Punggol Drive", "456 Sengkang East Avenue", "789 Hougang Street 21",
    "234 Serangoon Avenue 3", "567 Compassvale Road", "89 Punggol Field",
    "345 Fernvale Lane", "678 Anchorvale Crescent", "901 Buangkok Drive",
    "432 Compassvale Walk", "765 Rivervale Drive", "188 Edgefield Plains",
    "321 Compassvale Bow", "654 Rivervale Crescent", "987 Anchorvale Road"
]

CONTACT_PREFIXES = ["+65 9", "+65 8", "+65 6"]


def random_date(days_back=30, days_forward=30):
    """Generate a random date within range"""
    base = datetime.now()
    delta = random.randint(-days_back, days_forward)
    return (base + timedelta(days=delta)).strftime("%Y-%m-%d")


def random_phone():
    """Generate random Singapore phone number"""
    prefix = random.choice(CONTACT_PREFIXES)
    return f"{prefix}{random.randint(1000000, 9999999)}"


def create_page_in_database(database_id, properties):
    """Create a page in a database"""
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()


def populate_leads():
    """Populate Leads database with sample data"""
    print("👥 Populating Leads...")

    sources = ["🚪 Door Knocking", "👨‍👩‍👧 Referral", "💻 Online", "📱 Social Media", "🏢 Walk-in"]
    property_interests = [["🏢 HDB"], ["🏠 Condo"], ["🏢 HDB", "🏘️ EC"], ["🏠 Condo"], ["🏡 Landed"]]
    budget_ranges = ["<$500K", "$500K-$800K", "$800K-$1.2M", "$1.2M-$2M", ">$2M"]
    statuses = ["🆕 New", "📞 Contacted", "👀 Viewing Scheduled", "💰 Offer Made", "✅ Closed", "❌ Lost"]
    priorities = ["🔥 Hot", "⚡ Warm", "❄️ Cold"]

    created_leads = []
    for i, name in enumerate(SINGAPORE_NAMES[:10]):
        name_parts = name.split()
        first = name_parts[0]
        last = name_parts[-1]
        email = f"{first.lower()}.{last.lower()}@email.com"

        properties = {
            "Name": {"title": [{"text": {"content": name}}]},
            "Contact": {"phone_number": random_phone()},
            "Email": {"email": email},
            "Source": {"select": {"name": random.choice(sources)}},
            "Property Interest": {"multi_select": [{"name": p} for p in random.choice(property_interests)]},
            "Budget Range": {"select": {"name": random.choice(budget_ranges)}},
            "Status": {"select": {"name": statuses[i % len(statuses)]}},
            "Priority": {"select": {"name": random.choice(priorities)}},
            "Last Contact": {"date": {"start": random_date(14, 0)}},
            "Next Follow-up": {"date": {"start": random_date(0, 7)}},
            "Notes": {"rich_text": [{"text": {"content": f"Met {name}. Interested in property near MRT. Budget flexible for right unit."}}]}
        }

        result = create_page_in_database(DATABASES["leads"], properties)
        if "id" in result:
            created_leads.append({"id": result["id"], "name": name})
        print(f"  ✅ Lead: {name}")

    return created_leads


def populate_properties():
    """Populate Properties database with sample data"""
    print("🏢 Populating Properties...")

    types = ["🏢 HDB", "🏠 Condo", "🏡 Landed", "🏘️ EC"]
    districts = [f"D{i}" for i in range(1, 29)]
    areas = ["🚇 Punggol", "🚇 Sengkang", "🚇 Hougang", "🚇 Serangoon", "CBD", "Other"]
    bedrooms = ["1", "2", "3", "4", "5+"]
    statuses = ["✅ Available", "📝 Under Offer", "❌ Sold", "🔒 Off Market"]

    property_data = [
        ("Punggol Waterway Terrace", "🏢 HDB", "D19", "🚇 Punggol", 650000, 1100, "4"),
        ("Sengkang Grand Residences", "🏠 Condo", "D19", "🚇 Sengkang", 1200000, 850, "3"),
        ("Hougang Avenue 5", "🏢 HDB", "D19", "🚇 Hougang", 580000, 1000, "4"),
        ("Serangoon Garden Estate", "🏡 Landed", "D19", "🚇 Serangoon", 2800000, 2800, "5+"),
        ("Punggol Northshore", "🏘️ EC", "D19", "🚇 Punggol", 950000, 1050, "4"),
        ("Compassvale Beacon", "🏢 HDB", "D19", "🚇 Sengkang", 520000, 900, "3"),
        ("Buangkok Vale", "🏢 HDB", "D19", "🚇 Hougang", 480000, 850, "3"),
        ("Luxus Hills", "🏡 Landed", "D28", "Other", 3200000, 3200, "5+"),
    ]

    created_properties = []
    for name, ptype, district, area, price, size, beds in property_data:
        address = random.choice(SINGAPORE_ADDRESSES)

        properties = {
            "Property Name": {"title": [{"text": {"content": name}}]},
            "Address": {"rich_text": [{"text": {"content": address}}]},
            "Type": {"select": {"name": ptype}},
            "District": {"select": {"name": district}},
            "Area": {"select": {"name": area}},
            "Price": {"number": price},
            "Size (sqft)": {"number": size},
            "Bedrooms": {"select": {"name": beds}},
            "Status": {"select": {"name": random.choice(statuses)}},
            "Listing Date": {"date": {"start": random_date(60, 0)}},
            "Seller Contact": {"phone_number": random_phone()},
            "Notes": {"rich_text": [{"text": {"content": f"Well-maintained unit. Near amenities and MRT."}}]}
        }

        result = create_page_in_database(DATABASES["properties"], properties)
        if "id" in result:
            created_properties.append({"id": result["id"], "name": name})
        print(f"  ✅ Property: {name}")

    return created_properties


def populate_activities():
    """Populate Activities database with sample data"""
    print("📅 Populating Activities...")

    activity_types = ["🚪 Door Knocking", "☎️ Cold Call", "📧 Follow-up", "👀 Viewing", "🤝 Meeting", "💻 Research"]
    areas = ["🚇 Punggol", "🚇 Sengkang", "🚇 Hougang", "🚇 Serangoon", "CBD", "Other"]
    outcomes = ["✅ Lead Generated", "📞 Callback Scheduled", "❌ No Answer", "🚫 Not Interested", "📊 Market Intel", "✅ Completed"]

    activity_data = [
        ("🚪 Door Knock - Punggol - Apr 3", "🚪 Door Knocking", "🚇 Punggol", "✅ Lead Generated", 3, 12, 180, "Good response in Block 123-125. Owners receptive to upgrading."),
        ("☎️ Cold Call Session - Apr 4", "☎️ Cold Call", "🚇 Sengkang", "📞 Callback Scheduled", 2, 25, 90, "Called expired listings. 2 callbacks scheduled for next week."),
        ("👀 Viewing - Tan Wei Ming", "👀 Viewing", "🚇 Punggol", "✅ Completed", 1, 3, 45, "Client liked the unit but wants to compare. Following up tomorrow."),
        ("🤝 Meeting - Lim Shu Qi", "🤝 Meeting", "CBD", "✅ Lead Generated", 1, 1, 60, "Pre-approval discussion done. Ready to view properties next week."),
        ("🚪 Door Knock - Hougang - Apr 2", "🚪 Door Knocking", "🚇 Hougang", "📊 Market Intel", 0, 8, 120, "Many units under renovation. Market picking up in this area."),
        ("📧 Follow-up - Chen Jia Hao", "📧 Follow-up", "🚇 Serangoon", "✅ Completed", 0, 1, 30, "Sent new listings. Client reviewing and will revert by Friday."),
        ("💻 Research - Market Analysis", "💻 Research", "Other", "📊 Market Intel", 0, 0, 60, "Compiled Q1 transaction data for NEL areas. Prices up 3% vs last quarter."),
        ("👀 Viewing - Wong Mei Ling", "👀 Viewing", "🚇 Sengkang", "✅ Completed", 1, 2, 60, "Second viewing. Client comparing with another unit in the area."),
    ]

    created_activities = []
    for name, atype, area, outcome, leads, convos, duration, notes in activity_data:
        properties = {
            "Activity Name": {"title": [{"text": {"content": name}}]},
            "Date": {"date": {"start": random_date(7, 0)}},
            "Type": {"select": {"name": atype}},
            "Area": {"select": {"name": area}},
            "Outcome": {"select": {"name": outcome}},
            "Leads Generated": {"number": leads},
            "Conversations": {"number": convos},
            "Duration (mins)": {"number": duration},
            "Notes": {"rich_text": [{"text": {"content": notes}}]},
            "Added to KB": {"checkbox": random.choice([True, False])}
        }

        result = create_page_in_database(DATABASES["activities"], properties)
        if "id" in result:
            created_activities.append({"id": result["id"], "name": name})
        print(f"  ✅ Activity: {name}")

    return created_activities


def populate_deals():
    """Populate Deals database with sample data"""
    print("💼 Populating Deals...")

    stages = ["🆕 New", "👀 Viewing", "💰 Offer Made", "📝 OTP Issued", "✅ OTP Exercised",
              "📋 Resale Application", "🏛️ HDB Acceptance", "🔨 Legal Completion", "✅ Closed", "❌ Lost"]
    deal_types = ["🏢 HDB → HDB", "🏢 HDB → 🏠 Private", "🏠 Private → 🏠 Private", "🏠 Private → 🏢 HDB"]
    probabilities = ["10%", "25%", "50%", "75%", "90%", "100%"]

    deal_data = [
        ("Tan Wei Ming - Punggol Waterway Terrace", "🏢 HDB → HDB", "💰 Offer Made", 650000, "75%", "Draft OTP for review", 5),
        ("Lim Shu Qi - Sengkang Grand Residences", "🏠 Private → 🏠 Private", "👀 Viewing", 1200000, "50%", "Schedule second viewing", 7),
        ("Chen Jia Hao - Hougang Avenue 5", "🏢 HDB → HDB", "📝 OTP Issued", 580000, "90%", "Collect exercise documents", 3),
        ("Wong Mei Ling - Compassvale Beacon", "🏢 HDB → 🏠 Private", "✅ Closed", 520000, "100%", "Handover completed", 0),
        ("Ng Kok Peng - Serangoon Garden Estate", "🏡 Landed", "📋 Resale Application", 2800000, "75%", "Submit to HDB portal", 14),
        ("Lee Xiu Ying - Punggol Northshore", "🏘️ EC", "👀 Viewing", 950000, "25%", "Follow up on financing", 10),
    ]

    created_deals = []
    for name, dtype, stage, price, prob, next_action, days in deal_data:
        expected_close = (datetime.now() + timedelta(days=days + random.randint(30, 60))).strftime("%Y-%m-%d")
        next_due = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

        commission_pct = 0.02 if "Landed" not in dtype else 0.01

        properties = {
            "Deal Name": {"title": [{"text": {"content": name}}]},
            "Stage": {"select": {"name": stage}},
            "Deal Type": {"select": {"name": dtype}},
            "Price": {"number": price},
            "Commission %": {"number": commission_pct},
            "Probability": {"select": {"name": prob}},
            "Expected Close": {"date": {"start": expected_close}},
            "Next Action": {"rich_text": [{"text": {"content": next_action}}]},
            "Next Action Due": {"date": {"start": next_due}},
            "Notes": {"rich_text": [{"text": {"content": f"Regular follow-up. Client responsive."}}]}
        }

        # Add stage-specific dates
        if stage in ["📝 OTP Issued", "✅ OTP Exercised", "📋 Resale Application", "🏛️ HDB Acceptance", "🔨 Legal Completion", "✅ Closed"]:
            otp_date = (datetime.now() - timedelta(days=random.randint(7, 21))).strftime("%Y-%m-%d")
            properties["OTP Date"] = {"date": {"start": otp_date}}

        if stage in ["✅ OTP Exercised", "📋 Resale Application", "🏛️ HDB Acceptance", "🔨 Legal Completion", "✅ Closed"]:
            exercise_date = (datetime.now() - timedelta(days=random.randint(0, 14))).strftime("%Y-%m-%d")
            properties["OTP Exercise Date"] = {"date": {"start": exercise_date}}

        result = create_page_in_database(DATABASES["deals"], properties)
        if "id" in result:
            created_deals.append({"id": result["id"], "name": name})
        print(f"  ✅ Deal: {name}")

    return created_deals


def populate_knowledge_base():
    """Populate Knowledge Base databases with sample data"""
    print("📚 Populating Knowledge Base...")

    # Scripts
    scripts = [
        ("Door Knocking Opener", "🚪 Door Knocking", "Hi! I'm a property consultant helping homeowners in this area. I noticed some recent transactions and wanted to check if you might be considering a move?", ["HDB", "First-time buyer"], "High"),
        ("Cold Call Script", "☎️ Cold Call", "Hello, this is [name] from [agency]. I'm calling because I saw your property listing expired. Are you still looking to sell?", ["HDB", "Condo"], "Medium"),
        ("Handling Price Objection", "❌ Objection Handling", "I understand your concern about the price. Let me show you some recent comparable sales in this area to help set realistic expectations.", ["HDB", "Condo", "Landed"], "High"),
        ("Follow-up Email Template", "📧 Follow-up", "Thank you for viewing the property today. As discussed, I've attached additional information about the unit and the neighborhood amenities.", ["HDB", "Condo", "EC"], "High"),
        ("Closing Script - OTP", "🤝 Closing", "Based on our discussions, shall we proceed with the OTP? I'll prepare the documents and we can meet tomorrow to sign.", ["HDB", "Condo"], "High"),
    ]

    for name, stype, content, best_for, success in scripts:
        properties = {
            "Script Name": {"title": [{"text": {"content": name}}]},
            "Type": {"select": {"name": stype}},
            "Content": {"rich_text": [{"text": {"content": content}}]},
            "Best For": {"multi_select": [{"name": b} for b in best_for]},
            "Success Rate": {"select": {"name": success}},
            "Last Used": {"date": {"start": random_date(14, 0)}}
        }
        result = create_page_in_database(DATABASES["knowledge"], properties)
        print(f"  ✅ Script: {name}")

    # Market Insights
    insights = [
        ("Punggol Prices Rising", "Punggol", "📈 Price Trend", "2026-04-01", "URA Data", "High"),
        ("New EC Launch - Anchorvale", "Sengkang", "🏗️ New Launch", "2026-03-15", "Developer Announcement", "High"),
        ("HDB Resale Volume Up 12%", "Other", "📊 Transaction Volume", "2026-03-28", "HDB Report", "Medium"),
        ("Cooling Measure Impact", "Other", "📝 Policy Change", "2026-01-15", "Gov.sg", "High"),
        ("Hougang MRT Extension", "Hougang", "🏗️ New Launch", "2026-02-20", "LTA News", "Medium"),
    ]

    for insight, area, itype, date, source, impact in insights:
        properties = {
            "Insight": {"title": [{"text": {"content": insight}}]},
            "Area": {"select": {"name": area}},
            "Type": {"select": {"name": itype}},
            "Date": {"date": {"start": date}},
            "Source": {"rich_text": [{"text": {"content": source}}]},
            "Impact": {"select": {"name": impact}}
        }
        result = create_page_in_database(DATABASES["knowledge"], properties)
        print(f"  ✅ Insight: {insight}")

    # Lessons Learned
    lessons = [
        ("Follow up within 24 hours", "✅ What Worked", "2026-04-01", "Quick follow-up increases conversion by 40%"),
        ("Door knocking evening better", "💡 Insight", "2026-03-28", "After 6pm gets more responses than afternoon"),
        ("Script too aggressive", "❌ What Didn't", "2026-03-25", "Soft opener works better than direct pitch"),
        ("Use CMA in first meeting", "✅ What Worked", "2026-03-20", "Showing data builds credibility immediately"),
    ]

    for lesson, context, date, action in lessons:
        properties = {
            "Lesson": {"title": [{"text": {"content": lesson}}]},
            "Context": {"select": {"name": context}},
            "Date": {"date": {"start": date}},
            "Action Item": {"rich_text": [{"text": {"content": action}}]}
        }
        result = create_page_in_database(DATABASES["knowledge"], properties)
        print(f"  ✅ Lesson: {lesson}")


def main():
    print("=" * 60)
    print("🎯 Populating SG Property Pro with Sample Data")
    print("=" * 60)
    print()

    # Populate databases
    leads = populate_leads()
    print()

    properties = populate_properties()
    print()

    activities = populate_activities()
    print()

    deals = populate_deals()
    print()

    populate_knowledge_base()
    print()

    print("=" * 60)
    print("🎉 SAMPLE DATA POPULATION COMPLETE!")
    print("=" * 60)
    print()
    print("Summary:")
    print(f"  • {len(leads)} Leads created")
    print(f"  • {len(properties)} Properties created")
    print(f"  • {len(activities)} Activities created")
    print(f"  • {len(deals)} Deals created")
    print(f"  • Knowledge Base populated with scripts, insights, lessons")
    print()
    print("🌐 Open Notion to see your fully populated system!")
    print("   https://notion.so/33999ce826308191ab04f2bb6e45ca47")


if __name__ == "__main__":
    main()
