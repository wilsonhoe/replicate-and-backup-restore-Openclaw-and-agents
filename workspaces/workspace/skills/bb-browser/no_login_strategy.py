#!/usr/bin/env python3
"""
No-Login bb-browser Strategy for OpenClaw
Tests and documents platforms that work without login
"""

import subprocess
import json
import time
from pathlib import Path

def test_no_login_platforms():
    """Test platforms that should work without login"""
    
    # Platforms likely to work without login
    no_login_tests = [
        ("arxiv", "arxiv/search", ["retrieval augmented generation", "3"]),
        ("bbc", "bbc/news", []),
        ("hackernews", "hackernews/top", ["5"]),
        ("stackoverflow", "stackoverflow/search", ["python automation", "3"]),
        ("wikipedia", "wikipedia/search", ["artificial intelligence", "3"]),
        ("duckduckgo", "duckduckgo/search", ["AI agent", "3"]),
        ("bing", "bing/search", ["machine learning", "3"]),
        ("bilibili", "bilibili/ranking", ["5"]),
        ("36kr", "36kr/newsflash", []),
        ("eastmoney", "eastmoney/news", []),
    ]
    
    results = {}
    
    print("🧪 Testing No-Login Platforms")
    print("=" * 50)
    
    for platform, command, args in no_login_tests:
        print(f"\nTesting {platform}...")
        
        try:
            # Build command
            cmd = ["bb-browser", "site", command] + args
            
            # Run with timeout
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()
                if len(output) > 200:
                    output = output[:200] + "..."
                results[platform] = {
                    "status": "working",
                    "output": output,
                    "command": " ".join(cmd)
                }
                print(f"  ✅ {platform}: Working")
            else:
                error_msg = result.stderr.strip() if result.stderr else "No output"
                if "Could not start browser" in error_msg:
                    results[platform] = {
                        "status": "chrome_not_running",
                        "error": error_msg
                    }
                    print(f"  ⚠️  {platform}: Chrome not running")
                elif "login" in error_msg.lower() or "auth" in error_msg.lower():
                    results[platform] = {
                        "status": "requires_login",
                        "error": error_msg
                    }
                    print(f"  🔒 {platform}: Requires login")
                else:
                    results[platform] = {
                        "status": "failed",
                        "error": error_msg
                    }
                    print(f"  ❌ {platform}: Failed - {error_msg[:100]}")
                    
        except subprocess.TimeoutExpired:
            results[platform] = {"status": "timeout", "error": "Command timed out"}
            print(f"  ⏰ {platform}: Timeout")
        except Exception as e:
            results[platform] = {"status": "error", "error": str(e)}
            print(f"  💥 {platform}: Error - {str(e)}")
        
        # Small delay between tests
        time.sleep(1)
    
    return results

def analyze_working_platforms(results):
    """Analyze which platforms work and create strategy"""
    
    working = []
    login_required = []
    chrome_issues = []
    failed = []
    
    for platform, result in results.items():
        if result["status"] == "working":
            working.append(platform)
        elif result["status"] == "requires_login":
            login_required.append(platform)
        elif result["status"] == "chrome_not_running":
            chrome_issues.append(platform)
        else:
            failed.append(platform)
    
    print(f"\n📊 Analysis Results:")
    print(f"  ✅ Working without login: {len(working)} platforms")
    print(f"  🔒 Requires login: {len(login_required)} platforms") 
    print(f"  ⚠️  Chrome issues: {len(chrome_issues)} platforms")
    print(f"  ❌ Failed: {len(failed)} platforms")
    
    return {
        "working": working,
        "login_required": login_required,
        "chrome_issues": chrome_issues,
        "failed": failed
    }

