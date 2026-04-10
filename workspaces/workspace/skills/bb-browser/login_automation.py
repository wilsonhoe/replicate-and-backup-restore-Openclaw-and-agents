#!/usr/bin/env python3
"""
bb-browser Login Automation Helper
Opens login pages in Chrome for you
"""

import webbrowser
import time
import subprocess

def open_login_pages():
    """Open common login pages"""
    
    login_urls = [
        ("Twitter/X", "https://twitter.com/login"),
        ("Reddit", "https://reddit.com/login"),
        ("LinkedIn", "https://linkedin.com/login"),
        ("GitHub", "https://github.com/login"),
        ("HackerNews", "https://news.ycombinator.com/login"),
        ("Arxiv", "https://arxiv.org/login"),
        ("StackOverflow", "https://stackoverflow.com/users/login"),
        ("Weibo", "https://weibo.com/login"),
        ("Zhihu", "https://www.zhihu.com/signin"),
    ]
    
    print("🌐 Opening login pages in Chrome...")
    print("   Please log into each account, then close the tabs.")
    print("")
    
    for name, url in login_urls:
        try:
            print(f"   Opening {name}: {url}")
            webbrowser.open(url)
            time.sleep(3)  # Wait between openings
        except Exception as e:
            print(f"   ⚠️  Could not open {name}: {e}")
    
    print("\n✅ All login pages opened!")
    print("   Please log into each account.")
    print("   When done, test with: bb-browser site twitter/search 'AI agent' 5")

if __name__ == "__main__":
    print("🔑 bb-browser Login Helper")
    print("=" * 40)
    open_login_pages()
