// Zoho Social Manual Posting Guide
// Since Zoho Social has no public API, use browser automation

const fs = require('fs');

// Load Day 2 content
const content = fs.readFileSync('./content/social-post-002.md', 'utf8');

// Extract Twitter version
const twitterMatch = content.match(/## Twitter Version \(280 chars\)\n\n([\s\S]+?)(?=\n---)/);
const twitterContent = twitterMatch ? twitterMatch[1].trim() : '';

// Extract LinkedIn version
const linkedinMatch = content.match(/## LinkedIn Version\n\n([\s\S]+?)(?=\n---)/);
const linkedinContent = linkedinMatch ? linkedinMatch[1].trim() : '';

console.log('📋 Zoho Social Posting Instructions\n');
console.log('================================\n');

console.log('Step 1: Open Chrome and go to:');
console.log('https://social.zoho.com\n');

console.log('Step 2: Log in with:');
console.log('  Email: lisamolbot@gmail.com');
console.log('  Password: mv9p@T8iRWWQwBw\n');

console.log('Step 3: Click "New Post" button (top-right)\n');

console.log('Step 4: Select Twitter channel\n');

console.log('Step 5: Paste Twitter content:\n');
console.log('--- TWITTER CONTENT ---');
console.log(twitterContent);
console.log('--- END TWITTER ---\n');

console.log('Step 6: Select LinkedIn channel (in same post)\n');

console.log('Step 7: Paste LinkedIn content:\n');
console.log('--- LINKEDIN CONTENT ---');
console.log(linkedinContent);
console.log('--- END LINKEDIN ---\n');

console.log('Step 8: Click "Publish"\n');

console.log('Step 9: Save the post URLs for proof\n');

console.log('================================');
