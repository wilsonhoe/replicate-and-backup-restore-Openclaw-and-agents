#!/usr/bin/env python3
"""
bb-browser Setup and Configuration Helper for OpenClaw
Helps install Chrome and configure bb-browser for optimal use
"""

import subprocess
import json
import sys
import os
from pathlib import Path

def check_chrome_installation():
    """Check if Chrome/Chromium is installed"""
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable", 
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium"
    ]
    
    for path in chrome_paths:
        if Path(path).exists():
            return path
    
    return None

def install_chrome():
    """Install Google Chrome"""
    print("🔧 Installing Google Chrome...")
    
    try:
        # Detect package manager
        if Path("/usr/bin/apt").exists():
            # Ubuntu/Debian
            commands = [
                ["wget", "-q", "-O", "/tmp/google-chrome.deb", 
                 "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"],
                ["sudo", "apt", "install", "-y", "/tmp/google-chrome.deb"]
            ]
        elif Path("/usr/bin/yum").exists():
            # CentOS/RHEL/Fedora
            commands = [
                ["sudo", "yum", "install", "-y", "wget"],
                ["wget", "-q", "-O", "/tmp/google-chrome.rpm",
                 "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm"],
                ["sudo", "yum", "install", "-y", "/tmp/google-chrome.rpm"]
            ]
        elif Path("/usr/bin/dnf").exists():
            # Fedora
            commands = [
                ["sudo", "dnf", "install", "-y", "wget"],
                ["wget", "-q", "-O", "/tmp/google-chrome.rpm",
                 "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm"],
                ["sudo", "dnf", "install", "-y", "/tmp/google-chrome.rpm"]
            ]
        else:
            return {"error": "Unsupported package manager. Please install Chrome manually.", "success": False}
        
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return {"error": f"Command failed: {' '.join(cmd)}\n{result.stderr}", "success": False}
        
        return {"success": True, "message": "Chrome installed successfully"}
        
    except Exception as e:
        return {"error": f"Installation error: {str(e)}", "success": False}

def setup_bb_browser_extension():
    """Guide user through extension setup"""
    extension_path = "/home/wls/Downloads/bb-browser-extension-bb-browser-v0.10.0"
    
    if not Path(extension_path).exists():
        return {"error": f"Extension not found at {extension_path}", "success": False}
    
    print("📋 Extension Setup Instructions:")
    print("1. Open Chrome and navigate to: chrome://extensions/")
    print("2. Enable 'Developer mode' (toggle in top right)")
    print("3. Click 'Load unpacked'")
    print(f"4. Select folder: {extension_path}")
    print("5. Extension should appear with 'bb-browser' name")
    
    return {"success": True, "message": "Extension setup instructions provided", "path": extension_path}

def start_chrome_with_debugging():
    """Start Chrome with remote debugging enabled"""
    chrome_path = check_chrome_installation()
    if not chrome_path:
        return {"error": "Chrome not found. Please install Chrome first.", "success": False}
    
    print(f"🚀 Starting Chrome with debugging on port 9222...")
    print(f"Using Chrome at: {chrome_path}")
    
    # Try to start Chrome with debugging
    try:
        # Kill any existing Chrome processes
        subprocess.run(["pkill", "chrome"], capture_output=True)
        
        # Start Chrome with debugging
        cmd = [chrome_path, "--remote-debugging-port=9222", "--user-data-dir=/tmp/chrome-profile"]
        
        # Start in background
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait a moment for Chrome to start
        import time
        time.sleep(3)
        
        # Check if Chrome is running on port 9222
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 9222))
        sock.close()
        
        if result == 0:
            return {"success": True, "message": "Chrome started with debugging on port 9222", "pid": process.pid}
        else:
            return {"error": "Chrome may not be listening on port 9222", "success": False}
            
    except Exception as e:
        return {"error": f"Failed to start Chrome: {str(e)}", "success": False}

def test_bb_browser_connection():
    """Test bb-browser connection"""
    print("🧪 Testing bb-browser connection...")
    
    try:
        # Test basic functionality
        result = subprocess.run(["bb-browser", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return {"error": "bb-browser not working", "success": False}
        
        # Test site list
        result = subprocess.run(["bb-browser", "site", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return {"error": f"bb-browser site list failed: {result.stderr}", "success": False}
        
        # Count available sites
        sites = result.stdout.strip().split('\n')
        site_count = len([s for s in sites if '/' in s])
        
        return {"success": True, "message": f"bb-browser working with {site_count} site adapters", "version": result.stdout.strip()[:50]}
        
    except subprocess.TimeoutExpired:
        return {"error": "bb-browser command timed out", "success": False}
    except Exception as e:
        return {"error": f"Test error: {str(e)}", "success": False}

def create_chrome_desktop_entry():
    """Create a desktop entry for Chrome with debugging"""
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=Chrome (Debug Mode)
Comment=Google Chrome with remote debugging for bb-browser
Exec=/usr/bin/google-chrome-stable --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile %U
Icon=google-chrome
Terminal=false
Categories=Network;WebBrowser;
"""
    
    desktop_path = Path.home() / ".local" / "share" / "applications" / "chrome-debug.desktop"
    
    try:
        desktop_path.parent.mkdir(parents=True, exist_ok=True)
        desktop_path.write_text(desktop_content)
        
        # Make executable
        os.chmod(desktop_path, 0o755)
        
        return {"success": True, "message": f"Desktop entry created: {desktop_path}"}
    except Exception as e:
        return {"error": f"Failed to create desktop entry: {str(e)}", "success": False}

def main():
    """Main setup function"""
    print("🌐 bb-browser Setup Assistant for OpenClaw")
    print("=" * 50)
    
    # Check current status
    print("\n1. Checking Chrome installation:")
    chrome_path = check_chrome_installation()
    if chrome_path:
        print(f"   ✅ Chrome found: {chrome_path}")
    else:
        print("   ❌ Chrome not found")
        print("\n2. Installing Chrome:")
        result = install_chrome()
        if result["success"]:
            print(f"   ✅ {result['message']}")
            chrome_path = check_chrome_installation()
        else:
            print(f"   ❌ {result['error']}")
            print("   Please install Chrome manually from: https://www.google.com/chrome/")
            return
    
    # Setup extension
    print("\n3. Setting up browser extension:")
    ext_result = setup_bb_browser_extension()
    if ext_result["success"]:
        print(f"   ✅ {ext_result['message']}")
    else:
        print(f"   ❌ {ext_result['error']}")
    
    # Test bb-browser
    print("\n4. Testing bb-browser:")
    test_result = test_bb_browser_connection()
    if test_result["success"]:
        print(f"   ✅ {test_result['message']}")
    else:
        print(f"   ⚠️  {test_result['error']}")
    
    # Create desktop entry
    print("\n5. Creating desktop entry:")
    desktop_result = create_chrome_desktop_entry()
    if desktop_result["success"]:
        print(f"   ✅ {desktop_result['message']}")
    else:
        print(f"   ℹ️  {desktop_result['error']}")
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Start Chrome with debugging: google-chrome --remote-debugging-port=9222")
    print("2. Load the extension in Chrome (see instructions above)")
    print("3. Test with: bb-browser site twitter/search 'AI agent' 5")
    print("4. Use the Python integration in OpenClaw")
    print("\n📚 Full guide: skills/bb-browser/INTEGRATION_GUIDE.md")

if __name__ == "__main__":
    main()