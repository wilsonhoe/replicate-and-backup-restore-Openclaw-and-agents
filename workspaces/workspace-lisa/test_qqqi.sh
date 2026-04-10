#!/bin/bash
cd /home/wls/.openclaw/workspace-lisa/daily_stock_analysis
python3 main.py --dry-run 2>&1 | tee /tmp/qqqi_test.log