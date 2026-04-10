# Door Knocking Mastery System — Complete Setup Guide

## Step-by-Step Notion Setup Instructions

---

## Prerequisites

**Before you start:**
- Notion account (free plan works)
- Notion mobile app installed (iOS/Android)
- 30 minutes for complete setup
- CSV files from `Templates/` folder

---

## Part 1: Import Databases (15 minutes)

### Step 1.1: Create Your Workspace

1. Log into Notion (notion.so)
2. Create a new page called "Door Knocking Mastery"
3. Add an icon (🚪 recommended)
4. This will be your home base

### Step 1.2: Import Sessions Database

1. Create new page → Type `/import`
2. Select **CSV**
3. Upload `door_knocking_sessions.csv`
4. Name it: "Door Knocking Sessions"
5. Set icon: 🎯

**Verify these properties imported correctly:**
- Date (Date)
- Area (Select)
- Block (Title)
- Time Slot (Select)
- Doors Knocked (Number)
- Doors Opened (Number)
- Conversations (Number)
- Leads Captured (Number)
- Appointments Set (Number)
- Open Rate % (Formula)
- Conversation Rate % (Formula)
- Lead Rate % (Formula)

**Formula check:** If formulas didn't import, set them manually:
- Open Rate %: `prop("Doors Opened") / prop("Doors Knocked") * 100`
- Conversation Rate %: `prop("Conversations") / prop("Doors Opened") * 100`
- Lead Rate %: `prop("Leads Captured") / prop("Conversations") * 100`

### Step 1.3: Import Leads Database

1. Create new page → Type `/import`
2. Select **CSV**
3. Upload `leads.csv`
4. Name it: "Leads"
5. Set icon: 👤

