#!/bin/bash
# Round-51 attempt-3 fix for the w2 spec defect: refuse a wave dispatch whose taskCall still carries an unfilled
# template placeholder (`@P@`, found 95x in w2-dispatch.json; 41 seat files landed under literal @P@ names).
# Usage: placeholder-guard.sh DISPATCH_JSON. Exit 0 clean, 1 placeholder present, 2 unreadable.
f=$1; [ -r "$f" ] || { echo "PLACEHOLDER_GUARD: SETUP unreadable $f"; exit 2; }
n=$(python3 -c 'import json,sys,re; s=json.dumps(json.load(open(sys.argv[1]))["taskCall"]); print(len(re.findall(r"@[A-Z]@", s)))' "$f") || { echo "PLACEHOLDER_GUARD: SETUP parse"; exit 2; }
if [ "$n" = 0 ]; then echo "PLACEHOLDER_GUARD: PASS placeholders=0 $f"; exit 0; fi
echo "PLACEHOLDER_GUARD: FAIL placeholders=$n $f"; exit 1
