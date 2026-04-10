#!/bin/bash
# Revenue Tracker - Check Goal Progress
# Usage: ./check_goals.sh --target <amount> --period <period>

# Default values
TARGET="1000"
PERIOD="monthly"
TYPE="revenue"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET="$2"
            shift 2
            ;;
        --period)
            PERIOD="$2"
            shift 2
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--target <amount>] [--period <monthly|quarterly|yearly>] [--type <revenue|profit>"
            exit 1
            ;;
    esac
done

# Validate period
if [[ "$PERIOD" != "monthly" && "$PERIOD" != "quarterly" && "$PERIOD" != "yearly" ]]; then
    echo "❌ Error: Period must be monthly, quarterly, or yearly"
    exit 1
fi

# Data directory
DATA_DIR="$(dirname "$0")/../data"
REVENUE_FILE="$DATA_DIR/revenue.csv"

# Check if revenue file exists
if [[ ! -f "$REVENUE_FILE" ]]; then
    echo "❌ No revenue data found. Use add_revenue.sh to add entries."
    exit 1
fi

echo "🎯 Revenue Goal Progress Check"
echo "==============================="
echo "Target: \$$TARGET ($PERIOD)"
echo "Type: $TYPE"
echo ""

# Calculate date range based on period
case $PERIOD in
    monthly)
        # Current month
        CURRENT_MONTH=$(date +%Y-%m)
        START_DATE="${CURRENT_MONTH}-01"
        END_DATE=$(date -d "$(date +%Y-%m-01) +1 month -1 day" +%Y-%m-%d)
        PERIOD_NAME="This Month"
        ;;
    quarterly)
        # Current quarter
        CURRENT_MONTH=$(date +%m)
        CURRENT_YEAR=$(date +%Y)
        
        if [[ $CURRENT_MONTH -ge 1 && $CURRENT_MONTH -le 3 ]]; then
            QUARTER=1
            START_DATE="${CURRENT_YEAR}-01-01"
            END_DATE="${CURRENT_YEAR}-03-31"
        elif [[ $CURRENT_MONTH -ge 4 && $CURRENT_MONTH -le 6 ]]; then
            QUARTER=2
            START_DATE="${CURRENT_YEAR}-04-01"
            END_DATE="${CURRENT_YEAR}-06-30"
        elif [[ $CURRENT_MONTH -ge 7 && $CURRENT_MONTH -le 9 ]]; then
            QUARTER=3
            START_DATE="${CURRENT_YEAR}-07-01"
            END_DATE="${CURRENT_YEAR}-09-30"
        else
            QUARTER=4
            START_DATE="${CURRENT_YEAR}-10-01"
            END_DATE="${CURRENT_YEAR}-12-31"
        fi
        PERIOD_NAME="Q${QUARTER} $(date +%Y)"
        ;;
    yearly)
        # Current year
        CURRENT_YEAR=$(date +%Y)
        START_DATE="${CURRENT_YEAR}-01-01"
        END_DATE="${CURRENT_YEAR}-12-31"
        PERIOD_NAME="$(date +%Y)"
        ;;
esac

echo "Period: $PERIOD_NAME ($START_DATE to $END_DATE)"
echo ""

# Calculate current period revenue
CURRENT_REVENUE=$(tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
    if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]] && [[ "$date" < "$END_DATE" || "$date" == "$END_DATE" ]]; then
        echo "$amount"
    fi
done | awk '{sum += $1} END {print sum}')

# Handle case where no revenue found
if [[ -z "$CURRENT_REVENUE" ]]; then
    CURRENT_REVENUE=0
fi

echo "📊 Current Performance"
echo "====================="
echo "Current Revenue: \$$CURRENT_REVENUE"
echo "Target: \$$TARGET"

# Calculate progress percentage
PROGRESS=$(echo "scale=1; ($CURRENT_REVENUE / $TARGET) * 100" | bc -l)
echo "Progress: $PROGRESS%"

# Determine status and recommendations
echo ""
echo "🎯 Goal Assessment"
echo "=================="

