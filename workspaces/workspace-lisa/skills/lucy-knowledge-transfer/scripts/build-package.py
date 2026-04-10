#!/usr/bin/env python3
"""
Lucy Knowledge Transfer — Build Replication Package

Creates a portable zip containing all scripts, configs, templates, and cron jobs
needed to replicate Lisa's OpenClaw agent to a new agent (Lucy) on Mac Studio.

Usage:
    python3 build-package.py --target lucy --output ~/lucy-package.zip
    python3 build-package.py --interactive
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/wls/.openclaw/workspace-lisa"))
TEMP_DIR = Path("/tmp/lucy-replication-package")

# Platform adaptation rules
PLATFORM_ADAPTATIONS = {
    "macos": {
        "home_path": "/Users/{user}",
        "chrome_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "brew_prefix": "/opt/homebrew",  # M-series; use /usr/local for Intel
        "python": "python3",
    },
    "linux": {
        "home_path": "/home/{user}",
        "chrome_path": "/usr/bin/google-chrome",
        "brew_prefix": "/home/linuxbrew/.linuxbrew",
        "python": "python3",
    }
}

def adapt_script_for_platform(script_path: Path, target_platform: str, target_user: str) -> str:
    """Read script and adapt paths for target platform."""
    content = script_path.read_text()
    
    # Path replacements
    content = content.replace("/home/wls/.openclaw/workspace-lisa", 
                              f"{PLATFORM_ADAPTATIONS[target_platform]['home_path'].format(user=target_user)}/.openclaw/workspace-{{agent_name}}")
    content = content.replace("/home/wls/", 
                              f"{PLATFORM_ADAPTATIONS[target_platform]['home_path'].format(user=target_user)}/")
    
    # Use environment variable fallback
    content = content.replace(
        'Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/wls/.openclaw/workspace-lisa"))',
        'Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace-{agent_name}"))'
    )
    
    return content

def build_package(target_agent: str, target_platform: str, target_user: str, output_path: str):
    """Build the replication package."""
    
    print(f"📦 Building replication package for {target_agent} on {target_platform}")
    
    # Clean temp directory
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)
    
    # Create directory structure
    (TEMP_DIR / "scripts").mkdir()
    (TEMP_DIR / "templates").mkdir()
    (TEMP_DIR / "cron").mkdir()
    (TEMP_DIR / "learnings").mkdir()
    (TEMP_DIR / "secrets-templates").mkdir()
    (TEMP_DIR / "skills").mkdir()
    
    # Copy and adapt scripts
    scripts_source = WORKSPACE / "scripts"
    if scripts_source.exists():
        for script in scripts_source.glob("*.py"):
            adapted = adapt_script_for_platform(script, target_platform, target_user)
            adapted = adapted.replace("{agent_name}", target_agent)
            (TEMP_DIR / "scripts" / script.name).write_text(adapted)
            print(f"  ✅ Adapted script: {script.name}")
    
    # Copy templates
    templates_source = WORKSPACE
    template_files = ["SOUL.md", "IDENTITY.md", "AGENTS.md", "TOOLS.md", "USER.md"]
    for tf in template_files:
        src = templates_source / tf
        if src.exists():
            content = src.read_text()
            content = content.replace("lisa", target_agent).replace("Lisa", target_agent.capitalize())
            content = content.replace("/home/wls/", f"/{target_platform == 'macos' and 'Users' or 'home'}/{target_user}/")
            (TEMP_DIR / "templates" / tf).write_text(content)
            print(f"  ✅ Adapted template: {tf}")
    
    # Copy user_model.json
    user_model_src = WORKSPACE / "memory" / "user_model.json"
    if user_model_src.exists():
        shutil.copy(user_model_src, TEMP_DIR / "templates" / "user_model.json")
        print("  ✅ Copied: user_model.json")
    
    # Export cron jobs
    try:
        result = subprocess.run(["openclaw", "cron", "list", "--json"], capture_output=True, text=True)
        if result.returncode == 0:
            crons = json.loads(result.stdout)
            for cron in crons:
                cron_name = cron.get("name", cron.get("id", "unknown"))
                cron_file = TEMP_DIR / "cron" / f"{cron_name}.json"
                cron_file.write_text(json.dumps(cron, indent=2))
                print(f"  ✅ Exported cron: {cron_name}")
    except Exception as e:
        print(f"  ⚠️ Could not export crons: {e}")
    
    # Copy learnings
    learnings_src = WORKSPACE / ".learnings"
    if learnings_src.exists():
        for lf in learnings_src.glob("*.md"):
            shutil.copy(lf, TEMP_DIR / "learnings" / lf.name)
            print(f"  ✅ Copied learning: {lf.name}")
    
    # Create secrets templates
    secrets_templates = {
        "telegram-bot-token.example": "YOUR_TELEGRAM_BOT_TOKEN_HERE",
        "discord-bot-token.example": "YOUR_DISCORD_BOT_TOKEN_HERE",
        "notion-api-key.example": "YOUR_NOTION_API_KEY_HERE",
        "github-pat.example": "YOUR_GITHUB_PAT_HERE"
    }
    for name, content in secrets_templates.items():
        (TEMP_DIR / "secrets-templates" / name).write_text(content + "\n")
    
    # Copy skills (optional)
    skills_src = WORKSPACE / "skills"
    if skills_src.exists():
        for skill_dir in skills_src.iterdir():
            if skill_dir.is_dir() and skill_dir.name != "lucy-knowledge-transfer":
                dest = TEMP_DIR / "skills" / skill_dir.name
                shutil.copytree(skill_dir, dest)
                print(f"  ✅ Copied skill: {skill_dir.name}")
    
    # Create INSTALL.md
    install_md = f"""# {target_agent.capitalize()} Replication Package

