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
- Status: Working (verified April 10, 2026)
- Chrome version: 146.0.7680.177 (system), HeadlessChrome/145.0.7632.0 (CDP)
- CDP ready: true (ws://localhost:18800/devtools/browser/)
- OpenClaw browser tool: enabled, running
- Log: `/tmp/chrome-cdp.log`
- ⚠️ Note: v2026.4.9 fixes SSRF bypass in browser automation (#63226) — recommend updating

**Agent System:**
- Lisa (CEO): Authority layer
- Nyx (Research): Intelligence
- Kael (Execution): Implementation

**Key Channels:**
- #command-center: Decisions
- #research: Nyx output
- #execution: Kael output
- #logs: Reports

**Persistent Browser Profiles (Social Automation):**
- Profile dir: `~/.openclaw/workspace-lisa/browser-profiles/social-automation/`
- Launch script: `scripts/chrome-social-profile.sh` (port 18801)
- **Status (Apr 10):** Profile created, NOT YET AUTHENTICATED
- **Twitter/X:** ✅ Has auth cookies in Wilson's regular Chrome (Default profile)
- **Reddit:** ❌ No cookies found — needs manual login
- **Indie Hackers:** ❌ No cookies found — needs manual login
- **Important:** OpenClaw's default browser (port 18800) runs Playwright headless Chromium in incognito mode — sessions DON'T persist. For authenticated automation, Wilson must log into each platform via the persistent Chrome profile (port 18801) one time.

**Authentication Steps (one-time, requires Wilson):**
1. Run: `bash ~/.openclaw/workspace-lisa/scripts/chrome-social-profile.sh`
2. In the new Chrome window, manually log into: Reddit, Twitter/X, Indie Hackers
3. Close browser — cookies are saved in the persistent profile
4. Future automation can use this profile via CDP on port 18801

**Monitoring:**
- Check Discord channels every 15 min
- Check Bridge file every 15 min
- Daily system health check

---

Add whatever helps you do your job. This is your cheat sheet.
