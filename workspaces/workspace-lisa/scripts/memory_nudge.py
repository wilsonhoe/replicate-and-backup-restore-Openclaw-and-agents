#!/usr/bin/env python3
"""
Memory Nudge System — Inspired by Hermes Agent's closed learning loop.
Checks for undocumented knowledge before context is lost during compression.
Runs as part of heartbeat or can be invoked manually.

Output: List of nudge items that need to be persisted to memory/skills.
"""

import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/wls/.openclaw/workspace-lisa"))
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = WORKSPACE / ".learnings"
SKILLS_DIR = WORKSPACE / "skills"
STATE_FILE = MEMORY_DIR / "nudge_state.json"

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_nudge": None, "nudged_items": [], "flushed_sessions": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))

def check_learnings_gap(state):
    """Check if .learnings/ has entries that haven't been promoted to memory/skills."""
    nudges = []
    if not LEARNINGS_DIR.exists():
        return nudges

    for f in LEARNINGS_DIR.glob("*.md"):
        content = f.read_text().strip()
        if not content:
            continue
        # Check if this learning has been referenced in recent memory files
        learning_name = f.stem
        referenced = False
        for mem_file in MEMORY_DIR.glob("*.md"):
            if learning_name.lower() in mem_file.read_text().lower():
                referenced = True
                break
        if not referenced and learning_name not in state.get("nudged_items", []):
            nudges.append({
                "type": "unpromoted_learning",
                "source": str(f),
                "message": f"Learning '{learning_name}' exists but hasn't been promoted to memory or skills"
            })
    return nudges

def check_skill_quality(state):
    """Check skills for missing quality metadata."""
    nudges = []
    if not SKILLS_DIR.exists():
        return nudges

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        manifest = skill_dir / "manifest.json"
        if skill_md.exists() and not manifest.exists():
            nudges.append({
                "type": "missing_skill_metadata",
                "source": str(skill_dir),
                "message": f"Skill '{skill_dir.name}' has no manifest.json — quality tracking not possible"
            })
    return nudges

def check_memory_freshness(state):
    """Check if today's memory file exists and has meaningful content."""
    nudges = []
    today = datetime.now().strftime("%Y-%m-%d")
    today_file = MEMORY_DIR / f"{today}.md"

    if not today_file.exists():
        nudges.append({
            "type": "missing_daily_memory",
            "source": str(today_file),
            "message": f"No memory file for today ({today}) — session context may be lost"
        })
    elif today_file.exists():
        content = today_file.read_text().strip()
        if len(content) < 50:
            nudges.append({
                "type": "thin_daily_memory",
                "source": str(today_file),
                "message": f"Today's memory file is very thin ({len(content)} chars) — likely missing important context"
            })
    return nudges

def check_recent_activity(state):
    """Check for recent learnings/errors that need documentation."""
    nudges = []
    errors_file = LEARNINGS_DIR / "ERRORS.md"
    if errors_file.exists():
        content = errors_file.read_text().strip()
        if content and len(content) > 100:
            # Check if errors have been reviewed recently
            last_nudge = state.get("last_nudge")
            if not last_nudge:
                nudges.append({
                    "type": "unreviewed_errors",
                    "source": str(errors_file),
                    "message": "ERRORS.md has content that hasn't been reviewed for pattern extraction"
                })
    return nudges

def run_nudge_check():
    """Run all nudge checks and return items needing attention."""
    state = load_state()
    all_nudges = []

    all_nudges.extend(check_learnings_gap(state))
    all_nudges.extend(check_skill_quality(state))
    all_nudges.extend(check_memory_freshness(state))
    all_nudges.extend(check_recent_activity(state))

    # Update state
    state["last_nudge"] = datetime.now().isoformat()
    for n in all_nudges:
        if n["source"] not in state.get("nudged_items", []):
            state.setdefault("nudged_items", []).append(n["source"])
    save_state(state)

    return all_nudges

if __name__ == "__main__":
    nudges = run_nudge_check()
    if nudges:
        print(f"🧠 MEMORY NUDGES ({len(nudges)} items need attention):")
        for i, n in enumerate(nudges, 1):
            print(f"  {i}. [{n['type']}] {n['message']}")
            print(f"     Source: {n['source']}")
    else:
        print("✅ All memory systems healthy — no nudges needed.")