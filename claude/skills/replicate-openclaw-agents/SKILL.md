---
name: replicate-openclaw-agents
description: Backup and restore the complete OpenClaw multi-agent system (Lisa, Nyx, Kael, Main) plus Claude Code configuration. One command to replicate your entire AI agent stack on a new machine, with automatic secret redaction for safe public repos.
origin: OpenClaw
---

# Replicate OpenClaw Agents

Back up, restore, and replicate the entire OpenClaw multi-agent system and Claude Code configuration to any machine.

## When to Activate

- User says "replicate openclaw", "backup openclaw", "restore openclaw", "move openclaw to new machine", "clone my agent stack", or similar
- User wants to back up their OpenClaw + Claude Code setup to GitHub
- User wants to restore an OpenClaw setup from the backup repo
- User wants to transfer secrets via USB for a new machine
- User wants to verify their backup is current and complete

## Overview

The backup repo lives at:
```
https://github.com/wilsonhoe/replicate-and-backup-restore-Openclaw-and-agents
```

Local path:
```
~/replicate-and-backup-restore-Openclaw-and-agents
```

It contains:
- `openclaw/` — Agent configs (SOUL.md, models.json, skills/), system config, scripts, wiki, telegram, devices
- `claude/` — Claude Code settings, agents, rules, skills, hooks, memory
- `workspaces/` — Per-agent workspace files (excluding browser profiles and runtime data)
- `scripts/backup.sh` — Syncs live system into the repo (with secret redaction)
- `scripts/restore.sh` — Restores from repo to a new machine
- `.env.example` — Template for environment variables

## Operations

### Backup (Sync Live System to Repo)

Run from repo root:

```bash
cd ~/replicate-and-backup-restore-Openclaw-and-agents

# Preview changes
./scripts/backup.sh --dry-run

# Sync for real
./scripts/backup.sh

# Commit and push
git add -A
git commit -m "sync: backup update $(date +%Y-%m-%d)"
git push
```

**What backup.sh does:**
1. Syncs agent configs from `~/.openclaw/agents/` to `openclaw/agents/`
2. Redacts secrets from `openclaw.json` (any auth value >10 chars becomes `REDACTED_SET_FROM_ENV`)
3. Copies system files (scripts, config, templates, wiki, telegram, devices, subagents)
4. Syncs workspaces (excluding browser profiles, daily analysis, venvs)
5. Redacts Claude settings (env vars, MCP env, permissions, auto-approve lists)

### Restore (New Machine)

```bash
# 1. Clone the repo
git clone https://github.com/wilsonhoe/replicate-and-backup-restore-Openclaw-and-agents.git
cd replicate-and-backup-restore-Openclaw-and-agents

# 2. Preview what will be restored
./scripts/restore.sh --dry-run

# 3. Full restore
./scripts/restore.sh

# 4. Set up secrets (see Secrets section below)
cp .env.example ~/.openclaw/.env
nano ~/.openclaw/.env

# 5. Fill in REDACTED values in Claude settings
nano ~/.claude/settings.json

# 6. Install dependencies
cd ~/.openclaw && npm install

# 7. Copy auth profiles (from USB secrets)
# Copy auth-profiles-{lisa,nyx,kael,main}.json to respective agent dirs

# 8. Restart services
```

Partial restore options:
```bash
./scripts/restore.sh --agents-only    # Only OpenClaw agents
./scripts/restore.sh --claude-only    # Only Claude Code settings
```

### Secrets Transfer (USB)

For moving to a new machine where network secret transfer is risky:

```bash
# 1. Consolidate all secrets to a directory
mkdir -p ~/Downloads/secret

# 2. Copy .env
cp ~/.openclaw/.env ~/Downloads/secret/dot-env

# 3. Copy individual secret files
cp -r ~/.openclaw/secrets/* ~/Downloads/secret/

# 4. Copy auth profiles (for direct restore)
for agent in lisa nyx kael main; do
  cp ~/.openclaw/agents/$agent/agent/auth-profiles.json \
     ~/Downloads/secret/auth-profiles-$agent.json
done

# 5. Copy email config
cp ~/.openclaw/config/email.json ~/Downloads/secret/email.json

# 6. Create consolidated reference file
# (See "Consolidated Secrets File" section below)

# 7. Set restrictive permissions
chmod -R 600 ~/Downloads/secret/

# 8. Copy to USB, then DELETE from both locations after restore
```

