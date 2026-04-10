# SG Property Pro — Feature Comparison

## Quick Reference: What's in Each Edition

| Feature | Starter | Pro | Agency |
|---------|:-------:|:---:|:------:|
| **Core Databases** |
| Leads database | ✅ | ✅ | ✅ |
| Properties database | ✅ | ✅ | ✅ |
| Deals database | ✅ | ✅ | ✅ |
| Activities database | ✅ | ✅ | ✅ |
| Knowledge base | Basic | Full | Full |
| **Singapore-Specific Features** |
| D1-28 district tracking | ✅ | ✅ | ✅ |
| HDB/Condo/Landed types | ✅ | ✅ | ✅ |
| BTO/Resale distinction | ✅ | ✅ | ✅ |
| OTP workflow tracking | Basic | Advanced | Advanced |
| PSF calculations | Manual | Auto | Auto |
| **NEL Zone Intelligence** |
| NEL zone tagging | — | ✅ | ✅ |
| NEL corridor filtering | — | ✅ | ✅ |
| NEL marketing templates | — | ✅ | ✅ |
| **Commission Features** |
| Basic commission tracking | ✅ | ✅ | ✅ |
| Auto-calculated splits | — | ✅ | ✅ |
| Weighted pipeline value | — | ✅ | ✅ |
| Multi-agent splits | — | — | ✅ |
| **Productivity Tools** |
| Sample data (20+ records) | ✅ | ✅ | ✅ |
| Activity templates | Basic | Full | Full |
| Sales scripts | — | ✅ | ✅ |
| Objection handling | — | ✅ | ✅ |
| **Team Features** |
| Team sharing | — | — | ✅ |
| Agent performance dashboard | — | — | ✅ |
| Shared pipeline view | — | — | ✅ |
| White-label ready | — | — | ✅ |
| **Bonuses** |
| HDB OTP Checklist | — | ✅ | ✅ |
| Commission Calculator | — | ✅ | ✅ |

**Legend:** ✅ Included — Not included

---

## Database Schema by Edition

### All Editions Include:

**Leads Database**
- Name, Phone, Email, Budget Min/Max
- Property Type Preference (HDB/Condo/Landed)
- District Preference (D1-28)
- NEL Zone Interest (Pro/Agency only)
- Source (Referral, PropertyGuru, Facebook, etc.)
- Status: New → Contacted → Qualified → Active → Closed Lost
- Created Date, Last Contact Date
- Notes

**Properties Database**
- Address, Postal Code, District (D1-28)
- Property Type: HDB (BTO/Resale), Condo (Executive/Private), Landed (Terrace/Semi-D/Bungalow)
- Size (sqft), Asking Price, PSF
- OTP: Option Fee Date, Exercise Date, Completion Date
- Commission: Buyer %, Seller %, Total %
- Status: Available → Under Offer → Sold → Off Market
- Owner Contact, Key Holder

**Deals Database**
- Linked Lead, Linked Property
- Stage: Prospecting → Viewing → Negotiation → OTP → Closing → Commission Received
- Probability %
- Expected Close Date, Actual Close Date
- Commission: Gross, Agency Split %, Net
- Weighted Value (Probability × Net Commission)

**Activities Database**
- Type: Call, Viewing, Follow-up, Meeting, Documentation
- Linked Lead/Deal
- Due Date, Completed Date
- Status: Pending → Completed → Cancelled
- Notes, Outcome
- Priority: Low, Medium, High

**Knowledge Base Database**
- Category: Script, Objection, Process, Market Insight, Lesson Learned
- Title, Content
- Usage Count, Last Used Date
- Effectiveness Rating (Pro/Agency only)

---

## Which Edition Should I Use?

### Start with Starter if:
- You're a new agent (< 2 years experience)
- You're currently using Excel or paper
- You close < 5 deals per quarter
- You want to test the system before upgrading

### Upgrade to Pro if:
- You're actively working the NEL corridor
- You want automated commission calculations
- You need sales scripts and objection handling
- You close 5-15 deals per quarter

### Choose Agency if:
- You lead a team of 2+ agents
- You need shared pipeline visibility
- You want white-label branding
- You're managing 20+ active deals

---

## Migration Path

**Starter → Pro:** Import additional CSV files for NEL zones, commission formulas, and knowledge base items.

**Pro → Agency:** Import team dashboard, add agent assignments to deals, enable shared views.

---

## Technical Specifications

| Spec | Value |
|------|-------|
| Platform | Notion |
| Required Plan | Free Personal |
| Import Format | CSV |
| Mobile Support | Yes (iOS/Android apps) |
| Offline Access | Limited (Notion feature) |
| Data Export | Yes (Notion native) |
| Team Sharing | Agency only |

---

**All three editions are included in your purchase. Start with Starter and upgrade as you grow.**
