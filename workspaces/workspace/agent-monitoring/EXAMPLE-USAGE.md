# Example Usage: Integrating Agent Activity Monitor with OpenClaw Agents

This document shows how to integrate the Agent Activity Monitor with existing OpenClaw agents.

## Basic Integration

### 1. Install the Monitoring System
```bash
# In your OpenClaw workspace
cd agent-monitoring
npm install
```

### 2. Import and Initialize in Your Agent
Add this to your agent's initialization code:

```javascript
// At the top of your agent file
const path = require('path');
const AgentActivityMonitor = require('./agent-monitoring/agent-activity-monitor');

// Initialize the monitor (typically in agent constructor or init method)
this.activityMonitor = new AgentActivityMonitor({
    logDirectory: path.join(__dirname, '..', 'agent-monitoring', 'logs'),
    checkInterval: 5000, // 5 second health checks
    hallucinationThreshold: 0.7, // Trigger verification at 70%+ risk
    verificationRequired: true
});

// Register your agent with the monitor
await this.activityMonitor.registerAgent(
    this.agentId || 'unknown-agent', 
    this.agentType || 'general-purpose'
);
```

### 3. Log Agent Activities
Replace your existing action logging with calls to the monitor:

```javascript
// Instead of direct logging, use the monitor:
await this.activityMonitor.logActivity(
    this.agentId,
    actionName, 
    inputData,  // Parameters/data passed to the action
    outputData  // Results/response from the action
);

// Example implementations:
```

## Example Integrations

### Content Generation Agent
```javascript
async function generateBlogPost(topic, audience) {
    const input = { topic, audience, timestamp: Date.now() };
    
    // Your existing content generation logic
    const output = await this.aiModel.generateContent({
        prompt: `Write a blog post about ${topic} for ${audience}`,
        maxTokens: 1500,
        temperature: 0.7
    });
    
    // Log the activity with the monitor
    await this.activityMonitor.logActivity(
        this.agentId,
        'blog_post_generation',
        input,
        {
            content: output,
            wordCount: output.split(/\s+/).length,
            generationTime: Date.now() - input.timestamp
        }
    );
    
    return output;
}
```

### Research Analysis Agent
```javascript
async function analyzeMarketData(sector, timeframe) {
    const input = { sector, timeframe, dataPoints: 0 };
    
    // Your existing research logic
    const rawData = await this.dataCollector.fetchMarketData(sector, timeframe);
    const analysis = await this.analystModel.processData(rawData);
    
    // Log the activity
    await this.activityMonitor.logActivity(
        this.agentId,
        'market_analysis',
        input,
        {
            sector: sector,
            timeframe: timeframe,
            dataPoints: rawData.length,
            keyFindings: analysis.keyFindings,
            confidenceScore: analysis.confidence,
            recommendations: analysis.recommendations
        }
    );
    
    return analysis;
}
```

### Social Media Posting Agent
```javascript
async function createSocialPost(platform, content, hashtags) {
    const input = { platform, contentLength: content.length, hashtagCount: hashtags.length };
    
    // Your existing posting logic
    const postResult = await this.socialApi.postContent(platform, {
        content: content,
        hashtags: hashtags,
        scheduleTime: null // Post immediately
    });
    
    // Log the activity
    await this.activityMonitor.logActivity(
        this.agentId,
        'social_media_post',
        input,
        {
            platform: platform,
            postId: postResult.id,
            engagementPredicted: postResult.engagementEstimate,
            postedAt: new Date().toISOString(),
            contentLength: content.length
        }
    );
    
    return postResult;
}
```

## Advanced Integration Patterns

### Conditional Monitoring
For performance-sensitive operations, you can conditionally enable monitoring:

```javascript
async function performAction(actionName, inputData) {
    // Skip monitoring for very fast, low-risk operations
    const shouldMonitor = !(actionName === 'internal_calculation' && 
                           Object.keys(inputData).length < 3);
    
    let outputData;
    if (shouldMonitor) {
        const startTime = Date.now();
        outputData = await this.coreLogic(actionName, inputData);
        const processingTime = Date.now() - startTime;
        
        // Add performance metrics to output
        outputData = {
            ...outputData,
            _monitoring: { processingTimeMs: processingTime }
        };
        
        await this.activityMonitor.logActivity(
            this.agentId,
            actionName,
            inputData,
            outputData
        );
    } else {
        outputData = await this.coreLogic(actionName, inputData);
    }
    
    return outputData;
}
```

### Batch Activity Logging
For agents that perform many similar actions:

