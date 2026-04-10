#!/usr/bin/env python3
"""
bb-browser Integration for OpenClaw - Updated with correct commands
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
    # Map common platforms to their actual commands
    command_map = {
        "google": "google/search",
        "twitter": "twitter/search", 
        "reddit": "reddit/search",
        "github": None,  # GitHub doesn't have search in current adapter
        "stackoverflow": "stackoverflow/search",
        "youtube": "youtube/search",
        "zhihu": "zhihu/search",
        "baidu": "baidu/search",
        "bing": "bing/search",
        "duckduckgo": "duckduckgo/search",
        "arxiv": "arxiv/search",
        "wikipedia": "wikipedia/search"
    }
    
    if platform in command_map:
        if command_map[platform] is None:
            return {"error": f"Search not available for {platform}", "success": False, "available_commands": get_platform_commands(platform)}
        
        args = ["site", command_map[platform], query]
        if limit:
            args.append(str(limit))
        return run_bb_command(args)
    else:
        # Try direct command
        args = ["site", f"{platform}/search", query]
        if limit:
            args.append(str(limit))
        return run_bb_command(args)

def get_platform_commands(platform: str) -> List[str]:
    """Get available commands for a platform"""
    platform_commands = {
        "twitter": ["search", "bookmarks", "notifications", "thread", "tweets", "user"],
        "reddit": ["search", "hot", "posts", "thread", "context"],
        "github": ["repo", "issues", "me", "fork", "issue-create", "pr-create"],
        "youtube": ["search", "video", "channel", "comments", "transcript", "feed"],
        "zhihu": ["search", "hot", "question", "me"],
        "weibo": ["search", "hot", "feed", "user", "user_posts", "comments", "me"],
        "xueqiu": ["stock", "search", "hot-stock", "feed", "hot", "watchlist"],
        "bilibili": ["search", "video", "popular", "ranking", "comments", "feed", "history", "me", "trending"],
        "douban": ["search", "movie", "movie-hot", "movie-top", "top250", "comments"],
        "stackoverflow": ["search"],
        "arxiv": ["search"],
        "wikipedia": ["search", "summary"],
        "news": ["bbc/headlines", "reuters/search", "36kr/newsflash", "toutiao/hot", "toutiao/search"]
    }
    return platform_commands.get(platform, [])

def get_social_feed(platform: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get social media feed from a platform"""
    feed_commands = {
        "twitter": "twitter/feed",
        "reddit": "reddit/hot", 
        "weibo": "weibo/feed",
        "bilibili": "bilibili/feed",
        "zhihu": "zhihu/hot",
        "jike": "jike/feed"
    }
    
    if platform in feed_commands:
        args = ["site", feed_commands[platform]]
        if limit:
            args.append(str(limit))
        return run_bb_command(args)
    else:
        return {"error": f"Feed not available for {platform}", "success": False}

def get_trending_content(platform: str, category: Optional[str] = None) -> Dict[str, Any]:
    """Get trending/hot content from a platform"""
    trending_commands = {
        "twitter": "twitter/search",  # Use search for trending
        "reddit": "reddit/hot",
        "weibo": "weibo/hot",
        "zhihu": "zhihu/hot",
        "bilibili": "bilibili/popular",
        "douban": "douban/movie-hot",
        "v2ex": "v2ex/hot",
        "hackernews": "hackernews/top",
        "toutiao": "toutiao/hot",
        "hupu": "hupu/hot"
    }
    
    if platform in trending_commands:
        args = ["site", trending_commands[platform]]
        if category:
            args.append(category)
        return run_bb_command(args)
    else:
        return {"error": f"Trending not available for {platform}", "success": False}

def get_stock_info(symbol: str, platform: str = "xueqiu") -> Dict[str, Any]:
    """Get stock information"""
    return run_bb_command(["site", f"{platform}/stock", symbol])

def get_hot_stocks(limit: int = 10, platform: str = "xueqiu") -> Dict[str, Any]:
    """Get hot/trending stocks"""
    return run_bb_command(["site", f"{platform}/hot-stock", str(limit)])

