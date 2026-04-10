#!/usr/bin/env python3
"""
GitHub Skill Hook for OpenClaw
Monitors GitHub repositories for issues, PRs, and workflow status
"""

import json
import sys
from pathlib import Path

# Add the skills directory to path
sys.path.insert(0, str(Path.home() / ".openclaw" / "workspace" / "skills" / "github"))

try:
    from github_integration import (
        list_issues, list_recent_workflows, get_repository_info,
        test_github_connection
    )
except ImportError:
    print("GitHub integration not available")
    sys.exit(1)

def check_github_status(repos):
    """Check status of monitored repositories"""
    results = []
    
    for repo in repos:
        try:
            # Get repo info
            repo_info = get_repository_info(repo)
            if not repo_info.get("success"):
                results.append(f"❌ {repo}: {repo_info.get('error')}")
                continue
            
            # Check for open issues
            issues = list_issues(repo, state="open", limit=5)
            issue_count = len(issues.get("output", [])) if issues.get("success") else 0
            
            # Check recent workflows
            workflows = list_recent_workflows(repo, limit=3)
            workflow_status = "✅ OK"
            if workflows.get("success") and workflows.get("output"):
                recent_workflows = workflows["output"]
                failed_workflows = [w for w in recent_workflows if w.get("conclusion") == "failure"]
                if failed_workflows:
                    workflow_status = f"❌ {len(failed_workflows)} failed"
            
            results.append(f"📊 {repo}: {issue_count} open issues, workflows {workflow_status}")
            
        except Exception as e:
            results.append(f"⚠️ {repo}: Error checking - {str(e)}")
    
    return results

def main():
    """Main hook function"""
    print("🔍 GitHub Repository Monitor")
    
    # Test GitHub connection first
    connection_test = test_github_connection()
    if not connection_test.get("success"):
        print(f"❌ GitHub connection issue: {connection_test.get('error')}")
        return
    
    # Define repositories to monitor (customize this list)
    monitored_repos = [
        "openclaw/openclaw",  # Main OpenClaw repo
        # Add your repositories here:
        # "your-username/your-repo",
        # "your-username/another-repo",
    ]
    
    if not monitored_repos or monitored_repos == ["openclaw/openclaw"]:
        print("ℹ️  No custom repositories configured. Add your repos to the monitored_repos list.")
        return
    
    print(f"📡 Monitoring {len(monitored_repos)} repositories...")
    
    # Check status of all repos
    status_results = check_github_status(monitored_repos)
    
    if status_results:
        print("Repository Status:")
        for result in status_results:
            print(f"  {result}")
        
        # Check if any need attention
        attention_needed = [r for r in status_results if "❌" in r or "⚠️" in r]
        if attention_needed:
            print(f"\n⚠️  {len(attention_needed)} repositories need attention!")
            return {
                "action": "alert",
                "message": f"GitHub repositories need attention: {len(attention_needed)} issues found",
                "details": attention_needed
            }
        else:
            print("\n✅ All repositories are healthy!")
            return {
                "action": "status",
                "message": "All GitHub repositories are healthy",
                "repositories": len(monitored_repos)
            }
    else:
        print("ℹ️  No repositories to monitor")
        return {"action": "none", "message": "No repositories configured for monitoring"}

if __name__ == "__main__":
    result = main()
    if isinstance(result, dict):
        print(json.dumps(result, indent=2))