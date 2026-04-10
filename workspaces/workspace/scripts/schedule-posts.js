#!/usr/bin/env node
/**
 * Schedule Posts - Automated Content Distribution Scheduler
 * 
 * Reads content from content calendar and schedules posts at optimal times.
 * Uses saved browser sessions for Twitter and LinkedIn automation.
 * 
 * Usage: node schedule-posts.js [--dry-run] [--day=N]
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  browserData: {
    twitter: '/home/wls/.openclaw/browser-data',
    linkedin: '/home/wls/.openclaw/browser-data-linkedin'
  },
  contentDir: '/home/wls/.openclaw/workspace/content',
  logsDir: '/home/wls/.openclaw/workspace/logs',
  schedule: {
    // SGT times (UTC+8)
    morning: { hour: 8, minute: 0 },   // 8 AM SGT
    midday: { hour: 12, minute: 0 },    // 12 PM SGT
    evening: { hour: 18, minute: 0 }    // 6 PM SGT
  }
};

// Ensure logs directory exists
if (!fs.existsSync(CONFIG.logsDir)) {
  fs.mkdirSync(CONFIG.logsDir, { recursive: true });
}

/**
 * Parse content calendar file
 */
function parseContentCalendar(calendarPath) {
  const content = fs.readFileSync(calendarPath, 'utf-8');
  const days = [];
  
  // Extract day content using regex
  const dayRegex = /## Day (\d+).*?\*\*Twitter:\*\*(.+?)\*\*LinkedIn:\*\*(.+?)(?=## Day|\*\*Image|$)/gs;
  let match;
  
  while ((match = dayRegex.exec(content)) !== null) {
    days.push({
      day: parseInt(match[1]),
      twitter: match[2].trim(),
      linkedin: match[3].trim()
    });
  }
  
  return days;
}

/**
 * Load content for specific day
 */
function loadDayContent(day) {
  const contentFiles = fs.readdirSync(CONFIG.contentDir);
  const dayFile = contentFiles.find(f => f.includes(`post-${day.toString().padStart(3, '0')}`) || f.includes(`social-post-${day.toString().padStart(3, '0')}`));
  
  if (!dayFile) {
    // Try to read from calendar
    const calendarPath = path.join(CONFIG.contentDir, 'content-calendar-001.md');
    if (fs.existsSync(calendarPath)) {
      const days = parseContentCalendar(calendarPath);
      return days.find(d => d.day === day);
    }
  }
  
  if (dayFile) {
    const content = fs.readFileSync(path.join(CONFIG.contentDir, dayFile), 'utf-8');
    const twitterMatch = content.match(/\*\*Twitter Version.*?\*\*\n\n```\n(.+?)\n```/s);
    const linkedinMatch = content.match(/\*\*LinkedIn Version.*?\*\*\n\n```\n(.+?)\n```/s);
    
    return {
      day,
      twitter: twitterMatch ? twitterMatch[1].trim() : null,
      linkedin: linkedinMatch ? linkedinMatch[1].trim() : null
    };
  }
  
  return null;
}

/**
 * Post to Twitter
 */
