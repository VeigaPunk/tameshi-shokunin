#!/bin/bash
# Round-46 receipts for the verified-at lines of the three C3 entries (QUALITY criterion 51): live fetch, digest vs committed snapshot,
# the located recheck phrase, with the extraction tool's sha256. Usage: entry-rechecks.sh LANE
L=${1:-/home/vgpnk/Projects/shokunin/tameshi-shokunin}
S=$L/.ufo/evidence/round-46/coverage/sources
M=$L/.ufo/evidence/round-45/freshness/measure.py
T=$(mktemp -d)
echo "TOOL $M sha256 $(sha256sum $M | cut -c1-64)"
echo "LANE_HEAD $(git -C $L rev-parse master)"
chk() { name=$1; url=$2; snap=$3; phrase=$4
  curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o $T/f "$url"; rc=$?
  live=$(sha256sum $T/f | cut -c1-64); pin=$(sha256sum $S/$snap | cut -c1-64)
  n=$(python3 $M --extract $T/f | grep -oF "$phrase" | wc -l)
  echo "RECHECK $name curl_exit=$rc live_sha256=$live snapshot_sha256=$pin identical=$([ "$live" = "$pin" ] && echo yes || echo no) phrase_count=$n phrase=[$phrase]"; }
chk r6-flaky-failures-cluster https://arxiv.org/abs/2504.16777 arxiv-2504.16777-abs.html 'co-occurring failures that share the same root causes'
chk r5-undetected-flaky-failures 'https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/' tum-portal-flaky-failures.html 'Modern CI systems commonly rerun failed tests within the same job to identify flaky failures'
chk r9-false-red-rate 'https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json' google-flaky-feed-6277555988217606236.json 'about 84% of the transitions we observe from pass to fail involve a flaky test'
rm -rf $T
