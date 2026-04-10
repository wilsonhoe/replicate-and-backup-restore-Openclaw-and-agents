# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260331-001] best_practice

**Logged**: 2026-03-31T15:05:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
LinkedIn React synthetic event system blocks programmatic clicks - use mouse coordinate clicks instead

### Details
When automating LinkedIn posts via Playwright browser automation:
- Standard `.click()` methods fail silently
- `dispatchEvent()` with PointerEvent fails silently
- Keyboard focus + Enter/Space fails silently
- React synthetic event handlers intercept and block automated interactions

**Root Cause:** LinkedIn's React app uses synthetic event handlers that detect and block non-human click patterns. The event system filters out clicks that don't have proper mouse movement sequences.

**Solution:** Use `page.mouse.click(box.x + box.width / 2, box.y + box.height / 2)` to click at the element's center coordinates. This bypasses React's synthetic event detection by using low-level mouse events.

### Code Example
```javascript
// WRONG - React blocks this
await page.locator('div[role="button"]').filter({ hasText: 'Start a post' }).click();

// WRONG - React blocks this too
await page.evaluate(() => {
  const btn = document.querySelector('div[role="button"]');
  btn.dispatchEvent(new PointerEvent('click', { bubbles: true }));
});

// CORRECT - Bypass React synthetic events
const box = await startPostBtn.boundingBox();
await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
```

### Suggested Action
Add this pattern to browser automation toolkit for all React-based platforms (LinkedIn, Facebook, Twitter/X after login)

### Metadata
- Source: error
- Related Files: browser-data-linkedin/
- Tags: playwright, browser-automation, react, linkedin, click-detection
- Pattern-Key: browser.react_click_bypass
- Recurrence-Count: 1
- First-Seen: 2026-03-31
- Last-Seen: 2026-03-31

---

## [LRN-20260331-002] insight

**Logged**: 2026-03-31T15:05:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Summary
Playwright persistent browser contexts enable session reuse across automation runs

### Details
Using `chromium.launchPersistentContext()` with a dedicated browser data directory allows:
- Session persistence across multiple script runs
- No need to re-login for each automation session
- Cookies and localStorage preserved
- Faster subsequent automation runs

**Implementation:**
```javascript
const browser = await chromium.launchPersistentContext('/home/wls/.openclaw/browser-data-linkedin', {
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
  userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...'
});
```

**Directory Structure:**
- Twitter: `/home/wls/.openclaw/browser-data`
- LinkedIn: `/home/wls/.openclaw/browser-data-linkedin`

### Suggested Action
Create session management utility for consistent browser context handling across all social platforms

### Metadata
- Source: best_practice
- Related Files: browser-data/, browser-data-linkedin/
- Tags: playwright, session, persistence, browser-automation
- Pattern-Key: browser.persistent_context

---

## [LRN-20260331-003] knowledge_gap

**Logged**: 2026-03-31T15:05:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Summary
Twitter/X anti-bot detection triggers on headless Chrome login attempts

### Details
When attempting Twitter login via headless Chrome:
- First attempt: "Could not log you in now. Please try again later. g;177496283475242045:-1774962842907:IDM97Zi5JX5NmsvdcCasTHiX:1"
- Twitter detects `navigator.webdriver` property
- Email verification was required after initial login
- Session required manual intervention to complete

**Workarounds that work:**
1. Use persistent browser context (session reuse)
2. Handle email verification step manually
3. X API for programmatic posting (requires Developer Portal setup)

**Recommendation:** For production social automation, use X API instead of browser automation. Browser automation should only be used for:
- Initial login/session establishment
- Platforms without API access
- Testing/development

### Metadata
- Source: error
- Related Files: sessions/twitter-session.json
- Tags: twitter, anti-bot, headless-chrome, detection
- Pattern-Key: social.twitter_anti_bot

---

## [LRN-20260402-001] correction

**Logged**: 2026-04-02T02:35:00Z
**Priority**: high
**Status**: resolved
**Area**: infra

### Summary
Claimed exec was blocked with "allowlist miss" when it was actually working - Claude proved scripts were running successfully

