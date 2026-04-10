# SG Property Pro - Template Setup Guide (Free Tier Friendly)

## The Problem
The Notion API creates pages in the integration's workspace, not yours. You cannot access them directly.

## Solution: Create Your Own Copy

### Option 1: Manual Template Creation (Recommended for Free Tier)

I've created a complete template structure you can recreate in your own Notion workspace:

#### Step 1: Create the Main Page
1. In your Notion, create a new page called "SG Property Pro"
2. Add an icon (🏠) and cover image
3. Write this description: "Singapore Real Estate CRM - Track leads, properties, deals, and activities"

#### Step 2: Create 5 Databases

**Database 1: Leads**
- Properties:
  - Name (Title)
  - Contact (Phone)
  - Email (Email)
  - Source (Select: 🚪 Door Knocking, 👨‍👩‍👧 Referral, 💻 Online, 📱 Social Media, 🏢 Walk-in)
  - Property Interest (Multi-select: 🏢 HDB, 🏠 Condo, 🏘️ EC, 🏡 Landed)
  - Budget Range (Select: <$500K, $500K-$800K, $800K-$1.2M, $1.2M-$2M, >$2M)
  - Status (Select: 🆕 New, 📞 Contacted, 👀 Viewing Scheduled, 💰 Offer Made, ✅ Closed, ❌ Lost)
  - Priority (Select: 🔥 Hot, ⚡ Warm, ❄️ Cold)
  - Last Contact (Date)
  - Next Follow-up (Date)
  - Notes (Text)

**Database 2: Properties**
- Properties:
  - Property Name (Title)
  - Address (Text)
  - Type (Select: 🏢 HDB, 🏠 Condo, 🏘️ EC, 🏡 Landed)
  - District (Select: D1-D28)
  - Area (Select: 🚇 Punggol, 🚇 Sengkang, 🚇 Hougang, 🚇 Serangoon, CBD, Other)
  - Price (Number - SGD)
  - Size (sqft) (Number)
  - PSF (Formula: prop("Price") / prop("Size (sqft)"))
  - Bedrooms (Select: 1, 2, 3, 4, 5+)
  - Status (Select: ✅ Available, 📝 Under Offer, ❌ Sold, 🔒 Off Market)
  - Listing Date (Date)
  - Seller Contact (Phone)
  - Notes (Text)

**Database 3: Activities**
- Properties:
  - Activity Name (Title)
  - Date (Date)
  - Type (Select: 🚪 Door Knocking, ☎️ Cold Call, 📧 Follow-up, 👀 Viewing, 🤝 Meeting, 💻 Research)
  - Area (Select: 🚇 Punggol, 🚇 Sengkang, 🚇 Hougang, 🚇 Serangoon, CBD, Other)
  - Outcome (Select: ✅ Lead Generated, 📞 Callback Scheduled, ❌ No Answer, 🚫 Not Interested, 📊 Market Intel)
  - Leads Generated (Number)
  - Conversations (Number)
  - Duration (mins) (Number)
  - Notes (Text)
  - Added to KB (Checkbox)

**Database 4: Deals**
- Properties:
  - Deal Name (Title)
  - Stage (Select: 🆕 New, 👀 Viewing, 💰 Offer Made, 📝 OTP Issued, ✅ OTP Exercised, 📋 Resale Application, 🏛️ HDB Acceptance, 🔨 Legal Completion, ✅ Closed, ❌ Lost)
  - Deal Type (Select: 🏢 HDB → HDB, 🏢 HDB → 🏠 Private, 🏠 Private → 🏠 Private)
  - Price (Number - SGD)
  - Commission % (Number)
  - Est. Commission (Formula: prop("Price") * prop("Commission %"))
  - Probability (Select: 10%, 25%, 50%, 75%, 90%, 100%)
  - Weighted Commission (Formula: prop("Est. Commission") * (toNumber(replaceAll(prop("Probability"), "%", "")) / 100))
  - Expected Close (Date)
  - OTP Date (Date)
  - OTP Exercise Date (Date)
  - Next Action (Text)
  - Next Action Due (Date)
  - Notes (Text)

