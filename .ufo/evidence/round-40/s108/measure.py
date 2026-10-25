#!/usr/bin/env python3
"""Round-40 C2 counter — S108 quote pinned to a committed snapshot.

C2_R40_PASS=true only when the snapshot blob at REV matches the contract
sha256 and the frozen quote occurs in its tag-stripped text. The live page
wraps the flag and `.expected` in <code> tags, so a raw-byte search for the
contiguous quote is the wrong check; the predicate is the stripped text.
A missing snapshot is the do-nothing control. Removing the contiguous
prefix 可以通过使用参数 from the raw bytes must make the stripped quote miss
(stripped_quote_fails=1). A status edit is not a substitute for the bytes.

Exit codes: 0 pass · 1 fail · 2 usage or unreadable revision.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys

SNAPSHOT = '.ufo/evidence/round-40/s108/golden_tests.zh-cn.html'
CONTRACT = '.ufo/evidence/round-40/contract.json'
QUOTE = '可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。'


def git_show(lane, rev, path):
    proc = subprocess.run(
        ['git', '-C', lane, 'show', '%s:%s' % (rev, path)],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def stripped_text(blob):
    text = re.sub(rb'<script[\s\S]*?</script>', b' ', blob, flags=re.I)
    text = re.sub(rb'<style[\s\S]*?</style>', b' ', text, flags=re.I)
    text = re.sub(rb'<[^>]+>', b' ', text)
    text = re.sub(rb'\s+', b' ', text)
    return text


def emit(fields, ok):
    body = ' '.join('%s=%s' % (k, v) for k, v in fields)
    print('C2_R40: %s C2_R40_PASS=%s' % (body, 'true' if ok else 'false'))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description='round-40 C2 S108 snapshot counter')
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    args = ap.parse_args()
    blob = git_show(args.lane, args.rev, SNAPSHOT)
    contract = git_show(args.lane, args.rev, CONTRACT)
    pin = None
    frozen_quote = QUOTE
    if contract is not None:
        try:
            claims = json.loads(contract.decode('utf-8'))['claims']['C2']
            pin = claims['snapshot_sha256']
            frozen_quote = claims['quote']
        except (json.JSONDecodeError, KeyError, TypeError, UnicodeDecodeError):
            pin = None
    if blob is None:
        return emit([
            ('snapshot_absent', 1),
            ('quote_in_snapshot', 0),
            ('sha_ok', 0),
            ('stripped_quote_fails', 0),
            ('rev', args.rev),
        ], False)
    digest = hashlib.sha256(blob).hexdigest()
    quote_bytes = frozen_quote.encode('utf-8')
    present = int(quote_bytes in stripped_text(blob))
    prefix = '可以通过使用参数'.encode('utf-8')
    removed = blob.replace(prefix, b'QUOTE_REMOVED', 1)
    stripped_fails = int(prefix in blob and quote_bytes not in stripped_text(removed))
    sha_ok = int(pin == digest and pin is not None)
    ok = present == 1 and sha_ok == 1 and stripped_fails == 1
    return emit([
        ('snapshot_absent', 0),
        ('quote_in_snapshot', present),
        ('sha_ok', sha_ok),
        ('stripped_quote_fails', stripped_fails),
        ('rev', args.rev),
    ], ok)


if __name__ == '__main__':
    sys.exit(main())
