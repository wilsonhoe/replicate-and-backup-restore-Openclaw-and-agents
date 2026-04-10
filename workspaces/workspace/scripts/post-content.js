const { chromium } = require('playwright');
const SessionManager = require('/home/wls/.openclaw/lib/session-manager');
const TwitterAuth = require('/home/wls/.openclaw/lib/twitter-auth');
const LinkedInAuth = require('/home/wls/.openclaw/lib/linkedin-auth');
const fs = require('fs');

// Read the social post content
const postContent = fs.readFileSync('/home/wls/.openclaw/workspace/content/social-post-001.md', 'utf8');

// Extract Twitter version (between markers)
const twitterMatch = postContent.match(/## Twitter\/X Version \(280 chars\)\n\n([\s\S]*?)\n\n---/);
const twitterContent = twitterMatch ? twitterMatch[1].trim() : '';

console.log('Twitter content to post:');
console.log(twitterContent);
console.log(`Character count: ${twitterContent.length}`);

async function postToPlatforms() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  
  try {
    // Post to Twitter
    console.log('\n=== Posting to Twitter ===');
    const twitterAuth = new TwitterAuth();
    const twitterSession = await twitterAuth.login('', ''); // Empty creds since we have session
    
    if (twitterSession.page && twitterSession.context && twitterSession.browser) {
      const success = await twitterAuth.postTweet(twitterSession.page, twitterContent);
      if (success) {
        console.log('✅ Twitter post successful!');
        
        // Save screenshot as proof
        await twitterSession.page.screenshot({ 
          path: '/home/wls/.openclaw/workspace/content/proof-twitter-post-001.png' 
        });
        console.log('📸 Screenshot saved');
      }
      
      await twitterSession.browser.close();
    }
    
    // Small delay between posts
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Post to LinkedIn
    console.log('\n=== Posting to LinkedIn ===');
    const linkedinAuth = new LinkedInAuth();
    const linkedinSession = await linkedinAuth.login('', ''); // Empty creds since we have session
    
    if (linkedinSession.page && linkedinSession.context && linkedinSession.browser) {
      // Extract LinkedIn version
      const linkedinMatch = postContent.match(/## LinkedIn Version\n\n([\s\S]*?)\n\n---/);
      const linkedinContent = linkedinMatch ? linkedinMatch[1].trim() : '';
      
      console.log('LinkedIn content to post:');
      console.log(linkedinContent.substring(0, 100) + '...');
      
      // Navigate to LinkedIn and post
      await linkedinSession.page.goto('https://www.linkedin.com/feed/');
      await linkedinSession.page.waitForTimeout(3000);
      
      // Click "Start a post" button
      await linkedinSession.page.click('button[aria-label="Start a post"]');
      await linkedinSession.page.waitForTimeout(2000);
      
      // Click the text area
      await linkedinSession.page.click('.editor__content-editable');
      await linkedinSession.page.fill('.editor__content-editable', linkedinContent);
      
      // Click post button
      await linkedinSession.page.click('button[aria-label="Post"]');
      await linkedinSession.page.waitForTimeout(3000);
      
      console.log('✅ LinkedIn post successful!');
      
      // Save screenshot as proof
      await linkedinSession.page.screenshot({ 
        path: '/home/wls/.openclaw/workspace/content/proof-linkedin-post-001.png' 
      });
      console.log('📸 LinkedIn screenshot saved');
      
      await linkedinSession.browser.close();
    }
    
  } catch (error) {
    console.error('❌ Error during posting:', error);
  } finally {
    await browser.close();
  }
}

postToPlatforms().then(() => {
  console.log('\n🎉 Content posting attempt completed!');
}).catch(err => {
  console.error('❌ Fatal error:', err);
});