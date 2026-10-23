#!/usr/bin/env python3
"""c1-measure.py — round-35 C1 counter: does tally-audit-v3 close the routed classes?

Frozen before data (round 35, TameshiR35). One predicate, `C1_R35_PASS`, evaluated over
a panel of runner copies whose ground truth is BEHAVIOR, computed by this counter without
using the tool:

  kill copy   the copy's tally block, run under at least one of the runner's four
              (auto,KEEP) triples, must produce a different (exit, FULL stdout) tuple
              than the pristine block under that same triple; the tool must KILL it
              (rc 1) and the failing check must be `runtime` alone.
  accept copy the copy's block must be behaviorally identical to the pristine block under
              ALL four triples and every vector; the tool must ACCEPT it (rc 0).
  invalid     a kill copy with no behavioral divergence, or an accept copy that diverges,
              or a copy whose edits do not apply exactly `count` times.

The panel is public (`panel/`, committed before the freeze) and sealed (`--sealed DIR`,
authored after the freeze by seats that never see the tool edit; each sealed file's LAST
modifying commit must descend from the freeze revision — the round-34 PanelSeed4 F2
routing: first-add is not enough).

A7 (pre-data, round-35 wave 2): the tally-block locator selects the LAST `local nlegs=` match
and ends at the first depth-0 `}` (a here-doc decoy before the block no longer becomes the
audited span; seat AttackPerIndexParse CRITICAL), and a specimen that reassigns `root` or adds
an `rm -rf` is invalid, never executed for scoring (seat SentinelSandbox CRITICAL).

Modes:
  deciding (default)  tool = tools/tally-audit-v3.py at REV; requires the sealed set
  control             --tool PATH (lane-relative at REV or absolute); never needs sealed
  before              --before: asserts the tool is absent at REV and scores nothing

Counting command (deciding):
  python3 .ufo/evidence/round-35/c1/c1-measure.py --lane LANE --rev REV --work EMPTY_DIR \
      --sealed .ufo/evidence/round-35/c1/sealed

Exit 0 iff the predicate is true. Prints one line per copy and the predicate line.
"""
import argparse
import atexit
import hashlib
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile

PIN_RUNNER = 'a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9'
TOOL_PATH = 'tools/tally-audit-v3.py'
TOOL_SHA256 = '6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354'  # v3 after A7 (final bytes)
# None in the root slot means "the runner's real auto root" (auto_root()); the explicit
# triples keep representative caller-supplied --workdir values, relative and absolute.
# The tool carries the same four triples; the oracle must not import the object it tests,
# so the two lists are kept in lockstep by hand and by the control receipt.
CONFIGS = ((None, '1', '0'), (None, '1', '1'),
           ('tally-audit', '0', '1'), ('/tmp/tally-audit-explicit', '0', '0'))
AUTO_ROOT = [None]
SEP = '\x1f'


