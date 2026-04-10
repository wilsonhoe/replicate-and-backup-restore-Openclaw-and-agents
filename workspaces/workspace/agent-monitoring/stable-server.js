#!/usr/bin/env node

/**
 * BULLETPROOF OpenClaw Monitoring Server
 * Production-ready with error handling and stability
 */

const express = require('express');
const http = require('http');
const path = require('path');
const fs = require('fs');

class StableMonitorServer {
    constructor() {
        this.app = express();
        this.server = null;
        this.activities = [];
        this.agents = new Map();
        this.maxActivities = 1000;
        this.startTime = new Date();
        
        this.setupMiddleware();
        this.setupRoutes();
        this.loadExistingData();
    }

    setupMiddleware() {
        this.app.use(express.json({ limit: '10mb' }));
        this.app.use(express.static(path.join(__dirname, 'public')));
        
        // CORS for local development
        this.app.use((req, res, next) => {
            res.header('Access-Control-Allow-Origin', '*');
            res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
            res.header('Access-Control-Allow-Headers', 'Content-Type');
            if (req.method === 'OPTIONS') {
                res.sendStatus(200);
            } else {
                next();
            }
        });
    }

    setupRoutes() {
        // API Routes
        this.app.get('/api/monitor/status', (req, res) => {
            try {
                const status = this.getSystemStatus();
                res.json(status);
            } catch (error) {
                console.error('Status endpoint error:', error);
                res.status(500).json({ error: 'Internal server error' });
            }
        });

        this.app.post('/api/monitor/activity', (req, res) => {
            try {
                const activity = this.addActivity(req.body);
                res.json({ success: true, message: 'Activity logged', activityId: activity.id });
            } catch (error) {
                console.error('Activity endpoint error:', error);
                res.status(500).json({ error: 'Failed to log activity' });
            }
        });

        // Serve dashboard
        this.app.get('/', (req, res) => {
            res.sendFile(path.join(__dirname, 'dashboard.html'));
        });

        // Health check
        this.app.get('/health', (req, res) => {
            res.json({ status: 'healthy', uptime: Date.now() - this.startTime.getTime() });
        });
    }

    loadExistingData() {
        try {
            const dataFile = path.join(__dirname, 'monitoring-data.json');
            if (fs.existsSync(dataFile)) {
                const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
                this.activities = data.activities || [];
                this.agents = new Map(data.agents || []);
                console.log(`[Monitor] Loaded ${this.activities.length} existing activities`);
            }
        } catch (error) {
            console.log(`[Monitor] No existing data found, starting fresh`);
        }
    }

    saveData() {
        try {
            const dataFile = path.join(__dirname, 'monitoring-data.json');
            const data = {
                activities: this.activities,
                agents: Array.from(this.agents.entries())
            };
            fs.writeFileSync(dataFile, JSON.stringify(data, null, 2));
        } catch (error) {
            console.error('Failed to save data:', error);
        }
    }

    addActivity(activityData) {
        const timestamp = activityData.timestamp || new Date().toISOString();
        
        // Update agent tracking
        const agentId = activityData.agentId;
        if (!this.agents.has(agentId)) {
            this.agents.set(agentId, {
                id: agentId,
                type: 'agent',
                lastSeen: timestamp,
                activityCount: 0
            });
        }
        
        const agent = this.agents.get(agentId);
        agent.lastSeen = timestamp;
        agent.activityCount++;
        
        // Create activity record
        const activity = {
            id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
            timestamp,
            agentId,
            action: activityData.action,
            inputHash: activityData.inputHash || this.generateHash(activityData.inputData || {}),
            outputData: this.serializeData(activityData.outputData || {}),
            hallucinationCheck: activityData.hallucinationScore || this.calculateHallucinationScore(activityData),
            verificationStatus: activityData.verificationStatus || 'completed',
            metadata: activityData.metadata || {}
        };
        
        this.activities.push(activity);
        
        // Maintain size limit
        if (this.activities.length > this.maxActivities) {
            this.activities.shift();
        }
        
        // Save to file
        this.saveData();
        
        console.log(`[Monitor] Activity logged: ${agentId} - ${activityData.action}`);
        return activity;
    }

