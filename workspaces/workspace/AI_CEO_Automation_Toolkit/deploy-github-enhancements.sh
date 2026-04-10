#!/bin/bash
# GitHub Repository Enhancement Deployment Script
# Deploys enhanced README, CI/CD workflow, and repository improvements
# Usage: ./deploy-github-enhancements.sh

REPO="wilsonhoe/Digital-Brain"
BRANCH="main"

echo "🚀 Deploying GitHub Repository Enhancements"
echo "==========================================="
echo "Repository: $REPO"
echo "Branch: $BRANCH"
echo ""

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

# Create temporary directory for enhancements
setup_temp_dir() {
    TEMP_DIR=$(mktemp -d)
    echo "📁 Working directory: $TEMP_DIR"
    cd "$TEMP_DIR"
}

# Clone the repository
clone_repo() {
    echo "📥 Cloning repository..."
    gh repo clone "$REPO" digital-brain
    cd digital-brain
    echo "✅ Repository cloned successfully"
}

# Create enhanced README
create_enhanced_readme() {
    echo "📝 Creating enhanced README..."
    
    # Copy the enhanced README from workspace
    cp /home/wls/.openclaw/workspace/enhanced-README.md README.md
    
    echo "✅ Enhanced README created"
}

# Create CI/CD workflow
create_cicd_workflow() {
    echo "⚙️ Creating CI/CD workflow..."
    
    mkdir -p .github/workflows
    cp /home/wls/.openclaw/workspace/ci-cd-workflow.yml .github/workflows/ci.yml
    
    echo "✅ CI/CD workflow created"
}

# Create additional repository files
create_additional_files() {
    echo "📄 Creating additional repository files..."
    
    # Create CONTRIBUTING.md
    cat > CONTRIBUTING.md << 'EOF'
# Contributing to Digital Brain

Thank you for your interest in contributing to Digital Brain! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📋 Development Guidelines

### Code Style
- Follow existing code formatting patterns
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular

### Testing
- Test your changes thoroughly
- Add tests for new features
- Ensure all existing tests pass
- Test edge cases and error conditions

### Documentation
- Update README.md if needed
- Add inline comments for complex code
- Update configuration documentation
- Include usage examples

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, versions)

## 💡 Feature Requests

For feature requests, please provide:
- Clear description of the feature
- Use cases and benefits
- Implementation suggestions
- Potential impact on existing functionality

## 📞 Contact

For questions or discussions:
- Open an issue in the repository
- Start a discussion in GitHub Discussions
- Contact the maintainers

Thank you for contributing to Digital Brain! 🙏
EOF

    # Create .gitignore
    cat > .gitignore << 'EOF'
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs/
*.log

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env.test

# Stores VSCode versions used for testing VSCode extensions
.vscode-test

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# Temporary files
tmp/
temp/
*.tmp

# Build outputs
dist/
build/
*.tar.gz

# Database files
*.db
*.sqlite
*.sqlite3

