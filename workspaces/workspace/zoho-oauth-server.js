// Zoho OAuth Server-based Application Flow
// Following: https://www.zoho.com/accounts/protocol/oauth/web-server-applications.html

const http = require('http');
const https = require('https');
const querystring = require('querystring');
const fs = require('fs');

const CLIENT_ID = '1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS';
const CLIENT_SECRET = '1ce34ab8330b4c8a864695ada08aa001303cf81bfb';
const REDIRECT_URI = 'http://localhost/callback';
const PORT = 3000;

// Step 1: Generate Authorization URL
function getAuthorizationUrl() {
  // Following documented endpoint: oauth/v2/auth
  const params = {
    client_id: CLIENT_ID,
    response_type: 'code',
    redirect_uri: REDIRECT_URI,
    scope: 'ZohoSocial.posts.ALL',
    access_type: 'offline',
    prompt: 'consent'
  };
  return `https://accounts.zoho.com/oauth/v2/auth?${querystring.stringify(params)}`;
}

// Step 2: Exchange authorization code for tokens
async function exchangeCodeForTokens(authCode) {
  return new Promise((resolve, reject) => {
    const postData = querystring.stringify({
      grant_type: 'authorization_code',
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      redirect_uri: REDIRECT_URI,
      code: authCode
    });

    const options = {
      hostname: 'accounts.zoho.com',
      port: 443,
      path: '/oauth/v2/token',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': postData.length
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ raw: data });
        }
      });
    });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

// Start local server to receive callback
function startCallbackServer() {
  return new Promise((resolve) => {
    const server = http.createServer(async (req, res) => {
      console.log(`\n📥 Received request: ${req.url}`);

      if (req.url.startsWith('/callback')) {
        const url = new URL(req.url, `http://localhost:${PORT}`);
        const code = url.searchParams.get('code');
        const error = url.searchParams.get('error');

        if (error) {
          console.log(`❌ OAuth Error: ${error}`);
          res.end('<h1>Authorization Failed</h1><p>Check console for error.</p>');
          server.close();
          resolve(null);
        } else if (code) {
          console.log(`✅ Authorization code received: ${code.substring(0, 20)}...`);
          res.end('<h1>Authorization Successful!</h1><p>You can close this window.</p>');
          server.close();
          resolve(code);
        } else {
          res.end('<h1>No code received</h1>');
          server.close();
          resolve(null);
        }
      }
    });

    server.listen(PORT, () => {
      console.log(`🌐 Callback server running on http://localhost:${PORT}`);
    });
  });
}

async function main() {
  console.log('🚀 Zoho OAuth Server-based Flow\n');
  console.log('================================\n');

  // Check if we already have tokens
  if (fs.existsSync('./zoho-tokens.json')) {
    const tokens = JSON.parse(fs.readFileSync('./zoho-tokens.json', 'utf8'));
    console.log('✅ Tokens already exist!');
    console.log('Access Token:', tokens.access_token.substring(0, 30) + '...');
    console.log('\nReady to post to Zoho Social.');
    return tokens;
  }

  console.log('Step 1: Starting authorization flow...\n');
  console.log('Open this URL in your browser:\n');
  console.log(getAuthorizationUrl());
  console.log('\n================================');
  console.log('Waiting for authorization...\n');

  // Start server and wait for callback
  const authCode = await startCallbackServer();

  if (!authCode) {
    console.log('❌ Failed to get authorization code');
    return;
  }

  console.log('\nStep 2: Exchanging code for tokens...');
  const tokens = await exchangeCodeForTokens(authCode);

  if (tokens.access_token) {
    console.log('✅ Success! Tokens received:');
    console.log('  Access Token:', tokens.access_token.substring(0, 30) + '...');
    console.log('  Refresh Token:', tokens.refresh_token ? 'Yes' : 'No');
    console.log('  Expires in:', tokens.expires_in, 'seconds');

    // Save tokens
    fs.writeFileSync('./zoho-tokens.json', JSON.stringify(tokens, null, 2));
    console.log('\n💾 Tokens saved to zoho-tokens.json');

    return tokens;
  } else {
    console.log('❌ Token exchange failed:', tokens);
    return null;
  }
}

main().catch(console.error);
