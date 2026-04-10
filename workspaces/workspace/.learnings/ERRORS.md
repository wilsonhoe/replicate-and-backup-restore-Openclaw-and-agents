# Errors

Command failures and integration errors.

---

## [ERR-20260331-001] linkedin_click_failure

**Logged**: 2026-03-31T15:05:00Z
**Priority**: high
**Status**: resolved
**Area**: backend

### Summary
LinkedIn "Start a post" button clicks detected but no dialog opened - React synthetic event blocking

### Error
```
Error: locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator('div[contenteditable="true"], textarea').first()
  - element is visible, enabled, stable
  - <h1> from <div id="artdeco-modal-outlet"> subtree intercepts pointer events
```

### Context
- Attempted: `page.locator('div[role="button"]').filter({ hasText: 'Start a post' }).click()`
- Result: Click registered in console logs but no dialog opened
- Multiple approaches failed: `.click()`, `dispatchEvent()`, keyboard focus + Enter
- Root cause: React synthetic event system blocks programmatic clicks

### Resolution
- **Resolved**: 2026-03-31T15:00:00Z
- **Solution**: Use `page.mouse.click(box.x + box.width / 2, box.y + box.height / 2)` on element's bounding box center
- **Notes**: This bypasses React's synthetic event detection by using low-level mouse events

### Metadata
- Reproducible: yes (on LinkedIn feed page)
- Related Files: browser-data-linkedin/
- See Also: LRN-20260331-001

---

## [ERR-20260331-002] twitter_login_blocked

**Logged**: 2026-03-31T15:05:00Z
**Priority**: high
**Status**: resolved
**Area**: backend

### Summary
Twitter login blocked with anti-bot detection error code

### Error
```
Could not log you in now. Please try again later. 
g;177496283475242045:-1774962842907:IDM97Zi5JX5NmsvdcCasTHiX:1
```

### Context
- Attempted: Headless Chrome login via Playwright
- Twitter detected `navigator.webdriver` property
- First login attempt blocked

### Resolution
- **Resolved**: 2026-03-31T14:30:00Z
- **Solution**: Use persistent browser context with session reuse; handle email verification step; for production, use X API instead
- **Notes**: Session saved to `/home/wls/.openclaw/browser-data` for reuse

### Metadata
- Reproducible: yes (on fresh browser sessions)
- Related Files: browser-data/
- See Also: LRN-20260331-003

---

## [ERR-20260402-001] twitter_react_editor_disabled

**Logged**: 2026-04-02T02:37:00Z
**Priority**: high
**Status**: pending
**Area**: frontend

### Summary
Twitter compose page loads successfully but tweet button remains disabled (aria-disabled="true") even after text input

### Error
```
page.click: Timeout 30000ms exceeded
waiting for locator('[data-testid="tweetButton"]')
element is not enabled (aria-disabled="true")
```

### Context
- Command: `node import-and-post.js` (Playwright automation)
- Input: Attempted to post Day 2 content to Twitter
- Environment: Headless Chrome with persistent session
- Script successfully: imports cookies, navigates to compose page, fills textarea
- Failure point: Tweet button click - button stays disabled

### Root Cause Analysis
Twitter uses React synthetic events for text input. Standard Playwright methods:
- `textarea.fill()` - doesn't trigger React state updates
- `page.type()` - may not work either
- `page.keyboard.type()` - needs investigation

The React editor requires specific input simulation to update its internal state and enable the tweet button.

### Suggested Fix
Investigate and implement proper React input simulation:
1. Try `page.keyboard.type()` with proper focus
2. Try simulating key events with `page.keyboard.press()`
3. Try using `page.dispatchEvent()` for synthetic events
4. Try `element.focus()` followed by keyboard input
5. Check if text needs to be typed character-by-character with delays

### Metadata
- Reproducible: yes (consistent across test runs)
- Related Files: import-and-post.js, debug-before-tweet.png
- See Also: LRN-20260402-001 (exec confusion)

### Resolution
- **Resolved**: 2026-04-02T02:42:00Z
- **Promoted**: TOOLS.md
- **Notes**: Added React editor technical details to TOOLS.md for future reference. Pattern: React synthetic events require specific input simulation.