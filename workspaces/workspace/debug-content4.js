// Debug content extraction - check character codes
const fs = require('fs');

function loadContent(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

const fullContent = loadContent('./content/social-post-002.md');
const parts = fullContent.split(/---[\r\n]+/);
console.log('Number of parts:', parts.length);
const twitterPart = parts[1];
console.log('twitterPart length:', twitterPart.length);

// Check first 200 characters and their char codes
console.log('First 200 chars:');
for (let i = 0; i < Math.min(200, twitterPart.length); i++) {
  const char = twitterPart[i];
  const code = char.charCodeAt(0);
  process.stdout.addListener === undefined ? null : null; // Just to avoid lint issues
  if (code === 10) { // LF
    process.stdout.write('\\n');
  } else if (code === 13) { // CR
    process.stdout.write('\\r');
  } else if (code === 32) { // Space
    process.stdout.write(' ');
  } else {
    process.stdout.write(char);
  }
}
console.log('\n');

console.log('Checking for different newline types:');
const lfCount = (twitterPart.match(/\n/g) || []).length;
const crlfCount = (twitterPart.match(/\r\n/g) || []).length;
const crCount = (twitterPart.match(/\r/g) || []).length;
console.log('LF (\\\\n) count:', lfCount);
console.log('CRLF (\\\\r\\\\n) count:', crlfCount);
console.log('CR (\\\\r) count:', crCount);

// Try splitting by different newline types
console.log('\\nSplitting tests:');
console.log('Split by \\\\n:', twitterPart.split('\n').length, 'parts');
console.log('Split by \\\\r\\\\n:', twitterPart.split('\r\n').length, 'parts');
console.log('Split by \\\\r:', twitterPart.split('\r').length, 'parts');
console.log('Split by /[\\\\r\\\\n]+/:', twitterPart.split(/[\r\n]+/).length, 'parts');

// Let's see what we actually get when we split correctly
const lines = twitterPart.split(/[\r\n]+/);
console.log('Lines when splitting by /[\\\\r\\\\n]+/:', lines.length);
lines.forEach((line, index) => {
  console.log(`  Line ${index}: [${JSON.stringify(line)}]`);
});

// Now try the extraction with the correct splitting
let contentLines = [];
let foundContent = false;
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.includes('## Twitter Version')) {
    foundContent = true;
    continue;
  }
  if (foundContent && line.trim() !== '') {
    contentLines.push(line);
  }
}
const result = contentLines.join('\\n').trim();
console.log('Extracted content:', JSON.stringify(result));
