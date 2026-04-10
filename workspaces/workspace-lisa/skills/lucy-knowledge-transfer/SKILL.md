# Lucy Knowledge Transfer Skill

## Description
Complete OpenClaw agent replication system. Creates a portable package to replicate Lisa's infrastructure (scripts, configs, memory systems, cron jobs) to a new agent (Lucy) on Mac Studio — or any target machine.

**Use this skill when:**
- Setting up a new OpenClaw agent from scratch
- Backing up Lisa's configuration for disaster recovery
- Replicating proven workflows to a sister agent
- Migrating an agent to a new machine/OS

---

## Tools Used
- `python3` — Script adaptation and path conversion
- `zip` — Package creation
- `openclaw` — Config validation, cron import
- `npm` — OpenClaw installation on target
- `brew` — macOS dependency installation

---

## Usage

### Quick Start (One Command)
```bash
# From Lisa's workspace
python3 ~/.openclaw/workspace-lisa/skills/lucy-knowledge-transfer/scripts/build-package.py --target lucy --output ~/lucy-replication-package.zip
```

### Interactive Mode
```bash
python3 ~/.openclaw/workspace-lisa/skills/lucy-knowledge-transfer/scripts/build-package.py --interactive
```

### Custom Target
```bash
python3 ~/.openclaw/workspace-lisa/skills/lucy-knowledge-transfer/scripts/build-package.py \
  --target my-new-agent \
  --platform macos \
  --output ~/my-agent-package.zip
```

---

## What Gets Packaged

| Component | Source Path | Target Path | Notes |
|-----------|-------------|-------------|-------|
| Memory Nudge | `scripts/memory_nudge.py` | `scripts/memory_nudge.py` | Paths adapted for target OS |
| FTS5 Search | `scripts/fts5_search.py` | `scripts/fts5_search.py` | SQLite-compatible |
| Skill Factory | `scripts/skill_factory.py` | `scripts/skill_factory.py` | Auto-skill creation |
| User Model | `memory/user_model.json` | `templates/user_model.json` | Customizable |
| SOUL Template | — | `templates/SOUL.md` | Role-specific template |
| Cron Jobs | `openclaw cron list` | `cron/*.json` | Exported as JSON |
| Learnings | `.learnings/*.md` | `learnings/*.md` | Pattern library |
| Skills | `skills/*/` | `skills/` | Optional, selective |
| Setup Guide | — | `INSTALL.md` | Step-by-step instructions |
| Checklist | — | `SETUP-CHECKLIST.md` | Verification steps |

---

## Output Structure

```
lucy-replication-package.zip
├── scripts/
│   ├── memory_nudge.py
│   ├── fts5_search.py
│   └── skill_factory.py
├── templates/
│   ├── SOUL.md
│   ├── IDENTITY.md
│   ├── AGENTS.md
│   └── user_model.json
├── cron/
│   ├── lucy-morning-checkin.json
│   ├── lucy-bridge-monitor.json
│   └── ... (all exported crons)
├── learnings/
│   ├── ERRORS.md
│   ├── LEARNINGS.md
│   └── FEATURE_REQUESTS.md
├── secrets-templates/
│   ├── telegram-bot-token.example
│   ├── discord-bot-token.example
│   └── notion-api-key.example
├── INSTALL.md
├── SETUP-CHECKLIST.md
└── README.md
```

---

## Target Platform Adaptations

### Linux → macOS
- Path conversion: `/home/wls/` → `/Users/wls/`
- Chrome path: Custom → `/Applications/Google Chrome.app/...`
- Python: `python3` (same)
- Homebrew prefix: `/opt/homebrew` (M-series) or `/usr/local` (Intel)

### Linux → Linux (Different Machine)
- Path conversion: `/home/wls/` → `/home/<user>/`
- Same OS, minimal changes

### macOS → Linux
- Reverse path conversion
- Chrome path adjustment
- Service startup scripts adapted

---

## Post-Package Steps (Target Machine)

1. **Install Dependencies**
   ```bash
   brew install node@22 python@3.12 git ffmpeg  # macOS
   # or
   sudo apt install nodejs python3 git ffmpeg   # Linux
   ```

2. **Install OpenClaw**
   ```bash
   npm install -g openclaw
   openclaw doctor
   ```

3. **Unzip Package**
   ```bash
   unzip lucy-replication-package.zip -d ~/temp-lucy
   cd ~/temp-lucy
   ```

4. **Copy Files**
   ```bash
   cp -r scripts/* ~/.openclaw/workspace-lucy/scripts/
   cp -r templates/* ~/.openclaw/workspace-lucy/
   cp -r cron/* ~/.openclaw/workspace-lucy/cron-jobs/
   ```

5. **Configure Secrets**
   - Create Telegram bot via @BotFather
   - Create Discord bot (if needed)
   - Save tokens to `~/.openclaw/secrets/`

6. **Update OpenClaw Config**
   - Add agent to `agents.list`
   - Add channel bindings
   - Run `openclaw gateway restart`

7. **Import Cron Jobs**
   ```bash
   for f in cron-jobs/*.json; do
     openclaw cron add --file "$f"
   done
   ```

8. **Verify**
   ```bash
   python3 ~/.openclaw/workspace-lucy/scripts/memory_nudge.py
   python3 ~/.openclaw/workspace-lucy/scripts/fts5_search.py search "test"
   openclaw cron list
   ```

---

## Customization Options

### Change Agent Role
Edit `templates/SOUL.md` before deployment:
- `CEO/Authority` → Full decision power
- `Operator/Executor` → Task-focused
- `Researcher` → Intelligence gathering
- `Specialist` → Domain-specific (trading, content, etc.)

### Change Model
Edit cron jobs and templates:
- Cloud Ollama: `ollama/glm-5.1:cloud`
- Local Ollama: `ollama/glm-5.1` (requires local model download)

### Change Channels
- Telegram only: Minimal setup
- Discord only: Create Discord bot, add to servers
- Both: Configure both channel bindings

### Enable/Disable Features
- Memory Wiki: Toggle in config
- Browser Automation: Requires Chrome debug mode
- Local Ollama: Requires model download (`ollama pull glm-5.1`)

---

## Disaster Recovery

**If Lisa's workspace is corrupted:**
1. Locate latest `lucy-replication-package.zip` (or create new one)
2. Restore to fresh workspace
3. Re-import cron jobs
4. Reconfigure secrets
5. Resume operation

**Backup Frequency:**
- After major config changes
- After new Hermes system deployment
- Monthly (scheduled)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-09 | Initial release — Lisa → Lucy replication |

---

## Notes
- This skill is idempotent — safe to run multiple times
- Package size: ~50-200KB (excluding large skills)
- Excludes: Secrets, large media files, node_modules
- Includes: All scripts, configs, templates, cron definitions

---

## Related Skills
- `skill-creator` — Author new skills from patterns
- `healthcheck` — Verify target system health
- `coding-agent` — Automate code adaptation for target OS
