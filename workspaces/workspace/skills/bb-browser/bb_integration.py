#!/usr/bin/env python3
"""
bb-browser Integration for OpenClaw
Provides wrapper functions for browser automation using bb-browser
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

def run_bb_command(args: List[str], timeout: int = 30) -> Dict[str, Any]:
    """Run a bb-browser command and return the result"""
    try:
        cmd = ["bb-browser"] + args
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=True)
        
        # Try to parse as JSON if possible
        output = result.stdout.strip()
        if output:
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                return {"output": output, "success": True, "raw": True}
        return {"success": True, "message": "Command executed successfully"}
        
    except subprocess.CalledProcessError as e:
        return {"error": f"bb-browser error: {e.stderr}", "success": False}
    except subprocess.TimeoutExpired:
        return {"error": "Command timed out", "success": False}
    except FileNotFoundError:
        return {"error": "bb-browser not found. Please install it first.", "success": False}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "success": False}

def install_bb_browser() -> Dict[str, Any]:
    """Install bb-browser globally"""
    try:
        result = subprocess.run(["npm", "install", "-g", "bb-browser"], 
                              capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            return {"success": True, "message": "bb-browser installed successfully"}
        else:
            return {"error": f"Installation failed: {result.stderr}", "success": False}
    except Exception as e:
        return {"error": f"Installation error: {str(e)}", "success": False}

def update_sites() -> Dict[str, Any]:
    """Update community adapters"""
    return run_bb_command(["site", "update"])

def get_site_info(site: str) -> Dict[str, Any]:
    """Get information about a specific site adapter"""
    return run_bb_command(["site", "info", site])

def search_platform(platform: str, query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Search on a specific platform"""
    args = ["site", f"{platform}/search", query]
    if limit:
        args.append(str(limit))
    return run_bb_command(args)

