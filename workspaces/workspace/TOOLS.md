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

Add whatever helps you do your job. This is your cheat sheet.

## Social Media Automation Tools

### Twitter/X Browser Automation
**Known Issue:** Twitter's React editor requires specific input simulation
- Standard `textarea.fill()` doesn't trigger React state updates
- Tweet button stays disabled (`aria-disabled="true"`) even after text input
- Solution needed: Proper React synthetic event simulation

**Working Approach (Investigating):**
- `page.keyboard.type()` with proper focus may work
- Character-by-character typing with delays might be required
- React synthetic events need specific triggering

**Debug Files Available:**
- `debug-twitter-home.png` - logged-in state
- `debug-twitter-compose.png` - compose page loaded
- `debug-before-tweet.png` - pre-click state (button disabled)

### LinkedIn Browser Automation
**Known Pattern:** LinkedIn uses React synthetic events that block programmatic clicks
- Standard `element.click()` fails silently
- Solution: Use mouse coordinate clicks: `page.mouse.click(box.x + box.width / 2, box.y + box.height / 2)`

**Session Files:**
- Twitter: `/home/wls/.openclaw/browser-data/cookies.json`
- LinkedIn: `/home/wls/.openclaw/browser-data-linkedin/cookies.json`