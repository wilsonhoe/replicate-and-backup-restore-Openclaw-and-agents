# Zoho Social OAuth Setup Guide (FIXED SCOPES)

## Step 1: Generate Authorization URL

Try this URL first:

```
https://accounts.zoho.com/oauth/v2/auth?scope=Social.posts.ALL,Social.messages.ALL&client_id=1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS&response_type=code&access_type=offline&redirect_uri=http://localhost:8080/callback
```

If that fails, try these alternative scope formats:

### Option 2: Simpler scope
```
https://accounts.zoho.com/oauth/v2/auth?scope=Social.ALL&client_id=1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS&response_type=code&access_type=offline&redirect_uri=http://localhost:8080/callback
```

### Option 3: Basic scope only
```
https://accounts.zoho.com/oauth/v2/auth?scope=Social&client_id=1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS&response_type=code&access_type=offline&redirect_uri=http://localhost:8080/callback
```

### Option 4: ZohoSocial prefix (original)
```
https://accounts.zoho.com/oauth/v2/auth?scope=ZohoSocial.posts.ALL,ZohoSocial.messages.ALL&client_id=1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS&response_type=code&access_type=offline&redirect_uri=http://localhost:8080/callback
```

### Option 5: Read/Write separate
```
https://accounts.zoho.com/oauth/v2/auth?scope=Social.posts.READ,Social.posts.CREATE&client_id=1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS&response_type=code&access_type=offline&redirect_uri=http://localhost:8080/callback
```

## Step 2: Login & Authorize

1. Login with **lisamolbot@gmail.com**
2. Enter password: **mv9p@T8iRWWQwBw**
3. Click **"Accept"** to authorize the app

## Step 3: Get Authorization Code

After authorizing, you'll see a page that says:
- "This site can't be reached" or similar error (that's OK!)
- Look at the URL in your browser address bar
- Find the `code=` parameter
- Copy the code (looks like: `1000.abc123...xyz`)

## Step 4: Exchange Code for Tokens

Run this curl command (replace CODE with your actual code):

```bash
curl -X POST https://accounts.zoho.com/oauth/v2/token \
  -d "grant_type=authorization_code" \
  -d "client_id=1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS" \
  -d "client_secret=1ce34ab8330b4c8a864695ada08aa001303cf81bfb" \
  -d "redirect_uri=http://localhost:8080/callback" \
  -d "code=YOUR_CODE_HERE"
```

## Step 5: Save the Tokens

You'll get JSON response like:
```json
{
  "access_token": "1000.xxx...",
  "refresh_token": "1000.yyy...",
  "expires_in": 3600
}
```

**IMPORTANT:**
- `access_token` - valid for 1 hour
- `refresh_token` - valid forever (used to get new access tokens)

## Step 6: Update TOOLS.md

Add to `/home/wls/.openclaw/workspace-kael/TOOLS.md`:

```markdown
### Zoho Social OAuth Tokens
| Token Type | Value |
|------------|-------|
| Refresh Token | 1000.your_refresh_token_here |
| Access Token | 1000.your_access_token_here |
| Expires At | 2026-04-08 10:00:00 |
```

---

**Try the URLs above in order. Tell me which one works!**
