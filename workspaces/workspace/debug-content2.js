// Debug content extraction for the final script
const fs = require('fs');

function loadContent(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

// Function to extract Twitter content
function extractTwitterContent(fullContent) {
  // Split by --- followed by newline(s)
  const parts = fullContent.split(/---[\r\n]+/);
  console.log('Number of parts:', parts.length);
  for (let i = 0; i < parts.length; i++) {
    console.log('Part', i, 'length:', parts[i].length);
    console.log('Part', i, 'first 100 chars:', JSON.stringify(parts[i].substring(0, 100)));
  }
  // Part 1 contains "## Twitter Version" header + content
  const twitterPart = parts[1];
  console.log('twitterPart:', twitterPart);
  if (!twitterPart) {
    console.log('twitterPart is undefined or empty!');
    return '';
  }
  const lines = twitterPart.split('\\n');
  console.log('Lines in twitterPart:', lines);
  let contentLines = [];
  let foundContent = false;
  for (let i = 0; i < lines.length; i++) {
    console.log('Processing line', i, ':', JSON.stringify(lines[i]));
    if (lines[i].includes('## Twitter Version')) {
      foundContent = true;
      console.log('Found Twitter header');
      continue;
    }
    if (foundContent && lines[i].trim() !== '') {
      contentLines.push(lines[i]);
      console.log('Added line to content:', JSON.stringify(lines[i]));
    }
  }
  const result = contentLines.join('\\n').trim();
  console.log('Final Twitter content:', JSON.stringify(result));
  return result;
}

const fullContent = loadContent('./content/social-post-002.md');
extractTwitterContent(fullContent);
