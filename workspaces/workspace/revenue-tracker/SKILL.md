---
name: revenue-tracker
description: Track and analyze business revenue, income streams, and financial performance. Use when monitoring income sources, analyzing revenue trends, setting financial targets, or tracking progress toward income goals. Triggers on phrases like "track revenue", "monitor income", "analyze earnings", "revenue report", "income tracking", "financial performance".
---

# Revenue Tracker

AI-powered revenue tracking and analysis system designed for entrepreneurs and business owners working toward income goals.

## Overview

Transform your revenue tracking from manual spreadsheets into intelligent, automated financial monitoring that provides actionable insights for growing your business income.

## Core Capabilities

### 1. Multi-Stream Income Tracking
- Track multiple revenue sources (products, services, affiliate income, investments)
- Categorize income by type, source, and time period
- Monitor recurring vs one-time revenue
- Track seasonal patterns and trends

### 2. Revenue Analytics & Insights
- Calculate key metrics (MRR, ARR, growth rates, churn)
- Identify top-performing income streams
- Analyze revenue concentration and diversification
- Project future earnings based on historical data

### 3. Goal Setting & Progress Monitoring
- Set and track income targets ($1K/month, $10K/month, etc.)
- Monitor progress toward financial goals
- Receive alerts when off-track
- Get recommendations for goal achievement

### 4. Automated Reporting
- Generate daily, weekly, monthly revenue reports
- Create visual charts and trend analysis
- Export data for tax and accounting purposes
- Schedule automated report delivery

## Quick Start

### Track New Revenue
```bash
# Add revenue entry
./scripts/add_revenue.sh --amount 500 --source "Product Sales" --category "Digital Products"

# View recent revenue
./scripts/view_revenue.sh --period week

# Generate report
./scripts/generate_report.sh --type monthly --format markdown
```

### Analyze Performance
```bash
# Check goal progress
./scripts/check_goals.sh --target 1000 --period monthly

# Identify top sources
./scripts/top_sources.sh --limit 5 --period quarter

# Revenue trends
./scripts/revenue_trends.sh --period year --chart line
```

## Revenue Categories

### Digital Products
- Online courses and educational content
- Software licenses and SaaS subscriptions
- Digital templates and tools
- E-books and guides

### Services
- Consulting and coaching
- Freelance work and contracts
- Speaking engagements
- Training and workshops

### Passive Income
- Affiliate commissions
- Advertising revenue
- Investment returns
- Royalty payments

### Physical Products
- Merchandise sales
- Book sales
- Hardware products
- Subscription boxes

## Key Metrics Dashboard

### Revenue Performance
- **Total Revenue**: Current period vs previous
- **Growth Rate**: Month-over-month and year-over-year
- **Average Revenue Per Source**: Identify top performers
- **Revenue Concentration**: Risk assessment of income distribution

### Goal Tracking
- **Progress to Target**: Percentage completion of income goals
- **Trajectory Analysis**: Are you on track to meet targets?
- **Gap Analysis**: What's needed to reach goals
- **Timeline Projections**: When will targets be achieved?

### Trend Analysis
- **Seasonal Patterns**: Identify recurring revenue cycles
- **Growth Trends**: Acceleration or deceleration patterns
- **Source Performance**: Which streams are growing/declining
- **Market Correlation**: External factors affecting revenue

## Advanced Analytics

### Revenue Forecasting
```bash
# Project next month's revenue
./scripts/forecast_revenue.sh --period month --confidence 0.95

# Scenario planning
./scripts/scenario_analysis.sh --growth-rate 0.15 --months 6
```

### Risk Assessment
```bash
# Revenue concentration analysis
./scripts/concentration_risk.sh --threshold 0.3

# Dependency analysis
./scripts/dependency_check.sh --sources 3
```

### Optimization Recommendations
```bash
# Revenue optimization suggestions
./scripts/optimization_suggestions.sh --focus growth

# Pricing analysis
./scripts/pricing_analysis.sh --category "digital-products"
```

## Integration with Business Systems

### OpenClaw Integration
- Automatic revenue tracking through OpenClaw workflows
- Integration with memory system for historical analysis
- Coordination with other business skills (marketing, operations)
- Automated alerting through messaging systems

### External Platform Integration
- Stripe/PayPal transaction import
- Affiliate network data synchronization
- Investment account performance tracking
- E-commerce platform revenue aggregation

## Configuration

### Environment Setup
```bash
# Copy configuration template
cp config/revenue-tracker.example.json config/revenue-tracker.json

# Set your income goals
nano config/revenue-tracker.json
```

### Configuration Options
```json
{
  "goals": {
    "monthly_target": 1000,
    "quarterly_target": 3000,
    "annual_target": 12000
  },
  "categories": ["digital-products", "services", "affiliate", "investments"],
  "alerting": {
    "daily_summary": true,
    "goal_milestone": true,
    "unusual_activity": true
  },
  "reporting": {
    "format": "markdown",
    "frequency": "daily",
    "include_charts": true
  }
}
```

## Monitoring & Alerts

### Automated Monitoring
- Daily revenue summary reports
- Goal milestone notifications
- Unusual revenue pattern alerts
- Source performance degradation warnings

### Custom Alerts
```bash
# Set up custom alert
./scripts/setup_alert.sh --condition "revenue < 500" --period month

# Configure notification channels
./scripts/setup_notifications.sh --email --slack --telegram
```

## Best Practices

### Data Quality
- **Consistent Recording**: Track revenue immediately when received
- **Accurate Categorization**: Use consistent categories for meaningful analysis
- **Regular Validation**: Cross-check with bank statements and platform reports
- **Backup Strategy**: Maintain multiple copies of revenue data

### Analysis Frequency
- **Daily**: Quick status checks and unusual activity monitoring
- **Weekly**: Performance reviews and short-term trend analysis
- **Monthly**: Comprehensive reporting and goal assessment
- **Quarterly**: Strategic planning and major adjustments

### Goal Setting
- **SMART Goals**: Specific, Measurable, Achievable, Relevant, Time-bound
- **Progressive Targets**: Gradually increase goals as you grow
- **Multiple Timeframes**: Set daily, weekly, monthly, and annual targets
- **Flexibility**: Adjust goals based on market conditions and learnings

## Troubleshooting

### Common Issues
- **Missing Revenue Entries**: Check data import scripts and manual recording
- **Incorrect Categorization**: Review category definitions and assignment logic
- **Goal Tracking Errors**: Verify target calculations and date ranges
- **Report Generation Failures**: Check data integrity and file permissions

### Performance Optimization
- **Large Dataset Handling**: Implement data archiving for historical records
- **Calculation Accuracy**: Use appropriate precision for financial calculations
- **Memory Management**: Optimize for long-running revenue tracking sessions
- **Integration Efficiency**: Minimize API calls and external dependencies

## Revenue Growth Strategies

### Scaling Existing Sources
- **Product Line Expansion**: Add complementary products to successful lines
- **Service Enhancement**: Improve and increase pricing of current services
- **Geographic Expansion**: Reach new markets with proven offerings
- **Partnership Development**: Create affiliate and referral programs

### Diversification
- **New Revenue Streams**: Develop additional income sources to reduce risk
- **Passive Income**: Create systems that generate revenue without active involvement
- **Recurring Revenue**: Build subscription and membership models
- **High-Margin Products**: Focus on offerings with better profit margins

This revenue tracker skill transforms scattered income data into actionable business intelligence, helping you systematically grow toward your $1K/month and beyond revenue goals.