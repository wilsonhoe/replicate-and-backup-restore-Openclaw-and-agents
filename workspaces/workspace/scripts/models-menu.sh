#!/bin/bash
# OpenClaw Models Switcher Menu

clear
echo "=========================================="
echo "   OpenClaw Models Switcher Menu"
echo "=========================================="
echo ""

# Get current model
CURRENT=$(openclaw config get agents.defaults.model.primary 2>/dev/null || echo "Unknown")
echo "Current Primary Model: $CURRENT"
echo ""
echo "=========================================="
echo ""

# Show menu
echo "Select a model to switch to:"
echo ""
echo "LOCAL OLLAMA MODELS:"
echo "  1) kimi-k2.5:cloud (198k ctx) - DEFAULT ✓"
echo "  2) glm-5:cloud (198k ctx)"
echo "  3) deepseek-v3.1:671b-cloud (262k ctx)"
echo "  4) gpt-oss:120b-cloud (262k ctx)"
echo "  5) qwen3-coder:480b-cloud (262k ctx)"
echo "  6) minimax-m2.5:cloud (204k ctx)"
echo ""
echo "CLOUD MODELS (iflow):"
echo "  7) kimi-k2 (125k ctx)"
echo "  8) deepseek-v3 (125k ctx)"
echo "  9) qwen3-coder (125k ctx)"
echo ""
echo "CLOUD MODELS (alibaba-qwen):"
echo "  10) qwen-plus (195k ctx)"
echo "  11) qwen-max (128k ctx)"
echo "  12) qwen-turbo (98k ctx)"
echo ""
echo "OTHER OPTIONS:"
echo "  13) View full models list"
echo "  14) Test current model"
echo "  15) Exit"
echo ""
echo -n "Enter choice [1-15]: "
read choice

case $choice in
  1)
    MODEL="ollama/kimi-k2.5:cloud"
    ;;
  2)
    MODEL="ollama/glm-5:cloud"
    ;;
  3)
    MODEL="ollama/deepseek-v3.1:671b-cloud"
    ;;
  4)
    MODEL="ollama/gpt-oss:120b-cloud"
    ;;
  5)
    MODEL="ollama/qwen3-coder:480b-cloud"
    ;;
  6)
    MODEL="ollama/minimax-m2.5:cloud"
    ;;
  7)
    MODEL="iflow/kimi-k2"
    ;;
  8)
    MODEL="iflow/deepseek-v3"
    ;;
  9)
    MODEL="iflow/qwen3-coder"
    ;;
  10)
    MODEL="alibaba-qwen/qwen-plus"
    ;;
  11)
    MODEL="alibaba-qwen/qwen-max"
    ;;
  12)
    MODEL="alibaba-qwen/qwen-turbo"
    ;;
  13)
    openclaw models list
    exit 0
    ;;
  14)
    echo "Testing current model..."
    openclaw models test "$CURRENT"
    exit 0
    ;;
  15)
    echo "Exiting..."
    exit 0
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "Switching to: $MODEL"
echo ""

# Update config
openclaw config set agents.defaults.model.primary "$MODEL"
openclaw config set agents.list[0].model "$MODEL"

if [ $? -eq 0 ]; then
  echo "✅ Model switched successfully!"
  echo ""
  echo "Restart OpenClaw to apply:"
  echo "  systemctl --user restart openclaw-gateway"
else
  echo "❌ Failed to switch model"
  exit 1
fi
