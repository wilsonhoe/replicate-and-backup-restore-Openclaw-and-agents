#!/bin/bash
# Secure Stripe Configuration Script
# YOU control your secret key - never share it

echo "🔐 Secure Stripe Configuration"
echo "==============================="
echo ""
echo "IMPORTANT: You'll enter your secret key locally - it will not be stored in scripts"
echo ""

# Prompt for secret key (hidden input)
read -s -p "Enter your Stripe SECRET key (sk_live_...): " STRIPE_SECRET_KEY
echo ""

# Validate key format
if [[ "$STRIPE_SECRET_KEY" =~ ^sk_live_[a-zA-Z0-9]+$ ]]; then
    echo "✅ Secret key format validated"
else
    echo "❌ Invalid secret key format"
    exit 1
fi

# Test the key (secure API call)
echo "Testing secret key..."
RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/account)

if echo "$RESPONSE" | grep -q "id"; then
    echo "✅ Secret key is valid and working"
    ACCOUNT_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*' | grep -o '[^"]*$' | head -1)
    echo "   Account ID: $ACCOUNT_ID"
else
    echo "❌ Secret key test failed"
    echo "   Response: $RESPONSE"
    exit 1
fi

# Create environment file (secure)
cat > ~/.stripe_env << ENV_EOF
# Stripe Environment Variables
# Generated on $(date)
export STRIPE_SECRET_KEY="$STRIPE_SECRET_KEY"
export STRIPE_ACCOUNT_ID="$ACCOUNT_ID"
ENV_EOF

echo "✅ Configuration saved to ~/.stripe_env"
echo ""
echo "To use this configuration, run:"
echo "   source ~/.stripe_env"
echo ""
echo "Your secret key is now available as: \$STRIPE_SECRET_KEY"
