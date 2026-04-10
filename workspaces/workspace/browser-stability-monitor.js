#!/usr/bin/env node

/**
 * Browser Stability Monitor
 * Monitors and maintains browser health for autonomous operations
 */

const { spawn, exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

class BrowserStabilityMonitor {
  constructor(config = {}) {
    this.config = {
      chromePort: config.chromePort || 9223,
      firefoxPort: config.firefoxPort || 9224,
      checkInterval: config.checkInterval || 30000, // 30 seconds
      maxRestartAttempts: config.maxRestartAttempts || 3,
      restartDelay: config.restartDelay || 5000,
      logFile: config.logFile || path.join(__dirname, 'browser-monitor.log'),
      ...config
    };
    
    this.isRunning = false;
    this.checkInterval = null;
    this.restartAttempts = 0;
    this.lastHealthCheck = null;
    this.browserProcess = null;
  }

  async start() {
    if (this.isRunning) return;
    
    console.log('[Browser Monitor] Starting browser stability monitoring...');
    this.isRunning = true;
    
    // Initial browser check and startup
    await this.ensureBrowserRunning();
    
    // Start health monitoring
    this.startHealthMonitoring();
    
    console.log('[Browser Monitor] Monitoring started successfully');
  }

  async stop() {
    if (!this.isRunning) return;
    
    console.log('[Browser Monitor] Stopping monitoring...');
    this.isRunning = false;
    
    if (this.checkInterval) {
      clearInterval(this.checkInterval);
      this.checkInterval = null;
    }
    
    if (this.browserProcess) {
      this.browserProcess.kill();
      this.browserProcess = null;
    }
    
    console.log('[Browser Monitor] Monitoring stopped');
  }

  async ensureBrowserRunning() {
    try {
      const isHealthy = await this.checkBrowserHealth();
      
      if (!isHealthy) {
        console.log('[Browser Monitor] Browser not healthy, starting...');
        await this.startBrowser();
      } else {
        console.log('[Browser Monitor] Browser is healthy');
      }
    } catch (error) {
      console.error('[Browser Monitor] Error ensuring browser:', error.message);
      await this.startBrowser();
    }
  }

  async startBrowser() {
    if (this.restartAttempts >= this.config.maxRestartAttempts) {
      console.error('[Browser Monitor] Max restart attempts reached');
      throw new Error('Browser restart limit exceeded');
    }
    
    this.restartAttempts++;
    console.log(`[Browser Monitor] Starting browser (attempt ${this.restartAttempts})...`);
    
    try {
      // Kill any existing Chrome processes on our port
      await this.killExistingBrowser();
      
      // Start Chrome with debugging port
      this.browserProcess = spawn('google-chrome', [
        `--remote-debugging-port=${this.config.chromePort}`,
        '--user-data-dir=/tmp/openclaw-browser-stable',
        '--no-first-run',
        '--no-default-browser-check',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        '--disable-backgrounding-occluded-windows',
        '--enable-features=NetworkService,NetworkServiceInProcess',
        '--disable-gpu', // Sometimes helps with stability
        '--no-sandbox', // For testing environments
        '--disable-dev-shm-usage' // Helps with memory issues
      ], {
        stdio: ['ignore', 'pipe', 'pipe'],
        detached: true
      });
      
      // Wait for browser to start
      await this.waitForBrowserStartup();
      
      console.log('[Browser Monitor] Browser started successfully');
      this.restartAttempts = 0; // Reset on success
      
    } catch (error) {
      console.error('[Browser Monitor] Failed to start browser:', error.message);
      
      if (this.restartAttempts < this.config.maxRestartAttempts) {
        console.log(`[Browser Monitor] Retrying in ${this.config.restartDelay}ms...`);
        await this.sleep(this.config.restartDelay);
        return this.startBrowser();
      }
      
      throw error;
    }
  }

  async killExistingBrowser() {
    try {
      // Find and kill Chrome processes using our debugging port
      const { stdout } = await execAsync(`lsof -ti :${this.config.chromePort} || true`);
      const pids = stdout.trim().split('\n').filter(pid => pid.length > 0);
      
      for (const pid of pids) {
        try {
          process.kill(parseInt(pid), 'SIGTERM');
          console.log(`[Browser Monitor] Killed existing browser process: ${pid}`);
        } catch (error) {
          // Process might already be dead
        }
      }
      
      // Give processes time to terminate
      await this.sleep(2000);
      
    } catch (error) {
      // Ignore errors in cleanup
    }
  }

  async waitForBrowserStartup() {
    const maxWaitTime = 30000; // 30 seconds
    const checkInterval = 1000; // 1 second
    const startTime = Date.now();
    
    while (Date.now() - startTime < maxWaitTime) {
      try {
        const isHealthy = await this.checkBrowserHealth();
        if (isHealthy) {
          return;
        }
      } catch (error) {
        // Browser not ready yet
      }
      
      await this.sleep(checkInterval);
    }
    
    throw new Error('Browser startup timeout');
  }

  async checkBrowserHealth() {
    try {
      // Check if Chrome debugging port is accessible
      const response = await fetch(`http://127.0.0.1:${this.config.chromePort}/json/version`, {
        method: 'GET',
        timeout: 5000
      });
      
      if (response.ok) {
        const data = await response.json();
        this.lastHealthCheck = new Date().toISOString();
        return true;
      }
      
      return false;
    } catch (error) {
      return false;
    }
  }

  startHealthMonitoring() {
    this.checkInterval = setInterval(async () => {
      if (!this.isRunning) return;
      
      try {
        const isHealthy = await this.checkBrowserHealth();
        
        if (!isHealthy) {
          console.warn('[Browser Monitor] Browser health check failed');
          await this.handleBrowserFailure();
        } else {
          console.log('[Browser Monitor] Browser health check passed');
        }
        
      } catch (error) {
        console.error('[Browser Monitor] Health check error:', error.message);
        await this.handleBrowserFailure();
      }
    }, this.config.checkInterval);
  }

  async handleBrowserFailure() {
    console.log('[Browser Monitor] Handling browser failure...');
    
    try {
      await this.ensureBrowserRunning();
    } catch (error) {
      console.error('[Browser Monitor] Failed to recover browser:', error.message);
      this.logError('Browser recovery failed', error);
    }
  }

  logError(message, error) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      message,
      error: error.message,
      stack: error.stack
    };
    
    // Simple file logging
    fs.appendFile(this.config.logFile, JSON.stringify(logEntry) + '\n').catch(err => {
      console.error('[Browser Monitor] Failed to log error:', err.message);
    });
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getStatus() {
    return {
      isRunning: this.isRunning,
      lastHealthCheck: this.lastHealthCheck,
      restartAttempts: this.restartAttempts,
      browserPort: this.config.chromePort,
      uptime: this.isRunning ? Date.now() - this.startTime : 0
    };
  }
}

// Create and export monitor instance
const monitor = new BrowserStabilityMonitor({
  checkInterval: 15000, // Check every 15 seconds
  maxRestartAttempts: 5,
  debug: true
});

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n[Browser Monitor] Received SIGINT, shutting down...');
  await monitor.stop();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('\n[Browser Monitor] Received SIGTERM, shutting down...');
  await monitor.stop();
  process.exit(0);
});

// Start monitoring if run directly
if (require.main === module) {
  monitor.start().catch(error => {
    console.error('[Browser Monitor] Failed to start:', error);
    process.exit(1);
  });
}

module.exports = BrowserStabilityMonitor;