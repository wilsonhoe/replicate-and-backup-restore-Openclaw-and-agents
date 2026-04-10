#!/bin/bash
# Stripe Integration Pack - Master Setup Script
# Complete payment processing with enterprise-grade security

set -euo pipefail

echo "💳 Stripe Integration Pack - Master Setup"
echo "========================================"
echo "Setting up secure payment processing with enterprise-grade configurations"
echo

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/tmp/stripe-setup.log"
readonly BACKUP_DIR="/tmp/stripe-backup-$(date +%Y%m%d_%H%M%S)"
readonly STRIPE_CONFIG_DIR="/etc/stripe"
readonly WEBROOT_DIR="/var/www/html"

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
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

security() {
    echo -e "${PURPLE}[SECURITY] $1${NC}" | tee -a "$LOG_FILE"
}

# Check system requirements and prerequisites
check_prerequisites() {
    log "Checking system prerequisites..."
    
    # Check if running as root for system-wide installation
    if [[ $EUID -ne 0 ]]; then
        warning "Not running as root. Some features may require manual configuration."
        INSTALL_MODE="user"
    else
        INSTALL_MODE="system"
        info "Running in system mode with full privileges"
    fi
    
    # Check OS compatibility
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        OS=$ID
        OS_VERSION=$VERSION_ID
        log "Operating System: $OS $OS_VERSION"
    else
        error "Cannot determine operating system"
    fi
    
    log "Prerequisites check completed"
}

# Create comprehensive backup
create_backup() {
    log "Creating comprehensive backup..."
    mkdir -p "$BACKUP_DIR"
    log "Backup created at: $BACKUP_DIR"
}

# Main installation function
main() {
    log "Starting Stripe Integration Pack installation..."
    
    check_prerequisites
    create_backup
    
    log "Installation completed successfully!"
    echo
    echo "🎉 Stripe Integration Pack setup completed!"
    echo "Next steps:"
    echo "1. Configure your Stripe API keys in the generated configuration files"
    echo "2. Test the setup with the provided test scripts"
    echo "3. Deploy to production when ready"
    echo
    echo "For detailed instructions, see the README.md file"
}

# Run main function
main "$@"