def get_social_feed(platform: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get social media feed from a platform"""
    args = ["site", f"{platform}/feed"]
    if limit:
        args.append(str(limit))
    return run_bb_command(args)

def get_trending_content(platform: str, category: Optional[str] = None) -> Dict[str, Any]:
    """Get trending/hot content from a platform"""
    args = ["site", f"{platform}/hot"]
    if category:
        args.append(category)
    return run_bb_command(args)

def get_stock_info(symbol: str, platform: str = "xueqiu") -> Dict[str, Any]:
    """Get stock information"""
    return run_bb_command(["site", f"{platform}/stock", symbol])

def get_hot_stocks(limit: int = 10, platform: str = "xueqiu") -> Dict[str, Any]:
    """Get hot/trending stocks"""
    return run_bb_command(["site", f"{platform}/hot-stock", str(limit)])

def get_youtube_transcript(video_id: str) -> Dict[str, Any]:
    """Get YouTube video transcript"""
    return run_bb_command(["site", "youtube/transcript", video_id])

def search_github_repos(query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Search GitHub repositories"""
    args = ["site", "github/search", query]
    if limit:
        args.append(str(limit))
    return run_bb_command(args)

def get_github_issues(repo: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get GitHub issues for a repository"""
    args = ["site", "github/issues", repo]
    if limit:
        args.append(str(limit))
    return run_bb_command(args)

def search_stackoverflow(query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Search StackOverflow questions"""
    args = ["site", "stackoverflow/search", query]
    if limit:
        args.append(str(limit))
    return run_bb_command(args)

def get_wikipedia_summary(page: str) -> Dict[str, Any]:
    """Get Wikipedia page summary"""
    return run_bb_command(["site", "wikipedia/summary", page])

def get_news_headlines(source: str = "bbc", category: Optional[str] = None) -> Dict[str, Any]:
    """Get news headlines"""
    args = ["site", f"{source}/headlines"]
    if category:
        args.append(category)
    return run_bb_command(args)

def cross_platform_research(query: str, platforms: List[str] = None) -> Dict[str, Any]:
    """Perform cross-platform research on a topic"""
    if platforms is None:
        platforms = ["arxiv", "twitter", "github", "stackoverflow", "zhihu"]
    
    results = {"query": query, "platforms": {}, "success": True}
    
    for platform in platforms:
        try:
            if platform == "arxiv":
                result = search_platform(platform, query)
            elif platform == "twitter":
                result = search_platform(platform, query, 5)
            elif platform == "github":
                result = search_platform(platform, query, 5)
            elif platform == "stackoverflow":
                result = search_platform(platform, query, 5)
            elif platform == "zhihu":
                result = search_platform(platform, query, 3)
            else:
                result = search_platform(platform, query)
            
            results["platforms"][platform] = result
            
        except Exception as e:
            results["platforms"][platform] = {"error": str(e), "success": False}
    
    return results

def browser_automation(command: str, **kwargs) -> Dict[str, Any]:
    """Execute browser automation commands"""
    args = [command]
    for key, value in kwargs.items():
        if value is not None:
            args.extend([f"--{key}", str(value)])
    return run_bb_command(args)

def take_screenshot(url: Optional[str] = None, full_page: bool = False) -> Dict[str, Any]:
    """Take a screenshot of a webpage"""
    if url:
        return run_bb_command(["screenshot", url] + (["--full-page"] if full_page else []))
    else:
        return run_bb_command(["screenshot"] + (["--full-page"] if full_page else []))

def get_page_info(url: str) -> Dict[str, Any]:
    """Get page information (title, meta tags, etc.)"""
    return run_bb_command(["eval", "document.title", "--url", url])

def extract_links(url: str) -> Dict[str, Any]:
    """Extract all links from a page"""
    js_code = "Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.textContent}))"
    return run_bb_command(["eval", js_code, "--url", url])

def test_bb_browser() -> Dict[str, Any]:
    """Test if bb-browser is working"""
    return run_bb_command(["--version"])

def get_available_sites() -> Dict[str, Any]:
    """Get list of available sites/commands"""
    return run_bb_command(["site", "list"])

# Example usage and testing
if __name__ == "__main__":
    print("🌐 bb-browser Integration - Test Mode")
    print("=" * 50)
    
    # Test if bb-browser is available
    print("\n1. Testing bb-browser installation:")
    result = test_bb_browser()
    if result.get("success"):
        print(f"   ✅ bb-browser is available: {result.get('output', 'Unknown version')}")
    else:
        print(f"   ❌ bb-browser not found: {result.get('error')}")
        print("   Install with: npm install -g bb-browser")
        sys.exit(1)
    
    # Test getting available sites
    print("\n2. Getting available sites:")
    sites = get_available_sites()
    if sites.get("success") and sites.get("output"):
        if isinstance(sites["output"], list):
            print(f"   ✅ Found {len(sites['output'])} available sites/commands")
            # Show first 10 as examples
            for site in sites["output"][:10]:
                print(f"     • {site}")
            if len(sites["output"]) > 10:
                print(f"     ... and {len(sites['output']) - 10} more")
        else:
            print(f"   ✅ Sites available: {sites['output']}")
    else:
        print(f"   ⚠️  Could not get sites list: {sites.get('error')}")
    
    # Test a simple search
    print("\n3. Testing GitHub search:")
    github_result = search_github_repos("openclaw", 3)
    if github_result.get("success"):
        print("   ✅ GitHub search working")
        if github_result.get("output"):
            print(f"   Found {len(github_result['output'])} repositories")
    else:
        print(f"   ⚠️  GitHub search test: {github_result.get('error')}")
    
    print("\n✅ bb-browser integration test completed!")
    print("\n📚 Example commands:")
    print("  # Search Twitter for AI agents")
    print("  python3 skills/bb-browser/bb_integration.py")
    print("  # Then use: search_platform('twitter', 'AI agent', 5)")
    print("  # Get trending stocks")
    print("  # get_hot_stocks(10)")
    print("  # Cross-platform research")
    print("  # cross_platform_research('retrieval augmented generation')")