#!/bin/bash
# Stripe Revenue Integration Script
# Uses publishable key for client-side operations
# You control the secret key locally

# Configuration (you set these locally)
STRIPE_PUBLISHABLE_KEY="${STRIPE_PUBLISHABLE_KEY:-pk_live_51NfNl7Iakw4Xf7FscJU0bJOTAwyTJ2gG7b2NiQzl6iT7C8qzkNRid1A96OIvqbmXuppsTqsD2FFQrlRIUidwVxJQ00i2AghF4a}"
STRIPE_SECRET_KEY="${STRIPE_SECRET_KEY:-}"  # You set this locally

# Revenue tracker integration
REVENUE_TRACKER_DIR="/home/wls/.openclaw/workspace/revenue-tracker"
REVENUE_SCRIPT="$REVENUE_TRACKER_DIR/scripts/add_revenue.sh"

# Function to check Stripe account status
check_stripe_status() {
    echo "🔍 Checking Stripe Account Status"
    echo "=================================="
    
    # Test publishable key validity (safe to check)
    if [[ -n "$STRIPE_PUBLISHABLE_KEY" ]]; then
        echo "✅ Publishable key configured"
        echo "   Key type: $(echo $STRIPE_PUBLISHABLE_KEY | cut -d'_' -f1)"
        echo "   Account: $(echo $STRIPE_PUBLISHABLE_KEY | cut -d'_' -f2)"
    else
        echo "❌ No publishable key configured"
    fi
    
    # Check if secret key is set (you do this locally)
    if [[ -n "$STRIPE_SECRET_KEY" ]]; then
        echo "✅ Secret key is configured locally"
        echo "   Key type: $(echo $STRIPE_SECRET_KEY | cut -d'_' -f1)"
    else
        echo "⚠️  Secret key not set - you'll need to configure this locally"
        echo "   Set environment variable: export STRIPE_SECRET_KEY='your_secret_key'"
    fi
    
    echo ""
}

# Function to set up secure Stripe CLI integration
setup_stripe_cli() {
    echo "🔧 Setting Up Stripe CLI Integration"
    echo "===================================="
    
    # Check if Stripe CLI is installed
    if ! command -v stripe &> /dev/null; then
        echo "Installing Stripe CLI..."
        curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
        sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" >> /etc/apt/sources.list.d/stripe.list'
        sudo apt update && sudo apt install stripe
        echo "✅ Stripe CLI installed"
    else
        echo "✅ Stripe CLI already installed"
    fi
    
    # Create secure configuration script
    cat > "$REVENUE_TRACKER_DIR/scripts/configure_stripe_secure.sh" << 'EOF'
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
EOF

    chmod +x "$REVENUE_TRACKER_DIR/scripts/configure_stripe_secure.sh"
    echo "✅ Secure configuration script created"
    echo "   Run: ./configure_stripe_secure.sh (to set up your secret key)"
    echo ""
}

