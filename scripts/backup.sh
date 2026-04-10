#!/bin/bash
# ============================================
# OpenClaw & Agents Backup Script
# Run from the repo root to sync latest state
# Usage: ./scripts/backup.sh [--dry-run]
# ============================================
set -euo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

DRY_RUN=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
  esac
done

run_cmd() {
  if $DRY_RUN; then
    echo "[DRY RUN] $*"
  else
    "$@"
  fi
}

echo "=== Syncing backup from live system ==="
echo "OpenClaw: $OPENCLAW_HOME"
echo "Claude:   $CLAUDE_HOME"
echo "Repo:     $REPO_DIR"
echo ""

# --- OpenClaw Agents ---
for agent in lisa nyx kael; do
  echo "Syncing $agent..."
  run_cmd cp -v "$OPENCLAW_HOME/agents/$agent/agent/SOUL.md" "$REPO_DIR/openclaw/agents/$agent/" 2>/dev/null || true
  run_cmd cp -v "$OPENCLAW_HOME/agents/$agent/agent/auth-profiles.json" "$REPO_DIR/openclaw/agents/$agent/" 2>/dev/null || true
  run_cmd cp -v "$OPENCLAW_HOME/agents/$agent/agent/models.json" "$REPO_DIR/openclaw/agents/$agent/" 2>/dev/null || true
  if [ -d "$OPENCLAW_HOME/agents/$agent/skills" ]; then
    run_cmd rsync -av --delete "$OPENCLAW_HOME/agents/$agent/skills/" "$REPO_DIR/openclaw/agents/$agent/skills/"
  fi
done

# Main agent
run_cmd cp -v "$OPENCLAW_HOME/agents/main/agent/SOUL.md" "$REPO_DIR/openclaw/agents/main/" 2>/dev/null || true
run_cmd cp -v "$OPENCLAW_HOME/agents/main/agent/auth-profiles.json" "$REPO_DIR/openclaw/agents/main/" 2>/dev/null || true
run_cmd cp -v "$OPENCLAW_HOME/agents/main/agent/models.json" "$REPO_DIR/openclaw/agents/main/" 2>/dev/null || true

# --- OpenClaw System Config ---
echo "Syncing OpenClaw system config..."
# Redact secrets from openclaw.json
run_cmd python3 -c "
import json
with open('$OPENCLAW_HOME/openclaw.json') as f:
    d = json.load(f)
if 'auth' in d:
    for k in d['auth']:
        if isinstance(d['auth'][k], str) and len(d['auth'][k]) > 10:
            d['auth'][k] = 'REDACTED_SET_FROM_ENV'
with open('$REPO_DIR/openclaw/openclaw.json', 'w') as f:
    json.dump(d, f, indent=2)
"

run_cmd cp -v "$OPENCLAW_HOME/entities.json" "$REPO_DIR/openclaw/"
run_cmd cp -v "$OPENCLAW_HOME/package.json" "$REPO_DIR/openclaw/"
run_cmd rsync -av --delete "$OPENCLAW_HOME/scripts/" "$REPO_DIR/openclaw/scripts/" --exclude='__pycache__'
run_cmd rsync -av "$OPENCLAW_HOME/config/" "$REPO_DIR/openclaw/config/"
run_cmd rsync -av "$OPENCLAW_HOME/templates/" "$REPO_DIR/openclaw/templates/"
run_cmd rsync -av "$OPENCLAW_HOME/wiki/" "$REPO_DIR/openclaw/wiki/"
run_cmd rsync -av "$OPENCLAW_HOME/telegram/" "$REPO_DIR/openclaw/telegram/" --exclude='sessions'
run_cmd rsync -av "$OPENCLAW_HOME/subagents/" "$REPO_DIR/openclaw/subagents/"
run_cmd rsync -av "$OPENCLAW_HOME/devices/" "$REPO_DIR/openclaw/devices/"

# --- Workspaces ---
echo "Syncing workspaces..."
for ws in workspace-lisa workspace-nyx workspace-kael workspace-main; do
  if [ -d "$OPENCLAW_HOME/$ws" ]; then
    run_cmd rsync -av --delete \
      --exclude='browser-profiles' \
      --exclude='daily_stock_analysis' \
      --exclude='venv' \
      --exclude='__pycache__' \
      "$OPENCLAW_HOME/$ws/" "$REPO_DIR/workspaces/$ws/"
  fi
done

# --- Claude Code ---
echo "Syncing Claude Code..."
run_cmd python3 -c "
import json
with open('$CLAUDE_HOME/settings.json') as f:
    d = json.load(f)
if 'env' in d:
    for k in d['env']:
        d['env'][k] = 'REDACTED_SET_FROM_ENV'
if 'mcpServers' in d:
    for srv in d['mcpServers']:
        if 'env' in d['mcpServers'][srv]:
            for k in d['mcpServers'][srv]['env']:
                d['mcpServers'][srv]['env'][k] = 'REDACTED_SET_FROM_ENV'
if 'permissions' in d and 'allow' in d['permissions']:
    d['permissions']['allow'] = ['[REDACTED - review and set manually]']
if 'autoApprove' in d and 'safeCommands' in d['autoApprove']:
    d['autoApprove']['safeCommands'] = ['[REDACTED - review and set manually]']
with open('$REPO_DIR/claude/settings.json', 'w') as f:
    json.dump(d, f, indent=2)
"

run_cmd rsync -av "$CLAUDE_HOME/agents/" "$REPO_DIR/claude/agents/"
run_cmd rsync -av "$CLAUDE_HOME/rules/" "$REPO_DIR/claude/rules/"
run_cmd rsync -av "$CLAUDE_HOME/skills/" "$REPO_DIR/claude/skills/"
run_cmd rsync -av "$CLAUDE_HOME/commands/" "$REPO_DIR/claude/commands/" 2>/dev/null || true
run_cmd rsync -av "$CLAUDE_HOME/hooks/" "$REPO_DIR/claude/hooks/" 2>/dev/null || true
run_cmd rsync -av "$CLAUDE_HOME/memory/" "$REPO_DIR/claude/memory/" 2>/dev/null || true
run_cmd rsync -av "$CLAUDE_HOME/projects/" "$REPO_DIR/claude/projects/" --exclude='*.log' --exclude='*.jsonl' 2>/dev/null || true

echo ""
echo "=== Backup sync complete ==="
echo "Next: cd $REPO_DIR && git add -A && git commit -m 'sync: latest backup' && git push"