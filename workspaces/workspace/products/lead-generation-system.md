# AI Lead Generation System
## Complete B2B Lead Gen Agency Toolkit

**Version:** 1.0
**Created:** 2026-03-31
**Revenue Potential:** $1,500-3,000/month per client

---

## System Overview

**Business Model:** AI-Powered Lead Generation Agency
**Target:** Local service businesses (plumbers, electricians, roofers, dentists, etc.)
**Service:** Generate qualified leads → Sell to businesses → Charge monthly retainer

**Your Value Proposition:**
> "We generate 50+ qualified leads per month for your business using AI automation. You pay only for results."

---

## Phase 1: Market Research (Day 1)

### Identify Target Niches

**High-Value Local Niches:**
| Industry | Avg Lead Value | Competition | Ease of Scraping |
|----------|---------------|-------------|------------------|
| Roofing | $500-2,000 | Medium | Easy |
| Plumbing | $150-500 | High | Easy |
| Electrical | $200-800 | Medium | Easy |
| HVAC | $300-1,500 | Medium | Medium |
| Landscaping | $100-300 | High | Easy |
| Painting | $200-600 | High | Easy |
| Pest Control | $150-400 | Medium | Easy |
| Dentists | $200-800 | Low | Medium |
| Chiropractors | $150-500 | Low | Medium |
| Law Firms | $500-5,000 | Low | Hard |

**Recommended Starting Niches:**
1. **Roofing** — High ticket, urgent need
2. **Dentists** — Stable, repeat customers
3. **HVAC** — Seasonal demand, high value
4. **Pest Control** — Recurring service

---

## Phase 2: Lead Scraping System (Day 1-2)

### Google Maps Scraping

**Python Script:**
```python
#!/usr/bin/env python3
"""
Google Maps Lead Scraper
Requirements: playwright, beautifulsoup4
"""

import json
import time
from playwright.sync_api import sync_playwright

def scrape_google_maps(location, business_type):
    """
    Scrape business leads from Google Maps

    Args:
        location: City/region (e.g., "Miami, FL")
        business_type: Type of business (e.g., "roofing contractor")

    Returns:
        List of business dicts with name, address, phone, website
    """

    leads = []
    search_query = f"{business_type} in {location}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to Google Maps
        page.goto(f"https://www.google.com/maps/search/{search_query}")
        page.wait_for_load_state("networkidle")

        # Wait for results to load
        page.wait_for_selector("[data-result-index]", timeout=10000)

        # Get all business listings
        listings = page.query_selector_all("[data-result-index]")

        for listing in listings[:50]:  # Limit to 50 results
            try:
                # Click to open details
                listing.click()
                page.wait_for_timeout(1000)

                # Extract business info
                name = page.query_selector("h1").inner_text() if page.query_selector("h1") else ""
                address = page.query_selector("[data-tooltip='Address']").inner_text() if page.query_selector("[data-tooltip='Address']") else ""
                phone = page.query_selector("[data-tooltip='Phone']").inner_text() if page.query_selector("[data-tooltip='Phone']") else ""
                website = page.query_selector("a[data-tooltip='Website']").get_attribute("href") if page.query_selector("a[data-tooltip='Website']") else ""

                lead = {
                    "business_name": name,
                    "address": address,
                    "phone": phone,
                    "website": website,
                    "source": "Google Maps",
                    "scraped_date": time.strftime("%Y-%m-%d")
                }

                leads.append(lead)
                print(f"✓ Scraped: {name}")

                # Go back to results
                page.go_back()
                page.wait_for_timeout(500)

            except Exception as e:
                print(f"✗ Error scraping listing: {e}")
                continue

        browser.close()

    # Save to JSON
    filename = f"leads_{business_type.replace(' ', '_')}_{location.replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(leads, f, indent=2)

    print(f"\n✅ Scraped {len(leads)} leads")
    print(f"💾 Saved to: {filename}")

    return leads

# Example usage
if __name__ == "__main__":
    leads = scrape_google_maps("Miami, FL", "roofing contractor")
```

