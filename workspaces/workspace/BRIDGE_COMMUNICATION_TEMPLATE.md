# BRIDGE COMMUNICATION TEMPLATE
## Standardized Format for Effective Communication

Use this template for all bridge communications between system components to ensure clarity, consistency, and efficiency.

## TEMPLATE STRUCTURE

**[TIMESTAMP] [SENDER] → [RECIPIENT]**

**🎯 OBJECTIVE:** [Clear, concise objective statement - what you're trying to accomplish]

**📊 STATUS:** [Current state - include any blockers, progress, or relevant context]

**✅ ACCOMPLISHED:** 
- [Specific completed action]
- [Specific completed action]

**🚧 BLOCKERS/ISSUES:**
- [Specific blocker preventing progress] 
- [Specific issue that needs attention]

**🎯 NEXT ACTIONS:**
1. [Specific, actionable step - begin with verb]
2. [Specific, actionable step - include any prerequisites]

**📎 REFERENCES:**
- File: `/path/to/file.md` - [brief description of what it contains]
- Command: `command to run` - [what it accomplishes]

**⏱️ TIME ESTIMATE:** [X minutes/hours - realistic estimate for completion]

---

## STATUS INDICATORS (Use at beginning of status updates)

- **✅ COMPLETED** - Action successfully finished and verified
- **🚧 IN_PROGRESS** - Work actively underway
- **⏳ PENDING** - Waiting on external factor or dependency
- **🔄 ITERATING** - Multiple attempts being made to solve a problem
- **🚫 BLOCKED** - Cannot proceed without external intervention
- **⭐ RECOMMENDATION** - Suggested course of action based on analysis
- **⚠️ WARNING** - Potential issue that needs attention but not currently blocking
- **ℹ️ INFORMATION** - Informational update, no action required

---

## EXAMPLE USAGE

**[2026-04-02T18:30:00Z] Lisa → Claude & Wilson**

**🎯 OBJECTIVE:** Establish reliable Twitter posting automation for daily content distribution

**📊 STATUS:** Twitter API investigation complete - determined paid API not viable for $0 budget scenario. Existing browser automation scripts available and ready to test.

**✅ ACCOMPLISHED:** 
- Evaluated three Twitter automation approaches (Playwright, bb-browser, Twitter API)
- Confirmed Twitter API requires payment ($0.01 per tweet)
- Verified existing cookie files are present and valid
- Prepared backup plan using browser automation

**🚧 BLOCKERS/ISSUES:**
- None - path forward is clear using existing free resources

**🎯 NEXT ACTIONS:**
1. Execute Twitter posting script: `node import-and-post.js`
2. Verify successful posting by checking for `proof-day2-twitter.png`
3. Report results with screenshot evidence

**📎 REFERENCES:**
- File: `/home/wls/.openclaw/workspace/import-and-post.js` - Main posting script
- File: `/home/wls/.openclaw/chrome-profile/twitter-cookies.json` - Authentication cookies
- Command: `ls -la /home/wls/.openclaw/workspace/proof-*` - Check for proof files

**⏱️ TIME ESTIMATE:** 5 minutes for execution and verification

---
*Template Version: 1.0*
*Last Updated: 2026-04-02*
*Use for all inter-component communications*