const fs = require('fs');
const content = fs.readFileSync('./content/social-post-002.md', 'utf8');
const parts = content.split(/---[\r\n]+/);
const twitterPart = parts[1];
const lines = twitterPart.split(/[\r\n]+/);
let contentLines = [];
let foundContent = false;
for (let i = 0; i < lines.length; i++) {
  if (lines[i].includes('## Twitter Version')) {
    foundContent = true;
    continue;
  }
  if (foundContent && lines[i].trim() !== '') {
    contentLines.push(lines[i]);
  }
}
const twitterContent = contentLines.join('\n').trim();
console.log('Twitter content:');
console.log(twitterContent);
console.log('');
console.log('Character analysis:');
for (let i = 0; i < twitterContent.length; i++) {
  const char = twitterContent[i];
  const code = char.charCodeAt(0);
  if (code > 127 || code < 32 && code !== 10 && code !== 13) {
    console.log(`${i}: '${char}' (${code})`);
  }
}
