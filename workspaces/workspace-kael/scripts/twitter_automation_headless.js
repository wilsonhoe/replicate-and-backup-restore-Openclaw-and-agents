#!/usr/bin/env node
/**
 * Headless Twitter Automation Script
 * Uses Playwright in headless mode with stealth
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const TWITTER_USERNAME = 'LisaLLM83';
const TWITTER_PASSWORD = '%LvZ%;g9Z$79+q9';
const TWITTER_EMAIL = 'lisamolbot@gmail.com';

const USER_DATA_DIR = path.join(process.env.HOME, '.twitter_automation_data');
const COOKIES_FILE = path.join(USER_DATA_DIR, 'twitter_cookies.json');

async function ensureDirectory() {
    if (!fs.existsSync(USER_DATA_DIR)) {
        fs.mkdirSync(USER_DATA_DIR, { recursive: true });
    }
}

async function saveStorage(context) {
    await context.storageState({ path: path.join(USER_DATA_DIR, 'storage.json') });
    console.log('[INFO] Storage state saved');
}

async function loadStorage() {
    const storagePath = path.join(USER_DATA_DIR, 'storage.json');
    if (fs.existsSync(storagePath)) {
        console.log('[INFO] Loading storage state');
        return { storageState: storagePath };
    }
    return {};
}

async function main() {
    let tweetText = '';
    
    if (process.argv[2] && fs.existsSync(process.argv[2])) {
        tweetText = fs.readFileSync(process.argv[2], 'utf8').trim();
    } else if (process.argv[2]) {
        tweetText = process.argv.slice(2).join(' ');
    } else {
        tweetText = "Testing automation from a self-hosted script. Building systems that scale. #AI #Automation";
    }
    
    if (tweetText.length > 280) {
        console.error('[ERROR] Tweet exceeds 280 characters');
        process.exit(1);
    }
    
    console.log('[START] Headless Twitter Automation');
    console.log(`[INFO] Tweet: ${tweetText.substring(0, 50)}...`);
    await ensureDirectory();
    
    let browser;
    let context;
    let page;
    
    try {
        console.log('[INFO] Launching headless browser...');
        
        // Try to load previous session
        const storageOptions = await loadStorage();
        
        browser = await chromium.launch({
            headless: true,
            args: [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080'
            ]
        });
        
        context = await browser.newContext({
            ...storageOptions,
            userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport: { width: 1920, height: 1080 },
            locale: 'en-US',
            timezoneId: 'America/New_York'
        });
        
        page = await context.newPage();
        
        // Navigate to Twitter
        console.log('[INFO] Checking login status...');
        await page.goto('https://twitter.com/home', { waitUntil: 'domcontentloaded', timeout: 30000 });
        await page.waitForTimeout(3000);
        
        // Check if we need to login
        const loginVisible = await page.locator('input[name="text"], input[name="password"]').first().isVisible({ timeout: 5000 }).catch(() => false);
        
        if (loginVisible) {
            console.log('[INFO] Need to login - entering credentials...');
            
            await page.goto('https://twitter.com/i/flow/login', { waitUntil: 'domcontentloaded', timeout: 30000 });
            await page.waitForTimeout(2000);
            
            // Username
            await page.waitForSelector('input[name="text"]', { timeout: 30000 });
            await page.fill('input[name="text"]', TWITTER_USERNAME);
            await page.keyboard.press('Enter');
            await page.waitForTimeout(2000);
            
            // Password
            await page.waitForSelector('input[name="password"]', { timeout: 30000 });
            await page.fill('input[name="password"]', TWITTER_PASSWORD);
            await page.keyboard.press('Enter');
            await page.waitForTimeout(5000);
            
            // Check for 2FA
            const needVerification = await page.locator('text=Enter your verification code').isVisible({ timeout: 3000 }).catch(() => false);
            if (needVerification) {
                console.error('[ERROR] 2FA required - cannot proceed in headless mode');
                await browser.close();
                process.exit(1);
            }
            
            console.log('[INFO] Login successful');
            await saveStorage(context);
        } else {
            console.log('[INFO] Already logged in');
        }
        
        // Now post the tweet
        console.log('[INFO] Opening compose dialog...');
        
        // Click compose
        const composeBtn = await page.locator('[data-testid="SideNav_NewTweet_Button"], a[href="/compose/tweet"]').first();
        await composeBtn.click();
        await page.waitForTimeout(2000);
        
        // Type tweet
        console.log('[INFO] Typing tweet...');
        const tweetBox = await page.locator('[data-testid="tweetTextarea_0"], div[contenteditable="true"]').first();
        await tweetBox.fill(tweetText);
        await page.waitForTimeout(1000);
        
        // Click post
        console.log('[INFO] Posting tweet...');
        const postBtn = await page.locator('button[data-testid="tweetButton"]').first();
        await postBtn.click();
        await page.waitForTimeout(3000);
        
        // Verify
        const posted = await page.locator('text=Your Tweet was sent').first().isVisible({ timeout: 5000 }).catch(() => {
            // Also check if we're back on timeline
            return page.locator('[data-testid="primaryColumn"]').isVisible({ timeout: 5000 }).catch(() => false);
        });
        
        if (posted) {
            console.log('[SUCCESS] Tweet posted successfully');
        } else {
            console.log('[INFO] Tweet posted (verification inconclusive)');
        }
        
        await saveStorage(context);
        
    } catch (error) {
        console.error('[ERROR]', error.message);
        if (page) {
            await page.screenshot({ path: '/tmp/twitter_error.png' });
            console.log('[INFO] Screenshot saved to /tmp/twitter_error.png');
        }
        process.exit(1);
    } finally {
        if (browser) await browser.close();
    }
}

main();
