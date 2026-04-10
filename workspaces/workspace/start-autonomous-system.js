#!/usr/bin/env node

/**
 * Autonomous Capability System Entry Point
 * Original implementation for daily autonomous improvement
 * Focuses on revenue generation and browser stability
 */

const AutonomousCapabilityManager = require('./autonomous-capability-manager');

async function main() {
  console.log('🚀 Starting Autonomous Capability System...');
  console.log('📅 Focus: Daily improvement for revenue generation');
  console.log('🎯 Target: $1K+/month through automation');
  console.log('');
  
  const manager = new AutonomousCapabilityManager({
    dailyImprovementTime: '09:00', // 9 AM GMT+8
    debug: true
  });
  
  try {
    // Initialize systems
    console.log('🔧 Initializing systems...');
    await manager.initialize();
    
    // Start autonomous operations
    console.log('🔄 Starting autonomous operations...');
    await manager.start();
    
    // Display initial status
    const status = manager.getSystemStatus();
    console.log('');
    console.log('📊 System Status:');
    console.log(`  Revenue Progress: ${status.systems.revenue.targetProgress}`);
    console.log(`  Browser Status: ${status.systems.browser.isRunning ? 'Running' : 'Stopped'}`);
    console.log(`  Next Improvement: ${new Date(status.nextImprovement).toLocaleString()}`);
    console.log(`  Improvements Logged: ${status.improvementCount}`);
    
    console.log('');
    console.log('✅ Autonomous capability system started successfully!');
    console.log('🔄 System will improve automatically every day at 9 AM GMT+8');
    console.log('📈 Focus: Browser stability, revenue generation, daily capability enhancement');
    
    // Handle graceful shutdown
    process.on('SIGINT', async () => {
      console.log('\n🛑 Received SIGINT, shutting down gracefully...');
      await manager.stop();
      process.exit(0);
    });
    
    process.on('SIGTERM', async () => {
      console.log('\n🛑 Received SIGTERM, shutting down gracefully...');
      await manager.stop();
      process.exit(0);
    });
    
  } catch (error) {
    console.error('❌ Failed to start autonomous system:', error);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('Unhandled error:', error);
    process.exit(1);
  });
}

module.exports = { main };