# Configuration backups
*.bak
*.backup
config/*.local.json
EOF

    # Create basic package.json if it doesn't exist
    if [ ! -f "package.json" ]; then
        cat > package.json << 'EOF'
{
  "name": "digital-brain",
  "version": "1.0.0",
  "description": "Digital Brain for AI CEO - Intelligent automation and strategic insights",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "start": "node index.js",
    "lint": "echo \"Linting not configured\"",
    "format": "echo \"Formatting not configured\""
  },
  "keywords": [
    "ai",
    "automation",
    "ceo-tools",
    "digital-brain",
    "openclaw",
    "productivity"
  ],
  "author": "Wilson",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/wilsonhoe/Digital-Brain.git"
  },
  "bugs": {
    "url": "https://github.com/wilsonhoe/Digital-Brain/issues"
  },
  "homepage": "https://github.com/wilsonhoe/Digital-Brain#readme"
}
EOF
    fi
    
    echo "✅ Additional files created"
}

# Create issue templates
create_issue_templates() {
    echo "🎯 Creating issue templates..."
    
    mkdir -p .github/ISSUE_TEMPLATE
    
    # Bug report template
    cat > .github/ISSUE_TEMPLATE/bug_report.yml << 'EOF'
name: Bug Report
description: Report a bug to help us improve
title: '[BUG] '
labels: ['bug', 'triage']
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug in Digital Brain!
        Please fill out the sections below to help us understand and fix the issue.
  
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
      placeholder: Describe the bug...
    validations:
      required: true
  
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. Scroll down to '...'
        4. See error
    validations:
      required: true
  
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: A clear description of what you expected to happen.
      placeholder: What should have happened?
    validations:
      required: true
  
  - type: dropdown
    id: severity
    attributes:
      label: Severity
      description: How severe is this bug?
      options:
        - Low - Minor inconvenience
        - Medium - Affects functionality but has workaround
        - High - Major functionality broken
        - Critical - System unusable
    validations:
      required: true
  
  - type: input
    id: environment
    attributes:
      label: Environment
      description: Your operating system and version
      placeholder: e.g., Ubuntu 22.04, macOS 13.1, Windows 11
    validations:
      required: true
  
  - type: textarea
    id: logs
    attributes:
      label: Logs/Screenshots
      description: Any relevant logs, error messages, or screenshots
      placeholder: Paste logs or describe what you see
      render: shell
  
  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have searched for similar issues
          required: true
        - label: I have provided detailed reproduction steps
          required: true
        - label: I have tested with the latest version
          required: true
EOF

    # Feature request template
    cat > .github/ISSUE_TEMPLATE/feature_request.yml << 'EOF'
name: Feature Request
description: Suggest a new feature or enhancement
title: '[FEATURE] '
labels: ['enhancement', 'triage']
body:
  - type: markdown
    attributes:
      value: |
        Thank you for suggesting a feature for Digital Brain!
        Your input helps make this project better for everyone.
  
  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: Is your feature request related to a problem? Please describe.
      placeholder: I'm always frustrated when...
    validations:
      required: true
  
  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: A clear description of what you want to happen.
      placeholder: I would like...
    validations:
      required: true
  
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Describe any alternative solutions you've considered.
      placeholder: I also considered...
  
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      description: How important is this feature to you?
      options:
        - Low - Nice to have
        - Medium - Would improve workflow
        - High - Significant improvement needed
        - Critical - Blocking important work
    validations:
      required: true
  
  - type: textarea
    id: use-case
    attributes:
      label: Use Case
      description: Describe the specific use case or workflow where this would be helpful
      placeholder: This would help me when...
    validations:
      required: true
  
  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I have searched for similar feature requests
          required: true
        - label: I have considered the impact on existing functionality
          required: true
        - label: I am willing to help implement this feature (if applicable)
          required: false
EOF
    
    echo "✅ Issue templates created"
}

# Show deployment preview
show_preview() {
    echo "📋 Deployment Preview:"
    echo "======================"
    echo ""
    
    echo "Files to be added/modified:"
    echo "├── README.md (enhanced)"
    echo "├── .github/workflows/ci.yml (new)"
    echo "├── .github/ISSUE_TEMPLATE/"
    echo "│   ├── bug_report.yml"
    echo "│   └── feature_request.yml"
    echo "├── CONTRIBUTING.md (new)"
    echo "├── .gitignore (new/enhanced)"
    echo "└── package.json (enhanced)"
    echo ""
    
    echo "Repository improvements:"
    echo "✅ Comprehensive README with setup instructions"
    echo "✅ CI/CD pipeline with quality checks"
    echo "✅ Issue templates for better community engagement"
    echo "✅ Contributing guidelines"
    echo "✅ Proper .gitignore configuration"
    echo "✅ Enhanced package.json with keywords"
    echo ""
}

# Commit and push changes
commit_changes() {
    echo "💾 Committing changes..."
    
    # Check if there are changes to commit
    if [ -n "$(git status --porcelain)" ]; then
        git add .
        git commit -m "🚀 Enhance repository with comprehensive documentation and CI/CD

- Add detailed README with installation and usage instructions
- Set up GitHub Actions CI/CD pipeline with quality checks
- Create issue templates for bug reports and feature requests
- Add contributing guidelines and development setup
- Configure proper .gitignore and package.json
- Implement automated testing and security scanning

This enhancement prepares the repository for community engagement and
systematic development with proper automation and documentation."
        
        echo "✅ Changes committed"
        
        # Push changes
        read -p "Push changes to GitHub? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push origin "$BRANCH"
            echo "✅ Changes pushed to GitHub"
        else
            echo "💡 Changes committed locally. Push manually when ready:"
            echo "   git push origin $BRANCH"
        fi
    else
        echo "ℹ️  No changes to commit"
    fi
}

# Main execution
main() {
    echo "Starting GitHub repository enhancement deployment..."
    echo ""
    
    check_gh_cli
    setup_temp_dir
    clone_repo
    
    show_preview
    
    read -p "Proceed with enhancements? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_enhanced_readme
        create_cicd_workflow
        create_additional_files
        create_issue_templates
        
        echo ""
        echo "🎉 Repository enhancements created!"
        echo ""
        
        commit_changes
        
        echo ""
        echo "✨ Repository enhancement complete!"
        echo ""
        echo "Next steps:"
        echo "1. Review the changes in your repository"
        echo "2. Enable GitHub Actions in repository settings"
        echo "3. Monitor the first CI/CD run"
        echo "4. Share your enhanced repository with the community"
        echo ""
        echo "Repository URL: https://github.com/$REPO"
    else
        echo "Enhancement deployment cancelled"
    fi
    
    # Cleanup
    cd /
    rm -rf "$TEMP_DIR"
}

# Run the deployment script
main