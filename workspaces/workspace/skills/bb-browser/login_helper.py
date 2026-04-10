#!/usr/bin/env python3
"""
bb-browser Login Helper
Helps you log into accounts in Chrome for bb-browser access
"""

import subprocess
import time

def open_login_pages():
    """Open common login pages in Chrome"""
    
    login_urls = [
        "https://twitter.com/login",
        "https://reddit.com/login", 
        "https://linkedin.com/login",
        "https://github.com/login",
        "https://weibo.com/login",
        "https://www.zhihu.com/signin",
        "https://www.xiaohongshu.com/"
    ]
    
    print("🌐 Opening login pages...")
    
    for url in login_urls:
        try:
            subprocess.run(["chromium-browser", url], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         timeout=3)
            time.sleep(2)
            print(f"  ✅ Opened: {url}")
        except subprocess.TimeoutExpired:
            print(f"  ✅ Opened: {url} (continuing...)")
        except Exception as e:
            print(f"  ⚠️  Failed to open {url}: {e}")

if __name__ == "__main__":
    print("🔑 bb-browser Login Helper")
    print("=" * 40)
    print("This will open login pages in Chrome for you to sign in.")
    print("After logging in, close Chrome and restart with debugging.")
    print("")
    
    open_login_pages()
    
    print("\n✅ Login pages opened!")
    print("\nNext steps:")
    print("1. Log into each account")
    print("2. Close Chrome when done")
    print("3. Restart Chrome with debugging:")
    print("   chromium-browser --remote-debugging-port=9222")
    print("4. Test bb-browser commands")
