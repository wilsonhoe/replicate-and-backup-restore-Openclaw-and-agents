const puppeteer = require('puppeteer');

async function clickContinueAsLisa() {
  console.log('Clicking "Continue as Lisa" button...');
  
  const browser = await puppeteer.launch({
    headless: false,
    userDataDir: '/home/wls/.config/google-chrome',
    args: ['--profile-directory=Default', '--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const pages = await browser.pages();
    let targetPage = null;
    
    // Find Twitter developer page
    for (const page of pages) {
      const url = page.url();
      if (url.includes('developer.twitter.com') || url.includes('twitter.com')) {
        targetPage = page;
        break;
      }
    }
    
    if (!targetPage) {
      targetPage = await browser.newPage();
      await targetPage.goto('https://developer.twitter.com/en/portal/petition/essential/basic-info', { waitUntil: 'networkidle2' });
    }

    // Wait for page to load
    await targetPage.waitForNetworkIdle();
    
    // Take screenshot before click
    await targetPage.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-sso-before.png' });
    console.log('📸 Screenshot: twitter-sso-before.png');

    // Look for "Continue as" button
    const continueButton = await targetPage.evaluate(() => {
      // Find button with "Continue as" text
      const buttons = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
      const continueBtn = buttons.find(btn => btn.innerText && btn.innerText.includes('Continue as'));
      
      if (continueBtn) {
        continueBtn.click();
        return true;
      }
      return false;
    });

    if (continueButton) {
      console.log('✅ Clicked "Continue as Lisa" button');
      
      // Wait for navigation
      await targetPage.waitForNavigation({ waitUntil: 'networkidle2', timeout: 10000 }).catch(() => {});
      
      // Take screenshot after click
      await targetPage.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-sso-after.png' });
      console.log('📸 Screenshot: twitter-sso-after.png');
    } else {
      console.log('⚠️ Button not found - check screenshot');
    }

    // Keep browser open for user to continue
    console.log('Browser open - complete the application in the window');
    await new Promise(r => setTimeout(r, 30000));
    
    return true;
  } catch (error) {
    console.error('❌ Error:', error.message);
    
    // Screenshot on error
    const pages = await browser.pages();
    if (pages.length > 0) {
      await pages[0].screenshot({ path: '/home/wls/.openclaw/workspace/twitter-sso-error.png' });
      console.log('📸 Screenshot: twitter-sso-error.png');
    }
    
    return false;
  }
}

clickContinueAsLisa();