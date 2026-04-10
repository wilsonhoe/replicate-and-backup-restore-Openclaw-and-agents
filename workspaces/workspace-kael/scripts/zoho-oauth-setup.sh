#!/bin/bash
# Zoho Social OAuth Setup Script
# This script generates the authorization URL and exchanges code for tokens

CLIENT_ID="1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS"
CLIENT_SECRET="1ce34ab8330b4c8a864695ada08aa001303cf81bfb"
REDIRECT_URI="http://localhost:8080/callback"
SCOPE="ZohoSocial.posts.ALL,ZohoSocial.messages.ALL"

# Generate authorization URL
echo "=========================================="
echo "ZOHO SOCIAL OAuth Setup"
echo "=========================================="
echo ""
echo "Step 1: Visit this URL in your browser:"
echo ""
AUTH_URL="https://accounts.zoho.com/oauth/v2/auth?scope=${SCOPE}&client_id=${CLIENT_ID}&response_type=code&access_type=offline&redirect_uri=${REDIRECT_URI}"
echo "$AUTH_URL"
echo ""
echo "Step 2: Login with lisamolbot@gmail.com"
echo "Step 3: Authorize the app"
echo "Step 4: You'll be redirected to localhost (will show error, that's OK)"
echo "Step 5: Copy the 'code' parameter from the URL"
echo ""
echo "Paste the authorization code here:"
read -r AUTH_CODE

echo ""
echo "Exchanging code for tokens..."

# Exchange code for tokens
RESPONSE=$(curl -s -X POST https://accounts.zoho.com/oauth/v2/token \
  -d "grant_type=authorization_code" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "redirect_uri=${REDIRECT_URI}" \
  -d "code=${AUTH_CODE}")

echo ""
echo "Response:"
echo "$RESPONSE" | jq .

# Extract tokens
ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh_token')
EXPIRES_IN=$(echo "$RESPONSE" | jq -r '.expires_in')

if [ "$REFRESH_TOKEN" != "null" ] && [ -n "$REFRESH_TOKEN" ]; then
    echo ""
    echo "=========================================="
    echo "SUCCESS! Tokens obtained:"
    echo "=========================================="
    echo "Access Token: ${ACCESS_TOKEN:0:30}..."
    echo "Refresh Token: ${REFRESH_TOKEN:0:30}..."
    echo "Expires in: ${EXPIRES_IN} seconds"
    echo ""
    echo "Save these to TOOLS.md"
    
    # Append to TOOLS.md
    cat >> /home/wls/.openclaw/workspace-kael/TOOLS.md << EOF

### Zoho Social OAuth Tokens
| Token Type | Value |
|------------|-------|
| Access Token | ${ACCESS_TOKEN} |
| Refresh Token | ${REFRESH_TOKEN} |
| Expires At | $(date -d "+${EXPIRES_IN} seconds" "+%Y-%m-%d %H:%M:%S") |

EOF
    echo "Tokens appended to TOOLS.md"
else
    echo "ERROR: Failed to get refresh token"
    echo "Full response: $RESPONSE"
fi
