---
name: Notion Real Estate System Creator
description: Create complete Notion systems with databases, sample data, and beautiful PDF user guides for real estate operations
tools: [Read, Write, Edit, Bash, Glob]
---

# Notion Real Estate System Creator

Skill for creating comprehensive Notion-based real estate management systems with accompanying documentation and user guides.

## When to Use

Use this skill when:
- Building Notion-based CRM or field activity tracking systems for real estate
- Creating databases with relations (Sessions ↔ Leads ↔ Follow-ups)
- Populating sample data via Notion API
- Generating professional PDF user guides from Markdown
- Need mobile-first systems for agents on the move

## How It Works

### 1. System Architecture

The Door Knocking Mastery System consists of 6 interconnected databases:

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────┐
│  Door Knocking  │────→│    Leads    │────→│  Follow-ups │
│    Sessions     │     └──────┬──────┘     └─────────────┘
└─────────────────┘            │
         │                       │
         ↓                       ↓
┌─────────────────┐     ┌─────────────┐
│ Weekly Reviews  │     │   Scripts   │
└─────────────────┘     └─────────────┘
         ↑
┌─────────────────┐
│  Training Log   │
└─────────────────┘
```

**Database Relations:**
- Sessions → Leads (1:N): Each session generates multiple leads
- Leads → Follow-ups (1:N): Each lead requires multiple touchpoints
- Sessions → Weekly Reviews (N:1): Multiple sessions reviewed together

### 2. Notion API Population

**Prerequisites:**
- Notion API key with integration permissions
- Parent page where databases will be created
- Python 3 with `requests` library

**Database Schema Pattern:**
```python
# Example: Door Knocking Sessions database
{
    "parent": {"database_id": parent_id},
    "title": [{"text": {"content": "🚪 Door Knocking Sessions"}}],
    "properties": {
        "Session Date": {"date": {}},
        "Area": {"select": {"options": [...]}},
        "Doors Knocked": {"number": {"format": "number"}},
        "Conversations": {"number": {}},
        "Leads Generated": {"number": {}},
        "Status": {"select": {"options": [
            {"name": "Planned", "color": "gray"},
            {"name": "In Progress", "color": "yellow"},
            {"name": "Completed", "color": "green"}
        ]}},
        "Notes": {"rich_text": {}}
    }
}
```

**Data Population Pattern:**
```python
# Parse CSV and create entries
def populate_database(database_id, csv_file):
    rows = csv.DictReader(open(csv_file))
    for row in rows:
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Property Name": {"title": [{"text": {"content": row["name"]}}]},
                "Price": {"number": parse_price(row["price"])},
                # ... other fields
            }
        }
        requests.post(f"{BASE_URL}/pages", headers=HEADERS, json=data)
```

### 3. PDF Generation

**Process:**
1. Write comprehensive Markdown guide (`USER_GUIDE.md`)
2. Use Python + WeasyPrint for professional PDF output
3. Apply CSS styling for visual appeal:
   - Gradient cover pages
   - Section headers with icons
   - Callout boxes (tips, warnings, info)
   - Step cards with numbered indicators
   - Styled tables with shadows
   - Checklists for daily routines

**Tools Required:**
```bash
pip3 install markdown weasyprint --break-system-packages
```

**CSS Design System:**
- Primary: `#1a365d` (dark blue)
- Secondary: `#2b6cb0` (medium blue)
- Accent: `#3182ce` (bright blue)
- Backgrounds: Gradient overlays
- Typography: Playfair Display (headers), Inter (body)

### 4. File Structure

```
workspace/
├── USER_GUIDE.md                     # Source Markdown
├── convert_to_pdf.py                  # PDF generation script
├── populate_door_knocking.py          # Notion API population
├── create_main_dashboard.py           # Dashboard creation
├── Singapore_Real_Estate_User_Guide_Beautiful.pdf
├── DOOR_KNOCKING_SYSTEM/
│   ├── Templates/
│   │   ├── door_knocking_sessions.csv
│   │   ├── leads.csv
│   │   ├── follow_ups.csv
│   │   ├── scripts.csv
│   │   ├── training_sessions.csv
│   │   └── weekly_reviews.csv
│   └── Documentation/
│       ├── QUICK_START.md
│       ├── SALES_SCRIPTS.md
│       └── SETUP_GUIDE.md
└── GUMROAD_PACKAGE/
    ├── Marketing/
    ├── INDEX.md
    └── FEATURE-COMPARISON.md
```

## Examples

### Example 1: Creating a Database

```python
import requests

API_KEY = "ntn_your_api_key"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
BASE_URL = "https://api.notion.com/v1"

def create_database(parent_page_id, title, properties):
    data = {
        "parent": {"page_id": parent_page_id},
        "title": [{"text": {"content": title}}],
        "properties": properties
    }
    response = requests.post(f"{BASE_URL}/databases", headers=HEADERS, json=data)
    return response.json()["id"]
```

### Example 2: Generating Styled PDF

```python
from weasyprint import HTML
import markdown

# Convert MD to HTML with CSS
md_content = open('USER_GUIDE.md').read()
html_content = markdown.markdown(md_content, extensions=['tables'])

# Add styled wrapper
styled_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @page {{ margin: 2cm; }}
        body {{ font-family: Georgia, serif; font-size: 11pt; }}
        h1 {{ color: #1a365d; border-bottom: 3px solid #1a365d; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #1a365d; color: white; padding: 10px; }}
        td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
    </style>
</head>
<body>{html_content}</body>
</html>
"""

# Generate PDF
HTML(string=styled_html).write_pdf('User_Guide.pdf')
```

### Example 3: Mobile-First Database Design

Design databases for quick mobile entry:
- Use Select properties (dropdowns) over free text
- Number properties with validation
- Rich text for notes with voice-to-text
- Date properties with calendar picker
- Checkbox properties for quick toggles

## Key Insights

**Database Design Principles:**
- Use emoji in titles for visual identification
- Create relations between databases for linked records
- Select properties > text for data consistency
- Number formats for KPIs (percentage, currency)

**Mobile Optimization:**
- Test data entry on mobile before finalizing
- Use voice-to-text for notes fields
- Photo capture for property/lead documentation
- Quick-tap checkboxes for status updates

**PDF Best Practices:**
- A4 format for print compatibility
- Page numbers at bottom center
- Section breaks for each major topic
- Tables for benchmarks and KPIs
- Checklists for daily routines
- Tips/warnings in colored boxes

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Database creation fails (400) | Ensure title property exists in schema |
| Page creation fails | Use database_id as parent, not page_id |
| Numeric values rejected | Parse "172 doors" → 172 before sending |
| PDF generation fails | Install weasyprint dependencies: `sudo apt-get install libcairo2` |
| Browser sandbox error | Use weasyprint instead of headless Chrome |
| Rate limiting | Add delays: `time.sleep(0.3)` between requests |

## Related Skills

- `python-patterns` — For API client structure
- `pdf-generation` — For advanced PDF features
- `notion-api` — For database operations

## Resources

- Notion API Docs: https://developers.notion.com/
- WeasyPrint Docs: https://doc.courtbouillon.org/weasyprint/
- Real Estate KPIs: Open Rate, Conversation Rate, Lead Rate, Appointment Rate