**Verify properties:**
- Name (Title)
- Unit (Text)
- Block (Text)
- Contact (Text)
- Owner/Tenant (Select)
- Intent (Select: Sell/Buy/Exploring)
- Timeline (Select)
- Budget/Price (Text)
- Source (Select)
- Status (Select)
- Last Contact Date (Date)
- Linked Session (Relation - we'll set this up later)
- Area (Select)
- Priority (Select: High/Medium/Low)

### Step 1.4: Import Follow-ups Database

1. Create new page → Type `/import`
2. Select **CSV**
3. Upload `follow_ups.csv`
4. Name it: "Follow-ups"
5. Set icon: 📞

**Verify properties:**
- Lead Name (Title - will become Relation)
- Follow-up Date (Date)
- Method (Select: Call/WhatsApp/Visit)
- Outcome (Text)
- Next Action (Text)
- Priority (Select)
- Status (Select: Pending/Done/Overdue)

### Step 1.5: Import Training Database

1. Create new page → Type `/import`
2. Select **CSV**
3. Upload `training_sessions.csv`
4. Name it: "Training"
5. Set icon: 🧠

**Verify properties:**
- Date (Date)
- Practice Type (Select: Warm-up/Simulation/Review)
- Difficulty (Select: Easy/Medium/Hard)
- Scenario Type (Select: Punggol/Serangoon/Objection)
- Script Used (Text - will become Relation)
- Score (Text)
- Feedback (Text)
- Improvement Notes (Text)
- Duration (Text)

### Step 1.6: Import Scripts Database

1. Create new page → Type `/import`
2. Select **CSV**
3. Upload `scripts.csv`
4. Name it: "Scripts"
5. Set icon: 📚

**Verify properties:**
- Script Name (Title)
- Area (Select: Punggol/Serangoon/Both)
- Type (Select: Opening/Hook/Close/Objection)
- Script Content (Text)
- Effectiveness Score (Text)
- Usage Count (Number)
- Notes (Text)

### Step 1.7: Import Weekly Reviews

1. Create new page → Type `/import`
2. Select **CSV**
3. Upload `weekly_reviews.csv`
4. Name it: "Weekly Reviews"
5. Set icon: 📊

---

## Part 2: Set Up Relations (10 minutes)

### Step 2.1: Link Leads to Sessions

1. Go to **Leads** database
2. Add new property → Type: **Relation**
3. Select database: **Door Knocking Sessions**
4. Name: "Session"
5. Enable "Show on Sessions database"
6. Sessions side name: "Leads from Session"

### Step 2.2: Link Follow-ups to Leads

1. Go to **Follow-ups** database
2. Add new property → Type: **Relation**
3. Select database: **Leads**
4. Name: "Lead"
5. Enable "Show on Leads database"
6. Leads side name: "Follow-ups"

### Step 2.3: Link Training to Scripts

1. Go to **Training** database
2. Add new property → Type: **Relation**
3. Select database: **Scripts**
4. Name: "Script Practiced"
5. Enable "Show on Scripts database"
6. Scripts side name: "Training Sessions"

---

## Part 3: Create Views (10 minutes)

### Step 3.1: Sessions Views

**View 1: This Week**
1. In Sessions database, click "+ New view"
2. Select **Table**
3. Name: "This Week"
4. Add filter: Date "is within" "the past week"

**View 2: By Area**
1. Click "+ New view"
2. Select **Board**
3. Name: "By Area"
4. Group by: Area

**View 3: High Performers**
1. Click "+ New view"
2. Select **Table**
3. Name: "High Performers"
4. Add filter: Lead Rate % ">" 25
5. Sort: Lead Rate % Descending

**View 4: My Sessions (Gallery)**
1. Click "+ New view"
2. Select **Gallery**
3. Name: "Session Cards"
4. Card preview: Block

### Step 3.2: Leads Views

**View 1: Hot Leads**
1. In Leads database, create new view
2. Type: Table
3. Name: "Hot Leads"
4. Filter: Priority "is" High
5. Sort: Last Contact Date Descending

**View 2: By Area**
1. New view → Board
2. Name: "By Area"
3. Group by: Area

**View 3: This Week's Leads**
1. New view → Table
2. Name: "This Week"
3. Filter: Last Contact Date "is within" "the past week"

**View 4: By Intent**
1. New view → Board
2. Name: "By Intent"
3. Group by: Intent

**View 5: High Priority Pipeline**
1. New view → Table
2. Name: "Pipeline"
3. Filter: Priority "is" High
4. Sort: Status Ascending

### Step 3.3: Follow-ups Views

**View 1: Due Today**
1. In Follow-ups, new view
2. Type: Table
3. Name: "Due Today"
4. Filter: Follow-up Date "is" Today
5. Filter: Status "is" Pending

**View 2: Overdue**
1. New view
2. Name: "Overdue"
3. Filter: Follow-up Date "is before" Today
4. Filter: Status "is" Pending
5. Sort: Follow-up Date Ascending

**View 3: High Priority**
1. New view
2. Name: "High Priority"
3. Filter: Priority "is" High

**View 4: Completed This Week**
1. New view
2. Name: "Done This Week"
3. Filter: Follow-up Date "is within" "the past week"
4. Filter: Status "is" Done

### Step 3.4: Training Views

**View 1: This Week's Practice**
1. In Training, new view
2. Name: "This Week"
3. Filter: Date "is within" "the past week"

**View 2: By Scenario Type**
1. New view → Board
2. Name: "By Scenario"
3. Group by: Scenario Type

**View 3: Needs Improvement**
1. New view
2. Name: "Needs Work"
3. Filter: Score "contains" 6 (or adjust based on your scoring)

**View 4: Warm-ups Only**
1. New view
2. Name: "Warm-ups"
3. Filter: Practice Type "is" Warm-up

### Step 3.5: Scripts Views

**View 1: By Area**
1. In Scripts, new view → Board
2. Name: "By Area"
3. Group by: Area

**View 2: By Type**
1. New view → Board
2. Name: "By Type"
3. Group by: Type

**View 3: Top Performers**
1. New view
2. Name: "Top Scripts"
3. Sort: Effectiveness Score Descending
4. Filter: Effectiveness Score ">" 8

---

## Part 4: Create Dashboard (5 minutes)

### Step 4.1: Build Home Page

1. Go to your main "Door Knocking Mastery" page
2. Delete default content
3. Add sections:

**Section 1: Header**
```
# 🚪 Door Knocking Mastery System
> Complete execution + training + tracking for Singapore real estate
```

**Section 2: Quick Actions**
```
## Quick Actions
- [Log New Session] → Link to Sessions database
- [Add New Lead] → Link to Leads database
- [Start Training] → Link to Training database
- [View Scripts] → Link to Scripts database
```

**Section 3: Today's Dashboard**
```
## 📍 Today's Execution
[Link to Sessions: This Week view]

## 🔥 Hot Leads
[Link to Leads: Hot Leads view]

## 📞 Follow-ups Due
[Link to Follow-ups: Due Today view]

## 📊 This Week's KPIs
[Link to Weekly Reviews database]

## 🧠 Training Zone
[Link to Training: This Week view]

## 📚 Quick Script Access
- [Punggol Scripts] → Link to Scripts: Punggol filter
- [Serangoon Scripts] → Link to Scripts: Serangoon filter
- [Objection Handling] → Link to Scripts: Objection filter
```

### Step 4.2: Add Linked Databases

1. Type `/linked` and select "Linked database"
2. Select each database and add to relevant section
3. Apply appropriate filters

---

## Part 5: Test Your Setup (5 minutes)

### Step 5.1: Create Test Session

1. Go to Sessions database
2. Click "New"
3. Fill in:
   - Date: Today
   - Area: Punggol
   - Block: 123A
   - Time Slot: Evening (6-8pm)
   - Doors Knocked: 50
   - Doors Opened: 20
   - Conversations: 12
   - Leads Captured: 5
   - Appointments Set: 2
4. Verify formulas calculate automatically

### Step 5.2: Create Test Lead

1. Go to Leads database
2. Click "New"
3. Fill in:
   - Name: Test Lead
   - Block: 123A
   - Intent: Exploring
   - Priority: High
   - Linked Session: Select your test session
4. Verify session shows this lead in relation

### Step 5.3: Create Test Follow-up

1. Go to Follow-ups database
2. Click "New"
3. Fill in:
   - Lead: Select test lead
   - Follow-up Date: Tomorrow
   - Method: WhatsApp
   - Priority: High
4. Verify lead shows this follow-up

### Step 5.4: Check Dashboard

1. Go to home page
2. Verify all linked databases show data
3. Test each link works

---

## Part 6: Mobile Setup (5 minutes)

### Step 6.1: Install Notion App

1. Download Notion from App Store (iOS) or Play Store (Android)
2. Log in with same account
3. Navigate to your Door Knocking Mastery workspace

### Step 6.2: Star Key Pages

1. Open each database
2. Tap "..." menu
3. Select "Add to Favorites"
4. Add these to favorites:
   - Home page
   - Sessions
   - Leads
   - Follow-ups
   - Scripts

### Step 6.3: Test Mobile Input

1. Create a test entry from mobile
2. Verify it syncs to desktop
3. Practice voice-to-text for quick notes

---

## Part 7: Replace Sample Data

### Step 7.1: Clear Sample Sessions

1. Go to Sessions database
2. Select all sample rows
3. Delete (keep 1-2 as reference)

### Step 7.2: Clear Sample Leads

1. Go to Leads database
2. Select all sample rows
3. Delete (keep 1-2 as reference)

### Step 7.3: Keep Scripts

**Don't delete scripts** — these are your reference materials

---

## Quick Reference Card

### Daily Workflow Checklist

**Morning:**
- [ ] Check Follow-ups: Due Today
- [ ] Review Hot Leads
- [ ] Plan today's area/block

**Pre-Session:**
- [ ] Review area-specific scripts
- [ ] Quick 5-min warm-up
- [ ] Check supplies (flyers, cards)

**During Session:**
- [ ] Take photo of block map
- [ ] Voice memo quick notes
- [ ] Note unit numbers

**Post-Session (within 1 hour):**
- [ ] Log session
- [ ] Add new leads
- [ ] Schedule follow-ups

**Evening:**
- [ ] Update follow-up statuses
- [ ] Review KPIs
- [ ] Plan tomorrow

### Formula Reference

**Sessions Database:**
```
Open Rate % = prop("Doors Opened") / prop("Doors Knocked") * 100
Conversation Rate % = prop("Conversations") / prop("Doors Opened") * 100
Lead Rate % = prop("Leads Captured") / prop("Conversations") * 100
```

---

## Troubleshooting

**Formulas not working?**
- Check property names match exactly
- Ensure division by zero protection: `prop("Doors Opened") == 0 ? 0 : prop("Conversations") / prop("Doors Opened") * 100`

**Relations not showing?**
- Verify both databases exist
- Check relation is two-way enabled
- Refresh page

**CSV import failed?**
- Check file encoding is UTF-8
- Remove special characters
- Try smaller batches

---

## You're Ready!

**Next Steps:**
1. Log your first real session
2. Add your first real lead
3. Schedule your first follow-up
4. Do 10 minutes of script practice

**See QUICK_START.md for daily workflow**
**See SALES_SCRIPTS.md for complete scripts**

---

**Setup complete! Time to knock some doors.** 🚪
