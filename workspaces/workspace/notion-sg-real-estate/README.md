# SG Property Pro - Singapore Real Estate Notion Template

## Problem Solved

The Notion API creates content in the **integration's workspace**, not your personal workspace. This means you cannot see the data created via API - it's a Notion limitation that affects free tier users.

## Solution: Import-Ready Template Files

I've created everything you need to build this system in your own Notion workspace:

### Quick Setup Options

#### Option 1: Copy-Paste Setup (Easiest, Free Tier Friendly)

1. **Open `TEMPLATE_SETUP_GUIDE.md`** - Complete step-by-step instructions
2. Follow the database schemas to create your own databases
3. Copy the sample data from the markdown tables
4. Total setup time: ~30 minutes

#### Option 2: CSV Import (Notion Free Tier)

Use the included CSV files to bulk import sample data:

1. Create each database in Notion with the correct properties (see schemas below)
2. Go to database → "..." → "Merge with CSV"
3. Upload the corresponding CSV file
4. Map columns to properties

**Available CSVs:**
- `leads.csv` - 10 sample leads
- `properties.csv` - 8 sample properties
- `activities.csv` - 8 sample activities
- `deals.csv` - 6 sample deals
- `knowledge_base.csv` - 14 scripts, insights, and lessons

#### Option 3: Markdown Import (Notion Free Tier)

1. Open `template-export.md`
2. Copy all content
3. In Notion, create a new page
4. Paste the content - Notion will auto-convert headings, lists, and tables

### Database Schemas

#### 1. Leads Database

**Properties:**
- `Name` (Title)
- `Contact` (Phone)
- `Email` (Email)
- `Source` (Select): 🚪 Door Knocking, 👨‍👩‍👧 Referral, 💻 Online, 📱 Social Media, 🏢 Walk-in
- `Property Interest` (Multi-select): 🏢 HDB, 🏠 Condo, 🏘️ EC, 🏡 Landed
- `Budget Range` (Select): <$500K, $500K-$800K, $800K-$1.2M, $1.2M-$2M, >$2M
- `Status` (Select): 🆕 New, 📞 Contacted, 👀 Viewing Scheduled, 💰 Offer Made, ✅ Closed, ❌ Lost
- `Priority` (Select): 🔥 Hot, ⚡ Warm, ❄️ Cold
- `Last Contact` (Date)
- `Next Follow-up` (Date)
- `Notes` (Text)

#### 2. Properties Database

**Properties:**
- `Property Name` (Title)
- `Address` (Text)
- `Type` (Select): 🏢 HDB, 🏠 Condo, 🏘️ EC, 🏡 Landed
- `District` (Select): D1-D28
- `Area` (Select): 🚇 Punggol, 🚇 Sengkang, 🚇 Hougang, 🚇 Serangoon, CBD, Other
- `Price` (Number - SGD)
- `Size (sqft)` (Number)
- `PSF` (Formula): `prop("Price") / prop("Size (sqft)")`
- `Bedrooms` (Select): 1, 2, 3, 4, 5+
- `Status` (Select): ✅ Available, 📝 Under Offer, ❌ Sold, 🔒 Off Market
- `Listing Date` (Date)
- `Seller Contact` (Phone)
- `Notes` (Text)

#### 3. Activities Database

**Properties:**
- `Activity Name` (Title)
- `Date` (Date)
- `Type` (Select): 🚪 Door Knocking, ☎️ Cold Call, 📧 Follow-up, 👀 Viewing, 🤝 Meeting, 💻 Research
- `Area` (Select): 🚇 Punggol, 🚇 Sengkang, 🚇 Hougang, 🚇 Serangoon, CBD, Other
- `Outcome` (Select): ✅ Lead Generated, 📞 Callback Scheduled, ❌ No Answer, 🚫 Not Interested, 📊 Market Intel
- `Leads Generated` (Number)
- `Conversations` (Number)
- `Duration (mins)` (Number)
- `Notes` (Text)
- `Added to KB` (Checkbox)

#### 4. Deals Database

**Properties:**
- `Deal Name` (Title)
- `Stage` (Select): 🆕 New, 👀 Viewing, 💰 Offer Made, 📝 OTP Issued, ✅ OTP Exercised, 📋 Resale Application, 🏛️ HDB Acceptance, 🔨 Legal Completion, ✅ Closed, ❌ Lost
- `Deal Type` (Select): 🏢 HDB → HDB, 🏢 HDB → 🏠 Private, 🏠 Private → 🏠 Private
- `Price` (Number - SGD)
- `Commission %` (Number)
- `Est. Commission` (Formula): `prop("Price") * prop("Commission %")`
- `Probability` (Select): 10%, 25%, 50%, 75%, 90%, 100%
- `Weighted Commission` (Formula): `prop("Est. Commission") * (toNumber(replaceAll(prop("Probability"), "%", "")) / 100)`
- `Expected Close` (Date)
- `OTP Date` (Date)
- `OTP Exercise Date` (Date)
- `Next Action` (Text)
- `Next Action Due` (Date)
- `Notes` (Text)