### Yelp Scraping (Alternative)

```python
#!/usr/bin/env python3
"""
Yelp Business Scraper
"""

import requests
from bs4 import BeautifulSoup
import json

def scrape_yelp(location, category):
    """
    Scrape businesses from Yelp
    """
    base_url = f"https://www.yelp.com/search?find_desc={category}&find_loc={location}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    leads = []

    for page in range(0, 50, 10):  # 5 pages
        url = f"{base_url}&start={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        businesses = soup.find_all('div', class_='businessName__09f24__EYSZE')

        for business in businesses:
            try:
                name = business.find('a').text
                link = business.find('a')['href']

                # Visit business page for details
                biz_url = f"https://www.yelp.com{link}"
                biz_response = requests.get(biz_url, headers=headers)
                biz_soup = BeautifulSoup(biz_response.content, 'html.parser')

                # Extract phone
                phone_elem = biz_soup.find('p', text=lambda t: t and 'phone' in t.lower())
                phone = phone_elem.text if phone_elem else ""

                # Extract website
                website_elem = biz_soup.find('a', text='Website')
                website = website_elem['href'] if website_elem else ""

                lead = {
                    "business_name": name,
                    "phone": phone,
                    "website": website,
                    "yelp_url": biz_url,
                    "source": "Yelp",
                    "scraped_date": time.strftime("%Y-%m-%d")
                }

                leads.append(lead)
                print(f"✓ {name}")

            except Exception as e:
                print(f"✗ Error: {e}")
                continue

    # Save results
    filename = f"yelp_{category.replace(' ', '_')}_{location.replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(leads, f, indent=2)

    return leads
```

---

## Phase 3: Email Enrichment (Day 2)

### Find Email Addresses

**Method 1: Domain guessing**
```python
def find_email_from_website(website, business_name):
    """
    Try common email patterns
    """
    import re

    # Extract domain
    domain = website.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]

    # Common patterns
    name_parts = business_name.lower().split()
    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""

    patterns = [
        f"info@{domain}",
        f"contact@{domain}",
        f"hello@{domain}",
        f"sales@{domain}",
        f"{first_name}@{domain}",
        f"{first_name}.{last_name}@{domain}",
        f"{first_name[0]}{last_name}@{domain}" if last_name else "",
    ]

    return list(set([p for p in patterns if p]))
```

**Method 2: Email verification**
```python
import requests

def verify_email(email):
    """
    Verify if email is valid using Hunter.io API (free tier: 50/month)
    """
    # Or use verification logic
    # For now, just check format
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

---

## Phase 4: Outreach Automation (Day 3)

### Email Templates

**Template 1: Cold Outreach**
```
Subject: 50+ qualified leads for {{business_name}} this month?

Hi {{first_name}},

I noticed {{business_name}} serves the {{location}} area.

I'm reaching out because we help {{business_type}} companies like yours generate qualified leads using AI automation.

**What we do:**
✓ Find 50+ homeowners actively looking for {{service}}
✓ Verify contact info (phone + email)
✓ Deliver hot leads to your inbox daily
✓ You close the deals

**Recent results:**
- {{competitor_name}} in {{nearby_city}}: 67 leads → 12 sales = $24,000 revenue

**Pricing:**
We only charge when you get results:
- Setup: $0
- Monthly: $297
- Or pay-per-lead: $25/qualified lead

Want to see a sample of 10 leads for your area?

Best regards,
{{your_name}}
{{your_company}}

P.S. No long-term contracts. Cancel anytime.
```

**Template 2: Follow-up (Day 3)**
```
Subject: Re: 50+ qualified leads for {{business_name}}

Hi {{first_name}},

Quick follow-up on my email from Tuesday.

I generated a sample list of 10 actual leads in {{location}} who need {{service}}:

1. {{lead_1_name}} - {{lead_1_address}} - {{lead_1_phone}}
2. {{lead_2_name}} - {{lead_2_address}} - {{lead_2_phone}}
...

These are real homeowners looking for help right now.

