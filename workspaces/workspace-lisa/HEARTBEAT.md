# HEARTBEAT.md Template

```markdown
# HEARTBEAT.md - Proactive & Self-Improving Tasks

## Daily Checks (rotate during heartbeat polls)

### 1. Browser Health Check
- Run `openclaw browser status`
- If down → run `scripts/chrome-launcher.sh` and verify
- Update TOOLS.md if status changed

### 2. Memory Nudge Check (NEW - P1)
- Run `python3 scripts/memory_nudge.py`
- If nudges found → promote learnings, update skills, or flush to daily memory
- Review .learnings/ for unpromoted entries

### 3. FTS5 Index Update (NEW - P4)
- Run `python3 scripts/fts5_search.py` to re-index memory files
- Ensures search covers latest daily logs

### 4. Skill Quality Review (NEW - P5)
- Check `skills/*/manifest.json` for skills flagged `needs_revision: true`
- If found → update SKILL.md with improved workflow

### 5. Community Intel (if not done today)
- Check if `memory/community-intel/YYYY-MM-DD.md` exists for today
- If missing → cron handles this at 10:00 AM, but flag if after 10 AM

### 6. Self-Improvement Review
- Check `.learnings/` for new entries since last review
- If actionable patterns found → promote to SOUL.md, AGENTS.md, or TOOLS.md

### 7. System Health
- Verify cron jobs are running (`openclaw cron list`)
- Check disk space if needed
- Verify agent coordination (Nyx/Kael last activity)

### 8. Dynamic User Model Update (NEW - P3)
- Review `memory/user_model.json` for accuracy
- If new preferences/patterns observed → update domain expertise scores and priority weights

## Notes
- Rotate through 2-3 checks per heartbeat to limit token burn
- P1-P5 systems auto-check via scripts, heartbeat just triggers them
- Log results to `memory/YYYY-MM-DD.md`
```
