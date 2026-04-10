#!/bin/bash
# ============================================
# OpenClaw & Agents Restore Script
# Usage: ./restore.sh [--dry-run] [--agents-only] [--claude-only]
# ============================================
set -euo pipefail

OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

DRY_RUN=false
AGENTS_ONLY=false
CLAUDE_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --agents-only) AGENTS_ONLY=true ;;
    --claude-only) CLAUDE_ONLY=true ;;
    --help|-h)
      echo "Usage: $0 [--dry-run] [--agents-only] [--claude-only]"
      echo ""
      echo "  --dry-run       Show what would be restored without making changes"
      echo "  --agents-only   Only restore OpenClaw agents (Lisa, Nyx, Kael)"
      echo "  --claude-only   Only restore Claude Code settings"
      echo ""
      echo "  Defaults to full restore of both OpenClaw and Claude Code"
      exit 0
      ;;
  esac
done

run_cmd() {
  if $DRY_RUN; then
    echo "[DRY RUN] $*"
  else
    echo "$ $*"
    "$@"
  fi
}

echo "=== OpenClaw & Agents Restore ==="
echo "Repo:    $REPO_DIR"
echo "OpenClaw: $OPENCLAW_HOME"
echo "Claude:   $CLAUDE_HOME"
echo ""

# --- Pre-flight checks ---
if [ ! -d "$REPO_DIR/openclaw" ]; then
  echo "ERROR: Repository openclaw directory not found at $REPO_DIR/openclaw"
  exit 1
fi

if [ ! -d "$REPO_DIR/claude" ]; then
  echo "ERROR: Repository claude directory not found at $REPO_DIR/claude"
  exit 1
fi

# --- OpenClaw Restore ---
if ! $CLAUDE_ONLY; then
  echo "--- Restoring OpenClaw ---"

  # Create directories
  run_cmd mkdir -p "$OPENCLAW_HOME"
  run_cmd mkdir -p "$OPENCLAW_HOME/agents/lisa/agent"
  run_cmd mkdir -p "$OPENCLAW_HOME/agents/nyx/agent"
  run_cmd mkdir -p "$OPENCLAW_HOME/agents/kael/agent"
  run_cmd mkdir -p "$OPENCLAW_HOME/agents/main/agent"
  run_cmd mkdir -p "$OPENCLAW_HOME/scripts"
  run_cmd mkdir -p "$OPENCLAW_HOME/config"
  run_cmd mkdir -p "$OPENCLAW_HOME/templates"
  run_cmd mkdir -p "$OPENCLAW_HOME/wiki"
  run_cmd mkdir -p "$OPENCLAW_HOME/telegram"
  run_cmd mkdir -p "$OPENCLAW_HOME/devices"
  run_cmd mkdir -p "$OPENCLAW_HOME/subagents"
  run_cmd mkdir -p "$OPENCLAW_HOME/flows"
  run_cmd mkdir -p "$OPENCLAW_HOME/secrets"
  run_cmd mkdir -p "$OPENCLAW_HOME/credentials"
  run_cmd mkdir -p "$OPENCLAW_HOME/workspace-lisa"
  run_cmd mkdir -p "$OPENCLAW_HOME/workspace-nyx"
  run_cmd mkdir -p "$OPENCLAW_HOME/workspace-kael"
  run_cmd mkdir -p "$OPENCLAW_HOME/workspace-main"
  run_cmd mkdir -p "$OPENCLAW_HOME/workspace"
  run_cmd mkdir -p "$OPENCLAW_HOME/sessions"
  run_cmd mkdir -p "$OPENCLAW_HOME/delivery-queue"

  # Agent configs
  for agent in lisa nyx kael main; do
    AGENT_SRC="$REPO_DIR/openclaw/agents/$agent"
    AGENT_DST="$OPENCLAW_HOME/agents/$agent/agent"
    if [ -d "$AGENT_SRC" ]; then
      run_cmd cp -v "$AGENT_SRC/SOUL.md" "$AGENT_DST/" 2>/dev/null || true
      run_cmd cp -v "$AGENT_SRC/auth-profiles.json" "$AGENT_DST/" 2>/dev/null || true
      run_cmd cp -v "$AGENT_SRC/models.json" "$AGENT_DST/" 2>/dev/null || true
      # Skills
      if [ -d "$AGENT_SRC/skills" ]; then
        run_cmd mkdir -p "$OPENCLAW_HOME/agents/$agent/skills"
        run_cmd cp -rv "$AGENT_SRC/skills/"* "$OPENCLAW_HOME/agents/$agent/skills/" 2>/dev/null || true
      fi
    fi
  done

  # Core config
  run_cmd cp -v "$REPO_DIR/openclaw/openclaw.json" "$OPENCLAW_HOME/"
  run_cmd cp -v "$REPO_DIR/openclaw/entities.json" "$OPENCLAW_HOME/" 2>/dev/null || true
  run_cmd cp -v "$REPO_DIR/openclaw/package.json" "$OPENCLAW_HOME/" 2>/dev/null || true

  # Scripts
  run_cmd cp -rv "$REPO_DIR/openclaw/scripts/"* "$OPENCLAW_HOME/scripts/"

  # Config, templates, wiki, etc.
  run_cmd cp -rv "$REPO_DIR/openclaw/config/"* "$OPENCLAW_HOME/config/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/openclaw/templates/"* "$OPENCLAW_HOME/templates/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/openclaw/wiki/"* "$OPENCLAW_HOME/wiki/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/openclaw/telegram/"* "$OPENCLAW_HOME/telegram/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/openclaw/devices/"* "$OPENCLAW_HOME/devices/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/openclaw/subagents/"* "$OPENCLAW_HOME/subagents/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/openclaw/flows/"* "$OPENCLAW_HOME/flows/" 2>/dev/null || true

  # Workspaces (excluding browser profiles and runtime data)
  for ws in workspace-lisa workspace-nyx workspace-kael workspace-main; do
    if [ -d "$REPO_DIR/workspaces/$ws" ]; then
      run_cmd rsync -av --exclude='browser-profiles' --exclude='daily_stock_analysis' \
        "$REPO_DIR/workspaces/$ws/" "$OPENCLAW_HOME/$ws/"
    fi
  done

  # .env - create from template if not exists
  if [ ! -f "$OPENCLAW_HOME/.env" ] && [ -f "$REPO_DIR/.env.example" ]; then
    echo ""
    echo "NOTE: .env not found. Copy .env.example and fill in your secrets:"
    echo "  cp $REPO_DIR/.env.example $OPENCLAW_HOME/.env"
    echo "  nano $OPENCLAW_HOME/.env"
  fi

  # npm install
  if [ -f "$OPENCLAW_HOME/package.json" ]; then
    echo ""
    echo "Installing OpenClaw dependencies..."
    run_cmd bash -c "cd $OPENCLAW_HOME && npm install"
  fi

  echo "--- OpenClaw restore complete ---"
  echo ""