## Quick Start

1. Install dependencies:
   ```bash
   # macOS
   brew install node@22 python@3.12 git ffmpeg
   
   # Linux
   sudo apt install nodejs python3 git ffmpeg
   ```

2. Install OpenClaw:
   ```bash
   npm install -g openclaw
   openclaw doctor
   ```

3. Create workspace:
   ```bash
   mkdir -p ~/.openclaw/workspace-{target_agent}
   ```

4. Copy files from this package:
   ```bash
   cp -r scripts/* ~/.openclaw/workspace-{target_agent}/scripts/
   cp -r templates/* ~/.openclaw/workspace-{target_agent}/
   ```

5. Configure secrets in `~/.openclaw/secrets/`

6. Update OpenClaw config (add agent to agents.list)

7. Import cron jobs:
   ```bash
   for f in cron/*.json; do openclaw cron add --file "$f"; done
   ```

8. Verify:
   ```bash
   python3 ~/.openclaw/workspace-{target_agent}/scripts/memory_nudge.py
   openclaw cron list
   ```

## Platform: {target_platform}
## Target User: {target_user}
## Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    (TEMP_DIR / "INSTALL.md").write_text(install_md)
    
    # Create README
    readme = f"""# {target_agent.capitalize()} Replication Package

Complete OpenClaw agent replication system created from Lisa.

## Contents

- `scripts/` — Adapted Python scripts (memory_nudge, fts5_search, skill_factory)
- `templates/` — Agent identity files (SOUL.md, IDENTITY.md, etc.)
- `cron/` — Exported cron job definitions
- `learnings/` — Learning/error logs from Lisa
- `secrets-templates/` — Placeholder files for tokens
- `skills/` — Copied skills from Lisa

## Setup Time

~30 minutes for basic setup

## Support

See `INSTALL.md` for step-by-step instructions.
"""
    (TEMP_DIR / "README.md").write_text(readme)
    
    # Create zip
    output_file = Path(output_path).expanduser()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    shutil.make_archive(str(output_file.with_suffix("")), 'zip', TEMP_DIR)
    
    # Get file size
    size_kb = output_file.stat().st_size / 1024
    
    print(f"\n✅ Package created: {output_file}")
    print(f"📊 Size: {size_kb:.1f} KB")
    print(f"📁 Contents: {len(list(TEMP_DIR.rglob('*')))} files")
    
    # Cleanup
    shutil.rmtree(TEMP_DIR)
    
    return str(output_file)

def interactive_mode():
    """Interactive package builder."""
    print("🛠️ Lucy Knowledge Transfer — Interactive Mode\n")
    
    target_agent = input("Target agent name [lucy]: ").strip() or "lucy"
    target_platform = input("Target platform [macos/linux]: ").strip().lower()
    if target_platform not in ["macos", "linux"]:
        target_platform = "macos"
    target_user = input("Target username [wls]: ").strip() or "wls"
    output_path = input("Output path [~/lucy-replication-package.zip]: ").strip()
    if not output_path:
        output_path = f"~/{target_agent}-replication-package.zip"
    
    print("\n--- Confirm ---")
    print(f"Target Agent: {target_agent}")
    print(f"Platform: {target_platform}")
    print(f"Username: {target_user}")
    print(f"Output: {output_path}")
    
    confirm = input("\nProceed? [Y/n]: ").strip().lower()
    if confirm in ["n", "no"]:
        print("Cancelled.")
        return
    
    build_package(target_agent, target_platform, target_user, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build OpenClaw agent replication package")
    parser.add_argument("--target", default="lucy", help="Target agent name")
    parser.add_argument("--platform", default="macos", choices=["macos", "linux"])
    parser.add_argument("--user", default="wls", help="Target username")
    parser.add_argument("--output", default="~/lucy-replication-package.zip")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    else:
        build_package(args.target, args.platform, args.user, args.output)