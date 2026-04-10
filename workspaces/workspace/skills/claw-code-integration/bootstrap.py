#!/usr/bin/env python3
"""
Bootstrap script for OpenClaw + Claw-Code Integration
Run this on OpenClaw startup to initialize enhanced agent execution
"""

import sys
import os

# Ensure claw-code is in path
CLAW_CODE_PATH = "/home/wls/.openclaw/claw-code"
if CLAW_CODE_PATH not in sys.path:
    sys.path.insert(0, CLAW_CODE_PATH)

# Import integration modules
from claw_integration import register_lisa_nyx_kael, get_integration
from openclaw_bridge import get_bridge

def bootstrap():
    """Initialize the claw-code integration for OpenClaw"""
    print("=" * 70)
    print("🦞 OpenClaw + Claw-Code Integration Bootstrap")
    print("=" * 70)

    # Step 1: Register agents
    print("\n1️⃣  Registering agents...")
    integration = register_lisa_nyx_kael()

    # Step 2: Initialize bridge
    print("\n2️⃣  Initializing bridge...")
    bridge = get_bridge()

    # Step 3: Verify claw-code modules
    print("\n3️⃣  Verifying claw-code modules...")
    try:
        from src.tools import get_tools
        from src.commands import get_commands
        from src.permissions import ToolPermissionContext
        from src.cost_tracker import CostTracker
        print("   ✅ All claw-code modules loaded successfully")
    except ImportError as e:
        print(f"   ⚠️  Some modules not available: {e}")

    # Step 4: Show status
    print("\n4️⃣  Integration status:")
    status = bridge.get_status()
    print(f"   Agents registered: {', '.join(status['agents_registered'])}")
    print(f"   Total executions: {status['total_executions']}")
    print(f"   Total tokens tracked: {status['total_tokens']}")

    print("\n" + "=" * 70)
    print("✅ OpenClaw + Claw-Code Integration Ready")
    print("=" * 70)
    print("\nEnhanced features available:")
    print("  • Permission-aware tool execution")
    print("  • Cost tracking per agent")
    print("  • 207 Claude Code mirrored commands")
    print("  • 184 permission-aware tools")
    print("\nTo use in your skill:")
    print("  from claw_integration import track_execution, check_tool_permission")
    print("  from openclaw_bridge import get_bridge, check_before_tool")
    print("=" * 70)

    return True

if __name__ == "__main__":
    try:
        bootstrap()
    except Exception as e:
        print(f"\n❌ Bootstrap failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
