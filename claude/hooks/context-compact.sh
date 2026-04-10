#!/bin/bash
# Strategic context compaction hook
# Triggers compaction when threshold reached

COMPACT_THRESHOLD=${ECC_COMPACT_THRESHOLD:-0.7}
CONTEXT_USAGE=${ECC_CONTEXT_USAGE:-0}

if (( $(echo "$CONTEXT_USAGE > $COMPACT_THRESHOLD" | bc -l) )); then
    echo "🔄 Context threshold reached ($CONTEXT_USAGE). Triggering compaction..." >&2
    # Signal to compact context
    export ECC_SHOULD_COMPACT=1
fi

exit 0