def auto_root():
    """The runner's real auto root: root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX).

    mutate-and-run.sh:1357-1365 builds exactly that path when --regression runs without
    --workdir. Fixed literals never equal it, so a copy gated on the real root value
    diverged under the runner's default config while every simulated triple agreed
    (round-35 seat RevengerRootShape CRITICAL). Ground truth must see the real value.
    """
    if AUTO_ROOT[0] is None:
        # runner shape: mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX (six alphanumerics);
        # tempfile.mkdtemp's eight-char suffix escaped a shape-keyed gate (ScoutRunnerConfigs).
        for _ in range(1000):
            cand = '/tmp/tameshi-r4-2-regression.' + ''.join(
                random.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not os.path.exists(cand):
                os.makedirs(cand)
                AUTO_ROOT[0] = cand
                atexit.register(lambda: shutil.rmtree(cand, ignore_errors=True))
                break
        else:
            raise SystemExit('SETUP: cannot allocate a real auto root')
    elif not os.path.isdir(AUTO_ROOT[0]):
        os.makedirs(AUTO_ROOT[0], exist_ok=True)
    return AUTO_ROOT[0]


def cfg_root(cfg):
    return auto_root() if cfg[0] is None else cfg[0]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_show(lane, rev, path):
    p = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout


def git_ok(lane, *args):
    return subprocess.run(['git', '-C', lane] + list(args), capture_output=True).returncode == 0


# ---------------------------------------------------------------- behavior oracle

def code_view(text):
    """Same-length copy with shell comment text blanked (quote-aware)."""
    out = list(text)
    i, n, quote = 0, len(text), None
    while i < n:
        c = text[i]
        if quote == "'":
            if c == "'":
                quote = None
            i += 1
            continue
        if quote == '"':
            if c == '\\' and i + 1 < n:
                i += 2
                continue
            if c == '"':
                quote = None
            i += 1
            continue
        if c == '\\' and i + 1 < n:
            i += 2
            continue
        if c in ("'", '"'):
            quote = c
            i += 1
            continue
        if c == '#' and (i == 0 or text[i - 1] in ' \t\n;|&('):
            j = text.find('\n', i)
            j = n if j < 0 else j
            for k in range(i, j):
                out[k] = ' '
            i = j
            continue
        i += 1
    return ''.join(out)


def tally_block(text):
    """Cut (head, block) from run_regression: head is everything before `local nlegs=`,
    block runs from `local nlegs=` to the function's last brace."""
    cv = code_view(text)
    m = re.search(r'^run_regression\s*\(\)\s*\{[ \t]*\n', cv, re.M)
    if not m:
        raise SystemExit('SETUP: run_regression not found')
    depth, i = 1, m.end()
    while depth > 0 and i < len(cv):
        depth += {'{': 1, '}': -1}.get(cv[i], 0)
        i += 1
    if depth != 0:
        raise SystemExit('SETUP: unbalanced run_regression braces')
    body = text[m.start():i]
    cvb = code_view(body)
    starts = list(re.finditer(r'^[ \t]*local nlegs=', cvb, re.M))
    if not starts:
        raise SystemExit('SETUP: tally start not found')
    if len(starts) != 1:
        # Ambiguity is refused, never guessed: a here-doc decoy before the block wins a
        # first-match rule (seat AttackPerIndexParse) and a dead copy after it wins a
        # last-match rule (seat ReviewAttribution CRITICAL-2).
        raise SystemExit('SETUP: tally start occurs %d times; ambiguous body refused' % len(starts))
    start = starts[0].start()
    depth, end = 0, -1
    for i in range(start, len(cvb)):
        c = cvb[i]
        if c == '{':
            depth += 1
        elif c == '}':
            if depth == 0:
                end = i
                break
            depth -= 1
    if end < start:
        raise SystemExit('SETUP: tally end not found')
    return body[:start], body[start:end]


ASSIGN_RE = re.compile(r'^[ \t]*(st_[A-Za-z0-9_]+)=\$\?[ \t]*$', re.M)


def leg_names(head):
    return ASSIGN_RE.findall(code_view(head))


def run_block(block, names, vectors, cfg, tmp):
    """Run every vector in one bash process; return [(exit, FULL stdout)] in order."""
    root_s, auto_s, keep_s = cfg_root(cfg), cfg[1], cfg[2]
    decl = ' '.join('%s=${%d}' % (n, i + 1) for i, n in enumerate(names))
    lines = ['set -u -o pipefail', 'tally() {', '  local ' + decl,
             "  local root=%s auto=%s KEEP=%s" % (root_s, auto_s, keep_s),
             block.rstrip('\n'), '}']
    for v in vectors:
        lines.append('out=$(tally ' + ' '.join(str(s) for s in v) + ' 2>/dev/null); rc=$?; '
                     "printf 'R\\t%s\\t%s\\n' \"$rc\" \"${out//$'\\n'/$'\\x1f'}\"")
    path = os.path.join(tmp, 'b%d.sh' % len(os.listdir(tmp)))
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp}
    p = subprocess.run(['bash', path], cwd=tmp, env=env, capture_output=True, timeout=300)
    got = []
    for ln in p.stdout.decode('utf-8', 'replace').split('\n'):
        if ln.startswith('R\t'):
            parts = ln.split('\t', 2)
            got.append((int(parts[1]), parts[2].replace('\x1f', '\n')))
    if p.returncode != 0 or len(got) != len(vectors):
        raise SystemExit('SETUP: block driver failed (exit %s, %d/%d): %s'
                         % (p.returncode, len(got), len(vectors),
                            p.stderr.decode('utf-8', 'replace')[:300]))
    return got


