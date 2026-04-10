# 📊 Notion Finance Dashboard - Complete Template
**Price:** $39 | **Target:** Freelancers, Solopreneurs

---

## QUICK START (For Manual Build - 30 minutes)

### Step 1: Create Main Page
1. Open Notion
2. Create new page: "💰 Finance Dashboard"
3. Add icon: 💰 or 📊
4. Add cover image (optional - finance themed)

### Step 2: Create Databases (Inline)

Type `/database` and create each database inline on the page:

---

## DATABASE 1: 💸 Transactions
**Type:** Table (Inline)

**Columns:**
| Column Name | Type | Options/Format |
|-------------|------|----------------|
| Name | Title | - |
| Amount | Number | Dollar format |
| Category | Select | Income, Freelance, Investment, Salary, Expense-Business, Expense-Personal, Tax |
| Date | Date | - |
| Type | Select | Income, Expense |
| Status | Select | Pending, Completed, Reconciled |
| Source | Select | Bank, Cash, Credit Card, PayPal, Stripe |
| Client/Project | Text | - |
| Notes | Text | - |

**Views to Create:**
1. **All Transactions** (Table) - Sort: Date ↓
2. **This Month** (Table) - Filter: Date = This month
3. **Income Only** (Table) - Filter: Type = Income
4. **Expenses Only** (Table) - Filter: Type = Expense
5. **By Category** (Board) - Group by: Category

**Sample Data (Add 5-10 entries):**
- Freelance Project - Website Design | $2,500 | Freelance | Apr 1 | Income | Completed | Bank
- Office Supplies | -$150 | Expense-Business | Apr 3 | Expense | Completed | Credit Card
- Monthly Software | -$99 | Expense-Business | Apr 5 | Expense | Completed | Credit Card
- Consulting Gig | $1,800 | Freelance | Apr 10 | Income | Completed | Bank
- Client Dinner | -$85 | Expense-Business | Apr 12 | Expense | Completed | Credit Card

---

## DATABASE 2: 💰 Budget Planner
**Type:** Table (Inline)

**Columns:**
| Column Name | Type | Options/Format |
|-------------|------|----------------|
| Category | Title | - |
| Monthly Limit | Number | Dollar format |
| Current Spent | Number | Dollar format |
| Remaining | Formula | `prop("Monthly Limit") - prop("Current Spent")` |
| Status | Formula | See below |

**Status Formula:**
```
if(prop("Remaining") < 0, "🔴 Over Budget", if(prop("Remaining") < prop("Monthly Limit") * 0.8, "🟡 Warning", "🟢 Under Budget"))
```

**Views:**
1. **All Budgets** (Table)
2. **Over Budget** (Table) - Filter: Status contains "Over"

**Sample Data:**
| Category | Monthly Limit | Current Spent |
|----------|---------------|---------------|
| Marketing & Ads | $500 | $275 |
| Software & Tools | $200 | $180 |
| Office Supplies | $100 | $45 |
| Travel | $300 | $0 |
| Professional Dev | $150 | $50 |

---

## DATABASE 3: 📋 Invoice Tracker
**Type:** Table (Inline)

**Columns:**
| Column Name | Type | Options/Format |
|-------------|------|----------------|
| Invoice # | Title | - |
| Client | Text | - |
| Amount | Number | Dollar format |
| Date Sent | Date | - |
| Due Date | Date | - |
| Status | Select | Draft, Sent, Paid, Overdue, Cancelled |
| Paid Date | Date | - |
| Notes | Text | - |

**Days Overdue Formula (Optional):**
```
if(prop("Status") == "Overdue", dateBetween(now(), prop("Due Date"), "days"), 0)
```

**Views:**
1. **All Invoices** (Table) - Sort: Due Date ↑
2. **Outstanding** (Table) - Filter: Status = Sent OR Overdue
3. **Overdue** (Table) - Filter: Status = Overdue
4. **Paid** (Table) - Filter: Status = Paid
5. **By Status** (Board) - Group by: Status