### Consolidated Secrets File

Create a single human-readable file (`openclaw-secrets.conf`) containing:

| Section | Source | Keys |
|---------|--------|------|
| Environment Variables | `~/.openclaw/.env` | TELEGRAM_BOT_TOKEN, DISCORD_BOT_TOKEN, DISCORD_KAEL_TOKEN, DISCORD_NYX_TOKEN, OPENCLAW_GATEWAY_TOKEN |
| API Keys | `~/.openclaw/secrets/` | github-pat, google-maps-key, notion-api-key, openai-api-key, telegram-bot-token, discord-*-token, gateway-token |
| OAuth Tokens | `~/.openclaw/agents/*/agent/auth-profiles.json` | OpenAI Codex refresh tokens, access tokens, account IDs |
| Extra Profiles | Main agent auth-profiles.json | Google API key, Ollama key, xAI Grok key, secondary OpenAI profile |
| Email | `~/.openclaw/config/email.json` | Lisa bot Gmail + app password |
| Discord Pairing | `~/.openclaw/credentials/` | allowFrom user ID |
| Claude Settings | `~/.claude/settings.json` | Non-secret env vars (MAX_THINKING_TOKENS, etc.), MCP config |

### Verify Backup Integrity

```bash
# Check no secrets leaked into the repo
cd ~/replicate-and-backup-restore-Openclaw-and-agents

# Search for common secret patterns
git grep -i "sk-proj\|sk-\|xai-\|ghp_\|github_pat_\|ntn_\|AIzaSy\|bot_token\|MTQ4" -- '*.json' '*.md' '*.sh' '*.py' '*.js' '*.env.example'

# Verify REDACTED placeholders exist
grep -r "REDACTED_SET_FROM_ENV" openclaw/openclaw.json claude/settings.json

# Check gitignore is covering secrets
grep -E "\.env|secrets|credentials|auth-profiles" .gitignore
```

### Post-Restore Checklist

After restoring on a new machine:
- [ ] Edit `~/.openclaw/.env` with actual API tokens
- [ ] Edit `~/.claude/settings.json` to replace all `REDACTED_SET_FROM_ENV` values
- [ ] Copy `auth-profiles-{agent}.json` to `~/.openclaw/agents/{agent}/agent/auth-profiles.json`
- [ ] Set up `~/.openclaw/secrets/` with individual token files
- [ ] Set up `~/.openclaw/credentials/` with Discord pairing files
- [ ] Run `npm install` in `~/.openclaw/`
- [ ] Install Python venv for MemPalace
- [ ] Verify Telegram bot token
- [ ] Verify Discord bot tokens
- [ ] Test agent bridge monitors
- [ ] Restart OpenClaw daemon
- [ ] Delete secrets file from USB and local machine

## Security Guarantees

The backup repo is designed to be **safe for public sharing**:

| Protection | Method |
|-----------|--------|
| API keys | Auto-redacted to `REDACTED_SET_FROM_ENV` |
| Discord tokens | Removed from all Python/JSON/shell files |
| Telegram tokens | Redacted from scripts and configs |
| JWT access tokens | Excluded via `.gitignore` (`auth-profiles.json`) |
| `.env` files | Gitignored — use `.env.example` as template |
| Browser profiles | Excluded (500MB+ runtime data) |
| Session data | Excluded (ephemeral) |
| Claude project history | Excluded (contains tool call results) |

**Critical**: The `backup.sh` script handles redaction automatically. Never manually copy secrets into the repo. Always run `backup.sh` and verify with `git grep` before pushing.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| GitHub push rejected (secret scan) | Rewrite git history: `git reset --soft HEAD~1 && git commit --amend`, verify with `git grep`, then push |
| Auth profiles expired after restore | Run `openclaw login` on each agent to refresh OAuth tokens |
| `npm install` fails | Check Node.js version >= 18, delete `node_modules` and retry |
| Bridge monitors not starting | Verify `.env` tokens, check `~/.openclaw/secrets/` files exist |
| Missing workspace files | Re-run `./scripts/restore.sh` or check `.gitignore` exclusions |