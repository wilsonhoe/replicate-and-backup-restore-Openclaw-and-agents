#!/usr/bin/env python3
"""
Chrome Profile Solutions for bb-browser
Fixes login session issues with Chrome debugging
"""

import subprocess
import os
import shutil
from pathlib import Path

def find_chrome_profiles():
    """Find all Chrome profiles on the system"""
    profiles = []
    
    # Common Chrome profile locations
    profile_paths = [
        Path.home() / ".config/google-chrome",
        Path.home() / ".config/chromium", 
        Path.home() / "snap/chromium/common/.config/chromium",
        Path("/tmp/chrome-profile")
    ]
    
    print("🔍 Searching for Chrome profiles...")
    
    for path in profile_paths:
        if path.exists():
            print(f"\n📁 Found profile directory: {path}")
            
            # Look for profile folders
            for item in path.iterdir():
                if item.is_dir() and (item / "Preferences").exists():
                    print(f"  ✅ Profile: {item.name}")
                    profiles.append(item)
    
    return profiles

def create_profile_backup():
    """Create a backup of current Chrome profile"""
    source = Path.home() / ".config/google-chrome"
    backup = Path.home() / ".config/google-chrome-backup"
    
    if source.exists():
        print(f"\n💾 Creating backup of Chrome profile...")
        try:
            if backup.exists():
                shutil.rmtree(backup)
            shutil.copytree(source, backup)
            print(f"  ✅ Backup created: {backup}")
            return backup
        except Exception as e:
            print(f"  ⚠️  Backup failed: {e}")
            return None
    return None

def start_chrome_with_existing_profile():
    """Start Chrome with existing profile and debugging"""
    
    print("\n🚀 Starting Chrome with existing profile...")
    
    # Method 1: Use default profile directory
    default_profile = Path.home() / ".config/google-chrome"
    
    if default_profile.exists():
        print(f"  Using profile: {default_profile}")
        
        # Kill existing Chrome processes
        subprocess.run(["pkill", "chrome"], capture_output=True)
        time.sleep(2)
        
        # Start with existing profile
        cmd = [
            "chromium-browser" if shutil.which("chromium-browser") else "google-chrome",
            f"--user-data-dir={default_profile}",
            "--remote-debugging-port=9222",
            "--no-first-run",
            "--no-default-browser-check"
        ]
        
        print(f"  Command: {' '.join(cmd)}")
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ Chrome started with PID: {process.pid}")
            return process.pid
        except Exception as e:
            print(f"  ❌ Failed to start Chrome: {e}")
            return None
    else:
        print("  ❌ No existing Chrome profile found")
        return None

def create_persistent_profile():
    """Create a persistent profile for bb-browser"""
    
    persistent_profile = Path.home() / ".bb-browser-profile"
    
    print(f"\n🏗️  Creating persistent profile: {persistent_profile}")
    
    try:
        # Create directory
        persistent_profile.mkdir(exist_ok=True)
        
        # Copy Chrome's default preferences if they exist
        default_prefs = Path.home() / ".config/google-chrome/Default/Preferences"
        if default_prefs.exists():
            (persistent_profile / "Default").mkdir(exist_ok=True)
            shutil.copy2(default_prefs, persistent_profile / "Default/Preferences")
            print("  ✅ Copied Chrome preferences")
        
        return persistent_profile
        
    except Exception as e:
        print(f"  ⚠️  Failed to create persistent profile: {e}")
        return None

def test_profile_access():
    """Test if Chrome profile can be accessed"""
    
    print("\n🧪 Testing profile access...")
    
    # Test commands
    test_commands = [
        ["bb-browser", "--version"],
        ["bb-browser", "site", "list"],
        ["bb-browser", "site", "arxiv/search", "test", "1"]
    ]
    
    for cmd in test_commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"  ✅ {' '.join(cmd[:3])}: Working")
            else:
                error = result.stderr.strip()
                if "Could not start browser" in error:
                    print(f"  ⚠️  {' '.join(cmd[:3])}: Chrome not accessible")
                else:
                    print(f"  ❌ {' '.join(cmd[:3])}: {error[:100]}")
        except Exception as e:
            print(f"  💥 {' '.join(cmd[:3])}: {str(e)}")

def show_chrome_startup_options():
    """Show different ways to start Chrome with debugging"""
    
    print("\n🚀 Chrome Startup Options")
    print("=" * 50)
    
    print("\n1. Use existing profile (recommended):")
    print("   chromium-browser --remote-debugging-port=9222")
    print("   # or")
    print("   google-chrome --remote-debugging-port=9222")
    
    print("\n2. Specify custom profile directory:")
    print("   chromium-browser --user-data-dir=/home/$USER/.config/google-chrome --remote-debugging-port=9222")
    
    print("\n3. Create new persistent profile:")
    print("   mkdir -p ~/.bb-browser-profile")
    print("   chromium-browser --user-data-dir=~/.bb-browser-profile --remote-debugging-port=9222")
    
    print("\n4. Copy existing profile to new location:")
    print("   cp -r ~/.config/google-chrome ~/.bb-browser-profile")
    print("   chromium-browser --user-data-dir=~/.bb-browser-profile --remote-debugging-port=9222")

def create_login_helper():
    """Create a helper script for logging into accounts"""
    
    helper_script = '''#!/usr/bin/env python3
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
    
    print("\\n✅ Login pages opened!")
    print("\\nNext steps:")
    print("1. Log into each account")
    print("2. Close Chrome when done")
    print("3. Restart Chrome with debugging:")
    print("   chromium-browser --remote-debugging-port=9222")
    print("4. Test bb-browser commands")
'''
    
    script_path = "/home/wls/.openclaw/workspace/skills/bb-browser/login_helper.py"
    Path(script_path).write_text(helper_script)
    
    import os
    os.chmod(script_path, 0o755)
    
    return script_path

def main():
    print("🔧 Chrome Profile Solutions for bb-browser")
    print("=" * 60)
    
    # Find existing profiles
    profiles = find_chrome_profiles()
    
    if not profiles:
        print("\n⚠️  No existing Chrome profiles found")
        print("   Creating new persistent profile...")
        
        # Create persistent profile
        persistent_profile = create_persistent_profile()
        if persistent_profile:
            print(f"   ✅ Created: {persistent_profile}")
            print(f"   Start Chrome with: chromium-browser --user-data-dir={persistent_profile} --remote-debugging-port=9222")
    
    # Show startup options
    show_chrome_startup_options()
    
    # Create login helper
    login_helper = create_login_helper()
    print(f"\n✅ Created login helper: {login_helper}")
    
    # Test current setup
    test_profile_access()
    
    print("\n" + "=" * 60)
    print("🎯 Recommended Solution:")
    print("1. Kill current Chrome: pkill chrome")
    print("2. Start Chrome normally: chromium-browser")
    print("3. Log into your accounts")
    print("4. Close and restart with debugging: chromium-browser --remote-debugging-port=9222")
    print("5. Test: bb-browser site twitter/search 'AI agent' 5")
    
    print("\n💡 Alternative: Use login helper:")
    print(f"   python3 {login_helper}")

if __name__ == "__main__":
    import time
    main()