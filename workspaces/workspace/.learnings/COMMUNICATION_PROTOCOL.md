# Communication Protocol - Claude & Lisa Collaboration

**Created:** 2026-03-31T16:35:00Z
**Status:** ACTIVE
**Purpose:** Ensure clear action ownership and prevent deadlocks

---

## The Problem

During the Content Distribution Engine build, a **deadlock incident** occurred where:
- Lisa reported "BLOCKED awaiting human auth"
- Claude asked for status updates
- No explicit action owner was assigned
- Both parties were waiting for the other to act
- Screenshots existed but no proof of completion was sent

**Root Cause:** No explicit action ownership in communication.

---

## The Solution: Action Ownership Protocol

### Rule 1: Every Message Includes Action Owner

Every message must include:

1. **Action Owner** — Who moves next (Claude or Lisa)
2. **Next Action** — What the owner must do
3. **Expected By** — When it should complete
4. **Verification** — Confirm receipt and understanding

### Message Format

```
## [TIMESTAMP] Sender
**Action Owner: [Claude/Lisa]**

[Content...]

**Next Action:** [Specific task]
**Expected By:** [Timeframe]
**Blockers:** [None/Specific blocker]
```

---

## Examples

### Example 1: Assignment from Claude

```
## [2026-04-01T12:20:00Z] Claude
**Action Owner: Lisa**

Create the 7-Day Content Calendar.

**Next Action:** Post Day 2 content with citations
**Expected By:** Next hour
**Blockers:** Report any immediately

— Claude
```

### Example 2: Status Update from Lisa

```
## [2026-03-31T16:25:00Z] Lisa
**Action Owner: Lisa**

**Status: BLOCKED — Twitter Session Expired**

**Next Action:** Re-auth Twitter session (requires Wilson)
**Expected By:** Upon Wilson's return
**Blocker:** Twitter session expired during Day 2 posting attempt

— Lisa
```

### Example 3: Task Complete from Lisa

```
## [2026-03-31T16:40:00Z] Lisa
**Action Owner: Claude**

**Status: COMPLETE — Scheduling Script Created**

**Next Action:** Review and approve scheduling script
**Expected By:** Next 10 minutes
**Blockers:** None

— Lisa
```

---

## Verification Pattern

When receiving a message, confirm understanding:

```
**Received.** 
**Action Owner:** [Confirm who owns next]
**Next Action:** [Confirm what to do]
**Expected By:** [Confirm timeframe]
```

---

## Deadlock Prevention Checklist

Before sending a message, ask yourself:

- [ ] Have I specified who owns the next action?
- [ ] Have I described the specific task?
- [ ] Have I set a clear timeframe?
- [ ] Have I listed any blockers?
- [ ] Have I verified receipt if waiting for a response?

---

## Status Codes

| Status | Meaning |
|--------|---------|
| `COMPLETE` | Task finished successfully |
| `IN PROGRESS` | Working on it now |
| `BLOCKED` | Cannot proceed without external input |
| `PENDING` | Queued but not started |
| `FAILED` | Attempted and failed |

---

## Escalation Rules

If no response within expected timeframe:

1. **5 minutes** — Send reminder
2. **15 minutes** — Escalate to Wilson
3. **30 minutes** — Consider alternative approach

---

## Reference: The Deadlock Incident

**What happened:**
- Lisa reported "BLOCKED awaiting human auth"
- Claude asked for proof of completion
- Lisa had screenshots but didn't send them
- Claude had no proof, Lisa had no response
- Both were waiting for the other to act

**Lesson learned:**
- Always include action owner
- Always include verification method
- Always include expected timeframe
- Always confirm receipt when waiting

---

## Implementation

**For Lisa:**
- Include action ownership in every message to Claude
- Include verification (screenshots, file paths, URLs) when reporting completion
- Include blockers immediately when stuck
- Include expected timeframe for every task

**For Claude:**
- Include action ownership in every message to Lisa
- Specify verification method when assigning tasks
- Set clear timeframes for completion
- Acknowledge receipt of status updates

---

**File Location:** `/home/wls/.openclaw/workspace/.learnings/COMMUNICATION_PROTOCOL.md`
**Last Updated:** 2026-03-31T16:35:00Z