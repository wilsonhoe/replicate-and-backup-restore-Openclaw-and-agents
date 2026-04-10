#!/usr/bin/env python3
"""
OpenClaw Bridge for Claw-Code Integration
Connects OpenClaw agents to enhanced execution with permissions and cost tracking
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Import the integration module
from claw_integration import (
    get_integration,
    track_execution,
    check_tool_permission,
    elevate_permissions,
    get_session_costs,
    get_permissions_report,
    register_lisa_nyx_kael
)


class OpenClawAgentBridge:
    """
    Bridge between OpenClaw agent execution and claw-code enhanced features.
    This wraps agent actions with permission checks and cost tracking.
    """

    def __init__(self):
        self.integration = get_integration()
        self._ensure_agents_registered()

    def _ensure_agents_registered(self):
        """Ensure Lisa, Nyx, Kael are registered"""
        if not self.integration.agents:
            register_lisa_nyx_kael()

    def before_tool_execution(self, agent_id: str, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pre-execution hook: Check permissions before allowing tool use
        Returns: {"allowed": bool, "reason": str}
        """
        allowed = check_tool_permission(agent_id, tool_name)

        if not allowed:
            current_perm = self.integration.agents.get(agent_id, {}).get("permissions", "unknown")
            return {
                "allowed": False,
                "reason": f"Agent '{agent_id}' (mode: {current_perm}) cannot use '{tool_name}'. "
                          f"Requires elevation. Use elevate_permissions('{agent_id}', 'reason') to grant access."
            }

        return {"allowed": True, "reason": "Permission granted"}

    def after_tool_execution(self, agent_id: str, tool_name: str, result: Any, tokens_used: int = 0):
        """
        Post-execution hook: Track cost and log execution
        """
        # Estimate tokens if not provided
        if tokens_used == 0:
            tokens_used = len(str(result)) // 4  # Rough estimate

        track_execution(
            agent_name=agent_id,
            task=f"{tool_name} execution",
            estimated_tokens=tokens_used
        )

    def wrap_agent_execution(self, agent_id: str, task: str, execute_func, *args, **kwargs) -> Any:
        """
        Wrapper for agent task execution with full tracking
        Usage: result = bridge.wrap_agent_execution("lisa", "Research task", actual_function, arg1, arg2)
        """
        # Pre-execution tracking
        execution_result = track_execution(agent_id, task, estimated_tokens=1000)

        if not execution_result["success"]:
            return {
                "error": execution_result["error"],
                "blocked": True
            }

        try:
            # Execute the actual function
            result = execute_func(*args, **kwargs)

            # Post-execution tracking
            self.after_tool_execution(agent_id, task, result)

            return {
                "success": True,
                "result": result,
                "cost_units": execution_result["cost_units"],
                "execution_id": execution_result["execution_id"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_id": execution_result.get("execution_id")
            }

    def get_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        costs = get_session_costs()
        return {
            "claw_code_available": True,
            "agents_registered": list(self.integration.agents.keys()),
            "total_executions": costs["executions"],
            "total_tokens": costs["total_tokens"],
            "session_costs": costs
        }


# Singleton bridge instance
_bridge: Optional[OpenClawAgentBridge] = None


def get_bridge() -> OpenClawAgentBridge:
    """Get or create the bridge instance"""
    global _bridge
    if _bridge is None:
        _bridge = OpenClawAgentBridge()
    return _bridge


# Convenience functions for direct use in OpenClaw

def check_before_tool(agent_id: str, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
    """Check permission before tool execution"""
    return get_bridge().before_tool_execution(agent_id, tool_name, tool_input)


def track_after_tool(agent_id: str, tool_name: str, result: Any, tokens_used: int = 0):
    """Track execution after tool use"""
    get_bridge().after_tool_execution(agent_id, tool_name, result, tokens_used)


def get_integration_status() -> Dict[str, Any]:
    """Get full integration status"""
    return get_bridge().get_status()


def wrap_task(agent_id: str, task: str, func, *args, **kwargs):
    """Wrap any function with tracking"""
    return get_bridge().wrap_agent_execution(agent_id, task, func, *args, **kwargs)


# Command-line interface for OpenClaw
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw Claw-Code Bridge")
    parser.add_argument("command", choices=["status", "costs", "permissions", "check"])
    parser.add_argument("--agent", "-a", help="Agent ID")
    parser.add_argument("--tool", "-t", help="Tool name to check")

    args = parser.parse_args()

    if args.command == "status":
        status = get_integration_status()
        print(json.dumps(status, indent=2))

    elif args.command == "costs":
        costs = get_session_costs()
        print(json.dumps(costs, indent=2))

    elif args.command == "permissions":
        print(get_permissions_report())

    elif args.command == "check":
        if not args.agent or not args.tool:
            print("Usage: --check --agent lisa --tool Bash")
            sys.exit(1)
        result = check_before_tool(args.agent, args.tool, {})
        print(json.dumps(result, indent=2))