# Function to create revenue import script (uses your secret key locally)
create_revenue_import_script() {
    echo "📥 Creating Revenue Import Script"
    echo "================================="
    
    cat > "$REVENUE_TRACKER_DIR/scripts/import_stripe_revenue.sh" << 'EOF'
#!/bin/bash
# Import Stripe Revenue Data
# Uses your locally configured secret key

# Load Stripe credentials
if [[ -f ~/.stripe_env ]]; then
    source ~/.stripe_env
fi

if [[ -z "$STRIPE_SECRET_KEY" ]]; then
    echo "❌ STRIPE_SECRET_KEY not set"
    echo "   Run: ./configure_stripe_secure.sh first"
    exit 1
fi

# Configuration
REVENUE_SCRIPT="/home/wls/.openclaw/workspace/revenue-tracker/scripts/add_revenue.sh"
DATE_RANGE="${1:-7}"  # Default: last 7 days

# Calculate date range
END_DATE=$(date +%Y-%m-%d)
START_DATE=$(date -d "$END_DATE - $DATE_RANGE days" +%Y-%m-%d)

echo "📊 Importing Stripe Revenue Data"
echo "================================="
echo "Period: $START_DATE to $END_DATE"
echo ""

# Fetch successful charges from Stripe
echo "Fetching transactions from Stripe..."
RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" \
  -G https://api.stripe.com/v1/charges \
  --data-urlencode "created[gte]=$(date -d "$START_DATE" +%s)" \
  --data-urlencode "created[lte]=$(date -d "$END_DATE 23:59:59" +%s)" \
  --data-urlencode "limit=100" \
  --data-urlencode "status=succeeded")

# Process transactions
TOTAL_IMPORTED=0
echo "$RESPONSE" | jq -r '.data[] | [.created, .amount, .description, .receipt_email, .id] | @csv' 2>/dev/null | while IFS=',' read -r timestamp amount description email charge_id; do
    # Clean up values
    timestamp=$(echo $timestamp | tr -d '"')
    amount=$(echo $amount | tr -d '"')
    description=$(echo $description | tr -d '"')
    email=$(echo $email | tr -d '"')
    charge_id=$(echo $charge_id | tr -d '"')
    
    # Convert Stripe amount (cents) to dollars
    DOLLARS=$(echo "scale=2; $amount / 100" | bc -l)
    
    # Convert timestamp to date
    DATE=$(date -d "@$timestamp" +%Y-%m-%d)
    
    # Add to revenue tracker
    echo "Importing: \$$DOLLARS - $description"
    $REVENUE_SCRIPT \
      --amount "$DOLLARS" \
      --source "Stripe - $description" \
      --category "digital-products" \
      --date "$DATE" \
      --notes "Customer: $email | Charge: $charge_id"
    
    TOTAL_IMPORTED=$((TOTAL_IMPORTED + 1))
done

echo ""
echo "✅ Import completed!"
echo "   Transactions imported: $TOTAL_IMPORTED"
echo ""
echo "💡 Next steps:"
echo "   View revenue: ./view_revenue.sh --period week"
echo "   Check goals: ./check_goals.sh --target 1000 --period monthly"
echo "   Run dashboard: ./monitor_dashboard.sh --detailed"
EOF

    chmod +x "$REVENUE_TRACKER_DIR/scripts/import_stripe_revenue.sh"
    echo "✅ Revenue import script created"
    echo "   Usage: ./import_stripe_revenue.sh [days_back]"
    echo "   Example: ./import_stripe_revenue.sh 30 (imports last 30 days)"
    echo ""
}

# Function to create product creation script
create_product_setup_script() {
    echo "🛍️ Creating Product Setup Script"
    echo "==============================="
    
    cat > "$REVENUE_TRACKER_DIR/scripts/create_stripe_products.sh" << 'EOF'
#!/bin/bash
# Create Stripe Products for Revenue Generation
# Uses your locally configured secret key

# Load Stripe credentials
if [[ -f ~/.stripe_env ]]; then
    source ~/.stripe_env
fi

if [[ -f ~/.openclaw/workspace/stripe_products.env ]]; then
    source ~/.openclaw/workspace/stripe_products.env
fi

if [[ -z "$STRIPE_SECRET_KEY" ]]; then
    echo "❌ STRIPE_SECRET_KEY not set"
    echo "   Run: ./configure_stripe_secure.sh first"
    exit 1
fi

echo "🛍️ Creating Revenue-Generating Products"
echo "======================================="
echo ""

# Product 1: AI Automation Course
echo "Creating AI Automation Course..."
COURSE_RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/products \
  -d name="AI Automation for Small Business" \
  -d type=good \
  -d description="Complete guide to automating business processes with AI tools" \
  -d metadata[category]="digital-products" \
  -d metadata[revenue_type]="course")

if echo "$COURSE_RESPONSE" | grep -q '"id"'; then
    COURSE_ID=$(echo "$COURSE_RESPONSE" | jq -r '.id')
    echo "✅ Course product created: $COURSE_ID"
    
    # Create price
    PRICE_RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/prices \
      -d product="$COURSE_ID" \
      -d unit_amount=9700 \
      -d currency=usd)
    
    if echo "$PRICE_RESPONSE" | grep -q '"id"'; then
        COURSE_PRICE_ID=$(echo "$PRICE_RESPONSE" | jq -r '.id')
        echo "✅ Course price set: \$97 ($COURSE_PRICE_ID)"
    fi
fi

# Product 2: Automation Templates
echo ""
echo "Creating Automation Templates..."
TEMPLATE_RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/products \
  -d name="Business Automation Template Pack" \
  -d type=good \
  -d description="Ready-to-use automation templates and scripts" \
  -d metadata[category]="digital-products" \
  -d metadata[revenue_type]="templates")

