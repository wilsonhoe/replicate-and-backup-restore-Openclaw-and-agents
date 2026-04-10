const puppeteer = require('puppeteer-core');
const SessionManager = require('../lib/session-manager');

/**
 * Google SSO Login for Twitter and LinkedIn
 * 
 * Usage:
 *   node google-sso-login.js twitter   - Login to Twitter via Google SSO
 *   node google-sso-login.js linkedin  - Login to LinkedIn via Google SSO
 */

const PLATFORMS = {
  twitter: {
    name: 'Twitter/X',
    loginUrl: 'https://twitter.com/i/flow/login',
    homeUrl: 'https://twitter.com',
    selectors: {
      googleBtn: ['button:has-text("Continue with Google")', 'div[role="button"]:has-text("Google")', '[data-testid="googleButton"]'],
      signInBtn: 'a[href="/login"]',
      profileIcon: '[data-testid="SideNav_AccountSwitcher_Button"]',
      composeBtn: '[data-testid="SideNav_NewTweet_Button"]'
    }
  },
  linkedin: {
    name: 'LinkedIn',
    loginUrl: 'https://www.linkedin.com/login',
    homeUrl: 'https://www.linkedin.com/feed',
    selectors: {
      googleBtn: ['button:has-text("Continue with Google")', '[data-id="google-oauth"]', 'button[data-tracking-control-name="login_google"],
      signInBtn: 'a[href="/login"]',
      profileIcon: '.global-nav__me',
      composeBtn: '.share-box-feed-entry'
    }
  }
};

async function loginWithGoogleSSO(platform) {
  const config = PLATFORMS[platform];
  if (!config) {
    console.log(`❌ Unknown platform: ${platform}`);
    console.log(`Available: ${Object.keys(PLATFORMS).join(', ')}`);
    return;
  }

  console.log(`\n🔐 ${config.name} Google SSO Login\n`);
  console.log('🔌 Connecting to Chrome...');

  const sessionManager = new SessionManager();

  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null
    });

    let page = (await browser.pages()).find(p => 
      p.url().includes(platform) || p.url().includes('google')
    ) || await browser.newPage();

    // Check for existing session
    const hasSession = await sessionManager.isSessionValid(platform);
    if (hasSession) {
      console.log('🔄 Found saved session, checking validity...');
      
      const context = browser.browserContexts()[0];
      await sessionManager.loadSession(platform, context);
      await page.goto(config.homeUrl);
      await page.waitForTimeout(3000);

      // Check if logged in
      const profileBtn = await page.$(config.selectors.profileIcon);
      if (profileBtn) {
        console.log(`✅ Already logged into ${config.name}`);
        await page.screenshot({ path: `/home/wls/.openclaw/workspace/${platform}-logged-in.png` });
        return { success: true, browser };
      }
      console.log('⚠️ Session expired, need fresh login...');
    }

    // Navigate to login page
    console.log(`📱 Navigating to ${config.name} login...`);
    await page.goto(config.loginUrl);
    await page.waitForTimeout(2000);

    await page.screenshot({ path: `/home/wls/.openclaw/workspace/${platform}-login-page.png` });
    console.log(`📸 Screenshot: ${platform}-login-page.png`);

    // Look for Google SSO button
    console.log('\n🔍 Looking for Google SSO button...');
    
    let clicked = false;
    for (const selector of config.selectors.googleBtn) {
      try {
        const btn = await page.$(selector);
        if (btn) {
          console.log(`✅ Found: ${selector}`);
          await btn.click();
          clicked = true;
          break;
        }
      } catch (e) {
        // Try next selector
      }
    }

    if (!clicked) {
      // Fallback: Look for any button containing "Google" text
      console.log('🔍 Searching for Google button by text...');
      
      const found = await page.evaluate(() => {
        const buttons = document.querySelectorAll('button, [role="button"], div[role="button"], a');
        for (const btn of buttons) {
          const text = (btn.innerText || btn.textContent || '').toLowerCase();
          if (text.includes('continue with google') || text.includes('sign in with google') || 
              text.includes('google') && text.includes('continue')) {
            btn.click();
            return true;
          }
        }
        return false;
      });
      
      if (found) {
        console.log('✅ Clicked Google button by text');
        clicked = true;
      }
    }

    if (clicked) {
      console.log('\n⏳ Waiting for Google login popup...');
      await page.waitForTimeout(3000);

      // Handle Google login in popup
      const pages = await browser.pages();
      const googlePopup = pages.find(p => p.url().includes('accounts.google.com'));
      
      if (googlePopup) {
        console.log('🔐 Google login popup detected');
        console.log('   → Complete login manually in the popup window');
        console.log('   → This script will wait for you...');
        
        // Wait for popup to close (login complete)
        await new Promise((resolve) => {
          const checkClosed = setInterval(async () => {
            const currentPages = await browser.pages();
            const stillOpen = currentPages.find(p => p.url().includes('accounts.google.com'));
            if (!stillOpen) {
              clearInterval(checkClosed);
              console.log('✅ Google login completed');
              resolve();
            }
          }, 1000);
        });
      }
    } else {
      console.log('⚠️ No Google SSO button found');
      console.log('   → Please click "Continue with Google" manually in Chrome');
      console.log('   → This script will wait for login completion...');
    }

    // Wait for login completion
    console.log('\n⏳ Waiting for login to complete...');
    console.log('   → Check the Chrome window');
    console.log('   → Complete Google authentication if needed');
    console.log('   → Login is detected automatically when redirected to home\n');

    // Wait for redirect to home page
    let loggedIn = false;
    for (let i = 0; i < 60; i++) {
      await page.waitForTimeout(2000);
      const currentUrl = page.url();
      
      // Check if we're on home page
      if (currentUrl.includes(config.homeUrl.split('/')[2]) && 
          !currentUrl.includes('login') && 
          !currentUrl.includes('google')) {
        
        // Verify login by checking for profile element
        const profileBtn = await page.$(config.selectors.profileIcon);
        if (profileBtn) {
          loggedIn = true;
          break;
        }
      }
      
      // Refresh page reference in case of navigation
      page = (await browser.pages()).find(p => 
        p.url().includes(platform) && !p.url().includes('google')
      ) || page;
    }

    if (loggedIn) {
      console.log(`✅ Successfully logged into ${config.name}!`);
      
      // Save session
      await sessionManager.saveSession(platform, page);
      console.log('💾 Session saved for future use');
      
      await page.screenshot({ path: `/home/wls/.openclaw/workspace/${platform}-logged-in.png` });
      console.log(`📸 Screenshot: ${platform}-logged-in.png`);
      
      return { success: true, browser };
    } else {
      console.log('❌ Login timed out or failed');
      return { success: false, browser };
    }

  } catch (error) {
    console.error('❌ Error:', error.message);
    return { success: false, error };
  }
}

// Run if called directly
if (require.main === module) {
  const platform = process.argv[2] || 'twitter';
  loginWithGoogleSSO(platform)
    .then(result => {
      if (result?.success) {
        console.log(`\n🎉 ${platform.toUpperCase()} login complete!`);
        console.log('   You can now use session for automation.');
      }
      process.exit(result?.success ? 0 : 1);
    });
}

module.exports = { loginWithGoogleSSO, PLATFORMS };