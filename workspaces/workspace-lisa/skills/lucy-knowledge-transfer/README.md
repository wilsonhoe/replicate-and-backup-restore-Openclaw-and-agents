# Lucy Knowledge Transfer

A reusable skill for replicating OpenClaw agent infrastructure to new agents.

## Quick Usage

**Build a replication package:**
```bash
python3 ~/.openclaw/workspace-lisa/skills/lucy-knowledge-transfer/scripts/build-package.py --target lucy --output ~/lucy-package.zip
```

**Interactive mode:**
```bash
python3 ~/.openclaw/workspace-lisa/skills/lucy-knowledge-transfer/scripts/build-package.py --interactive
```

## What It Does

1. **Adapts scripts** — Converts Linux paths to macOS paths automatically
2. **Copies templates** — SOUL.md, IDENTITY.md, USER.md, etc. with agent name substitutions
3. **Exports crons** — All cron job definitions as JSON files
4. **Copies learnings** — ERRORS.md, LEARNINGS.md, FEATURE_REQUESTS.md
5. **Creates install guide** — Step-by-step setup instructions
6. **Packages everything** — Single zip file ready for transfer

## Output Location

Default: `~/lucy-replication-package.zip` (or specify with `--output`)

## Related Files

- `SKILL.md` — Full documentation
- `manifest.json` — Skill metadata
- `scripts/build-package.py` — Package builder script