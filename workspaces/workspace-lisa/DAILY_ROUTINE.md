# Lisa's Daily Autonomous Routine

## Overview
This document defines Lisa's automated daily schedule for proactive execution.

## Cron Schedule

### Morning Routine (08:00)
```json
{
  "name": "lisa-morning-checkin",
  "schedule": "0 8 * * *",
  "task": "Morning autonomy check-in",
  "actions": [
    "Read INBOX.md for new assignments",
    "Check BRIDGE_LISA.md for priority updates",
    "Review ERRORS.md for unresolved issues",
    "Scan LEARNINGS.md for relevant patterns",
    "Prioritize revenue tasks for the day",
    "Post status to Discord #general"
  ]
}
```

### Midday Sync (12:00)
```json
{
  "name": "lisa-midday-sync",
  "schedule": "0 12 * * *",
  "task": "Midday progress report",
  "actions": [
    "Review completed tasks",
    "Identify blockers",
    "Adjust priorities if needed",
    "Report progress to BRIDGE_LISA.md"
  ]
}
```

### Evening Wrap (18:00)
```json
{
  "name": "lisa-evening-wrap",
  "schedule": "0 18 * * *",
  "task": "Evening wrap-up",
  "actions": [
    "Log day's learnings to LEARNINGS.md",
    "Update ERRORS.md with any new issues",
    "Plan tomorrow's priorities",
    "Report daily summary to BRIDGE_LISA.md"
  ]
}
```

### Deep Work (20:00)
```json
{
  "name": "lisa-deep-work",
  "schedule": "0 20 * * *",
  "task": "Deep work session",
  "actions": [
    "Focus on highest-value revenue task",
    "No interruptions unless critical",
    "Complete or make significant progress",
    "Log results to workspace"
  ]
}
```

## Activation Commands

```bash
# Create all 4 cron jobs
openclaw cron create --name "lisa-morning" --schedule "0 8 * * *" --agent lisa --task "Execute morning routine: read INBOX, check bridge, prioritize revenue tasks"

openclaw cron create --name "lisa-midday" --schedule "0 12 * * *" --agent lisa --task "Execute midday sync: review progress, identify blockers, adjust priorities"

openclaw cron create --name "lisa-evening" --schedule "0 18 * * *" --agent lisa --task "Execute evening wrap: log learnings, plan tomorrow, report summary"

openclaw cron create --name "lisa-deepwork" --schedule "0 20 * * *" --agent lisa --task "Execute deep work: focus on highest-value revenue task, complete significant progress"
```

## Manual Trigger
```bash
openclaw agent lisa --message "Execute morning routine"
```
