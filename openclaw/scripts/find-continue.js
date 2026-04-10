const puppeteer = require('puppeteer-core');

async function findAndClickContinue() {
  console.log('🔌 Connecting to Chrome...\n');
  
  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null
    });

    const pages = await browser.pages();
    console.log(`Found ${pages.length} tabs\n`);

    // Check all pages for "Continue as" button
    for (const page of pages) {
      const url = page.url();
      console.log(`Checking: ${url.substring(0, 80)}...`);
      
      try {
        await page.bringToFront();
        await new Promise(r => setTimeout(r, 1000));
        
        // Get all clickable elements
        const elements = await page.evaluate(() => {
          const results = [];
          
          // Check all buttons
          document.querySelectorAll('button, [role="button"], input[type="button"], input[type="submit"]').forEach(el => {
            results.push({
              type: 'button',
              text: el.innerText || el.textContent || el.value || '',
              tag: el.tagName
            });
          });
          
          // Check links
          document.querySelectorAll('a').forEach(el => {
            results.push({
              type: 'link',
              text: el.innerText || el.textContent || '',
              href: el.href || ''
            });
          });
          
          // Check divs with click handlers
          document.querySelectorAll('div[onclick], div[role="button"], span[role="button"]').forEach(el => {
            results.push({
              type: 'div',
              text: el.innerText || el.textContent || ''
            });
          });
          
          return results;
        });
        
        for (const el of elements) {
          const text = el.text.toLowerCase();
          if (text.includes('continue') || text.includes('lisa') || text.includes('sign in')) {
            console.log(`  ✅ Found: "${el.text.substring(0, 50)}" (${el.type})`);
          }
        }
        
      } catch (e) {
        console.log(`  Skip (chrome:// or restricted)`);
      }
    }

    // Try the X.com login page
    const xPage = pages.find(p => p.url().includes('x.com') || p.url().includes('twitter.com'));
    if (xPage) {
      console.log('\n📱 Bringing X page to front...');
      await xPage.bringToFront();
      await new Promise(r => setTimeout(r, 2000));
      await xPage.screenshot({ path: '/home/wls/.openclaw/workspace/x-page.png' });
      console.log('📸 Screenshot: x-page.png');
    }

    // Try the Google sign-in page
    const gPage = pages.find(p => p.url().includes('accounts.google.com') && !p.url().includes('RotateCookies'));
    if (gPage) {
      console.log('\n📱 Bringing Google sign-in page to front...');
      await gPage.bringToFront();
      await new Promise(r => setTimeout(r, 2000));
      
      // Click any "Continue as" button
      const clicked = await gPage.evaluate(() => {
        const buttons = document.querySelectorAll('button, [role="button"], div[role="button"]');
        for (const btn of buttons) {
          const text = (btn.innerText || '').toLowerCase();
          if (text.includes('continue') && text.includes('lisa')) {
            btn.click();
            return btn.innerText;
          }
        }
        return null;
      });
      
      if (clicked) {
        console.log(`✅ Clicked: "${clicked}"`);
        await new Promise(r => setTimeout(r, 3000));
      }
      
      await gPage.screenshot({ path: '/home/wls/.openclaw/workspace/google-page.png' });
      console.log('📸 Screenshot: google-page.png');
    }

    console.log('\n📱 Current URLs after interaction:');
    for (const page of pages) {
      console.log(`  ${page.url().substring(0, 100)}`);
    }

  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

findAndClickContinue();