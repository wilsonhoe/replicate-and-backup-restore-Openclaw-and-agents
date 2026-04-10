# Door Knocking Mastery System — Quick Start Guide

> Complete Singapore real estate door knocking system for Punggol, Serangoon, and Sengkang (NEL corridor)

---

## What You're Getting

A **7-database execution system** that tracks, trains, and optimizes your door knocking performance:

| Database | Purpose |
|----------|---------|
| **Door Knocking Sessions** | Track every field session with auto-calculated KPIs |
| **Leads** | HDB-specific pipeline with owner/tenant, intent, timeline |
| **Follow-ups** | Structured conversion system with priority scoring |
| **Training Sessions** | Daily skill practice with scoring and feedback |
| **Scripts** | Punggol/Serangoon optimized scripts library |
| **Weekly Reviews** | Performance analysis and optimization loop |

---

## 5-Minute Setup

### Step 1: Import Databases
Import these 6 CSV files to Notion:

1. **door_knocking_sessions.csv** → Create "Sessions" database
2. **leads.csv** → Create "Leads" database
3. **follow_ups.csv** → Create "Follow-ups" database
4. **training_sessions.csv** → Create "Training" database
5. **scripts.csv** → Create "Scripts" database
6. **weekly_reviews.csv** → Create "Weekly Reviews" database

### Step 2: Set Up Relations
- Leads → Sessions (Linked Session)
- Follow-ups → Leads (Lead Name)
- Training → Scripts (Script Used)

### Step 3: Create Views

**Sessions Database:**
- View: "This Week" (Date is within last 7 days)
- View: "By Area" (Group by Area)
- View: "High Performers" (Lead Rate % > 25%)

**Leads Database:**
- View: "Hot Leads" (Priority = High)
- View: "Today Follow-ups" (Last Contact Date is today)
- View: "By Area" (Group by Area)

**Follow-ups Database:**
- View: "Due Today" (Follow-up Date is today)
- View: "Overdue" (Follow-up Date is before today, Status = Pending)
- View: "High Priority" (Priority = High)

**Training Database:**
- View: "This Week's Practice" (Date is within last 7 days)
- View: "By Scenario" (Group by Scenario Type)
- View: "Needs Improvement" (Score < 7/10)

---

## Daily Workflow

### Morning (5 minutes)
1. **Check Views:**
   - Follow-ups → "Due Today"
   - Leads → "Hot Leads"
2. **Plan:** Schedule today's follow-ups

### Pre-Session (2 minutes)
3. **Review Scripts:** Check Scripts database for your target area
4. **Quick Practice:** Do 1 warm-up from Training database

### Post-Session (5 minutes)
5. **Log Session:** Add to Sessions database
6. **Add Leads:** Import new leads from session
7. **Schedule Follow-ups:** Create follow-up tasks

### Evening (5 minutes)
8. **Update Follow-ups:** Mark completed calls/WhatsApps
9. **Review KPIs:** Check today's metrics

---

## Mobile Input Template

**Quick Session Log (voice-to-text friendly):**

```
Date: Today
Area: Punggol
Block: ___
Doors Knocked: ___
Doors Opened: ___
Conversations: ___
Leads: ___
Appointments: ___
Notes: ___
```

**Quick Lead Capture:**

```
Name: ___
Block-Unit: ___
Contact: ___
Owner/Tenant: ___
Intent: Sell/Buy/Exploring
Timeline: ___
Priority: High/Medium/Low
```

---

## Area-Specific Quick Reference

### Punggol (Young Families, Upgraders)
- **Time:** 6:30-8pm best
- **Tone:** Energetic, opportunity-focused
- **Hook:** MOP completion, upgrading trends
- **Script:** "Young families upgrading..."

### Serangoon (Mature Owners, Investors)
- **Time:** 7-8:30pm best
- **Tone:** Calm, advisory, authoritative
- **Hook:** Infrastructure, value preservation, en-bloc
- **Script:** "Property consultant specializing..."

### Sengkang (Mixed, Young Professionals)
- **Time:** 6:30-8pm
- **Tone:** Professional but friendly
- **Hook:** Connectivity, newer estates
- **Script:** Blend of Punggol energy + Serangoon authority

---

## Key Metrics to Watch

**Weekly Targets:**
- Sessions: 4-5 per week
- Doors per session: 40-50
- Open rate: >35%
- Lead rate: >25%
- Appointment rate: >40% of leads

**Red Flags:**
- Open rate <30% → Check approach/timing
- Conversation rate <50% → Script needs work
- Lead rate <20% → Qualification issue
- No follow-ups completed → System breakdown

---

## Emergency Scripts (Print These)

### Door Opens - First 10 Seconds
**Punggol:** *"Hi! I'm helping several Punggol families explore upgrading options. Do you have a moment?"*

**Serangoon:** *"Good evening. I'm a property advisor tracking changes in Serangoon. May I share what's happening with values here?"*

### They Say "Not Interested"
*"I understand. Most homeowners aren't looking until they see the recent sales data. Can I leave a market report? Takes 2 seconds to receive."*

### They Say "No Time"
*"Of course. Can I WhatsApp you a brief market update instead? You can review when convenient."*

### They Say "Have Agent"
*"That's great. Many homeowners like a second opinion on market conditions. Would current sales data be helpful?"*

---

## Quick Tips

**Before Each Session:**
- Print block map
- Charge phone
- Bring 30+ flyers/market reports
- Review target block amenities

**During Session:**
- Start from top floor (take stairs down)
- Smile before door opens
- Step back after knocking (give space)
- Note which units were home/not home

**After Session:**
- Log within 1 hour (while memory fresh)
- Send follow-ups within 24 hours
- Update CRM same day

---

## Support

**Questions?**
- Full guide: `SETUP_GUIDE.md`
- Scripts: `SALES_SCRIPTS.md`
- Sample data: See Templates/ folder

---

**Ready to knock? Import the CSVs and log your first session.**
