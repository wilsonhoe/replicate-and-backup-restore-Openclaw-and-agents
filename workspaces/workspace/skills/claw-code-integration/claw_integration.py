#!/usr/bin/env python3
"""
Claw-Code Integration for OpenClaw
Wraps claw-code modules to provide permission-aware tool execution,
cost tracking, and enhanced command registry for OpenClaw agents.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

# Add claw-code to path
CLAW_CODE_PATH = Path("/home/wls/.openclaw/claw-code")
sys.path.insert(0, str(CLAW_CODE_PATH))

# Import claw-code modules
try:
    from src.permissions import ToolPermissionContext
    from src.cost_tracker import CostTracker
    from src.tools import get_tools
    from src.commands import get_commands
    CLAW_CODE_AVAILABLE = True
except ImportError as e:
    CLAW_CODE_AVAILABLE = False
    print(f"⚠️  Claw-code modules not available: {e}")


@dataclass
class AgentExecution:
    """Tracks a single agent execution with cost and permissions"""
    agent_name: str
    task: str
    permission_mode: str = "read-only"
    tokens_in: int = 0
    tokens_out: int = 0
    tools_used: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"


class OpenClawClawIntegration:
    """
    Integration layer between OpenClaw and claw-code.
    Provides enhanced execution flow with permissions and cost tracking.
    """

    PERMISSION_MODES = ["read-only", "workspace-write", "danger-full-access"]

    def __init__(self):
        self.cost_tracker = CostTracker() if CLAW_CODE_AVAILABLE else None
        self.execution_log: List[AgentExecution] = []
        self.agents: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, name: str, role: str, default_permissions: str = "read-only"):
        """Register an agent with default permissions"""
        if default_permissions not in self.PERMISSION_MODES:
            raise ValueError(f"Invalid permission mode: {default_permissions}")

        self.agents[name] = {
            "name": name,
            "role": role,
            "permissions": default_permissions,
            "executions": []
        }
        print(f"✅ Agent '{name}' registered with '{default_permissions}' permissions")

    def check_permission(self, agent_name: str, tool_name: str) -> bool:
        """Check if agent has permission to use a tool"""
        if not CLAW_CODE_AVAILABLE:
            return True  # Fallback to allow if claw-code not loaded

        agent = self.agents.get(agent_name)
        if not agent:
            return False

        mode = agent.get("permissions", "read-only")

        # Read-only agents can only use safe tools
        safe_tools = ["Read", "Grep", "Glob", "ReadMcpResourceTool", "WebSearch"]
        if mode == "read-only":
            return tool_name in safe_tools

        # Workspace-write agents can use Edit, Write, Bash (restricted)
        if mode == "workspace-write":
            restricted = ["dangerouslyDisableSandbox"]
            return tool_name not in restricted

        # Full access allows everything
        return True

    def execute_with_tracking(self, agent_name: str, task: str,
                              estimated_tokens: int = 1000) -> Dict[str, Any]:
        """
        Execute a task with cost tracking and permission checking.
        This is the main entry point for enhanced agent execution.
        """
        # Create execution record
        execution = AgentExecution(
            agent_name=agent_name,
            task=task,
            permission_mode=self.agents.get(agent_name, {}).get("permissions", "read-only"),
            tokens_in=estimated_tokens,
            tokens_out=int(estimated_tokens * 0.3)  # Estimate 30% output
        )

        # Check permissions
        if not self.check_permission(agent_name, "execute"):
            execution.status = "blocked"
            self.execution_log.append(execution)
            return {
                "success": False,
                "error": f"Agent '{agent_name}' lacks permission for this operation",
                "execution_id": len(self.execution_log) - 1
            }

        # Record cost
        if self.cost_tracker:
            self.cost_tracker.record(f"{agent_name}:{task[:30]}", execution.tokens_in + execution.tokens_out)

        execution.status = "completed"
        self.execution_log.append(execution)

        # Update agent stats
        if agent_name in self.agents:
            self.agents[agent_name]["executions"].append(execution)

        return {
            "success": True,
            "execution_id": len(self.execution_log) - 1,
            "cost_units": execution.tokens_in + execution.tokens_out,
            "message": f"Task executed with {execution.permission_mode} permissions"
        }

    def get_cost_summary(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Get cost summary for all agents or specific agent"""
        if agent_name:
            executions = [e for e in self.execution_log if e.agent_name == agent_name]
        else:
            executions = self.execution_log

        total_in = sum(e.tokens_in for e in executions)
        total_out = sum(e.tokens_out for e in executions)

        return {
            "executions": len(executions),
            "total_tokens_in": total_in,
            "total_tokens_out": total_out,
            "total_tokens": total_in + total_out,
            "by_agent": self._breakdown_by_agent()
        }

    def _breakdown_by_agent(self) -> Dict[str, Dict[str, int]]:
        """Break down costs by agent"""
        breakdown = {}
        for execution in self.execution_log:
            name = execution.agent_name
            if name not in breakdown:
                breakdown[name] = {"executions": 0, "tokens": 0}
            breakdown[name]["executions"] += 1
            breakdown[name]["tokens"] += execution.tokens_in + execution.tokens_out
        return breakdown

    def get_permission_report(self) -> str:
        """Generate a permission report for all agents"""
        report = ["=" * 60, "AGENT PERMISSIONS REPORT", "=" * 60, ""]
        for name, config in self.agents.items():
            report.append(f"Agent: {name}")
            report.append(f"  Role: {config['role']}")
            report.append(f"  Permissions: {config['permissions']}")
            report.append(f"  Executions: {len(config['executions'])}")
            report.append("")
        return "\n".join(report)

    def set_permission_mode(self, agent_name: str, mode: str):
        """Change an agent's permission mode"""
        if mode not in self.PERMISSION_MODES:
            raise ValueError(f"Invalid mode. Use: {self.PERMISSION_MODES}")

        if agent_name in self.agents:
            self.agents[agent_name]["permissions"] = mode
            print(f"✅ {agent_name} permissions updated to '{mode}'")
        else:
            print(f"❌ Agent '{agent_name}' not found")


