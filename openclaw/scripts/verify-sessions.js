const { chromium } = require('playwright');
const fs = require('fs');

async function verifySessions() {
  console.log('🔍 Verifying Browser Sessions\n');

  // Load session files
  const twitterSession = JSON.parse(fs.readFileSync('/home/wls/.openclaw/sessions/twitter-session.json', 'utf8'));
  const linkedinSession = JSON.parse(fs.readFileSync('/home/wls/.openclaw/sessions/linkedin-session.json', 'utf8'));

  console.log('✅ Session files loaded');
  console.log('  Twitter cookies:', twitterSession.twitter.cookies.length);
  console.log('  LinkedIn cookies:', linkedinSession.linkedin.cookies.length);

  // Connect to Chrome CDP
  console.log('\n🌐 Connecting to Chrome CDP...');
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const page = await context.newPage();

  // Add Twitter cookies
  console.log('\n🐦 Testing Twitter session...');
  await context.addCookies(twitterSession.twitter.cookies);
  await page.goto('https://twitter.com');
  await page.waitForTimeout(3000);

  const twitterUrl = page.url();
  const twitterHtml = await page.content();
  const isTwitterLoggedIn = twitterHtml.includes('SideNav_AccountSwitcher_Button') ||
                            twitterHtml.includes('data-testid="AppTabBar_Profile_Link"') ||
                            !twitterUrl.includes('login');

  console.log('  URL:', twitterUrl);
  console.log('  Logged in:', isTwitterLoggedIn ? '✅ YES' : '❌ NO');

  // Add LinkedIn cookies
  console.log('\n💼 Testing LinkedIn session...');
  await context.clearCookies();
  await context.addCookies(linkedinSession.linkedin.cookies);
  await page.goto('https://www.linkedin.com/feed/');
  await page.waitForTimeout(3000);

  const linkedinUrl = page.url();
  const linkedinHtml = await page.content();
  const isLinkedInLoggedIn = linkedinHtml.includes('global-nav__me') ||
                               linkedinHtml.includes('feed-identity-module') ||
                               linkedinHtml.includes('profile-nav') ||
                               !linkedinUrl.includes('login');

  console.log('  URL:', linkedinUrl);
  console.log('  Logged in:', isLinkedInLoggedIn ? '✅ YES' : '❌ NO');

  await browser.close();

  console.log('\n📊 Summary:');
  console.log('  Twitter:', isTwitterLoggedIn ? '✅ Session valid' : '❌ Needs login');
  console.log('  LinkedIn:', isLinkedInLoggedIn ? '✅ Session valid' : '❌ Needs login');
}

verifySessions().catch(console.error);