def vectors_for(n):
    vs = [[0] * n]
    for s in range(0, 256):
        v = [0] * n
        v[0] = s
        vs.append(v)
    for v in ([1] + [0] * (n - 1), [2] + [0] * (n - 1), [1, 2] + [0] * (n - 2),
              [0, 1] + [0] * (n - 2), [0, 2] + [0] * (n - 2), [1] * n, [2] * n,
              [3] + [0] * (n - 1), [255] + [0] * (n - 1), [0] * (n - 1) + [1]):
        if len(v) == n:
            vs.append(v)
    return vs


def behavior(text, tmp):
    head, block = tally_block(text)
    names = leg_names(head)
    if not names:
        raise SystemExit('SETUP: no leg assignments found in the copy')
    vs = vectors_for(len(names))
    out = {}
    for cfg in CONFIGS:
        out[cfg] = run_block(block, names, vs, cfg, tmp)
    return out


def diverge(a, b):
    return [cfg for cfg in CONFIGS if a[cfg] != b[cfg]]


# ---------------------------------------------------------------- panel

def _docs_to_copies(docs):
    copies = []
    for fn, doc in docs:
        if 'copies' in doc and isinstance(doc['copies'], list):
            for c in doc['copies']:
                c.setdefault('file', fn)
                copies.append(c)
        else:
            doc.setdefault('file', fn)
            copies.append(doc)
    return copies


def load_copies(directory):
    """Panel copies from disk (public panel only; the sealed set is read at REV)."""
    docs = []
    if not os.path.isdir(directory):
        return []
    for fn in sorted(os.listdir(directory)):
        if not fn.endswith('.json') or fn == 'manifest.json':
            continue
        with open(os.path.join(directory, fn), encoding='utf-8') as f:
            docs.append((fn, json.load(f)))
    return _docs_to_copies(docs)


def load_copies_rev(lane, rev, reldir):
    """Copies from COMMITTED bytes at REV (round-35 seat ReviewSealedGate BOUND-4: the
    provenance gate reads history while the scorer read the working tree, so an
    uncommitted edit passed the gate and was scored anyway). `manifest.json` is a
    manifest, never a specimen (HYGIENE-1)."""
    p = subprocess.run(['git', '-C', lane, 'ls-tree', '-r', '--name-only', rev, '--', reldir],
                       capture_output=True)
    names = [n for n in p.stdout.decode('utf-8', 'replace').split('\n')
             if n.endswith('.json') and os.path.basename(n) != 'manifest.json']
    docs = []
    for name in sorted(names):
        raw = git_show(lane, rev, name)
        if raw is None:
            continue
        docs.append((os.path.basename(name), json.loads(raw.decode('utf-8'))))
    return _docs_to_copies(docs)


def apply_edits(text, edits):
    out = text
    for old, new, cnt in edits:
        got = out.count(old)
        if got != cnt:
            return None, 'edit %r applies %d times, want %d' % (old[:40], got, cnt)
        out = out.replace(old, new)
    return out, None


