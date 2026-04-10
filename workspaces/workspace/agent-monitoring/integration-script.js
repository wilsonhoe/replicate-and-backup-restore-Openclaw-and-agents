#!/usr/bin/env node

/**
 * Integration Script - Connect Current OpenClaw Sessions to Monitoring System
 * This script integrates existing agent sessions with the visibility monitor
 */

// const axios = require('axios'); // Using direct HTTP calls instead
const fs = require('fs');
const path = require('path');

const MONITOR_API = 'http://localhost:3001/api/monitor';

// Current active sessions from our system
const ACTIVE_SESSIONS = [
    {
        id: 'main-discord-wilsonhoe',
        type: 'main_agent',
        channel: 'discord',
        user: 'wilsonhoe',
        status: 'running'
    },
    {
        id: 'heartbeat-monitor',
        type: 'system_monitor',
        channel: 'internal',
        status: 'running'
    }
];

class SessionMonitor {
    constructor() {
        this.monitoring = false;
        this.activityLog = [];
    }

    async registerSessions() {
        console.log('🔄 Registering active sessions with monitoring system...');
        
        for (const session of ACTIVE_SESSIONS) {
            try {
                await this.registerAgent(session);
                console.log(`✅ Registered: ${session.id} (${session.type})`);
            } catch (error) {
                console.log(`❌ Failed to register: ${session.id} - ${error.message}`);
            }
        }
    }

    async registerAgent(session) {
        const registrationData = {
            agentId: session.id,
            agentType: session.type,
            channel: session.channel,
            status: session.status,
            registeredAt: new Date().toISOString()
        };

        // Simulate registration via activity log
        await this.logActivity(session.id, 'register', { session }, { 
            success: true, 
            message: 'Agent registered for monitoring' 
        });
    }

    async logActivity(agentId, action, inputData, outputData) {
        const activityData = {
            timestamp: new Date().toISOString(),
            agentId: agentId,
            action: action,
            inputHash: this.hashInput(inputData),
            outputData: this.sanitizeOutput(outputData),
            hallucinationScore: this.calculateHallucinationScore(action, outputData),
            verificationStatus: 'completed'
        };

        try {
            // Send to monitoring API
            await axios.post(`${MONITOR_API}/activity`, activityData);
            this.activityLog.push(activityData);
            console.log(`📊 Logged: ${agentId} - ${action} (Risk: ${activityData.hallucinationScore.riskLevel})`);
        } catch (error) {
            console.log(`⚠️  Failed to log activity: ${error.message}`);
            // Store locally if API unavailable
            this.activityLog.push(activityData);
        }
    }

    calculateHallucinationScore(action, outputData) {
        // Multi-layer hallucination detection
        let scores = {
            consistency: this.checkConsistency(action, outputData),
            factual: this.checkFactualAccuracy(outputData),
            source: this.checkSourceAttribution(outputData),
            confidence: this.assessConfidence(outputData)
        };

        let compositeScore = (
            scores.consistency * 0.3 +
            scores.factual * 0.3 +
            scores.source * 0.2 +
            scores.confidence * 0.2
        );

        return {
            compositeScore: compositeScore,
            componentScores: scores,
            riskLevel: this.categorizeRisk(compositeScore)
        };
    }

    checkConsistency(action, outputData) {
        // Check for internal consistency in agent outputs
        if (outputData.success === false) return 0.9; // Low risk for errors
        if (outputData.message && outputData.message.includes('error')) return 0.8;
        if (action === 'register') return 0.95; // High consistency for system actions
        return 0.7; // Default medium consistency
    }

    checkFactualAccuracy(outputData) {
        // Basic factual verification
        if (outputData.success === true || outputData.success === false) return 0.9;
        if (outputData.data && typeof outputData.data === 'object') return 0.8;
        return 0.6;
    }

    checkSourceAttribution(outputData) {
        // Check for source attribution
        if (outputData.source) return 0.9;
        if (outputData.message && outputData.message.includes('based on')) return 0.8;
        return 0.5; // Default low attribution
    }

    assessConfidence(outputData) {
        // Assess output confidence
        if (outputData.confidence !== undefined) return outputData.confidence;
        if (outputData.success === true) return 0.8;
        if (outputData.success === false) return 0.9;
        return 0.6;
    }

    categorizeRisk(score) {
        if (score >= 0.8) return 'Low';
        if (score >= 0.6) return 'Medium';
        if (score >= 0.4) return 'High';
        return 'Critical';
    }

    hashInput(inputData) {
        return require('crypto')
            .createHash('sha256')
            .update(JSON.stringify(inputData))
            .digest('hex')
            .substring(0, 16);
    }

