// Zoho Social API Posting Script
// Posts to Twitter and LinkedIn via Zoho Social

const https = require('https');
const fs = require('fs');
const querystring = require('querystring');

// Zoho OAuth Configuration
const CLIENT_ID = '1000.CJWJUBMWNRNAXW9BCVC81J6XCQOPBS';
const CLIENT_SECRET = '1ce34ab8330b4c8a864695ada08aa001303cf81bfb';
const REDIRECT_URI = 'http://localhost/callback';
const SCOPE = 'ZohoSocial.messages.ALL';

// Zoho Social Profile ID from URL
const SOCIAL_PROFILE_ID = '1663181000000023017';

// Function to make HTTPS requests
function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ statusCode: res.statusCode, data: parsed, headers: res.headers });
        } catch (e) {
          resolve({ statusCode: res.statusCode, data: data, headers: res.headers });
        }
      });
    });
    req.on('error', reject);
    if (postData) req.write(postData);
    req.end();
  });
}

// Step 1: Generate Authorization URL
function getAuthorizationUrl() {
  const params = {
    client_id: CLIENT_ID,
    response_type: 'code',
    redirect_uri: REDIRECT_URI,
    access_type: 'offline',
    prompt: 'consent'
  };
  return `https://accounts.zoho.com/oauth/v2/auth?${querystring.stringify(params)}`;
}

// Step 2: Exchange authorization code for tokens
async function exchangeCodeForTokens(authCode) {
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

  return await makeRequest(options, postData);
}

// Step 3: Refresh access token
async function refreshAccessToken(refreshToken) {
  const postData = querystring.stringify({
    grant_type: 'refresh_token',
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    refresh_token: refreshToken
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

  return await makeRequest(options, postData);
}

// Step 4: Get connected social channels
async function getSocialChannels(accessToken) {
  const options = {
    hostname: 'social.zoho.com',
    port: 443,
    path: `/api/v1/socialprofiles/${SOCIAL_PROFILE_ID}/channels`,
    method: 'GET',
    headers: {
      'Authorization': `Zoho-oauthtoken ${accessToken}`,
      'Content-Type': 'application/json'
    }
  };

  return await makeRequest(options);
}

// Step 5: Create a post
async function createPost(accessToken, message, channelIds) {
  const postData = JSON.stringify({
    content: message,
    channelIds: channelIds,
    scheduledTime: null // Post immediately
  });

  const options = {
    hostname: 'social.zoho.com',
    port: 443,
    path: `/api/v1/socialprofiles/${SOCIAL_PROFILE_ID}/messages`,
    method: 'POST',
    headers: {
      'Authorization': `Zoho-oauthtoken ${accessToken}`,
      'Content-Type': 'application/json',
      'Content-Length': postData.length
    }
  };

  return await makeRequest(options, postData);
}

// Load content from file
function loadContent(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  // Parse markdown frontmatter
  const parts = content.split('---\n');
  if (parts.length >= 3) {
    return {
      frontmatter: parts[1],
      content: parts[2].trim()
    };
  }
  return { content: content.trim() };
}

// Main execution
async function main() {
  console.log('🚀 Zoho Social Posting Script\n');

  // Check if we have stored tokens
  const tokenFile = './zoho-tokens.json';
  let accessToken, refreshToken;

  if (fs.existsSync(tokenFile)) {
    console.log('📋 Loading existing tokens...');
    const tokens = JSON.parse(fs.readFileSync(tokenFile, 'utf8'));
    accessToken = tokens.access_token;
    refreshToken = tokens.refresh_token;

    // Try to refresh the token
    console.log('🔄 Refreshing access token...');
    const refreshResult = await refreshAccessToken(refreshToken);
    if (refreshResult.data.access_token) {
      accessToken = refreshResult.data.access_token;
      fs.writeFileSync(tokenFile, JSON.stringify({
        access_token: accessToken,
        refresh_token: refreshToken || tokens.refresh_token
      }, null, 2));
      console.log('✅ Token refreshed successfully\n');
    } else {
      console.log('❌ Token refresh failed:', refreshResult.data);
      accessToken = null;
    }
  }

  if (!accessToken) {
    console.log('\n🔐 AUTHORIZATION REQUIRED');
    console.log('========================');
    console.log('\nPlease visit this URL in your browser and authorize:');
    console.log('\n' + getAuthorizationUrl());
    console.log('\nAfter authorization, you will be redirected to localhost.');
    console.log('Copy the "code" parameter from the URL and run:');
    console.log('\n  node zoho-social-post.js AUTH_CODE');
    console.log('\n========================\n');
    return;
  }

  // Load Day 2 content
  console.log('📝 Loading content...');
  const postData = loadContent('./content/social-post-002.md');

  // Get channels
  console.log('📡 Fetching connected social channels...');
  const channelsResult = await getSocialChannels(accessToken);
  console.log('Channels:', JSON.stringify(channelsResult.data, null, 2));

  if (!channelsResult.data || !channelsResult.data.data) {
    console.log('❌ Failed to fetch channels');
    return;
  }

  const channels = channelsResult.data.data;
  const twitterChannel = channels.find(c => c.channelType === 'twitter');
  const linkedinChannel = channels.find(c => c.channelType === 'linkedin');

  if (!twitterChannel && !linkedinChannel) {
    console.log('❌ No Twitter or LinkedIn channels found. Please connect them in Zoho Social first.');
    return;
  }

  // Post to Twitter
  if (twitterChannel) {
    console.log(`\n🐦 Posting to Twitter (${twitterChannel.channelName})...`);
    const twitterContent = postData.content.split('\n').slice(0, 10).join('\n'); // First 10 lines for Twitter
    const twitterResult = await createPost(accessToken, twitterContent, [twitterChannel.channelId]);
    console.log('Result:', JSON.stringify(twitterResult.data, null, 2));
  }

  // Post to LinkedIn
  if (linkedinChannel) {
    console.log(`\n💼 Posting to LinkedIn (${linkedinChannel.channelName})...`);
    const linkedinResult = await createPost(accessToken, postData.content, [linkedinChannel.channelId]);
    console.log('Result:', JSON.stringify(linkedinResult.data, null, 2));
  }

  console.log('\n✅ Done!');
}

// Handle command line arguments
const authCode = process.argv[2];

if (authCode && authCode.startsWith('1000.')) {
  // Exchange authorization code for tokens
  console.log('🔐 Exchanging authorization code for tokens...');
  exchangeCodeForTokens(authCode).then(result => {
    if (result.data.access_token) {
      fs.writeFileSync('./zoho-tokens.json', JSON.stringify({
        access_token: result.data.access_token,
        refresh_token: result.data.refresh_token
      }, null, 2));
      console.log('✅ Tokens saved to zoho-tokens.json');
      console.log('\nRun the script again to post content.');
    } else {
      console.log('❌ Token exchange failed:', result.data);
    }
  });
} else {
  main().catch(console.error);
}
