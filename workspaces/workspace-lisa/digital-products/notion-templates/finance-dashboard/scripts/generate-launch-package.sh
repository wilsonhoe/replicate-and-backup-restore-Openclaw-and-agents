#!/bin/bash
# Generate Launch Package for Notion Finance Dashboard
# Usage: ./generate-launch-package.sh

set -e

PRODUCT_DIR="/home/wls/.openclaw/workspace-lisa/digital-products/notion-templates/finance-dashboard"
OUTPUT_DIR="$PRODUCT_DIR/launch-package"
TIMESTAMP=$(date +%Y%m%d_%H%M)

echo "📦 Generating Launch Package for Finance Dashboard"
echo "================================================"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Copy all deliverables
echo "✅ Copying documentation..."
cp "$PRODUCT_DIR/"*.md "$OUTPUT_DIR/" 2>/dev/null || true
cp "$PRODUCT_DIR/gumroad-listing.md" "$OUTPUT_DIR/LISTING_COPY.txt"
cp "$PRODUCT_DIR/launch-announcement.md" "$OUTPUT_DIR/SOCIAL_POSTS.txt"

# Create compressed archive
echo "✅ Creating archive..."
cd "$PRODUCT_DIR"
tar -czf "$OUTPUT_DIR/finance-dashboard-launch-$TIMESTAMP.tar.gz" \
    COMPLETE_TEMPLATE.md \
    TEMPLATE_BUILD_GUIDE.md \
    sales-copy.md \
    gumroad-listing.md \
    launch-announcement.md \
    SCREENSHOT_GUIDE.md \
    GUMROAD_SETUP_COMPLETE.md \
    delivery-package/ 2>/dev/null || true

echo ""
echo "📊 LAUNCH PACKAGE READY"
echo "======================="
echo "Location: $OUTPUT_DIR/"
echo "Archive:  finance-dashboard-launch-$TIMESTAMP.tar.gz"
echo ""
echo "📋 NEXT STEPS (Manual - 70 minutes):"
echo "===================================="
echo "1. Complete Notion template (25 min)"
echo "   - Add properties to remaining 5 databases"
echo "   - Add sample data (2-3 entries each)"
echo "   - Make page public, copy duplicate link"
echo ""
echo "2. Capture screenshots (10 min)"
echo "   - 5-7 PNG images at 1920x1080"
echo "   - Hero, transactions, budget, invoices, goals, forecast, mobile"
echo ""
echo "3. Create delivery PDF (5 min)"
echo "   - Use Canva or Google Docs"
echo "   - Copy from DELIVERY.pdf.txt"
echo ""
echo "4. Gumroad setup (25 min)"
echo "   - Create account, connect Stripe"
echo "   - Create product listing"
echo "   - Upload files and images"
echo "   - Test purchase flow"
echo ""
echo "5. Launch (5 min)"
echo "   - Post announcements on social"
echo ""
echo "💰 EXPECTED REVENUE: $39/sale"
echo "🎯 TARGET: 26 sales = $1,000/month"
echo ""
