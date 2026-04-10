//!/usr/bin/env node

/**
 * Monitoring API Server
 * Provides REST API endpoints for the agent activity monitor dashboard
 */

const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');
const AgentActivityMonitor = require('./agent-activity-monitor');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Initialize the activity monitor
const activityMonitor = new AgentActivityMonitor({
    logDirectory: path.join(__dirname, 'logs'),
    checkInterval: 5000,
    hallucinationDetectionEnabled: true,
    verificationRequired: true
});

// API Routes
app.get('/api/monitor/status', async (req, res) => {
    try {
        const status = activityMonitor.getStatus();
        const agentMetrics = activityMonitor.getAgentMetrics();
        const recentActivities = activityMonitor.getRecentActivities(50);
        
        res.json({
            systemStatus: {
                isRunning: activityMonitor.isRunning,
                totalAgents: status.totalAgents,
                activeAgents: status.activeAgents,
                totalActivities: status.totalActivities,
                verificationRequests: status.verificationRequests,
                lastUpdate: new Date().toISOString()
            },
            agentMetrics: agentMetrics,
            recentActivities: recentActivities
        });
    } catch (error) {
        console.error('[API] Error fetching status:', error.message);
        res.status(500).json({ error: 'Failed to fetch monitoring data' });
    }
});

// POST endpoint for logging activities
app.post('/api/monitor/activity', async (req, res) => {
    try {
        const activityData = req.body;
        
        // Validate required fields
        if (!activityData.agentId || !activityData.action) {
            return res.status(400).json({ 
                error: 'Missing required fields: agentId, action' 
            });
        }
        
        // Log the activity through the monitor
        await activityMonitor.logActivity(
            activityData.agentId,
            activityData.action,
            activityData.inputData || {},
            activityData.outputData || {},
            activityData.metadata || {}
        );
        
        console.log(`[API] Activity logged: ${activityData.agentId} - ${activityData.action}`);
        
        // Broadcast to all connected WebSocket clients
        io.emit('activity-update', {
            activity: activityData,
            timestamp: new Date().toISOString()
        });
        
        res.json({ 
            success: true, 
            message: 'Activity logged successfully',
            activityId: Date.now().toString()
        });
        
    } catch (error) {
        console.error('[API] Error logging activity:', error.message);
        res.status(500).json({ 
            error: 'Failed to log activity',
            details: error.message 
        });
    }
});

// WebSocket connection for real-time updates
io.on('connection', (socket) => {
    console.log('[WebSocket] Client connected:', socket.id);
    
    // Send initial data
    socket.emit('initial-data', {
        systemStatus: {
            isRunning: activityMonitor.isRunning,
            totalAgents: activityMonitor.getStatus().totalAgents,
            activeAgents: activityMonitor.getStatus().activeAgents,
            totalActivities: activityMonitor.getStatus().totalActivities,
            verificationRequests: activityMonitor.getStatus().verificationRequests
        }
    });
    
    // Handle client disconnection
    socket.on('disconnect', () => {
        console.log('[WebSocket] Client disconnected:', socket.id);
    });
});

// Start the monitoring system
async function startMonitoringSystem() {
    try {
        await activityMonitor.start();
        console.log('[Monitor] Activity monitoring system started');
        
// Broadcast updates to connected clients every 5 seconds
        setInterval(() => {
            const status = activityMonitor.getStatus();
            io.emit('system-update', {
                systemStatus: {
                    isRunning: activityMonitor.isRunning,
                    totalAgents: status.totalAgents,
                    activeAgents: status.activeAgents,
                    totalActivities: status.totalActivities,
                    verificationRequests: status.verificationRequests,
                    lastUpdate: new Date().toISOString()
                }
            });
        }, 5000);
        
    } catch (error) {
        console.error('[Monitor] Failed to start monitoring system:', error.message);
    }
}

// Serve the dashboard
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// Error handling
app.use((err, req, res, next) => {
    console.error('[API] Error:', err.message);
    res.status(500).json({ error: 'Internal server error' });
});

// Start server
const startServer = async () => {
    try {
        await startMonitoringSystem();
        
        server.listen(PORT, () => {
            console.log(`[Server] Monitoring dashboard running on http://localhost:${PORT}`);
            console.log(`[Server] Press Ctrl+C to stop`);
        });
        
    } catch (error) {
        console.error('[Server] Failed to start:', error.message);
        process.exit(1);
    }
};

// Handle graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n[Server] Received SIGINT, shutting down...');
    try {
        await activityMonitor.stop();
        server.close(() => {
            console.log('[Server] Monitoring system stopped');
            process.exit(0);
        });
    } catch (error) {
        console.error('[Server] Error during shutdown:', error.message);
        process.exit(1);
    }
});

process.on('SIGTERM', async () => {
    console.log('\n[Server] Received SIGTERM, shutting down...');
    try {
        await activityMonitor.stop();
        server.close(() => {
            console.log('[Server] Monitoring system stopped');
            process.exit(0);
        });
    } catch (error) {
        console.error('[Server] Error during shutdown:', error.message);
        process.exit(1);
    }
});

// Start the server
startServer();

module.exports = { app, server, io };