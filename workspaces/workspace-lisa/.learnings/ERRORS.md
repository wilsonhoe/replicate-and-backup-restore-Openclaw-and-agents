# Errors

Command failures and integration errors.

---

## [2026-04-05] Consolidated from Legacy Files

### Daily Performance Review Telegram Issue
**Category**: integration_error | **Severity**: High | **Status**: Identified, needs resolution
**Error**: Job failing due to Telegram resolution errors (@heartbeat unresolved)
**Root Cause**: Attempting to send reports to unresolved Telegram recipient
**Impact**: Reporting pipeline broken, losing daily optimization insights
**Job ID**: 119b7592-ef26-4e80-a993-35a78923fa03
**Resolution Path**: Change `sessionTarget` from `isolated` to `main`; Change `payload.kind` from `agentTurn` to `systemEvent`

### Memory File Access Pattern Error
**Category**: file_access | **Severity**: Medium | **Status**: Identified, optimization needed
**Error**: Heartbeat agent looking for non-existent date-specific memory files
**Root Cause**: Date-based memory file naming convention not matching actual file availability
**Evidence**: Looking for `2026-03-31.md` when only `2026-03-28-*.md` and `2026-04-02.md` exist
**Resolution Path**: Add file existence check before reading memory files; Fallback to current MEMORY.md or most recent available file

### Config Apply Catastrophic Incident
**Category**: configuration | **Severity**: Critical | **Status**: Recovered, protocol established
**Error**: Using config.apply for partial updates caused system-wide configuration corruption
**Root Cause**: config.apply overwrites entire configuration rather than patching
**Resolution**: System recovered and config.patch protocol established
**Prevention**: Always use config.patch for partial updates, never config.apply

### Evening Wrap Cron Test
**Category**: cron_test | **Severity**: Low | **Status**: Success
**Error**: None - test execution successful
**Date**: 2026-04-07
**Action**: Verified evening wrap protocol functionality

---

## [2026-04-08] Discord Agent Coordination Failure — CRITICAL

**Category**: integration_error | **Severity**: Critical | **Status**: Mitigated (decentralized execution)
**Error**: Bot-to-bot mentions (@Kael, @Nyx) blocked by Discord API
**Root Cause**: Discord prevents bots from mentioning other bots — assignments never received
**Impact**: 3 missions stalled 36+ hours, zero execution output from Kael
**Missions Affected**: #3 Digital Products, #4 High-Ticket Affiliate, #5 Faceless YouTube
**Resolution**: Shifted to decentralized execution (Lisa + Claude direct via bridge)
**Prevention**: Design agent coordination without @mentions; use bridge for direct execution
**Lesson**: Agent coordination layer failed; bridge communication reliable

---

### Social Media Authentication Blockade - RESOLVED
**Category**: authentication | **Severity**: Critical | **Status**: **RESOLVED via Zoho Social**
**Error**: Social media posting blocked due to Twitter verification challenges and expired sessions
**Root Cause**: Direct Twitter posting triggers verification; LinkedIn has React synthetic event issues
**Solution Applied**: Zoho Social browser automation working
**Resolution Date**: 2026-04-02
**Working Method**: `post-day2-click.js` - Playwright browser automation via Zoho Social
**Status**: Days 1-3 posted successfully; Days 4-7 ready to post
**Next Action**: Use Zoho Social for all remaining posts

---

## [2026-04-09] Evening Wrap — New Issues

### Telegram Daily Review Cron — Still Broken
**Category**: cron | **Severity**: Medium | **Status**: Open
**Error**: sessionTarget/payload mismatch causing job failure
**Job ID**: 119b7592-ef26-4e80-a993-35a78923fa03
**Impact**: Daily review not delivered to Telegram
**Resolution Path**: Fix sessionTarget (change to `main`) and payload.kind (change to `systemEvent`)

### Gumroad Revenue — $0 Despite Live Products
**Category**: business | **Severity**: High | **Status**: Open
**Error**: 3 products live but zero traffic or sales
**Root Cause**: No marketing/distribution strategy in place
**Impact**: Revenue pipeline non-functional despite product readiness
**Resolution Path**: Implement distribution strategy (social media, SEO, communities)

### Bridge Monitor — Missing Cron (Fixed)
**Category**: monitoring | **Severity**: Medium | **Status**: Fixed
**Error**: Bridge file not being checked every 15 min, Claude messages missed
**Root Cause**: No cron job for bridge monitoring
**Fix Applied**: Bridge monitor cron added 14:22 SGT
**Verification**: claude-outbox.md now checked every 15 min

## [2026-04-10] Evening Wrap — New Issues

### Distribution Auth Blockade — Day 2 (CRITICAL)
**Category**: authentication | **Severity**: Critical | **Status**: Open
**Error**: 3 Gumroad products live, marketing content ready, but $0 revenue because no platform auth exists
**Root Cause**: Reddit (network block), Twitter/X (auth redirect), Indie Hackers (auth required) — all require Wilson to log into persistent Chrome profile (port 18801)
**Impact**: Revenue pipeline completely stalled at the distribution stage
**Resolution Path**: Wilson 15-min manual auth session on port 18801
**Previous**: Same issue since April 9 — content ready in `marketing/distribution-ready.md`

### Mission #7 — Partially Blocked
**Category**: execution | **Severity**: Medium | **Status**: Partial
**Error**: Phase 1 (NotebookLM intel) complete, Phase 2 (distribution) blocked by auth
**Root Cause**: Same auth issue as above
**Impact**: Marketing content created but not posted
**Resolution Path**: Human auth session needed

### Telegram Daily Review Cron — Still Unfixed (Day 3)
**Category**: cron | **Severity**: Medium | **Status**: Open
**Error**: Job 119b7592 still failing — sessionTarget/payload mismatch
**Impact**: No daily Telegram review delivery
**Resolution Path**: Change sessionTarget to `main`, payload.kind to `systemEvent`

### Mission #8a Meeting Scheduler — Active
**Category**: mission | **Severity**: Low | **Status**: Executing
**Detail**: Kael spawned subagent for Meeting Scheduler, deadline 2026-04-11 23:59
