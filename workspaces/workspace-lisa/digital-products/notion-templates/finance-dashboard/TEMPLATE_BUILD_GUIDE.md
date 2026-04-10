# Notion Finance Dashboard - Build Guide
**Template Page ID:** 33b99ce8-2630-815e-b271-d069f14b10e9
**URL:** https://www.notion.so/Finance-Dashboard-Template-33b99ce82630815eb271d069f14b10e9

---

## CURRENT STATUS
✅ Main template page created
✅ Basic structure outlined
⏳ Databases need to be created
⏳ Formulas need to be added
⏳ Views need to be configured
⏳ Page needs to be made public/shareable

---

## DATABASES TO CREATE

### 1. Transactions Database
**Purpose:** Track all income and expenses

**Properties:**
- Name (Title) - Transaction name/description
- Amount (Number, format: USD) - Transaction amount
- Category (Select) - Income, Freelance, Investment, Salary, Expense-Business, Expense-Personal, Tax
- Date (Date) - Transaction date
- Type (Select) - Income, Expense
- Status (Select) - Pending, Completed, Reconciled
- Source (Select) - Bank, Cash, Credit Card, PayPal, Stripe
- Notes (Rich Text) - Additional details
- Client/Project (Rich Text) - For freelance income tracking

**Views:**
- All Transactions (Table, sorted by Date descending)
- This Month (Table, filtered by Date = This month)
- Income Only (Table, filtered by Type = Income)
- Expenses Only (Table, filtered by Type = Expense)
- By Category (Board, grouped by Category)

---

### 2. Budget Planner Database
**Purpose:** Monthly budget limits and tracking

**Properties:**
- Category (Title) - Budget category name
- Monthly Limit (Number, format: USD) - Budget limit
- Current Spent (Rollup) - Sum of expenses in this category
- Remaining (Formula) - Monthly Limit - Current Spent
- Alert Threshold (Number, %) - Percentage at which to alert (e.g., 80)
- Status (Formula) - "Under Budget" / "Warning" / "Over Budget"

**Formula: Remaining**
```
prop("Monthly Limit") - prop("Current Spent")
```

**Formula: Status**
```
if(prop("Remaining") < 0, "🔴 Over Budget", if(prop("Remaining") < prop("Monthly Limit") * prop("Alert Threshold") / 100, "🟡 Warning", "🟢 Under Budget"))
```

**Views:**
- All Budgets (Table)
- Over Budget (Table, filtered by Status contains "Over")
- By Category (Board)

---

### 3. Cash Flow Forecast Database
**Purpose:** 6-month cash flow projection

**Properties:**
- Month (Title) - e.g., "April 2026"
- Starting Balance (Number, USD)
- Expected Income (Number, USD)
- Expected Expenses (Number, USD)
- Ending Balance (Formula) - Starting + Income - Expenses
- Notes (Rich Text)

**Formula: Ending Balance**
```
prop("Starting Balance") + prop("Expected Income") - prop("Expected Expenses")
```

**Views:**
- 6-Month Forecast (Timeline or Table)
- Monthly Summary (Gallery)

---

### 4. Tax Calculator Database
**Purpose:** Estimate and track tax obligations

**Properties:**
- Quarter (Title) - e.g., "Q1 2026"
- Total Income (Rollup) - Sum of income transactions
- Deductible Expenses (Rollup) - Sum of business expenses
- Taxable Income (Formula) - Total Income - Deductible Expenses
- Tax Rate (Select) - 10%, 12%, 22%, 24%, 32%, 35%, 37%
- Estimated Tax (Formula) - Taxable Income × Tax Rate
- Amount Paid (Number, USD)
- Remaining Due (Formula) - Estimated Tax - Amount Paid

**Views:**
- 2026 Quarters (Table)
- Tax Summary (Gallery)

---

### 5. Invoice Tracker Database
**Purpose:** Track client invoices

**Properties:**
- Invoice # (Title) - Invoice number
- Client (Rich Text) - Client name
- Amount (Number, USD)
- Date Sent (Date)
- Due Date (Date)
- Status (Select) - Draft, Sent, Paid, Overdue, Cancelled
- Days Overdue (Formula) - if(Status = "Overdue", now() - Due Date, 0)
- Paid Date (Date)
- Notes (Rich Text)

