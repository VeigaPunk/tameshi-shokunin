#!/usr/bin/env python3
"""Reader-report validator: accept exactly the reports the cold-read credit code accepts.

    validate-reader.py --lane LANE --rev REV [--c0 C0] [--mode M] [--quote-check] FILE...

REV is the revision the wave tree (and the round-18 sectionize) is read at; C0 is
the content commit a binder pass pins (default: REV).  Every read is a git object
read at REV/C0 - the live working tree is never consulted, so a report cannot be
credited by bytes that are not committed.

What the credit code actually accepts (frozen round-54 evidence, cited in the
report as `credit-acceptance`):

  * round-54 `integrate/binder.py` (the thing that turns a reader into a ledger
    entry): a committed `.ufo/waves/round-54/w{1,2}/*.json` whose `heading` is a
    str, whose `cand` equals the full 40-hex c0, whose `section_sha256` equals the
    section's sha at c0 (frozen round-18 `sectionize`), whose `findings` list is no
    longer than the adjudicated allowance, and which has a sibling `<stem>.md`.
  * frozen round-54 `c1/measure.py` arm 4: `cand == c0` and
    `section_sha256 == sections-at-REV[heading].sha256`.
  * frozen round-21 selector / round-18 `measure.py` (the credit algorithm over the
    ledger): the bound entry must carry `read_rev == c0`, `sha256` equal to the
    section bytes at the read rev, `(skill_sha256, start)` matching the section, and
    pass `entry_reason(..., strict=True)` - which is why a report must name a
    section that exists AT ITS OWN `cand`.

Modes
  canonical   heading exists at `cand`; `cand` is the full 40-hex sha of a commit in
              the lane; `section_sha256` is the sha of that section's bytes at
              `cand`; `findings` is a list of {quote, why} objects.  This is the
              contract the round-55 reader must satisfy (section-at-own-cand).
  binder      canonical + `cand == C0` + sibling `.md` present.
  counter     canonical + `cand == C0` + sha equals the section at REV (arm 4).
  all         run every mode and accept only when all three accept (fail-closed).

`--quote-check` adds the honesty arm the credit code does NOT have: every
`findings[].quote` must occur verbatim in the section body at `cand`.  It is
reported separately, never folded into the credit verdict.

Exit 0 iff every named file is accepted; 1 otherwise.  Stdlib only.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile

R18 = '.ufo/evidence/round-18/measure.py'
FULL_SHA = re.compile(r'^[0-9a-f]{40}$')

MOD = None          # frozen round-18 module, loaded from the lane at REV
_CACHE = {}


def env_clean():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1')
    return env


def git(lane, *args, check=False):
    return subprocess.run(['git', '-C', lane, *args], capture_output=True, env=env_clean(),
                          check=check)


def resolve(lane, value):
    run = git(lane, 'rev-parse', '--verify', str(value) + '^{commit}')
    if run.returncode != 0:
        return None
    return run.stdout.decode().strip()


def show(lane, rev, path):
    run = git(lane, 'show', '%s:%s' % (rev, path))
    return run.stdout if run.returncode == 0 else None


def load_module(lane, rev, work):
    key = (rev,)
    if key in _CACHE:
        return _CACHE[key]
    raw = show(lane, rev, R18)
    if raw is None:
        raise SystemExit('cannot read %s at %s' % (R18, rev))
    path = os.path.join(work, 'r18-%s.py' % rev[:12])
    with open(path, 'wb') as fh:
        fh.write(raw)
    spec = importlib.util.spec_from_file_location('r18_%s' % rev[:8], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _CACHE[key] = mod
    return mod


def sections_at(lane, rev, work):
    key = (rev)
    if ('sec', key) in _CACHE:
        return _CACHE[('sec', key)]
    mod = load_module(lane, rev, work)
    raw = show(lane, rev, 'SKILL.md')
    if raw is None:
        raise SystemExit('cannot read SKILL.md at %s' % rev)
    secs = {s['heading']: s for s in mod.sectionize(raw)}
    _CACHE[('sec', key)] = (secs, raw)
    return secs, raw


def section_body(raw, sec):
    """The exact bytes-fed text sectionize hashes: lines[start-1:end], trailing
    whitespace-only lines stripped, joined with \\n, no trailing newline."""
    text = raw.decode('utf-8', 'surrogateescape')
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    body = list(lines[sec['start'] - 1:sec['end']])
    while body and body[-1].strip() == '':
        body.pop()
    return '\n'.join(body)


def validate(lane, path, mode, rev, c0, work, quote_check):
    """Return (accepted, [reason...], facts)."""
    reasons = []
    facts = {}
    try:
        with open(path, 'rb') as fh:
            d = json.loads(fh.read().decode('utf-8', 'surrogateescape'))
    except (ValueError, OSError) as exc:
        return False, ['unparsable:%s' % type(exc).__name__], facts
    if not isinstance(d, dict):
        return False, ['not-an-object'], facts
    heading = d.get('heading')
    if not isinstance(heading, str):
        return False, ['heading-not-str'], facts
    facts['file'] = os.path.basename(path)
    facts['heading'] = heading

    # cand: full 40-hex and resolvable (the credit code compares it by string
    # equality with a resolved c0, so an abbreviation can never match).
    cand_raw = d.get('cand')
    facts['cand'] = cand_raw
    cand = None
    if not isinstance(cand_raw, str) or not FULL_SHA.match(cand_raw):
        reasons.append('cand-not-full-sha')
    else:
        cand = resolve(lane, cand_raw)
        if cand is None:
            reasons.append('cand-unresolvable')
        elif cand != cand_raw:
            reasons.append('cand-not-commit-sha')

    # section at cand
    sec = None
    if cand:
        secs, raw = sections_at(lane, cand, work)
        sec = secs.get(heading)
        if sec is None:
            reasons.append('heading-absent-at-cand')
        else:
            facts['start'] = sec['start']
            facts['end'] = sec['end']
            facts['section_sha256_at_cand'] = sec['sha256']
            if d.get('section_sha256') != sec['sha256']:
                reasons.append('section_sha256-mismatch-at-cand')

    # findings: a list of {quote, why} objects (the credit code only takes
    # len(findings); a non-list crashes it, an unquotable finding passes it).
    findings = d.get('findings')
    if findings is None:
        findings = []
    if not isinstance(findings, list):
        reasons.append('findings-not-list')
        findings = []
    for i, item in enumerate(findings):
        if not isinstance(item, dict):
            reasons.append('finding-%d-not-object' % i)
            continue
        if not isinstance(item.get('quote'), str) or not item.get('quote').strip():
            reasons.append('finding-%d-quote-missing' % i)
        if not isinstance(item.get('why'), str) or not item.get('why').strip():
            reasons.append('finding-%d-why-missing' % i)
    facts['findings'] = len(findings)

    # the honesty arm: quotes must be derivable from the section bytes at cand
    if quote_check and sec is not None:
        body = section_body(raw, sec)
        for i, item in enumerate(findings):
            q = item.get('quote') if isinstance(item, dict) else None
            if isinstance(q, str) and q and q not in body:
                reasons.append('finding-%d-quote-not-in-section-at-cand' % i)

    # binder mode: c0 equality + the sibling markdown report it requires
    if mode in ('binder', 'all'):
        if c0 and cand_raw != c0:
            reasons.append('binder-cand-not-c0')
        if not os.path.exists(path[:-5] + '.md'):
            reasons.append('binder-sibling-md-missing')

    # counter mode: sha must equal the section at REV (arm 4 of the frozen
    # round-54 counter).  Only meaningful when SKILL.md is byte-identical at c0
    # and REV; reported separately precisely so that divergence is visible.
    if mode in ('counter', 'all'):
        if c0 and cand_raw != c0:
            reasons.append('counter-cand-not-c0')
        rev_secs, _raw = sections_at(lane, rev, work)
        rsec = rev_secs.get(heading)
        if rsec is None:
            reasons.append('counter-heading-absent-at-rev')
        elif d.get('section_sha256') != rsec['sha256']:
            reasons.append('counter-section_sha256-mismatch-at-rev')
        facts['skill_identical_c0_rev'] = (show(lane, c0, 'SKILL.md') == show(lane, rev, 'SKILL.md')
                                           if c0 else None)

    accepted = not reasons
    return accepted, reasons, facts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--c0')
    ap.add_argument('--mode', default='canonical', choices=('canonical', 'binder', 'counter', 'all'))
    ap.add_argument('--quote-check', action='store_true')
    ap.add_argument('--json-out')
    ap.add_argument('files', nargs='+')
    a = ap.parse_args()

    rev = resolve(a.lane, a.rev)
    if rev is None:
        print('VALIDATOR error=rev-unresolvable', file=sys.stderr)
        return 2
    c0 = resolve(a.lane, a.c0) if a.c0 else rev
    if c0 is None:
        print('VALIDATOR error=c0-unresolvable', file=sys.stderr)
        return 2
    work = tempfile.mkdtemp(prefix='r55-validate-', dir=os.environ.get('TMPDIR'))

    rows = []
    accepted_n = 0
    for path in a.files:
        ok, reasons, facts = validate(a.lane, path, a.mode, rev, c0, work, a.quote_check)
        accepted_n += ok
        rows.append({'path': path, 'accepted': ok, 'reasons': reasons, 'facts': facts})
        print('%s %s %s %s' % ('ACCEPT' if ok else 'REJECT', os.path.basename(path),
                               'reasons=none' if ok else 'reasons=' + ','.join(reasons),
                               'findings=%d' % facts.get('findings', -1)))
    print('VALIDATOR mode=%s rev=%s c0=%s files=%d accepted=%d rejected=%d'
          % (a.mode, rev[:12], c0[:12], len(rows), accepted_n, len(rows) - accepted_n))
    if a.json_out:
        with open(a.json_out, 'w') as fh:
            json.dump({'mode': a.mode, 'rev': rev, 'c0': c0, 'rows': rows}, fh, indent=1)
    return 0 if accepted_n == len(rows) else 1


if __name__ == '__main__':
    sys.exit(main())
