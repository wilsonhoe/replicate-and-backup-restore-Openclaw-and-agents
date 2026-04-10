// Corrected Cookie Import Playwright Script
// Uses actual cookie file paths from browser-data directory
const { chromium } = require('playwright');
const fs = require('fs');

// Function to load content from file
function loadContent(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

(async () => {
  let twitterPage;
  let linkedinPage;
  let browser;

  try {
    console.log('Starting cookie-based posting with corrected paths...');

    // Load Day 2 content
    const twitterContent = loadContent('./content/social-post-002.md').split('---\n')[2].trim();
    const linkedinContent = loadContent('./content/social-post-002.md').split('---\n')[4].trim();

    console.log('Twitter content:', twitterContent.substring(0, 100) + '...');
    console.log('LinkedIn content:', linkedinContent.substring(0, 100) + '...');

    // Launch browser with cookie context
    browser = await chromium.launch({ headless: false }); // Set to false for debugging
    const context = await browser.newContext();
    
    // Import Twitter cookies from correct path
    const twitterCookiePath = '/home/wls/.openclaw/browser-data/cookies.json';
    if (fs.existsSync(twitterCookiePath)) {
      const twitterCookies = JSON.parse(fs.readFileSync(twitterCookiePath));
      await context.addCookies(twitterCookies);
      console.log('Twitter cookies imported successfully from:', twitterCookiePath);
    } else {
      console.log('Twitter cookies not found at:', twitterCookiePath);
      console.log('Attempting manual login...');
    }
    
    // Post to Twitter
    twitterPage = await context.newPage();
    console.log('Navigating to Twitter...');
    await twitterPage.goto('https://x.com');
    await twitterPage.waitForTimeout(3000);
    console.log('Current URL after x.com:', await twitterPage.url());
    
    // Check if we're logged in
    const isLoggedIn = await twitterPage.locator('[data-testid="SideNav_AccountSwitcher_Button"]').count() > 0;
    console.log('Twitter login status:', isLoggedIn ? 'LOGGED IN' : 'NOT LOGGED IN');
    
    if (!isLoggedIn) {
      console.log('Need to handle login - stopping for now');
      await twitterPage.screenshot({ path: './debug-twitter-not-logged-in.png' });
      return;
    }
    
    await twitterPage.screenshot({ path: './debug-twitter-home.png' });
    
    // Navigate to compose tweet
    console.log('Navigating to compose tweet...');
    await twitterPage.goto('https://x.com/compose/tweet');
    await twitterPage.waitForTimeout(3000);
    console.log('Current URL after compose:', await twitterPage.url());
    await twitterPage.screenshot({ path: './debug-twitter-compose.png' });
    
    // Wait for textarea
    await twitterPage.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });

    // Method 1: Focus and type character by character (most natural for React)
    console.log('Entering tweet content using character-by-character typing...');
    const textarea = twitterPage.locator('[data-testid="tweetTextarea_0"]').first();
    await textarea.click();
    await twitterPage.waitForTimeout(500);

    // Clear any existing content
    await twitterPage.keyboard.press('Control+a');
    await twitterPage.keyboard.press('Delete');
    await twitterPage.waitForTimeout(300);

    // Type character by character to trigger React state updates
    for (let i = 0; i < twitterContent.length; i++) {
      await twitterPage.keyboard.type(twitterContent[i]);
      await twitterPage.waitForTimeout(50); // Small delay between characters
    }
    
    await twitterPage.waitForTimeout(1000);
    console.log('Content entered, checking button state...');
    
    // Check if tweet button is enabled
    const tweetButton = twitterPage.locator('[data-testid="tweetButtonInline"]');
    const isDisabled = await tweetButton.getAttribute('aria-disabled') === 'true';
    console.log('Tweet button disabled:', isDisabled);
    
    if (!isDisabled) {
      console.log('Clicking tweet button...');
      await tweetButton.click();
      await twitterPage.waitForTimeout(3000);
      console.log('Tweet posted!');
      await twitterPage.screenshot({ path: './proof-day2-twitter.png' });
    } else {
      console.log('Button still disabled, trying fallback method...');
      
      // Method 2: Try execCommand approach
      await twitterPage.evaluate((text) => {
        const textarea = document.querySelector('[data-testid="tweetTextarea_0"]');
        if (textarea) {
          textarea.focus();
          document.execCommand('insertText', false, text);
          
          // Trigger input events
          const inputEvent = new Event('input', { bubbles: true });
          const changeEvent = new Event('change', { bubbles: true });
          textarea.dispatchEvent(inputEvent);
          textarea.dispatchEvent(changeEvent);
        }
      }, twitterContent);
      
      await twitterPage.waitForTimeout(1000);
      
      // Check button again
      const isStillDisabled = await tweetButton.getAttribute('aria-disabled') === 'true';
      if (!isStillDisabled) {
        console.log('Fallback worked! Clicking tweet button...');
        await tweetButton.click();
        await twitterPage.waitForTimeout(3000);
        console.log('Tweet posted with fallback method!');
        await twitterPage.screenshot({ path: './proof-day2-twitter-fallback.png' });
      } else {
        console.log('Both methods failed, taking debug screenshot...');
        await twitterPage.screenshot({ path: './debug-twitter-failed.png' });
      }
    }

    // LinkedIn posting
    console.log('Starting LinkedIn posting...');
    const linkedinContext = await browser.newContext();
    
    // Import LinkedIn cookies
    const linkedinCookiePath = '/home/wls/.openclaw/browser-data-linkedin/cookies.json';
    if (fs.existsSync(linkedinCookiePath)) {
      const linkedinCookies = JSON.parse(fs.readFileSync(linkedinCookiePath));
      await linkedinContext.addCookies(linkedinCookies);
      console.log('LinkedIn cookies imported successfully');
    }
    
    linkedinPage = await linkedinContext.newPage();
    await linkedinPage.goto('https://linkedin.com');
    await linkedinPage.waitForTimeout(3000);
    
    // Check LinkedIn login status
    const linkedinLoggedIn = await linkedinPage.locator('[data-testid="nav-profile-photo"]').count() > 0;
    console.log('LinkedIn login status:', linkedinLoggedIn ? 'LOGGED IN' : 'NOT LOGGED IN');
    
    if (linkedinLoggedIn) {
      console.log('Posting to LinkedIn...');
      // Navigate to LinkedIn post creation
      await linkedinPage.goto('https://www.linkedin.com/feed/');
      await linkedinPage.waitForTimeout(2000);
      
      // Click on start a post
      const startPostButton = linkedinPage.locator('[data-testid="share-box-toggle"]');
      if (await startPostButton.count() > 0) {
        await startPostButton.click();
        await linkedinPage.waitForTimeout(1000);
        
        // Find the contenteditable div
        const contentEditable = linkedinPage.locator('[contenteditable="true"]').first();
        await contentEditable.click();
        await linkedinPage.waitForTimeout(500);
        
        // Type the content
        await linkedinPage.keyboard.type(linkedinContent);
        await linkedinPage.waitForTimeout(1000);
        
        // Find and click post button using coordinate method
        const postButton = linkedinPage.locator('[data-testid="share-action"]').first();
        const box = await postButton.boundingBox();
        if (box) {
          await linkedinPage.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
          console.log('LinkedIn post submitted!');
          await linkedinPage.waitForTimeout(3000);
          await linkedinPage.screenshot({ path: './proof-day2-linkedin.png' });
        }
      }
    }

    console.log('Posting complete!');
    
  } catch (error) {
    console.error('Error during posting:', error);
    if (twitterPage) {
      await twitterPage.screenshot({ path: './debug-error-twitter.png' });
    }
  } finally {
    if (browser) {
      await browser.close();
    }
  }
})();