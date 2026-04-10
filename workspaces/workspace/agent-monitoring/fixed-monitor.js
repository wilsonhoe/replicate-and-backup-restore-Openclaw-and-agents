const { execSync } = require('child_process');
const http = require('http');

/**
 * FIXED OpenClaw Session Monitor
 * Uses correct command syntax for session detection
 */

class FixedSessionMonitor {
    constructor() {
        this.monitoringUrl = 'http://localhost:3001/api/monitor/activity';
        this.knownSessions = new Set();
        this.pollInterval = 15000; // 15 seconds
        this.startTime = new Date();
        this.log('Fixed session monitor starting...');
    }

    log(message) {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] FIXED MONITOR: ${message}`);
    }

    async getCurrentSessions() {
        try {
            // Use correct command - no 'list' argument
            const output = execSync('openclaw sessions 2>&1', { encoding: 'utf8' });
            return this.parseSessionsOutput(output);
        } catch (error) {
            this.log(`Session detection error: ${error.message}`);
            return [];
        }
    }

    parseSessionsOutput(output) {
        const sessions = [];
        const lines = output.split('\n');
        
        for (const line of lines) {
            // Look for agent sessions in the table
            if (line.includes('agent:main:')) {
                const parts = line.split(/\s+/).filter(p => p.length > 0);
                
                if (parts.length >= 4) {
                    const key = parts[1];
                    const age = parts[2];
                    const model = parts[3];
                    
                    // Extract agent name
                    let agentName = this.extractAgentName(key, line);
                    
                    sessions.push({
                        key: key,
                        agentId: agentName,
                        age: age,
                        model: model,
                        status: line.includes('done') ? 'completed' : 'running',
                        detectedAt: new Date().toISOString()
                    });
                }
            }
        }
        
        return sessions;
    }

    extractAgentName(key, line) {
        // Check for KAEL/NYX in the line
        if (line.includes('KAEL')) return 'kael-execution-architect';
        if (line.includes('NYX')) return 'nyx-growth-intelligence';
        
        // Extract from key patterns
        if (key.includes('subag')) {
            return 'subagent-' + key.split('-').pop();
        }
        
        return key.split(':').pop() || 'unknown-agent';
    }

    async logActivity(activity) {
        try {
            const response = await fetch(this.monitoringUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(activity)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const result = await response.json();
            this.log(`Logged: ${activity.agentId} - ${activity.action}`);
            return result;
        } catch (error) {
            this.log(`Failed to log activity: ${error.message}`);
            return null;
        }
    }

    async pollSessions() {
        const sessions = await this.getCurrentSessions();
        const currentTime = new Date().toISOString();
        
        this.log(`Detected ${sessions.length} sessions`);
        
        for (const session of sessions) {
            const sessionId = session.key;
            
            if (!this.knownSessions.has(sessionId)) {
                // New session detected
                this.knownSessions.add(sessionId);
                
                await this.logActivity({
                    agentId: session.agentId,
                    action: 'session_started',
                    outputData: {
                        message: `New session: ${session.agentId}`,
                        key: session.key,
                        age: session.age,
                        model: session.model,
                        status: session.status
                    },
                    timestamp: currentTime
                });
            } else {
                // Existing session - heartbeat
                await this.logActivity({
                    agentId: session.agentId,
                    action: 'session_heartbeat',
                    outputData: {
                        message: `Session active: ${session.agentId}`,
                        age: session.age,
                        status: session.status
                    },
                    timestamp: currentTime
                });
            }
        }
    }

    start() {
        this.log('Starting fixed session monitoring...');
        
        // Initial poll
        this.pollSessions();
        
        // Schedule regular polling
        setInterval(() => {
            this.pollSessions();
        }, this.pollInterval);
        
        this.log(`Fixed monitoring started - polling every ${this.pollInterval/1000} seconds`);
    }
}

// Start the fixed monitor
const monitor = new FixedSessionMonitor();
monitor.start();