async function postTwitter(content, dryRun = false) {
  if (dryRun) {
    console.log('🐦 [DRY RUN] Would post to Twitter:', content.substring(0, 100) + '...');
    return { success: true, platform: 'twitter', dryRun: true };
  }
  
  console.log('🐦 Posting to Twitter...');
  
  const browser = await chromium.launchPersistentContext(CONFIG.browserData.twitter, {
    headless: true,
    viewport: { width: 1280, height: 800 }
  });
  
  const page = browser.pages()[0] || await browser.newPage();
  
  try {
    await page.goto('https://x.com/compose/post', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    
    const composeBox = page.locator('[data-testid="tweetTextarea_0"]').first();
    if (await composeBox.count() === 0) {
      throw new Error('Twitter session expired - re-auth required');
    }
    
    await composeBox.click();
    await page.keyboard.type(content, { delay: 10 });
    await page.waitForTimeout(1000);
    
    const postBtn = page.locator('[data-testid="tweetButtonInline"]');
    await postBtn.click();
    await page.waitForTimeout(3000);
    
    console.log('✅ Twitter posted successfully');
    
    const screenshotPath = path.join(CONFIG.contentDir, `proof-twitter-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });
    
    await browser.close();
    return { success: true, platform: 'twitter', screenshot: screenshotPath };
    
  } catch (err) {
    console.log('❌ Twitter error:', err.message);
    await page.screenshot({ path: path.join(CONFIG.contentDir, 'proof-twitter-error.png') });
    await browser.close();
    return { success: false, platform: 'twitter', error: err.message };
  }
}

/**
 * Post to LinkedIn
 */
async function postLinkedIn(content, dryRun = false) {
  if (dryRun) {
    console.log('💼 [DRY RUN] Would post to LinkedIn:', content.substring(0, 100) + '...');
    return { success: true, platform: 'linkedin', dryRun: true };
  }
  
  console.log('💼 Posting to LinkedIn...');
  
  const browser = await chromium.launchPersistentContext(CONFIG.browserData.linkedin, {
    headless: true,
    viewport: { width: 1280, height: 800 }
  });
  
  const page = browser.pages()[0] || await browser.newPage();
  
  try {
    await page.goto('https://www.linkedin.com/feed/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    
    // Find and click Start a post
    const startPostBtn = page.locator('div[role="button"]').filter({ hasText: 'Start a post' }).first();
    if (await startPostBtn.count() === 0) {
      throw new Error('LinkedIn session expired - re-auth required');
    }
    
    await startPostBtn.scrollIntoViewIfNeeded();
    const box = await startPostBtn.boundingBox();
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForTimeout(2000);
    
    // Type content
    const editor = page.locator('.ql-editor').first();
    await editor.click();
    await page.keyboard.type(content, { delay: 10 });
    await page.waitForTimeout(1500);
    
    // Click Post button
    const postBtn = page.locator('button').filter({ hasText: 'Post' }).first();
    await postBtn.scrollIntoViewIfNeeded();
    const postBox = await postBtn.boundingBox();
    await page.mouse.click(postBox.x + postBox.width / 2, postBox.y + postBox.height / 2);
    await page.waitForTimeout(3000);
    
    console.log('✅ LinkedIn posted successfully');
    
    const screenshotPath = path.join(CONFIG.contentDir, `proof-linkedin-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });
    
    await browser.close();
    return { success: true, platform: 'linkedin', screenshot: screenshotPath };
    
  } catch (err) {
    console.log('❌ LinkedIn error:', err.message);
    await page.screenshot({ path: path.join(CONFIG.contentDir, 'proof-linkedin-error.png') });
    await browser.close();
    return { success: false, platform: 'linkedin', error: err.message };
  }
}

/**
 * Log posting result
 */
function logResult(result, day) {
  const logEntry = {
    timestamp: new Date().toISOString(),
    day,
    platform: result.platform,
    success: result.success,
    screenshot: result.screenshot || null,
    error: result.error || null,
    dryRun: result.dryRun || false
  };
  
  const logFile = path.join(CONFIG.logsDir, 'posts.log');
  const logLine = JSON.stringify(logEntry) + '\n';
  fs.appendFileSync(logFile, logLine);
  
  console.log(`📝 Logged: ${logEntry.timestamp} | Day ${day} | ${result.platform} | ${result.success ? 'SUCCESS' : 'FAILED'}`);
}

/**
 * Main execution
 */
async function main() {
  const args = process.argv.slice(2);
  const dryRun = args.includes('--dry-run');
  const dayArg = args.find(a => a.startsWith('--day='));
  const day = dayArg ? parseInt(dayArg.split('=')[1]) : null;
  
  console.log('📅 Schedule Posts - Automated Content Distribution');
  console.log('━'.repeat(50));
  
  if (dryRun) {
    console.log('🔄 DRY RUN MODE - No actual posts will be made');
  }
  
  // Load content
  let content;
  if (day) {
    content = loadDayContent(day);
    if (!content) {
      console.log(`❌ No content found for Day ${day}`);
      process.exit(1);
    }
    console.log(`📄 Loaded content for Day ${day}`);
  } else {
    // Use today's content (Day 2 by default)
    content = loadDayContent(2);
    console.log('📄 Loaded content for Day 2 (default)');
  }
  
  // Post to platforms
  const results = [];
  
  if (content.twitter) {
    const twitterResult = await postTwitter(content.twitter, dryRun);
    results.push(twitterResult);
    logResult(twitterResult, day || 2);
  }
  
  if (content.linkedin) {
    const linkedinResult = await postLinkedIn(content.linkedin, dryRun);
    results.push(linkedinResult);
    logResult(linkedinResult, day || 2);
  }
  
  // Summary
  console.log('\n' + '━'.repeat(50));
  console.log('📊 POSTING SUMMARY');
  console.log('━'.repeat(50));
  
  results.forEach(r => {
    console.log(`${r.platform.toUpperCase()}: ${r.success ? '✅ SUCCESS' : '❌ FAILED'}`);
    if (r.error) console.log(`   Error: ${r.error}`);
    if (r.screenshot) console.log(`   Screenshot: ${r.screenshot}`);
  });
  
  const successCount = results.filter(r => r.success).length;
  console.log(`\n📈 Success Rate: ${successCount}/${results.length}`);
  
  if (successCount < results.length) {
    console.log('\n⚠️ Some posts failed. Check screenshots for details.');
    console.log('💡 Tip: Sessions may need re-authentication. Run with --re-auth flag.');
  }
}

// Run
main().catch(console.error);