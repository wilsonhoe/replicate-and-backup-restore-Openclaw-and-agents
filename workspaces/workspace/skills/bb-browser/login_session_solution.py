#!/usr/bin/env python3
"""
bb-browser Login Session Solution
Solves the Chrome profile login issue for bb-browser
"""

import subprocess
import json
import time
from pathlib import Path

def test_current_setup():
    """Test what's working right now"""
    
    print("🧪 Testing Current Chrome Setup")
    print("=" * 50)
    
    # Test platforms that should work without login
    no_login_tests = [
        ("Arxiv", ["site", "arxiv/search", "artificial intelligence", "2"]),
        ("StackOverflow", ["site", "stackoverflow/search", "python", "2"]),
        ("HackerNews", ["site", "hackernews/top", "5"]),
        ("BBC News", ["site", "bbc/news", "3"]),
        ("DuckDuckGo", ["site", "duckduckgo/search", "machine learning", "2"]),
    ]
    
    working_platforms = []
    
    for name, cmd_args in no_login_tests:
        print(f"\nTesting {name}...")
        
        try:
            cmd = ["bb-browser"] + cmd_args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()
                if len(output) > 100:
                    output = output[:100] + "..."
                print(f"  ✅ {name}: Working")
                print(f"     Sample: {output[:50]}...")
                working_platforms.append(name)
            else:
                error = result.stderr.strip()
                if "login" in error.lower() or "auth" in error.lower():
                    print(f"  🔒 {name}: Requires login")
                elif "Could not start browser" in error:
                    print(f"  ⚠️  {name}: Chrome not accessible")
                else:
                    print(f"  ❌ {name}: {error[:50]}...")
                    
        except subprocess.TimeoutExpired:
            print(f"  ⏰ {name}: Timeout")
        except Exception as e:
            print(f"  💥 {name}: {str(e)}")
    
    return working_platforms

def show_login_strategy():
    """Show the correct login strategy"""
    
    print("\n🔑 Login Session Strategy")
    print("=" * 50)
    
    print("\n🎯 The Problem:")
    print("   Chrome with --user-data-dir creates a NEW empty profile")
    print("   Your existing logins are in your DEFAULT Chrome profile")
    
    print("\n✅ The Solution:")
    print("   1. Use your EXISTING Chrome profile (not a new one)")
    print("   2. Log into accounts in your NORMAL Chrome")
    print("   3. Then start Chrome with debugging (preserving logins)")
    
    print("\n📋 Step-by-Step Process:")
    print("   1. Close all Chrome processes: pkill chrome")
    print("   2. Start Chrome normally: chromium-browser")
    print("   3. Log into your accounts in this Chrome window")
    print("   4. Keep Chrome open, then start debugging in SAME session")
    print("   5. Test bb-browser commands")

def create_smart_startup_script():
    """Create a smart startup script that preserves logins"""
    
    script_content = '''#!/bin/bash
# Smart Chrome startup for bb-browser with login preservation

echo "🚀 Smart Chrome Startup for bb-browser"
echo "======================================"

# Kill existing Chrome processes
echo "1. Stopping existing Chrome processes..."
pkill chrome 2>/dev/null
pkill chromium 2>/dev/null
sleep 2

# Find Chrome executable
if command -v chromium-browser &> /dev/null; then
    CHROME_CMD="chromium-browser"
elif command -v google-chrome &> /dev/null; then
    CHROME_CMD="google-chrome"
elif command -v chromium &> /dev/null; then
    CHROME_CMD="chromium"
else
    echo "❌ No Chrome/Chromium found!"
    exit 1
fi

echo "2. Using Chrome: $CHROME_CMD"

# Method 1: Use existing profile (recommended)
echo "3. Starting Chrome with existing profile..."
echo "   Open your accounts in this Chrome window, then press Ctrl+C to continue..."

# Start Chrome normally first
$CHROME_CMD &
CHROME_PID=$!
echo "   Chrome PID: $CHROME_PID"
echo ""
echo "   📝 NOW: Log into your accounts (Twitter, Reddit, LinkedIn, etc.)"
echo "   📝 When done logging in, press Ctrl+C to continue..."
echo ""

# Wait for user to log in
wait $CHROME_PID

echo ""
echo "4. Restarting Chrome with debugging port..."

# Now restart with debugging, preserving the profile
$CHROME_CMD --remote-debugging-port=9222 &
NEW_PID=$!

echo "   Chrome with debugging PID: $NEW_PID"
echo "   Debugging port: 9222"
echo ""
echo "✅ Chrome is ready for bb-browser!"
echo ""
echo "Test commands:"
echo "  bb-browser site twitter/search 'AI agent' 5"
echo "  bb-browser site reddit/hot 10"
echo "  bb-browser site arxiv/search 'machine learning' 3"
'''
    
    script_path = "/home/wls/.openclaw/workspace/skills/bb-browser/smart_startup.sh"
    Path(script_path).write_text(script_content)
    
    import os
    os.chmod(script_path, 0o755)
    
    return script_path