```javascript
class BatchActivityLogger {
    constructor(monitor, agentId, batchSize = 10) {
        this.monitor = monitor;
        this.agentId = agentId;
        this.batchSize = batchSize;
        this.pendingActivities = [];
    }
    
    async logActivity(actionName, inputData, outputData) {
        this.pendingActivities.push({
            timestamp: new Date().toISOString(),
            agentId: this.agentId,
            action: actionName,
            inputHash: this.hashData(inputData),
            outputData: this.truncateOutput(outputData, 200),
            hallucinationCheck: null, // Will be filled by monitor
            verificationStatus: 'pending'
        });
        
        if (this.pendingActivities.length >= this.batchSize) {
            await this.flushBatch();
        }
    }
    
    async flushBatch() {
        if (this.pendingActivities.length === 0) return;
        
        // Process batch through monitor (simplified for example)
        for (const activity of this.pendingActivities) {
            await this.monitor.logActivity(
                activity.agentId,
                activity.action,
                {}, // Input already hashed
                activity.outputData
            );
        }
        
        this.pendingActivities = [];
    }
    
    hashData(data) {
        const crypto = require('crypto');
        return crypto.createHash('sha256').update(String(data)).digest().hex().substring(0, 16);
    }
    
    truncateOutput(data, maxLength) {
        const str = String(data);
        return str.length <= maxLength ? str : str.substring(0, maxLength - 3) + '...';
    }
}
```

## Error Handling and Resilience

### Graceful Degradation
Ensure your agent continues to work even if the monitoring system is unavailable:

```javascript
async function safeLogActivity(agentId, action, input, output) {
    try {
        if (this.activityMonitor && this.activityMonitor.isRunning) {
            await this.activityMonitor.logActivity(agentId, action, input, output);
        }
    } catch (error) {
        // Log to local file as fallback
        const fallbackLog = `./logs/fallback-${agentId}.log`;
        const logEntry = `[${new Date().toISOString()}] ${agentId}.${action}: ${JSON.stringify({input, output})}\n`;
        require('fs').appendFileSync(fallbackLog, logEntry);
        
        // Optionally alert administrator
        console.warn(`Monitoring failed for ${agentId}.${action}: ${error.message}`);
    }
}
```

### Health Checks
Periodically verify the monitoring system is responsive:

```javascript
async function checkMonitorHealth() {
    try {
        if (!this.activityMonitor) return false;
        
        const status = this.activityMonitor.getStatus();
        return status.isRunning && 
               status.totalAgents >= 0 && 
               Date.now() - new Date(status.lastUpdate || 0).getTime() < 30000; // Within 30s
    } catch (error) {
        return false;
    }
}
```

## Best Practices

### 1. Consistent Agent Identification
Use stable, unique agent IDs:
```javascript
// Good: Uses predictable, unique identifiers
this.agentId = `content-agent-${this.instanceId || process.pid}`;

// Avoid: Changing or non-unique identifiers  
// this.agentId = Math.random().toString(36).substring(2); // ❌ Bad
```

### 2. Meaningful Action Names
Use descriptive, consistent action names:
```javascript
// Good: Clear, standardized action names
await monitor.logActivity(agentId, 'content_generation', input, output);
await monitor.logActivity(agentId, 'fact_checking', input, output);
await monitor.logActivity(agentId, 'data_analysis', input, output);

// Avoid: Vague or inconsistent names
// await monitor.logActivity(agentId, 'do_stuff', input, output); // ❌ Bad
// await monitor.logActivity(agentId, 'processThing', input, output); // ❌ Bad
```

### 3. Proper Data Structure
Structure your input/output data for meaningful analysis:
```javascript
// Good: Structured data that can be analyzed
const input = {
    topic: 'artificial intelligence',
    audience: 'cto_level',
    wordCountTarget: 1000,
    tone: 'professional',
    references: ['study1', 'study2']
};

const output = {
    content: 'Generated blog post content...',
    wordCount: 1045,
    referencesUsed: ['study1'],
    toneMatch: 0.92,
    readabilityScore: 8.5
};

// Avoid: Unstructured strings or overly complex objects
// await monitor.logActivity(agentId, 'action', 'unstructured string', {/* complex nested obj */}); // ❌ Less useful
```

### 4. Regular Maintenance
Include monitoring health checks in your agent's maintenance routines:
```javascript
// In your agent's maintenance cycle
async function performMaintenance() {
    // ... other maintenance tasks ...
    
    // Check monitoring system health
    const monitorHealthy = await this.checkMonitorHealth();
    if (!monitorHealthy) {
        this.logWarning('Activity monitoring system appears unhealthy');
        // Attempt restart or notify administrator
    }
}
```

## Troubleshooting Common Issues

