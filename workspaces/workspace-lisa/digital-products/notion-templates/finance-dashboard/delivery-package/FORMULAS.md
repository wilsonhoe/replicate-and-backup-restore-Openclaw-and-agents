# Formula Reference - Notion Finance Dashboard

All formulas used in the Finance Dashboard template.

---

## Budget Planner Formulas

### Remaining
**Property:** Number (Dollar format)

```
prop("Monthly Limit") - prop("Current Spent")
```

**What it does:** Calculates how much budget is left.

---

### Status
**Property:** Formula (Text)

```
if(prop("Remaining") < 0, "🔴 Over Budget", if(prop("Remaining") < prop("Monthly Limit") * 0.8, "🟡 Warning", "🟢 Under Budget"))
```

**What it does:** Shows visual status based on spending:
- 🔴 Over Budget: You've exceeded your limit
- 🟡 Warning: You've spent 80%+ of your budget
- 🟢 Under Budget: You're within budget

**Customize the threshold:** Change `0.8` to `0.7` for earlier warnings or `0.9` for later.

---

## Financial Goals Formulas

### Progress %
**Property:** Formula (Text)

```
format(round(prop("Current Amount") / prop("Target Amount") * 100)) + "%"
```

**What it does:** Shows percentage of goal achieved.

**Example:** $6,500 / $10,000 = 65%

---

### Days Left (Optional)
**Property:** Formula (Number)

```
dateBetween(prop("Deadline"), now(), "days")
```

**What it does:** Shows days remaining until deadline.

**Note:** Shows negative if deadline has passed.

---

### On Track? (Optional)
**Property:** Formula (Text)

```
if(prop("Progress %") >= (100 - (dateBetween(prop("Deadline"), now(), "days") / dateBetween(prop("Deadline"), now(), "days") * 100)), "✅ On Track", "⚠️ Behind")
```

**What it does:** Compares actual progress to expected progress based on time elapsed.

---

## Cash Flow Forecast Formulas

### Ending Balance
**Property:** Formula (Number, Dollar format)

```
prop("Starting Balance") + prop("Expected Income") - prop("Expected Expenses")
```

**What it does:** Projects end-of-month balance.

---

### Month-over-Month Change (Optional)
**Property:** Formula (Percent)

```
if(prop("Starting Balance") == 0, 0, (prop("Ending Balance") - prop("Starting Balance")) / prop("Starting Balance"))
```

**What it does:** Shows growth rate as percentage.

---

## Tax Calculator Formulas

### Taxable Income
**Property:** Formula (Number, Dollar format)

```
prop("Total Income") - prop("Deductible Expenses")
```

**What it does:** Calculates income subject to tax.

---

### Estimated Tax (Simple)
**Property:** Formula (Number, Dollar format)

```
prop("Taxable Income") * 0.22
```

**What it does:** Estimates tax at 22% rate (adjust as needed).

**Customize:** Change `0.22` to your tax bracket:
- 10% = 0.10
- 12% = 0.12
- 22% = 0.22
- 24% = 0.24
- 32% = 0.32
- 35% = 0.35
- 37% = 0.37

---

### Estimated Tax (Advanced with Rate Selection)
**Property:** Formula (Number, Dollar format)

```
prop("Taxable Income") * (if(prop("Tax Rate") == "10%", 0.10, if(prop("Tax Rate") == "12%", 0.12, if(prop("Tax Rate") == "22%", 0.22, if(prop("Tax Rate") == "24%", 0.24, if(prop("Tax Rate") == "32%", 0.32, if(prop("Tax Rate") == "35%", 0.35, 0.37)))))))
```

**What it does:** Uses selected tax rate from dropdown.

---

### Remaining Due
**Property:** Formula (Number, Dollar format)

```
prop("Estimated Tax") - prop("Amount Paid")
```

**What it does:** Shows how much tax you still owe.

---

## Net Worth Tracker Formulas

### Total Assets
**Property:** Formula (Number, Dollar format)

```
prop("Cash") + prop("Investments") + prop("Real Estate") + prop("Other Assets")
```

**What it does:** Sums all asset categories.

---

### Total Liabilities
**Property:** Formula (Number, Dollar format)

```
prop("Loans") + prop("Credit Card Debt") + prop("Other Liabilities")
```

**What it does:** Sums all debt/liabilities.

---

### Net Worth
**Property:** Formula (Number, Dollar format)

```
prop("Total Assets") - prop("Total Liabilities")
```

**What it does:** Calculates your net worth (Assets - Liabilities).

---

### Net Worth Change (Optional)
**Property:** Formula (Number, Dollar format)

Requires a relation to previous month's entry.

```
prop("Net Worth") - prop("Previous Net Worth")
```

**What it does:** Shows month-over-month change in net worth.

---

## Invoice Tracker Formulas

### Days Overdue
**Property:** Formula (Number)

```
if(prop("Status") == "Overdue", dateBetween(now(), prop("Due Date"), "days"), 0)
```

**What it does:** Shows how many days an invoice is overdue.

---

### Days Until Due (Optional)
**Property:** Formula (Number)

```
if(prop("Status") == "Paid", 0, dateBetween(prop("Due Date"), now(), "days"))
```

**What it does:** Shows days remaining until due date (negative if overdue).

---

### Amount Outstanding (Optional)
**Property:** Formula (Number, Dollar format)

```
if(prop("Status") == "Paid", 0, prop("Amount"))
```

**What it does:** Shows amount only if unpaid.

---

## Transactions Formulas (Advanced)

### Month Name (Optional)
**Property:** Formula (Text)

```
formatDate(prop("Date"), "MMMM YYYY")
```

**What it does:** Extracts month name for grouping (e.g., "April 2026").

---

### Week Number (Optional)
**Property:** Formula (Number)

```
formatDate(prop("Date"), "W")
```

**What it does:** Shows week number (1-53).

---

### Category Type (Optional)
**Property:** Formula (Text)

```
if(contains(prop("Category"), "Income"), "💰 Income", if(contains(prop("Category"), "Expense"), "💸 Expense", "📊 Other"))
```

**What it does:** Groups categories into Income/Expense/Other.

---

## Tips for Editing Formulas

### 1. Test Before Saving
- Click "Test" to see result before saving
- Fix errors before closing

### 2. Use Property Names Exactly
- Formula is case-sensitive
- Use exact property names from your database

### 3. Handle Empty Values
```
if(empty(prop("Amount")), 0, prop("Amount"))
```

### 4. Format Numbers
```
format(prop("Amount"))
```

### 5. Format Currency
```
"$" + format(prop("Amount"))
```

### 6. Format Percentages
```
format(prop("Progress") * 100) + "%"
```

---

## Common Formula Errors

### "Property not found"
**Cause:** Property name doesn't match exactly
**Fix:** Check spelling and capitalization

### "Invalid expression"
**Cause:** Syntax error in formula
**Fix:** Check parentheses, commas, quotes

### "Circular reference"
**Cause:** Formula references itself
**Fix:** Remove circular dependency

### "Wrong type"
**Cause:** Trying to do math on text
**Fix:** Ensure properties are correct type (Number, Date, etc.)

---

## Formula Resources

- **Notion Formula Guide:** https://www.notion.so/help/formula-property
- **Notion Formula Examples:** https://www.notion.so/help/formula-examples
- **Formula Reference:** https://www.notion.so/help/formula-property-reference

---

## Need Help?

If a formula isn't working:

1. Check property names match exactly
2. Verify property types (Number vs Text)
3. Test with sample data
4. Simplify complex formulas (build step by step)
5. Contact support for assistance

---

**Version:** 1.0  
**Last Updated:** April 2026
