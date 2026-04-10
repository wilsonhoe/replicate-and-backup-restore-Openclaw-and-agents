<div align="center">

# OpenClaw Multi-Agent System

### Backup, Restore & Replicate Your AI Agent Stack

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security: Redacted](https://img.shields.io/badge/Secrets-REDACTED-brightgreen.svg)]()
[![Agents: 4](https://img.shields.io/badge/Agents-4-blue.svg)]()
[![Skills: 130+](https://img.shields.io/badge/Skills-130+-9cf.svg)]()

*A complete backup and restore toolkit for the OpenClaw multi-agent system — Lisa, Nyx, Kael, and the Main orchestrator — plus Claude Code configuration. One command to replicate your entire AI agent stack on any machine.*

</div>

---

## Why This Exists

Setting up a multi-agent AI system from scratch is painful. After months of configuring agents, writing skills, tuning prompts, and wiring bridges between agents, the last thing you want is to lose it all — or spend days recreating it on a new machine.

This repo solves that. It's a **battle-tested backup and restore system** that:

- Captures your complete agent stack in one `git clone`
- Redacts all secrets automatically before they reach the repo
- Restores everything with a single command
- Works across machines, OS reinstalls, or just for peace of mind

## What's Inside

### OpenClaw Agents (`openclaw/`)

| Agent | Role | Skills |
|-------|------|--------|
| **Lisa** | Marketing, Revenue, Social Media | Content creation, analytics, Zoho integration |
| **Nyx** | Research, Analysis | Data analysis, web research, reporting |
| **Kael** | Automation, Deployment | System ops, CI/CD, infrastructure |
| **Main** | Orchestrator | Agent coordination, bridge monitoring |

Each agent includes:
- `SOUL.md` — Personality, instructions, and behavioral rules
- `models.json` — Model routing configuration
- `skills/` — Agent-specific skill definitions

### System Configuration (`openclaw/`)

- `openclaw.json` — Main system config (secrets redacted)
- `entities.json` — Entity definitions and relationships
- `scripts/` — Bridge monitors, SSO login, system monitors, MemPalace CLI
- `templates/` — Message templates and flow registry
- `wiki/` — Knowledge base, concepts, syntheses, reports
- `telegram/` — Telegram bot integration
- `devices/` — Device pairing configurations
- `subagents/` — Subagent run states

### Claude Code Settings (`claude/`)

- **30+ agent definitions** — architect, planner, code-reviewer, security-reviewer, and more
- **130+ skills** — From TDD to deployment, from Python to Rust
- **Rules** — Common, web, and language-specific coding rules
- **Hooks** — Pre/post tool use automation
- **Memory** — Project memory files
- **Global CLAUDE.md** — Your personalized Claude instructions

### Workspaces (`workspaces/`)

Each agent has its own workspace with scripts, skills, and working files — excluding browser profiles and generated data.

## Security

This repo is designed to be **safe to make public**:

| Protection | How |
|-----------|-----|
| API keys | Auto-redacted to `REDACTED_SET_FROM_ENV` |
| Discord tokens | Removed from all Python/JSON/shell files |
| Telegram tokens | Redacted from scripts and configs |
| JWT access tokens | Excluded via `.gitignore` (`auth-profiles.json`) |
| `.env` files | Gitignored — use `.env.example` as template |
| Browser profiles | Excluded (500MB+ runtime data) |
| Session data | Excluded (ephemeral) |
| Claude project history | Excluded (contains tool call results) |

All secret values are replaced with `REDACTED_SET_FROM_ENV` so you know exactly where to fill in your own values on restore.

## Quick Start

### Restore to a New Machine

```bash
# 1. Clone this repo
git clone https://github.com/wilsonhoe/replicate-and-backup-restore-Openclaw-and-agents.git
cd replicate-and-backup-restore-Openclaw-and-agents

# 2. Preview what will be restored
./scripts/restore.sh --dry-run

# 3. Full restore
./scripts/restore.sh

# 4. Set up your secrets
cp .env.example ~/.openclaw/.env
nano ~/.openclaw/.env  # Fill in your actual tokens

# 5. Fill in REDACTED values in Claude settings
nano ~/.claude/settings.json

# 6. Install dependencies
cd ~/.openclaw && npm install

# 7. Restart services
```

### Update Backup

```bash
# Sync latest state from your live system
./scripts/backup.sh --dry-run  # Preview changes
./scripts/backup.sh            # Sync for real

# Commit and push
git add -A
git commit -m "sync: backup update $(date +%Y-%m-%d)"
git push
```

### Partial Restore

```bash
# Only restore OpenClaw agents (Lisa, Nyx, Kael)
./scripts/restore.sh --agents-only

# Only restore Claude Code settings
./scripts/restore.sh --claude-only
```

## Architecture

```
~/.openclaw/                    # OpenClaw home
├── agents/                     # Agent configurations
│   ├── lisa/                   # Marketing & revenue
│   ├── nyx/                    # Research & analysis
│   ├── kael/                   # Automation & deployment
│   └── main/                   # Orchestrator
├── workspace-{agent}/          # Per-agent workspaces
├── scripts/                   # Bridge monitors, tools
├── wiki/                      # Knowledge base
├── secrets/                   # API tokens (NOT in repo)
└── .env                       # Environment variables (NOT in repo)

~/.claude/                      # Claude Code home
├── settings.json               # Settings (secrets REDACTED)
├── CLAUDE.md                   # Global instructions
├── agents/                     # 30+ agent definitions
├── rules/                      # Coding rules & standards
├── skills/                     # 130+ skill definitions
├── hooks/                      # Automation hooks
└── memory/                     # Project memory
```

## Post-Restore Checklist

- [ ] Edit `~/.openclaw/.env` with your actual API tokens
- [ ] Edit `~/.claude/settings.json` to replace all `REDACTED_SET_FROM_ENV` values
- [ ] Set up `~/.openclaw/secrets/` with individual token files
- [ ] Set up `~/.openclaw/credentials/` with Discord pairing files
- [ ] Run `npm install` in `~/.openclaw/`
- [ ] Install Python venv for MemPalace
- [ ] Verify Telegram bot token
- [ ] Verify Discord bot tokens
- [ ] Test agent bridge monitors
- [ ] Restart OpenClaw daemon

## How the Backup Script Works

The `backup.sh` script:

1. **Syncs agent configs** from `~/.openclaw/agents/` to `openclaw/agents/`
2. **Redacts secrets** from `openclaw.json` using inline Python (any auth value >10 chars becomes `REDACTED_SET_FROM_ENV`)
3. **Copies system files** — scripts, config, templates, wiki, telegram, devices, subagents
4. **Syncs workspaces** — excluding browser profiles, daily analysis data, and venvs
5. **Redacts Claude settings** — env vars, MCP server env, permissions, and auto-approve lists

Run with `--dry-run` to preview what will change without writing anything.

## How the Restore Script Works

The `restore.sh` script:

1. **Creates directory structure** — all required paths under `~/.openclaw/` and `~/.claude/`
2. **Copies agent configs** — SOUL.md, models.json, and skills for each agent
3. **Restores system files** — scripts, config, templates, wiki, telegram, devices
4. **Syncs workspaces** — excluding runtime data
5. **Warns about redacted secrets** — you must fill in your own values
6. **Runs `npm install`** if package.json exists

Supports `--dry-run`, `--agents-only`, and `--claude-only` flags.

## Environment Variables

See `.env.example` for the full list. Key variables:

| Variable | Purpose |
|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot integration |
| `DISCORD_LISA_TOKEN` | Lisa's Discord bot |
| `DISCORD_NYX_TOKEN` | Nyx's Discord bot |
| `DISCORD_KAEL_TOKEN` | Kael's Discord bot |
| `OPENAI_API_KEY` | OpenAI API access |
| `GITHUB_PAT` | GitHub personal access token |

## Contributing

Found a security issue? Please open an issue first before creating a PR. All contributions that improve the backup/restore workflow are welcome.

## License

MIT — Use freely. Just don't commit real secrets.

---

<div align="center">

**If this saved you from rebuilding your agent stack from scratch, consider giving it a star** ⭐

</div>