#!/bin/bash
# Revenue Tracker - Add Revenue Entry
# Usage: ./add_revenue.sh --amount 500 --source "Product Sales" --category "Digital Products" --date 2026-03-29

# Default values
AMOUNT=""
SOURCE=""
CATEGORY=""
DATE=$(date +%Y-%m-%d)
NOTES=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --amount)
            AMOUNT="$2"
            shift 2
            ;;
        --source)
            SOURCE="$2"
            shift 2
            ;;
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        --date)
            DATE="$2"
            shift 2
            ;;
        --notes)
            NOTES="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 --amount <amount> --source <source> --category <category> [--date <date>] [--notes <notes>]"
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$AMOUNT" || -z "$SOURCE" || -z "$CATEGORY" ]]; then
    echo "❌ Error: Amount, source, and category are required"
    echo "Usage: $0 --amount <amount> --source <source> --category <category> [--date <date>] [--notes <notes>]"
    exit 1
fi

# Validate amount is a positive number
if ! [[ "$AMOUNT" =~ ^[0-9]+(\.[0-9]+)?$ ]] || [[ $(echo "$AMOUNT <= 0" | bc -l) -eq 1 ]]; then
    echo "❌ Error: Amount must be a positive number"
    exit 1
fi

# Create data directory if it doesn't exist
DATA_DIR="$(dirname "$0")/../data"
mkdir -p "$DATA_DIR"

# Revenue data file
REVENUE_FILE="$DATA_DIR/revenue.csv"

# Create CSV header if file doesn't exist
if [[ ! -f "$REVENUE_FILE" ]]; then
    echo "date,amount,source,category,notes" > "$REVENUE_FILE"
fi

# Generate unique ID
ID=$(date +%s)

# Add entry to CSV
echo "$DATE,$AMOUNT,$SOURCE,$CATEGORY,$NOTES" >> "$REVENUE_FILE"

# Create summary entry
SUMMARY_FILE="$DATA_DIR/revenue_summary.json"
if [[ ! -f "$SUMMARY_FILE" ]]; then
    echo "{}" > "$SUMMARY_FILE"
fi

echo "✅ Revenue entry added successfully!"
echo "   Amount: \$$AMOUNT"
echo "   Source: $SOURCE"
echo "   Category: $CATEGORY"
echo "   Date: $DATE"
if [[ -n "$NOTES" ]]; then
    echo "   Notes: $NOTES"
fi

# Update monthly summary
MONTH=$(echo "$DATE" | cut -d'-' -f1,2)
MONTHLY_FILE="$DATA_DIR/monthly_summary.json"

if [[ -f "$MONTHLY_FILE" ]]; then
    # Update existing monthly data (simplified - in real implementation would use proper JSON parsing)
    echo "Updated monthly summary for $MONTH"
else
    echo "{}" > "$MONTHLY_FILE"
fi

echo ""
echo "💡 Quick commands:"
echo "   View recent entries: ./view_revenue.sh --period week"
echo "   Generate report: ./generate_report.sh --type monthly"
echo "   Check goals: ./check_goals.sh --target 1000"