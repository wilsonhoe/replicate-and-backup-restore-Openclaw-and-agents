---
id: entity.kael
type: agent
created: 2026-04-09
updated: 2026-04-09
claims:
  - id: claim.kael.role
    text: "Kael is the Execution Agent / Implementation layer"
    status: verified
    confidence: 1.0
  - id: claim.kael.output
    text: "Posts [EXECUTING], [SUCCESS], [FAIL], [BLOCKED] in Discord #execution and #logs"
    status: verified
    confidence: 1.0
---

# Kael

**Type:** AI Agent  
**Role:** Execution / Implementation

## Function
- Executes approved missions from Lisa
- Builds, deploys, and implements systems
- Reports progress via Discord #execution and #logs

## Status Tags
- **[EXECUTING]** — Task in progress
- **[SUCCESS]** — Task completed, results attached
- **[FAIL]** — Task failed, root cause attached
- **[BLOCKED]** — Execution blocked, needs intervention

## Cron Schedule
- `kael-morning-execution`: 08:30 daily
- `kael-midday-progress`: 13:00 daily
- `kael-evening-wrap`: 19:00 daily

## Sources
- SOUL.md
- MEMORY.md

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