**Database 5: Knowledge Base**
- Properties:
  - Title (Title)
  - Type (Select: 🚪 Door Knocking Script, ☎️ Cold Call Script, ❌ Objection Handling, 📧 Follow-up Template, 🤝 Closing Script, 📈 Market Insight, 💡 Lesson Learned)
  - Content (Text)
  - Tags (Multi-select: HDB, Condo, EC, Landed, First-time buyer)
  - Success Rate (Select: High, Medium, Low)
  - Last Used (Date)
  - Source (Text)
  - Date (Date)
  - Impact (Select: High, Medium, Low)
  - Context (Select: ✅ What Worked, ❌ What Didn't, 💡 Insight)
  - Action Item (Text)

#### Step 3: Create Dashboard Page

Create a subpage called "Dashboard" and add these sections:

**📊 KPI Overview**
- Active Leads: [count from Leads]
- Commission Pipeline: Sum of Est. Commission from Deals
- Weighted Pipeline: Sum of Weighted Commission from Deals
- Follow-ups Due: Count from Leads (Next Follow-up)

**🔥 Hot Leads**
Link to Leads database filtered by Priority = 🔥 Hot

**💼 Active Deals Pipeline**
Link to Deals database filtered by Stage ≠ ✅ Closed, ❌ Lost

**📅 Recent Activities**
Link to Activities database filtered by Date = This week

**🚇 NEL Zone Activity Summary**
Create a table view showing:
- Punggol: [X] leads | [Y] activities | [Z] deals
- Sengkang: [X] leads | [Y] activities | [Z] deals
- Hougang: [X] leads | [Y] activities | [Z] deals
- Serangoon: [X] leads | [Y] activities | [Z] deals

**🔥 Hot Properties**
Link to Properties database filtered by Status = ✅ Available

**📚 Knowledge Base**
Link to Knowledge Base database

**⚡ Quick Actions**
- Add New Lead → Link to Leads database
- Log Activity → Link to Activities database
- Add Property → Link to Properties database
- Create Deal → Link to Deals database

**💡 Daily Workflow Tips**
1. Check 🔥 Hot Leads every morning for follow-ups due
2. Review Active Deals for Next Action Due dates
3. Log activities immediately after door knocking
4. Update deal stages within 24 hours of client contact
5. Add lessons learned after significant wins/losses
6. Review Knowledge Base before client meetings

---

## Option 2: Sample Data

### Sample Leads (10 records)

| Name | Contact | Email | Source | Property Interest | Budget Range | Status | Priority |
|------|---------|-------|--------|-------------------|--------------|--------|----------|
| Tan Wei Ming | +6591234567 | tan.weiming@email.com | 🚪 Door Knocking | 🏢 HDB | $500K-$800K | 💰 Offer Made | 🔥 Hot |
| Lim Shu Qi | +6592345678 | lim.shuqi@email.com | 👨‍👩‍👧 Referral | 🏠 Condo | $1.2M-$2M | 👀 Viewing Scheduled | ⚡ Warm |
| Chen Jia Hao | +6593456789 | chen.jiahao@email.com | 💻 Online | 🏢 HDB | $500K-$800K | 📝 OTP Issued | 🔥 Hot |
| Wong Mei Ling | +6594567890 | wong.meiling@email.com | 📱 Social Media | 🏢 HDB, 🏘️ EC | $800K-$1.2M | ✅ Closed | ⚡ Warm |
| Ng Kok Peng | +6595678901 | ng.kokpeng@email.com | 🏢 Walk-in | 🏡 Landed | >$2M | 📋 Resale Application | 🔥 Hot |
| Lee Xiu Ying | +6596789012 | lee.xiuying@email.com | 🚪 Door Knocking | 🏘️ EC | $800K-$1.2M | 👀 Viewing Scheduled | ⚡ Warm |
| Goh Zhi Xiang | +6597890123 | goh.zhixiang@email.com | 👨‍👩‍👧 Referral | 🏠 Condo | >$2M | 📞 Contacted | ❄️ Cold |
| Chua Pei Shan | +6598901234 | chua.peishan@email.com | 💻 Online | 🏢 HDB | $500K-$800K | 🆕 New | ⚡ Warm |
| Koh Jun Wei | +6599012345 | koh.junwei@email.com | 📱 Social Media | 🏠 Condo | $1.2M-$2M | 📞 Contacted | ❄️ Cold |
| Ong Li Na | +6590123456 | ong.lina@email.com | 🏢 Walk-in | 🏢 HDB | <$500K | 👀 Viewing Scheduled | ⚡ Warm |

### Sample Properties (8 records)

| Property Name | Address | Type | District | Area | Price | Size (sqft) | Bedrooms | Status |
|---------------|---------|------|----------|------|-------|-------------|----------|--------|
| Punggol Waterway Terrace | 123 Punggol Drive | 🏢 HDB | D19 | 🚇 Punggol | $650,000 | 1100 | 4 | ✅ Available |
| Sengkang Grand Residences | 456 Sengkang East Avenue | 🏠 Condo | D19 | 🚇 Sengkang | $1,200,000 | 850 | 3 | ✅ Available |
| Hougang Avenue 5 | 789 Hougang Street 21 | 🏢 HDB | D19 | 🚇 Hougang | $580,000 | 1000 | 4 | 📝 Under Offer |
| Serangoon Garden Estate | 234 Serangoon Avenue 3 | 🏡 Landed | D19 | 🚇 Serangoon | $2,800,000 | 2800 | 5+ | 📝 Under Offer |
| Punggol Northshore | 567 Compassvale Road | 🏘️ EC | D19 | 🚇 Punggol | $950,000 | 1050 | 4 | ✅ Available |
| Compassvale Beacon | 89 Punggol Field | 🏢 HDB | D19 | 🚇 Sengkang | $520,000 | 900 | 3 | ❌ Sold |
| Buangkok Vale | 345 Fernvale Lane | 🏢 HDB | D19 | 🚇 Hougang | $480,000 | 850 | 3 | ✅ Available |
| Luxus Hills | 678 Anchorvale Crescent | 🏡 Landed | D28 | Other | $3,200,000 | 3200 | 5+ | ✅ Available |

### Sample Activities (8 records)

| Activity Name | Date | Type | Area | Outcome | Leads Generated | Conversations | Duration (mins) | Notes |
|---------------|------|------|------|---------|-----------------|---------------|-----------------|-------|
| 🚪 Door Knock - Punggol - Apr 3 | 2025-04-03 | 🚪 Door Knocking | 🚇 Punggol | ✅ Lead Generated | 3 | 12 | 180 | Good response in Block 123-125. Owners receptive to upgrading. |
| ☎️ Cold Call Session - Apr 4 | 2025-04-04 | ☎️ Cold Call | 🚇 Sengkang | 📞 Callback Scheduled | 2 | 25 | 90 | Called expired listings. 2 callbacks scheduled for next week. |
| 👀 Viewing - Tan Wei Ming | 2025-04-04 | 👀 Viewing | 🚇 Punggol | ✅ Completed | 1 | 3 | 45 | Client liked the unit but wants to compare. Following up tomorrow. |
| 🤝 Meeting - Lim Shu Qi | 2025-04-03 | 🤝 Meeting | CBD | ✅ Lead Generated | 1 | 1 | 60 | Pre-approval discussion done. Ready to view properties next week. |
| 🚪 Door Knock - Hougang - Apr 2 | 2025-04-02 | 🚪 Door Knocking | 🚇 Hougang | 📊 Market Intel | 0 | 8 | 120 | Many units under renovation. Market picking up in this area. |
| 📧 Follow-up - Chen Jia Hao | 2025-04-05 | 📧 Follow-up | 🚇 Serangoon | ✅ Completed | 0 | 1 | 30 | Sent new listings. Client reviewing and will revert by Friday. |
| 💻 Research - Market Analysis | 2025-04-04 | 💻 Research | Other | 📊 Market Intel | 0 | 0 | 60 | Compiled Q1 transaction data for NEL areas. Prices up 3% vs last quarter. |
| 👀 Viewing - Wong Mei Ling | 2025-04-02 | 👀 Viewing | 🚇 Sengkang | ✅ Completed | 1 | 2 | 60 | Second viewing. Client comparing with another unit in the area. |

### Sample Deals (6 records)

| Deal Name | Stage | Deal Type | Price | Commission % | Probability | Next Action | Next Action Due |
|-----------|-------|-----------|-------|--------------|-------------|-------------|-----------------|
| Tan Wei Ming - Punggol Waterway Terrace | 💰 Offer Made | 🏢 HDB → HDB | $650,000 | 2% | 75% | Draft OTP for review | 2025-04-10 |
| Lim Shu Qi - Sengkang Grand Residences | 👀 Viewing | 🏠 Private → 🏠 Private | $1,200,000 | 2% | 50% | Schedule second viewing | 2025-04-12 |
| Chen Jia Hao - Hougang Avenue 5 | 📝 OTP Issued | 🏢 HDB → HDB | $580,000 | 2% | 90% | Collect exercise documents | 2025-04-08 |
| Wong Mei Ling - Compassvale Beacon | ✅ Closed | 🏢 HDB → 🏠 Private | $520,000 | 2% | 100% | Handover completed | - |
| Ng Kok Peng - Serangoon Garden Estate | 📋 Resale Application | 🏡 Landed | $2,800,000 | 1% | 75% | Submit to HDB portal | 2025-04-19 |
| Lee Xiu Ying - Punggol Northshore | 👀 Viewing | 🏘️ EC | $950,000 | 2% | 25% | Follow up on financing | 2025-04-15 |

---

## Option 3: Notion Template Marketplace

To make this truly shareable, create it as a **Notion Template**:

1. Duplicate your workspace page
2. Go to Settings → Workspace → Export
3. Or use Notion's Template Gallery feature
4. Share the public template link

Users can then duplicate it to their own workspace with one click.

---

## Scripts Library (for Knowledge Base)

### Door Knocking Opener
```
"Hi! I'm a property consultant helping homeowners in this area. I noticed some recent transactions and wanted to check if you might be considering a move?"
```

### Cold Call Script
```
"Hello, this is [name] from [agency]. I'm calling because I saw your property listing expired. Are you still looking to sell?"
```

### Handling Price Objection
```
"I understand your concern about the price. Let me show you some recent comparable sales in this area to help set realistic expectations."
```

### Follow-up Email Template
```
Subject: Property Viewing Follow-up - [Property Name]

Dear [Client Name],

Thank you for viewing the property today. As discussed, I've attached additional information about the unit and the neighborhood amenities.

Please let me know if you have any questions or would like to schedule another viewing.

Best regards,
[Your Name]
```

### Closing Script - OTP
```
"Based on our discussions, shall we proceed with the OTP? I'll prepare the documents and we can meet tomorrow to sign."
```

---

## Quick Start Checklist

- [ ] Create main "SG Property Pro" page
- [ ] Create 5 databases (Leads, Properties, Activities, Deals, Knowledge Base)
- [ ] Configure all database properties with proper types
- [ ] Add formulas for PSF, Est. Commission, Weighted Commission
- [ ] Create Dashboard subpage
- [ ] Add linked database views to Dashboard
- [ ] Import sample data (copy from above)
- [ ] Add scripts to Knowledge Base
- [ ] Test the workflow

---

## Support

For questions or issues, refer to Notion's help documentation or create a duplicate of this template structure in your own workspace.

**Note:** This is designed for Singapore real estate agents managing leads, properties, deals, and activities in the North-East Line (NEL) corridor areas (Punggol, Sengkang, Hougang, Serangoon).
