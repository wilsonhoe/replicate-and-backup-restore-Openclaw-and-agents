const TwitterAuth = require('../lib/twitter-auth');
const LinkedInAuth = require('../lib/linkedin-auth');

async function testBrowserSessions() {
  console.log('🧪 Testing Browser Session Persistence\n');

  // Test Twitter
  console.log('--- Testing Twitter ---');
  const twitter = new TwitterAuth();
  try {
    const { page: twPage, browser: twBrowser } = await twitter.login(
      process.env.TWITTER_USERNAME,
      process.env.TWITTER_PASSWORD
    );

    // Test posting
    await twitter.postTweet(twPage, 'Test tweet from Lisa automation system 🤖');

    await twBrowser.close();
    console.log('✅ Twitter test passed\n');
  } catch (error) {
    console.error('❌ Twitter test failed:', error.message);
    if (error.message.includes('TWITTER_USERNAME')) {
      console.log('💡 Hint: Set TWITTER_USERNAME and TWITTER_PASSWORD environment variables');
    }
  }

  // Test LinkedIn
  console.log('--- Testing LinkedIn ---');
  const linkedin = new LinkedInAuth();
  try {
    const { page: liPage, browser: liBrowser } = await linkedin.login(
      process.env.LINKEDIN_USERNAME,
      process.env.LINKEDIN_PASSWORD
    );

    // Test posting
    await linkedin.postUpdate(liPage, 'Testing LinkedIn automation from Lisa AI system 🤖');

    await liBrowser.close();
    console.log('✅ LinkedIn test passed\n');
  } catch (error) {
    console.error('❌ LinkedIn test failed:', error.message);
    if (error.message.includes('LINKEDIN_USERNAME')) {
      console.log('💡 Hint: Set LINKEDIN_USERNAME and LINKEDIN_PASSWORD environment variables');
    }
  }

  console.log('🎉 Browser session tests complete!');
}

// Run tests
if (require.main === module) {
  testBrowserSessions();
}

module.exports = { testBrowserSessions };
