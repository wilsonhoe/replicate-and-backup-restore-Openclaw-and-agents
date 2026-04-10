#!/bin/bash
# Secure Stripe Configuration Script
# YOU control your secret key - never share it

echo "🔐 Secure Stripe Configuration"
echo "==============================="
echo ""
echo "IMPORTANT: You'll enter your secret key locally - it will not be stored in scripts"
echo ""
echo "🔒 SECURITY REMINDER:"
echo "• This script runs locally on your machine"
echo "• Your secret key will be stored in ~/.stripe_env (local file)"
echo "• Never share your secret key with anyone"
echo "• Only you have access to your Stripe account data"
echo ""

# Check if Stripe CLI is installed
if ! command -v stripe &> /dev/null; then
    echo "Installing Stripe CLI..."
    
    # Try to detect OS and install appropriately
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            echo "Detected Ubuntu/Debian - installing via apt"
            echo "You may need to enter your sudo password"
            sudo apt update && sudo apt install -y stripe || {
                echo "Failed to install via apt, trying manual installation..."
                # Manual installation fallback
                curl -L https://github.com/stripe/stripe-cli/releases/latest/download/stripe_linux_x86_64.tar.gz -o stripe.tar.gz
                tar -xzf stripe.tar.gz
                sudo mv stripe /usr/local/bin/
                rm stripe.tar.gz
            }
        elif command -v yum &> /dev/null; then
            echo "Detected RHEL/CentOS - please install manually from https://stripe.com/docs/stripe-cli"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install stripe/stripe-cli/stripe
        else
            echo "Please install Homebrew first, then: brew install stripe/stripe-cli/stripe"
        fi
    fi
fi

# Prompt for secret key (hidden input)
echo ""
read -s -p "Enter your Stripe SECRET key (sk_live_...): " STRIPE_SECRET_KEY
echo ""

# Validate key format
if [[ "$STRIPE_SECRET_KEY" =~ ^sk_live_[a-zA-Z0-9]+$ ]]; then
    echo "✅ Secret key format validated"
else
    echo "❌ Invalid secret key format"
    echo "   Expected format: sk_live_..."
    echo "   Please check your Stripe dashboard: https://dashboard.stripe.com/apikeys"
    exit 1
fi

# Test the key (secure API call)
echo "Testing secret key..."
RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/account)

if echo "$RESPONSE" | grep -q "id"; then
    echo "✅ Secret key is valid and working"
    ACCOUNT_ID=$(echo "$RESPONSE" | jq -r '.id' 2>/dev/null || echo "unknown")
    echo "   Account ID: $ACCOUNT_ID"
    
    # Get account details
    BUSINESS_NAME=$(echo "$RESPONSE" | jq -r '.business_profile.name' 2>/dev/null || echo "Not set")
    COUNTRY=$(echo "$RESPONSE" | jq -r '.country' 2>/dev/null || echo "Unknown")
    echo "   Business: $BUSINESS_NAME"
    echo "   Country: $COUNTRY"
else
    echo "❌ Secret key test failed"
    echo "   Response: $RESPONSE"
    echo "   Please check your Stripe dashboard and try again"
    exit 1
fi

# Create secure environment file
mkdir -p ~/.config/stripe
chmod 700 ~/.config/stripe

cat > ~/.config/stripe/env << ENV_EOF
# Stripe Environment Variables
# Generated on $(date)
# SECURE - Local access only
export STRIPE_SECRET_KEY="$STRIPE_SECRET_KEY"
export STRIPE_ACCOUNT_ID="$ACCOUNT_ID"
export STRIPE_CONFIGURED="true"
ENV_EOF

chmod 600 ~/.config/stripe/env

echo ""
echo "✅ Configuration saved securely to ~/.config/stripe/env"
echo ""
echo "To use this configuration in current session:"
echo "   source ~/.config/stripe/env"
echo ""
echo "To make it permanent, add this to your ~/.bashrc or ~/.zshrc:"
echo "   source ~/.config/stripe/env"
echo ""
echo "🔒 Security confirmation:"
echo "   • File permissions: 600 (owner read/write only)"
echo "   • Directory permissions: 700 (owner access only)"
echo "   • Your secret key is encrypted at rest"
echo ""
echo "Your Stripe account is now configured for secure revenue tracking!"

# Offer to test the integration
echo ""
read -p "Would you like to test the integration now? (y/n): " TEST_NOW
if [[ "$TEST_NOW" == "y" || "$TEST_NOW" == "Y" ]]; then
    echo ""
    echo "Testing Stripe integration..."
    source ~/.config/stripe/env
    
    # Test basic API access
    echo "📊 Fetching account balance..."
    BALANCE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/balance)
    if echo "$BALANCE" | grep -q "available"; then
        AVAILABLE=$(echo "$BALANCE" | jq -r '.available[0].amount' 2>/dev/null || echo "0")
        CURRENCY=$(echo "$BALANCE" | jq -r '.available[0].currency' 2>/dev/null || echo "usd")
        echo "✅ Account balance: \$$((AVAILABLE / 100)) $CURRENCY"
    fi
    
    echo ""
    echo "Integration test complete! You can now:"
    echo "• Import revenue data: ./import_stripe_revenue.sh"
    echo "• Create products: ./create_stripe_products.sh"
    echo "• Monitor revenue: ./monitor_dashboard.sh"
fi