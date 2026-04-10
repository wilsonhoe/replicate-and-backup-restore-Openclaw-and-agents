const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('https://news.yahoo.com', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/tmp/yahoo_news.png', fullPage: true });
  const headlines = await page.$$eval('h3 a', anchors =>
    anchors.slice(0,5).map(a => a.innerText.trim()).filter(t => t.length > 10)
  );
  console.log('Top Yahoo News:');
  headlines.forEach((h, i) => console.log(`${i+1}. ${h}`));
  await browser.close();
})().catch(console.error);