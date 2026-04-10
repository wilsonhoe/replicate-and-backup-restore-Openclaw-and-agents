#!/usr/bin/env python3
"""
Setup database relations and rollups for SG Real Estate System
Must run after setup_notion_system.py
"""

import requests
import json

NOTION_TOKEN = "REDACTED_SET_FROM_ENV"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Database IDs from previous run - UPDATE THESE after first run
DATABASES = {
    "leads": "33999ce8-2630-8174-a825-f6dcc772eefd",
    "properties": "33999ce8-2630-816d-9a27-e1213823e18e",
    "activities": "33999ce8-2630-810f-a7cf-d83850c96746",
    "deals": "33999ce8-2630-814b-acef-c98560716a75",
    "knowledge": "33999ce8-2630-8151-b68f-e4ba9619d08e"
}


def add_database_property(database_id, property_name, property_config):
    """Add a new property to existing database"""
    url = f"https://api.notion.com/v1/databases/{database_id}"

    data = {
        "properties": {
            property_name: property_config
        }
    }

    response = requests.patch(url, headers=HEADERS, json=data)
    return response.json()


def setup_leads_relations():
    """Add relation properties to Leads database"""
    print("🔗 Setting up Leads relations...")

    # Linked Property (relation to Properties)
    add_database_property(
        DATABASES["leads"],
        "Linked Property",
        {
            "relation": {
                "database_id": DATABASES["properties"],
                "single_property": {}
            }
        }
    )

    # Activities (relation to Activities)
    add_database_property(
        DATABASES["leads"],
        "Activities",
        {
            "relation": {
                "database_id": DATABASES["activities"],
                "single_property": {}
            }
        }
    )

    # Linked Deals (relation to Deals)
    add_database_property(
        DATABASES["leads"],
        "Linked Deals",
        {
            "relation": {
                "database_id": DATABASES["deals"],
                "single_property": {}
            }
        }
    )

    # Total Activities (rollup)
    add_database_property(
        DATABASES["leads"],
        "Total Activities",
        {
            "rollup": {
                "relation_property_name": "Activities",
                "rollup_property_name": "Name",
                "function": "count"
            }
        }
    )

    # Days Since Contact (formula)
    add_database_property(
        DATABASES["leads"],
        "Days Since Contact",
        {
            "formula": {
                "expression": 'dateBetween(now(), prop("Last Contact"), "days")'
            }
        }
    )

    print("✅ Leads relations configured")


def setup_properties_relations():
    """Add relation properties to Properties database"""
    print("🔗 Setting up Properties relations...")

    # Linked Leads (relation to Leads - two-way)
    add_database_property(
        DATABASES["properties"],
        "Linked Leads",
        {
            "relation": {
                "database_id": DATABASES["leads"],
                "single_property": {}
            }
        }
    )

    # Viewings (relation to Activities)
    add_database_property(
        DATABASES["properties"],
        "Viewings",
        {
            "relation": {
                "database_id": DATABASES["activities"],
                "single_property": {}
            }
        }
    )

    # Linked Deals (relation to Deals)
    add_database_property(
        DATABASES["properties"],
        "Linked Deals",
        {
            "relation": {
                "database_id": DATABASES["deals"],
                "single_property": {}
            }
        }
    )

    # PSF (formula)
    add_database_property(
        DATABASES["properties"],
        "PSF",
        {
            "formula": {
                "expression": 'prop("Price") / prop("Size (sqft)")'
            }
        }
    )

    # Lead Count (rollup)
    add_database_property(
        DATABASES["properties"],
        "Lead Count",
        {
            "rollup": {
                "relation_property_name": "Linked Leads",
                "rollup_property_name": "Name",
                "function": "count"
            }
        }
    )

    # Total Viewings (rollup)
    add_database_property(
        DATABASES["properties"],
        "Total Viewings",
        {
            "rollup": {
                "relation_property_name": "Viewings",
                "rollup_property_name": "Name",
                "function": "count"
            }
        }
    )

    print("✅ Properties relations configured")


def setup_activities_relations():
    """Add relation properties to Activities database"""
    print("🔗 Setting up Activities relations...")

    # Linked Lead (relation to Leads)
    add_database_property(
        DATABASES["activities"],
        "Linked Lead",
        {
            "relation": {
                "database_id": DATABASES["leads"],
                "single_property": {}
            }
        }
    )

    # Linked Property (relation to Properties)
    add_database_property(
        DATABASES["activities"],
        "Linked Property",
        {
            "relation": {
                "database_id": DATABASES["properties"],
                "single_property": {}
            }
        }
    )

    print("✅ Activities relations configured")


