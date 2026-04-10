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
