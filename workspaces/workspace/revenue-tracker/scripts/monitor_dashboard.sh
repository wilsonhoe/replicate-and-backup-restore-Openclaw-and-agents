#!/bin/bash
# Revenue Monitoring Dashboard
# Usage: ./monitor_dashboard.sh [--detailed] [--alert]

# Parse arguments
DETAILED=false
ALERT=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --detailed)
            DETAILED=true
            shift
            ;;
        --alert)
            ALERT=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--detailed] [--alert]"
            exit 1
            ;;
    esac
done

# Data directory
DATA_DIR="$(dirname "$0")/../data"
REVENUE_FILE="$DATA_DIR/revenue.csv"
CONFIG_FILE="$(dirname "$0")/../config/revenue-tracker.json"

# Load configuration if exists
if [[ -f "$CONFIG_FILE" ]]; then
    MONTHLY_GOAL=$(grep -o '"monthly_target": [0-9]*' "$CONFIG_FILE" | grep -o '[0-9]*')
    MONTHLY_GOAL=${MONTHLY_GOAL:-1000}
else
    MONTHLY_GOAL=1000
fi

# Check if revenue file exists
if [[ ! -f "$REVENUE_FILE" ]]; then
    echo "🎯 Revenue Dashboard - $(date)"
    echo "================================"
    echo "⚠️  No revenue data found. Start tracking with add_revenue.sh"
    echo "💡 Example: ./add_revenue.sh --amount 100 --source \"Initial Test\" --category \"other\""
    exit 0
fi

echo "🎯 Revenue Dashboard - $(date)"
echo "================================"

# Today's revenue
TODAY=$(date +%Y-%m-%d)
TODAY_REVENUE=$(grep "^$TODAY" "$REVENUE_FILE" 2>/dev/null | awk -F',' '{sum += $2} END {print sum}')
TODAY_REVENUE=${TODAY_REVENUE:-0}

# This month's progress
CURRENT_MONTH=$(date +%Y-%m)
MONTHLY_REVENUE=$(grep "^$CURRENT_MONTH" "$REVENUE_FILE" 2>/dev/null | awk -F',' '{sum += $2} END {print sum}')
MONTHLY_REVENUE=${MONTHLY_REVENUE:-0}

# Yesterday's revenue for comparison
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
YESTERDAY_REVENUE=$(grep "^$YESTERDAY" "$REVENUE_FILE" 2>/dev/null | awk -F',' '{sum += $2} END {print sum}')
YESTERDAY_REVENUE=${YESTERDAY_REVENUE:-0}

# Calculate goal progress
PROGRESS=$(echo "scale=1; ($MONTHLY_REVENUE / $MONTHLY_GOAL) * 100" | bc -l 2>/dev/null || echo "0")

# Daily comparison
if (( $(echo "$TODAY_REVENUE > $YESTERDAY_REVENUE" | bc -l 2>/dev/null || echo "0") )); then
    DAILY_TREND="📈"
    DAILY_DIFF=$(echo "$TODAY_REVENUE - $YESTERDAY_REVENUE" | bc -l 2>/dev/null || echo "0")
elif (( $(echo "$TODAY_REVENUE < $YESTERDAY_REVENUE" | bc -l 2>/dev/null || echo "0") )); then
    DAILY_TREND="📉"
    DAILY_DIFF=$(echo "$YESTERDAY_REVENUE - $TODAY_REVENUE" | bc -l 2>/dev/null || echo "0")
else
    DAILY_TREND="➡️"
    DAILY_DIFF=0
fi

echo "💰 Today's Revenue: \$$TODAY_REVENUE $DAILY_TREND"
if [[ "$DAILY_DIFF" != "0" ]]; then
    echo "   vs Yesterday: \$$DAILY_DIFF difference"
fi
echo "📈 Monthly Revenue: \$$MONTHLY_REVENUE"
echo "🎯 Goal Progress: $PROGRESS% (Target: \$$MONTHLY_GOAL)"

# Status indicator with color coding
if (( $(echo "$PROGRESS >= 100" | bc -l 2>/dev/null || echo "0") )); then
    STATUS="✅ GOAL ACHIEVED! 🎉"
    COLOR="32" # Green
elif (( $(echo "$PROGRESS >= 75" | bc -l 2>/dev/null || echo "0") )); then
    STATUS="🟡 Close to target - Final push needed!"
    COLOR="33" # Yellow
elif (( $(echo "$PROGRESS >= 50" | bc -l 2>/dev/null || echo "0") )); then
    STATUS="🟡 Halfway there - Good momentum!"
    COLOR="33" # Yellow
