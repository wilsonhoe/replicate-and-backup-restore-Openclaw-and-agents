const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth');
const sessionManager = require('/home/wls/.openclaw/lib/session-manager.js');
const fs = require('fs').promises;
const path = require('path');

// Use stealth plugin
chromium.use(stealth());

class BBBrowserStyle {
  constructor() {
    this.browser = null;
    this.context = null;
    this.page = null;
    this.sessionManager = new sessionManager();
  }

  async launch(options = {}) {
    const defaultOptions = {
      headless: false, // bb-browser style - visible browser
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-features=IsolateOrigins,site-per-process',
        '--disable-site-isolation-trials',
        '--disable-web-security',
        '--disable-features=BlockInsecurePrivateNetworkRequests',
        '--disable-features=OutOfBlinkCors',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--no-zygote',
        '--disable-gpu',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-renderer-backgrounding'
      ],
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    };

    const launchOptions = { ...defaultOptions, ...options };
    
    this.browser = await chromium.launch(launchOptions);
    this.context = await this.browser.newContext({
      viewport: launchOptions.viewport,
      userAgent: launchOptions.userAgent
    });
    
    this.page = await this.context.newPage();
    
    // bb-browser style - human-like behavior
    await this.humanizePage();
    
    return { browser: this.browser, context: this.context, page: this.page };
  }

  async humanizePage() {
    // Inject human-like properties
    await this.page.evaluateOnNewDocument(() => {
      // Override navigator properties
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
      });
      
      // Add realistic plugins
      Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
      });
      
      // Add realistic languages
      Object.defineProperty(navigator, 'languages', {
        get: () => ['en-US', 'en'],
      });
      
      // Override permissions
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
          Promise.resolve({ state: Notification.permission }) :
          originalQuery(parameters)
      );
    });
  }

  async loadSession(platform) {
    return await this.sessionManager.loadSession(platform, this.context);
  }

  async saveSession(platform) {
    return await this.sessionManager.saveSession(platform, this.page);
  }

  async goto(url, options = {}) {
    return await this.page.goto(url, { 
      waitUntil: 'networkidle',
      timeout: 30000,
      ...options 
    });
  }

  async click(selector, options = {}) {
    // bb-browser style - human-like clicking
    const element = await this.page.locator(selector);
    await element.scrollIntoViewIfNeeded();
    await this.page.waitForTimeout(Math.random() * 1000 + 500); // Random delay
    await element.click({ 
      delay: Math.random() * 100 + 50,
      ...options 
    });
  }

  async type(selector, text, options = {}) {
    // bb-browser style - human-like typing
    await this.click(selector);
    await this.page.waitForTimeout(Math.random() * 500 + 300);
    
    // Type with human-like speed
    for (const char of text) {
      await this.page.type(selector, char, { delay: Math.random() * 100 + 50 });
    }
  }

  async waitForSelector(selector, options = {}) {
    return await this.page.waitForSelector(selector, { 
      timeout: 10000,
      ...options 
    });
  }

  async screenshot(options = {}) {
    return await this.page.screenshot({ 
      fullPage: true,
      ...options 
    });
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

// Export for use
module.exports = BBBrowserStyle;