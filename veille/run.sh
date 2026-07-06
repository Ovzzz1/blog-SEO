#!/bin/bash
cd "$(dirname "$0")" || exit 1
echo "=== $(date) ===" >> veille.log
python3 scripts/fetch.py >> veille.log 2>&1
python3 scripts/summarize.py >> veille.log 2>&1
python3 scripts/build.py >> veille.log 2>&1

cd .. || exit 1
if ! git diff --quiet -- veille/data/items.json veille/index.html || ! git diff --cached --quiet -- veille/data/items.json veille/index.html; then
    git add veille/data/items.json veille/index.html
    git commit -m "veille: refresh auto $(date '+%Y-%m-%d %H:%M')" >> veille/veille.log 2>&1
    git push >> veille/veille.log 2>&1
fi