def setup_deals_relations():
    """Add relation and formula properties to Deals database"""
    print("🔗 Setting up Deals relations...")

    # Lead (relation to Leads - required)
    add_database_property(
        DATABASES["deals"],
        "Lead",
        {
            "relation": {
                "database_id": DATABASES["leads"],
                "single_property": {}
            }
        }
    )

    # Property (relation to Properties - required)
    add_database_property(
        DATABASES["deals"],
        "Property",
        {
            "relation": {
                "database_id": DATABASES["properties"],
                "single_property": {}
            }
        }
    )

    # Deal Type
    add_database_property(
        DATABASES["deals"],
        "Deal Type",
        {
            "select": {
                "options": [
                    {"name": "🏢 HDB → HDB", "color": "blue"},
                    {"name": "🏢 HDB → 🏠 Private", "color": "purple"},
                    {"name": "🏠 Private → 🏠 Private", "color": "green"},
                    {"name": "🏠 Private → 🏢 HDB", "color": "yellow"}
                ]
            }
        }
    )

    # Commission %
    add_database_property(
        DATABASES["deals"],
        "Commission %",
        {
            "number": {
                "format": "percent"
            }
        }
    )

    # Commission Est (formula)
    add_database_property(
        DATABASES["deals"],
        "Commission Est",
        {
            "formula": {
                "expression": 'prop("Price") * prop("Commission %")'
            }
        }
    )

    # Probability
    add_database_property(
        DATABASES["deals"],
        "Probability",
        {
            "select": {
                "options": [
                    {"name": "10%", "color": "gray"},
                    {"name": "25%", "color": "blue"},
                    {"name": "50%", "color": "yellow"},
                    {"name": "75%", "color": "orange"},
                    {"name": "90%", "color": "green"},
                    {"name": "100%", "color": "red"}
                ]
            }
        }
    )

    # Weighted Commission (formula)
    add_database_property(
        DATABASES["deals"],
        "Weighted Commission",
        {
            "formula": {
                "expression": 'prop("Commission Est") * toNumber(replaceAll(prop("Probability"), "%", "")) / 100'
            }
        }
    )

    # Days in Stage (formula)
    add_database_property(
        DATABASES["deals"],
        "Days in Stage",
        {
            "formula": {
                "expression": 'dateBetween(now(), prop("Created time"), "days")'
            }
        }
    )

    # Next Action Due
    add_database_property(
        DATABASES["deals"],
        "Next Action Due",
        {
            "date": {}
        }
    )

    # Next Action
    add_database_property(
        DATABASES["deals"],
        "Next Action",
        {
            "rich_text": {}
        }
    )

    print("✅ Deals relations configured")


def setup_knowledge_base_properties():
    """Add additional properties to Knowledge Base databases"""
    print("🔗 Setting up Knowledge Base properties...")

    # Scripts Library properties
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
        "Content": {"rich_text": {}},
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

    # Market Insights properties
    insights_props = {
        "Insight": {"title": {}},
        "Area": {
            "select": {
                "options": [
                    {"name": "Punggol", "color": "purple"},
                    {"name": "Sengkang", "color": "pink"},
                    {"name": "Hougang", "color": "yellow"},
                    {"name": "Serangoon", "color": "orange"},
                    {"name": "Other NEL", "color": "gray"},
                    {"name": "CBD", "color": "blue"},
                    {"name": "Other", "color": "brown"}
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
                    {"name": "Low", "color": "gray"}
                ]
            }
        }
    }

    # Lessons Learned properties
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
        "Related Activity": {
            "relation": {
                "database_id": DATABASES["activities"],
                "single_property": {}
            }
        },
        "Action Item": {"rich_text": {}}
    }

    print("✅ Knowledge Base properties configured")
    return scripts_props, insights_props, lessons_props


def main():
    print("=" * 60)
    print("🔗 SG Real Estate System - Relations Setup")
    print("=" * 60)
    print()

    try:
        setup_leads_relations()
        setup_properties_relations()
        setup_activities_relations()
        setup_deals_relations()
        setup_knowledge_base_properties()

        print()
        print("=" * 60)
        print("🎉 RELATIONS SETUP COMPLETE!")
        print("=" * 60)
        print()
        print("Relations configured:")
        print("  • Leads ↔ Properties (Linked Property)")
        print("  • Leads ↔ Activities (Activities)")
        print("  • Leads ↔ Deals (Linked Deals)")
        print("  • Properties ↔ Activities (Viewings)")
        print("  • Deals → Leads (Lead)")
        print("  • Deals → Properties (Property)")
        print("  • Lessons → Activities (Related Activity)")
        print()
        print("Formulas configured:")
        print("  • PSF = Price / Size")
        print("  • Commission Est = Price × Commission %")
        print("  • Weighted Commission = Commission × Probability")
        print("  • Days Since Contact = days since Last Contact")
        print("  • Days in Stage = days since Created")
        print()
        print("Next: Open Notion and create filtered views manually")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
