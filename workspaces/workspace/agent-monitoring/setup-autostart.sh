#!/bin/bash

# OpenClaw Monitoring System Auto-Start Script
# Systemd service configuration and management

SERVICE_NAME="openclaw-monitor"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
WORKING_DIR="/home/wls/.openclaw/workspace/agent-monitoring"
SERVER_FILE="embedded-server.js"
USER="wls"

echo "🔧 OpenClaw Monitoring System Auto-Start Configuration"
echo "======================================================"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "❌ This script must be run as root (use sudo)"
   exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if working directory exists
if [[ ! -d "$WORKING_DIR" ]]; then
    echo "❌ Working directory not found: $WORKING_DIR"
    exit 1
fi

# Check if server file exists
if [[ ! -f "$WORKING_DIR/$SERVER_FILE" ]]; then
    echo "❌ Server file not found: $WORKING_DIR/$SERVER_FILE"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create systemd service file
echo "📝 Creating systemd service file..."
cat > "$SERVICE_FILE" << EOF
[Unit]
Description=OpenClaw Agent Monitor - Real-time activity monitoring with hallucination detection
Documentation=https://github.com/openclaw/openclaw
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$WORKING_DIR
ExecStart=/usr/bin/node $SERVER_FILE
Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=3

# Environment
Environment=NODE_ENV=production
Environment=PORT=3001

# Logging
StandardOutput=append:$WORKING_DIR/systemd.log
StandardError=append:$WORKING_DIR/systemd-error.log
SyslogIdentifier=$SERVICE_NAME

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=$WORKING_DIR

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service file created: $SERVICE_FILE"

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable service to start on boot
echo "🚀 Enabling service to start on boot..."
systemctl enable "$SERVICE_NAME"

# Stop any existing server on port 3001
echo "🛑 Stopping any existing monitoring server..."
pkill -f "node.*monitor" 2>/dev/null || true
sleep 2

# Start the service
echo "▶️ Starting monitoring service..."
systemctl start "$SERVICE_NAME"

# Wait a moment and check status
sleep 3

# Check service status
echo "📊 Service Status:"
systemctl status "$SERVICE_NAME" --no-pager -l

# Test if server is responding
echo "🧪 Testing server response..."
if curl -s -f http://localhost:3001/health > /dev/null; then
    echo "✅ Server is responding at http://localhost:3001"
    echo "✅ Dashboard: http://localhost:3001"
    echo "✅ API Status: http://localhost:3001/api/monitor/status"
else
    echo "❌ Server is not responding. Check logs:"
    echo "   sudo journalctl -u $SERVICE_NAME -f"
    exit 1
fi

# Show useful commands
echo ""
echo "🎯 Useful Commands:"
echo "==================="
echo "Start service:   sudo systemctl start $SERVICE_NAME"
echo "Stop service:    sudo systemctl stop $SERVICE_NAME"
echo "Restart service: sudo systemctl restart $SERVICE_NAME"
echo "Status:          sudo systemctl status $SERVICE_NAME"
echo "Logs:            sudo journalctl -u $SERVICE_NAME -f"
echo "Disable auto-start: sudo systemctl disable $SERVICE_NAME"
echo ""
echo "✅ Auto-start configuration complete!"
echo "✅ Monitoring system will start automatically on boot"
echo "✅ Dashboard available at: http://localhost:3001"