#!/bin/bash
# Pre-read hook - optimizes file reading
# Skips reading large files that aren't needed

MAX_FILE_SIZE=${ECC_MAX_FILE_SIZE:-100000}  # 100KB default
FILE="$1"

if [ -f "$FILE" ]; then
    FILE_SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE" 2>/dev/null)
    if [ "$FILE_SIZE" -gt "$MAX_FILE_SIZE" ]; then
        echo "⚠️ Large file detected ($FILE_SIZE bytes). Use offset/limit parameters." >&2
    fi
fi

exit 0