def run_tool(tool_path, runner_copy, tmp):
    p = subprocess.run([sys.executable, tool_path, '--runner', runner_copy],
                       capture_output=True, timeout=1800)
    out = p.stdout.decode('utf-8', 'replace')
    failed = re.findall(r'^CHECK (\w+) FAIL', out, re.M)
    last = [ln for ln in out.splitlines() if ln.startswith('TALLY_AUDIT:')]
    return p.returncode, failed, (last[-1] if last else out.strip()[-120:]), out


def unsafe_block(block):
    """Fail-closed filesystem-safety gate on specimen text (round-35 wave-2 seat SentinelSandbox).

    The counter RUNS specimen-derived bash. A copy that reassigns `root` or adds another
    `rm -rf` can delete a path outside --work through the block's own cleanup line, while
    returning a valid tuple. Such a copy is not scored: it is invalid with this reason.
    """
    cv = code_view(block)
    if re.search(r'^[ \t]*root=', cv, re.M):
        return 'specimen reassigns root (filesystem-safety gate)'
    # The harness-provided $root is disposable; any other rm target is not. A legitimate
    # behavioral copy may add another `rm -rf "$root"` (workdir-cleanup classes).
    for m in re.finditer(r'\brm\b[^\n;]*', cv):
        seg = m.group(0)
        if '"$root"' not in seg and "'$root'" not in seg and '$root' not in seg:
            return 'specimen removes a path other than $root (filesystem-safety gate)'
    return None


def score_copies(copies, runner_text, tool_path, tmp):
    rows = []
    for c in copies:
        copy_text, err = apply_edits(runner_text, [tuple(e) for e in c['edits']])
        row = {'class': c.get('class', '?'), 'set': c['set'], 'file': c.get('file', '?')}
        if err:
            row.update(valid=False, why=err)
            rows.append(row)
            continue
        try:
            bad = unsafe_block(tally_block(copy_text)[1])
        except SystemExit as e:
            row.update(valid=False, why='block extraction refused: %s' % str(e)[:120])
            rows.append(row)
            print('COPY %-5s %-34s %s INVALID (extraction refused)' % (row['set'], row['class'], row['file']))
            continue
        if bad:
            row.update(valid=False, why=bad)
            rows.append(row)
            print('UNSAFE %-5s %-34s %s' % (row['set'], row['class'], bad))
            continue
        bdir = os.path.join(tmp, 'b%d' % len(os.listdir(tmp)))
        os.mkdir(bdir)
        try:
            copy_beh = behavior(copy_text, bdir)
            pristine_beh = behavior(runner_text, bdir)
        except SystemExit as e:
            # A copy whose extracted block cannot even be driven (quote-blind brace fence,
            # legal in bash: `: '}'` before the closer) is INVALID, never a counter crash
            # (round-35 wave-2 seat ScoutTailRegion BOUND-3).
            row.update(valid=False, why='block driver refused: %s' % str(e)[:120])
            rows.append(row)
            print('COPY %-5s %-34s %s INVALID (driver refused)' % (row['set'], row['class'], row['file']))
            continue
        div = diverge(pristine_beh, copy_beh)
        row['diverged_configs'] = ['(%s,%s)' % (c_[1], c_[2]) for c_ in div]
        rpath = os.path.join(tmp, 'copy%d.sh' % len(os.listdir(tmp)))
        with open(rpath, 'w', encoding='utf-8') as f:
            f.write(copy_text)
        rc, failed, last, _ = run_tool(tool_path, rpath, tmp)
        row.update(rc=rc, failed_checks=failed, last=last)
        if c['set'] == 'kill':
            row['valid'] = bool(div)
            row['pass'] = bool(div) and rc == 1 and failed == ['runtime']
        else:
            row['valid'] = not div
            row['pass'] = (not div) and rc == 0
        rows.append(row)
        print('COPY %-5s %-34s %s div=%s rc=%s checks=%s pass=%s'
              % (row['set'], row['class'], row['file'], ','.join(row['diverged_configs']) or '-',
                 rc, ','.join(failed) or '-', row['pass']))
        if not row['valid']:
            print('  INVALID: %s' % ('kill copy without behavioral divergence' if c['set'] == 'kill'
                                     else 'accept copy that diverges: %s' % row['diverged_configs']))
    return rows


