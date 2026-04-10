# Commission Calculator

## Google Sheets Template

### Instructions

1. Open Google Sheets
2. Go to File → Make a copy
3. Use the formulas below

---

## Deal Calculator Tab

### Single Deal Commission

| Field | Input | Formula/Value |
|-------|-------|---------------|
| **Property Price** | $________ | User input |
| **Commission %** | ____% | User input (e.g., 2.0%) |
| **Gross Commission** | Auto | `=Price * Commission%` |
| **Agency Split %** | ____% | User input (e.g., 30%) |
| **Agent Portion** | Auto | `=Gross Commission * (1 - Agency Split%)` |
| **GST (9%)** | Auto | `=Agent Portion * 0.09` |
| **Net Commission** | Auto | `=Agent Portion - GST` |
| **Probability** | ____% | Deal closing probability |
| **Weighted Commission** | Auto | `=Net Commission * Probability%` |

### Example: $650,000 HDB Deal

| Field | Value |
|-------|-------|
| Property Price | $650,000 |
| Commission % | 2.0% |
| **Gross Commission** | **$13,000** |
| Agency Split | 30% |
| **Agent Portion** | **$9,100** |
| GST (9%) | $819 |
| **Net Commission** | **$8,281** |
| Probability | 75% |
| **Weighted Commission** | **$6,211** |

---

## Monthly Summary Tab

| Deal | Price | Commission % | Gross | Agent Portion | GST | Net | Probability | Weighted |
|------|-------|--------------|-------|---------------|-----|-----|-------------|----------|
| Deal 1 | $650,000 | 2.0% | $13,000 | $9,100 | $819 | $8,281 | 75% | $6,211 |
| Deal 2 | $580,000 | 2.0% | $11,600 | $8,120 | $731 | $7,389 | 90% | $6,650 |
| Deal 3 | $2,800,000 | 1.0% | $28,000 | $19,600 | $1,764 | $17,836 | 75% | $13,377 |
| **TOTAL** | | | **$52,600** | **$36,820** | **$3,314** | **$33,506** | | **$26,238** |

### Formulas for Monthly Summary

- **Total Gross**: `=SUM(D2:D10)`
- **Total Agent**: `=SUM(E2:E10)`
- **Total GST**: `=SUM(F2:F10)`
- **Total Net**: `=SUM(G2:G10)`
- **Total Weighted**: `=SUM(I2:I10)`

---

## Co-Broke Calculator Tab

### Split Commission Calculation

| Field | Agent A | Agent B | Total |
|-------|---------|---------|-------|
| **Split %** | ____% | Auto | 100% |
| **Gross Commission** | Auto | Auto | `=Total Gross` |
| **Agent Portion** | Auto | Auto | `=Gross * Split%` |
| **GST** | Auto | Auto | `=Portion * 0.09` |
| **Net Commission** | Auto | Auto | `=Portion - GST` |

### Example: 50/50 Split on $650,000 Deal

| Field | Agent A | Agent B |
|-------|---------|---------|
| Split % | 50% | 50% |
| Gross Commission | $6,500 | $6,500 |
| Agency Split (30%) | $1,950 | $1,950 |
| Agent Portion | $4,550 | $4,550 |
| GST (9%) | $410 | $410 |
| **Net Commission** | **$4,140** | **$4,140** |

---

## Year-End Tax Summary Tab

### Annual Commission Tracking

| Month | Gross | Agent Portion | GST | Net | CPF (Optional) | Take Home |
|-------|-------|---------------|-----|-----|----------------|-----------|
| Jan | | | | | | |
| Feb | | | | | | |
| ... | | | | | | |
| **Total** | `=SUM()` | `=SUM()` | `=SUM()` | `=SUM()` | `=SUM()` | `=SUM()` |

---

## Quick Reference Formulas

```
Gross Commission = Property Price × Commission %
Agent Portion = Gross Commission × (1 - Agency Split %)
GST = Agent Portion × 0.09
Net Commission = Agent Portion - GST
Weighted Commission = Net Commission × Probability %
```

---

## Singapore-Specific Notes

- **GST Rate**: 9% (as of 2024)
- **Agency Splits**: Typically 20-40% to agency
- **HDB Commission**: Usually 1-2%
- **Private Commission**: Usually 1-2%
- **Landed Commission**: Usually 1%
- **Co-broke Splits**: Usually 50/50

---

## Tax Reporting

Track these for annual tax filing:
- Total Gross Commission
- Agency Fees Paid
- GST Collected
- Business Expenses (fuel, phone, marketing)
- CPF Contributions (if applicable)

**File**: Commission Calculator (Google Sheets)
**Access**: Make a copy to your Google Drive
