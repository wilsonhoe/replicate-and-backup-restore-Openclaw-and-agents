const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://bbc.com/news', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/tmp/bbc_news.png', fullPage: true });
  const headlines = await page.$$eval('h3', hs => hs.slice(0,5).map(h => h.innerText.trim()).filter(t => t.length > 10));
  console.log('Top BBC News:');
  headlines.forEach((h, i) => console.log(`${i+1}. ${h}`));
  await browser.close();
})().catch(e => console.error(e));