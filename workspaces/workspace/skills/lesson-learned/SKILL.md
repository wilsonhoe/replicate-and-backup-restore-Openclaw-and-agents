# Lesson-Learned & Self-Improvement Skill

Automated daily lesson capture, error analysis, and self-improvement loops for Lisa.

## Usage

Log a lesson:
```bash
node skills/lesson-learned/lesson.js log "Execution" "Browser automation failed due to selector change" "Use data-testid instead of class" "Update selector library"
```

Daily summary:
```bash
node skills/lesson-learned/lesson.js summary
```

Migrate today’s lessons to MEMORY.md:
```bash
node skills/lesson-learned/lesson.js migrate
```

## Categories
- Execution
- Automation
- Memory
- Revenue
- Security
- Communication

## Automation Hooks
Add to cron for nightly migration:
```
0 23 * * * cd /home/wls/.openclaw/workspace && node skills/lesson-learned/lesson.js migrate
```

## Files
- `lessons/YYYY-MM-DD.md` – daily logs
- Updates `MEMORY.md` – distilled insights