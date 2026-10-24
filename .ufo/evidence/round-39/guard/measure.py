#!/usr/bin/env python3
"""Round-39 C1 counter — depth no-harm guard versus canonical command D.

Contract: C1_R39_PASS=true iff the round-39 contract at REV names a depth-guard
regex, that regex's recorded_cases and depth_score equal canonical SCORECARD
command D on the live runner and on a ledger-stripped copy of that runner, and
the round-38 guard regex ^\\s*leg matches 0 lines of the live runner.
A missing round-39 contract is the do-nothing control and cannot pass.

Exit codes: 0 pass · 1 fail · 2 usage or unreadable revision.
"""
import argparse
import re
import subprocess
import sys

COMMAND_D = re.compile(r'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+', re.M)
R38_VACUOUS = re.compile(r'^\s*leg', re.M)


def git_show(lane, rev, path):
    proc = subprocess.run(
        ['git', '-C', lane, 'show', '%s:%s' % (rev, path)],
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.decode('utf-8', 'replace')


def counts(pattern, text):
    n = len(pattern.findall(text))
    return n, min(10, n)


def strip_ledger(text):
    kept = [line for line in text.splitlines() if not COMMAND_D.match(line)]
    return '\n'.join(kept) + '\n'


def load_regex(contract_text):
    import json
    try:
        doc = json.loads(contract_text)
    except json.JSONDecodeError:
        return None
    guard = doc.get('no_harm_guard') or {}
    raw = guard.get('depth_command_d_regex')
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return re.compile(raw, re.M)
    except re.error:
        return None


def emit(fields, ok):
    body = ' '.join('%s=%s' % (k, v) for k, v in fields)
    print('C1_R39: %s C1_R39_PASS=%s' % (body, 'true' if ok else 'false'))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description='round-39 C1 guard counter')
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    args = ap.parse_args()
    runner = git_show(args.lane, args.rev, 'tools/mutate-and-run.sh')
    if runner is None:
        print('C1_R39: runner_unreadable=1 C1_R39_PASS=false', file=sys.stderr)
        return 2
    r38_hits = len(R38_VACUOUS.findall(runner))
    live_d, live_score = counts(COMMAND_D, runner)
    stripped = strip_ledger(runner)
    strip_d, strip_score = counts(COMMAND_D, stripped)
    contract = git_show(args.lane, args.rev, '.ufo/evidence/round-39/contract.json')
    if contract is None:
        return emit([
            ('guard_absent', 1),
            ('live_d', '%d/%d' % (live_d, live_score)),
            ('strip_d', '%d/%d' % (strip_d, strip_score)),
            ('live_agree', 0),
            ('stripped_agree', 0),
            ('r38_regex_hits', r38_hits),
            ('mismatches', 1),
            ('rev', args.rev),
        ], False)
    guard_re = load_regex(contract)
    if guard_re is None:
        return emit([
            ('guard_absent', 0),
            ('regex_unreadable', 1),
            ('r38_regex_hits', r38_hits),
            ('mismatches', 1),
            ('rev', args.rev),
        ], False)
    live_g, live_gs = counts(guard_re, runner)
    strip_g, strip_gs = counts(guard_re, stripped)
    live_agree = int((live_g, live_gs) == (live_d, live_score))
    stripped_agree = int((strip_g, strip_gs) == (strip_d, strip_score))
    mismatches = (1 - live_agree) + (1 - stripped_agree)
    ok = live_agree == 1 and stripped_agree == 1 and r38_hits == 0 and mismatches == 0
    return emit([
        ('guard_absent', 0),
        ('live_guard', '%d/%d' % (live_g, live_gs)),
        ('live_d', '%d/%d' % (live_d, live_score)),
        ('strip_guard', '%d/%d' % (strip_g, strip_gs)),
        ('strip_d', '%d/%d' % (strip_d, strip_score)),
        ('live_agree', live_agree),
        ('stripped_agree', stripped_agree),
        ('r38_regex_hits', r38_hits),
        ('mismatches', mismatches),
        ('rev', args.rev),
    ], ok)


if __name__ == '__main__':
    sys.exit(main())
