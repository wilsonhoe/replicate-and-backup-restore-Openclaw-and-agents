#!/usr/bin/env python3
"""
bb-browser Testing Workaround
Tests basic functionality without requiring Chrome debugging
"""

import subprocess
import json
from pathlib import Path

def test_site_list():
    """Test getting site list"""
    try:
        result = subprocess.run(["bb-browser", "site", "list"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            sites = result.stdout.strip().split('\n')
            print(f"✅ Found {len(sites)} available sites/commands")
            # Show first 5 examples
            for site in sites[:5]:
                print(f"  • {site}")
            return True
        else:
            print(f"❌ Site list failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_version():
    """Test bb-browser version"""
    try:
        result = subprocess.run(["bb-browser", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ bb-browser version: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Version check failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔍 bb-browser Basic Testing (No Chrome Required)")
    print("=" * 50)
    
    print("\n1. Testing version:")
    version_ok = test_version()
    
    print("\n2. Testing site list:")
    sites_ok = test_site_list()
    
    if version_ok and sites_ok:
        print("\n✅ Basic tests passed!")
        print("\nNext steps:")
        print("1. Install Chrome/Chromium")
        print("2. Start with: chrome --remote-debugging-port=9222")
        print("3. Load extension in chrome://extensions/")
        print("4. Test with: bb-browser site twitter/search 'test' 5")
    else:
        print("\n❌ Basic tests failed")
        print("Check installation and try again")

if __name__ == "__main__":
    main()