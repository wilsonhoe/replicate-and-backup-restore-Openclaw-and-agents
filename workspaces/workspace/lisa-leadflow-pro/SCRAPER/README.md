# LeadFlow Pro - Real Estate Lead Scraper

Automated lead generation system for real estate agents.

## Features

- Scrape property listings from multiple cities
- Extract lead information (name, phone, email, budget)
- Auto-export to Notion CRM
- Schedule automated runs
- Duplicate detection

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd leadflow-scraper

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Edit `config.json`:

```json
{
  "cities": ["New York", "Los Angeles", "Chicago"],
  "property_types": ["house", "condo", "apartment"],
  "price_range": {
    "min": 200000,
    "max": 2000000
  },
  "schedule": {
    "enabled": true,
    "interval_hours": 6
  },
  "notion": {
    "api_key": "your_notion_api_key",
    "database_id": "your_leads_database_id"
  }
}
```

## Usage

### Run Once
```bash
python scraper.py --run-once
```

### Start Scheduled Scraper
```bash
python scraper.py --daemon
```

### Export to Notion
```bash
python export_to_notion.py --input leads.csv
```

## Supported Sources

- Zillow (via unofficial API)
- Realtor.com
- Local MLS listings (via configured endpoints)

## Output Format

Leads are saved to `leads.csv` with columns:
- name
- phone
- email
- budget
- property_interest
- source
- scraped_date
- status

## License

Included with LeadFlow Pro purchase.

## Support

For support, contact: support@leadflowpro.com