fi

# --- Claude Code Restore ---
if ! $AGENTS_ONLY; then
  echo "--- Restoring Claude Code ---"

  run_cmd mkdir -p "$CLAUDE_HOME"
  run_cmd mkdir -p "$CLAUDE_HOME/agents"
  run_cmd mkdir -p "$CLAUDE_HOME/rules"
  run_cmd mkdir -p "$CLAUDE_HOME/skills"
  run_cmd mkdir -p "$CLAUDE_HOME/commands"
  run_cmd mkdir -p "$CLAUDE_HOME/hooks"
  run_cmd mkdir -p "$CLAUDE_HOME/memory"
  run_cmd mkdir -p "$CLAUDE_HOME/projects"

  # Settings (redacted - user must fill in secrets)
  if [ -f "$REPO_DIR/claude/settings.json" ]; then
    echo ""
    echo "IMPORTANT: settings.json contains REDACTED secrets."
    echo "After restore, edit $CLAUDE_HOME/settings.json and fill in:"
    echo "  - MCP server environment variables"
    echo "  - Permission allow lists"
    echo "  - Auto-approve safe commands"
    echo ""
    run_cmd cp -v "$REPO_DIR/claude/settings.json" "$CLAUDE_HOME/"
  fi

  run_cmd cp -v "$REPO_DIR/claude/settings.local.json" "$CLAUDE_HOME/" 2>/dev/null || true
  run_cmd cp -v "$REPO_DIR/claude/CLAUDE.md" "$CLAUDE_HOME/"

  # Agents, rules, skills, etc.
  run_cmd cp -rv "$REPO_DIR/claude/agents/"* "$CLAUDE_HOME/agents/"
  run_cmd cp -rv "$REPO_DIR/claude/rules/"* "$CLAUDE_HOME/rules/"
  run_cmd cp -rv "$REPO_DIR/claude/skills/"* "$CLAUDE_HOME/skills/"
  run_cmd cp -rv "$REPO_DIR/claude/commands/"* "$CLAUDE_HOME/commands/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/claude/hooks/"* "$CLAUDE_HOME/hooks/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/claude/memory/"* "$CLAUDE_HOME/memory/" 2>/dev/null || true
  run_cmd cp -rv "$REPO_DIR/claude/projects/"* "$CLAUDE_HOME/projects/" 2>/dev/null || true

  # Other key files
  run_cmd cp -v "$REPO_DIR/claude/AGENTS.md" "$CLAUDE_HOME/" 2>/dev/null || true
  run_cmd cp -v "$REPO_DIR/claude/EVERYTHING-CLAUDE-CODE.md" "$CLAUDE_HOME/" 2>/dev/null || true
  run_cmd cp -v "$REPO_DIR/claude/soul.md" "$CLAUDE_HOME/" 2>/dev/null || true

  echo "--- Claude Code restore complete ---"
  echo ""
fi

echo "=== Restore Complete ==="
echo ""
if ! $DRY_RUN; then
  echo "Post-restore steps:"
  echo "  1. Edit $OPENCLAW_HOME/.env with your actual secrets"
  echo "  2. Edit $CLAUDE_HOME/settings.json to fill in REDACTED values"
  echo "  3. Run: cd $OPENCLAW_HOME && npm install"
  echo "  4. Set up secrets in $OPENCLAW_HOME/secrets/"
  echo "  5. Restart OpenClaw and Claude Code"
else
  echo "This was a dry run. Remove --dry-run to actually restore."
fi