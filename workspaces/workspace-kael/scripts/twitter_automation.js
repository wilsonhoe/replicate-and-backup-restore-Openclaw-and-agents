#!/usr/bin/env node
/**
 * Self-hosted Twitter Automation Script
 * Uses Playwright for browser automation
 * 
 * Usage: node twitter_automation.js [tweet_text_file]
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Credentials from TOOLS.md
const TWITTER_USERNAME = 'LisaLLM83';
const TWITTER_PASSWORD = '%LvZ%;g9Z$79+q9';
const TWITTER_EMAIL = 'lisamolbot@gmail.com';

// Configuration
const USER_DATA_DIR = path.join(process.env.HOME, '.twitter_automation_data');
const COOKIES_FILE = path.join(USER_DATA_DIR, 'twitter_cookies.json');

async function ensureDirectory() {
    if (!fs.existsSync(USER_DATA_DIR)) {
        fs.mkdirSync(USER_DATA_DIR, { recursive: true });
    }
}

async function saveCookies(page) {
    const cookies = await page.context().cookies();
    fs.writeFileSync(COOKIES_FILE, JSON.stringify(cookies, null, 2));
    console.log('[INFO] Cookies saved');
}

async function loadCookies(context) {
    if (fs.existsSync(COOKIES_FILE)) {
        const cookies = JSON.parse(fs.readFileSync(COOKIES_FILE, 'utf8'));
        await context.addCookies(cookies);
        console.log('[INFO] Cookies loaded');
        return true;
    }
    return false;
}

async function isLoggedIn(page) {
    try {
        // Check for profile menu or compose button
        const composeBtn = await page.locator('a[href="/compose/tweet"], [data-testid="SideNav_NewTweet_Button"]').first();
        const isVisible = await composeBtn.isVisible({ timeout: 5000 }).catch(() => false);
        return isVisible;
    } catch {
        return false;
    }
}

async function login(page) {
    console.log('[INFO] Navigating to Twitter login...');
    await page.goto('https://twitter.com/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(3000);
    
    // Check if already logged in via cookies
    if (await isLoggedIn(page)) {
        console.log('[INFO] Already logged in');
        return true;
    }
    
    console.log('[INFO] Waiting for login form...');
    await page.waitForSelector('input[name="text"]', { timeout: 30000 });
    
    console.log('[INFO] Entering username...');
    await page.fill('input[name="text"]', TWITTER_USERNAME);
    await page.waitForTimeout(1000);
    
    console.log('[INFO] Clicking Next...');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(2000);
    
    // Check for password field
    const passwordField = await page.locator('input[name="password"]').isVisible({ timeout: 5000 }).catch(() => false);
    if (!passwordField) {
        // Might need email/phone verification
        const phoneField = await page.locator('input[name="text"]').first().isVisible({ timeout: 5000 }).catch(() => false);
        if (phoneField) {
            console.log('[INFO] Entering email...');
            await page.fill('input[name="text"]', TWITTER_EMAIL);
            await page.keyboard.press('Enter');
            await page.waitForTimeout(2000);
        }
    }
    
    console.log('[INFO] Waiting for password field...');
    await page.waitForSelector('input[name="password"]', { timeout: 30000 });
    
    console.log('[INFO] Entering password...');
    await page.fill('input[name="password"]', TWITTER_PASSWORD);
    await page.waitForTimeout(1000);
    
    console.log('[INFO] Clicking Log in...');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(5000);
    
    // Check for 2FA / verification
    const verifyVisible = await page.locator('text=Enter your verification code, text=Confirm your identity').isVisible({ timeout: 10000 }).catch(() => false);
    if (verifyVisible) {
        console.error('[ERROR] 2FA/Verification required. Manual intervention needed.');
        console.error('[PAUSED] Complete login manually in the browser window...');
        await page.waitForTimeout(120000); // Wait 2 minutes for manual input
    }
    
    // Check if logged in
    const loggedIn = await isLoggedIn(page);
    if (loggedIn) {
        console.log('[SUCCESS] Logged in successfully');
        await saveCookies(page);
        return true;
    } else {
        console.error('[ERROR] Login failed - taking screenshot');
        await page.screenshot({ path: '/tmp/twitter_login_fail.png' });
        return false;
    }
}

async function postTweet(page, text) {
    console.log('[INFO] Opening compose dialog...');
    
    // Click compose button
    const composeBtn = await page.locator('a[href="/compose/tweet"], [data-testid="SideNav_NewTweet_Button"]').first();
    await composeBtn.click();
    
    await page.waitForTimeout(1000);
    
    // Find and fill tweet text box
    console.log('[INFO] Typing tweet...');
    const tweetBox = await page.locator('[data-testid="tweetTextarea_0"], div[role="textbox"][contenteditable="true"]').first();
    await tweetBox.fill(text);
    
    await page.waitForTimeout(500);
    
    // Click post button
    console.log('[INFO] Clicking post button...');
    const postBtn = await page.locator('button[data-testid="tweetButton"], button:has-text("Post")').first();
    await postBtn.click();
    
    // Wait for post to complete
    await page.waitForTimeout(3000);
    
    console.log('[SUCCESS] Tweet posted');
    return true;
}

async function main() {
    // Get tweet text from file or arguments
    let tweetText = '';
    
    if (process.argv[2] && fs.existsSync(process.argv[2])) {
        tweetText = fs.readFileSync(process.argv[2], 'utf8').trim();
    } else if (process.argv[2]) {
        tweetText = process.argv.slice(2).join(' ');
    } else {
        // Default tweets if no input
        console.log('[INFO] Usage: node twitter_automation.js [tweet_text_file]');
        console.log('[INFO] Using default test tweet');
        tweetText = "Testing automation from a self-hosted script. Building systems that scale. #AI #Automation";
    }
    
    if (tweetText.length > 280) {
        console.error('[ERROR] Tweet exceeds 280 characters');
        process.exit(1);
    }
    
    console.log('[START] Twitter Automation Script');
    console.log(`[INFO] Tweet length: ${tweetText.length} chars`);
    await ensureDirectory();
    
    let browser;
    let context;
    let page;
    
    try {
        // Launch browser with persistent context
        console.log('[INFO] Launching browser...');
        browser = await chromium.launch({ 
            headless: false,  // Visible browser for debugging
            slowMo: 1000,     // Slow down for visibility
            args: [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ]
        });
        
        context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport: { width: 1280, height: 800 }
        });
        
        // Load cookies if they exist
        await loadCookies(context);
        
        page = await context.newPage();
        
        // Login (or use existing session)
        const loggedIn = await login(page);
        if (!loggedIn) {
            throw new Error('Failed to login');
        }
        
        // Post tweet
        await postTweet(page, tweetText);
        
        // Save updated cookies
        await saveCookies(page);
        
        console.log('[SUCCESS] Automation complete');
        
        // Wait a bit before closing
        await page.waitForTimeout(3000);
        
    } catch (error) {
        console.error('[ERROR]', error.message);
        console.error('[FAIL] Automation failed');
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

main();
