// Debug content extraction with detailed line processing
const fs = require('fs');

function loadContent(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

// Function to extract Twitter content
function extractTwitterContent(fullContent) {
  // Split by --- followed by newline(s)
  const parts = fullContent.split(/---[\r\n]+/);
  console.log('Number of parts:', parts.length);
  // Part 1 contains "## Twitter Version" header + content
  const twitterPart = parts[1];
  console.log('twitterPart:', JSON.stringify(twitterPart));
  const lines = twitterPart.split('\\n');
  console.log('Number of lines:', lines.length);
  lines.forEach((line, index) => {
    console.log(`Line ${index}: [${JSON.stringify(line)}] (trimmed: [${JSON.stringify(line.trim())}], length: ${line.trim().length})`);
  });
  
  let contentLines = [];
  let foundContent = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    console.log(`Processing line ${i}: '${line}' (trimmed: '${trimmed}')`);
    
    if (line.includes('## Twitter Version')) {
      foundContent = true;
      console.log(`  -> Found Twitter header, set foundContent = true`);
      continue;
    }
    if (foundContent) {
      console.log(`  -> foundContent is true`);
      if (trimmed !== '') {
        console.log(`  -> Line is not empty, adding to contentLines`);
        contentLines.push(line);
      } else {
        console.log(`  -> Line is empty, skipping`);
      }
    } else {
      console.log(`  -> foundContent is false, skipping`);
    }
  }
  
  const result = contentLines.join('\\n').trim();
  console.log('Final Twitter content:', JSON.stringify(result));
  return result;
}

const fullContent = loadContent('./content/social-post-002.md');
extractTwitterContent(fullContent);
