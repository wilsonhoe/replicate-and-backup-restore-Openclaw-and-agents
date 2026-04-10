# NotebookLM Integration

> Skill for OpenClaw agents to integrate with Google NotebookLM

## Installation

```bash
# Base install
pip install notebooklm-py --break-system-packages

# With browser automation (for automated login/source adding)
pip install "notebooklm-py[browser]" --break-system-packages
playwright install chromium
```

## Authentication

```bash
# One-time login (opens browser)
notebooklm login

# Or set auth token for headless (CI/CD)
export NOTEBOOKLM_AUTH_JSON='{"cookie": "...", "token": "..."}'
```

```bash
# One-time login (opens browser)
notebooklm login
```

## Basic Commands

### List Notebooks
```bash
notebooklm list
```

### Create Notebook
```bash
notebooklm create "Research: AI Agents"
```

### Set Active Notebook
```bash
notebooklm use <notebook-id>
```

### Add Sources
```bash
# Add file
notebooklm source add /path/to/document.pdf

# Add URL
notebooklm source add https://example.com/article

# Add Google Drive file
notebooklm source add-drive <drive-url>

# Add research (auto-web search)
notebooklm source add-research "latest AI agent frameworks"
```

### Ask Questions
```bash
# Interactive chat
notebooklm ask "Summarize the key findings"

# Get specific
notebooklm ask "What are the main challenges with multi-agent systems?"
```

### Get Summary
```bash
notebooklm summary
```

## Agent Integration

### Python Usage (CLI Wrapper)
```python
import subprocess
import json

def notebooklm_list():
    """List all notebooks"""
    result = subprocess.run(
        ["notebooklm", "list", "--format", "json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout) if result.returncode == 0 else None

def notebooklm_create(name: str) -> str:
    """Create a new notebook"""
    result = subprocess.run(
        ["notebooklm", "create", name],
        capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else None

def notebooklm_add_source(path: str) -> bool:
    """Add a source to current notebook"""
    result = subprocess.run(
        ["notebooklm", "source", "add", path],
        capture_output=True, text=True
    )
    return result.returncode == 0

def notebooklm_ask(question: str) -> str:
    """Ask the notebook a question"""
    result = subprocess.run(
        ["notebooklm", "ask", question],
        capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else result.stderr
```

### Python Module Usage (notebooklm-py)
```python
from notebooklm import Notebook, Source

# Initialize with auth
notebook = Notebook(auth_json={"cookie": "...", "token": "..."})

# Create notebook
nb = notebook.create("My Research")

# Add source
source = Source.add_url("https://example.com/article")
nb.add_source(source)

# Ask question
response = nb.ask("Summarize this")
print(response.text)
```

## Common Workflows

### Research Pipeline
```bash
# 1. Create research notebook
notebooklm create "Market Research: $TOPIC"

# 2. Add sources
notebooklm source add-research "$QUERY"
notebooklm source add /path/to/local/docs

# 3. Wait for processing
notebooklm source wait

# 4. Get insights
notebooklm summary
notebooklm ask "What are the key trends?"
```

### Daily Intelligence Report
```bash
# Create dated notebook
notebooklm create "Daily Intel - $(date +%Y-%m-%d)"

# Add URLs from research
for url in $URLS; do
    notebooklm source add "$url"
done

# Generate summary
notebooklm summary > report.md
```

## Storage Location

- State: `~/.notebooklm/storage_state.json`

## Output Formats

```bash
# JSON output for parsing
notebooklm list --format json
notebooklm source list --format json
```

## Error Handling

Common issues:
- `login required` → Run `notebooklm login` first
- `no active notebook` → Run `notebooklm use <id>` or `notebooklm create`
- `source not ready` → Run `notebooklm source wait` for processing

## MemPalace Integration

Store Notebook IDs in MemPalace for agent persistence:

```bash
# Save notebook ID
python3 /home/wls/.openclaw/scripts/mempalace_cli.py add-drawer ".openclaw" "notebooklm" "NOTEBOOK_ID: abc123... | Topic: AI Agents | Created: 2026-04-10"

# Query later
python3 /home/wls/.openclaw/scripts/mempalace_cli.py search "notebooklm"
```
