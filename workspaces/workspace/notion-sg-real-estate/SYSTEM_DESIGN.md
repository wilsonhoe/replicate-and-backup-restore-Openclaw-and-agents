# Singapore Real Estate Notion System
## Complete Design Specification

---

## 1. SYSTEM OVERVIEW

**Name:** SG Property Pro — Real Estate Agent OS  
**Target User:** Singapore real estate agents (solo → team scale)  
**Core Philosophy:** Memory-first, execution-tracked, AI-ready

---

## 2. PAGE STRUCTURE

```
🏠 SG Property Pro (Homepage)
├── 📊 Dashboard
├── 👥 Leads Hub
│   └── Leads Database
├── 🏢 Properties Hub
│   └── Properties Database
├── 📅 Activities Hub
│   └── Activities Database
├── 💼 Deals Pipeline
│   └── Deals Database
├── 📚 Knowledge Base
│   ├── Scripts Library
│   ├── Market Insights
│   └── Lessons Learned
├── 📍 NEL Zone Tracker
└── ⚙️ System Settings
```

---

## 3. DATABASE SCHEMAS

### 3.1 👥 LEADS DATABASE

| Property | Type | Options/Config |
|----------|------|----------------|
| **Name** | Title | — |
| **Contact** | Phone | — |
| **Email** | Email | — |
| **Source** | Select | 🚪 Door Knocking / 👨‍👩‍👧 Referral / 💻 Online / 📱 Social Media / 🏢 Walk-in |
| **Property Interest** | Multi-select | 🏢 HDB / 🏠 Condo / 🏡 Landed / 🏘️ EC |
| **Budget Range** | Select | <$500K / $500K-$800K / $800K-$1.2M / $1.2M-$2M / >$2M |
| **Status** | Select | 🆕 New / 📞 Contacted / 👀 Viewing Scheduled / 💰 Offer Made / ✅ Closed / ❌ Lost |
| **Priority** | Select | 🔥 Hot / ⚡ Warm / ❄️ Cold |
| **Assigned To** | Person | — |
| **Last Contact** | Date | — |
| **Next Follow-up** | Date | — |
| **Linked Property** | Relation | → Properties DB |
| **Linked Deals** | Relation | → Deals DB |
| **Activities** | Relation | → Activities DB |
| **Total Activities** | Rollup | Count of Activities |
| **Days Since Contact** | Formula | `dateBetween(now(), prop("Last Contact"), "days")` |
| **Notes** | Text | — |

**Views:**
- 🎯 **All Leads** (Table view, default)
- 🔥 **Hot Leads** (Filter: Priority = Hot, Status ≠ Closed/Lost)
- 📅 **Follow-ups Due** (Filter: Next Follow-up ≤ Today, Sort by date)
- 📍 **By Source** (Board view, group by Source)
- 📊 **By Status** (Board view, group by Status)
- 🏢 **HDB Focus** (Filter: Property Interest contains HDB)

---

### 3.2 🏢 PROPERTIES DATABASE

| Property | Type | Options/Config |
|----------|------|----------------|
| **Property Name** | Title | — |
| **Address** | Text | — |
| **Type** | Select | 🏢 HDB / 🏠 Condo / 🏡 Landed / 🏘️ EC |
| **District** | Select | D1-28 (Singapore districts) |
| **Area** | Select | 🚇 Punggol / 🚇 Sengkang / 🚇 Hougang / 🚇 Serangoon / Other |
| **MRT Station** | Select | NEL stations + others |
| **Price** | Number | SGD format |
| **Size (sqft)** | Number | — |
| **PSF** | Formula | `prop("Price") / prop("Size (sqft)")` |
| **Bedrooms** | Select | 1 / 2 / 3 / 4 / 5+ |
| **Status** | Select | ✅ Available / 📝 Under Offer / ❌ Sold / 🔒 Off Market |
| **Listing Date** | Date | — |
| **Linked Leads** | Relation | → Leads DB |
| **Linked Deals** | Relation | → Deals DB |
| **Lead Count** | Rollup | Count of Linked Leads |
| **Viewings** | Relation | → Activities DB |
| **Total Viewings** | Rollup | Count of Viewings |
| **Seller Contact** | Text | — |
| **Notes** | Text | — |

