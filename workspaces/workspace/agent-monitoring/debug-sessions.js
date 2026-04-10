const { execSync } = require('child_process');

console.log('=== DEBUGGING SESSION DETECTION ===');

try {
    console.log('1. Testing openclaw sessions command...');
    const output = execSync('openclaw sessions 2>&1', { encoding: 'utf8' });
    console.log('Raw output:', output.substring(0, 500));
    
    console.log('\n2. Testing sessions list...');
    const listOutput = execSync('openclaw sessions list 2>&1', { encoding: 'utf8' });
    console.log('List output:', listOutput.substring(0, 300));
    
    console.log('\n3. Testing JSON format...');
    const jsonOutput = execSync('openclaw sessions --json 2>&1 || echo "JSON failed"', { encoding: 'utf8' });
    console.log('JSON output:', jsonOutput.substring(0, 200));
    
} catch (error) {
    console.log('Error:', error.message);
    console.log('Stdout:', error.stdout);
    console.log('Stderr:', error.stderr);
}

console.log('\n=== MANUAL SESSION EXTRACTION ===');
try {
    const sessionsOutput = execSync('openclaw sessions', { encoding: 'utf8' });
    console.log('Sessions detected - parsing manually...');
    
    // Parse the table output manually
    const lines = sessionsOutput.split('\n');
    const sessions = [];
    
    for (const line of lines) {
        if (line.includes('agent:main:subag')) {
            // Extract session info from table
            const parts = line.split(/\s+/);
            const key = parts[1];
            const age = parts[2];
            const model = parts[3];
            
            // Extract agent name from key or check for KAEL/NYX patterns
            let agentName = 'unknown';
            if (line.includes('KAEL')) agentName = 'kael';
            else if (line.includes('NYX')) agentName = 'nyx';
            else if (key.includes('subag')) agentName = 'subagent-' + key.substring(key.length-8);
            
            sessions.push({
                agentId: agentName,
                key: key,
                age: age,
                model: model,
                status: line.includes('done') ? 'done' : 'running',
                detectedAt: new Date().toISOString()
            });
        }
    }
    
    console.log('Extracted sessions:', sessions);
    
    // Log to monitoring system
    const http = require('http');
    for (const session of sessions) {
        if (session.agentId === 'kael' || session.agentId === 'nyx') {
            const activity = {
                agentId: session.agentId,
                action: 'session_detected_manual',
                outputData: {
                    message: `Detected ${session.agentId} session via manual parsing`,
                    key: session.key,
                    age: session.age,
                    status: session.status
                },
                timestamp: new Date().toISOString()
            };
            
            console.log(`Would log: ${session.agentId} - ${session.status}`);
        }
    }
    
} catch (error) {
    console.log('Manual extraction error:', error.message);
}
