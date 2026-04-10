#!/bin/bash
# Post-edit hook - token-efficient verification
# Only runs essential checks

FILE="$1"

# Skip typecheck/lint for non-code files
if [[ "$FILE" =~ \.(md|txt|json|yaml|yml)$ ]]; then
    exit 0
fi

# Quick syntax check for code files
if [[ "$FILE" =~ \.(js|ts|jsx|tsx)$ ]]; then
    # Only check syntax, not full typecheck
    node --check "$FILE" 2>/dev/null || echo "⚠️ Syntax check failed"
fi

exit 0
