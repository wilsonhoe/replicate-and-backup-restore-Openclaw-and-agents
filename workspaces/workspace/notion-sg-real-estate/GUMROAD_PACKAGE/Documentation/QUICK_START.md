# 🏠 SG Property Pro - Quick Start Guide

## ⚠️ IMPORTANT: Why You Can't See the Data

**The Notion API creates pages in the integration's workspace, not yours.** This is a Notion security feature - you cannot access pages created by API in another workspace.

### Solution: Build Your Own Copy

I've created **import-ready files** so you can build this system in your own Notion workspace (works on **FREE tier**).

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create Main Page (1 min)

1. In **your** Notion, create new page: `SG Property Pro`
2. Add icon: 🏠
3. Add this description:
   > Singapore Real Estate CRM - Track leads, properties, deals, and activities

### Step 2: Create Leads Database (2 min)

1. Type `/database inline`
2. Name: `Leads`
3. Set up properties:

| Property | Type | Options |
|----------|------|---------|
| Name | Title | - |
| Contact | Phone | - |
| Email | Email | - |
| Source | Select | 🚪 Door Knocking, 👨‍👩‍👧 Referral, 💻 Online, 📱 Social Media, 🏢 Walk-in |
| Property Interest | Multi-select | 🏢 HDB, 🏠 Condo, 🏘️ EC, 🏡 Landed |
| Budget Range | Select | <$500K, $500K-$800K, $800K-$1.2M, $1.2M-$2M, >$2M |
| Status | Select | 🆕 New, 📞 Contacted, 👀 Viewing Scheduled, 💰 Offer Made, ✅ Closed, ❌ Lost |
| Priority | Select | 🔥 Hot, ⚡ Warm, ❄️ Cold |
| Last Contact | Date | - |
| Next Follow-up | Date | - |
| Notes | Text | - |

4. Add 3 sample leads:

| Name | Contact | Status | Priority | Next Follow-up |
|------|---------|--------|----------|----------------|
| Tan Wei Ming | +6591234567 | 💰 Offer Made | 🔥 Hot | Today |
| Lim Shu Qi | +6592345678 | 👀 Viewing | 🔥 Hot | Tomorrow |
| Chen Jia Hao | +6593456789 | 📝 OTP Issued | 🔥 Hot | Apr 10 |

### Step 3: Import Sample Data (2 min)

**Option A: CSV Import (Easiest)**
1. Click `...` on database → `Merge with CSV`
2. Upload `leads.csv`
3. Map columns → Done!

**Option B: Copy-Paste**
1. Open `leads.csv`
2. Copy rows
3. Paste into Notion database

---

## 📂 All Template Files

| File | Purpose | How to Use |
|------|---------|------------|
| `README.md` | Full documentation | Read first |
| `QUICK_START.md` | This file | Quick reference |
| `TEMPLATE_SETUP_GUIDE.md` | Step-by-step setup | Detailed instructions |
| `template-export.md` | Complete content | Copy-paste into Notion |
| `leads.csv` | 10 sample leads | CSV import |
| `properties.csv` | 8 sample properties | CSV import |
| `activities.csv` | 8 sample activities | CSV import |
| `deals.csv` | 6 sample deals | CSV import |
| `knowledge_base.csv` | 14 KB items | CSV import |

---

## 🗂️ Complete Database Schemas

### 2. Properties Database

| Property | Type | Options/Formula |
|----------|------|-----------------|
| Property Name | Title | - |
| Address | Text | - |
| Type | Select | 🏢 HDB, 🏠 Condo, 🏘️ EC, 🏡 Landed |
| District | Select | D1, D2... D28 |
| Area | Select | 🚇 Punggol, 🚇 Sengkang, 🚇 Hougang, 🚇 Serangoon, CBD, Other |
| Price | Number | SGD |
| Size (sqft) | Number | - |
| PSF | Formula | `prop("Price") / prop("Size (sqft)")` |
| Bedrooms | Select | 1, 2, 3, 4, 5+ |
| Status | Select | ✅ Available, 📝 Under Offer, ❌ Sold, 🔒 Off Market |
| Listing Date | Date | - |
| Seller Contact | Phone | - |
| Notes | Text | - |

### 3. Activities Database

| Property | Type | Options |
|----------|------|---------|
| Activity Name | Title | - |
| Date | Date | - |
| Type | Select | 🚪 Door Knocking, ☎️ Cold Call, 📧 Follow-up, 👀 Viewing, 🤝 Meeting, 💻 Research |
| Area | Select | 🚇 Punggol, 🚇 Sengkang, 🚇 Hougang, 🚇 Serangoon, CBD, Other |
| Outcome | Select | ✅ Lead Generated, 📞 Callback Scheduled, ❌ No Answer, 🚫 Not Interested, 📊 Market Intel |
| Leads Generated | Number | - |
| Conversations | Number | - |
| Duration (mins) | Number | - |
| Notes | Text | - |
| Added to KB | Checkbox | - |

### 4. Deals Database

