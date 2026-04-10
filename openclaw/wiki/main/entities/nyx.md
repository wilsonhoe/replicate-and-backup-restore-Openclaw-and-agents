---
id: entity.nyx
type: agent
created: 2026-04-09
updated: 2026-04-09
claims:
  - id: claim.nyx.role
    text: "Nyx is the Research Agent / Intelligence layer"
    status: verified
    confidence: 1.0
  - id: claim.nyx.output
    text: "Posts [OPPORTUNITY] findings in Discord #research channel"
    status: verified
    confidence: 1.0
---

# Nyx

**Type:** AI Agent  
**Role:** Research / Intelligence

## Function
- Scans for income opportunities, trending topics, market gaps
- Validates with data (search volume, competitor revenue, forum activity)
- Reports to Lisa via Discord #research

## Output Format
```
[OPPORTUNITY]
Source: [where found]
Validation: [demand evidence]
Monetization: [how to capture]
Complexity: [execution difficulty]
```

## Cron Schedule
- `nyx-morning-research`: 07:00 daily
- `nyx-afternoon-validation`: 14:00 daily
- `nyx-evening-intelligence`: 21:00 daily

## Sources
- SOUL.md
- MEMORY.md

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