**Views:**
- 📋 **All Properties** (Table view)
- 🏢 **By Type** (Board view, group by Type)
- 📍 **By District** (Gallery view, group by District)
- 🔥 **Hot Properties** (Filter: Lead Count > 0, Status = Available)
- 🚇 **NEL Line Focus** (Filter: Area = Punggol/Sengkang/Hougang/Serangoon)

---

### 3.3 📅 ACTIVITIES DATABASE

| Property | Type | Options/Config |
|----------|------|----------------|
| **Activity Name** | Title | Auto-generated: "[Type] - [Area] - [Date]" |
| **Date** | Date | — |
| **Type** | Select | 🚪 Door Knocking / ☎️ Cold Call / 📧 Follow-up / 👀 Viewing / 🤝 Meeting / 💻 Research / 📝 Admin |
| **Area** | Select | 🚇 Punggol / 🚇 Sengkang / 🚇 Hougang / 🚇 Serangoon / Other NEL / CBD / Other |
| **Outcome** | Select | ✅ Lead Generated / 📞 Callback Scheduled / ❌ No Answer / 🚫 Not Interested / 📊 Market Intel / ✅ Completed |
| **Leads Generated** | Number | Count |
| **Conversations** | Number | Count |
| **Linked Leads** | Relation | → Leads DB |
| **Linked Property** | Relation | → Properties DB |
| **Duration (mins)** | Number | — |
| **Notes** | Text | What worked, objections, insights |
| **Added to KB** | Checkbox | — |

**Views:**
- 📅 **All Activities** (Table view, sort by Date desc)
- 📆 **Calendar View** (Calendar view by Date)
- 🚪 **Door Knocking Log** (Filter: Type = Door Knocking)
- 📍 **By Area** (Board view, group by Area)
- 📊 **This Week** (Filter: Date is This Week)

---

### 3.4 💼 DEALS PIPELINE DATABASE

| Property | Type | Options/Config |
|----------|------|----------------|
| **Deal Name** | Title | "[Lead] - [Property]" |
| **Lead** | Relation | → Leads DB (required) |
| **Property** | Relation | → Properties DB (required) |
| **Stage** | Select | 🆕 New / 👀 Viewing / 💰 Offer Made / 📝 OTP Issued / ✅ OTP Exercised / 📋 Resale Application / 🏛️ HDB Acceptance / 🔨 Legal Completion / ✅ Closed / ❌ Lost |
| **Deal Type** | Select | 🏢 HDB → HDB / 🏢 HDB → 🏠 Private / 🏠 Private → 🏠 Private / 🏠 Private → 🏢 HDB |
| **Price** | Number | Agreed price |
| **Commission %** | Number | Default 2% |
| **Commission Est.** | Formula | `prop("Price") * prop("Commission %")` |
| **Expected Close** | Date | — |
| **OTP Date** | Date | — |
| **OTP Exercise Date** | Date | — |
| **Resale Application Date** | Date | — |
| **HDB Acceptance Date** | Date | — |
| **Legal Completion Date** | Date | — |
| **Days in Stage** | Formula | `dateBetween(now(), prop("Last Stage Change"), "days")` |
| **Probability** | Select | 10% / 25% / 50% / 75% / 90% / 100% |
| **Weighted Commission** | Formula | `prop("Commission Est.") * toNumber(replaceAll(prop("Probability"), "%", "")) / 100` |
| **Next Action** | Text | — |
| **Next Action Due** | Date | — |
| **Notes** | Text | — |

