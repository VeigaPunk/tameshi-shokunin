#!/bin/sh
set -eu
state=${FAILURE_ORACLE_STATE:?FAILURE_ORACLE_STATE is required}
count=0
if [ -f "$state" ]; then
    IFS= read -r count < "$state" || :
fi
count=$((count + 1))
printf '%s\n' "$count" > "$state"
printf 'CONTROL\n'
