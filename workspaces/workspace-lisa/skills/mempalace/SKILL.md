# MemPalace Skill

**Location:** `/home/wls/.openclaw/workspace-lisa/skills/mempalace/`  
**CLI:** `python3 /home/wls/.openclaw/scripts/mempalace_cli.py`  
**Purpose:** Structured, queryable knowledge base with relationships for all agents

---

## Overview

MemPalace provides 32,812+ drawers for structured knowledge storage with knowledge graph queries, relationship mapping, and diary entries. Complements existing memory systems:

- `memory/*.md` = raw daily logs
- `MEMORY.md` = curated long-term memory
- **MemPalace** = structured, queryable knowledge base with relationships

---

## Use Cases for Lisa (AI CEO)

1. **Store validated opportunities** with confidence scores
2. **Track agent relationships** (Lisa ↔ Nyx ↔ Kael interactions)
3. **Diary entries** for revenue milestones and decisions
4. **Knowledge graph** of what works/what doesn't in income generation
5. **Revenue tracking** with timestamps and outcomes
6. **Opportunity validation** history

---

## Commands (19 Total)

### 1. `status`
Show palace status (wings, rooms, drawers, health).

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py status
```

### 2. `search <query> [--limit N] [--wing WING] [--room ROOM]`
Search memories by keyword.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "Gumroad revenue" --limit 10
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "Notion template" --wing revenue
```

### 3. `kg-query <entity> [--as-of DATE] [--direction incoming|outgoing|both]`
Query knowledge graph for entity relationships.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "Finance Dashboard"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "Lisa" --direction outgoing
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "Gumroad" --as-of 2026-04-09
```

### 4. `kg-add <subject> <predicate> <object> [--valid-from DATE]`
Add fact to knowledge graph.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-add "Finance Dashboard" "has_price" "$39"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-add "Lisa" "approved" "Mission #6" --valid-from 2026-04-09
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-add "Gumroad" "generated_revenue" "$0" --valid-from 2026-04-09
```

### 5. `kg-invalidate <subject> <predicate> <object> [--ended DATE]`
Invalidate/remove a fact from knowledge graph.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-invalidate "Mission #3" "status" "active" --ended 2026-04-08
```

### 6. `kg-timeline <entity>`
Get timeline for an entity.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-timeline "Finance Dashboard"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-timeline "Lisa"
```

### 7. `kg-stats`
Get knowledge graph statistics (facts, entities, relationships).

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-stats
```

### 8. `add-drawer <wing> <room> <content> [--source-file PATH]`
Add a memory drawer with content.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py add-drawer revenue opportunities "Finance Dashboard: $39, live on Gumroad, 0 sales"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py add-drawer agents decisions "Lisa approved Mission #6 at 08:30 SGT"
python3 /home/wls/.openclaw/scripts/mempalace_cli.py add-drawer revenue milestones "First sale target: 2026-04-11" --source-file /tmp/notes.md
```

### 9. `delete-drawer <drawer_id>`
Delete a drawer by ID.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py delete-drawer 12345
```

### 10. `list-wings`
List all wings in the palace.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py list-wings
```

### 11. `list-rooms [--wing WING]`
List rooms, optionally filtered by wing.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py list-rooms
python3 /home/wls/.openclaw/scripts/mempalace_cli.py list-rooms --wing revenue
```

### 12. `traverse <start_room> [--max-hops N]`
Traverse palace graph from a starting room.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py traverse "opportunities" --max-hops 3
```

### 13. `find-tunnels [--wing-a WING_A] [--wing-b WING_B]`
Find connections between wings.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py find-tunnels --wing-a revenue --wing-b agents
```

### 14. `graph-stats`
Get graph statistics (nodes, edges, connectivity).

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py graph-stats
```

### 15. `diary-write <agent> <entry> [--topic TOPIC]`
Write diary entry in AAAK format (Action, Assessment, Adjustment, Knowledge).

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-write Lisa "Action: Launched 3 Gumroad products. Assessment: $0 revenue, distribution problem. Adjustment: Marketing sprint tomorrow. Knowledge: Build mode → distribution mode shift required." --topic revenue
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-write Nyx "Action: Researched market opportunities. Assessment: 5 validated leads. Adjustment: Focus on B2B SaaS. Knowledge: r/Notion high-conversion channel." --topic research
```

### 16. `diary-read <agent> [--last-n N]`
Read diary entries for an agent.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-read Lisa --last-n 5
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-read Kael --last-n 10
```

### 17. `check-duplicate <content>`
Check if content already exists in palace.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py check-duplicate "Finance Dashboard: $39, live on Gumroad"
```

### 18. `get-taxonomy`
Get palace taxonomy (wing/room structure).

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py get-taxonomy
```

### 19. `get-aaak-spec`
Get AAAK dialect specification for diary entries.

```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py get-aaak-spec
```

---

## Recommended Wings/Rooms for Lisa

```
revenue/
  ├── opportunities/      - Validated opportunities with confidence scores
  ├── milestones/         - Revenue milestones ($0 → $1K → $10K)
  ├── products/           - Product details, pricing, performance
  └── channels/           - Distribution channel performance

agents/
  ├── decisions/          - Lisa's approved/rejected decisions
  ├── relationships/      - Agent interaction history
  └── performance/        - Agent execution metrics

marketing/
  ├── campaigns/          - Marketing campaign results
  ├── content/            - Content performance (Twitter, Reddit, LinkedIn)
  └── metrics/            - Views, clicks, conversions

research/
  ├── validated/          - Nyx's validated opportunities
  ├── rejected/           - Rejected opportunities with reasons
  └── patterns/           - Market patterns and insights
```

---

## Example Workflows

### Store New Opportunity
```bash
# Add to knowledge graph
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-add "LeadFlow Pro" "status" "scoped" --valid-from 2026-04-09
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-add "LeadFlow Pro" "price_point" "$67"

# Add detailed drawer
python3 /home/wls/.openclaw/scripts/mempalace_cli.py add-drawer revenue opportunities "LeadFlow Pro: SG property scraper + Notion CRM, $67 price, PAUSED until Gumroad traction"
```

### Log Revenue Milestone
```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-add "Gumroad" "first_sale" "2026-04-10" --valid-from 2026-04-10
python3 /home/wls/.openclaw/scripts/mempalace_cli.py diary-write Lisa "Action: First sale achieved. Assessment: Reddit r/Notion drove conversion. Adjustment: Double down on Reddit. Knowledge: Value-first posts convert." --topic milestones
```

### Query Agent Performance
```bash
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-query "Kael" --direction incoming
python3 /home/wls/.openclaw/scripts/mempalace_cli.py kg-timeline "Mission #6"
```

---

## Integration with Existing Memory

- **Daily logs:** Continue using `memory/YYYY-MM-DD.md` for raw session logs
- **Curated memory:** Update `MEMORY.md` for long-term patterns and decisions
- **Structured knowledge:** Use MemPalace for queryable facts, relationships, and metrics
- **Diary entries:** Use MemPalace `diary-write` for AAAK-formatted agent reflections

---

## Notes

- MemPalace has 32,812+ drawers available
- Knowledge graph supports temporal queries (`--as-of`, `--valid-from`, `--ended`)
- AAAK format for diary: Action, Assessment, Adjustment, Knowledge
- All agents (Lisa, Nyx, Kael) can use this skill