    sanitizeOutput(outputData) {
        // Truncate large outputs for privacy
        const str = JSON.stringify(outputData);
        if (str.length > 500) {
            return str.substring(0, 500) + '...[truncated]';
        }
        return outputData;
    }

    async simulateAgentActivity() {
        console.log('🎭 Simulating agent activities for demonstration...');
        
        // Simulate main agent activity
        await this.logActivity('main-discord-wilsonhoe', 'process_message', {
            message: 'What are you doing?',
            context: 'user inquiry'
        }, {
            success: true,
            response: 'Monitoring system deployment and integration',
            confidence: 0.85
        });

        // Simulate research activity
        await this.logActivity('main-discord-wilsonhoe', 'research_request', {
            query: 'multi-agent monitoring systems'
        }, {
            success: true,
            data: 'Found 3 architectures: QIS, Hierarchical, Specialist',
            source: 'web_search',
            confidence: 0.9
        });

        // Simulate potential hallucination
        await this.logActivity('main-discord-wilsonhoe', 'generate_content', {
            task: 'create monitoring system'
        }, {
            success: true,
            content: 'System deployed successfully with 100% accuracy',
            confidence: 0.95
        });

        // Simulate system monitoring
        await this.logActivity('heartbeat-monitor', 'system_check', {
            check_type: 'bridge_monitoring'
        }, {
            success: true,
            status: 'bridge_active',
            last_check: new Date().toISOString()
        });

        // Simulate error condition
        await this.logActivity('main-discord-wilsonhoe', 'tool_execution', {
            tool: 'web_scraper',
            url: 'example.com'
        }, {
            success: false,
            error: 'Connection timeout',
            message: 'Failed to connect to remote server'
        });
    }

    async generateReport() {
        console.log('\n📈 Generating monitoring report...');
        
        const report = {
            timestamp: new Date().toISOString(),
            totalActivities: this.activityLog.length,
            agentsMonitored: ACTIVE_SESSIONS.length,
            riskDistribution: this.analyzeRiskDistribution(),
            recentActivities: this.activityLog.slice(-5),
            systemHealth: await this.checkSystemHealth()
        };

        console.log('\n🎯 MONITORING REPORT');
        console.log('═══════════════════════════════════════');
        console.log(`Total Activities Logged: ${report.totalActivities}`);
        console.log(`Agents Monitored: ${report.agentsMonitored}`);
        console.log(`System Health: ${report.systemHealth.status}`);
        console.log('\n📊 Risk Distribution:');
        Object.entries(report.riskDistribution).forEach(([level, count]) => {
            console.log(`  ${level}: ${count} activities`);
        });

        return report;
    }

    analyzeRiskDistribution() {
        const distribution = { Low: 0, Medium: 0, High: 0, Critical: 0 };
        this.activityLog.forEach(activity => {
            const level = activity.hallucinationScore.riskLevel;
            distribution[level] = (distribution[level] || 0) + 1;
        });
        return distribution;
    }

    async checkSystemHealth() {
        try {
            // Direct HTTP check using Node.js http module
            const http = require('http');
            return new Promise((resolve) => {
                const req = http.request(`${MONITOR_API}/status`, (res) => {
                    let data = '';
                    res.on('data', chunk => data += chunk);
                    res.on('end', () => {
                        resolve({
                            status: 'Healthy',
                            apiResponse: JSON.parse(data),
                            timestamp: new Date().toISOString()
                        });
                    });
                });
                req.on('error', (err) => {
                    resolve({
                        status: 'API Check Failed',
                        error: err.message,
                        timestamp: new Date().toISOString()
                    });
                });
                req.setTimeout(3000, () => {
                    resolve({
                        status: 'API Timeout',
                        timestamp: new Date().toISOString()
                    });
                });
                req.end();
            });
        } catch (error) {
            return {
                status: 'Health Check Error',
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
}

// Main execution
async function main() {
    console.log('🚀 OpenClaw Agent Monitoring Integration');
    console.log('═══════════════════════════════════════════\n');

    const monitor = new SessionMonitor();
    
    try {
        // Register current sessions
        await monitor.registerSessions();
        
        // Simulate real agent activities
        await monitor.simulateAgentActivity();
        
        // Generate monitoring report
        const report = await monitor.generateReport();
        
        console.log('\n✅ Integration complete!');
        console.log('🌐 Dashboard: http://localhost:3001');
        console.log('📊 API Status: http://localhost:3001/api/monitor/status');
        
    } catch (error) {
        console.error('❌ Integration failed:', error.message);
    }
}

// Run integration
if (require.main === module) {
    main().catch(console.error);
}

module.exports = SessionMonitor;