**Sample Data:**
| Invoice # | Client | Amount | Date Sent | Due Date | Status |
|-----------|--------|--------|-----------|----------|--------|
| INV-2026-001 | ABC Corporation | $3,500 | Mar 15 | Apr 15 | Sent |
| INV-2026-002 | XYZ Startup | $1,200 | Mar 20 | Apr 20 | Sent |
| INV-2026-003 | Local Business | $800 | Feb 1 | Mar 1 | Overdue |
| INV-2025-045 | Previous Client | $5,000 | Dec 15 | Jan 15 | Paid |

---

## DATABASE 4: 🎯 Financial Goals
**Type:** Gallery or Table (Inline)

**Columns:**
| Column Name | Type | Options/Format |
|-------------|------|----------------|
| Goal | Title | - |
| Target Amount | Number | Dollar format |
| Current Amount | Number | Dollar format |
| Deadline | Date | - |
| Priority | Select | High, Medium, Low |
| Status | Select | Not Started, In Progress, Achieved |
| Progress % | Formula | See below |
| Notes | Text | - |

**Progress % Formula:**
```
format(round(prop("Current Amount") / prop("Target Amount") * 100)) + "%"
```

**Views:**
1. **All Goals** (Gallery) - Show: Progress bar
2. **In Progress** (Table) - Filter: Status = In Progress
3. **Achieved** (Table) - Filter: Status = Achieved

**Sample Data:**
| Goal | Target | Current | Deadline | Priority | Status |
|------|--------|---------|----------|----------|--------|
| Emergency Fund - $10K | $10,000 | $6,500 | Dec 31 | High | In Progress |
| New Laptop | $3,000 | $1,200 | Jun 30 | Medium | In Progress |
| Vacation Fund | $5,000 | $5,000 | Aug 15 | Low | Achieved |
| Tax Savings Q1 | $4,000 | $0 | Mar 31 | High | Not Started |

---

## DATABASE 5: 📈 Cash Flow Forecast
**Type:** Table (Inline)

**Columns:**
| Column Name | Type | Options/Format |
|-------------|------|----------------|
| Month | Title | - |
| Starting Balance | Number | Dollar format |
| Expected Income | Number | Dollar format |
| Expected Expenses | Number | Dollar format |
| Ending Balance | Formula | `prop("Starting Balance") + prop("Expected Income") - prop("Expected Expenses")` |
| Notes | Text | - |

**Views:**
1. **6-Month Forecast** (Table) - Sort: Month
2. **Monthly Summary** (Gallery)

**Sample Data:**
| Month | Starting | Income | Expenses | Ending |
|-------|----------|--------|----------|--------|
| April 2026 | $8,500 | $5,000 | $3,200 | $10,300 |
| May 2026 | $10,300 | $6,000 | $3,500 | $12,800 |
| June 2026 | $12,800 | $5,500 | $4,000 | $14,300 |
| July 2026 | $14,300 | $7,000 | $3,800 | $17,500 |
| August 2026 | $17,500 | $5,000 | $5,500 | $17,000 |
| September 2026 | $17,000 | $6,500 | $3,200 | $20,300 |

---

## DATABASE 6: 🧾 Tax Calculator
**Type:** Table (Inline)

**Columns:**
| Column Name | Type | Options/Format |
|-------------|------|----------------|
| Quarter | Title | - |
| Total Income | Number | Dollar format |
| Deductible Expenses | Number | Dollar format |
| Taxable Income | Formula | `prop("Total Income") - prop("Deductible Expenses")` |
| Tax Rate | Select | 10%, 12%, 22%, 24%, 32%, 35%, 37% |
| Estimated Tax | Formula | `prop("Taxable Income") * 0.22` (or use rate from select) |
| Amount Paid | Number | Dollar format |
| Remaining Due | Formula | `prop("Estimated Tax") - prop("Amount Paid")` |

**Views:**
1. **2026 Quarters** (Table)
2. **Tax Summary** (Gallery)

**Sample Data:**
| Quarter | Income | Expenses | Taxable | Rate | Est. Tax | Paid | Due |
|---------|--------|----------|---------|------|----------|------|-----|
| Q1 2026 | $15,000 | $3,500 | $11,500 | 22% | $2,530 | $2,000 | $530 |
| Q2 2026 | $18,000 | $4,200 | $13,800 | 22% | $3,036 | $0 | $3,036 |

