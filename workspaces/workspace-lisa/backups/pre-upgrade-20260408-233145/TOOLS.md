# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### OpenClaw System

**Browser Automation:**
- Chrome port: 18800
- Launch script: `scripts/chrome-launcher.sh`
- Status: Working (verified April 8, 2026)
- Log: `/tmp/chrome-cdp.log`

**Agent System:**
- Lisa (CEO): Authority layer
- Nyx (Research): Intelligence
- Kael (Execution): Implementation

**Key Channels:**
- #command-center: Decisions
- #research: Nyx output
- #execution: Kael output
- #logs: Reports

**Monitoring:**
- Check Discord channels every 15 min
- Check Bridge file every 15 min
- Daily system health check

---

Add whatever helps you do your job. This is your cheat sheet.
