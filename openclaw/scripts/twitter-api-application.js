const puppeteer = require('puppeteer');

async function applyForTwitterAPI() {
  console.log('🐦 Automating Twitter Developer API application...\n');
  
  const browser = await puppeteer.launch({
    headless: false,
    userDataDir: '/home/wls/.config/google-chrome',
    args: ['--profile-directory=Default', '--no-sandbox', '--disable-setuid-sandbox', '--window-size=1920,1080']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  const wait = (ms) => new Promise(r => setTimeout(r, ms));

  try {
    // Navigate to developer portal
    console.log('📱 Navigating to Twitter Developer Portal...');
    await page.goto('https://developer.twitter.com/en/portal/petition/essential/basic-info', { 
      waitUntil: 'networkidle2',
      timeout: 30000 
    });
    
    await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-step1.png' });
    console.log('📸 Step 1: Portal loaded');

    // Wait for page to fully render
    await wait(2000);

    // Click "Continue as" button if present
    const continueBtn = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, a, div[role="button"]'));
      const btn = buttons.find(b => b.innerText && b.innerText.includes('Continue as'));
      if (btn) {
        btn.click();
        return true;
      }
      return false;
    });

    if (continueBtn) {
      console.log('✅ Clicked "Continue as" button');
      await wait(3000);
      await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-step2.png' });
    }

    // Wait for form
    await wait(2000);
    console.log('📝 Checking form elements...');

    // Try to fill visible textareas
    const textareas = await page.$$('textarea');
    console.log(`Found ${textareas.length} textarea(s)`);
    
    for (let i = 0; i < textareas.length; i++) {
      try {
        await textareas[i].click({ delay: 50 });
        await textareas[i].type('Automated content posting and engagement management for AI-powered business systems. Scheduling tweets and monitoring mentions.');
        console.log(`✅ Filled textarea ${i + 1}`);
        await wait(500);
      } catch (e) {
        console.log(`⚠️ Could not fill textarea ${i + 1}`);
      }
    }

    // Click checkboxes for terms
    const checkboxes = await page.$$('input[type="checkbox"]');
    for (const checkbox of checkboxes) {
      try {
        await checkbox.click();
        console.log('✅ Checkbox checked');
        await wait(300);
      } catch (e) {}
    }

    await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-step3.png' });
    console.log('📸 Step 3: Form elements processed');

    // Try to find and click continue/submit buttons
    const buttons = await page.$$('button');
    for (const btn of buttons) {
      try {
        const text = await btn.evaluate(el => el.innerText);
        if (text.includes('Continue') || text.includes('Submit') || text.includes('Next') || text.includes('Apply')) {
          console.log(`✅ Found button: "${text}"`);
          await btn.click();
          await wait(3000);
          await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-step4.png' });
          console.log('📸 Step 4: Button clicked');
          break;
        }
      } catch (e) {}
    }

    // Try to find select dropdowns for country and use case
    const selects = await page.$$('select');
    for (const sel of selects) {
      try {
        const name = await sel.evaluate(el => el.name || el.id || '');
        if (name.toLowerCase().includes('country')) {
          await sel.select('SG');
          console.log('✅ Selected country: Singapore');
        }
        if (name.toLowerCase().includes('use') || name.toLowerCase().includes('case')) {
          await sel.select('business');
          console.log('✅ Selected use case: Business');
        }
      } catch (e) {}
    }

    await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-step5.png' });
    console.log('📸 Step 5: Dropdowns processed');

    // Final submit attempt
    const submitBtns = await page.$$('button');
    for (const btn of submitBtns) {
      try {
        const text = await btn.evaluate(el => el.innerText);
        if (text.toLowerCase().includes('submit') || text.toLowerCase().includes('apply') || text.toLowerCase().includes('create')) {
          console.log(`✅ Clicking final button: "${text}"`);
          await btn.click();
          await wait(3000);
          await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-step6.png' });
        }
      } catch (e) {}
    }

    console.log('\n✅ Automation complete - check browser for results');
    console.log('📸 Screenshots saved to ~/.openclaw/workspace/');
    
    // Keep browser open for 2 minutes
    await wait(120000);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    try {
      await page.screenshot({ path: '/home/wls/.openclaw/workspace/twitter-error.png' });
      console.log('📸 Error screenshot saved');
    } catch (e) {}
    await wait(60000);
  }
}

applyForTwitterAPI();