if echo "$TEMPLATE_RESPONSE" | grep -q '"id"'; then
    TEMPLATE_ID=$(echo "$TEMPLATE_RESPONSE" | jq -r '.id')
    echo "✅ Template pack created: $TEMPLATE_ID"
    
    # Create price
    PRICE_RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/prices \
      -d product="$TEMPLATE_ID" \
      -d unit_amount=4700 \
      -d currency=usd)
    
    if echo "$PRICE_RESPONSE" | grep -q '"id"'; then
        TEMPLATE_PRICE_ID=$(echo "$PRICE_RESPONSE" | jq -r '.id')
        echo "✅ Template price set: \$47 ($TEMPLATE_PRICE_ID)"
    fi
fi

# Product 3: Consulting Service
echo ""
echo "Creating Consulting Service..."
CONSULTING_RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/products \
  -d name="AI Automation Consulting" \
  -d type=service \
  -d description="1-hour consultation on AI automation implementation" \
  -d metadata[category]="services" \
  -d metadata[revenue_type]="consulting")

if echo "$CONSULTING_RESPONSE" | grep -q '"id"'; then
    CONSULTING_ID=$(echo "$CONSULTING_RESPONSE" | jq -r '.id')
    echo "✅ Consulting service created: $CONSULTING_ID"
    
    # Create price
    PRICE_RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/prices \
      -d product="$CONSULTING_ID" \
      -d unit_amount=19700 \
      -d currency=usd)
    
    if echo "$PRICE_RESPONSE" | grep -q '"id"'; then
        CONSULTING_PRICE_ID=$(echo "$PRICE_RESPONSE" | jq -r '.id')
        echo "✅ Consulting price set: \$197 ($CONSULTING_PRICE_ID)"
    fi
fi

# Save product IDs for future reference
cat > ~/.openclaw/workspace/stripe_products.env << ENV_EOF
# Stripe Product IDs
# Generated on $(date)
export STRIPE_COURSE_ID="$COURSE_ID"
export STRIPE_COURSE_PRICE_ID="$COURSE_PRICE_ID"
export STRIPE_TEMPLATE_ID="$TEMPLATE_ID"
export STRIPE_TEMPLATE_PRICE_ID="$TEMPLATE_PRICE_ID"
export STRIPE_CONSULTING_ID="$CONSULTING_ID"
export STRIPE_CONSULTING_PRICE_ID="$CONSULTING_PRICE_ID"
ENV_EOF

echo ""
echo "✅ Products created and saved to ~/.openclaw/workspace/stripe_products.env"
echo ""
echo "🎯 Revenue Targets with These Products:"
echo "   Course (\$97): 11 sales/month = \$1,067"
echo "   Templates (\$47): 22 sales/month = \$1,034"
echo "   Consulting (\$197): 6 sales/month = \$1,182"
echo ""
echo "💡 Next steps:"
echo "   1. Set up payment pages on your website"
echo "   2. Create checkout links for each product"
echo "   3. Start marketing and content creation"
echo "   4. Monitor revenue with: ./import_stripe_revenue.sh"
EOF

    chmod +x "$REVENUE_TRACKER_DIR/scripts/create_stripe_products.sh"
    echo "✅ Product creation script created"
    echo "   This creates your revenue-generating products with proper pricing"
    echo ""
}

# Main execution
echo "🔐 Secure Stripe Integration Setup"
echo "==================================="
echo ""
echo "This setup will help you integrate Stripe revenue tracking securely."
echo "You maintain complete control of your secret keys."
echo ""

# Run setup functions
check_stripe_status
setup_stripe_cli
create_revenue_import_script
create_product_setup_script

echo "🎉 Secure Stripe Integration Complete!"
echo "======================================"
echo ""
echo "Next Steps:"
echo "1. Run: ./configure_stripe_secure.sh (to set up your secret key)"
echo "2. Run: ./create_stripe_products.sh (to create revenue products)"
echo "3. Run: ./import_stripe_revenue.sh (to import existing transactions)"
echo ""
echo "Security Notes:"
echo "• Your secret key is stored locally in ~/.stripe_env"
echo "• Never share your secret key with anyone"
echo "• Import scripts only access your data when you run them"
echo "• All revenue data is tracked in your local revenue tracker"
echo ""
echo "Revenue tracking is now ready for your $1K/month goal!"