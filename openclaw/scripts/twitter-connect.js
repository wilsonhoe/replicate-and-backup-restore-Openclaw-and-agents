const puppeteer = require('puppeteer-core');

async function connectToChrome() {
  console.log('🔌 Connecting to Google Chrome...\n');
  
  try {
    // Connect to Chrome DevTools
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:9222',
      defaultViewport: null
    });

    console.log('✅ Connected to Google Chrome');

    const pages = await browser.pages();
    console.log(`Found ${pages.length} tabs`);

    // Find Twitter page
    let page = pages.find(p => p.url().includes('twitter.com'));
    
    if (!page) {
      page = await browser.newPage();
      await page.goto('https://developer.twitter.com/en/portal/petition/essential/basic-info');
    }

    console.log('📱 Page URL:', page.url());

    // Wait for page
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-connected.png' });
    console.log('📸 Screenshot saved');

    // Get page info
    const title = await page.title();
    console.log('📄 Title:', title);

    // Look for form elements
    const elements = await page.evaluate(() => {
      return {
        inputs: document.querySelectorAll('input').length,
        textareas: document.querySelectorAll('textarea').length,
        selects: document.querySelectorAll('select').length,
        buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(b => b)
      };
    });
    
    console.log('\n📋 Form elements found:', elements);

    // Keep connection alive
    console.log('\n👀 Browser is open. Complete the application manually.');
    console.log('I can see and interact with the page.');

  } catch (error) {
    console.error('❌ Error:', error.message);
    console.log('\nChrome must be running with debugging port:');
    console.log('google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.config/google-chrome"');
  }
}

connectToChrome();