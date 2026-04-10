# LeadFlow Pro - Complete Package

Welcome to LeadFlow Pro! This is your complete real estate lead generation system.

## What's Included

### 📦 Package Contents

```
LeadFlow_Pro/
├── SCRAPER/              # Python lead scraper
│   ├── scraper.py      # Main scraper script
│   ├── config.json     # Configuration template
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── NOTION_TEMPLATE/      # Notion CRM setup
│   ├── setup_notion_crm.py
│   └── README.md
├── GUIDE/                # User documentation
│   ├── LeadFlow_Pro_User_Guide.pdf
│   └── generate_pdf_guide.py
├── EMAIL_TEMPLATES/      # Follow-up sequences
│   └── follow_up_sequence.md
├── SALES/                # Sales materials
│   └── sales_page.md
└── README.md            # This file
```

## Quick Start

1. **Install the Scraper**
   ```bash
   cd SCRAPER
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Set Up Notion**
   ```bash
   cd NOTION_TEMPLATE
   export NOTION_API_KEY=your_key_here
   python setup_notion_crm.py
   ```

3. **Run Your First Scrape**
   ```bash
   cd SCRAPER
   python scraper.py --run-once
   ```

4. **Follow the PDF Guide**
   Open `GUIDE/LeadFlow_Pro_User_Guide.pdf` for complete instructions.

## System Requirements

- Python 3.8+
- Notion account (free tier works)
- Computer that can run 24/7 (optional, for scheduled scraping)

## Support

- **Basic Package:** PDF guide + READMEs
- **Pro Package:** Email support
- **Agency Package:** Priority support + community access

## License

This product is licensed for your personal/business use. Do not redistribute.

---

**Ready to fill your pipeline? Let's go! 🚀**