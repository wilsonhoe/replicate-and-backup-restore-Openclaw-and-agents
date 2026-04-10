const { execSync } = require('child_process');
const http = require('http');

/**
 * ACTIVE OpenClaw Session Monitor
 * Polls session manager and logs real activity
 */

class ActiveSessionMonitor {
    constructor() {
        this.monitoringUrl = 'http://localhost:3001/api/monitor/activity';
        this.knownSessions = new Set();
        this.pollInterval = 10000; // 10 seconds
        this.startTime = new Date();
        this.log('Active session monitor starting...');
    }

    log(message) {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] ACTIVE MONITOR: ${message}`);
    }

    async getCurrentSessions() {
        try {
            const output = execSync('openclaw sessions list --json 2>/dev/null || echo "[]"', { encoding: 'utf8' });
            return JSON.parse(output || '[]');
        } catch (error) {
            this.log(`Session detection error: ${error.message}`);
            return [];
        }
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
        
        for (const session of sessions) {
            const sessionId = session.sessionId || session.key;
            const agentId = this.extractAgentId(session);
            
            if (!this.knownSessions.has(sessionId)) {
                // New session detected
                this.knownSessions.add(sessionId);
                
                await this.logActivity({
                    agentId: agentId,
                    action: 'session_started',
                    outputData: {
                        message: `New session detected: ${session.label || agentId}`,
                        sessionId: sessionId,
                        model: session.model,
                        channel: session.channel,
                        status: session.status
                    },
                    timestamp: currentTime
                });
            } else {
                // Existing session - heartbeat
                if (Math.random() < 0.1) { // 10% chance to log heartbeat
                    await this.logActivity({
                        agentId: agentId,
                        action: 'session_heartbeat',
                        outputData: {
                            message: `Session active: ${session.label || agentId}`,
                            sessionId: sessionId,
                            uptime: Date.now() - new Date(session.startedAt || session.updatedAt).getTime(),
                            tokens: session.totalTokens || 0
                        },
                        timestamp: currentTime
                    });
                }
            }
        }
        
        // Log system heartbeat
        await this.logActivity({
            agentId: 'active-monitor',
            action: 'system_heartbeat',
            outputData: {
                message: 'Active monitoring system polling sessions',
                sessionsTracked: sessions.length,
                knownSessions: this.knownSessions.size,
                uptime: Date.now() - this.startTime.getTime()
            },
            timestamp: currentTime
        });
    }

    extractAgentId(session) {
        if (session.label) {
            // Extract from label like "⚙️ KAEL — Execution Architect"
            const match = session.label.match(/[⚙️🌌]\s*(\w+)/);
            if (match) return match[1].toLowerCase();
        }
        
        if (session.key) {
            // Extract from key like "agent:main:subagent:5518ad47-8986-4ce1-9976-57f54d74ae73"
            const parts = session.key.split(':');
            if (parts.length >= 4) return parts[parts.length - 1].substring(0, 8);
        }
        
        return session.displayName || 'unknown-agent';
    }

    start() {
        this.log('Starting active session monitoring...');
        
        // Initial poll
        this.pollSessions();
        
        // Schedule regular polling
        setInterval(() => {
            this.pollSessions();
        }, this.pollInterval);
        
        this.log(`Active monitoring started - polling every ${this.pollInterval/1000} seconds`);
    }
}

// Start the active monitor
const monitor = new ActiveSessionMonitor();
monitor.start();
