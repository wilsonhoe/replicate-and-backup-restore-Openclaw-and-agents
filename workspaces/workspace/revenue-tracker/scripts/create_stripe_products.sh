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