    serializeData(data) {
        if (typeof data === 'object') {
            return JSON.stringify(data);
        }
        return String(data);
    }

    calculateHallucinationScore(activityData) {
        // Simple scoring based on action type
        let score = 0.85;
        let riskLevel = 'Low';
        
        if (activityData.action.includes('error')) {
            score = 0.3;
            riskLevel = 'High';
        } else if (activityData.action.includes('verification')) {
            score = 0.65;
            riskLevel = 'Medium';
        } else if (activityData.action.includes('system')) {
            score = 0.9;
            riskLevel = 'Low';
        }
        
        return {
            compositeScore: score,
            componentScores: {
                consistency: 0.9,
                factual: score,
                source: 0.8,
                confidence: score
            },
            riskLevel: riskLevel
        };
    }

    generateHash(data) {
        return require('crypto')
            .createHash('sha256')
            .update(JSON.stringify(data))
            .digest('hex')
            .substring(0, 16);
    }

    getSystemStatus() {
        const now = new Date();
        const recentActivities = this.activities.slice(-10).reverse();
        
        // Count agents by status
        let activeAgents = 0;
        let totalAgents = this.agents.size;
        
        for (const [agentId, agent] of this.agents) {
            const lastSeen = new Date(agent.lastSeen);
            const minutesSinceLastSeen = (now - lastSeen) / (1000 * 60);
            if (minutesSinceLastSeen < 5) {
                activeAgents++;
            }
        }
        
        // Generate alerts from high-risk activities
        const alerts = recentActivities.filter(activity => {
            const score = activity.hallucinationCheck?.compositeScore || 1;
            return score < 0.5;
        });
        
        return {
            systemStatus: {
                isRunning: true,
                totalAgents: totalAgents,
                activeAgents: activeAgents,
                totalActivities: this.activities.length,
                verificationRequests: alerts.length,
                lastUpdate: now.toISOString(),
                uptime: now - this.startTime
            },
            agentMetrics: Array.from(this.agents.values()),
            recentActivities: recentActivities,
            hallucinationAlerts: alerts,
            verificationRequests: alerts.map(activity => ({
                id: `verify_${activity.id}`,
                targetAgent: activity.agentId,
                activity: activity,
                requestedAt: activity.timestamp,
                status: 'pending'
            }))
        };
    }

    start(port = 3001) {
        return new Promise((resolve, reject) => {
            this.server = this.app.listen(port, (err) => {
                if (err) {
                    console.error(`[Monitor] Failed to start server on port ${port}:`, err);
                    reject(err);
                } else {
                    console.log(`[Monitor] Dashboard running on http://localhost:${port}`);
                    console.log(`[Monitor] API endpoints available`);
                    console.log(`[Monitor] ${this.activities.length} activities loaded`);
                    resolve();
                }
            });
            
            this.server.on('error', (err) => {
                console.error('[Monitor] Server error:', err);
                if (err.code === 'EADDRINUSE') {
                    console.log(`[Monitor] Port ${port} in use, trying ${port + 1}`);
                    this.start(port + 1).then(resolve).catch(reject);
                } else {
                    reject(err);
                }
            });
        });
    }

    stop() {
        return new Promise((resolve) => {
            if (this.server) {
                this.server.close(() => {
                    console.log('[Monitor] Server stopped');
                    resolve();
                });
            } else {
                resolve();
            }
        });
    }
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n[Monitor] Shutting down gracefully...');
    if (monitor) {
        await monitor.stop();
    }
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('\n[Monitor] Received SIGTERM, shutting down...');
    if (monitor) {
        await monitor.stop();
    }
    process.exit(0);
});

// Start the server
const monitor = new StableMonitorServer();
monitor.start().then(() => {
    console.log('[Monitor] System ready and stable');
}).catch((err) => {
    console.error('[Monitor] Failed to start system:', err);
    process.exit(1);
});