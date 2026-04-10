# GitHub Skill - Usage Guide

## Overview
The GitHub skill provides integration with GitHub through the `gh` CLI, enabling you to manage repositories, issues, pull requests, and workflow runs directly from OpenClaw.

## ✅ System Status
- **GitHub CLI**: ✅ Installed and authenticated
- **Integration**: ✅ Python wrapper ready
- **Rate Limits**: ✅ Monitoring available

## 🚀 Quick Start

### Test Connection
```bash
# Check if GitHub CLI is working
gh auth status

# Test the integration
python3 skills/github/github_integration.py
```

### Basic Operations
```python
# Import the integration
from skills.github.github_integration import (
    check_pr_status, list_recent_workflows, view_workflow_run,
    get_pr_info, list_issues, create_issue, get_repository_info
)

# Use with a repository
repo = "owner/repo"  # Replace with your repo
```

## 📋 Common Operations

### Pull Requests
```python
# Check CI status on a PR
check_pr_status(123, repo)

# Get PR information
get_pr_info(123, repo, ["title", "state", "user"])
```

### Issues
```python
# List open issues
list_issues(repo, state="open", limit=10)

# Create a new issue
create_issue(repo, "Bug: Something broken", "Details here...", ["bug", "high-priority"])
```

### Workflow Runs
```python
# List recent workflows
list_recent_workflows(repo, limit=10)

# View a specific run
view_workflow_run("run_id_here", repo)

# View only failed steps
view_workflow_run("run_id_here", repo, failed_only=True)
```

### Repository Info
```python
# Get repository information
get_repository_info(repo)

# List recent releases
list_releases(repo, limit=5)
```

## 🔧 Advanced Usage

### Direct API Calls
```bash
# Use gh api for advanced queries
gh api repos/owner/repo/pulls/123 --jq '.title, .state, .user.login'

# Get specific data fields
gh api repos/owner/repo/issues --jq '.[] | {number: .number, title: .title}'
```

### JSON Output with Filtering
```bash
# Get structured data
gh issue list --repo owner/repo --json number,title,labels --jq '.[] | "\(.number): \(.title)"'

# Complex queries
gh api repos/owner/repo/pulls --jq '.[] | select(.state == "open") | {number, title, author: .user.login}'
```

## 📊 Rate Limit Monitoring
```python
# Check rate limits
current_limits = get_rate_limit_status()
print(f"Rate limit status: {current_limits}")
```

## 🛠️ Setup for Your Repositories

### 1. Configure GitHub CLI (if not done)
```bash
# Login to GitHub
gh auth login

# Set default repository (optional)
gh repo set-default owner/repo
```

### 2. Test with Your Repo
```python
# Replace with your actual repository
your_repo = "your-username/your-repository"

# Test basic operations
test_result = get_repository_info(your_repo)
if test_result.get("success"):
    print(f"✅ Connected to {your_repo}")
else:
    print(f"❌ Error: {test_result.get('error')}")
```

## 💡 Use Cases for Your Setup

### 1. Project Management
- Track issues for your income projects
- Monitor CI/CD workflows
- Manage pull requests for automation scripts

### 2. Documentation
- Create issues for documentation updates
- Track progress on guides and tutorials
- Manage feature requests

### 3. Automation
- Monitor workflow runs for your automated systems
- Get notifications on build failures
- Track deployment status

### 4. Collaboration
- Review and manage contributions
- Track discussions on your projects
- Coordinate with team members

## ⚠️ Important Notes

1. **Authentication**: Ensure `gh auth status` shows you're logged in
2. **Repository Access**: You need appropriate permissions on target repos
3. **Rate Limits**: Monitor usage to avoid hitting GitHub API limits
4. **Privacy**: Be careful with repository names in shared environments

## 🔍 Example Workflow

```python
# Complete example: Monitor a repository
repo = "openclaw/openclaw"

print(f"📊 Repository Status for {repo}")
print("=" * 40)

# Get repo info
info = get_repository_info(repo)
if info.get("success"):
    print(f"Repository: {info.get('output', {}).get('name', 'Unknown')}")

# Check recent issues
issues = list_issues(repo, limit=5)
if issues.get("success"):
    print(f"Recent issues: {len(issues.get('output', []))}")

# Check recent workflows
workflows = list_recent_workflows(repo, limit=3)
if workflows.get("success"):
    print(f"Recent workflows: {len(workflows.get('output', []))}")

print("✅ Status check complete!")
```

## 🆘 Troubleshooting

### Common Issues:
1. **"gh: command not found"** → Install GitHub CLI
2. **"Not logged in"** → Run `gh auth login`
3. **"Repository not found"** → Check repo name format (owner/repo)
4. **"Rate limit exceeded"** → Wait and retry, or use different token

### Getting Help:
```bash
# Check GitHub CLI help
gh --help
gh <command> --help

# Check authentication
gh auth status
```

The GitHub skill is now ready to help you manage your repositories and workflows directly from OpenClaw!