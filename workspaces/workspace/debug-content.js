// Debug content extraction
const fs = require('fs');

function loadContent(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

const fullContent = loadContent('./content/social-post-002.md');
console.log('Full content length:', fullContent.length);
console.log('First 200 chars:', JSON.stringify(fullContent.substring(0, 200)));

const parts = fullContent.split('---\\n');
console.log('Number of parts:', parts.length);
console.log('Part 0:', JSON.stringify(parts[0]));
console.log('Part 1:', JSON.stringify(parts[1]));
console.log('Part 2:', JSON.stringify(parts[2]));
console.log('Part 3:', JSON.stringify(parts[3]));
console.log('Part 4:', JSON.stringify(parts[4]));

// Test extraction
const twitterPart = parts[1];
console.log('twitterPart:', twitterPart);
console.log('twitterPart type:', typeof twitterPart);
if (twitterPart !== undefined) {
  const lines = twitterPart.split('\\n');
  console.log('Lines:', lines);
} else {
  console.log('twitterPart is undefined!');
}
