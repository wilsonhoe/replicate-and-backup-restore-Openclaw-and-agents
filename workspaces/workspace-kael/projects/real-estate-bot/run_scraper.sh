#!/bin/bash
# Real Estate Lead Bot - Cron wrapper with error handling

SCRIPT_DIR="/home/wls/.openclaw/workspace-kael/projects/real-estate-bot"
LOG_FILE="$SCRIPT_DIR/cron.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting Real Estate Lead Bot" >> "$LOG_FILE"

# Run the scraper
python3 "$SCRIPT_DIR/scraper.py" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[$TIMESTAMP] SUCCESS: Scraper completed" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ERROR: Scraper failed with exit code $EXIT_CODE" >> "$LOG_FILE"
    # Optional: Send alert notification
    # echo "Real Estate Lead Bot failed" | mail -s "Scraper Alert" admin@example.com
fi

echo "[$TIMESTAMP] Finished" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

exit $EXIT_CODE