**Views:**
- 📊 **Pipeline Board** (Board view, group by Stage)
- 📈 **Forecast** (Table view, show Weighted Commission)
- 🔥 **Hot Deals** (Filter: Stage = Viewing → OTP Exercised, Sort by Probability)
- 📅 **Closing This Month** (Filter: Expected Close is This Month)
- ⚠️ **Stuck Deals** (Filter: Days in Stage > 14, Stage ≠ Closed/Lost)

---

### 3.5 📚 KNOWLEDGE BASE

#### Scripts Library (Database)
| Property | Type | Options |
|----------|------|---------|
| **Script Name** | Title | — |
| **Type** | Select | 🚪 Door Knocking / ☎️ Cold Call / 📧 Follow-up / ❌ Objection Handling / 🤝 Closing / 📊 CMA Presentation |
| **Content** | Text | Full script |
| **Best For** | Multi-select | HDB / Condo / Landed / First-time buyer / Investor |
| **Success Rate** | Select | High / Medium / Low / Untested |
| **Last Used** | Date | — |

#### Market Insights (Database)
| Property | Type | Options |
|----------|------|---------|
| **Insight** | Title | — |
| **Area** | Select | Punggol / Sengkang / etc. |
| **Type** | Select | 📈 Price Trend / 🏗️ New Launch / 📊 Transaction Volume / 📝 Policy Change |
| **Date** | Date | — |
| **Source** | Text | — |
| **Impact** | Select | High / Medium / Low |

#### Lessons Learned (Database)
| Property | Type | Options |
|----------|------|---------|
| **Lesson** | Title | — |
| **Context** | Select | ✅ What Worked / ❌ What Didn't / 💡 Insight / 🔧 System Improvement |
| **Date** | Date | — |
| **Related Activity** | Relation | → Activities DB |
| **Action Item** | Text | — |

---

## 4. DASHBOARD LAYOUT

### 🏠 Main Dashboard Structure

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 SG Property Pro                    [New Lead] [Log Activity]  │
├─────────────────────────────────────────────────────────────┤
│  📊 KPI OVERVIEW                                            │
│  ┌──────────┬──────────┬──────────┬──────────┐                │
│  │   🎯     │   💰     │   📈     │   ⏰     │                │
│  │  Active  │ Commission │ Conversion │ Follow-up │                │
│  │  Leads   │  Pipeline  │   Rate     │   Due     │                │
│  │    24    │   $45K    │    12%     │    8      │                │
│  └──────────┴──────────┴──────────┴──────────┘                │
├─────────────────────────────────────────────────────────────┤
│  🔥 HOT LEADS (This Week)                                   │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Name          │ Interest │ Budget     │ Next Action │    │
│  │ ──────────────┼──────────┼────────────┼─────────────│    │
│  │ John Tan      │ HDB      │ $600-800K  │ Viewing Fri │    │
│  │ Mary Lee      │ Condo    │ $1.2M-2M   │ OTP draft   │    │
│  └──────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  📅 THIS WEEK'S ACTIVITIES                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ [ ] Tue 9AM │ 🚪 Door Knock │ Punggol │ Target: 50 │    │
│  │ [ ] Wed 2PM │ 👀 Viewing    │ 123 Ave │ Lead: John  │    │
│  └──────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  💼 ACTIVE DEALS (In Pipeline)                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Deal                    │ Stage      │ Est. Comm.  │    │
│  │ ────────────────────────┼────────────┼─────────────│    │
│  │ John - Punggol HDB      │ OTP Issued │ $12,000     │    │
│  │ Mary - Sengkang Condo   │ Viewing    │ $28,000     │    │
│  └──────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  📍 NEL ZONE TRACKER                                        │
│  🚇 Punggol: 5 leads | 🚇 Sengkang: 3 leads |              │
│  🚇 Hougang: 2 leads | 🚇 Serangoon: 4 leads                │
├─────────────────────────────────────────────────────────────┤
│  🔗 QUICK LINKS                                             │
│  [👥 All Leads] [🏢 Properties] [📅 Calendar] [📚 Scripts]  │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. TEMPLATES