---

## DATABASE 7: 💵 Net Worth Tracker
**Type:** Table (Inline)

**Columns:**
| Column Name | Type | Options/Format |
|-------------|------|----------------|
| Date | Title | - |
| Cash | Number | Dollar format |
| Investments | Number | Dollar format |
| Real Estate | Number | Dollar format |
| Other Assets | Number | Dollar format |
| Total Assets | Formula | `prop("Cash") + prop("Investments") + prop("Real Estate") + prop("Other Assets")` |
| Loans | Number | Dollar format |
| Credit Card Debt | Number | Dollar format |
| Other Liabilities | Number | Dollar format |
| Total Liabilities | Formula | `prop("Loans") + prop("Credit Card Debt") + prop("Other Liabilities")` |
| Net Worth | Formula | `prop("Total Assets") - prop("Total Liabilities")` |

**Views:**
1. **History** (Table) - Sort: Date ↓
2. **Net Worth Trend** (Timeline if available)

**Sample Data:**
| Date | Cash | Investments | Real Estate | Assets | Loans | CC Debt | Liabilities | Net Worth |
|------|------|-------------|-------------|--------|-------|---------|-------------|-----------|
| Apr 2026 | $12,000 | $25,000 | $0 | $37,000 | $0 | $3,500 | $3,500 | $33,500 |
| Mar 2026 | $10,500 | $24,000 | $0 | $34,500 | $0 | $4,200 | $4,200 | $30,300 |

---

## MAIN DASHBOARD LAYOUT

Arrange the page like this:

```
┌─────────────────────────────────────────────────────────────┐
│  💰 Finance Dashboard                                       │
│  Your complete money management system                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## 📊 This Month Overview                                  │
│  [Linked view of Transactions - Income this month]          │
│  [Linked view of Transactions - Expenses this month]        │
│  [Linked view of Budget Planner]                            │
│                                                             │
│  ## 💸 Transactions                                         │
│  [Full Transactions Database]                               │
│                                                             │
│  ## 💰 Budget Planner                                       │
│  [Full Budget Database]                                     │
│                                                             │
│  ## 📋 Invoice Tracker                                      │
│  [Full Invoice Database]                                    │
│                                                             │
│  ## 🎯 Financial Goals                                      │
│  [Full Goals Database - Gallery View]                       │
│                                                             │
│  ## 📈 Cash Flow Forecast                                   │
│  [Full Forecast Database]                                   │
│                                                             │
│  ## 🧾 Tax Calculator                                       │
│  [Full Tax Database]                                        │
│                                                             │
│  ## 💵 Net Worth Tracker                                    │
│  [Full Net Worth Database]                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## MAKING IT SHAREABLE

### Option 1: Public Link (Easiest)
1. Click "Share" in top right
2. Click "Publish" tab
3. Toggle "Publish to web" ON
4. Copy the link
5. For duplicate access, add `?duplicate=true` to the URL

### Option 2: Template Button (Advanced)
1. Type `/template` on the page
2. Configure to duplicate all databases
3. Share the page

---

## SCREENSHOTS TO CAPTURE

1. **Hero Shot** - Full dashboard scroll (top to bottom)
2. **Transactions View** - Table with colorful categories
3. **Budget Progress** - Showing the formula results
4. **Invoice Board** - Kanban view by status
5. **Goals Gallery** - Progress bars visible
6. **Cash Flow** - 6-month forecast table
7. **Mobile View** - Show it works on phone

**Screenshot Tips:**
- Use clean sample data
- Hide browser bookmarks bar
- Use light mode for clarity
- Crop to focus on content
- Export as PNG, 1920x1080 minimum

---

## DELIVERY FILES

Create a PDF with:
1. Welcome message
2. "Duplicate Template" button/link
3. Quick start instructions (3 steps)
4. Video tutorial link (if created)
5. Support contact info

**PDF Text:**
```
🎉 Welcome to Your Finance Dashboard!

Thanks for purchasing! Here's how to get started:

1. CLICK HERE TO DUPLICATE THE TEMPLATE
   [Insert Notion duplicate link]

