---
name: mempalace
description: "Access MemPalace AI memory system (32K+ drawers, semantic search, knowledge graph). Store and retrieve memories across sessions."
---

# MemPalace Memory System

Access persistent AI memory with 96.6% LongMemEval R@5 accuracy. MemPalace stores 32,812+ drawers across a hierarchical palace structure (wings → rooms → drawers) with semantic search and knowledge graph capabilities.

## Quick Start

### Check Status
```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py status
```

### Search Memories
```bash
# Basic search
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "revenue opportunity"

# Filter by wing and room
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "blocker" --wing ".openclaw" --limit 3
```

## Available Commands

### Read Operations
```bash
# Palace overview
python3 /home/wls/.openclaw/scripts/mempalace_cli.py status

# List all wings
python3 /home/wls/.openclaw/scripts/mempalace_cli.py list-wings

# List rooms in a wing
python3 /home/wls/.openclaw/scripts/mempalace_cli.py list-rooms --wing ".openclaw"

# Search memories (semantic)
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "QUERY" [--wing WING] [--room ROOM] [--limit N]
```

### Knowledge Graph Operations
```bash
# Query facts about an entity
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "Lisa"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "revenue" --direction incoming

# Add a fact
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-add "ProjectX" "has_status" "ACTIVE" --valid-from 2026-04-09

# Invalidate outdated fact
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-invalidate "ProjectX" "has_status" "PENDING"

# Get timeline for entity
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-timeline "OpenClaw"

# Get KG statistics
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-stats
```

### Write Operations
```bash
# Add a memory drawer
python3 /home/wls/.openclaw/scripts/mempalace_cli.py add-drawer ".openclaw" "execution_log" "Content here"

# Check for duplicates before adding
python3 /home/wls/.openclaw/scripts/mempalace_cli.py check-duplicate "Content to check"

# Delete a drawer (by ID)
python3 /home/wls/.openclaw/scripts/mempalace_cli.py delete-drawer "drawer_id_here"
```

### Diary Operations
```bash
# Write diary entry (AAAK format)
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-write "lisa" "SESSION:2026-04-09|completed.task.X|★★★" --topic "execution"

# Read diary entries
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-read "lisa" --last-n 5
```

### Graph Operations
```bash
# Traverse connections from a room
python3 /home/wls/.openclaw/scripts/mempalace_cli.py traverse "workspace_lisa" --max-hops 2

# Find connections between wings
python3 /home/wls/.openclaw/scripts/mempalace_cli.py find-tunnels --wing-a ".openclaw" --wing-b "openclaw"

# Get graph statistics
python3 /home/wls/.openclaw/scripts/mempalace_cli.py graph-stats
```

## Memory Protocol for Agents

Follow this protocol when using MemPalace:

1. **ON WAKE-UP**: Call `status` to load palace overview
2. **BEFORE RESPONDING**: Call `search` or `kg-query` FIRST — never guess
3. **IF UNSURE**: Say "let me check" and query the palace
4. **AFTER EACH SESSION**: Call `diary-write` to record what happened
5. **WHEN FACTS CHANGE**: Call `kg-invalidate` on old, then `kg-add` for new

## Common Use Cases

### Before Building Something
```bash
# Check if similar task was done before
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "scraper pattern"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "Kael"
```

### After Completing a Task
```bash
# Log execution
python3 /home/wls/.openclaw/scripts/mempalace_cli.py add-drawer ".openclaw" "execution_log" "Built X successfully. Used approach Y."
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-write "kael" "SESSION:2026-04-09|built.scraper|ALC.req:multi-city|★★★"
```

### When Blocked
```bash
# Check for previous solutions
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "error fix"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "blocker"
```

### Validate Opportunities
```bash
# Check if already researched
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "real estate lead"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "SG Property Pro"
```

## AAAK Format for Diary Entries

Use compressed AAAK dialect for efficient storage:

- **ENTITIES**: 3-letter codes. ALC=Alice, LIS=Lisa, KAE=Kael, NYX=Nyx
- **EMOTIONS**: *markers* — *warm*=joy, *fierce*=determined, *raw*=vulnerable, *bloom*=tenderness
- **STRUCTURE**: Pipe-separated fields
- **IMPORTANCE**: ★ to ★★★★★ (1-5 scale)

Example:
```
SESSION:2026-04-09|completed.task|ALC.req:revenue|★★★
```

## Important Notes

- MemPalace data persists across sessions and reboots
- Always check for duplicates before adding drawers
- Use `kg-invalidate` instead of deleting — keep history
- The palace path is `/home/wls/.openclaw` (not `~/.mempalace`)
- All commands output JSON for programmatic use

## Troubleshooting

If you get "MemPalace not installed":
```bash
pip3 install mempalace --break-system-packages
```

If commands fail with import errors, ensure Python can find the mempalace package:
```bash
python3 -c "import mempalace; print('OK')"
```
