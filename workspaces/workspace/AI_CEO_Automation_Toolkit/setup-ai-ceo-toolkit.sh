#!/bin/bash
# AI CEO Automation Toolkit - Master Setup Script
# Complete OpenClaw Setup with Security Hardening

set -euo pipefail

echo "🚀 AI CEO Automation Toolkit - Master Setup"
echo "=========================================="

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/tmp/ai-ceo-setup.log"
readonly BACKUP_DIR="/tmp/ai-ceo-backup-$(date +%Y%m%d_%H%M%S)"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}" | tee -a "$LOG_FILE"
}

# Check system requirements
check_requirements() {
    log "Checking system requirements..."
    
    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        error "Unsupported operating system: $OSTYPE"
    fi
    
    # Check if running as root (not recommended)
    if [[ $EUID -eq 0 ]]; then
        warning "Running as root is not recommended for security reasons"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Check available disk space (minimum 2GB)
    AVAILABLE_SPACE=$(df / | tail -1 | awk '{print $4}')
    if [[ $AVAILABLE_SPACE -lt 2097152 ]]; then
        error "Insufficient disk space. At least 2GB required."
    fi
    
    # Check internet connectivity
    if ! ping -c 1 google.com &> /dev/null; then
        error "Internet connection required for setup"
    fi
    
    log "System requirements check passed"
}

# Create backup
create_backup() {
    log "Creating backup of existing configuration..."
    mkdir -p "$BACKUP_DIR"
    
    # Backup existing OpenClaw config if it exists
    if [[ -d "$HOME/.openclaw" ]]; then
        cp -r "$HOME/.openclaw" "$BACKUP_DIR/" || warning "Failed to backup OpenClaw config"
    fi
    
    # Backup existing scripts
    if [[ -d "$HOME/scripts" ]]; then
        cp -r "$HOME/scripts" "$BACKUP_DIR/" || warning "Failed to backup scripts"
    fi
    
    log "Backup created at: $BACKUP_DIR"
}

# Install dependencies
install_dependencies() {
    log "Installing dependencies..."
    
    case $OS in
        linux)
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y curl wget git nodejs npm python3 python3-pip docker.io
            elif command -v yum &> /dev/null; then
                sudo yum update -y
                sudo yum install -y curl wget git nodejs npm python3 python3-pip docker
            else
                error "Unsupported package manager"
            fi
            ;;
        macos)
            if ! command -v brew &> /dev/null; then
                log "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install curl wget git node python3 docker
            ;;
    esac
    
    # Install Node.js global packages
    npm install -g pm2 forever nodemon
    
    # Install Python packages
    pip3 install requests beautifulsoup4 selenium pandas numpy
    
    log "Dependencies installed successfully"
}

# Setup OpenClaw
setup_openclaw() {
    log "Setting up OpenClaw..."
    
    # Create OpenClaw directory structure
    mkdir -p "$HOME/.openclaw/workspace"
    mkdir -p "$HOME/.openclaw/skills"
    mkdir -p "$HOME/.openclaw/logs"
    mkdir -p "$HOME/.openclaw/config"
    
    # Download and install OpenClaw
    if [[ ! -d "$HOME/.openclaw/bin" ]]; then
        log "Downloading OpenClaw..."
        curl -fsSL https://get.openclaw.com/install.sh | bash
    fi
    
    # Add to PATH
    if ! grep -q "$HOME/.openclaw/bin" "$HOME/.bashrc"; then
        echo 'export PATH="$HOME/.openclaw/bin:$PATH"' >> "$HOME/.bashrc"
    fi
    
    # Create main configuration
    cat > "$HOME/.openclaw/config/main.json" << EOF
{
    "version": "1.0.0",
    "environment": "production",
    "auto_update": true,
    "security": {
        "enable_encryption": true,
        "require_authentication": true,
        "log_level": "info"
    },
    "agents": {
        "max_concurrent": 10,
        "heartbeat_interval": 60,
        "auto_restart": true
    },
    "monitoring": {
        "enable_health_checks": true,
        "alert_threshold": 5,
        "log_retention_days": 30
    }
}
EOF
    
    log "OpenClaw setup completed"
}