Want me to send you 50 more like these every month?

{{your_name}}
```

**Template 3: Value Add (Day 7)**
```
Subject: Free lead gen strategy for {{business_name}}

Hi {{first_name}},

I put together a quick video showing exactly how we'd generate leads for {{business_name}}:

[Video link or loom recording]

The 3-step process:
1. We scrape Google Maps for active projects
2. Verify homeowner contact info
3. Send you qualified leads daily

Would you like me to run this for {{business_name}} this week?

{{your_name}}
```

### Gmail Automation Script

```python
#!/usr/bin/env python3
"""
Gmail Automation for Lead Gen Outreach
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import time

class LeadGenMailer:
    def __init__(self, gmail_user, gmail_password):
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
        self.sent_count = 0

    def send_outreach(self, lead, template_file='template1.txt'):
        """
        Send personalized email to lead
        """

        # Load template
        with open(template_file, 'r') as f:
            template = Template(f.read())

        # Personalize
        email_body = template.render(
            business_name=lead['business_name'],
            first_name=lead.get('first_name', 'there'),
            location=lead.get('city', 'your area'),
            business_type=lead.get('category', 'service'),
            service=lead.get('service', 'your service'),
            your_name='Your Name',
            your_company='Your Company'
        )

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"50+ qualified leads for {lead['business_name']}"
        msg['From'] = self.gmail_user
        msg['To'] = lead['email']

        msg.attach(MIMEText(email_body, 'plain'))

        # Send
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.gmail_user, self.gmail_password)
            server.sendmail(
                self.gmail_user,
                lead['email'],
                msg.as_string()
            )
            server.quit()

            self.sent_count += 1
            print(f"✅ Sent to {lead['business_name']} ({lead['email']})")

            # Rate limiting
            time.sleep(2)

            return True

        except Exception as e:
            print(f"❌ Failed to send to {lead['email']}: {e}")
            return False

    def bulk_send(self, leads_file, template_file='template1.txt'):
        """
        Send to all leads in file
        """
        with open(leads_file, 'r') as f:
            leads = json.load(f)

        print(f"📧 Sending to {len(leads)} leads...\n")

        for lead in leads:
            if lead.get('email'):
                self.send_outreach(lead, template_file)
            else:
                print(f"⏭️ Skipping {lead['business_name']} - no email")

        print(f"\n✅ Campaign complete! Sent {self.sent_count} emails")

# Usage
if __name__ == "__main__":
    mailer = LeadGenMailer(
        gmail_user='your-email@gmail.com',
        gmail_password='your-app-password'
    )

    mailer.bulk_send('leads_roofing_miami.json', 'template1.txt')
```

---

## Phase 5: Client Delivery System (Day 4-5)

### Lead Delivery Dashboard

**Simple HTML Dashboard:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Lead Gen Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background: #4CAF50; color: white; }
        tr:nth-child(even) { background: #f2f2f2; }
        .metric { display: inline-block; margin: 10px 20px; padding: 15px; background: #f9f9f9; border-radius: 5px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #4CAF50; }
    </style>
</head>
<body>
    <h1>Lead Generation Dashboard</h1>

    <div class="metrics">
        <div class="metric">
            <div>Total Leads</div>
            <div class="metric-value">{{total_leads}}</div>
        </div>
        <div class="metric">
            <div>This Month</div>
            <div class="metric-value">{{monthly_leads}}</div>
        </div>
        <div class="metric">
            <div>Conversion Rate</div>
            <div class="metric-value">{{conversion_rate}}%</div>
        </div>
    </div>

    <h2>Recent Leads</h2>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Business Name</th>
                <th>Contact</th>
                <th>Phone</th>
                <th>Source</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for lead in leads %}
            <tr>
                <td>{{lead.date}}</td>
                <td>{{lead.business_name}}</td>
                <td>{{lead.contact_name}}</td>
                <td>{{lead.phone}}</td>
                <td>{{lead.source}}</td>
                <td>{{lead.status}}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

### Daily Lead Report Email

```python
def send_daily_report(client_email, new_leads):
    """
    Send daily lead report to client
    """

    report = f"""
    Daily Lead Report - {time.strftime('%Y-%m-%d')}

    Hi there,

    Here are your {len(new_leads)} new leads for today:

    """

    for i, lead in enumerate(new_leads, 1):
        report += f"""
    Lead #{i}
    Business: {lead['business_name']}
    Contact: {lead.get('contact_name', 'N/A')}
    Phone: {lead['phone']}
    Email: {lead.get('email', 'N/A')}
    Address: {lead.get('address', 'N/A')}
    Source: {lead['source']}
    ---
    """

    report += """
    Next steps:
    1. Call leads within 24 hours (hot leads go cold fast)
    2. Mention "referral from Google Maps" (they're expecting calls)
    3. Track conversions in your CRM

    Questions? Reply to this email.

    Best regards,
    Your Lead Gen Team
    """

    # Send via Gmail API
    send_email(client_email, f"Daily Leads - {len(new_leads)} New Opportunities", report)
```

---

## Pricing Models

### Option 1: Pay-Per-Lead
- **Price:** $25-50 per qualified lead
- **Minimum:** 10 leads/month
- **Best for:** Businesses testing the service

### Option 2: Monthly Retainer
- **Price:** $297-997/month
- **Includes:** 50-100 leads + email support
- **Best for:** Established businesses wanting consistency

### Option 3: Performance-Based
- **Price:** 10-20% of closed revenue
- **Tracking:** Unique phone numbers, promo codes
- **Best for:** High-trust partnerships

---

## Scaling the System

### Month 1: Proof of Concept
- [ ] Pick 1 niche (roofing)
- [ ] Scrape 500 leads
- [ ] Enrich with emails
- [ ] Send 100 cold emails
- [ ] Close 1-2 clients
- [ ] Deliver leads manually

### Month 2: Automation
- [ ] Automate scraping (daily)
- [ ] Automate enrichment
- [ ] Automate outreach
- [ ] Build dashboard
- [ ] Scale to 5 clients

### Month 3: Expansion
- [ ] Add 2 more niches
- [ ] Hire VA for manual tasks
- [ ] Build referral system
- [ ] Target 20 clients
- [ ] Revenue: $5,000-10,000/month

---

## Tools & Resources

### Software Stack
| Tool | Purpose | Cost |
|------|---------|------|
| Playwright | Scraping | Free |
| Python | Automation | Free |
| Gmail | Email sending | Free |
| Hunter.io | Email finding | $0-49/month |
| Google Sheets | Lead tracking | Free |
| Make.com/Zapier | Workflows | $0-20/month |

### Skills Needed
- Basic Python scripting
- Web scraping (Playwright/Selenium)
- Email copywriting
- Sales (closing clients)

---

## Troubleshooting

**Low response rate?**
- Test different subject lines
- Personalize more (mention specific projects)
- Follow up 3-5 times
- Try LinkedIn instead of email

**Leads not converting?**
- Improve lead quality (more verification)
- Better handoff (warm intro vs cold)
- Client training (how to close)

**Scraping blocked?**
- Use proxies
- Rotate user agents
- Add delays between requests
- Use headless browser carefully

---

## Next Steps

### Immediate Actions (Today):
1. [ ] Choose niche (roofing recommended)
2. [ ] Set up Python environment
3. [ ] Install Playwright
4. [ ] Test Google Maps scraping

### This Week:
1. [ ] Scrape 500 leads
2. [ ] Enrich with emails
3. [ ] Send 50 test emails
4. [ ] Track responses

### This Month:
1. [ ] Close first client
2. [ ] Deliver first 50 leads
3. [ ] Get testimonial
4. [ ] Scale outreach

---

**Revenue Target:** $1,000/month = 20 leads @ $50 or 4 clients @ $250

**Timeline:** First client in 2 weeks, $1,000/month by week 6.

---

**System Status:** READY TO DEPLOY
**Version:** 1.0
**Last Updated:** 2026-03-31
