#!/usr/bin/env python3
"""Round-43 C3 counter — staged-package id guard (operability, capability).

Frozen before any seat scored and before the deciding run. It measures the tool
that answers the round-42 post-append hazard: the staged package
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` carries ids
S153–S255, and after round 42 the lane registry also holds S153–S158.

Predicate `C3_R43_PASS` is true iff:

  * self_pin=1 — this file's bytes at FREEZE and on disk equal
    `claims.C3.counter_sha256`;
  * tool_absent=0 and tool_sha_ok=1 — `tools/staged-id-guard.py` at REV is the
    pinned blob;
  * selftest_exit=0 — the tool's own selftest passes, and it reports at least
    the declared case count;
  * live_collisions_agree=1 — the tool's collision set equals the counter's own
    independent extraction (0-3-space pattern) over the registry at REV and the
    staged package;
  * live_held_agree=1 — the documents the tool calls already-held equal the
    counter's own document join (dedupe by URL);
  * live_unmapped=0, live_verdict=refused — every colliding staged row carries a
    document, and the tool refuses its own naive arithmetic map;
  * live_cascade=1 — that naive map's targets are all ids another staged row
    still holds;
  * naive_map_refused=1 — feeding that naive map back through `--map` is
    inadmissible;
  * safe_map_admitted=1 — a by-document map (held rows dedupe to their registry
    id; new documents take ids at or above the safe floor) is admitted;
  * map_dedupe_live=1 — the admitted safe map's dedupe entries are exactly the
    held documents;
  * staged_rows >= 100 — the package actually carries the staged set.

Counting command:

  python3 .ufo/evidence/round-43/guard/measure.py --lane LANE --rev REV --freeze FREEZE

`--control` scores a constant-empty stand-in tool for the collision check and
prints a CONTROL line; it is never the measurement. `--tool-file PATH` scores a
substitute tool (falsifier seats). Exit 0 iff the predicate is true, 1 if false,
2 on setup/refusal.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

SELF_REL = '.ufo/evidence/round-43/guard/measure.py'
CONTRACT_REL = '.ufo/evidence/round-43/contract.json'
TOOL_REL = 'tools/staged-id-guard.py'
SOURCES_REL = 'corpus/SOURCES.md'
STAGED_REL = '/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md'
TIMEOUT = 120
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
URL_RE = re.compile(r'https?://[^\s|,;]+')
SCHEME_RE = re.compile(r'^https?://')
WWW_RE = re.compile(r'^www\.')
MIN_CASES = 13


def git(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), capture_output=True)


def show(lane, rev, path):
    proc = git(lane, 'show', '%s:%s' % (rev, path))
    return proc.stdout if proc.returncode == 0 else None


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    with open(path, encoding='utf-8') as handle:
        return handle.read()


def number(sid):
    return int(sid[1:])


def norm_url(url):
    """The census' URL identity: no scheme, no www., lower case, no trailing slash."""
    text = url.strip().lower()
    text = SCHEME_RE.sub('', text)
    text = WWW_RE.sub('', text)
    return text.rstrip('/')


def own_parse(text):
    """Counter-side parse: {id: url} with the census-valid row pattern."""
    found = {}
    for line in text.splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
        blob = ' '.join(cells[1:6])
        url = URL_RE.search(blob)
        found[match.group(1)] = norm_url(url.group(0).rstrip('.,;)]')) if url else ''
    return found