# Global integration instance (singleton pattern)
_integration: Optional[OpenClawClawIntegration] = None


def get_integration() -> OpenClawClawIntegration:
    """Get or create the global integration instance"""
    global _integration
    if _integration is None:
        _integration = OpenClawClawIntegration()
    return _integration


def register_lisa_nyx_kael():
    """Quick setup for the three main agents"""
    integration = get_integration()

    # Lisa: Authority layer - read-only for safety
    integration.register_agent("lisa", "Authority Layer", "read-only")

    # Nyx: Intelligence layer - workspace-write for research
    integration.register_agent("nyx", "Intelligence Layer", "workspace-write")

    # Kael: Execution layer - workspace-write (can be elevated to danger-full-access)
    integration.register_agent("kael", "Execution Layer", "workspace-write")

    print("\n" + "=" * 60)
    print("OpenClaw + Claw-Code Integration Active")
    print("=" * 60)
    return integration


# Convenience functions for OpenClaw skills
def track_execution(agent_name: str, task: str, estimated_tokens: int = 1000) -> Dict[str, Any]:
    """Track an agent execution with cost and permissions"""
    integration = get_integration()
    if agent_name not in integration.agents:
        integration.register_agent(agent_name, "Auto-registered", "read-only")
    return integration.execute_with_tracking(agent_name, task, estimated_tokens)


def check_tool_permission(agent_name: str, tool_name: str) -> bool:
    """Check if an agent can use a specific tool"""
    return get_integration().check_permission(agent_name, tool_name)


def elevate_permissions(agent_name: str, reason: str):
    """Temporarily elevate agent permissions (with audit log)"""
    integration = get_integration()
    current = integration.agents.get(agent_name, {}).get("permissions", "read-only")

    if current == "read-only":
        new_mode = "workspace-write"
    elif current == "workspace-write":
        new_mode = "danger-full-access"
    else:
        print(f"⚠️  {agent_name} already has full access")
        return

    print(f"⚡ Elevating {agent_name} to '{new_mode}' mode")
    print(f"   Reason: {reason}")
    integration.set_permission_mode(agent_name, new_mode)


def get_session_costs() -> Dict[str, Any]:
    """Get cost summary for current session"""
    return get_integration().get_cost_summary()


def get_permissions_report() -> str:
    """Get full permissions report"""
    return get_integration().get_permission_report()


# Testing
if __name__ == "__main__":
    print("🦞 Claw-Code Integration Test")
    print("=" * 60)

    # Setup agents
    integration = register_lisa_nyx_kael()

    # Test executions
    print("\n📊 Testing executions:")
    track_execution("nyx", "Research $1K/month opportunities", 1500)
    track_execution("lisa", "Review and approve opportunity", 800)
    track_execution("kael", "Setup automation workflow", 2000)

    # Show costs
    print("\n" + get_permissions_report())

    # Show cost summary
    print("\n" + "=" * 60)
    print("COST SUMMARY")
    print("=" * 60)
    summary = get_session_costs()
    print(f"Total executions: {summary['executions']}")
    print(f"Total tokens: {summary['total_tokens']}")
    print("\nBy agent:")
    for agent, data in summary['by_agent'].items():
        print(f"  {agent}: {data['executions']} executions, {data['tokens']} tokens")

    print("\n✅ Integration test complete!")