def distinct_bodies(copies, runner_text):
    seen = set()
    for c in copies:
        t, err = apply_edits(runner_text, [tuple(e) for e in c['edits']])
        seen.add(sha256((t if t is not None else c['file']).encode()))
    return len(seen)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--rev', required=True)
    ap.add_argument('--work', required=True)
    ap.add_argument('--sealed')
    ap.add_argument('--tool')
    ap.add_argument('--before', action='store_true')
    a = ap.parse_args()

    lane = os.path.abspath(a.lane)
    rev = subprocess.run(['git', '-C', lane, 'rev-parse', a.rev], capture_output=True).stdout.decode().strip()
    if not rev:
        print('C1_R35: SETUP rev_unresolved=%s' % a.rev)
        return 2
    if os.listdir(a.work):
        print('C1_R35: SETUP work_not_empty=%s' % a.work)
        return 2
    tmp = os.path.abspath(a.work)

    runner_bytes = git_show(lane, rev, 'tools/mutate-and-run.sh')
    if runner_bytes is None:
        print('C1_R35: SETUP runner_missing_at_rev')
        return 2
    runner_text = runner_bytes.decode('utf-8')
    runner_ok = sha256(runner_bytes) == PIN_RUNNER

    tool_bytes = git_show(lane, rev, TOOL_PATH)
    tool_present = tool_bytes is not None
    if a.before:
        print('C1_R35: mode=before tool_present=%d runner_sha_ok=%d rev=%s C1_R35_PASS=false'
              % (tool_present, runner_ok, rev))
        return 1

    label = 'C1_R35'
    if a.tool:
        label = 'C1_R35_CONTROL'
        if os.path.isabs(a.tool):
            tool_bytes = open(a.tool, 'rb').read()
        else:
            tool_bytes = git_show(lane, rev, a.tool)
        tool_present = tool_bytes is not None
    tool_sha = sha256(tool_bytes) if tool_bytes is not None else '-'
    tool_sha_ok = tool_bytes is not None and (a.tool is not None or tool_sha == TOOL_SHA256)

    tool_file = os.path.join(tmp, 'tool.py')
    if tool_bytes is not None:
        with open(tool_file, 'wb') as f:
            f.write(tool_bytes)

    pub = load_copies_rev(lane, rev, '.ufo/evidence/round-35/c1/panel')
    pub_kill_slots = sum(1 for c in pub if c['set'] == 'kill')
    pub_accept_slots = sum(1 for c in pub if c['set'] == 'accept')
    pub_distinct = distinct_bodies(pub, runner_text)

    results = {'pub': [], 'ho': []}
    if tool_bytes is not None:
        results['pub'] = score_copies(pub, runner_text, tool_file, tmp)
    else:
        results['pub'] = [{'set': c['set'], 'class': c.get('class', '?'), 'pass': False, 'valid': True}
                          for c in pub]

    sealed_ok = True
    ho_kill_total = ho_accept_total = 0
    ho_distinct = 0
    if a.sealed:
        sdir = a.sealed if os.path.isabs(a.sealed) else os.path.join(lane, a.sealed)
        srel = os.path.relpath(os.path.abspath(sdir), lane).replace(os.sep, '/')
        ho = load_copies_rev(lane, rev, srel)
        mbytes = git_show(lane, rev, srel + '/manifest.json')
        manifest = json.loads(mbytes.decode('utf-8')) if mbytes is not None else None
        # The freeze is not self-declared (ReviewSealedGate BOUND-1): it is the commit that
        # first added the contract, read from history at REV, and the manifest must name it.
        first = subprocess.run(['git', '-C', lane, 'log', rev, '--diff-filter=A', '-1', '--format=%H',
                                '--', '.ufo/evidence/round-35/contract.json'],
                               capture_output=True).stdout.decode().strip()
        declared = (manifest or {}).get('freeze_rev', '')
        sealed_ok = (manifest is not None and bool(first) and declared == first
                     and rev != first and git_ok(lane, 'merge-base', '--is-ancestor', first, rev))
        if not sealed_ok:
            print('SEALED-FREEZE-FAIL manifest=%s contract_first_add=%s rev=%s'
                  % (declared[:12] or '-', first[:12] or '-', rev[:12]))
        for c in ho:
            fpath = '%s/%s' % (srel, c['file'])
            # Strict ancestry (BOUND-3: equality accepted a copy committed in the freeze itself)
            # and lineage creation (BOUND-2: a move into sealed/ would otherwise pass as a touch).
            last = subprocess.run(['git', '-C', lane, 'log', rev, '-1', '--format=%H', '--', fpath],
                                  capture_output=True).stdout.decode().strip()
            origin = subprocess.run(['git', '-C', lane, 'log', rev, '--follow', '--diff-filter=A', '-1',
                                     '--format=%H', '--', fpath],
                                    capture_output=True).stdout.decode().strip()
            if (not last or last == first or not git_ok(lane, 'merge-base', '--is-ancestor', first, last)
                    or not git_ok(lane, 'merge-base', '--is-ancestor', last, rev)
                    or not origin or not git_ok(lane, 'merge-base', '--is-ancestor', first, origin)):
                sealed_ok = False
                print('SEALED-PROVENANCE-FAIL %s last=%s origin=%s freeze=%s'
                      % (c['file'], last[:12] or '-', origin[:12] or '-', first[:12] or '-'))
        if not ho:
            sealed_ok = False
            print('SEALED-SET-EMPTY %s' % srel)
        ho_kill_total = sum(1 for c in ho if c['set'] == 'kill')
        ho_accept_total = sum(1 for c in ho if c['set'] == 'accept')
        ho_distinct = distinct_bodies(ho, runner_text)
        results['ho'] = score_copies(ho, runner_text, tool_file, tmp) if tool_bytes is not None else []

    def counted(rows, s):
        return sum(1 for r in rows if r.get('set') == s and r.get('pass'))

    pub_kill = counted(results['pub'], 'kill')
    pub_accept = counted(results['pub'], 'accept')
    ho_kill = counted(results['ho'], 'kill')
    ho_accept = counted(results['ho'], 'accept')
    ho_invalid = sum(1 for r in results['ho'] if not r.get('valid', False))

    ok = (runner_ok and tool_present and tool_sha_ok
          and pub_kill == pub_kill_slots and pub_accept == pub_accept_slots
          and ho_kill_total >= 4 and ho_accept_total >= 2
          and ho_kill == ho_kill_total and ho_accept == ho_accept_total
          and ho_invalid == 0 and sealed_ok)

    print('%s: mode=%s tool_present=%d tool_sha=%s tool_sha_ok=%d runner_sha_ok=%d '
          'pub_kill=%d/%d pub_accept=%d/%d pub_slots=%d pub_distinct=%d '
          'ho_kill=%d/%d ho_accept=%d/%d ho_invalid=%d ho_distinct=%d sealed_after_freeze=%d '
          'rev=%s %s_PASS=%s'
          % (label, 'control' if a.tool else 'deciding', tool_present, tool_sha[:16], tool_sha_ok,
             runner_ok, pub_kill, pub_kill_slots, pub_accept, pub_accept_slots,
             pub_kill_slots + pub_accept_slots, pub_distinct,
             ho_kill, ho_kill_total, ho_accept, ho_accept_total, ho_invalid, ho_distinct,
             int(sealed_ok), rev, label, 'true' if ok else 'false'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