# Configure security
configure_security() {
    log "Configuring security settings..."
    
    # Create security configuration
    cat > "$HOME/.openclaw/config/security.json" << EOF
{
    "firewall": {
        "enable": true,
        "allowed_ports": [22, 80, 443],
        "rate_limiting": true,
        "max_requests_per_minute": 60
    },
    "authentication": {
        "method": "jwt",
        "token_expiry": 3600,
        "refresh_token_expiry": 86400,
        "require_2fa": true
    },
    "encryption": {
        "algorithm": "AES-256-GCM",
        "key_rotation_interval": 86400,
        "secure_storage": true
    },
    "logging": {
        "level": "info",
        "retention_days": 90,
        "secure_transport": true
    }
}
EOF
    
    # Set proper file permissions
    chmod 700 "$HOME/.openclaw/config"
    chmod 600 "$HOME/.openclaw/config"/*.json
    
    # Create SSH key if it doesn't exist
    if [[ ! -f "$HOME/.ssh/id_rsa" ]]; then
        ssh-keygen -t rsa -b 4096 -f "$HOME/.ssh/id_rsa" -N ""
    fi
    
    log "Security configuration completed"
}

# Deploy AI agents
deploy_agents() {
    log "Deploying AI agents..."
    
    # Create agent directory structure
    mkdir -p "$HOME/.openclaw/agents/revenue-tracker"
    mkdir -p "$HOME/.openclaw/agents/content-marketing"
    mkdir -p "$HOME/.openclaw/agents/customer-service"
    mkdir -p "$HOME/.openclaw/agents/financial-analysis"
    
    # Copy agent scripts
    cp "$SCRIPT_DIR"/*.sh "$HOME/.openclaw/agents/" 2>/dev/null || warning "No agent scripts found to copy"
    
    # Create agent configuration files
    for agent in revenue-tracker content-marketing customer-service financial-analysis; do
        cat > "$HOME/.openclaw/agents/$agent/config.json" << EOF
{
    "name": "$agent",
    "enabled": true,
    "schedule": "*/30 * * * *",
    "max_execution_time": 300,
    "retry_attempts": 3,
    "notification_enabled": true
}
EOF
    done
    
    # Start agents using PM2
    if command -v pm2 &> /dev/null; then
        cd "$HOME/.openclaw/agents"
        for script in *.sh; do
            if [[ -f "$script" ]]; then
                chmod +x "$script"
                pm2 start "$script" --name "ai-ceo-$script" || warning "Failed to start $script"
            fi
        done
        pm2 save
    fi
    
    log "AI agents deployed successfully"
}

# Setup monitoring
setup_monitoring() {
    log "Setting up monitoring and alerting..."
    
    # Create monitoring script
    cat > "$HOME/.openclaw/monitor.sh" << 'EOF'
#!/bin/bash
# System monitoring script

HEALTH_CHECK_URL="https://api.openclaw.com/health"
ALERT_EMAIL="admin@yourdomain.com"
LOG_FILE="/tmp/openclaw-monitor.log"

while true; do
    # Check system health
    if ! curl -f "$HEALTH_CHECK_URL" > /dev/null 2>&1; then
        echo "$(date): Health check failed" >> "$LOG_FILE"
        # Send alert (configure your alerting method)
    fi
    
    # Check disk space
    DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ $DISK_USAGE -gt 80 ]]; then
        echo "$(date): High disk usage: ${DISK_USAGE}%" >> "$LOG_FILE"
    fi
    
    # Check memory usage
    MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    if [[ $MEMORY_USAGE -gt 85 ]]; then
        echo "$(date): High memory usage: ${MEMORY_USAGE}%" >> "$LOG_FILE"
    fi
    
    sleep 300  # Check every 5 minutes
done
EOF
    
    chmod +x "$HOME/.openclaw/monitor.sh"
    
    # Add monitoring to crontab
    if ! crontab -l | grep -q "openclaw-monitor"; then
        (crontab -l 2>/dev/null; echo "*/5 * * * * $HOME/.openclaw/monitor.sh") | crontab -
    fi
    
    log "Monitoring system configured"
}

# Create startup script
create_startup_script() {
    log "Creating startup script..."
    
    cat > "$HOME/.openclaw/start-ai-ceo.sh" << 'EOF'
#!/bin/bash
# AI CEO Automation Toolkit - Startup Script

echo "🚀 Starting AI CEO Automation Toolkit..."

# Start OpenClaw
openclaw gateway start

# Start monitoring
nohup "$HOME/.openclaw/monitor.sh" > /tmp/openclaw-monitor.log 2>&1 &

# Start all agents
if command -v pm2 &> /dev/null; then
    pm2 resurrect || pm2 start all
fi

echo "✅ AI CEO Automation Toolkit started successfully!"
echo "📊 Monitor dashboard: http://localhost:3000"
echo "📧 Check logs: tail -f /tmp/openclaw-monitor.log"
EOF
    
    chmod +x "$HOME/.openclaw/start-ai-ceo.sh"
    
    # Create systemd service (Linux only)
    if [[ "$OS" == "linux" ]] && command -v systemctl &> /dev/null; then
        sudo tee /etc/systemd/system/ai-ceo.service > /dev/null << EOF
[Unit]
Description=AI CEO Automation Toolkit
After=network.target

[Service]
Type=forking
User=$USER
ExecStart=$HOME/.openclaw/start-ai-ceo.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        sudo systemctl daemon-reload
        sudo systemctl enable ai-ceo.service
    fi
    
    log "Startup script created"
}

# Main installation function
main() {
    log "Starting AI CEO Automation Toolkit installation..."
    
    check_requirements
    create_backup
    install_dependencies
    setup_openclaw
    configure_security
    deploy_agents
    setup_monitoring
    create_startup_script
    
    log "Installation completed successfully!"
    echo
    echo "🎉 AI CEO Automation Toolkit is ready to use!"
    echo
    echo "Next steps:"
    echo "1. Run: source ~/.bashrc"
    echo "2. Start the system: ~/.openclaw/start-ai-ceo.sh"
    echo "3. Monitor logs: tail -f /tmp/openclaw-monitor.log"
    echo "4. Configure your specific business settings in ~/.openclaw/config/"
    echo
    echo "For support, visit: https://github.com/ai-ceo/toolkit"
    echo
    echo "Backup created at: $BACKUP_DIR"
}

# Run main function
main "$@"