| Property | Type | Options/Formula |
|----------|------|-----------------|
| Deal Name | Title | - |
| Stage | Select | 🆕 New, 👀 Viewing, 💰 Offer Made, 📝 OTP Issued, ✅ OTP Exercised, 📋 Resale Application, 🏛️ HDB Acceptance, 🔨 Legal Completion, ✅ Closed, ❌ Lost |
| Deal Type | Select | 🏢 HDB → HDB, 🏢 HDB → 🏠 Private, 🏠 Private → 🏠 Private |
| Price | Number | SGD |
| Commission % | Number | e.g., 0.02 |
| Est. Commission | Formula | `prop("Price") * prop("Commission %")` |
| Probability | Select | 10%, 25%, 50%, 75%, 90%, 100% |
| Weighted Commission | Formula | `prop("Est. Commission") * (toNumber(replaceAll(prop("Probability"), "%", "")) / 100)` |
| Expected Close | Date | - |
| OTP Date | Date | - |
| OTP Exercise Date | Date | - |
| Next Action | Text | - |
| Next Action Due | Date | - |
| Notes | Text | - |

### 5. Knowledge Base Database

| Property | Type | Options |
|----------|------|---------|
| Title | Title | - |
| Type | Select | 🚪 Door Knocking Script, ☎️ Cold Call Script, ❌ Objection Handling, 📧 Follow-up Template, 🤝 Closing Script, 📈 Market Insight, 💡 Lesson Learned |
| Content | Text | - |
| Tags | Multi-select | HDB, Condo, EC, Landed, First-time buyer |
| Success Rate | Select | High, Medium, Low |
| Last Used | Date | - |
| Source | Text | - |
| Date | Date | - |
| Impact | Select | High, Medium, Low |
| Context | Select | ✅ What Worked, ❌ What Didn't, 💡 Insight |
| Action Item | Text | - |

---

## 📊 Dashboard Setup

Create a "Dashboard" subpage with these sections:

### 1. 📊 KPI Overview (Callout)
```
🎯 Active Leads: 10 | 💰 Pipeline: $189K | 📈 Weighted: $142K | ⏰ Follow-ups: 4
```

### 2. 🔥 Hot Leads
- Type `/link` → Select Leads database
- Add filter: Priority = 🔥 Hot

### 3. 💼 Active Deals Pipeline
- Link to Deals database
- Filter: Stage ≠ ✅ Closed, ❌ Lost

### 4. 📅 Recent Activities
- Link to Activities database
- Filter: Date = This week

### 5. 🚇 NEL Zone Summary (Bulleted list)
```
🚇 Punggol: 4 leads | 3 activities | 2 deals | 📈 Up
🚇 Sengkang: 3 leads | 2 activities | 1 deal | → Stable
🚇 Hougang: 2 leads | 2 activities | 1 deal | 📈 Up
🚇 Serangoon: 1 lead | 1 activity | → Stable
```

### 6. 📚 Knowledge Base
- Link to Knowledge Base database

### 7. ⚡ Quick Actions (Bulleted list)
```
➕ Add New Lead — Go to Leads database
📝 Log Activity — Track door knocking, calls
🏠 Add Property — New listing
💼 Create Deal — Link lead to property
```

---

## 💡 Sample Scripts (for Knowledge Base)

### Door Knocking Opener
> "Hi! I'm a property consultant helping homeowners in this area. I noticed some recent transactions and wanted to check if you might be considering a move?"

### Cold Call Script
> "Hello, this is [name] from [agency]. I'm calling because I saw your property listing expired. Are you still looking to sell?"

### Handling Price Objection
> "I understand your concern about the price. Let me show you some recent comparable sales in this area to help set realistic expectations."

---

## 🎯 Sample Data Summary

**10 Leads:** Mix of Hot/Warm/Cold, various property types and budgets

**8 Properties:** HDB, Condo, EC, Landed across NEL corridor

**8 Activities:** Door knocking, calls, viewings, meetings

**6 Deals:** Various stages with commission calculations

**14 KB Items:** Scripts, insights, lessons learned

---

## 📱 Daily Workflow Tips

1. **Morning:** Check 🔥 Hot Leads for follow-ups due
2. **After activities:** Log immediately (door knocking, calls, viewings)
3. **End of day:** Update deal stages within 24 hours
4. **Weekly:** Review Knowledge Base before client meetings
5. **After wins/losses:** Add lessons learned

---

## ❓ Troubleshooting

**"I don't see the API data"**
→ Normal! The API creates data in another workspace. Use the CSV files to import into your own workspace.

**"CSV import fails"**
→ Create database properties FIRST (with exact names), then import.

**"Formulas show errors"**
→ Property names must match EXACTLY (case-sensitive, no extra spaces).

**"Can't see databases"**
→ You need to create them in YOUR workspace first. The files provide the schemas and sample data.

---

## 🎁 What You Get

✅ Complete database schemas for 5 databases
✅ 45+ sample data records (leads, properties, activities, deals, KB)
✅ Singapore-specific fields (HDB, OTP workflow, D1-28 districts)
✅ NEL zone tracking (Punggol, Sengkang, Hougang, Serangoon)
✅ Sales scripts library
✅ Market insights
✅ Commission formulas with probability weighting
✅ Daily workflow tips

---

## 🏆 Next Steps

1. **Create the main page** in your Notion
2. **Create all 5 databases** with correct properties
3. **Import sample data** using CSV files
4. **Set up the Dashboard** with linked database views
5. **Start using!** Add your real leads and properties

**Full instructions:** See `TEMPLATE_SETUP_GUIDE.md`

---

**Version:** 1.0  
**Created:** 2026-04-05  
**For:** Singapore Real Estate Agents (Free & Paid Notion tiers)
