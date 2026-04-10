const { TwitterApi } = require('twitter-api-v2');

/**
 * Twitter API v2 - Simple Tweet Poster
 *
 * PREREQUISITES:
 * 1. Twitter Developer Account: https://developer.twitter.com/en/portal/dashboard
 * 2. Create an app and get API keys
 * 3. Copy this file and fill in your credentials below
 *
 * USAGE:
 * node twitter-api-post.js
 */

// ============================================
// STEP 1: FILL IN YOUR CREDENTIALS
// Get these from https://developer.twitter.com/en/portal/dashboard
// ============================================
const credentials = {
  appKey: 'nhOANfzRDWoW4kqy8LfwE1QC3',
  appSecret: 'mBr3Oif3P9DSzhGEMc1bFa0KRajwvFcQAio9q1PlaWSpAtGIg3',
  // Note: Need User Access Token (not App-Only Bearer Token) to post tweets
  // Go to Developer Portal → Keys and Tokens → Generate Access Token and Secret
  accessToken: process.env.TWITTER_ACCESS_TOKEN || 'NEED_USER_ACCESS_TOKEN_HERE',
  accessSecret: process.env.TWITTER_ACCESS_SECRET || 'NEED_USER_ACCESS_SECRET_HERE',
};

// ============================================
// STEP 2: DEFINE YOUR CONTENT
// Day 2: Automation ROI Calculator
// ============================================
const tweetContent = `Automation ROI Calculator 🔢

Day 2: Is automation actually worth it?

Real example:
• 2 hours/day saved
• $50/hour value
• = $2,500/month value

Tools cost: $50/month
Net gain: $2,450/month

ROI: 4,900%

This is why I build systems.

#Automation #AI #Productivity`;

// ============================================
// STEP 3: POST THE TWEET
// ============================================
async function postTweet() {
  console.log('🐦 Initializing Twitter API client...\n');

  // Validate credentials
  if (credentials.appKey === 'YOUR_API_KEY_HERE') {
    console.error('❌ ERROR: Please fill in your Twitter API credentials!');
    console.error('   Get them at: https://developer.twitter.com/en/portal/dashboard');
    console.error('   Or set environment variables:\n');
    console.error('   export TWITTER_API_KEY=your_key');
    console.error('   export TWITTER_API_SECRET=your_secret');
    console.error('   export TWITTER_ACCESS_TOKEN=your_token');
    console.error('   export TWITTER_ACCESS_SECRET=your_secret\n');
    process.exit(1);
  }

  try {
    // Create client
    const client = new TwitterApi(credentials);

    console.log('✅ Connected to Twitter API v2');
    console.log('📝 Preparing tweet...\n');
    console.log('Content preview:');
    console.log('─'.repeat(50));
    console.log(tweetContent);
    console.log('─'.repeat(50));
    console.log();

    // Post tweet
    const { data } = await client.v2.tweet(tweetContent);

    console.log('✅ SUCCESS! Tweet posted!');
    console.log(`🔗 Tweet URL: https://twitter.com/i/web/status/${data.id}`);
    console.log(`🆔 Tweet ID: ${data.id}`);
    console.log();
    console.log('🎉 Day 2 content posted successfully!');

    return data;

  } catch (error) {
    console.error('❌ ERROR posting tweet:\n');

    if (error.code === 401) {
      console.error('Authentication failed. Check your API credentials.');
    } else if (error.code === 403) {
      console.error('Authorization failed. Your app may not have write permissions.');
      console.error('Go to your app settings and enable "Read and Write" permissions.');
    } else if (error.code === 429) {
      console.error('Rate limit exceeded. Wait 15 minutes before trying again.');
    } else {
      console.error(error.message || error);
    }

    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  postTweet().then(() => {
    console.log('\n✨ Done! Check your Twitter account to verify the post.\n');
    process.exit(0);
  }).catch((error) => {
    console.error('Unexpected error:', error);
    process.exit(1);
  });
}

module.exports = { postTweet };
