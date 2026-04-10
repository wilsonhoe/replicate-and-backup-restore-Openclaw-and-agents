# Learnings Log

## 2026-04-10: Community Intel & Browser Status

### Learning: OpenClaw v2026.4.9 Released (Apr 9)
- **Category:** knowledge_gap
- **Detail:** Major release with security fixes (browser SSRF bypass #63226, node exec injection #62659, dotenv leak #62660/#62663) and new Memory/Dreaming system with grounded REM backfill. Should update from current version.
- **Action:** Schedule OpenClaw update to 2026.4.9 for security patches.

### Learning: Browser Automation Timeout Issues Are Common
- **Category:** best_practice
- **Detail:** Multiple open GitHub issues (#43012, #43654, #38844) about browser tool timeouts on fill/click/upload operations. Our browser CDP on port 18800 is working, but these are known issues to watch for.
- **Action:** If browser automation hits timeouts, check these issues for workarounds.

### Learning: Discord Community Access Requires Login
- **Category:** best_practice
- **Detail:** Cannot access OpenClaw Discord channels via browser automation because Discord requires login. The community repo at github.com/openclaw/community has moderation docs, rules, and onboarding guides but not live discussion content.
- **Action:** For future Discord intel, Wilson needs to be logged in, or use the Discord API/bot. GitHub releases and issues are the best automated source.

### Learning: Ollama Thinking Output Now Supported
- **Category:** best_practice
- **Detail:** v2026.4.9 allows Ollama models (native `api: "ollama"` path) to display thinking output when `/think` is set to non-off. Relevant since we use Ollama/Groq models.
- **Action:** Consider enabling thinking output for better reasoning visibility.

### Learning: sessions_send No Longer Steals Channel Delivery
- **Category:** best_practice
- **Detail:** Fix #58013 ensures `sessions_send` follow-ups preserve established external routes (Telegram, Discord). Previously could steal delivery.
- **Action:** Good news for our multi-channel setup.

## 2026-04-10: Evening Wrap Learnings

### Learning: Distribution Auth Remains #1 Blocker
- **Category:** correction
- **Detail:** Day 2 with live products and $0 revenue. All distribution channels (Reddit, Twitter/X, Indie Hackers) still blocked by authentication. Content is READY but cannot be posted without Wilson logging into the persistent Chrome profile (port 18801). This has been the blocker since April 9.
- **Action:** Escalate to Wilson for a 15-min manual auth session. No amount of automation solves this without human login.

### Learning: Mission #8 Notion Planner AI Is On Track
- **Category:** insight
- **Detail:** Phases 1 & 2 completed rapidly (under 10 min). Phase 3 (Intelligence Layer) started — smart meeting scheduling, daily briefing, voice commands. This is a legitimate product candidate.
- **Action:** Monitor Phase 3 progress; if it completes, this could become a monetizable offering ($50-150 template, $500-2000 DFY setup).

### Learning: MemPalace Skill Created — Structured Knowledge Base
- **Category:** best_practice
- **Detail:** MemPalace CLI tool now available with 32,812 drawers, knowledge graph, diary system, and 19 commands. Initial data loaded: Gumroad product prices, revenue status, mission history.
- **Action:** Use MemPalace for structured queries instead of raw file reads when possible.

### Learning: NotebookLM Integration Complete
- **Category:** best_practice
- **Detail:** NotebookLM CLI available for AI-powered research notebooks. Auth complete. Can create notebooks, add sources, ask questions. Used for Mission #7 market intel.
- **Action:** Leverage for competitor analysis, content research, and product validation.

### Learning: Telegram Cron (job 119b7592) Still Broken
- **Category:** best_practice
- **Detail:** Known since April 8 — sessionTarget/payload mismatch. Needs sessionTarget changed to `main` and payload.kind changed to `systemEvent`.
- **Action:** Fix this cron tomorrow or remove it.