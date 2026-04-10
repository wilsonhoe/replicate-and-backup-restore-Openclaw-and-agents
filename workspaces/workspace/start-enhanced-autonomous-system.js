#!/usr/bin/env node

/**
 * Enhanced Autonomous Capability System Entry Point
 * Now includes immediate revenue generation without Stripe dependency
 * Focuses on revenue TODAY while Stripe verification completes
 */

const EnhancedAutonomousCapabilityManager = require('./enhanced-autonomous-capability-manager');

async function main() {
  console.log('🚀 Starting ENHANCED Autonomous Capability System...');
  console.log('📅 Focus: Immediate revenue + daily autonomous improvement');
  console.log('🎯 Target: $100 immediate + $1K/month through automation');
  console.log('⚡ Strategy: Revenue TODAY while Stripe verification completes');
  console.log('');
  
  const manager = new EnhancedAutonomousCapabilityManager({
    dailyImprovementTime: '09:00', // 9 AM GMT+8
    debug: true
  });
  
  try {
    // Initialize systems
    console.log('🔧 Initializing enhanced systems...');
    await manager.initialize();
    
    // Start autonomous operations
    console.log('🔄 Starting enhanced autonomous operations...');
    await manager.start();
    
    // Display enhanced status
    const status = manager.getSystemStatus();
    console.log('');
    console.log('📊 Enhanced System Status:');
    console.log(`  Revenue Progress: ${status.systems.revenue.targetProgress}`);
    console.log(`  Immediate Revenue Progress: ${status.systems.immediateRevenue.immediateProgress}`);
    console.log(`  Browser Status: ${status.systems.browser.isRunning ? 'Running' : 'Stopped'}`);
    console.log(`  Next Improvement: ${new Date(status.nextImprovement).toLocaleString()}`);
    console.log(`  Improvements Logged: ${status.improvementCount}`);
    console.log(`  Products Created: ${status.systems.immediateRevenue.products}`);
    
    console.log('');
    console.log('✅ ENHANCED autonomous capability system started successfully!');
    console.log('🔄 System will improve automatically every day at 9 AM GMT+8');
    console.log('💰 Focus: Immediate revenue + browser stability + daily capability enhancement');
    console.log('⚡ Revenue Strategy: Multiple platforms (Gumroad, Affiliate, Services) + Stripe when ready');
    
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
    console.error('❌ Failed to start enhanced autonomous system:', error);
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