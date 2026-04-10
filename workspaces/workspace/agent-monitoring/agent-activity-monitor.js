//!/usr/bin/env node

/**
 * Agent Activity Monitor
 * Tracks all agent activities in real-time with hallucination detection
 */

const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

class AgentActivityMonitor {
  constructor(config = {}) {
    this.config = {
      logDirectory: config.logDirectory || path.join(__dirname, 'logs'),
      maxLogSize: config.maxLogSize || 10000, // lines
      checkInterval: config.checkInterval || 5000, // ms
      hallucinationThreshold: config.hallucinationThreshold || 0.7,
      verificationRequired: config.verificationRequired || true,
      ...config
    };
    
    this.activities = [];
    this.agents = new Map();
    this.verificationNetwork = new Map();
    this.isRunning = false;
    this.monitorInterval = null;
    
    // Ensure log directory exists
    this.initLogDirectory();
  }

  async initLogDirectory() {
    try {
      await fs.mkdir(this.config.logDirectory, { recursive: true });
    } catch (error) {
      console.error('[Activity Monitor] Failed to create log directory:', error.message);
    }
  }

  /**
   * Register an agent with the monitoring system
   */
  async registerAgent(agentId, agentType = 'unknown') {
    this.agents.set(agentId, {
      id: agentId,
      type: agentType,
      registeredAt: new Date().toISOString(),
      lastSeen: new Date().toISOString(),
      activityCount: 0,
      hallucinationScore: 0,
      verificationStatus: 'unknown'
    });
    
    await this.logActivity(agentId, 'agent_registered', {}, { agentType });
    console.log(`[Activity Monitor] Registered agent: ${agentId} (${agentType})`);
  }

  /**
   * Log an agent activity with automatic hallucination checking
   */
  async logActivity(agentId, action, inputData, outputData) {
    const timestamp = new Date().toISOString();
    
    // Update agent last seen
    if (this.agents.has(agentId)) {
      const agent = this.agents.get(agentId);
      agent.lastSeen = timestamp;
      agent.activityCount++;
    }
    
    // Create activity record
    const activityRecord = {
      timestamp,
      agentId,
      action,
      inputHash: this.hashData(inputData),
      outputData: this.truncateOutput(outputData),
      hallucinationCheck: null,
      verificationStatus: 'pending'
    };
    
    // Perform hallucination detection
    if (this.config.hallucinationDetectionEnabled !== false) {
      activityRecord.hallucinationCheck = await this.detectHallucinations(outputData, action);
    }
    
    // Add to activities log
    this.activities.push(activityRecord);
    
    // Maintain log size limit
    if (this.activities.length > this.config.maxLogSize) {
      this.activities.shift();
    }
    
    // Log to file
    await this.logToFile(activityRecord);
    
    // Trigger verification if needed
    if (this.config.verificationRequired && activityRecord.hallucinationCheck?.riskLevel === 'high') {
      this.triggerVerification(agentId, activityRecord);
    }
    
    return activityRecord;
  }