### "Monitor not recording activities"
- Verify agent is calling `registerAgent()` before `logActivity()`
- Check that `isRunning` property is true on the monitor instance
- Verify log directory is writable
- Check for JavaScript errors in agent logs

### "Dashboard shows no data"
- Confirm WebSocket connection is working (check browser console)
- Verify server is running and accessible on configured port
- Check that activities are actually being logged (check log files)
- Ensure agent registration succeeded

### "High resource usage"
- Check log file sizes and consider reducing `maxLogSize`
- Verify verification network isn't creating excessive processes
- Monitor Node.js memory usage with standard tools
- Consider increasing `checkInterval` for less frequent health checks

### "False positive hallucination alerts"
- Adjust `hallucinationThreshold` based on your agent's typical output quality
- Review component scores to see which layer is triggering alerts
- Consider domain-specific adjustments to detection algorithms
- Add whitelisting for known-good output patterns

## Complete Example: Minimal Agent Integration

Here's a complete minimal example showing how to add monitoring to a basic agent:

```javascript
// basic-monitored-agent.js
const path = require('path');
const AgentActivityMonitor = require('./agent-monitoring/agent-activity-monitor');

class BasicMonitoredAgent {
    constructor(agentId, agentType) {
        this.agentId = agentId;
        this.agentType = agentType;
        this.activityMonitor = null;
        this.isInitialized = false;
    }
    
    async initialize() {
        // Initialize monitoring system
        this.activityMonitor = new AgentActivityMonitor({
            logDirectory: path.join(__dirname, '..', 'agent-monitoring', 'logs'),
            checkInterval: 5000
        });
        
        await this.activityMonitor.start();
        
        // Register this agent
        await this.activityMonitor.registerAgent(
            this.agentId,
            this.agentType
        );
        
        this.isInitialized = true;
        console.log(`Agent ${this.agentId} initialized with monitoring`);
    }
    
    async performAction(actionName, inputData) {
        if (!this.isInitialized) {
            throw new Error('Agent not initialized');
        }
        
        // Simulate agent work
        await this.simulateWork(100); // 100ms work simulation
        
        // Generate output based on action
        const outputData = this.generateOutput(actionName, inputData);
        
        // Log activity with monitoring
        await this.activityMonitor.logActivity(
            this.agentId,
            actionName,
            inputData,
            outputData
        );
        
        return outputData;
    }
    
    async simulateWork(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    generateOutput(action, input) {
        switch(action) {
            case 'content_generation':
                return {
                    content: `Generated content about ${input.topic || 'unknown topic'}`,
                    wordCount: Math.floor(Math.random() * 500) + 100,
                    createdAt: new Date().toISOString()
                };
            case 'data_analysis':
                return {
                    insights: [`Insight 1 about ${input.subject || 'topic'}`],
                    confidence: Math.random() * 0.4 + 0.6, // 0.6-1.0
                    dataPoints: input.sampleSize || 100
                };
            default:
                return {
                    action: action,
                    processedAt: new Date().toISOString(),
                    success: true
                };
        }
    }
    
    async shutdown() {
        if (this.activityMonitor && this.activityMonitor.isInitialized) {
            await this.activityMonitor.stop();
        }
    }
}

// Usage example
async function runDemo() {
    const agent = new BasicMonitoredAgent('demo-agent-001', 'demonstration');
    
    try {
        await agent.initialize();
        
        // Perform some actions
        await agent.performAction('content_generation', { 
            topic: 'artificial intelligence', 
            audience: 'technical' 
        });
        
        await agent.performAction('data_analysis', { 
            subject: 'market trends', 
            sampleSize: 1500 
        });
        
        await agent.performAction('content_generation', { 
            topic: 'renewable energy', 
            audience: 'executives' 
        });
        
        console.log('Demo completed successfully');
        
    } catch (error) {
        console.error('Demo failed:', error.message);
    } finally {
        await agent.shutdown();
    }
}

// Run if called directly
if (require.main === module) {
    runDemo().catch(console.error);
}

module.exports = BasicMonitoredAgent;
```

## Verification That Integration Works

After integrating the monitor, you should see:

1. **Agent Registration**: New agent appears in dashboard agent overview
2. **Activity Logging**: Actions appear in real-time activity feed
3. **Risk Assessment**: Each activity shows a hallucination risk percentage
4. **Verification Triggering**: High-risk activities trigger validation processes
5. **System Metrics**: Counters update for total agents and activities
6. **Live Updates**: Dashboard refreshes automatically without manual refresh

The monitoring system is designed to be lightweight and non-blocking, so it should not significantly impact your agent's performance while providing valuable visibility into agent behavior and output quality.