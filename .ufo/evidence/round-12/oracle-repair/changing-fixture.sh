#!/bin/sh
set -eu
state=${FAILURE_ORACLE_STATE:?FAILURE_ORACLE_STATE is required}
count=0
if [ -f "$state" ]; then
    IFS= read -r count < "$state" || :
fi
count=$((count + 1))
printf '%s\n' "$count" > "$state"
if [ "$count" -eq 1 ]; then printf 'CONTROL\n'; else printf 'ALTERNATE\n'; fi
