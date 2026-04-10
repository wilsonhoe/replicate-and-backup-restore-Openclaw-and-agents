const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://news.yahoo.com', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);
  await page.screenshot({ path: '/tmp/yahoo_news.png', fullPage: true });
  const headlines = await page.$$eval('h3 a, [data-test-locator="headline"] a', els =>
    els.slice(0,5).map(e => e.innerText.trim()).filter(t => t.length > 15)
  );
  console.log('Top Yahoo News:');
  headlines.forEach((h, i) => console.log(`${i+1}. ${h}`));
  await browser.close();
})().catch(e => console.error(e));