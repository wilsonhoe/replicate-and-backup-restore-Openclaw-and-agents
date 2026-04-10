# Claw-Code Integration for OpenClaw

Full integration of claw-code (Claude Code reimplementation) into OpenClaw's agent execution flow.

## Quick Start

```bash
cd /home/wls/.openclaw/workspace/skills/claw-code-integration
python3 bootstrap.py
```

## What Was Integrated

| Feature | OpenClaw Before | With Claw-Code |
|---------|-----------------|----------------|
| **Tool Permissions** | None | 3-tier: read-only → workspace-write → danger-full-access |
| **Cost Tracking** | None | Per-agent token usage logging |
| **Command Registry** | Custom | 207 Claude Code mirrored commands |
| **Tool System** | Basic | 184 permission-aware tools |

## Agents Configured

| Agent | Role | Default Permissions |
|-------|------|---------------------|
| **Lisa** | Authority Layer | `read-only` (safest) |
| **Nyx** | Intelligence Layer | `workspace-write` |
| **Kael** | Execution Layer | `workspace-write` |

## Usage

### In OpenClaw Skills

```python
# Import integration
from claw_integration import track_execution, check_tool_permission, elevate_permissions
from openclaw_bridge import check_before_tool, get_integration_status

# Check permission before tool use
result = check_before_tool("lisa", "Bash", {"command": "rm -rf /"})
if not result["allowed"]:
    print(f"Blocked: {result['reason']}")

# Track execution with cost
track_execution("nyx", "Research opportunity", estimated_tokens=1500)

# Elevate permissions when needed
elevate_permissions("kael", "Need to deploy production service")
```

### Command Line

```bash
# Check integration status
python3 openclaw_bridge.py status

# Check tool permission
python3 openclaw_bridge.py check --agent lisa --tool Read
python3 openclaw_bridge.py check --agent lisa --tool Bash  # Blocked

# Get cost summary
python3 openclaw_bridge.py costs

# Get permissions report
python3 openclaw_bridge.py permissions
```

## Permission Levels

1. **read-only**: Safe tools only (Read, Grep, Glob, WebSearch)
2. **workspace-write**: Can Edit, Write, Bash (non-destructive)
3. **danger-full-access**: No restrictions (destructive operations)

## Files

| File | Purpose |
|------|---------|
| `claw_integration.py` | Core integration module |
| `openclaw_bridge.py` | Bridge between OpenClaw and claw-code |
| `bootstrap.py` | Initialization script |
| `skill.json` | Skill metadata |

## Testing

```bash
# Test integration
python3 claw_integration.py

# Test bridge
python3 openclaw_bridge.py status

# Full bootstrap
python3 bootstrap.py
```

## Status

✅ **Integration Complete**
- Python modules: 67 loaded
- Commands: 207 available
- Tools: 184 permission-aware
- Agents: Lisa/Nyx/Kael configured
