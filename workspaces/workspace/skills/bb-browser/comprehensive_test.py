#!/usr/bin/env python3
"""
Comprehensive bb-browser Test Suite
Tests platforms with and without login requirements
"""

import subprocess
import json
import time

def run_test(name, command, timeout=15):
    """Run a single test command"""
    try:
        print(f"\n🧪 Testing {name}...")
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()
            # Try to parse as JSON if possible
            try:
                data = json.loads(output)
                if isinstance(data, list):
                    print(f"   ✅ {name}: Found {len(data)} results")
                elif isinstance(data, dict):
                    print(f"   ✅ {name}: Found data")
                else:
                    print(f"   ✅ {name}: Success")
                return {"status": "success", "data": data}
            except:
                # Not JSON, treat as text
                lines = output.split('\n')
                print(f"   ✅ {name}: Found {len(lines)} lines of data")
                return {"status": "success", "text": output}
        else:
            error = result.stderr.strip()
            if "login" in error.lower():
                print(f"   🔒 {name}: Requires login")
                return {"status": "login_required", "error": error}
            elif "Could not start browser" in error:
                print(f"   ⚠️  {name}: Chrome not accessible")
                return {"status": "chrome_error", "error": error}
            else:
                print(f"   ❌ {name}: {error[:50]}...")
                return {"status": "failed", "error": error}
                
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {name}: Timeout")
        return {"status": "timeout", "error": "Command timed out"}
    except Exception as e:
        print(f"   💥 {name}: {str(e)}")
        return {"status": "error", "error": str(e)}

def comprehensive_test():
    """Run comprehensive test suite"""
    
    print("🌐 Comprehensive bb-browser Test Suite")
    print("=" * 60)
    
    tests = [
        # No login required (should work)
        ("Arxiv Papers", ["bb-browser", "site", "arxiv/search", "artificial intelligence", "2"]),
        ("StackOverflow", ["bb-browser", "site", "stackoverflow/search", "python", "2"]),
        ("HackerNews", ["bb-browser", "site", "hackernews/top", "5"]),
        ("BBC News", ["bb-browser", "site", "bbc/news", "3"]),
        ("DuckDuckGo", ["bb-browser", "site", "duckduckgo/search", "machine learning", "2"]),
        ("Wikipedia", ["bb-browser", "site", "wikipedia/search", "neural networks", "2"]),
        
        # May require login (platform dependent)
        ("Twitter", ["bb-browser", "site", "twitter/search", "AI agent", "3"]),
        ("Reddit", ["bb-browser", "site", "reddit/hot", "5"]),
        ("GitHub", ["bb-browser", "site", "github/repo", "microsoft/vscode"]),
        
        # Chinese platforms
        ("Bilibili", ["bb-browser", "site", "bilibili/ranking", "5"]),
        ("36kr News", ["bb-browser", "site", "36kr/newsflash"]),
        
        # Finance
        ("Xueqiu Stocks", ["bb-browser", "site", "xueqiu/hot-stock", "10"]),
    ]
    
    results = {}
    working_count = 0
    login_required_count = 0
    failed_count = 0
    
    for name, command in tests:
        results[name] = run_test(name, command)
        
        if results[name]["status"] == "success":
            working_count += 1
        elif results[name]["status"] == "login_required":
            login_required_count += 1
        else:
            failed_count += 1
        
        time.sleep(1)  # Rate limiting
    
    print(f"\n📊 Test Results:")
    print(f"   ✅ Working: {working_count}")
    print(f"   🔒 Login Required: {login_required_count}")
    print(f"   ❌ Failed: {failed_count}")
    
    return results

def show_business_applications():
    """Show business applications based on working platforms"""
    
    print("\n💼 Business Applications")
    print("=" * 60)
    
    print("\n🎯 Real Estate Market Research:")
    print("   • Arxiv: Research property tech and AI applications")
    print("   • StackOverflow: Find technical solutions for automation")
    print("   • HackerNews: Track proptech trends and startups")
    print("   • BBC News: Monitor economic and market news")
    print("   • DuckDuckGo: Private research on competitors and trends")
    
    print("\n📈 Investment Research:")
    print("   • Xueqiu: Hot stocks and market sentiment (Chinese)")
    print("   • HackerNews: Tech investment trends")
    print("   • BBC News: Economic indicators and market news")
    print("   • Arxiv: Academic research on financial AI/ML")
    
    print("\n🤖 AI/Technology Research:")
    print("   • Arxiv: Latest AI research papers")
    print("   • StackOverflow: Technical implementation guides")
    print("   • HackerNews: AI industry trends and discussions")
    print("   • Wikipedia: Comprehensive background knowledge")

if __name__ == "__main__":
    # Run comprehensive test
    results = comprehensive_test()
    
    # Show business applications
    show_business_applications()
    
    print("\n✅ Test suite complete!")
    print("\nNext steps:")
    print("1. For login-required platforms, log into accounts in Chrome")
    print("2. Use working platforms for immediate research")
    print("3. Set up automated research workflows")
