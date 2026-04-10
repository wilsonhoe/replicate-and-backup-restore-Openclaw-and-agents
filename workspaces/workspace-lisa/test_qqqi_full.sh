#!/bin/bash
cd /home/wls/.openclaw/workspace-lisa/daily_stock_analysis
AGENT_MODE=true python3 main.py 2>&1 | tee /tmp/qqqi_full.log | tail -200