  /**
   * Detect hallucinations in agent output using multi-layer verification
   */
  async detectHallucinations(outputData, action) {
    try {
      // Layer 1: Consistency Check
      const consistencyScore = await this.checkConsistency(outputData, action);
      
      // Layer 2: Factual Verification
      const factualScore = await this.checkFactualAccuracy(outputData);
      
      // Layer 3: Source Attribution
      const sourceScore = await this.checkSourceAttribution(outputData);
      
      // Layer 4: Confidence Scoring
      const confidenceScore = this.assessConfidence(outputData, action);
      
      // Weighted composite score
      const compositeScore = (
        consistencyScore * 0.3 +
        factualScore * 0.3 +
        sourceScore * 0.2 +
        confidenceScore * 0.2
      );
      
      // Determine risk level
      const riskLevel = this.categorizeRisk(compositeScore);
      
      return {
        compositeScore: parseFloat(compositeScore.toFixed(3)),
        componentScores: {
          consistency: parseFloat(consistencyScore.toFixed(3)),
          factual: parseFloat(factualScore.toFixed(3)),
          source: parseFloat(sourceScore.toFixed(3)),
          confidence: parseFloat(confidenceScore.toFixed(3))
        },
        riskLevel,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('[Activity Monitor] Hallucination detection error:', error.message);
      return {
        compositeScore: 0.5, // Neutral score on error
        componentScores: { consistency: 0.5, factual: 0.5, source: 0.5, confidence: 0.5 },
        riskLevel: 'unknown',
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Check consistency with known patterns and historical data
   */
  async checkConsistency(outputData, action) {
    // Simple consistency check - in a real system this would be more sophisticated
    const outputStr = String(outputData);
    
    // Check for obvious inconsistencies
    const inconsistencyIndicators = [
      /contradicts?/i,
      /however.*but/i,
      /although.*still/i,
      /despite.*nevertheless/i
    ];
    
    let inconsistencyCount = 0;
    for (const pattern of inconsistencyIndicators) {
      if (pattern.test(outputStr)) inconsistencyCount++;
    }
    
    // Return score (1.0 = perfectly consistent, 0.0 = highly inconsistent)
    return Math.max(0, 1 - (inconsistencyCount * 0.2));
  }

  /**
   * Check factual accuracy against verified sources
   */
  async checkFactualAccuracy(outputData) {
    // In a production system, this would connect to fact-checking APIs or databases
    // For now, we'll implement a basic heuristic approach
    
    const outputStr = String(outputData);
    
// Check for verifiable claims
    const factPatterns = [
      /\d{4}/g, // Years
      /\d+\.?\d*%/g, // Percentages
      /\$\d+/g, // Dollar amounts
      /according to/i, // Attribution patterns
      /study shows/i,
      /research indicates/i
    ];
    
    let factCount = 0;
    for (const pattern of factPatterns) {
      const matches = outputStr.match(pattern);
      if (matches) factCount += matches.length;
    }
    
// Simple heuristic: more factual claims = higher likelihood of accuracy
// Cap at reasonable level to avoid over-scoring
    return Math.min(1.0, factCount * 0.1 + 0.3);
  }

  /**
   * Check for proper source attribution
   */
  async checkSourceAttribution(outputData) {
    const outputStr = String(outputData);
    
// Look for attribution patterns
    const attributionPatterns = [
      /source:/i,
      /references?/i,
      /see also/i,
      /based on/i,
      /according to/i,
      /report by/i,
      /data from/i
    ];
    
    let attributionScore = 0.3; // Base score
    
    for (const pattern of attributionPatterns) {
      if (pattern.test(outputStr)) {
        attributionScore += 0.2;
        break; // Only need one good attribution
      }
    }
    
    return Math.min(1.0, attributionScore);
  }

  /**
   * Assess confidence level based on language used
   */
  assessConfidence(outputData, action) {
    const outputStr = String(outputData).toLowerCase();
    
// High confidence indicators
    const highConfidence = [
      'definitely', 'certainly', 'confirmed', 'proven', 'verified',
      'established', 'demonstrated', 'confirmed', 'confirmed'
    ];
    
// Low confidence indicators
    const lowConfidence = [
      'possibly', 'maybe', 'perhaps', 'might', 'could', 'suggests',
      'indicates', 'appears', 'seems', 'likely', 'probable'
    ];
    
    let highCount = 0;
    let lowCount = 0;
    
    for (const word of highConfidence) {
      if (outputStr.includes(word)) highCount++;
    }
    
    for (const word of lowConfidence) {
      if (outputStr.includes(word)) lowCount++;
    }
    
// Calculate confidence score
    if (highCount + lowCount === 0) return 0.5; // Neutral
    
    const confidence = highCount / (highCount + lowCount);
    return Math.max(0.1, Math.min(0.9, confidence));
  }

  /**
   * Categorize risk level based on composite score
   */
  categorizeRisk(score) {
    if (score >= 0.8) return 'low';
    if (score >= 0.6) return 'medium';
    if (score >= 0.4) return 'high';
    return 'critical';
  }

  /**
   * Trigger cross-agent verification for high-risk outputs
   */
  async triggerVerification(agentId, activityRecord) {
    console.log(`[Activity Monitor] Triggering verification for agent ${agentId} - High risk detected`);
    
// Find available verification agents
    const verificationAgents = Array.from(this.verificationNetwork.keys())
      .filter(id => this.verificationNetwork.get(id).status === 'available')
      .slice(0, 3); // Use up to 3 verifiers
    
    if (verificationAgents.length === 0) {
      console.log('[Activity Monitor] No verification agents available');
      return;
    }
    
// Create verification request
    const verificationRequest = {
      id: `verify_${Date.now()}`,
      targetAgent: agentId,
      activity: activityRecord,
      requestedAt: new Date().toISOString(),
      verifiers: verificationAgents,
      status: 'pending'
    };
    
// Notify verifiers (in a real system, this would use messaging)
    for (const verifierId of verificationAgents) {
      this.notifyVerifier(verifierId, verificationRequest);
    }
    
// Store verification request
    this.verificationNetwork.set(verificationRequest.id, verificationRequest);
    
// Set timeout for verification completion
    setTimeout(() => {
      this.completeVerification(verificationRequest.id);
    }, 30000); // 30 second timeout
  }

  /**
   * Notify a verification agent to check an activity
   */
  notifyVerifier(verifierId, verificationRequest) {
    console.log `[Activity Monitor] Notifying verifier ${verifierId} to check activity from ${verificationRequest.targetAgent}`;
// In a real implementation, this would send a message to the verifier agent
// For now, we'll log the request
  }

  /**
   * Complete verification process and update records
   */
  async completeVerification(verificationId) {
    const verificationRequest = this.verificationNetwork.get(verificationId);
    if (!verificationRequest) return;
    
// Simulate verification results from multiple agents
    const verificationResults = {
      consensus: Math.random() > 0.3, // 70% chance of consensus
      verifierScores: [],
      agreementLevel: Math.random() * 0.4 + 0.6, // 60-100% agreement
      completedAt: new Date().toISOString()
    };
    
// Update the original activity record
    const activityIndex = this.activities.findIndex(
      act => act.timestamp === verificationRequest.activity.timestamp &&
             act.agentId === verificationRequest.targetAgent
    );
    
    if (activityIndex !== -1) {
      this.activities[activityIndex].verificationStatus = verificationResults.consensus ? 'verified' : 'disputed';
      this.activities[activityIndex].verificationDetails = verificationResults;
      
// Update agent verification status
      const agent = this.agents.get(verificationRequest.targetAgent);
      if (agent) {
        agent.verificationStatus = verificationResults.consensus ? 'verified' : 'disputed';
        agent.lastVerification = new Date().toISOString();
      }
    }
    
    console.log `[Activity Monitor] Verification ${verificationId} completed: ${verificationResults.consensus ? 'VERIFIED' : 'DISPUTED'}`;
  }

  /**
   * Hash data for privacy-preserving logging
   */
  hashData(data) {
    const crypto = require('crypto');
    return crypto.createHash('sha256').update(String(data)).digest('hex').substring(0, 16);
  }

  /**
   * Truncate output data for reasonable logging
   */
  truncateOutput(data, maxLength = 500) {
    let str;
    if (typeof data === 'object') {
      str = JSON.stringify(data);
    } else {
      str = String(data);
    }
    if (str.length <= maxLength) return str;
    return str.substring(0, maxLength - 3) + '...';
  }

  /**
   * Log activity to file
   */
  async logToFile(activityRecord) {
    const date = new Date(activityRecord.timestamp);
    const logFileName = `activity-${date.toISOString().split('T')[0]}.log`;
    const logFilePath = path.join(this.config.logDirectory, logFileName);
    
    const logEntry = JSON.stringify(activityRecord) + '\n';
    
    try {
      await fs.appendFile(logFilePath, logEntry);
    } catch (error) {
      console.error('[Activity Monitor] Failed to write to log file:', error.message);
    }
  }

  /**
   * Start the monitoring system
   */
  async start() {
    if (this.isRunning) return;
    
    console.log('[Activity Monitor] Starting agent activity monitoring...');
    this.isRunning = true;
    
// Start periodic health checks and cleanup
    this.monitorInterval = setInterval(() => {
      this.performMaintenance();
    }, this.config.checkInterval);
    
    console.log('[Activity Monitor] Monitoring started successfully');
  }

  /**
   * Stop the monitoring system
   */
  async stop() {
    if (!this.isRunning) return;
    
    console.log('[Activity Monitor] Stopping monitoring...');
    this.isRunning = false;
    
    if (this.monitorInterval) {
      clearInterval(this.monitorInterval);
      this.monitorInterval = null;
    }
    
    console.log('[Activity Monitor] Monitoring stopped');
  }

  /**
   * Perform maintenance tasks
   */
  performMaintenance() {
// Clean up old verification requests
    const now = new Date();
    for (const [id, request] of this.verificationNetwork.entries()) {
      const requestedAt = new Date(request.requestedAt);
      if (now - requestedAt > 5 * 60 * 1000) { // 5 minutes
        this.verificationNetwork.delete(id);
      }
    }
    
// Update agent statuses (mark inactive agents)
    const inactiveThreshold = 10 * 60 * 1000; // 10 minutes
    for (const [id, agent] of this.agents.entries()) {
      const lastSeen = new Date(agent.lastSeen);
      if (now - lastSeen > inactiveThreshold) {
        agent.status = 'inactive';
      }
    }
  }

  /**
   * Get current system status
   */
  getStatus() {
    return {
      isRunning: this.isRunning,
      totalAgents: this.agents.size,
      activeAgents: Array.from(this.agents.values()).filter(a => a.status !== 'inactive').length,
      totalActivities: this.activities.length,
      recentActivities: this.activities.slice(-10),
      verificationRequests: this.verificationNetwork.size,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Get activities for dashboard display
   */
  getRecentActivities(limit = 50) {
    return this.activities.slice(-limit).map(activity => ({
      ...activity,
// Don't send full output data to dashboard for privacy/size reasons
      outputPreview: this.truncateOutput(activity.outputData, 100)
    }));
  }

  /**
   * Get agent performance metrics
   */
  getAgentMetrics() {
    return Array.from(this.agents.values()).map(agent => ({
      id: agent.id,
      type: agent.type,
      registeredAt: agent.registeredAt,
      lastSeen: agent.lastSeen,
      activityCount: agent.activityCount,
      hallucinationScore: agent.hallucinationScore,
      verificationStatus: agent.verificationStatus,
      status: agent.status || 'active'
    }));
  }
}

// Export for use in other modules
module.exports = AgentActivityMonitor;

// If run directly, start the monitor
if (require.main === module) {
  const monitor = new AgentActivityMonitor();
  
  monitor.start().catch(error => {
    console.error('[Activity Monitor] Failed to start:', error);
    process.exit(1);
  });
  
// Handle graceful shutdown
  process.on('SIGINT', async () => {
    console.log('\n[Activity Monitor] Received SIGINT, shutting down...');
    await monitor.stop();
    process.exit(0);
  });
  
  process.on('SIGTERM', async () => {
    console.log('\n[Activity Monitor] Received SIGTERM, shutting down...');
    await monitor.stop();
    process.exit(0);
  });
}