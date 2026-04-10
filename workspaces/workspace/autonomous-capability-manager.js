/**
 * Autonomous Capability Manager
 * Coordinates all autonomous systems for daily improvement
 * Original implementation - no proprietary cloning
 */

const fs = require('fs').promises;
const path = require('path');
const RevenueAutomationSystem = require('./revenue-automation-system');
const BrowserStabilityMonitor = require('./browser-stability-monitor');

class AutonomousCapabilityManager {
  constructor(config = {}) {
    this.config = {
      dailyImprovementTime: config.dailyImprovementTime || '09:00', // 9 AM GMT+8
      revenueCheckInterval: config.revenueCheckInterval || 3600000, // 1 hour
      browserCheckInterval: config.browserCheckInterval || 30000, // 30 seconds
      improvementLogFile: config.improvementLogFile || path.join(__dirname, 'capability-improvements.json'),
      ...config
    };
    
    this.systems = {
      revenue: new RevenueAutomationSystem(),
      browser: new BrowserStabilityMonitor()
    };
    
    this.isRunning = false;
    this.dailyTimer = null;
    this.improvementLog = [];
  }

  async initialize() {
    console.log('[Autonomous Manager] Initializing autonomous capability systems...');
    
    // Initialize all subsystems
    await this.systems.revenue.initialize();
    
    // Load improvement log
    await this.loadImprovementLog();
    
    console.log('[Autonomous Manager] Autonomous systems initialized');
  }

  async start() {
    if (this.isRunning) return;
    
    console.log('[Autonomous Manager] Starting autonomous capability management...');
    this.isRunning = true;
    
    // Start browser monitoring immediately
    await this.systems.browser.start();
    
    // Start revenue automation
    await this.systems.revenue.start();
    
    // Schedule daily improvement routine
    this.scheduleDailyImprovement();
    
    // Run initial capability assessment
    await this.assessCurrentCapabilities();
    
    console.log('[Autonomous Manager] Autonomous capability management started');
  }

  async stop() {
    if (!this.isRunning) return;
    
    console.log('[Autonomous Manager] Stopping autonomous systems...');
    this.isRunning = false;
    
    if (this.dailyTimer) {
      clearTimeout(this.dailyTimer);
      this.dailyTimer = null;
    }
    
    await this.systems.revenue.stop();
    await this.systems.browser.stop();
    
    console.log('[Autonomous Manager] Autonomous systems stopped');
  }

  scheduleDailyImprovement() {
    const scheduleNext = () => {
      const now = new Date();
      const [hour, minute] = this.config.dailyImprovementTime.split(':');
      const nextImprovement = new Date(now);
      nextImprovement.setHours(parseInt(hour), parseInt(minute), 0, 0);
      
      if (nextImprovement <= now) {
        nextImprovement.setDate(nextImprovement.getDate() + 1);
      }
      
      const delay = nextImprovement - now;
      
      console.log(`[Autonomous Manager] Next improvement scheduled for ${nextImprovement.toLocaleString()}`);
      
      this.dailyTimer = setTimeout(async () => {
        await this.executeDailyImprovement();
        scheduleNext(); // Schedule next day's improvement
      }, delay);
    };
    
    scheduleNext();
  }

  async executeDailyImprovement() {
    console.log('\n🚀 [Autonomous Manager] Daily Capability Improvement Starting...\n');
    
    const improvementDate = new Date().toISOString().split('T')[0];
    
    try {
      // 1. Morning Assessment (9 AM GMT+8)
      console.log('📊 [Autonomous Manager] Phase 1: Morning Assessment');
      await this.performMorningAssessment(improvementDate);
      
      // 2. Browser Health Check
      console.log('🌐 [Autonomous Manager] Phase 2: Browser Health Optimization');
      await this.optimizeBrowserHealth(improvementDate);
      
      // 3. Revenue System Check
      console.log('💰 [Autonomous Manager] Phase 3: Revenue System Optimization');
      await this.optimizeRevenueSystem(improvementDate);
      
      // 4. New Capability Implementation
      console.log('⚡ [Autonomous Manager] Phase 4: New Capability Implementation');
      await this.implementNewCapability(improvementDate);
      
      // 5. Performance Optimization
      console.log('⚙️ [Autonomous Manager] Phase 5: Performance Optimization');
      await this.optimizePerformance(improvementDate);
      
      // 6. Evening Revenue Focus
      console.log('🎯 [Autonomous Manager] Phase 6: Revenue Generation Focus');
      await this.focusOnRevenueGeneration(improvementDate);
      
      console.log('\n✅ [Autonomous Manager] Daily improvement completed successfully!\n');
      
    } catch (error) {
      console.error('\n❌ [Autonomous Manager] Daily improvement failed:', error.message);
      this.logImprovement('daily_improvement_failed', { error: error.message, date: improvementDate });
    }
  }

