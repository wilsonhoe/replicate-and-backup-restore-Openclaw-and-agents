# HEARTBEAT.md Template

```markdown
# HEARTBEAT.md - Proactive & Self-Improving Tasks

## Daily Checks (rotate during heartbeat polls)

### 1. Browser Health Check
- Run `openclaw browser status`
- If down → run `scripts/chrome-launcher.sh` and verify
- Update TOOLS.md if status changed

### 2. Community Intel (if not done today)
- Check if `memory/community-intel/YYYY-MM-DD.md` exists for today
- If missing → cron handles this at 10:00 AM, but if heartbeat is after 10 AM and report is missing, flag it

### 3. Self-Improvement Review
- Check `.learnings/` for new entries since last review
- If actionable patterns found → promote to SOUL.md, AGENTS.md, or TOOLS.md

### 4. System Health
- Verify cron jobs are running (`openclaw cron list`)
- Check disk space if needed
- Verify agent coordination (Nyx/Kael last activity)

## Notes
- Only run 1-2 checks per heartbeat to limit token burn
- Rotate through checks across heartbeats
- Log results to `memory/YYYY-MM-DD.md`
```
