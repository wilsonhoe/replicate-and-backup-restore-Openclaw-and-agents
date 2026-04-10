# Multi-Agent Coordination Protocol

## Agent Hierarchy

```
User (Wilson)
    ↓
Lisa (Authority Layer)
    ↓
    ├── Nyx (Intelligence Layer)
    └── Kael (Execution Layer)
```

## Communication Matrix

| From | To | Channel | Purpose |
|------|-----|---------|---------|
| Nyx | Lisa | #research | Opportunities, research findings |
| Nyx | Lisa | INBOX.md | Direct intelligence reports |
| Lisa | Kael | #command_center | Approved tasks, requirements |
| Lisa | Kael | INBOX.md | Direct assignments |
| Kael | Lisa | #logs | Execution results, evidence |
| All | Claude | BRIDGE_*.md | Technical guidance, escalations |

## Discord Channel Purpose

### #research
- Nyx posts [OPPORTUNITY] with validation
- Lisa responds with [APPROVED]/[REJECTED]
- Market trends, competitor analysis

### #command_center
- Lisa posts directives to agents
- Agent status updates
- System-wide announcements
- Escalations from agents

### #execution
- Kael posts [EXECUTING] when starting work
- Progress updates for long tasks
- Technical blockers

### #logs
- Kael posts [SUCCESS] or [FAIL] with evidence
- Error logs with context
- Performance metrics

### #general
- Revenue reports
- Daily summaries
- Team coordination

## Opportunity Flow

```
┌─────────┐    [OPPORTUNITY]     ┌─────────┐
│   Nyx   │ ───────────────────→│  Lisa   │
│discovers│                      │reviews  │
└─────────┘                      └────┬────┘
                                      │
                         [APPROVED]   │
                                      ↓
                               ┌─────────────┐
                               │ Opportunity │
                               │   approved  │
                               └──────┬──────┘
                                      │
                                      ↓ [ASSIGNED]
┌─────────┐    [EXECUTING]     ┌─────────────┐
│  Kael   │ ←───────────────────│  INBOX.md   │
│  builds │                      │  assigned   │
└────┬────┘                      └─────────────┘
     │
     │ [SUCCESS] + evidence
     ↓
┌─────────┐   [SCALE]/[OPTIMIZE]  ┌─────────┐
│ #logs   │ ───────────────────→ │  Lisa   │
│ report  │                      │decides  │
└─────────┘                      └─────────┘
```

## Response Time Expectations

| Agent | Channel | Check Frequency | Response Time |
|-------|---------|-----------------|---------------|
| Nyx | Discord | Every 5 min | Within 2 min of mention |
| Lisa | Discord | Every 5 min | Within 2 min of mention |
| Kael | Discord | Every 5 min | Within 2 min of mention |
| All | INBOX.md | Every 5 min | Within 10 min |
| All | BRIDGE_*.md | Every 5 min | Within 10 min |

## Status Tags

### Nyx
- `[OPPORTUNITY]` - New validated opportunity
- `[TREND]` - Market trend identified
- `[VALIDATED]` - Research confirmed with sources
- `[BLOCKED]` - Research blocked, needs input

### Lisa
- `[APPROVED]` - Opportunity approved for execution
- `[REJECTED]` - Opportunity declined
- `[ASSIGNED]` - Task assigned to agent
- `[REVIEW]` - Requesting agent review
- `[SCALE]` - Expand successful execution
- `[OPTIMIZE]` - Improve existing execution
- `[TERMINATE]` - Stop execution

### Kael
- `[EXECUTING]` - Started work
- `[PROGRESS]` - Update on long task (every 30 min)
- `[SUCCESS]` - Task completed with evidence
- `[FAIL]` - Task failed after 10 attempts
- `[BLOCKED]` - Stuck, needs help

## Error Handling Flow

```
Agent encounters error
        ↓
Try self-healing (10 attempts)
        ↓
    Success? ──Yes──→ Log to .learnings/ERRORS.md
        │                    ↓
        No              Continue work
        ↓
Post [BLOCKED] in Discord
        ↓
Lisa reviews in #command_center
        ↓
    Can resolve? ──Yes──→ Provides guidance
        │                       ↓
        No                Agent continues
        ↓
Escalate to user via BRIDGE
        ↓
Log resolution to ERRORS.md
```

## Daily Schedule Alignment

| Time | Nyx | Lisa | Kael |
|------|-----|------|------|
| 07:00 | Morning research | - | - |
| 08:00 | - | Morning check-in | - |
| 08:30 | - | - | Morning execution |
| 12:00 | - | Midday sync | - |
| 13:00 | - | - | Midday progress |
| 14:00 | Afternoon validation | - | - |
| 18:00 | - | Evening wrap | - |
| 19:00 | - | - | Evening wrap |
| 20:00 | - | Deep work | - |
| 21:00 | Evening intelligence | - | - |

## Learning File Locations

| Agent | Learnings | Errors | Features |
|-------|-----------|--------|----------|
| Nyx | `workspace-nyx/.learnings/LEARNINGS.md` | `workspace-nyx/.learnings/ERRORS.md` | `workspace-nyx/.learnings/FEATURE_REQUESTS.md` |
| Lisa | `workspace-lisa/.learnings/LEARNINGS.md` | `workspace-lisa/.learnings/ERRORS.md` | `workspace-lisa/.learnings/FEATURE_REQUESTS.md` |
| Kael | `workspace-kael/.learnings/LEARNINGS.md` | `workspace-kael/.learnings/ERRORS.md` | `workspace-kael/.learnings/FEATURE_REQUESTS.md` |

## Conflict Resolution

1. **Same task assigned to multiple agents** - First to [EXECUTING] claims it, others support
2. **Disagreement on approach** - Lisa decides, agents implement
3. **Agent unavailable** - Task escalates to Lisa for reassignment
4. **Circular dependencies** - Break loop, assign to single agent with full context

## Success Metrics

- **Nyx**: Validated opportunities / week, research accuracy
- **Lisa**: Tasks approved/executed, revenue generated, blocker resolution time
- **Kael**: Tasks completed, success rate, evidence quality

---

**Protocol Version:** 1.0
**Last Updated:** 2026-04-06
**Maintained by:** System