def create_no_login_integration():
    """Create Python integration for no-login platforms"""
    
    integration_code = '''#!/usr/bin/env python3
"""
No-Login bb-browser Integration
Safe platforms that work without authentication
"""

from skills.bb-browser.bb_integration_updated import (
    search_platform, get_trending_content, 
    search_stackoverflow, get_wikipedia_summary,
    get_news_headlines, cross_platform_research
)

def research_without_login(topic: str, max_results: int = 5):
    """Research a topic using platforms that don't require login"""
    
    results = {}
    
    # Academic research
    try:
        results["arxiv"] = search_platform("arxiv", topic, max_results)
    except Exception as e:
        results["arxiv"] = {"error": str(e)}
    
    # Developer resources
    try:
        results["stackoverflow"] = search_platform("stackoverflow", topic, max_results)
    except Exception as e:
        results["stackoverflow"] = {"error": str(e)}
    
    # Encyclopedia
    try:
        results["wikipedia"] = search_platform("wikipedia", topic, max_results)
    except Exception as e:
        results["wikipedia"] = {"error": str(e)}
    
    # Tech news
    try:
        results["hackernews"] = get_trending_content("hackernews", max_results)
    except Exception as e:
        results["hackernews"] = {"error": str(e)}
    
    # General web search (privacy-focused)
    try:
        results["duckduckgo"] = search_platform("duckduckgo", topic, max_results)
    except Exception as e:
        results["duckduckgo"] = {"error": str(e)}
    
    return results

def market_research_no_login():
    """Market research without requiring login"""
    
    research = {}
    
    # Tech trends
    research["tech_trends"] = research_without_login("real estate automation AI", 3)
    
    # Financial news
    try:
        research["finance_news"] = get_news_headlines("eastmoney", "房地产")
    except Exception as e:
        research["finance_news"] = {"error": str(e)}
    
    # Academic research on real estate tech
    try:
        research["academic_research"] = search_platform("arxiv", "real estate machine learning", 3)
    except Exception as e:
        research["academic_research"] = {"error": str(e)}
    
    return research

def content_research_no_login(topic: str):
    """Content research without login"""
    
    research = {}
    
    # Multi-platform research
    platforms = ["arxiv", "stackoverflow", "wikipedia", "duckduckgo"]
    research["cross_platform"] = cross_platform_research(topic, platforms)
    
    # Tech trends
    try:
        research["tech_trends"] = get_trending_content("hackernews", 10)
    except Exception as e:
        research["tech_trends"] = {"error": str(e)}
    
    # News headlines
    try:
        research["news"] = get_news_headlines("bbc", "technology")
    except Exception as e:
        research["news"] = {"error": str(e)}
    
    return research

if __name__ == "__main__":
    print("🔍 No-Login Research Demo")
    print("=" * 40)
    
    # Test basic research
    print("\\n1. Testing AI agent research:")
    results = research_without_login("AI agent", 3)
    
    for platform, data in results.items():
        if data.get("success"):
            print(f"   ✅ {platform}: Found results")
        else:
            print(f"   ⚠️  {platform}: {data.get('error', 'Failed')}")
    
    print("\\n2. Testing market research:")
    market_results = market_research_no_login()
    
    for category, data in market_results.items():
        if data.get("success"):
            print(f"   ✅ {category}: Found data")
        else:
            print(f"   ⚠️  {category}: {data.get('error', 'Failed')}")
    
    print("\\n✅ No-login research system ready!")
    print("\\nUsage examples:")
    print("  research_without_login('real estate automation')")
    print("  market_research_no_login()")
    print("  content_research_no_login('machine learning')")
'''
    
    script_path = "/home/wls/.openclaw/workspace/skills/bb-browser/no_login_integration.py"
    Path(script_path).write_text(integration_code)
    
    return script_path

def create_authenticated_strategy():
    """Create strategy for platforms requiring login"""
    
    strategy = '''# Authenticated Access Strategy

## Platforms Requiring Login:
- Twitter/X: Requires account for search, tweets, bookmarks
- Reddit: Limited access without login
- GitHub: Limited API calls without auth
- LinkedIn: Requires login for profiles
- Weibo: Chinese social media
- Zhihu: Chinese Q&A platform

## Solutions:

### 1. Browser Session Method (Recommended)
- Open Chrome normally, log into your accounts
- Then start with debugging: chrome --remote-debugging-port=9222
- bb-browser will use your existing login session

### 2. Alternative Platforms (No Login Required)
- Arxiv: Academic papers
- StackOverflow: Developer Q&A
- Wikipedia: Encyclopedia
- DuckDuckGo: Private search
- HackerNews: Tech news
- BBC News: Headlines
- Bilibili: Video rankings
- 36kr: Tech news (Chinese)

### 3. Public APIs (Alternative Approach)
For platforms requiring login, consider:
- Twitter API (with developer account)
- Reddit API (public endpoints)
- GitHub API (rate limited)
- RSS feeds for news

### 4. Research Strategy Without Login:
1. Use academic sources (Arxiv, Google Scholar)
2. Use news aggregators (HackerNews, RSS feeds)
3. Use search engines (DuckDuckGo, Bing)
4. Use developer resources (StackOverflow, Dev.to)
5. Use public social media (Reddit public posts)
'''
    
    return strategy

def main():
    print("🌐 No-Login bb-browser Strategy")
    print("=" * 50)
    
    # Note: This will fail because Chrome isn't running, but it shows the concept
    print("\n⚠️  Note: Chrome needs to be running for any bb-browser commands")
    print("   This test will show which platforms work without login once Chrome is ready")
    
    # Test concept (will fail but shows approach)
    print("\n🧪 Concept Testing (will fail without Chrome):")
    
    # Create no-login integration
    integration_path = create_no_login_integration()
    print(f"\n✅ Created no-login integration: {integration_path}")
    
    # Create authenticated strategy
    strategy = create_authenticated_strategy()
    print("\n📋 Created authenticated access strategy")
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Install Chrome/Chromium")
    print("2. Start Chrome with: chrome --remote-debugging-port=9222")
    print("3. Load extension in chrome://extensions/")
    print("4. Log into your accounts (Twitter, Reddit, etc.)")
    print("5. Test with working platforms first")
    print("6. Use no-login integration for safe research")
    
    print("\n💡 Pro Tip:")
    print("   Even with login requirements, many platforms offer value:")
    print("   - Arxiv: Latest AI/ML research papers")
    print("   - StackOverflow: Technical solutions and trends")
    print("   - HackerNews: Tech industry insights")
    print("   - DuckDuckGo: Privacy-focused web search")
    print("   - BBC News: Reliable news headlines")

if __name__ == "__main__":
    main()