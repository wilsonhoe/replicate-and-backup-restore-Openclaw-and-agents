# OpenClaw Agent Activity Monitor

Real-time monitoring system for tracking agent activities with built-in hallucination detection and cross-agent verification capabilities.

## Overview

This monitoring system provides real-time visibility into agent activities within the OpenClaw ecosystem, featuring:

- **Real-time Activity Tracking**: Monitor all agent actions as they happen
- **Multi-layer Hallucination Detection**: Advanced verification system to catch false or misleading outputs
- **Cross-Agent Verification Network**: Agents verify each other's work for increased reliability
- **Live Dashboard**: Web-based interface for monitoring system health and agent performance
- **Automatic Alerting**: Immediate notifications for high-risk activities

## Features

### Activity Monitoring
- Tracks all agent tool calls, inputs, and outputs
- Maintains chronological activity logs
- Privacy-preserving hashing of sensitive data
- Configurable log retention policies

### Hallucination Detection
- **Consistency Checking**: Identifies internal contradictions in outputs
- **Factual Verification**: Validates claims against known patterns
- **Source Attribution**: Checks for proper citation and referencing
- **Confidence Scoring**: Analyzes language for certainty indicators
- **Risk Categorization**: Scores outputs from low to critical risk

### Cross-Agent Verification
- Automatic triggering for high-risk activities
- Distributed verification agent network
- Consensus-based validation
- Transparent verification processes

### Dashboard & Alerts
- Real-time web dashboard
- Activity feed with risk indicators
- Hallucination alert system
- Verification network status
- Performance metrics and trends

## Installation

1. **Install Node.js dependencies**:
   ```bash
   cd agent-monitoring
   npm install
   ```

2. **Start the monitoring system**:
   ```bash
   ./start-monitor.sh
   ```
   
   Or manually:
   ```bash
   npm start
   ```

3. **Access the dashboard**:
   Open your browser to: http://localhost:3001

## Usage

### Registering Agents
Agents can register themselves with the monitor:

```javascript
const AgentActivityMonitor = require('./agent-monitoring/agent-activity-monitor');

const monitor = new AgentActivityMonitor();
await monitor.registerAgent('my-agent-id', 'agent-type');
```

### Logging Activities
Agents should log their activities:

```javascript
await monitor.logActivity(
    'my-agent-id',
    'action_name',
    { /* input data */ },
    { /* output data */ }
);
```

The monitor will automatically perform hallucination detection and trigger verification if needed.

## Architecture

```
Agent Activity Monitor
├── Activity Logger           # Records all agent actions
├── Hallucination Detector    # Multi-layer verification system
├── Verification Network      # Cross-agent validation system
├── API Server               # REST API for dashboard communication
└── Web Dashboard            # Real-time monitoring interface
```

### Hallucination Detection Layers

1. **Consistency Check** (30% weight)
   - Detects internal contradictions
   - Identifies logical inconsistencies

2. **Factual Verification** (30% weight)
   - Validates numerical claims and statistics
   - Checks for verifiable facts

3. **Source Attribution** (20% weight)
   - Verifies proper citation and referencing
   - Checks source reliability indicators

4. **Confidence Assessment** (20% weight)
   - Analyzes linguistic certainty markers
   - Evaluates confidence vs. hesitation language

## API Endpoints

### GET `/api/monitor/status`
Returns current system status including:
- Agent counts and statuses
- Recent activities
- Verification request counts
- System health metrics

### WebSocket Events
- `initial-data`: Sent on connection with initial system state
- `system-update`: Periodic updates every 5 seconds

## Configuration

The monitor can be configured via constructor options:

```javascript
const monitor = new AgentActivityMonitor({
    logDirectory: './logs',           // Directory for activity logs
    maxLogSize: 10000,               // Maximum lines per log file
    checkInterval: 5000,             // Health check interval (ms)
    hallucinationThreshold: 0.7,     // Score above which verification triggers
    verificationRequired: true       // Enable cross-agent verification
});
```

## Data Privacy & Security

- **Input Hashing**: Sensitive input data is hashed for privacy
- **Output Truncation**: Large outputs are truncated for storage efficiency
- **Access Controls**: API access can be restricted via middleware
- **Audit Trails**: All activities are logged for compliance
- **Secure Communications**: WebSocket connections for real-time updates

## Extending the System

### Adding New Detection Methods
Modify the `HallucinationDetector` class in `agent-activity-monitor.js` to add new verification layers.

### Custom Verification Protocols
Extend the verification network logic to implement domain-specific validation rules.

### Integration with Existing Agents
Agents can integrate by:
1. Importing the monitor module
2. Registering at startup
3. Logging activities with appropriate metadata

## Development

### Running Tests
```bash
node test-monitor.js
```

### Development Server
```bash
npm run dev
```
Uses nodemon for automatic restart during development.

## Deployment

### Production Considerations
- Use process managers like PM2 for production deployment
- Configure proper logging rotation
- Set up monitoring for the monitor itself
- Consider HTTPS for dashboard access
- Implement authentication for sensitive environments

### Environment Variables
- `PORT`: Port for the HTTP server (default: 3001)
- `LOG_DIRECTORY`: Custom log storage location
- `MAX_LOG_SIZE`: Maximum log file size

## Troubleshooting

### Common Issues

1. **Dashboard not loading**
   - Ensure server is running (`npm start`)
   - Check port 3001 is accessible
   - Verify no firewall blocking access

2. **No agent data showing**
   - Confirm agents are registering with the monitor
   - Check agent activity logging
   - Verify WebSocket connections

3. **High memory usage**
   - Check log rotation settings
   - Monitor activity log sizes
   - Consider reducing maxLogSize

## License

MIT License - see LICENSE file for details.

## Part of OpenClaw Ecosystem

This monitoring system is designed to work seamlessly with the OpenClaw autonomous agent system, providing the visibility and reliability needed for production multi-agent operations.