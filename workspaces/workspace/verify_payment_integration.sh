#!/bin/bash
# Payment Integration Verification Script

echo "🔍 PAYMENT INTEGRATION VERIFICATION"
echo "===================================="
echo ""

# Check if Stripe environment is configured
if [[ -f ~/.stripe_env ]]; then
    echo "✅ Stripe environment file found: ~/.stripe_env"
    source ~/.stripe_env
    
    if [[ -n "$STRIPE_SECRET_KEY" ]]; then
        echo "✅ Stripe secret key configured"
        echo "🔑 Key type: $(echo $STRIPE_SECRET_KEY | cut -d'_' -f1)"
        
        # Test API connection
        echo "🧪 Testing API connection..."
        RESPONSE=$(curl -s -u "$STRIPE_SECRET_KEY:" https://api.stripe.com/v1/account 2>/dev/null || echo "CONNECTION_FAILED")
        
        if [[ "$RESPONSE" != "CONNECTION_FAILED" && "$RESPONSE" != "" ]]; then
            if echo "$RESPONSE" | grep -q '"id"'; then
                ACCOUNT_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*' | grep -o '[^"]*$' | head -1)
                echo "✅ API connection successful"
                echo "   Account ID: $ACCOUNT_ID"
                echo "   Account status: Verified and ready"
            else
                echo "⚠️  API responded but unexpected format"
            fi
        else
            echo "❌ API connection failed"
            echo "   Please check your secret key and internet connection"
        fi
    else
        echo "❝ Stripe secret key not set in environment"
    fi
else
    echo "❌ Stripe environment file not found"
    echo "   Run: ./revenue-tracker/scripts/configure_stripe_secure.sh"
fi

echo ""
echo "📦 PRODUCT VERIFICATION"
echo "======================"

if [[ -f ~/.openclaw/workspace/stripe_products.env ]]; then
    echo "✅ Stripe products file found"
    source ~/.openclaw/workspace/stripe_products.env
    
    PRODUCTS=0
    if [[ -n "$STRIPE_COURSE_ID" ]]; then
        echo "✅ AI Automation Course: $STRIPE_COURSE_ID"
        ((PRODUCTS++))
    fi
    if [[ -n "$STRIPE_TEMPLATE_ID" ]]; then
        echo "✅ Template Pack: $STRIPE_TEMPLATE_ID"  
        ((PRODUCTS++))
    fi
    if [[ -n "$STRIPE_CONSULTING_ID" ]]; then
        echo "✅ Consulting Service: $STRIPE_CONSULTING_ID"
        ((PRODUCTS++))
    fi
    
    echo ""
    echo "📊 Products created: $PRODUCTS/3"
else
    echo "❌ Stripe products not yet created"
    echo "   Run: ./revenue-tracker/scripts/create_stripe_products.sh"
fi

echo ""
echo "💰 REVENUE TRACKER STATUS"
echo "========================"

if [[ -d /home/wls/.openclaw/workspace/revenue-tracker/data ]]; then
    echo "✅ Revenue data directory exists"
    
    if [[ -f /home/wls/.openclaw/workspace/revenue-tracker/data/revenue.csv ]]; then
        LINE_COUNT=$(wc -l < /home/wls/.openclaw/workspace/revenue-tracker/data/revenue.csv)
        echo "✅ Revenue CSV found with $((LINE_COUNT-1)) entries"
        
        if [[ $LINE_COUNT -gt 1 ]]; then
            LATEST=$(tail -2 /home/wls/.openclaw/workspace/revenue-tracker/data/revenue.csv | head -1)
            echo "   Latest entry: $LATEST"
        fi
    else
        echo "⚠️  Revenue CSV not yet created (will be created on first entry)"
    fi
else
    echo "❌ Revenue data directory not found"
fi

echo ""
echo "📋 NEXT STEPS RECOMMENDATION"
echo "==========================="

if [[ ! -f ~/.stripe_env ]] || [[ -z "$STRIPE_SECRET_KEY" ]]; then
    echo "🔑 PRIMARY: Configure Stripe account"
    echo "   1. Create/login to Stripe account"
    echo "   2. Get secret key from Dashboard → Developers → API Keys"
    echo "   3. Run: ./revenue-tracker/scripts/configure_stripe_secure.sh"
elif [[ ! -f ~/.openclaw/workspace/stripe_products.env ]]; then
    echo "🛍️  SECONDARY: Create monetization products"
    echo "   Run: ./revenue-tracker/scripts/create_stripe_products.sh"
else
    echo "🚀 SYSTEM READY: Test revenue import"
    echo "   Run: source ~/.stripe_env && ./revenue-tracker/scripts/import_stripe_revenue.sh 7"
fi

echo ""
echo "🎯 INTEGRATION STATUS:"
if [[ -f ~/.stripe_env && -n "$STRIPE_SECRET_KEY" ]]; then
    if [[ -f ~/.openclaw/workspace/stripe_products.env ]]; then
        echo "   🟢 FULLY ACTIVE - Revenue tracking operational"
    else
        echo "   🟡 PARTIAL - API configured, products needed"
    fi
else
    echo "   🔴 INACTIVE - Awaiting Stripe configuration"
fi