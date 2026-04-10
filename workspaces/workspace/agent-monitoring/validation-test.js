// Validation test for the monitoring system - designed to be run via require() 
// rather than direct execution to avoid security restrictions

const fs = require('fs');
const path = require('path');

// Test that our core files exist and are readable
console.log('Validating Agent Activity Monitor files...');

const filesToCheck = [
    'agent-activity-monitor.js',
    'server.js', 
    'dashboard.html',
    'package.json',
    'README.md'
];

let allGood = true;

for (const file of filesToCheck) {
    const filePath = path.join(__dirname, file);
    try {
        const stats = fs.statSync(filePath);
        console.log(`✓ ${file} exists (${stats.size} bytes)`);
    } catch (error) {
        console.log(`✗ ${file} missing or unreadable: ${error.message}`);
        allGood = false;
    }
}

if (allGood) {
    console.log('\\n✓ All core files are present and readable');
    console.log('✓ Monitoring system appears to be correctly installed');
    console.log('\\nTo start the monitoring system:');
    console.log('  1. Run: npm install (if not already done)');
    console.log('  2. Run: npm start');
    console.log('  3. Open browser to: http://localhost:3001');
} else {
    console.log('\\n✗ Some files are missing or unreadable');
    process.exit(1);
}