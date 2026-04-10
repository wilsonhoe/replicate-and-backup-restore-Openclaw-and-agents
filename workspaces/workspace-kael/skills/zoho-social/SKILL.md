---
name: zoho-social
description: Automate Zoho Social for posting to Twitter/X, LinkedIn, Facebook, Instagram. Includes browser automation patterns and API methods for Zoho Social dashboard.
---

# Zoho Social Automation Skill

Automate social media posting through Zoho Social platform.

## When to Use This Skill

Use when:
- Posting tweets to Twitter/X via Zoho Social
- Scheduling social media content
- Managing multiple social accounts
- Checking engagement/messages
- Researching trending topics

## Credentials (from TOOLS.md)

| Field | Value |
|-------|-------|
| Portal | https://social.zoho.com/social/wilsoninc |
| Login | lisamolbot@gmail.com |
| Password | mv9p@T8iRWWQwBw |
| Client ID | 1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS |
| Client Secret | 1ce34ab8330b4c8a864695ada08aa001303cf81bfb |

## Browser Automation (Primary Method)

### Correct Browser Act Format

The browser tool requires specific action formats:

**Click an element:**
```javascript
// CORRECT format for browser:act
{
  "action": "act",
  "targetId": "PAGE_ID",
  "request": {
    "kind": "click",
    "ref": "e35"  // aria ref from snapshot
  }
}
```

**Type text into input:**
```javascript
{
  "action": "act",
  "targetId": "PAGE_ID",
  "request": {
    "kind": "fill",
    "ref": "e42",
    "text": "text to type"
  }
}
```

**Navigate to URL:**
```javascript
{
  "action": "open",
  "url": "https://social.zoho.com/social/wilsoninc"
}
```

**Get page snapshot:**
```javascript
{
  "action": "snapshot",
  "targetId": "PAGE_ID"
}
```

### Zoho Social Login Flow

1. **Open Zoho Social:**
   ```javascript
   browser({ action: "open", url: "https://social.zoho.com/social/wilsoninc" })
   ```

2. **Click Sign In:**
   ```javascript
   browser({ 
     action: "act", 
     targetId: "PAGE_ID",
     request: { kind: "click", ref: "e35" }  // Sign In link
   })
   ```

3. **Type email:**
   ```javascript
   browser({
     action: "act",
     targetId: "PAGE_ID",
     request: { kind: "fill", ref: "EMAIL_INPUT_REF", text: "lisamolbot@gmail.com" }
   })
   ```

4. **Type password:**
   ```javascript
   browser({
     action: "act",
     targetId: "PAGE_ID",
     request: { kind: "fill", ref: "PASSWORD_INPUT_REF", text: "mv9p@T8iRWWQwBw" }
   })
   ```

5. **Click Sign In button:**
   ```javascript
   browser({
     action: "act",
     targetId: "PAGE_ID",
     request: { kind: "click", ref: "SIGNIN_BUTTON_REF" }
   })
   ```

### Posting a Tweet

1. After login, look for "Compose" or "New Post" button
2. Click it
3. Fill in text area with tweet content
4. Click "Post" or "Schedule"

**Example Compose Flow:**
```javascript
// Click Compose button
browser({
  action: "act",
  targetId: "PAGE_ID",
  request: { kind: "click", ref: "COMPOSE_BUTTON_REF" }
})

// Wait for compose dialog (snapshot)
browser({ action: "snapshot", targetId: "PAGE_ID", delayMs: 2000 })

// Type tweet text
browser({
  action: "act",
  targetId: "PAGE_ID",
  request: { kind: "fill", ref: "TEXTAREA_REF", text: "Your tweet here #AI" }
})

// Click Post
browser({
  action: "act",
  targetId: "PAGE_ID",
  request: { kind: "click", ref: "POST_BUTTON_REF" }
})
```

## API Method (Alternative)

Zoho Social has REST APIs. Use when browser automation fails.

**Base URL:** `https://social.zoho.com/api/v1/`

**Authentication:** OAuth2 with Client ID/Secret

**Get Access Token:**
```bash
curl -X POST https://accounts.zoho.com/oauth/v2/token \
  -d "grant_type=client_credentials" \
  -d "client_id=1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS" \
  -d "client_secret=1ce34ab8330b4c8a864695ada08aa001303cf81bfb" \
  -d "scope=ZohoSocial.posts.ALL"
```

**Create Post:**
```bash
curl -X POST https://social.zoho.com/api/v1/posts \
  -H "Authorization: Zoho-oauthtoken ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Your tweet content here",
    "channels": ["twitter"],
    "scheduledTime": "2026-04-08T09:00:00+08:00"
  }'
```

## Workflow Patterns

### Daily Twitter Automation

```javascript
// Step 1: Login
await openZohoSocial();
await login("lisamolbot@gmail.com", "mv9p@T8iRWWQwBw");

// Step 2: Research trends (use web_search tool)
const trends = await searchTrendingTopics();

// Step 3: Compose tweets
for (const tweet of generateTweets(trends)) {
  await postTweet(tweet);
}

// Step 4: Check engagement
const mentions = await checkMentions();

// Step 5: Report
return summary(tweetsPosted, trends, mentions);
```

### Error Handling

**If browser automation fails:**
1. Try API method with curl
2. If API fails, check if token expired
3. If token expired, re-authenticate
4. Report [BLOCKED] if neither method works

**Common issues:**
- Element refs change between snapshots (always get fresh snapshot)
- Login redirects to 2FA (report if 2FA required)
- Rate limits (wait and retry)
- Session timeout (re-login)

## Tweet Templates

### Template 1: AI Trend Commentary
```
[Trend headline]

This isn't just news—it's a signal.

The companies [action] first will scale faster than those [alternative] first.

Are you building [approach]-first?

#AI #Automation #BusinessGrowth
```

### Template 2: Tool/Feature Release
```
[Feature] is here with [key benefit].

[Faster/Better/Cheaper]

The real story? [Strategic implication]

This changes the math on [topic].

#AI #[RelevantTags]
```

### Template 3: Industry Shift
```
[Number] [actions]. Zero [barrier].

[Company] just launched [feature] that can "[capability]."

The barrier to [outcome] just dropped to zero.

You don't need to be [old requirement] anymore. You need to be [new requirement].

#AI #Automation
```

## Output Format

Always return summary in this format:

```
[SUCCESS] or [BLOCKED] or [FAIL]
Mission: [task name]

Actions Taken:
1. [action] → [result]
2. [action] → [result]

Tweets Posted:
- [tweet summary] ([link if available])

Trends Researched:
1. [trend 1]
2. [trend 2]

Engagement:
- Mentions: [count]
- DMs requiring attention: [list or "none"]

Next: [recommendation]
```

## References

- Zoho Social API Docs: https://www.zoho.com/social/api.html
- Zoho OAuth Guide: https://www.zoho.com/accounts/protocol/oauth-setup.html

## Notes

- Zoho Social supports: Twitter/X, Facebook, LinkedIn, Instagram
- Portal URL: https://social.zoho.com/social/wilsoninc/1663181000000023017/Home.do
- Keep sessions short (re-login if inactive >30 min)