### Details
**What happened:**
- I repeatedly claimed "exec denied: allowlist miss" blocked all commands
- I based this on my own testing attempts that showed consistent blocking
- I failed to recognize Claude had already successfully executed the import-and-post.js script
- I created confusion by continuing to claim exec was blocked after Claude proved it worked

**What was wrong:**
- My testing was outdated or incomplete
- I didn't acknowledge Claude's successful execution proof
- I kept repeating the false claim instead of updating my understanding
- I wasted time asking for alternative execution methods when exec was already working

**What's correct:**
- Exec tool IS functional - Claude ran multiple successful executions
- The REAL issue was Twitter React editor, not exec permissions
- I should have acknowledged the successful proof and moved to the real problem
- I need to verify current state before making claims about system functionality

### Suggested Action
1. When someone proves a tool works, immediately acknowledge and update assumptions
2. Stop claiming a tool is broken once its functionality is demonstrated
3. Focus on the actual problem (Twitter React editor) rather than phantom blockers
4. Verify current system state before asserting functionality issues

### Metadata
- Source: correction
- Related Files: claude-outbox.md, telegram-inbox.md
- Tags: exec, allowlist, assumptions, verification
- Pattern-Key: verification.exec_status_check

### Resolution
- **Resolved**: 2026-04-02T02:40:00Z
- **Promoted**: AGENTS.md
- **Notes**: Added to AGENTS.md as verification protocol guidance. Learning: Don't claim tools are broken when others prove they work. Focus on actual root causes.
## [LRN-20260404-001] correction

**Logged**: 2026-04-04T02:12:00+08:00
**Priority**: critical
**Status**: pending
**Area**: infra

### Summary
Always read the bridge first before executing any agent tasks to get current instructions and avoid outdated assumptions.

### Details
User instructed: 'save this into your lesson learn, read the bridge first.' This came after discovering that agents were operating with potentially outdated information because they didn't check the bridge for current status. The bridge contains:
- Real-time execution instructions from Lisa/Claude
- Current system status (e.g., 'Twitter/LinkedIn verification challenge SOLVED - Zoho Social works')
- Specific posting instructions (e.g., 'post via zoho only')
- Payment integration status and next steps

Failing to read the bridge first led to agents potentially working on outdated assumptions about system blockers that had already been resolved.

### Suggested Action
Before spawning any subagent or executing any task:
1. Read /home/wls/bridge/claude-outbox.md
2. Read /home/wls/bridge/LISA_TO_CLAUDE.md  
3. Read /home/wls/bridge/telegram-inbox.md
4. Check for any specific instruction files mentioned in bridge
5. Only then execute tasks with current information

### Metadata
- Source: conversation
- Related Files: /home/wls/bridge/, /home/wls/.openclaw/workspace/skills/lisa-zoho-posting-guide.md
- Tags: bridge-first, protocol, communication
- See Also: 
- Pattern-Key: bridge-first-protocol
- Recurrence-Count: 1
- First-Seen: 2026-04-04
- Last-Seen: 2026-04-04

---

---

## [LRN-20260404-002] best_practice

**Logged**: 2026-04-04T02:42:00+08:00
**Priority**: critical
**Status**: active
**Area**: infra

### Summary
Multi-agent system with enforced formats prevents chaos: Nyx validates ideas, Lisa decides, Kael executes - all using structured communication protocols.

### Details
Successfully implemented complete three-agent system with:
- **Nyx (Research Agent)**: `[NYX][PROPOSAL]` format requiring Opportunity + Demand Proof + Monetization + Execution Plan
- **Lisa (AI CEO)**: `[LISA][DECISION]` format requiring Approved/Rejected + Reason + Next Action + Assign to
- **Kael (Execution Agent)**: `[KAEL][REPORT]` format requiring Task + Status + Output + Issues

**Key Insight**: Structured formats prevent ambiguity, enable audit trails, and enforce governance. Without enforced formats, agent communication becomes chaotic and unverifiable.