def get_youtube_transcript(video_id: str) -> Dict[str, Any]:
    """Get YouTube video transcript"""
    return run_bb_command(["site", "youtube/transcript", video_id])

def get_github_repo_info(repo: str) -> Dict[str, Any]:
    """Get GitHub repository information"""
    return run_bb_command(["site", "github/repo", repo])

def get_github_issues(repo: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get GitHub issues for a repository"""
    args = ["site", "github/issues", repo]
    if limit:
        args.append(str(limit))
    return run_bb_command(args)

def get_github_user_info() -> Dict[str, Any]:
    """Get current GitHub user information"""
    return run_bb_command(["site", "github/me"])

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
    news_sources = {
        "bbc": "bbc/news",
        "reuters": "reuters/search",
        "36kr": "36kr/newsflash",
        "toutiao": "toutiao/hot"
    }
    
    if source in news_sources:
        args = ["site", news_sources[source]]
        if category:
            args.append(category)
        return run_bb_command(args)
    else:
        return {"error": f"News source {source} not available", "success": False}

def cross_platform_research(query: str, platforms: List[str] = None) -> Dict[str, Any]:
    """Perform cross-platform research on a topic"""
    if platforms is None:
        platforms = ["arxiv", "twitter", "reddit", "stackoverflow", "zhihu"]
    
    results = {"query": query, "platforms": {}, "success": True}
    
    for platform in platforms:
        try:
            if platform == "arxiv":
                result = search_platform(platform, query)
            elif platform == "twitter":
                result = search_platform(platform, query, 5)
            elif platform == "reddit":
                result = get_trending_content(platform)  # Reddit hot posts
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

def get_bilibili_video_info(bvid: str) -> Dict[str, Any]:
    """Get Bilibili video information"""
    return run_bb_command(["site", "bilibili/video", bvid])

def get_douban_movie_info(movie_id: str) -> Dict[str, Any]:
    """Get Douban movie information"""
    return run_bb_command(["site", "douban/movie", movie_id])

def get_weibo_user_posts(username: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """Get Weibo user posts"""
    args = ["site", "weibo/user_posts", username]
    if limit:
        args.append(str(limit))
    return run_bb_command(args)

def translate_text(text: str, platform: str = "youdao") -> Dict[str, Any]:
    """Translate text"""
    return run_bb_command(["site", f"{platform}/translate", text])

def get_producthunt_trending() -> Dict[str, Any]:
    """Get Product Hunt trending products"""
    return run_bb_command(["site", "producthunt/today"])

def test_bb_browser() -> Dict[str, Any]:
    """Test if bb-browser is working"""
    return run_bb_command(["--version"])

def get_available_sites() -> Dict[str, Any]:
    """Get list of available sites/commands"""
    return run_bb_command(["site", "list"])

def get_recommendations() -> Dict[str, Any]:
    """Get site recommendations based on browsing habits"""
    return run_bb_command(["site", "recommend"])

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
    
    # Test a working command - get trending on Reddit
    print("\n3. Testing Reddit trending:")
    reddit_result = get_trending_content("reddit", 3)
    if reddit_result.get("success"):
        print("   ✅ Reddit trending working")
        if reddit_result.get("output"):
            print(f"   Found {len(reddit_result['output'])} trending posts")
    else:
        print(f"   ⚠️  Reddit test: {reddit_result.get('error')}")
    
    # Test hot stocks
    print("\n4. Testing hot stocks:")
    stocks_result = get_hot_stocks(5)
    if stocks_result.get("success"):
        print("   ✅ Hot stocks working")
        if stocks_result.get("output"):
            print(f"   Found {len(stocks_result['output'])} hot stocks")
    else:
        print(f"   ⚠️  Hot stocks test: {stocks_result.get('error')}")
    
    print("\n✅ bb-browser integration test completed!")
    print("\n📚 Example commands:")
    print("  # Search Twitter for AI agents")
    print("  python3 skills/bb-browser/bb_integration.py")
    print("  # Then use: search_platform('twitter', 'AI agent', 5)")
    print("  # Get trending stocks")
    print("  # get_hot_stocks(10)")
    print("  # Cross-platform research")
    print("  # cross_platform_research('retrieval augmented generation')")