#!/bin/bash
# GitHub Repository Enhancement Script
# Helps improve wilsonhoe/Digital-Brain repository
# Usage: ./github-enhance.sh [repo]

REPO="${1:-wilsonhoe/Digital-Brain}"

echo "🚀 GitHub Repository Enhancement for $REPO"
echo "=========================================="

# Check if gh CLI is available and authenticated
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        echo "❌ GitHub CLI (gh) is not installed"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        echo "❌ GitHub CLI is not authenticated"
        exit 1
    fi
    echo "✅ GitHub CLI authenticated and ready"
}

# Add repository topics
add_topics() {
    echo "📋 Adding repository topics..."
    gh api repos/$REPO/topics --method PUT --input - <<< '{
        "names": ["ai", "automation", "productivity", "ceo-tools", "digital-brain", "openclaw"]
    }' --jq '.names | @tsv' || echo "⚠️  Could not add topics (may already exist or permission issue)"
}

# Create issue templates
create_issue_templates() {
    echo "🎯 Creating issue templates..."
    
    # Create .github directory if it doesn't exist
    TEMP_DIR=$(mktemp -d)
    mkdir -p "$TEMP_DIR/.github/ISSUE_TEMPLATE"
    
    # Bug report template
    cat > "$TEMP_DIR/.github/ISSUE_TEMPLATE/bug_report.md" << 'EOF'
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. iOS]
 - Version: [e.g. 22]

**Additional context**
Add any other context about the problem here.
EOF

    # Feature request template
    cat > "$TEMP_DIR/.github/ISSUE_TEMPLATE/feature_request.md" << 'EOF'
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
EOF

    echo "✅ Issue templates created in temporary directory"
    echo "📁 Templates location: $TEMP_DIR/.github/ISSUE_TEMPLATE/"
    echo "💡 To apply these templates, commit and push them to your repository"
}

# Create a basic CI/CD workflow
create_ci_workflow() {
    echo "⚙️ Creating CI/CD workflow..."
    
    TEMP_DIR=$(mktemp -d)
    mkdir -p "$TEMP_DIR/.github/workflows"
    
    cat > "$TEMP_DIR/.github/workflows/ci.yml" << 'EOF'
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run basic validation
      run: |
        echo "Running basic validation..."
        # Add your validation commands here
        
    - name: Check file structure
      run: |
        echo "Checking repository structure..."
        find . -type f -name "*.md" | head -10
        
    - name: Validate configuration
      run: |
        echo "Validating configuration files..."
        # Add configuration validation here
EOF

    echo "✅ CI workflow created"
    echo "📁 Workflow location: $TEMP_DIR/.github/workflows/ci.yml"
    echo "💡 To enable CI/CD, commit and push this workflow to your repository"
}

# Suggest repository improvements
suggest_improvements() {
    echo "💡 Suggested improvements for $REPO:"
    echo ""
    
    # Check repository description
    DESCRIPTION=$(gh api repos/$REPO --jq '.description')
    if [ -z "$DESCRIPTION" ] || [ "$DESCRIPTION" = "null" ]; then
        echo "❌ No repository description set"
        echo "💡 Add a clear description of what Digital Brain does"
    else
        echo "✅ Repository description: $DESCRIPTION"
    fi
    
    # Check for README
    README_EXISTS=$(gh api repos/$REPO/contents/README.md 2>/dev/null --jq '.type' || echo "null")
    if [ "$README_EXISTS" != "file" ]; then
        echo "❌ No README.md file found"
        echo "💡 Create a comprehensive README with:"
        echo "   - Project overview and purpose"
        echo "   - Installation instructions"
        echo "   - Usage examples"
        echo "   - Contributing guidelines"
    else
        echo "✅ README.md exists"
    fi
    
    # Check for license
    LICENSE_EXISTS=$(gh api repos/$REPO/contents/LICENSE 2>/dev/null --jq '.type' || echo "null")
    if [ "$LICENSE_EXISTS" != "file" ]; then
        echo "❌ No LICENSE file found"
        echo "💡 Add a license file (MIT, Apache 2.0, etc.)"
    else
        echo "✅ LICENSE file exists"
    fi
    
    # Check topics
    TOPICS_COUNT=$(gh api repos/$REPO/topics --jq '.names | length')
    if [ "$TOPICS_COUNT" -eq 0 ]; then
        echo "❌ No repository topics set"
        echo "💡 Add relevant topics: ai, automation, productivity, ceo-tools, digital-brain"
    else
        echo "✅ Repository topics configured ($TOPICS_COUNT topics)"
    fi
    
    # Check for workflows
    WORKFLOWS=$(gh api repos/$REPO/actions/workflows 2>/dev/null --jq '.total_count' || echo "0")
    if [ "$WORKFLOWS" -eq 0 ]; then
        echo "❌ No GitHub Actions workflows"
        echo "💡 Set up CI/CD workflows for:"
        echo "   - Automated testing"
        echo "   - Code quality checks"
        echo "   - Documentation generation"
    else
        echo "✅ GitHub Actions workflows configured ($WORKFLOWS workflows)"
    fi
    
    echo ""
    echo "🎯 Priority Action Items:"
    echo "1. Add comprehensive README.md"
    echo "2. Choose and add a license"
    echo "3. Set up repository topics"
    echo "4. Create issue templates"
    echo "5. Set up basic CI/CD workflow"
}

# Main execution
main() {
    echo "Starting repository enhancement for $REPO..."
    echo ""
    
    check_gh_cli
    suggest_improvements
    
    echo ""
    echo "🛠️ Available Enhancements:"
    echo "1. Add repository topics"
    echo "2. Create issue templates"
    echo "3. Create CI/CD workflow"
    echo ""
    
    read -p "Would you like to apply these enhancements? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        add_topics
        create_issue_templates
        create_ci_workflow
        echo "✅ Enhancement templates created!"
        echo "💡 Review the generated files and commit them to your repository"
    else
        echo "Enhancement templates ready for manual review"
    fi
    
    echo ""
    echo "🎉 Repository enhancement complete!"
}

# Run the enhancement script
main