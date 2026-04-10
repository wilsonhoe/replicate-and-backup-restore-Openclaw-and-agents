#!/bin/bash
# GitHub Repository Monitor Script
# Monitors wilsonhoe/Digital-Brain repository
# Usage: ./github-monitor.sh [repo] [mode]

REPO="${1:-wilsonhoe/Digital-Brain}"
MODE="${2:-summary}"  # summary, detailed, issues, prs

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 GitHub Repository Monitor${NC}"
echo -e "${BLUE}Repository: $REPO${NC}"
echo -e "${BLUE}Mode: $MODE${NC}"
echo ""

# Function to check if gh CLI is available
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}❌ GitHub CLI is not authenticated${NC}"
        exit 1
    fi
}

# Get repository basic info
get_repo_info() {
    echo -e "${YELLOW}📊 Repository Information${NC}"
    gh api repos/$REPO --jq '. | {
        "Name": .name,
        "Description": .description,
        "Stars": .stargazers_count,
        "Forks": .forks_count,
        "Open Issues": .open_issues_count,
        "Language": (.language // "Not specified"),
        "Default Branch": .default_branch,
        "Created": .created_at,
        "Last Pushed": .pushed_at,
        "Size (KB)": .size
    }' | jq -r 'to_entries | .[] | "\(.key): \(.value)"'
    echo ""
}

# Get recent commits
get_recent_commits() {
    echo -e "${YELLOW}📝 Recent Commits (Last 5)${NC}"
    gh api repos/$REPO/commits --jq '.[0:5] | .[] | {
        sha: .sha[:7],
        message: .commit.message,
        author: .commit.author.name,
        date: .commit.author.date
    }' | jq -r '. | "\(.sha) - \(.message) (by \(.author) on \(.date))"'
    echo ""
}

# Get open issues
get_open_issues() {
    echo -e "${YELLOW}🐛 Open Issues${NC}"
    ISSUES=$(gh issue list --repo $REPO --state open --json number,title,author,createdAt,labels)
    ISSUE_COUNT=$(echo "$ISSUES" | jq length)
    
    if [ "$ISSUE_COUNT" -eq 0 ]; then
        echo -e "${GREEN}✅ No open issues${NC}"
    else
        echo -e "${RED}📋 $ISSUE_COUNT open issues:${NC}"
        echo "$ISSUES" | jq -r '.[] | "  #\(.number): \(.title) (by \(.author.login) on \(.createdAt))"'
    fi
    echo ""
}

# Get open pull requests
get_open_prs() {
    echo -e "${YELLOW}🔀 Open Pull Requests${NC}"
    PRS=$(gh pr list --repo $REPO --state open --json number,title,author,createdAt,headRefName)
    PR_COUNT=$(echo "$PRS" | jq length)
    
    if [ "$PR_COUNT" -eq 0 ]; then
        echo -e "${GREEN}✅ No open pull requests${NC}"
    else
        echo -e "${BLUE}📤 $PR_COUNT open pull requests:${NC}"
        echo "$PRS" | jq -r '.[] | "  #\(.number): \(.title) (by \(.author.login) from \(.headRefName))"'
    fi
    echo ""
}

# Get workflow runs
get_workflow_runs() {
    echo -e "${YELLOW}⚙️ Recent Workflow Runs${NC}"
    WORKFLOWS=$(gh api repos/$REPO/actions/runs --jq '.workflow_runs[0:3] | .[] | {
        name: .name,
        status: .status,
        conclusion: .conclusion,
        created_at: .created_at
    }' 2>/dev/null || echo "[]")
    
    if [ "$WORKFLOWS" = "[]" ] || [ -z "$WORKFLOWS" ]; then
        echo "No workflow runs found or workflows not enabled"
    else
        echo "$WORKFLOWS" | jq -r '. | "  \(.name): \(.status) - \(.conclusion // "N/A") (\(.created_at))"'
    fi
    echo ""
}

# Get repository health metrics
get_health_metrics() {
    echo -e "${YELLOW}🏥 Repository Health${NC}"
    
    # Check if repository is active (pushed within last 30 days)
    LAST_PUSH=$(gh api repos/$REPO --jq '.pushed_at')
    LAST_PUSH_EPOCH=$(date -d "$LAST_PUSH" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$LAST_PUSH" +%s 2>/dev/null || echo "0")
    CURRENT_EPOCH=$(date +%s)
    DAYS_SINCE_PUSH=$(( (CURRENT_EPOCH - LAST_PUSH_EPOCH) / 86400 ))
    
    if [ "$DAYS_SINCE_PUSH" -le 30 ]; then
        echo -e "${GREEN}✅ Active repository (last push $DAYS_SINCE_PUSH days ago)${NC}"
    else
        echo -e "${RED}⚠️  Inactive repository (last push $DAYS_SINCE_PUSH days ago)${NC}"
    fi
    
    # Check issue/PR activity
    OPEN_ISSUES=$(gh api repos/$REPO --jq '.open_issues_count')
    if [ "$OPEN_ISSUES" -eq 0 ]; then
        echo -e "${GREEN}✅ No open issues${NC}"
    elif [ "$OPEN_ISSUES" -le 5 ]; then
        echo -e "${YELLOW}⚡ $OPEN_ISSUES open issues (manageable)${NC}"
    else
        echo -e "${RED}🔥 $OPEN_ISSUES open issues (needs attention)${NC}"
    fi
    
    echo ""
}

# Generate summary report
generate_summary() {
    echo -e "${BLUE}📈 Repository Summary Report${NC}"
    echo "=================================="
    get_repo_info
    get_health_metrics
    
    if [ "$MODE" = "detailed" ]; then
        get_recent_commits
        get_open_issues
        get_open_prs
        get_workflow_runs
    fi
    
    echo -e "${GREEN}✅ Monitoring complete${NC}"
    echo ""
}

# Main execution
main() {
    check_gh_cli
    generate_summary
}

# Run the monitoring
main