### 5.1 New Lead Entry Template
```
## 🆕 New Lead: {{Name}}

**Contact Info:**
- Phone: {{Contact}}
- Email: {{Email}}

**Requirements:**
- Looking for: {{Property Interest}}
- Budget: {{Budget Range}}
- Area preference: 

**Source:** {{Source}}

**Initial Notes:**
{{Notes}}

**Next Steps:**
- [ ] Schedule follow-up
- [ ] Send listings
- [ ] Qualify needs

---
Added: {{today}}
```

### 5.2 Door Knocking Session Template
```
## 🚪 Door Knocking Session: {{Area}} - {{Date}}

**Location:** {{Area}}
**Time:** {{Time}}
**Duration:** {{Duration}} mins

### Results:
- 🏠 Doors knocked: 
- 💬 Conversations: 
- 🎯 Leads generated: 

### Key Interactions:
| Unit | Response | Notes |
|------|----------|-------|
|      |          |       |

### Insights:
{{Notes}}

### Follow-ups:
- [ ] Contact [Name] - interested in [type]

---
**Added to KB:** {{checkbox}}
```

### 5.3 Weekly Review Template
```
## 📊 Weekly Review: Week of {{Date}}

### Numbers:
- New leads: 
- Activities: 
- Deals progressed: 
- Commission secured: $

### What Worked:
{{What worked?}}

### What Didn't:
{{What to improve?}}

### Next Week Focus:
{{Priority areas}}

### Key Learnings:
{{Add to Lessons Learned}}
```

---

## 6. NAMING CONVENTIONS

### Database Entries:
- **Leads:** "[First] [Last]" (e.g., "John Tan")
- **Properties:** "[Address] | [Type]" (e.g., "123 Punggol Dr | 4R HDB")
- **Activities:** "[Type] - [Area] - [Date]" (e.g., "🚪 Door Knock - Punggol - Apr 5")
- **Deals:** "[Lead] - [Property]" (e.g., "John - Punggol HDB")

### Tagging:
- Status: Single emoji prefix
- Priority: 🔥/⚡/❄️ system
- Property type: 🏢/🏠/🏡/🏘️

---

## 7. AUTOMATION OPPORTUNITIES

### For AI Agent Integration (Lisa):
1. **Auto-capture** from voice/WhatsApp → create Lead entry
2. **Daily digest** of follow-ups due → sent to agent
3. **Weekly rollup** of activities → populate Weekly Review
4. **Deal stage tracking** → alert when deals stuck >14 days
5. **NEL zone insights** → auto-log market data from viewings

### Notion Formulas for Auto-calculation:
- Days since last contact
- Weighted commission forecast
- PSF calculation
- Days in current stage
- Conversion rate (deals closed / leads total)

---

## 8. SINGAPORE-SPECIFIC FIELDS

### Property Types:
- 🏢 HDB (BTO, Resale, SERS)
- 🏠 Condo (Private)
- 🏡 Landed (Terrace, Semi-D, Bungalow)
- 🏘️ EC (Executive Condo)

### Transaction Timelines (from ETD):
**HDB → HDB:** Intent to Sell → OTP → Resale Application → HDB Acceptance → Legal Completion
**HDB → Private:** OTP (1%) → Exercise (4%) → Stamp Duty → Legal Completion
**Private → Private:** OTP → Exercise → Legal Completion → CPF Refund

### Districts:
D1-28 Singapore districts  
Priority NEL areas: Punggol, Sengkang, Hougang, Serangoon

---

## 9. SETUP CHECKLIST

- [ ] Create homepage with dashboard
- [ ] Set up 5 databases with relations
- [ ] Configure views for each database
- [ ] Create dashboard with linked views
- [ ] Add emoji icons to all pages
- [ ] Set up templates for quick entry
- [ ] Configure rollups and formulas
- [ ] Test relation links work correctly
- [ ] Create sample entries for testing
- [ ] Export as template for Gumroad

---

**Next Step:** Create the actual Notion pages via API or provide step-by-step manual setup guide.
