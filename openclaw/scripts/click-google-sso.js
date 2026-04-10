const puppeteer = require('puppeteer-core');

async function clickGoogleSSO() {
  console.log('🔌 Connecting to Chrome...\n');
  
  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null
    });

    const pages = await browser.pages();
    const page = pages.find(p => p.url().includes('x.com') || p.url().includes('twitter.com'));
    
    if (!page) {
      console.log('❌ No X/Twitter page found');
      return;
    }

    console.log('📱 Current page:', page.url());
    await page.bringToFront();
    await new Promise(r => setTimeout(r, 2000));

    // Take screenshot before
    await page.screenshot({ path: '/home/wls/.openclaw/workspace/x-login-page.png', fullPage: true });
    console.log('📸 Screenshot: x-login-page.png');

    // Look for Google sign-in button
    console.log('\n🔍 Looking for Google SSO button...');
    
    // Get all clickable elements
    const elements = await page.evaluate(() => {
      const results = [];
      
      // Check all buttons
      document.querySelectorAll('button, [role="button"], div[role="button"]').forEach(el => {
        results.push({
          type: 'button',
          text: el.innerText || el.textContent || '',
          ariaLabel: el.getAttribute('aria-label') || '',
          className: el.className || ''
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
      
      // Check for Google icons/buttons
      document.querySelectorAll('[data-testid], [id], [class*="google"], [class*="Google"]').forEach(el => {
        results.push({
          type: 'element',
          tag: el.tagName,
          text: el.innerText || el.textContent || '',
          testId: el.getAttribute('data-testid') || '',
          id: el.id || '',
          className: el.className || ''
        });
      });
      
      return results;
    });

    console.log('\nElements found:');
    for (const el of elements) {
      const text = el.text.toLowerCase();
      if (text.includes('google') || text.includes('sign in') || text.includes('continue') || 
          el.className.includes('google') || el.className.includes('Google')) {
        console.log(`  ${el.type}: "${el.text.substring(0, 50)}"`);
      }
    }

    // Try to find and click Google SSO
    // X.com usually has a "Continue with Google" or "Sign in with Google" button
    const clicked = await page.evaluate(() => {
      // Look for Google sign-in button by text
      const buttons = document.querySelectorAll('button, [role="button"], div[role="button"]');
      for (const btn of buttons) {
        const text = (btn.innerText || '').toLowerCase();
        if (text.includes('google')) {
          console.log('Found Google button:', btn.innerText);
          btn.click();
          return { clicked: true, text: btn.innerText };
        }
      }
      
      // Look for Google icon/SVG
      const googleBtn = document.querySelector('[data-testid="googleButton"], button[onclick*="google"], [class*="google-login"]');
      if (googleBtn) {
        googleBtn.click();
        return { clicked: true, text: 'Google icon button' };
      }
      
      return { clicked: false };
    });

    if (clicked.clicked) {
      console.log(`\n✅ Clicked: "${clicked.text}"`);
      await new Promise(r => setTimeout(r, 3000));
    } else {
      console.log('\n⚠️ No Google button found. Looking for SSO options...');
      
      // Try clicking the Sign in button first
      const signInBtns = await page.$$('button');
      for (const btn of signInBtns) {
        const text = await btn.evaluate(el => el.innerText || '');
        if (text.toLowerCase().includes('sign in') && !text.toLowerCase().includes('apple')) {
          console.log('Clicking sign in button...');
          await btn.click();
          await new Promise(r => setTimeout(r, 2000));
          break;
        }
      }
    }

    await page.screenshot({ path: '/home/wls/.openclaw/workspace/x-after-click.png', fullPage: true });
    console.log('📸 Screenshot: x-after-click.png');

    console.log('\n📱 New URL:', page.url());
    console.log('\nWaiting for you to complete SSO in the Chrome window...');

  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

clickGoogleSSO();