def create_test_suite():
    """Create comprehensive test suite for bb-browser"""
    
    test_script = '''#!/usr/bin/env python3
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
        print(f"\\n🧪 Testing {name}...")
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
                lines = output.split('\\n')
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
    
    print(f"\\n📊 Test Results:")
    print(f"   ✅ Working: {working_count}")
    print(f"   🔒 Login Required: {login_required_count}")
    print(f"   ❌ Failed: {failed_count}")
    
    return results

def show_business_applications():
    """Show business applications based on working platforms"""
    
    print("\\n💼 Business Applications")
    print("=" * 60)
    
    print("\\n🎯 Real Estate Market Research:")
    print("   • Arxiv: Research property tech and AI applications")
    print("   • StackOverflow: Find technical solutions for automation")
    print("   • HackerNews: Track proptech trends and startups")
    print("   • BBC News: Monitor economic and market news")
    print("   • DuckDuckGo: Private research on competitors and trends")
    
    print("\\n📈 Investment Research:")
    print("   • Xueqiu: Hot stocks and market sentiment (Chinese)")
    print("   • HackerNews: Tech investment trends")
    print("   • BBC News: Economic indicators and market news")
    print("   • Arxiv: Academic research on financial AI/ML")
    
    print("\\n🤖 AI/Technology Research:")
    print("   • Arxiv: Latest AI research papers")
    print("   • StackOverflow: Technical implementation guides")
    print("   • HackerNews: AI industry trends and discussions")
    print("   • Wikipedia: Comprehensive background knowledge")

if __name__ == "__main__":
    # Run comprehensive test
    results = comprehensive_test()
    
    # Show business applications
    show_business_applications()
    
    print("\\n✅ Test suite complete!")
    print("\\nNext steps:")
    print("1. For login-required platforms, log into accounts in Chrome")
    print("2. Use working platforms for immediate research")
    print("3. Set up automated research workflows")
'''
    
    script_path = "/home/wls/.openclaw/workspace/skills/bb-browser/comprehensive_test.py"
    Path(script_path).write_text(test_script)
    
    import os
    os.chmod(script_path, 0o755)
    
    return script_path

def main():
    print("🌐 bb-browser Login Session Solution")
    print("=" * 60)
    
    # Test current setup
    working_platforms = test_current_setup()
    
    # Show login strategy
    show_login_strategy()
    
    # Create smart startup script
    startup_script = create_smart_startup_script()
    print(f"\n✅ Created smart startup script: {startup_script}")
    
    # Create comprehensive test
    test_script = create_test_suite()
    print(f"✅ Created comprehensive test: {test_script}")
    
    print("\n" + "=" * 60)
    print("🎯 Immediate Action Plan:")
    print(f"1. Run smart startup: bash {startup_script}")
    print("2. Log into your accounts when Chrome opens")
    print("3. Press Ctrl+C when done logging in")
    print("4. Chrome will restart with debugging")
    print("5. Test your command: bb-browser site twitter/search 'AI agent' 5")
    print(f"\n   Or run comprehensive test: python3 {test_script}")
    
    print(f"\n📊 Currently working platforms: {len(working_platforms)}")
    if working_platforms:
        print(f"   {', '.join(working_platforms[:3])}...")

if __name__ == "__main__":
    main()