// Post to Zoho Social using OAuth tokens
const https = require('https');
const fs = require('fs');

const ACCESS_TOKEN = '1000.b687d39363b88f62526079efc60459d4.bd69c109defaccbe836e59497a61bb25';
const SOCIAL_PROFILE_ID = '1663181000000023017';

function loadContent(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const parts = content.split('---\n');
  if (parts.length >= 3) {
    return parts[2].trim();
  }
  return content.trim();
}

async function makeRequest(options, postData = null) {
  return new Promise((resolve, reject) => {
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
    if (postData) req.write(postData);
    req.end();
  });
}

async function getSocialChannels() {
  const options = {
    hostname: 'www.zohoapis.com',
    port: 443,
    path: `/social/api/v1/socialprofiles/${SOCIAL_PROFILE_ID}/channels`,
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${ACCESS_TOKEN}`,
      'Content-Type': 'application/json'
    }
  };
  return await makeRequest(options);
}

async function createPost(content, channelIds) {
  const postData = JSON.stringify({
    content: content,
    channelIds: channelIds
  });

  const options = {
    hostname: 'www.zohoapis.com',
    port: 443,
    path: `/social/api/v1/socialprofiles/${SOCIAL_PROFILE_ID}/posts`,
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${ACCESS_TOKEN}`,
      'Content-Type': 'application/json',
      'Content-Length': postData.length
    }
  };
  return await makeRequest(options, postData);
}

async function main() {
  console.log('🚀 Posting Day 2 content via Zoho Social...\n');

  // Load content
  const content = loadContent('./content/social-post-002.md');
  console.log('Content loaded:', content.substring(0, 50) + '...\n');

  // Get social channels
  console.log('📡 Getting connected channels...');
  const channels = await getSocialChannels();
  console.log('Channels response:', JSON.stringify(channels, null, 2));

  // Post content
  console.log('\n📝 Creating post...');
  const result = await createPost(content, []); // Post to all channels
  console.log('Post result:', JSON.stringify(result, null, 2));

  console.log('\n✅ Done!');
}

main().catch(console.error);