def run_guard(tool, registry, staged, map_path=None):
    argv = [sys.executable, '-I', tool, '--registry', registry, '--staged', staged, '--json']
    if map_path:
        argv.extend(['--map', map_path])
    proc = subprocess.run(argv, capture_output=True, timeout=TIMEOUT)
    out = proc.stdout.decode('utf-8', 'replace')
    err = proc.stderr.decode('utf-8', 'replace')
    doc = None
    for line in out.splitlines():
        line = line.strip()
        if line.startswith('{'):
            doc = json.loads(line)
            break
    return proc.returncode, doc, err.strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--lane', default='.')
    parser.add_argument('--rev')
    parser.add_argument('--freeze')
    parser.add_argument('--staged', default=STAGED_REL)
    parser.add_argument('--tool-file')
    parser.add_argument('--control', action='store_true')
    args = parser.parse_args()
    lane = os.path.abspath(args.lane)
    rev = args.rev or subprocess.run(['git', '-C', lane, 'rev-parse', 'master'],
                                     capture_output=True).stdout.decode().strip()
    freeze = args.freeze or rev
    contract_raw = show(lane, freeze, CONTRACT_REL)
    if contract_raw is None:
        raise SystemExit('refusing: no contract at %s' % freeze)
    contract = json.loads(contract_raw)
    pin = contract['claims']['C3']['counter_sha256']
    self_raw = show(lane, freeze, SELF_REL)
    if self_raw is None:
        raise SystemExit('refusing: counter absent at freeze')
    with open(os.path.abspath(__file__), 'rb') as handle:
        running = sha(handle.read())
    self_pin = 1 if sha(self_raw) == pin and running == pin else 0

    tool_raw = show(lane, rev, TOOL_REL)
    tool_absent = 0 if tool_raw is not None else 1
    pins = contract.get('frozen_tools') or {}
    want_sha = pins.get(TOOL_REL, contract.get('tool_sha256'))
    tool_sha_ok = 1 if tool_raw is not None and sha(tool_raw) == want_sha else 0
    registry_raw = show(lane, rev, SOURCES_REL)
    if registry_raw is None:
        raise SystemExit('refusing: registry absent at REV')
    if not os.path.exists(args.staged):
        raise SystemExit('refusing: staged package absent at %s' % args.staged)

    work = tempfile.mkdtemp(prefix='tameshi-r43-c3-')
    try:
        registry_path = os.path.join(work, 'SOURCES.md')
        with open(registry_path, 'wb') as handle:
            handle.write(registry_raw)
        tool_path = os.path.join(work, TOOL_REL)
        os.makedirs(os.path.dirname(tool_path), exist_ok=True)
        if args.tool_file:
            with open(os.path.abspath(args.tool_file), 'rb') as src, open(tool_path, 'wb') as dst:
                dst.write(src.read())
        elif tool_raw is not None:
            with open(tool_path, 'wb') as handle:
                handle.write(tool_raw)
        else:
            tool_path = os.path.join(work, 'absent.py')
            with open(tool_path, 'w', encoding='utf-8') as handle:
                handle.write('import sys\nsys.exit(2)\n')

        selftest = subprocess.run([sys.executable, '-I', tool_path, '--selftest'],
                                  capture_output=True, timeout=TIMEOUT)
        selftest_text = selftest.stdout.decode('utf-8', 'replace')
        selftest_exit = 0 if selftest.returncode == 0 else 1
        cases_match = re.search(r'cases=(\d+) failed=(\d+)', selftest_text)
        cases = int(cases_match.group(1)) if cases_match else 0
        failed = int(cases_match.group(2)) if cases_match else -1

        code, doc, err = run_guard(tool_path, registry_path, args.staged)
        if doc is None:
            print('C3_R43: self_pin=%d tool_absent=%d tool_sha_ok=%d selftest_exit=%d '
                  'guard_error=%s C3_R43_PASS=false'
                  % (self_pin, tool_absent, tool_sha_ok, selftest_exit,
                     re.sub(r'\s', '_', err[:120]) or 'no_json'))
            return 1

        registry_ids = own_parse(registry_raw.decode('utf-8', 'replace'))
        staged_ids = own_parse(read(args.staged))
        own_collisions = sorted(set(registry_ids) & set(staged_ids), key=number)
        own_held = {}
        for sid in own_collisions:
            url = staged_ids.get(sid, '')
            if not url:
                continue
            for rid, rurl in registry_ids.items():
                if rurl and rurl == url:
                    own_held[sid] = rid
                    break
        top = max([number(sid) for sid in list(registry_ids) + list(staged_ids)] + [0])
        floor = 'S%03d' % (top + 1)

        live_collisions_agree = 1 if doc.get('collisions') == own_collisions else 0
        live_held_agree = 1 if doc.get('held') == own_held else 0
        live_unmapped = len(doc.get('unmapped') or [])
        live_verdict_refused = 1 if doc.get('verdict') == 'refused' else 0
        cascade = doc.get('cascade') or []
        live_cascade = 1 if cascade and all(sid in staged_ids for sid in cascade) else 0

        naive_path = os.path.join(work, 'naive-map.json')
        with open(naive_path, 'w', encoding='utf-8') as handle:
            json.dump({'map': doc.get('naive_map') or {}}, handle)
        naive_code, naive_doc, _ = run_guard(tool_path, registry_path, args.staged, naive_path)
        naive_refused = 1 if naive_code == 1 and (naive_doc or {}).get('verdict') == 'inadmissible' else 0

        safe_map = dict(own_held)
        index = 1
        for sid in own_collisions:
            if sid in safe_map:
                continue
            safe_map[sid] = 'S%03d' % (number(floor) + index - 1)
            index += 1
        safe_path = os.path.join(work, 'safe-map.json')
        with open(safe_path, 'w', encoding='utf-8') as handle:
            json.dump({'map': safe_map}, handle)
        safe_code, safe_doc, _ = run_guard(tool_path, registry_path, args.staged, safe_path)
        safe_admitted = 1 if safe_code == 0 and (safe_doc or {}).get('verdict') == 'admitted' else 0
        dedupe_live = 1 if (safe_doc or {}).get('map_dedupe') == own_held and own_held else 0

        if args.control:
            stub = os.path.join(work, 'stub.py')
            with open(stub, 'w', encoding='utf-8') as handle:
                handle.write('import json\nprint(json.dumps({"collisions": [], "held": {}, '
                             '"unmapped": [], "cascade": [], "verdict": "answered"}))\n')
            code2, doc2, _ = run_guard(stub, registry_path, args.staged)
            agree = 1 if doc2 and doc2.get('collisions') == own_collisions else 0
            print('C3_R43_CONTROL: stub_collisions_agree=%d expected_collisions=%d '
                  'C3_R43_CONTROL_PASS=%s' % (agree, len(own_collisions),
                                              'true' if agree else 'false'))
            return 0 if agree else 1

        passed = (self_pin == 1 and tool_absent == 0 and tool_sha_ok == 1
                  and selftest_exit == 0 and cases >= MIN_CASES and failed == 0
                  and live_collisions_agree == 1 and live_held_agree == 1
                  and live_unmapped == 0 and live_verdict_refused == 1
                  and live_cascade == 1 and naive_refused == 1
                  and safe_admitted == 1 and dedupe_live == 1
                  and len(staged_ids) >= 100)
        fields = [
            'C3_R43:',
            'self_pin=%d' % self_pin,
            'tool_absent=%d' % tool_absent,
            'tool_sha_ok=%d' % tool_sha_ok,
            'selftest_exit=%d' % selftest_exit,
            'selftest_cases=%d' % cases,
            'selftest_failed=%d' % failed,
            'staged_rows=%d' % len(staged_ids),
            'live_collisions=%d' % len(own_collisions),
            'live_collisions_agree=%d' % live_collisions_agree,
            'live_held=%d' % len(own_held),
            'live_held_agree=%d' % live_held_agree,
            'live_unmapped=%d' % live_unmapped,
            'live_cascade=%d' % live_cascade,
            'live_verdict=%s' % (doc.get('verdict') or 'none'),
            'naive_map_refused=%d' % naive_refused,
            'safe_map_admitted=%d' % safe_admitted,
            'map_dedupe_live=%d' % dedupe_live,
            'safe_floor=%s' % floor,
            'rev=%s' % rev,
            'freeze=%s' % freeze,
            'C3_R43_PASS=%s' % ('true' if passed else 'false'),
        ]
        print(' '.join(fields))
        return 0 if passed else 1
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