if (( $(echo "$PROGRESS >= 100" | bc -l) )); then
    echo "✅ GOAL ACHIEVED!"
    echo "   You've exceeded your \$$TARGET target!"
    EXCESS=$(echo "$CURRENT_REVENUE - $TARGET" | bc -l)
    echo "   Excess: \$$EXCESS"
    
    # Calculate how much ahead you are
    if (( $(echo "$PROGRESS > 100" | bc -l) )); then
        PERCENTAGE_AHEAD=$(echo "scale=1; $PROGRESS - 100" | bc -l)
        echo "   You're $PERCENTAGE_AHEAD% ahead of target!"
    fi
    
elif (( $(echo "$PROGRESS >= 75" | bc -l) )); then
    echo "🟡 CLOSE TO TARGET"
    REMAINING=$(echo "$TARGET - $CURRENT_REVENUE" | bc -l)
    echo "   Remaining to reach goal: \$$REMAINING"
    echo "   You're in the final stretch!"
    
elif (( $(echo "$PROGRESS >= 50" | bc -l) )); then
    echo "🟡 HALFWAY THERE"
    REMAINING=$(echo "$TARGET - $CURRENT_REVENUE" | bc -l)
    echo "   Remaining to reach goal: \$$REMAINING"
    echo "   Good progress - keep pushing forward!"
    
elif (( $(echo "$PROGRESS >= 25" | bc -l) )); then
    echo "🟠 MAKING PROGRESS"
    REMAINING=$(echo "$TARGET - $CURRENT_REVENUE" | bc -l)
    echo "   Remaining to reach goal: \$$REMAINING"
    echo "   You're building momentum!"
    
else
    echo "🔴 NEEDS ATTENTION"
    REMAINING=$(echo "$TARGET - $CURRENT_REVENUE" | bc -l)
    echo "   Remaining to reach goal: \$$REMAINING"
    echo "   Consider reviewing your strategy and increasing efforts"
fi

# Calculate daily/weekly targets needed to reach goal
echo ""
echo "📈 Trajectory Analysis"
echo "====================="

# Calculate days remaining in period
case $PERIOD in
    monthly)
        DAYS_REMAINING=$(echo "$(date -d "$(date +%Y-%m-01) +1 month -1 day" +%d) - $(date +%d)" | bc -l)
        ;;
    quarterly)
        # Simplified calculation
        DAYS_REMAINING=90
        ;;
    yearly)
        DAYS_REMAINING=$(echo "365 - $(date +%j)" | bc -l)
        ;;
esac

if [[ $DAYS_REMAINING -gt 0 ]]; then
    DAILY_TARGET=$(echo "scale=2; $REMAINING / $DAYS_REMAINING" | bc -l)
    echo "Days remaining in period: $DAYS_REMAINING"
    echo "Daily target needed: \$$DAILY_TARGET"
fi

# Show top performing sources for the current period
echo ""
echo "🏆 Top Revenue Sources ($PERIOD_NAME)"
echo "====================================="
tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
    if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]] && [[ "$date" < "$END_DATE" || "$date" == "$END_DATE" ]]; then
        echo "$source $amount"
    fi
done | awk '{sources[$1] += $2} END {for (src in sources) print src ": $" sources[src]}' | sort -k2 -nr | head -5

# Recommendations based on performance
echo ""
echo "💡 Recommendations"
echo "=================="

if (( $(echo "$PROGRESS < 50" | bc -l) )); then
    echo "• Focus on high-impact revenue activities"
    echo "• Consider launching promotional campaigns"
    echo "• Review and optimize your sales funnel"
    echo "• Reach out to existing customers for repeat business"
elif (( $(echo "$PROGRESS < 75" | bc -l) )); then
    echo "• Accelerate marketing efforts"
    echo "• Consider special offers or discounts"
    echo "• Leverage your top-performing sources more"
    echo "• Explore partnerships or collaborations"
else
    echo "• Maintain current momentum"
    echo "• Consider setting higher goals for next period"
    echo "• Focus on sustaining growth rather than acceleration"
    echo "• Document what's working well for replication"
fi

echo ""
echo "🎯 Action Items"
echo "==============="
echo "1. Review top-performing revenue sources and double down on them"
echo "2. Identify underperforming sources and analyze improvement opportunities"
echo "3. Consider adding new revenue streams for diversification"
echo "4. Set specific daily/weekly targets to stay on track"
echo "5. Schedule regular check-ins to monitor progress"

echo ""
echo "📅 Next Check Recommended: $(date -d '+7 days' +%Y-%m-%d)"
echo ""
echo "💪 Keep pushing forward! Every dollar counts toward your goals."