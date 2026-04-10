const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth');

// Apply stealth plugin
chromium.use(stealth);

(async () => {
  console.log('[STEALTH] Launching browser with anti-detection...');
  
  const browser = await chromium.launch({
    headless: true,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-web-security',
      '--disable-features=IsolateOrigins,site-per-process',
      '--no-sandbox',
      '--disable-dev-shm-usage'
    ]
  });
  
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    locale: 'en-US',
    timezoneId: 'Asia/Singapore'
  });
  
  const page = await context.newPage();
  
  console.log('[STEALTH] Navigating to Twitter login...');
  await page.goto('https://x.com/login', { waitUntil: 'domcontentloaded' });
  
  // Wait for page to stabilize
  await page.waitForTimeout(3000);
  
  // Take screenshot
  await page.screenshot({ path: '/home/wls/.openclaw/workspace/content/stealth-login-1.png', fullPage: true });
  console.log('[STEALTH] Screenshot saved: stealth-login-1.png');
  
  // Check page content
  const pageContent = await page.evaluate(() => document.body.innerText);
  const pageTitle = await page.title();
  
  console.log('[STEALTH] Page title:', pageTitle);
  console.log('[STEALTH] Page content preview:', pageContent.substring(0, 500));
  
  // Try multiple selectors for login
  const selectors = [
    'input[name="text"]',
    'input[autocomplete="username"]',
    'input[type="text"]',
    '[data-testid="ocf_challenge"]',
    '[data-testid="LoginForm"]',
    'div[lang] span' // Any visible text
  ];
  
  for (const sel of selectors) {
    const el = await page.$(sel);
    if (el) {
      console.log(`[STEALTH] Found: ${sel}`);
    }
  }
  
  // Check if redirected to challenge or error
  if (pageContent.includes('challenge') || pageContent.includes('automated') || pageContent.includes('blocked')) {
    console.log('[STEALTH] ❌ BOT DETECTION INDICATED');
    await page.screenshot({ path: '/home/wls/.openclaw/workspace/content/stealth-bot-detected.png', fullPage: true });
  }
  
  // Try direct URL to i/flow/login
  console.log('[STEALTH] Trying alternate login URL...');
  await page.goto('https://x.com/i/flow/login', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/home/wls/.openclaw/workspace/content/stealth-login-2.png', fullPage: true });
  
  const flowContent = await page.evaluate(() => document.body.innerText);
  console.log('[STEALTH] Flow page preview:', flowContent.substring(0, 500));
  
  // Check for login input in flow
  const flowInput = await page.$('input[name="text"], input[type="text"], input[autocomplete="username"]');
  if (flowInput) {
    console.log('[STEALTH] ✅ Login input found in flow page');
    
    // Get the actual HTML structure
    const html = await page.evaluate(() => document.body.innerHTML.substring(0, 2000));
    console.log('[STEALTH] HTML preview:', html);
  } else {
    console.log('[STEALTH] ❌ No login input found');
  }
  
  await browser.close();
  console.log('[STEALTH] Test complete');
})();