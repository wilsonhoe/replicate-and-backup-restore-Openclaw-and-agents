# Claw-Code Integration with OpenClaw

## Overview

Claw-code (`ultraworkers/claw-code`) is a Python/Rust reimplementation of Claude Code architecture that can enhance OpenClaw with advanced agent capabilities.

**Repository Location:** `/home/wls/.openclaw/claw-code/`

---

## What's Available

### 1. Python Workspace (`claw-code/src/`)
- **69 Python modules** for agent orchestration
- Command surface mirroring (`commands.py`)
- Tool abstractions with permission contexts (`tools.py`)
- QueryEngine for agent coordination (`query_engine.py`)
- Cost tracking and hooks (`cost_tracker.py`, `costHook.py`)
- Bootstrap graph for initialization (`bootstrap_graph.py`)
- Bridge, buddy, coordinator, hooks systems
- Skills, services, state management

### 2. Rust Workspace (`claw-code/rust/`)
- **Active CLI implementation** (`claw` binary)
- API crate for Anthropic integration
- Runtime for agent execution
- Mock Anthropic service for testing
- Parity harness for verification
- Telemetry and plugins

---

## Integration Opportunities

### Phase 1: Tool System Enhancement
**Files to integrate:**
- `claw-code/src/tools.py` - Permission-aware tool system
- `claw-code/src/permissions.py` - Tool permission contexts
- `claw-code/src/tool_pool.py` - Tool pool management

**Benefits:**
- Granular tool permissions (read-only, workspace-write, danger-full-access)
- Better permission prompts for user safety
- Tool filtering by context

### Phase 2: Command Surface Expansion
**Files to integrate:**
- `claw-code/src/commands.py` - Command registry
- `claw-code/src/command_graph.py` - Command dependency graph

**Benefits:**
- Mirrored command structure from Claude Code
- Command dependency resolution
- Command discovery and help

### Phase 3: Agent Orchestration
**Files to integrate:**
- `claw-code/src/coordinator/` - Multi-agent coordination
- `claw-code/src/assistant/` - Assistant management
- `claw-code/src/buddy/` - Buddy system

**Benefits:**
- Advanced multi-agent workflows
- Better agent-to-agent communication
- Agent lifecycle management

### Phase 4: Cost Tracking & Hooks
**Files to integrate:**
- `claw-code/src/cost_tracker.py` - Token usage tracking
- `claw-code/src/costHook.py` - Cost-aware hooks
- `claw-code/src/hooks/` - Hook system

**Benefits:**
- Real-time cost monitoring
- Budget enforcement
- Usage analytics

### Phase 5: Rust CLI Alternative
**Files to use:**
- `claw-code/rust/target/debug/claw` - Native CLI

**Benefits:**
- Native performance
- Direct Anthropic API integration
- Mock service for testing
- Session management

---

## Recommended Integration Path

### Option A: Hybrid Python Enhancement
1. Import claw-code Python modules as skills in OpenClaw
2. Use `commands.py` and `tools.py` for enhanced command/tool systems
3. Keep OpenClaw as the gateway, add claw-code capabilities

**Implementation:**
```python
# In OpenClaw skill
from claw_code.src.tools import get_tools, execute_tool
from claw_code.src.commands import execute_command
```

### Option B: Rust CLI as Alternative Interface
1. Build the Rust workspace: `cd claw-code/rust && cargo build`
2. Use `claw` CLI alongside `openclaw` CLI
3. Share configuration between them

**Implementation:**
```bash
# Build Rust CLI
cd /home/wls/.openclaw/claw-code/rust
cargo build --workspace

# Use claw CLI
./target/debug/claw prompt "task description"
```

### Option C: Full Migration
1. Replace OpenClaw gateway with Rust runtime
2. Port agent configs to claw-code format
3. Use claw-code as the primary system

---

## Quick Start Commands

```bash
# 1. Build Rust CLI
cd /home/wls/.openclaw/claw-code/rust
cargo build --workspace

# 2. Test Python modules
cd /home/wls/.openclaw/claw-code
python3 -m src.main summary

# 3. Run claw CLI
./rust/target/debug/claw --help

# 4. Run mock parity harness
./rust/scripts/run_mock_parity_harness.sh
```

---

## Configuration

Claw-code uses `.claw.json` configuration:
- `~/.claw.json` - Global settings
- `<repo>/.claw.json` - Repository-specific
- `<repo>/.claw/settings.json` - Detailed settings

**Key settings:**
- `ANTHROPIC_API_KEY` - API key
- `ANTHROPIC_BASE_URL` - Proxy URL (optional)
- Permission modes: `read-only`, `workspace-write`, `danger-full-access`

---

## Testing

```bash
# Python tests
cd /home/wls/.openclaw/claw-code
python3 -m unittest discover -s tests -v

# Rust tests
cd /home/wls/.openclaw/claw-code/rust
cargo test --workspace
```

---

## Next Steps

1. **Evaluate** - Decide which integration option (A, B, or C)
2. **Build** - If using Rust, run `cargo build`
3. **Test** - Run parity harness to verify compatibility
4. **Integrate** - Start with Phase 1 (Tools) for immediate benefit
5. **Migrate** - Gradually enhance OpenClaw with claw-code capabilities

---

## Documentation

- `claw-code/README.md` - Project overview
- `claw-code/USAGE.md` - Rust CLI usage
- `claw-code/PARITY.md` - Parity tracking
- `claw-code/PHILOSOPHY.md` - Design philosophy
- `claw-code/ROADMAP.md` - Development roadmap

---

**Status:** Repository cloned and ready for integration
**Last Updated:** 2026-04-05
