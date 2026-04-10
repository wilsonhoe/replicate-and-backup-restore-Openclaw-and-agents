#!/usr/bin/env node
/**
 * Social SSO Login Test
 * 
 * Logs into Twitter and LinkedIn via Google SSO
 * Uses existing Chrome CDP session on port 9222
 * 
 * Usage:
 *   node test-sso-login.js twitter   - Login to Twitter/X
 *   node test-sso-login.js linkedin  - Login to LinkedIn
 *   node test-sso-login.js both      - Login to both
 */

const puppeteer = require('puppeteer-core');
const SessionManager = require('../lib/session-manager');

const PLATFORMS = {
  twitter: {
    name: 'Twitter/X',
    loginUrl: 'https://twitter.com/i/flow/login',
    homeUrl: 'https://twitter.com/home',
    checkSelector: '[data-testid="SideNav_AccountSwitcher_Button"]',
    ssoButtonText: 'Continue with Google',
    sessionFile: 'twitter_session.json'
  },
  linkedin: {
    name: 'LinkedIn',
    loginUrl: 'https://www.linkedin.com/login',
    homeUrl: 'https://www.linkedin.com/feed/',
    checkSelector: '.global-nav__me, .feed-shared-avatar-image',
    ssoButtonText: 'Continue with Google',
    sessionFile: 'linkedin_session.json'
  }
};

async function loginWithGoogleSSO(platformKey) {
  const platform = PLATFORMS[platformKey];
  if (!platform) {
    console.log(`❌ Unknown platform: ${platformKey}`);
    return { success: false };
  }

  const sessionManager = new SessionManager();
  console.log(`\n🔐 ${platform.name} Google SSO Login`);
  console.log('='.repeat(50));

  try {
    console.log('\n🔌 Connecting to Chrome (port 9222)...');
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null
    });

    // Check existing session
    if (await sessionManager.isSessionValid(platformKey)) {
      console.log('📁 Found saved session, checking...');
      
      let page = (await browser.pages()).find(p => p.url().includes(platformKey));
      if (!page) page = await browser.newPage();
      
      const context = browser.browserContexts()[0];
      await sessionManager.loadSession(platformKey, context);
      await page.goto(platform.homeUrl);
      await new Promise(r => setTimeout(r, 3000));

      const checkEl = await page.$(platform.checkSelector);
      if (checkEl) {
        console.log(`✅ Already logged into ${platform.name}!`);
        await page.screenshot({ 
          path: `/home/wls/.openclaw/workspace/${platformKey}-session-valid.png` 
        });
        return { success: true, browser };
      }
      console.log('⚠️ Session expired, proceeding with fresh login...');
    }

    // Fresh login
    let page = (await browser.pages()).find(p => p.url().includes(platformKey));
    if (!page) page = await browser.newPage();

    console.log(`\n📱 Navigating to ${platform.loginUrl}...`);
    await page.goto(platform.loginUrl);
    await new Promise(r => setTimeout(r, 3000));

    await page.screenshot({ 
      path: `/home/wls/.openclaw/workspace/${platformKey}-login-start.png` 
    });
    console.log(`📸 Saved: ${platformKey}-login-start.png`);

    // Find Google SSO button
    console.log(`\n🔍 Searching for "${platform.ssoButtonText}" button...`);
    
    let found = false;
    
    // Method 1: Direct selector search
    const selectors = [
      `button:has-text("${platform.ssoButtonText}")`,
      `div[role="button"]:has-text("${platform.ssoButtonText}")`,
      `[data-testid="googleButton"]`,
      '[data-id="google-oauth"]',
      'button[data-tracking-control-name="login_google"]'
    ];

    for (const sel of selectors) {
      try {
        const btn = await page.$(sel);
        if (btn) {
          console.log(`   Found: ${sel}`);
          await btn.click();
          found = true;
          break;
        }
      } catch (e) {}
    }

    // Method 2: Text-based search
    if (!found) {
      found = await page.evaluate((buttonText) => {
        const elements = document.querySelectorAll('button, [role="button"], div[role="button"], a');
        for (const el of elements) {
          const text = (el.innerText || el.textContent || '').toLowerCase();
          if (text.includes('google') && (text.includes('continue') || text.includes('sign in'))) {
            el.click();
            return true;
          }
        }
        return false;
      }, platform.ssoButtonText);
    }

    if (found) {
      console.log('✅ Clicked Google SSO button');
    } else {
      console.log('⚠️ Button not found automatically');
      console.log('   → PLEASE CLICK "Continue with Google" in Chrome window');
    }

    // Wait for Google popup
    await new Promise(r => setTimeout(r, 2000));
    const pages = await browser.pages();
    const googlePopup = pages.find(p => p.url().includes('accounts.google.com'));
    
    if (googlePopup) {
      console.log('\n🔐 Google login popup opened!');
      console.log('   → Select your Google account');
      console.log('   → Script will detect when complete...\n');
    }

    // Wait for login completion
    console.log('⏳ Waiting for login to complete...');
    console.log('   (Timeout: 90 seconds)\n');

    let loggedIn = false;
    const startTime = Date.now();
    
    while (Date.now() - startTime < 90000) {
      await new Promise(r => setTimeout(r, 2000));
      
      // Get current page
      const currentPages = await browser.pages();
      page = currentPages.find(p => 
        p.url().includes(platformKey) && !p.url().includes('accounts.google')
      ) || page;

      const url = page.url();
      
      // Check for successful login
      if (url.includes(platform.homeUrl.split('/')[2]) && !url.includes('login')) {
        const checkEl = await page.$(platform.checkSelector);
        if (checkEl) {
          loggedIn = true;
          break;
        }
      }
    }

    if (loggedIn) {
      console.log(`\n✅ SUCCESS: Logged into ${platform.name}!`);
      
      // Save session
      await sessionManager.saveSession(platformKey, page);
      console.log('💾 Session saved');
      
      await page.screenshot({ 
        path: `/home/wls/.openclaw/workspace/${platformKey}-logged-in.png` 
      });
      console.log(`📸 Saved: ${platformKey}-logged-in.png`);
      
      return { success: true, browser };
    } else {
      console.log(`\n❌ FAILED: Login timeout or error`);
      console.log('   → Check Chrome window for error messages');
      await page.screenshot({ 
        path: `/home/wls/.openclaw/workspace/${platformKey}-login-failed.png` 
      });
      return { success: false, browser };
    }

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    return { success: false, error: error.message };
  }
}

// Main execution
async function main() {
  const arg = process.argv[2] || 'twitter';
  
  if (arg === 'both') {
    console.log('\n🔄 Logging into both platforms...\n');
    
    const twitter = await loginWithGoogleSSO('twitter');
    if (twitter.success) {
      console.log('\n✅ Twitter login complete!\n');
      // Keep browser open for LinkedIn
    }
    
    const linkedin = await loginWithGoogleSSO('linkedin');
    if (linkedin.success) {
      console.log('\n✅ LinkedIn login complete!\n');
    }
    
    console.log('\n🎉 Both platforms processed!');
    process.exit(twitter.success && linkedin.success ? 0 : 1);
    
  } else {
    const result = await loginWithGoogleSSO(arg);
    process.exit(result.success ? 0 : 1);
  }
}

main();