#### 5. Knowledge Base Database

**Properties:**
- `Title` (Title)
- `Type` (Select): 🚪 Door Knocking Script, ☎️ Cold Call Script, ❌ Objection Handling, 📧 Follow-up Template, 🤝 Closing Script, 📈 Market Insight, 💡 Lesson Learned
- `Content` (Text)
- `Tags` (Multi-select): HDB, Condo, EC, Landed, First-time buyer
- `Success Rate` (Select): High, Medium, Low
- `Last Used` (Date)
- `Source` (Text) - for market insights
- `Date` (Date) - for insights/lessons
- `Impact` (Select): High, Medium, Low
- `Context` (Select): ✅ What Worked, ❌ What Didn't, 💡 Insight
- `Action Item` (Text)

### Dashboard Setup

Create a "Dashboard" subpage with these sections:

1. **📊 KPI Overview** - Summary of key metrics
2. **🔥 Hot Leads** - Link to Leads database filtered by Priority = 🔥 Hot
3. **💼 Active Deals Pipeline** - Link to Deals database filtered by Stage ≠ Closed/Lost
4. **📅 Recent Activities** - Link to Activities database filtered by Date = This week
5. **🚇 NEL Zone Activity Summary** - Manual summary table
6. **🔥 Hot Properties** - Link to Properties database filtered by Status = Available
7. **📚 Knowledge Base** - Link to Knowledge Base database
8. **⚡ Quick Actions** - Links to add new entries
9. **💡 Daily Workflow Tips** - Numbered list of best practices

### Sample Data Included

**10 Leads** with Singapore names, phone numbers, and realistic property interests

**8 Properties** across Punggol, Sengkang, Hougang, Serangoon with correct PSF calculations

**8 Activities** including door knocking, cold calls, viewings, and meetings

**6 Deals** in various stages with commission calculations

**14 Knowledge Base items**:
- 5 Sales scripts (door knocking, cold call, objection handling, follow-up, closing)
- 5 Market insights (price trends, new launches, policy changes)
- 4 Lessons learned from field experience

### Scripts Library

#### Door Knocking Opener
```
"Hi! I'm a property consultant helping homeowners in this area. I noticed some recent transactions and wanted to check if you might be considering a move?"
```

#### Cold Call Script
```
"Hello, this is [name] from [agency]. I'm calling because I saw your property listing expired. Are you still looking to sell?"
```

#### Handling Price Objection
```
"I understand your concern about the price. Let me show you some recent comparable sales in this area to help set realistic expectations."
```

### Key Metrics Tracked

- **Active Leads**: 10
- **Commission Pipeline**: ~$189,400
- **Weighted Pipeline**: ~$142,050 (probability-adjusted)
- **Follow-ups Due**: 4

### NEL Zone Coverage

The template is optimized for Singapore's North-East Line (NEL) corridor:
- 🚇 Punggol: 4 leads, 3 activities, 2 active deals
- 🚇 Sengkang: 3 leads, 2 activities, 1 active deal
- 🚇 Hougang: 2 leads, 2 activities, 1 active deal
- 🚇 Serangoon: 1 lead, 1 activity

### Files Included

| File | Purpose |
|------|---------|
| `README.md` | This guide |
| `TEMPLATE_SETUP_GUIDE.md` | Detailed setup instructions |
| `template-export.md` | Complete template content for copy-paste |
| `leads.csv` | Sample leads data |
| `properties.csv` | Sample properties data |
| `activities.csv` | Sample activities data |
| `deals.csv` | Sample deals data |
| `knowledge_base.csv` | Sample knowledge base data |

### For Template Sellers

If you want to sell this as a template:

1. **Create a Public Template**:
   - Build the system in your Notion workspace
   - Share → Copy link → Set to "Anyone with the link can view"
   - Submit to Notion Template Gallery

2. **Gumroad/Gumlet**:
   - Create a duplicate link
   - Sell the duplicate link via Gumroad
   - Include setup instructions PDF

3. **Gumroad + Setup Service**:
   - Sell the template
   - Offer setup service for $50-100
   - Import all data for the buyer

### Support

This template is designed specifically for Singapore real estate agents and includes:
- Singapore property types (HDB, Condo, EC, Landed)
- District codes (D1-D28)
- OTP workflow stages
- Singapore phone number format
- NEL zone areas (Punggol, Sengkang, Hougang, Serangoon)

### License

Free to use, modify, and sell. No attribution required.
