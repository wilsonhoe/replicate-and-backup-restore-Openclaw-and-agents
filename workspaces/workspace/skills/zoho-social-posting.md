# Zoho Social Posting Skill

## When to Use This Skill

Use this skill when you need to post content to Twitter and LinkedIn via Zoho Social. This is the preferred method since:
- ✅ Multi-platform (Twitter + LinkedIn in one post)
- ✅ Free (no API costs)
- ✅ Already configured with your accounts
- ✅ Browser automation handles the posting

## Prerequisites

1. OAuth tokens must be saved in `zoho-tokens.json`
2. Content files in `/content/social-post-XXX.md` format
3. Zoho credentials configured (already done)

## How to Post

### Option 1: Direct Command

Tell Claude: "Post Day X content via Zoho Social"

Claude will:
1. Read the content from `/content/social-post-00X.md`
2. Launch browser automation
3. Log into Zoho Social
4. Create and publish the post
5. Save screenshots as proof

### Option 2: Run Script Directly

```bash
node post-day2-zoho-v2.js
```

## What Content Gets Posted

The script reads from markdown files with this structure:

```markdown
## Twitter Version (280 chars)

[Short content for Twitter]

## LinkedIn Version

[Longer content for LinkedIn]
```

## Expected Output

After posting, you'll see:
- `zoho-dayX-v2-01-home.png` - Zoho Social home page
- `zoho-dayX-v2-02-compose.png` - New post composition
- `zoho-dayX-v2-03-content.png` - Content entered
- `zoho-dayX-v2-04-ready.png` - Channels selected, ready to publish
- `zoho-dayX-v2-05-success.png` - Post published successfully

## Troubleshooting

### OAuth Tokens Expired

If tokens expire, re-run the OAuth flow:
```bash
node zoho-oauth-server.js
```

Then click the authorization link in your browser.

### Posting Failed

Check the error screenshot:
```bash
ls -la zoho-dayX-v2-error.png
```

Common issues:
- Zoho Social UI changed (update selectors in script)
- Session expired (re-run OAuth)
- Network issues (retry)

## Files You Need

- `zoho-tokens.json` - OAuth tokens (auto-generated)
- `post-day2-zoho-v2.js` - Main posting script
- `/content/social-post-00X.md` - Content files

## Next Steps for Days 3-7

1. Ensure content files exist: `social-post-003.md` through `social-post-007.md`
2. Run posting script for each day
3. Verify screenshots show successful posts
4. Check bridge for Claude's confirmation messages

## Questions?

Ask Claude: "Post Day X via Zoho" and I'll handle the rest!