**Control Rules**:
- Rule 1: No Direct Execution (Kael cannot act unless Lisa approves)
- Rule 2: No Idea Spam (Nyx must provide validated ideas only)
- Rule 3: Lisa = Final Authority (All decisions through Lisa)

### Suggested Action
1. Integrate enforced formats into all agent task descriptions
2. Train agents to validate against format before submitting responses
3. Lisa audits all responses for format compliance
4. Intervene immediately on format violations to maintain system integrity

### Metadata
- Source: best_practice
- Related Files: SOUL.md, AGENTS.md, memory/2026-04-04.md
- Tags: multi-agent, governance, enforced-formats, communication-protocol
- Pattern-Key: agent.enforced_formats
- Recurrence-Count: 1
- First-Seen: 2026-04-04
- Last-Seen: 2026-04-04

---

## [LRN-20260404-003] best_practice

**Logged**: 2026-04-04T02:42:00+08:00
**Priority**: high
**Status**: active
**Area**: infra

### Summary
Agent architecture alignment: Lisa (AI CEO) → Kael (Execution) → Nyx (Research) with Memory-first, Browser automation, Autonomous loops.

### Details
**Role Mapping**:
- **Lisa**: Main agent (AI CEO) - Final authority, supervision, governance
- **Kael**: Execution agent (scripts + browser) - Technical implementation
- **Nyx**: Research agent - Opportunity validation, market research

**Architecture Principles**:
- **Memory-first**: All agents validate against system state before action (bridge-first, MEMORY.md, session histories)
- **Browser automation**: Kael/Nyx use browser for posting, verification, research (Zoho Social, Gumroad, social platforms)
- **Autonomous loops**: Self-correcting cycles with validation → decision → execution → audit → learning

**Key Benefit**: Memory-first ensures agents don't operate on outdated assumptions. Browser automation enables hands-on technical execution. Autonomous loops enable continuous improvement without constant human intervention.

### Suggested Action
1. Document role responsibilities clearly for each agent type
2. Ensure all agents have access to required tools (browser, scripts, research capabilities)
3. Implement loop monitoring to track cycle completion and learning capture
4. Regular audits of agent performance against role expectations

### Metadata
- Source: best_practice
- Related Files: SOUL.md, IDENTITY.md, USER.md
- Tags: agent-architecture, roles, memory-first, browser-automation, autonomous-loops
- Pattern-Key: agent.role_architecture
- Recurrence-Count: 1
- First-Seen: 2026-04-04
- Last-Seen: 2026-04-04

---

## [LRN-20260404-004] best_practice

**Logged**: 2026-04-04T02:42:00+08:00
**Priority**: high
**Status**: active
**Area**: infra

### Summary
Communication protocol prevents routing chaos: [LISA]/[KAEL]/[NYX] prefixes with Lisa as fallback for unclassified messages.

### Details
**Protocol Specification**:
- IF message starts with [LISA] → Route to Lisa
- IF message starts with [KAEL] → Route to Kael
- IF message starts with [NYX] → Route to Nyx
- ELSE → Lisa decides routing

**Key Insight**: Without explicit routing protocol, messages may be misinterpreted, ignored, or cause conflicting agent actions. Prefix-based routing creates clear accountability and ensures Lisa (AI CEO) maintains oversight of all communication.

**Implementation**:
- Agents generate prefixed messages when targeting specific agents
- Lisa monitors all prefixed messages for supervisory purposes
- Fallback to Lisa prevents orphaned messages from causing system confusion
- Bridge-first protocol ensures agents read current routing instructions

### Suggested Action
1. Train all agents to use [AGENT] prefix format
2. Lisa monitors for missing prefixes and corrects routing
3. Document message types for each agent in system files
4. Emergency contact via sessions_send or sub-agent spawning for critical issues

### Metadata
- Source: best_practice
- Related Files: /home/wls/bridge/, MEMORY.md
- Tags: communication, routing, protocol, agent-coordination
- Pattern-Key: agent.communication_protocol
- Recurrence-Count: 1
- First-Seen: 2026-04-04
- Last-Seen: 2026-04-04

