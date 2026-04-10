#!/bin/bash
# Revenue Tracker - View Revenue Entries
# Usage: ./view_revenue.sh --period <period> [--limit <number>]

# Default values
PERIOD="week"
LIMIT=10
FORMAT="table"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --period)
            PERIOD="$2"
            shift 2
            ;;
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--period <week|month|quarter|year|all>] [--limit <number>] [--format <table|csv|json>]"
            exit 1
            ;;
    esac
done

# Validate period
if [[ "$PERIOD" != "week" && "$PERIOD" != "month" && "$PERIOD" != "quarter" && "$PERIOD" != "year" && "$PERIOD" != "all" ]]; then
    echo "❌ Error: Period must be week, month, quarter, year, or all"
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

# Calculate date range
case $PERIOD in
    week)
        START_DATE=$(date -d "7 days ago" +%Y-%m-%d)
        ;;
    month)
        START_DATE=$(date -d "30 days ago" +%Y-%m-%d)
        ;;
    quarter)
        START_DATE=$(date -d "90 days ago" +%Y-%m-%d)
        ;;
    year)
        START_DATE=$(date -d "365 days ago" +%Y-%m-%d)
        ;;
    all)
        START_DATE="1970-01-01"
        ;;
esac

echo "📊 Revenue Entries - Last $PERIOD"
echo "=================================="
echo "Period: $START_DATE to $(date +%Y-%m-%d)"
echo ""

# Filter and display revenue entries based on format
case $FORMAT in
    table)
        echo "Date       | Amount  | Source           | Category         | Notes"
        echo "-----------|---------|------------------|------------------|-------"
        
        # Read CSV and filter by date, then format as table
        tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
            if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]]; then
                printf "%-10s | \$%-6s | %-16s | %-16s | %s\n" "$date" "$amount" "$source" "$category" "$notes"
            fi
        done | tail -n $LIMIT
        ;;
    csv)
        echo "date,amount,source,category,notes"
        tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
            if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]]; then
                echo "$date,$amount,$source,$category,$notes"
            fi
        done | tail -n $LIMIT
        ;;
    json)
        echo "["
        first=true
        tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
            if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]]; then
                if [[ "$first" == true ]]; then
                    first=false
                else
                    echo ","
                fi
                echo "  {"
                echo "    \"date\": \"$date\","
                echo "    \"amount\": $amount,"
                echo "    \"source\": \"$source\","
                echo "    \"category\": \"$category\","
                echo "    \"notes\": \"$notes\""
                echo -n "  }"
            fi
        done | tail -n $LIMIT
        echo ""
        echo "]"
        ;;
esac

echo ""

# Calculate and display summary statistics
echo "📈 Summary Statistics"
echo "====================="

# Calculate total revenue for the period
TOTAL=$(tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
    if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]]; then
        echo "$amount"
    fi
done | awk '{sum += $1} END {print sum}')

# Count entries
COUNT=$(tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
    if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]]; then
        echo "1"
    fi
done | wc -l)

# Calculate average
if [[ "$COUNT" -gt 0 ]]; then
    AVERAGE=$(echo "scale=2; $TOTAL / $COUNT" | bc -l)
else
    AVERAGE=0
fi

echo "Total Revenue: \$$TOTAL"
echo "Number of Entries: $COUNT"
echo "Average per Entry: \$$AVERAGE"

# Show top categories
echo ""
echo "🏷️ Top Categories"
echo "================"
tail -n +2 "$REVENUE_FILE" | while IFS=',' read -r date amount source category notes; do
    if [[ "$date" > "$START_DATE" || "$date" == "$START_DATE" ]]; then
        echo "$category $amount"
    fi
done | awk '{categories[$1] += $2} END {for (cat in categories) print cat ": $" categories[cat]}' | sort -k2 -nr | head -5

echo ""
echo "💡 Next steps:"
echo "   Generate detailed report: ./generate_report.sh --type $PERIOD"
echo "   Check goal progress: ./check_goals.sh"
echo "   Add new entry: ./add_revenue.sh --amount <amount> --source <source> --category <category>"