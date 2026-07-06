#!/bin/bash
cd "$(dirname "$0")" || exit 1
echo "=== $(date) ===" >> veille.log
python3 scripts/fetch.py >> veille.log 2>&1
python3 scripts/summarize.py >> veille.log 2>&1
python3 scripts/build.py >> veille.log 2>&1
