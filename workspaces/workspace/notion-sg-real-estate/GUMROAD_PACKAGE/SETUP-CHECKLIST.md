# SG Property Pro — Setup Checklist

Print this checklist and check off each step as you complete it.

---

## Phase 1: Import (5-10 minutes)

### Create Notion Account
- [ ] Sign up at notion.so (free plan)
- [ ] Download mobile app (optional but recommended)
- [ ] Create a new workspace called "SG Property Pro"

### Import Databases
- [ ] Open Templates/leads.csv
- [ ] Import to Notion as "Leads" database
- [ ] Open Templates/properties.csv
- [ ] Import to Notion as "Properties" database
- [ ] Open Templates/deals.csv
- [ ] Import to Notion as "Deals" database
- [ ] Open Templates/activities.csv
- [ ] Import to Notion as "Activities" database
- [ ] Open Templates/knowledge_base.csv
- [ ] Import to Notion as "Knowledge Base" database

---

## Phase 2: Configure (10-15 minutes)

### Set Up Relations
- [ ] In Deals database: Link "Lead" column to Leads database
- [ ] In Deals database: Link "Property" column to Properties database
- [ ] In Activities database: Link "Related Lead" to Leads
- [ ] In Activities database: Link "Related Deal" to Deals

### Customize Commission Settings
- [ ] Open Deals database
- [ ] Adjust Agency Split % to match your agency (typically 30-50%)
- [ ] Verify Net Commission formula is calculating correctly
- [ ] Check Weighted Pipeline Value calculation

### Customize Property Types (if needed)
- [ ] Review HDB types: BTO, Resale, SBF
- [ ] Review Condo types: Executive, Private
- [ ] Review Landed types: Terrace, Semi-D, Bungalow
- [ ] Add any custom types your market uses

---

## Phase 3: Personalize (15-20 minutes)

### Replace Sample Data
- [ ] Delete sample leads (keep 1-2 as reference)
- [ ] Delete sample properties (keep 1-2 as reference)
- [ ] Delete sample deals (keep 1-2 as reference)
- [ ] Add your actual leads (start with 5-10)
- [ ] Add your actual properties (start with 3-5)

### Set Up Your First Active Deal
- [ ] Create a new deal
- [ ] Link to an existing lead
- [ ] Link to an existing property
- [ ] Set stage to "Prospecting" or "Viewing"
- [ ] Set probability %
- [ ] Set expected close date

### Customize Views
- [ ] Create "Active Leads" view (filter: Status = Active)
- [ ] Create "Hot Properties" view (filter: Status = Available)
- [ ] Create "This Month's Pipeline" view (filter: Expected Close Date is this month)
- [ ] Create "NEL Zone" view (filter: NEL Zone Interest = true)

---

## Phase 4: Knowledge Base (10 minutes)

### Add Your Scripts
- [ ] Write your first-call script
- [ ] Write your viewing script
- [ ] Write your closing script
- [ ] Add 3 common objections and responses

### Add Market Insights
- [ ] Current PSF trends in your focus districts
- [ ] Recent transaction examples
- [ ] Market commentary

---

## Phase 5: Go Live (5 minutes)

### Set Up Daily Routine
- [ ] Morning: Check "Today's Activities" view
- [ ] After each call: Log activity in Activities database
- [ ] Weekly: Review pipeline and update probabilities
- [ ] Monthly: Export data for agency reporting

### Mobile Setup
- [ ] Install Notion mobile app
- [ ] Star your main databases for quick access
- [ ] Test adding a lead from your phone

### Backup
- [ ] Export each database to CSV (monthly backup)
- [ ] Store backups in cloud storage

---

## Phase 6: Advanced (Optional)

### Pro Features
- [ ] Set up NEL zone tracking
- [ ] Add commission calculator formulas
- [ ] Create custom filters for your workflow

### Agency Features
- [ ] Invite team members (if applicable)
- [ ] Set up shared views
- [ ] Configure agent assignments

---

## Quick Reference Card

### Keyboard Shortcuts (Notion)
- `/` — Open command menu
- `[[` — Link to another page
- `@` — Mention a person or date
- `[]` — Create a checkbox
- `/database` — Create inline database

### Critical Fields to Update
- **Leads:** Status, Last Contact Date
- **Properties:** OTP dates, Status
- **Deals:** Stage, Probability, Expected Close Date
- **Activities:** Status, Completed Date

### Weekly Review Tasks
1. Update deal probabilities
2. Log any unrecorded activities
3. Check OTP deadlines for this week
4. Review pipeline value
5. Follow up with cold leads

---

**Setup complete! You're ready to close more deals.**

---

## Troubleshooting

**Database import failed?**
- Check CSV is UTF-8 encoded
- Remove any special characters from addresses
- Try importing smaller batches

**Relations not working?**
- Make sure database names match exactly
- Relations must be set up after both databases exist
- Try refreshing the page

**Formulas showing errors?**
- Check property names match exactly
- Some formulas need at least one record to calculate
- Try adding a sample deal first

---

**Need help?** See `Documentation/QUICK_START.md` or `Documentation/TEMPLATE_SETUP_GUIDE.md`