elif (( $(echo "$PROGRESS >= 25" | bc -l 2>/dev/null || echo "0") )); then
    STATUS="🟠 Building momentum - Stay consistent!"
    COLOR="33" # Yellow
else
    STATUS="🔴 Needs attention - Increase efforts!"
    COLOR="31" # Red
fi

echo -e "\033[${COLOR}m$STATUS\033[0m"

# Days remaining in month
CURRENT_DAY=$(date +%d)
DAYS_IN_MONTH=$(date -d "$(date +%Y-%m-01) +1 month -1 day" +%d)
DAYS_REMAINING=$((DAYS_IN_MONTH - CURRENT_DAY + 1))

# Daily target needed
REMAINING=$(echo "$MONTHLY_GOAL - $MONTHLY_REVENUE" | bc -l 2>/dev/null || echo "$MONTHLY_GOAL")
if (( $(echo "$REMAINING > 0" | bc -l 2>/dev/null || echo "1") )); then
    DAILY_TARGET=$(echo "scale=2; $REMAINING / $DAYS_REMAINING" | bc -l 2>/dev/null || echo "0")
    echo "📅 Days remaining: $DAYS_REMAINING"
    echo "💡 Daily target needed: \$$DAILY_TARGET"
fi

if [[ "$DETAILED" == true ]]; then
    echo ""
    echo "📊 Detailed Analysis"
    echo "==================="
    
    # Top sources this month
    echo "🏆 Top Revenue Sources (This Month):"
    grep "^$CURRENT_MONTH" "$REVENUE_FILE" 2>/dev/null | awk -F',' '{sources[$3] += $2} END {for (src in sources) print "  " src ": $" sources[src]}' | sort -k3 -nr | head -5
    
    # Top categories this month
    echo ""
    echo "🏷️ Top Categories (This Month):"
    grep "^$CURRENT_MONTH" "$REVENUE_FILE" 2>/dev/null | awk -F',' '{categories[$4] += $2} END {for (cat in categories) print "  " cat ": $" categories[cat]}' | sort -k3 -nr | head -5
    
    # Recent entries
    echo ""
    echo "📋 Recent Entries:"
    tail -n 5 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
        if [[ "$date" != "date" ]]; then
            echo "  $date: \$$amount from $source ($category)"
        fi
    done
fi

# Generate alerts if requested
if [[ "$ALERT" == true ]]; then
    echo ""
    echo "🚨 Alert Analysis"
    echo "================="
    
    # Check if significantly behind target
    EXPECTED_PROGRESS=$(echo "scale=1; ($CURRENT_DAY / $DAYS_IN_MONTH) * 100" | bc -l 2>/dev/null || echo "0")
    if (( $(echo "$PROGRESS < ($EXPECTED_PROGRESS * 0.7)" | bc -l 2>/dev/null || echo "0") )); then
        echo "⚠️  You're significantly behind schedule!"
        echo "   Expected progress: $EXPECTED_PROGRESS%"
        echo "   Actual progress: $PROGRESS%"
        echo "   Action needed: Increase revenue-generating activities"
    fi
    
    # Check for unusual patterns (no revenue for 3+ days)
    LAST_REVENUE_DATE=$(tail -n 1 "$REVENUE_FILE" | cut -d',' -f1)
    if [[ "$LAST_REVENUE_DATE" != "$TODAY" ]]; then
        DAYS_SINCE=$(echo "$(date -d "$TODAY" +%s) - $(date -d "$LAST_REVENUE_DATE" +%s)" | bc -l | xargs -I {} echo "scale=0; {}/86400" | bc -l)
        if [[ $DAYS_SINCE -gt 3 ]]; then
            echo "⚠️  No revenue recorded for $DAYS_SINCE days!"
            echo "   Action needed: Review and restart revenue activities"
        fi
    fi
fi

echo ""
echo "💡 Next Steps:"
if (( $(echo "$PROGRESS < 100" | bc -l 2>/dev/null || echo "1") )); then
    echo "• Focus on high-converting revenue activities"
    echo "• Review top-performing sources and scale them"
    echo "• Consider promotional campaigns or special offers"
    echo "• Set daily target of \$$DAILY_TARGET to stay on track"
else
    echo "• Congratulations! Consider setting higher goals"
    echo "• Analyze what's working and replicate success"
    echo "• Explore new revenue streams for diversification"
fi

echo ""
echo "📅 Next check recommended: $(date -d '+1 day' +%Y-%m-%d)"
echo "💪 Every dollar counts toward your goals!"