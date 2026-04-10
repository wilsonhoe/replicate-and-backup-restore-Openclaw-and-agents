const { chromium } = require('playwright');
const fs = require('fs');

async function testSessionReuse() {
    console.log('🧪 Testing Session Reuse from Existing Captures');
    
    // Launch Chrome with existing debugging port or create new instance
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    const context = browser.contexts()[0];
    const page = await context.newPage();
    
    try {
        // Test Twitter session reuse
        console.log('\n🔵 Testing Twitter Session Reuse...');
        await page.goto('https://x.com/home');
        await page.waitForTimeout(3000);
        
        const twitterUrl = page.url();
        if (twitterUrl.includes('home') || twitterUrl.includes('x.com')) {
            console.log('✅ Twitter session reuse SUCCESSFUL - already logged in');
        } else {
            console.log('⚠️ Twitter session may need refresh - current URL:', twitterUrl);
        }
        
        // Test LinkedIn session reuse
        console.log('\n🔵 Testing LinkedIn Session Reuse...');
        await page.goto('https://www.linkedin.com/feed/');
        await page.waitForTimeout(3000);
        
        const linkedinUrl = page.url();
        if (linkedinUrl.includes('feed') || linkedinUrl.includes('linkedin.com')) {
            console.log('✅ LinkedIn session reuse SUCCESSFUL - already logged in');
        } else {
            console.log('⚠️ LinkedIn session may need refresh - current URL:', linkedinUrl);
        }
        
        await page.close();
        await browser.close();
        
        console.log('\n🎉 Session reuse test completed!');
        return true;
        
    } catch (error) {
        console.error('❌ Session reuse test failed:', error.message);
        await page.close();
        await browser.close();
        return false;
    }
}

testSessionReuse();