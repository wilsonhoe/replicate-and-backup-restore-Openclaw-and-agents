# OpenClaw Models Status Report

**Generated:** 2026-03-30

## Provider Health Check

| Provider | Status | HTTP Code | Notes |
|----------|--------|-----------|-------|
| **ollama (local)** | ✅ **ONLINE** | 200 | 5 models available |
| **iflow** | ✅ **ONLINE** | 200 | API key valid |
| **alibaba-qwen** | ✅ **ONLINE** | 200 | API key valid |
| **xai** | ❌ **OFFLINE** | 401 | No API key configured |
| **qwen-portal** | ❌ **OFFLINE** | 404 | Endpoint not found |

## Available Models

### Local Ollama (http://127.0.0.1:11434)
| Model | Context | Status |
|-------|---------|--------|
| glm-5:cloud | 202k | ✅ Primary |
| deepseek-v3.1:671b-cloud | 262k | ✅ Available |
| gpt-oss:120b-cloud | 262k | ✅ Available |
| qwen3-coder:480b-cloud | 262k | ✅ Available |
| nomic-embed-text:latest | 198k | ✅ Available |

### Iflow (https://apis.iflow.cn/v1)
| Model | Context | Status |
|-------|---------|--------|
| kimi-k2 | 125k | ✅ Available |
| deepseek-v3 | 125k | ✅ Available |
| qwen3-coder | 125k | ✅ Available |
| qwen3-max | 128k | ✅ Available |
| qwen3-32b | 128k | ✅ Available |

### Alibaba Qwen (https://dashscope-intl.aliyuncs.com)
| Model | Context | Status |
|-------|---------|--------|
| qwen-max | 128k | ✅ Available |
| qwen-plus | 195k | ✅ Available |
| qwen-turbo | 98k | ✅ Available |

## Current Lisa Configuration

**Primary Model:** `ollama/glm-5:cloud` (LOCAL)
- Context: 198k tokens
- Cost: $0 (local)
- Status: ✅ Active

**Fallback Chain:**
1. `ollama/glm-5:cloud` (local)
2. `iflow/kimi-k2`
3. `iflow/deepseek-v3`
4. `alibaba-qwen/qwen-plus`
5. `iflow/qwen3-coder`

## Switching Models

### Via OpenClaw CLI:
```bash
# Switch primary model
openclaw config set agents.defaults.model.primary ollama/glm-5:cloud

# Switch to iflow
openclaw config set agents.defaults.model.primary iflow/kimi-k2

# Switch to alibaba
openclaw config set agents.defaults.model.primary alibaba-qwen/qwen-plus
```

### Manual Edit:
Edit `~/.openclaw/openclaw.json`:
```json
"model": {
  "primary": "PROVIDER/MODEL",
  "fallbacks": [...]
}
```

## Recommended Configurations

### Option 1: Local-First (Current)
- **Primary:** `ollama/glm-5:cloud`
- **Pros:** Free, fast, private
- **Cons:** Requires local GPU/resources

### Option 2: Cloud-First (Reliable)
- **Primary:** `iflow/kimi-k2`
- **Pros:** Always available, no local resources
- **Cons:** API key required

### Option 3: Hybrid (Balanced)
- **Primary:** `ollama/glm-5:cloud`
- **Fallback 1:** `iflow/kimi-k2`
- **Fallback 2:** `alibaba-qwen/qwen-plus`
- **Pros:** Local when possible, cloud backup

## Troubleshooting

### Model not responding:
1. Check provider status above
2. Verify API keys in config
3. Test with `openclaw models test MODEL`

### Switch model temporarily:
```bash
/model iflow/kimi-k2
```

### Check current model:
```bash
openclaw config get agents.defaults.model.primary
```

## Last Updated
2026-03-30