2. Watch the 5-minute setup video:
   [Insert video link]

3. Start adding your transactions!

Questions? Reply to this email or contact support.

Enjoy your new finance system! 💰
```

---

## VIDEO TUTORIAL SCRIPT (5 minutes)

**[0:00-0:30] Intro**
"Hey! In this video, I'll show you how to set up the Finance Dashboard in under 5 minutes."

**[0:30-1:30] Duplicate the Template**
"First, click the duplicate link. This creates a copy in your workspace..."

**[1:30-3:00] Add Your First Transactions**
"Let's add a few transactions. Click New, enter the details..."

**[3:00-4:00] Set Up Your Budget**
"Now let's set your budget categories. These are your spending limits..."

**[4:00-5:00] Explore the Views**
"Check out the different views - board, calendar, timeline. Customize as needed..."

**[5:00] Outro**
"That's it! You're all set. Check out the other databases for invoices, goals, and more."

---

## PRICING JUSTIFICATION

**$39 One-Time Payment**

Competitor Analysis:
- Notion Finance templates on Gumroad: $15-50
- Spreadsheet templates: $10-30
- Full accounting software: $10-50/month

Value Proposition:
- One-time payment (no subscription)
- 7 integrated databases
- Pre-built formulas
- Video tutorial included
- Lifetime updates
- 30-day money-back guarantee

---

## MARKETING COPY (Short Versions)

**Twitter (280 chars):**
Stop using spreadsheets for your finances.

The Notion Finance Dashboard helps freelancers track income, expenses, budgets, and goals in one beautiful system.

✅ 7 databases
✅ Pre-built formulas
✅ 5-min setup

$39 one-time → [link]

**LinkedIn:**
Freelancers: Are you still using spreadsheets to manage your business finances?

There's a better way.

I built the Notion Finance Dashboard specifically for solopreneurs who need:
- Income/expense tracking
- Budget planning
- Invoice management
- Tax estimation
- Cash flow forecasting

All in one place. No subscription. One-time $39.

Check it out: [link]

**Instagram/TikTok:**
POV: You finally stopped using 5 different apps to manage your money 📊

Notion Finance Dashboard = everything in one place
• Track income/expenses
• Set budgets
• Manage invoices
• Plan cash flow

Link in bio! $39 one-time 💰

---

## LAUNCH CHECKLIST

- [ ] Template fully built in Notion
- [ ] All 7 databases created with sample data
- [ ] Formulas tested and working
- [ ] Page made public/duplicateable
- [ ] Screenshots captured (5-7 images)
- [ ] Video tutorial recorded (optional)
- [ ] Delivery PDF created
- [ ] Gumroad account created
- [ ] Listing created with all copy
- [ ] Payment connected (Stripe)
- [ ] Test purchase completed
- [ ] Launch announcement written
- [ ] Social posts scheduled

---

## SUPPORT EMAILS

### Pre-Purchase Inquiry
**Subject:** Re: Notion Finance Dashboard question

"Thanks for your interest!

Yes, the template works with the free Notion plan. Once you duplicate it, it's 100% yours to customize.

The $39 is a one-time payment with lifetime updates. And there's a 30-day money-back guarantee if it doesn't work for you.

Any other questions? Happy to help!

Best,
[Your name]"

### Post-Purchase Support
**Subject:** Re: Help with Finance Dashboard

"Thanks for purchasing!

[Answer their specific question]

Let me know if you need anything else!

Best,
[Your name]"

### Refund Request
**Subject:** Re: Refund request

"No problem at all! I've processed your refund.

If you change your mind or have questions about setup, feel free to reach out.

Best,
[Your name]"

---

## SUCCESS METRICS

Track these on Gumroad:
- Views → Purchases conversion rate
- Average refund rate (should be <5%)
- Customer reviews (aim for 4.5+ stars)
- Repeat customers
- Revenue per day/week/month

**Goal:** $1,000/month = ~26 sales at $39

---

## NEXT STEPS AFTER LAUNCH

1. Collect customer feedback
2. Add requested features
3. Create update announcements
4. Build email list of customers
5. Consider upsells (advanced templates, coaching)
6. Expand to other platforms (Etsy, own website)