  async performMorningAssessment(date) {
    console.log('  📈 Checking system health...');
    
    const assessment = {
      timestamp: new Date().toISOString(),
      browserStatus: this.systems.browser.getStatus(),
      revenueStatus: this.systems.revenue.getRevenueStatus(),
      systemUptime: process.uptime(),
      memoryUsage: process.memoryUsage(),
      improvements: []
    };
    
    // Check browser stability
    if (!assessment.browserStatus.isRunning) {
      console.log('  🔧 Starting browser monitor...');
      await this.systems.browser.start();
      assessment.improvements.push('browser_monitor_started');
    }
    
    // Check revenue system
    if (assessment.revenueStatus.paymentStatus !== 'ready') {
      console.log('  🔧 Checking payment integration...');
      const paymentCheck = await this.systems.revenue.checkPaymentIntegration();
      assessment.improvements.push(`payment_status_${paymentCheck.status}`);
    }
    
    this.logImprovement('morning_assessment', assessment);
    console.log('  ✅ Morning assessment completed');
  }

  async assessCurrentCapabilities() {
    console.log('[Autonomous Manager] Assessing current capabilities...');
    
    const assessment = {
      timestamp: new Date().toISOString(),
      systems: {
        revenue: this.systems.revenue.getRevenueStatus(),
        browser: this.systems.browser.getStatus()
      },
      capabilities: {
        browser_automation: this.systems.browser.isRunning ? 'operational' : 'needs_attention',
        revenue_generation: 'pending_payment_integration',
        content_creation: 'ready_to_implement',
        lead_generation: 'ready_to_implement',
        analytics_tracking: 'ready_to_implement'
      },
      next_actions: [
        'Complete Stripe business verification',
        'Implement content creation automation',
        'Deploy lead generation system',
        'Set up analytics tracking'
      ]
    };
    
    console.log('[Autonomous Manager] Current capability assessment:', assessment);
    this.logImprovement('capability_assessment', assessment);
  }

  // Logging and tracking
  async loadImprovementLog() {
    try {
      const data = await fs.readFile(this.config.improvementLogFile, 'utf8');
      this.improvementLog = JSON.parse(data);
    } catch (error) {
      this.improvementLog = [];
    }
  }

  async saveImprovementLog() {
    await fs.writeFile(this.config.improvementLogFile, JSON.stringify(this.improvementLog, null, 2));
  }

  logImprovement(type, data) {
    const entry = {
      timestamp: new Date().toISOString(),
      type,
      data,
      sessionId: process.pid
    };
    
    this.improvementLog.push(entry);
    
    // Keep only last 1000 entries
    if (this.improvementLog.length > 1000) {
      this.improvementLog = this.improvementLog.slice(-1000);
    }
    
    this.saveImprovementLog().catch(console.error);
  }

  getSystemStatus() {
    return {
      isRunning: this.isRunning,
      systems: {
        revenue: this.systems.revenue.getRevenueStatus(),
        browser: this.systems.browser.getStatus()
      },
      nextImprovement: this.getNextImprovementTime(),
      improvementCount: this.improvementLog.length
    };
  }

  getNextImprovementTime() {
    if (!this.dailyTimer) return null;
    
    const now = new Date();
    const [hour, minute] = this.config.dailyImprovementTime.split(':');
    const next = new Date(now);
    next.setHours(parseInt(hour), parseInt(minute), 0, 0);
    
    if (next <= now) {
      next.setDate(next.getDate() + 1);
    }
    
    return next.toISOString();
  }
}

module.exports = AutonomousCapabilityManager;