**Views:**
- All Invoices (Table)
- Outstanding (Table, filtered by Status = Sent or Overdue)
- Overdue (Table, filtered by Status = Overdue)
- Paid (Table, filtered by Status = Paid)

---

### 6. Financial Goals Database
**Purpose:** Track financial milestones

**Properties:**
- Goal (Title) - Goal name
- Target Amount (Number, USD)
- Current Amount (Number, USD)
- Deadline (Date)
- Progress % (Formula) - Current / Target × 100
- Priority (Select) - High, Medium, Low
- Status (Select) - Not Started, In Progress, Achieved
- Notes (Rich Text)

**Formula: Progress %**
```
format(round(prop("Current Amount") / prop("Target Amount") * 100)) + "%"
```

**Views:**
- All Goals (Gallery with progress bars)
- In Progress (Table)
- Achieved (Table, filtered by Status = Achieved)

---

### 7. Net Worth Tracker Database
**Purpose:** Track overall wealth

**Properties:**
- Date (Title) - Snapshot date
- Cash (Number, USD)
- Investments (Number, USD)
- Real Estate (Number, USD)
- Other Assets (Number, USD)
- Total Assets (Formula) - Sum of all assets
- Loans (Number, USD)
- Credit Card Debt (Number, USD)
- Other Liabilities (Number, USD)
- Total Liabilities (Formula) - Sum of all liabilities
- Net Worth (Formula) - Total Assets - Total Liabilities

**Views:**
- History (Table, sorted by Date)
- Net Worth Trend (Timeline)

---

## MAIN DASHBOARD LAYOUT

### Section 1: Header
- Title: "💰 Finance Dashboard"
- Quick stats (using linked database views with calculations)

### Section 2: This Month Overview
- Income (linked view of Transactions, filtered + summed)
- Expenses (linked view of Transactions, filtered + summed)
- Net (Income - Expenses)
- Budget Status (linked view of Budget Planner)

### Section 3: Quick Actions
- Add Transaction (button or link to new page)
- Create Invoice
- Review Budget

### Section 4: Cash Flow Forecast
- Linked view of Cash Flow Forecast (next 6 months)

### Section 5: Outstanding Invoices
- Linked view of Invoice Tracker (filtered: Status = Sent or Overdue)

### Section 6: Financial Goals Progress
- Linked view of Financial Goals (Gallery with progress)

---

## MAKING THE TEMPLATE SHAREABLE

### Step 1: Share the Page
1. Open the template page in Notion
2. Click "Share" in top right
3. Click "Publish" tab
4. Toggle "Publish to web" ON
5. Copy the public link

### Step 2: Create Distribution PDF
Create a PDF with:
1. Welcome message
2. Link to duplicate template (use the public link with ?duplicate=true)
3. Link to video tutorial
4. Quick start instructions

### Step 3: Test the Duplicate Link
1. Open in incognito browser
2. Verify the "Duplicate" button appears
3. Test duplicating to a test workspace

---

## SCREENSHOTS TO CAPTURE

1. **Main Dashboard** - Full view showing all sections
2. **Transactions View** - Table with sample data
3. **Budget Planner** - Showing progress bars and status
4. **Cash Flow Forecast** - 6-month timeline view
5. **Tax Calculator** - Quarter summary view
6. **Invoice Tracker** - Board view by status
7. **Financial Goals** - Gallery with progress bars

**Screenshot specs:**
- Resolution: 1920x1080 minimum
- Format: PNG
- Clean browser window (no bookmarks bar, minimal UI)
- Use sample data that looks realistic

---

## NEXT STEPS

1. Complete all database creation in Notion
2. Add formulas and rollups
3. Create linked views on main dashboard
4. Add sample data for demonstration
5. Make page public and get shareable link
6. Capture screenshots
7. Create distribution PDF
8. Set up Gumroad listing
9. Test purchase flow
10. Launch

---

## NOTION API SCRIPTS (Optional Automation)

If building via API, use these endpoints:
- POST /v1/data_sources - Create databases
- PATCH /v1/blocks/{page_id}/children - Add content
- POST /v1/pages - Create entries

API Key: Stored in ~/.config/notion/api_key
