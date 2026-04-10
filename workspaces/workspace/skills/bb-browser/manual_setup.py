#!/usr/bin/env python3
"""
bb-browser Manual Setup Guide for OpenClaw
Since Chrome isn't installed, this provides alternative approaches
"""

import subprocess
import json
import sys
from pathlib import Path

def show_installation_options():
    """Show different ways to install Chrome/Chromium"""
    print("🌐 Chrome Installation Options for bb-browser")
    print("=" * 60)
    
    print("\n📦 Option 1: Install Google Chrome (Recommended)")
    print("   Download from: https://www.google.com/chrome/")
    print("   Or install via package manager:")
    print("   Ubuntu/Debian: wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -")
    print("                  sudo sh -c 'echo \"deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main\" >> /etc/apt/sources.list.d/google.list'")
    print("                  sudo apt update && sudo apt install google-chrome-stable")
    
    print("\n📦 Option 2: Install Chromium (Open Source)")
    print("   Ubuntu/Debian: sudo apt install chromium-browser")
    print("   Fedora: sudo dnf install chromium")
    print("   Arch: sudo pacman -S chromium")
    
    print("\n📦 Option 3: Use Snap Package")
    print("   sudo snap install chromium")
    print("   sudo snap install chromium --edge  # For latest version")
    
    print("\n📦 Option 4: Portable Chrome")
    print("   Download portable version from: https://portableapps.com/apps/internet/google_chrome_portable")
    print("   Extract and run with debugging flags")

def show_chrome_startup_commands():
    """Show different ways to start Chrome with debugging"""
    print("\n🚀 Chrome Startup Commands")
    print("=" * 60)
    
    print("\n# Basic debugging setup:")
    print("google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile")
    
    print("\n# With additional options for better compatibility:")
    print("google-chrome --remote-debugging-port=9222 \\")
    print("              --user-data-dir=/tmp/chrome-profile \\")
    print("              --no-first-run \\")
    print("              --no-default-browser-check \\")
    print("              --disable-blink-features=AutomationControlled")
    
    print("\n# For headless operation (if needed):")
    print("google-chrome --remote-debugging-port=9222 \\")
    print("              --user-data-dir=/tmp/chrome-profile \\")
    print("              --headless \\")
    print("              --disable-gpu")
    
    print("\n# Background process:")
    print("nohup google-chrome --remote-debugging-port=9222 \\")
    print("                   --user-data-dir=/tmp/chrome-profile \\")
    print("                   > /tmp/chrome.log 2>&1 &")

def show_extension_setup():
    """Show detailed extension setup steps"""
    print("\n🔌 Extension Setup Steps")
    print("=" * 60)
    
    extension_path = "/home/wls/Downloads/bb-browser-extension-bb-browser-v0.10.0"
    
    print(f"\n1. Extension Location: {extension_path}")
    print("   Files present:")
    
    # Check extension files
    ext_files = ["manifest.json", "background.js", "options.js", "content/trace.js"]
    for file in ext_files:
        file_path = Path(extension_path) / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   ❌ {file} (missing)")
    
    print("\n2. Installation Steps:")
    print("   a) Open Chrome/Chromium")
    print("   b) Navigate to: chrome://extensions/")
    print("   c) Toggle 'Developer mode' ON (top right)")
    print("   d) Click 'Load unpacked'")
    print(f"   e) Select folder: {extension_path}")
    print("   f) Extension should appear as 'bb-browser' with version 0.10.0")
    
    print("\n3. Verification:")
    print("   - Extension should show as 'Enabled'")
    print("   - No error messages should appear")
    print("   - Extension icon may appear in toolbar")

def show_troubleshooting_guide():
    """Show troubleshooting steps"""
    print("\n🔧 Troubleshooting Guide")
    print("=" * 60)
    
    print("\n❌ 'Could not start browser' error:")
    print("   → Chrome not running with debugging port")
    print("   → Solution: Start Chrome with --remote-debugging-port=9222")
    
    print("\n❌ 'Extension not loaded' error:")
    print("   → Extension not properly installed")
    print("   → Solution: Re-install extension following steps above")
    
    print("\n❌ 'Command not found' error:")
    print("   → bb-browser not installed or not in PATH")
    print("   → Solution: npm install -g bb-browser")
    
    print("\n❌ 'Permission denied' errors:")
    print("   → Extension permissions issues")
    print("   → Solution: Check extension permissions in chrome://extensions/")

def create_workaround_script():
    """Create a workaround script for testing without full Chrome setup"""
    print("\n🛠️ Testing Workaround Script")
    print("=" * 60)
    
    workaround_script = """#!/usr/bin/env python3
\"\"\"
bb-browser Testing Workaround
Tests basic functionality without requiring Chrome debugging
\"\"\"

import subprocess
import json

def test_site_list():
    \"\"\"Test getting site list\"\"\"
    try:
        result = subprocess.run([\"bb-browser\", \"site\", \"list\"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            sites = result.stdout.strip().split('\\n')
            print(f\"✅ Found {len(sites)} available sites/commands\")
            # Show first 5 examples
            for site in sites[:5]:
                print(f\"  • {site}\")
            return True
        else:
            print(f\"❌ Site list failed: {result.stderr}\")
            return False
    except Exception as e:
        print(f\"❌ Error: {e}\")
        return False

def test_version():
    \"\"\"Test bb-browser version\"\"\"
    try:
        result = subprocess.run([\"bb-browser\", \"--version\"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f\"✅ bb-browser version: {result.stdout.strip()}\")
            return True
        else:
            print(f\"❌ Version check failed: {result.stderr}\")
            return False
    except Exception as e:
        print(f\"❌ Error: {e}\")
        return False

def main():
    print(\"🔍 bb-browser Basic Testing (No Chrome Required)\")
    print(\"=\" * 50)
    
    print(\"\\n1. Testing version:\")
    version_ok = test_version()
    
    print(\"\\n2. Testing site list:\")
    sites_ok = test_site_list()
    
    if version_ok and sites_ok:
        print(\"\\n✅ Basic tests passed!\")
        print(\"\\nNext steps:\")
        print(\"1. Install Chrome/Chromium\")
        print(\"2. Start with: chrome --remote-debugging-port=9222\")
        print(\"3. Load extension in chrome://extensions/\")
        print(\"4. Test with: bb-browser site twitter/search 'test' 5\")
    else:
        print(\"\\n❌ Basic tests failed\")
        print(\"Check installation and try again\")

if __name__ == \"__main__\":
    main()
"""
    
    script_path = "/home/wls/.openclaw/workspace/skills/bb-browser/test_basic.py"
    Path(script_path).write_text(workaround_script)
    os.chmod(script_path, 0o755)
    
    print(f"\n✅ Created workaround script: {script_path}")
    print("   Run with: python3 skills/bb-browser/test_basic.py")

def main():
    """Main function"""
    print("🌐 bb-browser Manual Setup Guide")
    print("=" * 60)
    
    show_installation_options()
    show_chrome_startup_commands()
    show_extension_setup()
    show_troubleshooting_guide()
    create_workaround_script()
    
    print("\n" + "=" * 60)
    print("🎯 Summary:")
    print("1. Install Chrome/Chromium using one of the methods above")
    print("2. Start Chrome with debugging port")
    print("3. Install the bb-browser extension")
    print("4. Test with: bb-browser site twitter/search 'AI agent' 5")
    print("5. Use the Python integration in OpenClaw")
    print("\n📚 Full documentation: skills/bb-browser/INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    main()