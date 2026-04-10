// Direct Authentication Script for Twitter
// Uses provided credentials to login and post
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  let browser;
  let page;

  try {
    console.log('Starting direct authentication for Twitter...');

    // Load Day 2 content
    const content = fs.readFileSync('./content/social-post-002.md', 'utf8').split('---\n')[2].trim();
    console.log('Content loaded:', content.substring(0, 100) + '...');

    // Launch browser
    browser = await chromium.launch({ 
      headless: false, // Visible for debugging
      args: ['--disable-blink-features=AutomationControlled']
    });
    
    page = await browser.newPage();
    
    // Navigate to Twitter login
    await page.goto('https://x.com/login');
    await page.waitForTimeout(3000);
    
    console.log('At login page...');
    await page.screenshot({ path: './debug-login-start.png' });
    
    // Enter username
    await page.fill('input[autocomplete="username"]', 'lisamolbot@gmail.com');
    console.log('Username entered');
    await page.screenshot({ path: './debug-username-entered.png' });
    
    // Click Next
    await page.click('button[role="button"]:has-text("Next")');
    await page.waitForTimeout(3000);
    
    console.log('After Next click...');
    await page.screenshot({ path: './debug-after-next.png' });
    
    // Enter password - Wilson provided
    await page.fill('input[autocomplete="current-password"]', '%LvZ%;g9Z$79+q9');
    console.log('Password entered');
    await page.screenshot({ path: './debug-password-entered.png' });
    
    // Click Login
    await page.click('button[data-testid="LoginForm_Login_Button"]');
    await page.waitForTimeout(5000);
    
    console.log('After login attempt...');
    await page.screenshot({ path: './debug-after-login.png' });
    
    // Check if we're logged in
    const currentUrl = await page.url();
    console.log('Current URL:', currentUrl);
    
    if (currentUrl.includes('home') || currentUrl === 'https://x.com/') {
      console.log('✅ Login successful!');
      
      // Navigate to compose tweet
      await page.goto('https://x.com/compose/tweet');
      await page.waitForTimeout(3000);
      
      // Use character-by-character typing for React
      const tweetTextarea = await page.locator('[data-testid="tweetTextarea_0"]');
      await tweetTextarea.click();
      
      // Type content character by character to trigger React state
      for (const char of content) {
        await page.keyboard.type(char);
        await page.waitForTimeout(50); // Small delay between characters
      }
      
      console.log('Content typed');
      await page.screenshot({ path: './debug-content-typed.png' });
      
      // Click tweet button
      const tweetButton = await page.locator('[data-testid="tweetButtonInline"]');
      await tweetButton.click();
      await page.waitForTimeout(3000);
      
      console.log('Tweet posted!');
      await page.screenshot({ path: './proof-day2-twitter-SUCCESS.png' });
      
    } else {
      console.log('❌ Login may have failed or verification required');
      await page.screenshot({ path: './debug-login-failed.png' });
    }
    
  } catch (error) {
    console.error('Error during execution:', error);
    if (page) {
      await page.screenshot({ path: './debug-error.png' });
    }
  } finally {
    if (browser) {
      // Keep browser open for verification
      console.log('Keeping browser open for verification...');
      // await browser.close();
    }
  }
})();

console.log('Script completed');