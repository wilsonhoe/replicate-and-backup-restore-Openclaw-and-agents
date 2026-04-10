#!/usr/bin/env python3
"""
GitHub Skill Integration for OpenClaw
Provides wrapper functions for common GitHub operations using the gh CLI
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

def run_gh_command(args: List[str], repo: Optional[str] = None) -> Dict[str, Any]:
    """Run a gh command and return the result"""
    try:
        cmd = ["gh"] + args
        if repo and "--repo" not in args:
            cmd.extend(["--repo", repo])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Try to parse as JSON if possible
        output = result.stdout.strip()
        if output:
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                return {"output": output, "success": True}
        return {"success": True, "message": "Command executed successfully"}
        
    except subprocess.CalledProcessError as e:
        return {"error": f"GitHub CLI error: {e.stderr}", "success": False}
    except FileNotFoundError:
        return {"error": "GitHub CLI (gh) not found. Please install it first.", "success": False}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "success": False}

def check_pr_status(pr_number: int, repo: str) -> Dict[str, Any]:
    """Check CI status on a PR"""
    return run_gh_command(["pr", "checks", str(pr_number)], repo)

def list_recent_workflows(repo: str, limit: int = 10) -> Dict[str, Any]:
    """List recent workflow runs"""
    return run_gh_command(["run", "list", "--limit", str(limit), "--json", "databaseId,name,status,conclusion,createdAt"], repo)

def view_workflow_run(run_id: str, repo: str, failed_only: bool = False) -> Dict[str, Any]:
    """View a workflow run and see which steps failed"""
    args = ["run", "view", run_id]
    if failed_only:
        args.append("--log-failed")
    return run_gh_command(args, repo)

def get_pr_info(pr_number: int, repo: str, fields: List[str] = None) -> Dict[str, Any]:
    """Get PR information with specific fields"""
    if fields is None:
        fields = ["number", "title", "state", "user", "createdAt", "updatedAt"]
    
    jq_filter = "." + " | .".join(fields)
    return run_gh_command(["api", f"repos/{repo}/pulls/{pr_number}", "--jq", jq_filter], repo)

def list_issues(repo: str, state: str = "open", limit: int = 10) -> Dict[str, Any]:
    """List issues with JSON output"""
    return run_gh_command([
        "issue", "list", 
        "--state", state, 
        "--limit", str(limit), 
        "--json", "number,title,state,labels,createdAt"
    ], repo)

def create_issue(repo: str, title: str, body: str = "", labels: List[str] = None) -> Dict[str, Any]:
    """Create a new issue"""
    args = ["issue", "create", "--title", title]
    if body:
        args.extend(["--body", body])
    if labels:
        args.extend(["--label", ",".join(labels)])
    return run_gh_command(args, repo)

def clone_repository(repo_url: str, directory: Optional[str] = None) -> Dict[str, Any]:
    """Clone a repository"""
    args = ["repo", "clone", repo_url]
    if directory:
        args.append(directory)
    return run_gh_command(args)

def get_repository_info(repo: str) -> Dict[str, Any]:
    """Get repository information"""
    return run_gh_command(["repo", "view", repo, "--json", "name,owner,description,url,defaultBranch"])

def list_releases(repo: str, limit: int = 5) -> Dict[str, Any]:
    """List recent releases"""
    return run_gh_command(["release", "list", "--limit", str(limit), "--json", "tagName,name,publishedAt"], repo)

def get_rate_limit_status() -> Dict[str, Any]:
    """Check GitHub API rate limit status"""
    return run_gh_command(["api", "rate_limit"])

def test_github_connection() -> Dict[str, Any]:
    """Test GitHub CLI connection and authentication"""
    return run_gh_command(["auth", "status"])

# Example usage and testing
if __name__ == "__main__":
    print("🐙 GitHub Skill Integration - Test Mode")
    print("=" * 50)
    
    # Test GitHub connection
    print("\n1. Testing GitHub connection:")
    result = test_github_connection()
    if result.get("success"):
        print("   ✅ GitHub CLI is working and authenticated")
    else:
        print(f"   ❌ Connection issue: {result.get('error')}")
    
    # Test rate limit
    print("\n2. Checking rate limits:")
    rate_limit = get_rate_limit_status()
    if rate_limit.get("success"):
        print("   ✅ Rate limit check completed")
    else:
        print(f"   ⚠️  Rate limit check: {rate_limit.get('error')}")
    
    print("\n✅ GitHub Skill integration test completed!")
    print("\nExample usage:")
    print("  # Check PR status")
    print("  python3 skills/github/github_integration.py")
    print("  # Then use: check_pr_status(123, 'owner/repo')")
    print("  # List issues: list_issues('owner/repo')")
    print("  # Get repo info: get_repository_info('owner/repo')")