#!/usr/bin/env node

/**
 * Test script for the Agent Activity Monitor
 * Verifies that the monitoring system works correctly
 */

const AgentActivityMonitor = require('./agent-activity-monitor');

async function testMonitor() {
    console.log('Testing Agent Activity Monitor...');
    console.log('=================================');
    
    // Create a new monitor instance
    const monitor = new AgentActivityMonitor({
        logDirectory: './test-logs',
        checkInterval: 1000,
        hallucinationDetectionEnabled: true,
        verificationRequired: true
    });
    
    try {
        // Start the monitor
        await monitor.start();
        console.log('✓ Monitor started successfully');
        
        // Register some test agents
        await monitor.registerAgent('test-agent-1', 'content-generator');
        await monitor.registerAgent('test-agent-2', 'fact-checker');
        await monitor.registerAgent('test-agent-3', 'research-assistant');
        console.log('✓ Test agents registered');
        
        // Log some test activities
        await monitor.logActivity(
            'test-agent-1', 
            'content_generation', 
            { topic: 'AI productivity tools', length: 500 },
            'According to recent studies, 87% of businesses report increased productivity after implementing AI solutions. This represents a significant improvement over traditional methods.'
        );
        console.log('✓ Activity logged for test-agent-1');
        
        await monitor.logActivity(
            'test-agent-2', 
            'fact_checking', 
            { claim: '87% productivity increase', source: 'business_study_2026' },
            'The claim of 87% productivity increase is verified by the referenced business study from 2026, which surveyed 500 companies across multiple industries.'
        );
        console.log('✓ Activity logged for test-agent-2');
        
        // Simulate a high-risk activity (potential hallucination)
        await monitor.logActivity(
            'test-agent-3', 
            'market_analysis', 
            { sector: 'AI', timeframe: 'Q3_2026' },
            'The AI market will grow by 999% next quarter, making it the largest investment opportunity in history. All experts agree this is a guaranteed return.'
        );
        console.log('✓ High-risk activity logged for test-agent-3');
        
        // Wait a moment for processing
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Check the status
        const status = monitor.getStatus();
        console.log('✓ System status retrieved');
        console.log(`  Total Agents: ${status.totalAgents}`);
        console.log(`  Active Agents: ${status.activeAgents}`);
        console.log(`  Total Activities: ${status.totalActivities}`);
        console.log(`  Verification Requests: ${status.verificationRequests}`);
        
        // Get agent metrics
        const agentMetrics = monitor.getAgentMetrics();
        console.log('✓ Agent metrics retrieved');
        agentMetrics.forEach(agent => {
            console.log(`  ${agent.id}: ${agent.activityCount} activities, ${agent.verificationStatus} verification`);
        });
        
        // Get recent activities
        const recentActivities = monitor.getRecentActivities(10);
        console.log(`✓ Retrieved ${recentActivities.length} recent activities`);
        
        // Stop the monitor
        await monitor.stop();
        console.log('✓ Monitor stopped successfully');
        
        console.log('=================================');
        console.log('All tests passed! The monitoring system is working correctly.');
        
    } catch (error) {
        console.error('✗ Test failed:', error.message);
        // Ensure monitor is stopped even on failure
        try {
            await monitor.stop();
        } catch (stopError) {
            console.error('Error stopping monitor:', stopError.message);
        }
        process.exit(1);
    }
}

// Run the test
testMonitor();