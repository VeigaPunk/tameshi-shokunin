#!/usr/bin/env python3
"""tally-audit-v3.py — audit the mutation runner's --regression tally (round 35 successor).

Usage:
  python3 tools/tally-audit-v3.py [--runner PATH]      audit (default: tools/mutate-and-run.sh beside this file)
  python3 tools/tally-audit-v3.py --runner PATH --then-regression [--workdir DIR]
                                                       audit; only on PASS run `bash PATH --regression` under a
                                                       timeout, then check its REGRESSION line names cases=<legs>
  python3 tools/tally-audit-v3.py --selftest           show every check able to fail on seeded faults

Round 35 (tameshi), routed from the round-34 wave's eight-seat convergent Holds:

  1. Config sweep completed. The runtime oracle ran the tally block under only two of the
     runner's four (auto,KEEP) triples — (0,1) and (1,0). (0,0) and (1,1) are real runner
     states (explicit --workdir, --keep) and were UNSWEPT: a tally arm gated on
     `auto == 0 && KEEP == 0` (or on both being 1) passed the audit while changing the
     runner's verdict under that config (round-34 seat Mutkillvectorarmswap F3 — the one
     accept-side hole that was not fail-closed). All four triples now run.
  2. Whole-stdout comparison. The oracle compared the first stdout line and the exit code
     only, so a defect confined to the REGRESSION_WORKDIR line (the runner's kept/removed
     contract, which also decides whether the workdir is deleted) was accepted. The full
     stdout of the tally block is now compared, under every config.
  3. Comment-blind scanning. The twice-only head rule counted NAME SUBSTRINGS, so an inert
     comment naming a leg was KILLED (round-34: the single most-confirmed false-kill class);
     `regression_body` counted braces char-wise, so a `}` in a comment closed the body early;
     and `esac`/`do` in a comment seized the case/loop locators, refusing a pristine copy as
     SETUP. All structural scans now run on a quote-aware code view in which shell comment
     text is blanked (same length, newlines kept), so offsets and slices are unchanged.
     Source: S102 (POSIX.1-2024 §2.3 Token Recognition — a `#` at the start of a token
     discards it and everything up to, excluding, the next newline as a comment, so comment
     text is never code) and S097 (the status range and `case` first-match semantics the
     oracle sweeps).
  4. Real auto-root witness. The four triples were driven with fixed root literals, but the
     runner's real auto root is `$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)`
     (mutate-and-run.sh:1357-1365); a copy gated on that value masked a failing leg into a
     PASS under the runner's default config while every simulated triple agreed, and this
     audit ACCEPTED it (round-35 seat RevengerRootShape CRITICAL). The auto triples now run
     with a real directory carrying the runner's own prefix.

Every round-34 check is retained unchanged in intent; the three fixes only tighten or
de-blind them. The runner is never edited.

Round 33 (tameshi). Round 32's `tally-audit.py` (frozen as the round-32 measured object) was
defeated by a sealed held-out set of runner copies (`.ufo/evidence/round-32/heldout/`). The four
missed classes, and this tool's answer to each:

  1. Runtime vectors never produced 3-8 failing or setup legs (HeldOutPrintf-1/-2 count-field
     swaps, HeldOutGuard-1/-2 majority-gated FAIL, HeldOutTallyArms-01/-02 conditional double
     count). -> the runtime oracle now sweeps EVERY (failing-count, setup-count) pair 0..9 with
     failing+setup <= nlegs, representative placements, plus all-status extremes.
  2. Per-position statuses stopped at {1 2 3 4 126 127 255} (HeldOutRefactor-k1 status 5 at one
     position; HeldOutLoop-1 masked a status to seven bits, witness 128). -> EVERY status 0..255
     at EVERY leg position, not only position 0.
  3. The stress rewrote the first leg-status-named loop instead of the tally loop, so runner copies
     with an auxiliary loop were false-rejected (HeldOutLoop-3 wrapper, HeldOutRefactor-a4
     pre-count loop). -> the tally loop is identified by dataflow: the INNERMOST `for` whose body
     contains the `case` arm that increments the tally counters (npass/nfail/nsetup), never the
     first loop whose operands look like leg statuses. Only that loop is stressed.
  4. The harness check required exactly one `tblock=$(awk ...)` extraction line and refused
     (exit 2) a copy with a second, equivalent extraction (HeldOutRefactor-a3). -> >= 1 extraction
     lines are accepted; the injectable reference is spliced after the LAST one.

Also routed from the round-32 tool review: comparisons are stdout-only (stderr is captured
separately, never into the compared string), and `--then-regression` runs under a timeout.

Checks (each independent, each able to fail alone):
  head     per-leg presence upstream of the tally: every leg var is assigned exactly once, as a
           bare `st_x=$?`, in run_regression before the tally block; no other assignment to a leg
           var appears outside the identified tally loop's operand list. Catches out-of-block
           masking/overwrites of leg statuses.
  static   the identified tally loop's operands equal the head's leg assignments as multisets and
           `local nlegs=N` equals the leg count. A sum-preserving miscount passes the runner's
           own run-time guard; it fails here.
  runtime  the runner's tally block, run in bash, against an independent oracle: every status
           0..255 at every position, every (failing, setup) count pair 0..9, multi-status vectors,
           and stress with one operand duplicated (overcount) or removed (undercount) at every
           position of the IDENTIFIED tally loop. Exact stdout first line and exit code compared.
  harness  the runner's own tally selftest harness run against a panel of known-faulty tally
           blocks built from the pinned reference block; it must accept the reference block and
           reject every fault. A weakened harness (exit only, swallowed status, a skipped position
           or vector, a skipped guard stress) accepts at least one fault.

Prints one `CHECK <name> PASS|FAIL ...` line per check and a final
`TALLY_AUDIT: PASS|FAIL (head=.. static=.. runtime=.. harness=..)`. Exit 0 PASS, 1 FAIL,
2 cannot audit. The runner is never edited.
"""
import argparse
import atexit
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TIMEOUT = 120
THEN_REGRESSION_TIMEOUT = 1200

REF_BLOCK = r'''  local nlegs=9 npass=0 nfail=0 nsetup=0 st
  for st in "$st_js" "$st_kagi" "$st_tsu" "$st_mado" "$st_checklist" "$st_claims" "$st_roundgate" "$st_sourcescheck" "$st_citecheck"; do
    case $st in
      0) npass=$((npass + 1)) ;;
      1) nfail=$((nfail + 1)) ;;
      *) nsetup=$((nsetup + 1)) ;;
    esac
  done

  if [[ $nfail -gt 0 ]]; then
    printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
      "$nlegs" "$npass" "$nfail" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 1
  fi
  if [[ $nsetup -gt 0 ]]; then
    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
      "$nlegs" "$npass" "$nsetup"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  # r30: tally completeness (round-29 routed leg-sum defect). A PASS needs every one of the
  # nlegs statuses counted; counts that do not sum to nlegs refuse as SETUP (S087: the totals
  # of a mutation report are sums of its per-state counts).
  if (( npass + nfail + nsetup != nlegs )); then
    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
      "$nlegs" "$((npass + nfail + nsetup))"
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
    exit 2
  fi
  printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
    "$nlegs" "$npass"
  if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then
    printf 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)\n' "$root"
    rm -rf "$root"
  else
    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
  fi
  exit 0
'''
REF_NAMES = ['st_js', 'st_kagi', 'st_tsu', 'st_mado', 'st_checklist', 'st_claims', 'st_roundgate',
             'st_sourcescheck', 'st_citecheck']


class CannotAudit(Exception):
    pass


# ---------------------------------------------------------------- parsing

def code_view(text):
    """Same-length copy of `text` with shell comment text replaced by spaces.

    A `#` starts a comment only at the start of a word — at the beginning of the text or
    after whitespace or one of `;|&(` — and only outside single quotes, double quotes and
    backslash escapes; inside them it is literal data (POSIX shell lexical rules). Newlines
    are preserved, so line-anchored regexes still match at the same offsets and every slice
    taken from this view indexes the original text. Structural scans (brace counting, head
    token counting, case/loop locators) run on this view so inert comment text cannot kill
    or refuse a behaviorally pristine copy (round 35; round-34 false-kill class)."""
    out = list(text)
    i, n = 0, len(text)
    quote = None
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
        if c == "'" or c == '"':
            quote = c
            i += 1
            continue
        if c == '#' and (i == 0 or text[i - 1] in ' \t\n;|&('):
            j = text.find('\n', i)
            if j < 0:
                j = n
            for k in range(i, j):
                out[k] = ' '
            i = j
            continue
        i += 1
    return ''.join(out)

def regression_body(text):
    cv = code_view(text)
    hits = list(re.finditer(r'^run_regression\s*\(\)\s*\{[ \t]*\n', cv, re.M))
    if not hits:
        raise CannotAudit('run_regression() not found')
    if len(hits) != 1:
        # bash runs the LAST definition; a first-match extractor audits the shadowed one
        # (wave-2 seat ReviewAttribution CRITICAL-3). Refuse the ambiguity.
        raise CannotAudit('run_regression() defined %d times; shadowed definition refused' % len(hits))
    m = hits[0]
    depth = 1
    i = m.end()
    while depth > 0 and i < len(cv):
        c = cv[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        i += 1
    if depth != 0:
        raise CannotAudit('run_regression() has unbalanced braces')
    return text[m.start():i]


def brace_depth_at(text, offset):
    """brace nesting depth at offset, counting from the run_regression opening brace (depth 1 inside it)."""
    depth = 0
    for ch in text[:offset]:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
    return depth


START_RE = re.compile(r'^[ \t]*local nlegs=', re.M)


def _tally_start(cv):
    """The LAST `local nlegs=` in the body.

    A here-doc DECOY before the real tally can carry a byte-copy of the pristine tally
    block; the first-match extractor then audits the decoy (campaign round 35, wave-2 seat
    AttackPerIndexParse CRITICAL: the tool accepted a runner whose real block masked status
    4 into PASS). The runner has exactly one such line in its function, so the last match is
    the real block.
    """
    ms = list(START_RE.finditer(cv))
    if not ms:
        raise CannotAudit('tally start `local nlegs=` not found')
    if len(ms) != 1:
        # Uniqueness, not order: a decoy BEFORE the block (here-doc data) and a dead copy
        # AFTER it (wave-2 seat ReviewAttribution CRITICAL-2) both win a last/first-match
        # rule in one direction. An ambiguous body is refused, never guessed.
        raise CannotAudit('tally start `local nlegs=` occurs %d times; ambiguous body refused' % len(ms))
    return ms[0].start()


def _block_end(cv, start):
    """Index of the first depth-0 `}` at or after start (the enclosing function's close).

    `rfind('}')` scans the whole body, so a decoy AFTER the real block moves the end past
    it; brace depth from the chosen start cannot be moved by text outside the block.
    """
    depth = 0
    for i in range(start, len(cv)):
        c = cv[i]
        if c == '{':
            depth += 1
        elif c == '}':
            if depth == 0:
                return i
            depth -= 1
    return -1


def tally_block(body):
    cv = code_view(body)
    start = _tally_start(cv)
    end = _block_end(cv, start)
    if end < start:
        raise CannotAudit('tally block end not found')
    return body[start:end]


def head_section(body):
    cv = code_view(body)
    return body[:_tally_start(cv)]


ASSIGN_RE = re.compile(r'^[ \t]*(st_[A-Za-z0-9_]+)=\$\?[ \t]*$', re.M)


def leg_names(head):
    return ASSIGN_RE.findall(code_view(head))


# `for VAR in OPERANDS; do` or `... \n do`, OPERANDS possibly continued with backslash-newline.
LOOP_RE = re.compile(r'^([ \t]*for[ \t]+([A-Za-z_][A-Za-z0-9_]*)[ \t]+in[ \t]+)((?:[^;\n\\]|\\\n)*?)([ \t]*(?:;[ \t]*|\n[ \t]*)do\b)', re.M)
WLOOP_RE = re.compile(r'^[ \t]*(while|until)[ \t]+.*?([ \t]*(?:;[ \t]*|\n[ \t]*)do\b)', re.M)
OPERAND_RE = re.compile(r'"?\$\{?(st_[A-Za-z0-9_]+)\}?"?')
CASE_RE = re.compile(r'case[ \t]+\$([A-Za-z_][A-Za-z0-9_]*)[ \t]+in\b')
COUNTER_INC_RE = re.compile(r'\b(npass|nfail|nsetup)=\$\(\(')
DONE_RE = re.compile(r'^[ \t]*done[ \t]*$', re.M)


def loop_extent(block, m):
    """[start, end) span of the loop matched by m: from its header to the line holding its `done`."""
    d = DONE_RE.search(block, m.end())
    if not d:
        raise CannotAudit('loop has no done')
    return m.start(), d.end()


def counting_case(block):
    """The `case $VAR in` whose arms increment the tally counters; returns (match, var)."""
    cv = code_view(block)
    for m in CASE_RE.finditer(cv):
        tail = cv[m.end():m.end() + 400]
        body_end = tail.find('esac')
        seg = tail[:body_end] if body_end >= 0 else tail
        if len(COUNTER_INC_RE.findall(seg)) >= 2:
            return m, m.group(1)
    raise CannotAudit('counting `case $VAR in` not found')


def tally_loop(block):
    """The loop that governs the counting case, identified by dataflow (never operand shape).

    Auxiliary loops (pre-counts, single-leg wrappers) may enclose or precede the real tally loop;
    only the loop whose body contains the counting case is stressed. `for` loops supply their
    operand list; renamed loop variables are accepted when the case variable matches the loop
    variable. `while`/`until` traversals are accepted: their operand order is taken from the head's
    leg assignments (the runtime oracle still sweeps every status vector, and the sum-guard is
    exercised by the count-pair vectors; operand stress is skipped for them by construction)."""
    cv = code_view(block)
    case_m, case_var = counting_case(block)
    cands = []
    for m in LOOP_RE.finditer(cv):
        start, end = loop_extent(cv, m)
        if start < case_m.start() < end and m.group(2) == case_var:
            body_slice = cv[m.end():end]
            if COUNTER_INC_RE.search(body_slice):
                cands.append(('for', m))
    for m in WLOOP_RE.finditer(cv):
        start, end = loop_extent(cv, m)
        if start < case_m.start() < end:
            body_slice = cv[m.end():end]
            if COUNTER_INC_RE.search(body_slice):
                cands.append((m.group(1), m))
    if not cands:
        raise CannotAudit('no loop governing the counting case')
    kind, m = max(cands, key=lambda km: km[1].start())
    if kind == 'for':
        toks = m.group(3).replace('\\\n', ' ').split()
        ops = []
        for t in toks:
            mm = OPERAND_RE.fullmatch(t)
            if not mm:
                raise CannotAudit('tally loop operand not a leg status: %r' % t)
            ops.append(mm.group(1))
        if not ops:
            raise CannotAudit('tally loop has no operands')
        return m, ops, kind
    return m, None, kind


def loop_operands(block):
    return tally_loop(block)[1]


def with_operands(block, ops):
    m = tally_loop(block)[0]
    return block[:m.start(3)] + ' '.join('"$%s"' % o for o in ops) + block[m.end(3):]


# ---------------------------------------------------------------- bash runs

def bash(script, tmp):
    path = os.path.join(tmp, 'p%d.sh' % len(os.listdir(tmp)))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(script)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp}
    try:
        p = subprocess.run(['bash', path], cwd=tmp, env=env, capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        raise CannotAudit('bash run timed out after %ds' % TIMEOUT)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), p.stderr.decode('utf-8', 'replace')


# None in the root slot means "the runner's real auto root" (see auto_root()); the explicit
# triples keep representative caller-supplied --workdir values, relative and absolute.
CONFIGS = ((None, '1', '0'), (None, '1', '1'),
           ('tally-audit', '0', '1'), ('/tmp/tally-audit-explicit', '0', '0'))
AUTO_ROOT = [None]


def auto_root():
    """The runner's real auto root: root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX).

    mutate-and-run.sh:1357-1365 builds exactly that path when --regression runs without
    --workdir. Fixed literals can never equal it, so a copy gated on the real root value
    diverged under the runner's default config while every simulated triple agreed and the
    audit ACCEPTED it (round-35 seat RevengerRootShape CRITICAL). The auto triples now
    carry a real directory with the runner's own prefix; the compared stdout carries the
    value, not the directory's contents.
    """
    if AUTO_ROOT[0] is None:
        # The runner's mktemp template is SIX alphanumerics (XXXXXX); tempfile.mkdtemp makes
        # EIGHT from a-z0-9_, so a gate on the exact suffix shape escaped the A4 witness
        # (round-35 wave-2 seat ScoutRunnerConfigs CRITICAL). Generate the real shape.
        for _ in range(1000):
            cand = '/tmp/tameshi-r4-2-regression.' + ''.join(
                random.choice(string.ascii_letters + string.digits) for _ in range(6))
            if not os.path.exists(cand):
                os.makedirs(cand)
                AUTO_ROOT[0] = cand
                atexit.register(lambda: shutil.rmtree(cand, ignore_errors=True))
                break
        else:
            raise CannotAudit('cannot allocate a real auto root')
    elif not os.path.isdir(AUTO_ROOT[0]):
        os.makedirs(AUTO_ROOT[0], exist_ok=True)
    return AUTO_ROOT[0]


def cfg_root(cfg):
    return auto_root() if cfg[0] is None else cfg[0]


def run_vectors(block, names, vectors, tmp, cfg=CONFIGS[0]):
    """Run the tally block once per status vector in one bash process; return [(rc, stdout first line)].

    stdout-only: stderr goes to a side file, never into the compared string (round-32 tool review M1).
    cfg is the (root, auto, KEEP) triple the driver pins: config (0,1) is the audit's hermetic triple;
    config (1,0) is the runner's real --regression default (auto-workdir under /tmp, rm-on-PASS);
    (0,0) is an explicit --workdir without --keep and (1,1) is an auto workdir with --keep. A guard
    weakened by a conjunct over $auto/$KEEP/$root behaves identically under one config and diverges under
    another (DevGuard round 33; the (0,0)/(1,1) hole found by round-34 seat Mutkillvectorarmswap F3):
    the sweep must run under all four, and compare the FULL stdout (round 35), because the
    REGRESSION_WORKDIR line differs by config and a defect may be confined to it."""
    root_s, auto_s, keep_s = cfg_root(cfg), cfg[1], cfg[2]
    decl = ' '.join('%s=${%d}' % (n, i + 1) for i, n in enumerate(names))
    lines = ['set -u -o pipefail', 'tally() {', '  local ' + decl,
             "  local root=%s auto=%s KEEP=%s" % (root_s, auto_s, keep_s), block.rstrip('\n'), '}']
    for i, v in enumerate(vectors):
        lines.append('out=$(tally %s 2>"$TMPDIR/stderr.%d"); rc=$?; printf "R\\t%%s\\t%%s\\n" "$rc" "${out//$\'\\n\'/$\'\\x1f\'}"'
                     % (' '.join(str(s) for s in v), i))
    rc, out, err = bash('\n'.join(lines) + '\n', tmp)
    got = [ln.split('\t', 2) for ln in out.split('\n') if ln.startswith('R\t')]
    if rc != 0 or len(got) != len(vectors):
        raise CannotAudit('tally driver failed (exit %s, %d/%d results): %s' % (rc, len(got), len(vectors), err[:200]))
    return [(int(g[1]), (g[2] if len(g) > 2 else '').replace('\x1f', '\n')) for g in got]


def oracle(statuses_by_leg, counted_ops, nlegs, cfg=CONFIGS[0]):
    """Expected (exit, FULL stdout) for one run under one config.

    Full stdout, not the first line (round 35): the runner prints a second
    REGRESSION_WORKDIR line whose wording and whose rm decision both depend on the
    (auto,KEEP) triple, so a defect confined to that line was invisible to a
    first-line comparison (round-34 hold: whole-stdout comparison OPEN)."""
    root_s, auto_s, keep_s = cfg_root(cfg), cfg[1], cfg[2]
    kept = 'REGRESSION_WORKDIR: %s (kept)' % root_s
    removed = 'REGRESSION_WORKDIR: %s (removed on PASS; --keep retains)' % root_s
    vals = [statuses_by_leg[o] for o in counted_ops]
    p = sum(1 for s in vals if s == 0)
    f = sum(1 for s in vals if s == 1)
    s_ = len(vals) - p - f
    if f:
        return 1, 'REGRESSION: FAIL (cases=%d passed=%d failed=%d setup=%d)\n%s' % (nlegs, p, f, s_, kept)
    if s_:
        return 2, 'REGRESSION: SETUP (cases=%d passed=%d cannot-verify=%d)\n%s' % (nlegs, p, s_, kept)
    if p != nlegs:
        return 2, 'REGRESSION: SETUP (case-tally mismatch: cases=%d counted=%d)\n%s' % (nlegs, p + f + s_, kept)
    line = 'REGRESSION: PASS (cases=%d passed=%d; ledger legs exact: killed-delta<=0 flips<=0)' % (nlegs, p)
    return 0, line + '\n' + (removed if (auto_s == '1' and keep_s == '0') else kept)


def show(t):
    """A one-line rendering of a (exit, stdout) tuple for failure messages."""
    return '%s %r' % (t[0], t[1].replace('\n', ' | '))


# ---------------------------------------------------------------- checks

def check_head(body, block, names):
    head = head_section(body)
    head_code = code_view(head)  # comment text is data, never a leg occurrence (round 35)
    block_code = code_view(block)
    all_assigns = re.findall(r'^[ \t]*(st_[A-Za-z0-9_]+)=', head_code, re.M)
    bare = ASSIGN_RE.findall(head_code)
    problems = []
    if not all_assigns:
        problems.append('no st_* leg assignments before the tally block')
    # any leg assignment that is not a bare `st_x=$?` masks or overwrites the leg status
    nonbare = []
    for m in re.finditer(r'^[ \t]*(st_[A-Za-z0-9_]+)=(.*)$', head_code, re.M):
        if not re.fullmatch(r'\$\?', m.group(2).strip()):
            nonbare.append('%s=%s' % (m.group(1), m.group(2).strip()[:30]))
    if nonbare:
        problems.append('non-bare leg assignment(s) in the head: %s' % '; '.join(nombre for nombre in nonbare))
    for nm in set(all_assigns):
        if all_assigns.count(nm) != 1:
            problems.append('leg %s assigned %d times in the head' % (nm, all_assigns.count(nm)))
    if sorted(bare) != sorted(names):
        problems.append('head bare assignments %s != tally operands %s' % (sorted(bare), sorted(names)))
    # A leg name outside its `local` declaration and its one bare `$?` assignment is a
    # second write in some other form (`read -r st_x`, `printf -v st_x`, `st_x+=...`).
    # Round-35 wave-2 seat SealKillHeadRead: a `read`-based mask was ACCEPTED because no
    # rule counted non-assignment mentions.
    rest = head_code
    for ln in head_code.splitlines():
        if re.match(r'^[ \t]*local\b', ln):
            rest = rest.replace(ln, ' ' * len(ln), 1)
    for nm in set(all_assigns) | set(bare) | set(names):
        got = rest.count(nm)
        if got != 1:
            problems.append('leg %s mentioned %d times outside the local declaration' % (nm, got))
    # the twice-only rule (DevHead, round 33): in the head each leg name may appear EXACTLY twice -
    # once in the `local st_...` declaration line and once on its own bare `st_x=$?` line. Any other
    # occurrence (spaced arithmetic, printf -v, read, declare, unset, brace/group/function wrapping,
    # conditional zeroing) rewrites the captured status and fails closed here. Line-anchored scans
    # miss every non-line-initial form; substring counting catches them all.
    for nm in set(names):
        cnt = head_code.count(nm)
        if cnt != 2:
            problems.append('leg %s appears %d times in the head (want exactly 2: the local declaration and its bare st_x=$?)' % (nm, cnt))
    # no assignment to a leg var anywhere in the tally block
    for m in re.finditer(r'^[ \t]*(st_[A-Za-z0-9_]+)=', block_code, re.M):
        nm = m.group(1)
        if nm in names:
            problems.append('leg %s reassigned inside the tally block: %r' % (nm, m.group(0).strip()))
    return (not problems), 'legs=%d%s%s' % (len(names), '' if all_assigns else ' (none found)',
                                            '; ' + '; '.join(problems) if problems else '')


def check_static(body, block):
    names = leg_names(head_section(body))
    ops = loop_operands(block)
    m = re.match(r'[ \t]*local nlegs=(\d+)\b', block)
    nlegs = int(m.group(1)) if m else None
    problems = []
    if not names:
        problems.append('no st_*=$? leg assignments')
    if sorted(ops) != sorted(names):
        missing = sorted(set(names) - set(ops))
        extra = sorted(o for o in set(ops) if ops.count(o) != names.count(o))
        problems.append('loop operands != legs (missing %s; miscounted %s)' % (missing or '-', extra or '-'))
    if nlegs != len(names):
        problems.append('nlegs=%s but %d legs assigned' % (nlegs, len(names)))
    return (not problems), 'legs=%d operands=%d nlegs=%s%s' % (len(names), len(ops), nlegs,
                                                                '; ' + '; '.join(problems) if problems else '')


def count_vectors(n):
    """One representative vector per (failing, setup) count pair 0..9 (the round-32 held-out
    classes: printf count-field swaps, majority-gated FAIL, conditional double count)."""
    vs = []
    for fc in range(0, n + 1):
        for sc in range(0, n - fc + 1):
            vs.append([1] * fc + [2] * sc + [0] * (n - fc - sc))
    return vs


def check_runtime(block, names, tmp):
    n = len(names)
    ops = loop_operands(block)
    if set(ops) - set(names):
        return False, 'tally loop operands %s have no leg assignment in the head' % sorted(set(ops) - set(names))
    if not names:
        return False, 'no leg assignments to sweep'
    vectors = []
    # every status at position 0
    vectors += [[s] + [0] * (n - 1) for s in range(0, 256)]
    # every status at every other position
    for pos in range(1, n):
        for s in range(0, 256):
            v = [0] * n
            v[pos] = s
            vectors.append(v)
    # every (failing, setup) count pair, representative placements
    vectors += count_vectors(n)
    # position-varied mixes: same counts, different placements (catches placement-conditional arms)
    for fc, sc in ((1, 1), (1, 2), (2, 1), (2, 2), (1, 5), (3, 3)):
        if fc + sc > n:
            continue
        base = [1] * fc + [2] * sc + [0] * (n - fc - sc)
        vectors.append(base)
        vectors.append(list(reversed(base)))
        v = [0] * n
        for i in range(fc):
            v[n - 1 - i] = 1
        for i in range(sc):
            v[i] = 2
        vectors.append(v)
    # co-occurrence vectors: EVERY unordered position pair x EVERY ordered status pair over the
    # extended set (seven independent seats in round 33 converged here: cascade/keyed arms, skips
    # that turn SETUP into PASS, and nlegs recomputions all flip exactly these vectors and no
    # generated one combined a status >=3 with another non-zero leg)
    CO = (1, 2, 3, 4, 5, 7, 9, 120, 126, 127, 128, 255)
    for a in range(n):
        for b in range(a + 1, n):
            for s in CO:
                for t in CO:
                    v = [0] * n
                    v[a], v[b] = s, t
                    vectors.append(v)
    bad = []
    ran = 0
    for cfg in CONFIGS:
        got = run_vectors(block, names, vectors, tmp, cfg)
        ran += len(vectors)
        for v, g in zip(vectors, got):
            exp = oracle(dict(zip(names, v)), ops, n, cfg)
            if g != exp:
                bad.append('cfg(%s,%s) statuses %s: got %s, want %s'
                           % (cfg[1], cfg[2], ' '.join(map(str, v)), show(g), show(exp)))
    # stress: the IDENTIFIED tally loop with one operand duplicated (overcount) or removed (undercount),
    # under every config
    stress = 0
    for i in range(len(ops)):
        for kind, new in (('dup', ops[:i + 1] + ops[i:]), ('drop', ops[:i] + ops[i + 1:])):
            sb = with_operands(block, new)
            for cfg in CONFIGS:
                g = run_vectors(sb, names, [[0] * n], tmp, cfg)[0]
                exp = oracle(dict(zip(names, [0] * n)), new, n, cfg)
                stress += 1
                if g != exp:
                    bad.append('stress %s operand %d cfg(%s,%s): got %s, want %s'
                               % (kind, i, cfg[1], cfg[2], show(g), show(exp)))
    total = ran + stress
    return (not bad), 'vectors=%d mismatched=%d%s' % (total, len(bad), ('; first: ' + bad[0]) if bad else '')


def faults():
    """Known-faulty tally blocks built from REF_BLOCK; each must be rejected by a sound harness."""
    b = REF_BLOCK
    out = []
    def f(name, new):
        if new == b:
            raise CannotAudit('fault %s did not change the reference block' % name)
        out.append((name, new))
    f('label', b.replace('passed=%s', 'passing=%s'))
    f('fail-exits-0', b.replace('    exit 1\n', '    exit 0\n', 1))
    f('drop-last-operand', b.replace(' "$st_citecheck"; do\n', '; do\n', 1))
    start = b.split('\n', 1)[0] + '\n'
    for nm in REF_NAMES:
        f('ignore-' + nm, b.replace(start, start + '  %s=0\n' % nm, 1))
    # Position-only faults: leg NM is ignored only when it is the single failing (1) or setup (2)
    # leg, so only the harness's one-leg-at-each-position loop can see it; the multi-status vectors
    # (two non-zero legs, or status 3) never trigger it. A harness that skips a position accepts it.
    for nm in REF_NAMES:
        others = ' + '.join('$%s' % o for o in REF_NAMES if o != nm)
        f('ignore-alone-' + nm, b.replace(start, start + '  if (( %s == 0 )) && [[ $%s == 1 || $%s == 2 ]]; then %s=0; fi\n'
                                          % (others, nm, nm, nm), 1))
    guard = ('  if (( npass + nfail + nsetup != nlegs )); then\n'
             "    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\\n' \\\n"
             '      "$nlegs" "$((npass + nfail + nsetup))"\n'
             "    printf 'REGRESSION_WORKDIR: %s (kept)\\n' \"$root\"\n"
             '    exit 2\n  fi\n')
    if guard not in b:
        raise CannotAudit('reference guard not found')
    f('guard-removed', b.replace(guard, ''))
    f('guard-overcount-only', b.replace('!= nlegs', '> nlegs'))
    fail_if = b[b.index('  if [[ $nfail -gt 0 ]]'):b.index('  if [[ $nsetup -gt 0 ]]')]
    setup_if = b[b.index('  if [[ $nsetup -gt 0 ]]'):b.index('  if (( npass')]
    f('setup-before-fail', b.replace(fail_if + setup_if, setup_if + fail_if))
    f('fail-needs-exactly-one', b.replace('$nfail -gt 0', '$nfail -eq 1'))
    f('setup-needs-exactly-one', b.replace('$nsetup -gt 0', '$nsetup -eq 1'))
    f('status-3-passes', b.replace('      *) nsetup', '      3) npass=$((npass + 1)) ;;\n      *) nsetup', 1))
    # Round-33 (DevHarness): the five harness-region weakenings reproduced against the frozen tool.
    # Each new fault is visible ONLY through the case a weakened harness deletes or loosens, so a
    # runner harness carrying that weakening accepts it and fails this panel.
    f('fail-exits-2', b.replace('    exit 1\n', '    exit 2\n', 1))  # H24: `rc -ge want_rc` accepts 2>=1
    f('fail-wording', b.replace(' failed=%s setup=%s', ' failures=%s setup=%s', 1))  # H06: status-1 entry deleted
    f('setup-wording', b.replace(' cannot-verify=%s', ' unverified=%s', 1))  # H05: status-2 entry deleted
    f('verdict-word', b.replace("printf 'REGRESSION: FAIL (cases=%s", "printf 'REGRESSION: FAILURE (cases=%s", 1))  # H01: line match loosened
    f('pass-wording', b.replace('ledger legs exact: killed-delta<=0 flips<=0', 'ledger legs ok', 1))  # H11: all-pass case dropped
    f('printf-counts-swapped', b.replace('      "$nlegs" "$npass" "$nfail" "$nsetup"\n',
                                         '      "$nlegs" "$npass" "$nsetup" "$nfail"\n', 1))
    f('guard-overcount-only-alt', b.replace('!= nlegs', '> nlegs').replace('case-tally mismatch', 'tally over'))
    return out


HARNESS_START = re.compile(r'^[ \t]*local tblock\b.*$', re.M)
HARNESS_END = re.compile(r'^[ \t]*tblock=\$tblock_full[ \t]*\n', re.M)
EXTRACT_RE = re.compile(r'^[ \t]*tblock=\$\(awk .*"?\$SELF"?\)[ \t]*\n', re.M)


def harness_section(text):
    m = HARNESS_START.search(text)
    if not m:
        raise CannotAudit('selftest tally harness (`local tblock`) not found')
    e = HARNESS_END.search(text, m.start())
    if not e:
        raise CannotAudit('selftest tally harness end (`tblock=$tblock_full`) not found')
    sec = text[m.start():e.end()]
    extracts = list(EXTRACT_RE.finditer(sec))
    if len(extracts) < 1:
        raise CannotAudit('harness block extraction line not found')
    return sec, extracts


def run_harness(runner_path, section, extracts, injected, tmp):
    last = extracts[-1]
    sec = section[:last.end()] + '  tblock=$AUDIT_INJECT\n' + section[last.end():]
    script = ('set -u -o pipefail\nSELF=%s\n' % shquote(runner_path) +
              'audit_harness() {\n  local root cases=0 failed=0\n  root=$(mktemp -d "$TMPDIR/h.XXXXXX")\n'
              '  st() { cases=$((cases + 1)); if [[ $2 -ne 0 ]]; then failed=$((failed + 1)); fi; }\n' +
              sec + '  printf "HARNESS cases=%s failed=%s\\n" "$cases" "$failed"\n}\naudit_harness\n')
    path = os.path.join(tmp, 'h%d.sh' % len(os.listdir(tmp)))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(script)
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'LC_ALL': 'C', 'HOME': tmp, 'TMPDIR': tmp,
           'AUDIT_INJECT': injected.rstrip('\n')}
    try:
        p = subprocess.run(['bash', path], cwd=tmp, env=env, capture_output=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        raise CannotAudit('harness run timed out')
    m = re.search(r'^HARNESS cases=(\d+) failed=(\d+)$', p.stdout.decode('utf-8', 'replace'), re.M)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))


def shquote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def check_harness(runner_path, text, names, tmp):
    if names != REF_NAMES:
        return False, 'leg names differ from the reference panel (%s)' % ' '.join(names)
    sec, extracts = harness_section(text)
    good = run_harness(runner_path, sec, extracts, REF_BLOCK, tmp)
    if good is None or good[0] == 0 or good[1] != 0:
        return False, 'harness rejects or cannot run the reference block (%s)' % (good,)
    accepted = []
    panel = faults()
    for name, block in panel:
        r = run_harness(runner_path, sec, extracts, block, tmp)
        if r is None:
            continue  # harness aborted on the fault: counted as rejected
        if r[1] == 0:
            accepted.append(name)
    return (not accepted), 'reference cases=%d; faults rejected=%d/%d%s' % (
        good[0], len(panel) - len(accepted), len(panel), ('; accepted: ' + ' '.join(accepted)) if accepted else '')


def audit(runner_path):
    with open(runner_path, 'r', encoding='utf-8') as f:
        text = f.read()
    body = regression_body(text)
    head = head_section(body)
    block = tally_block(body)
    names = leg_names(head)
    tmp = tempfile.mkdtemp(prefix='tally-audit-v3.')
    try:
        rtmp = os.path.join(tmp, 'r')
        os.mkdir(rtmp)
        results = [('head',) + check_head(body, block, names),
                   ('static',) + check_static(body, block),
                   ('runtime',) + check_runtime(block, names, rtmp),
                   ('harness',) + check_harness(runner_path, text, names, tmp)]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, ok, detail in results:
        print('CHECK %s %s %s' % (name, 'PASS' if ok else 'FAIL', detail))
    verdict = all(ok for _, ok, _ in results)
    print('TALLY_AUDIT: %s (%s)' % ('PASS' if verdict else 'FAIL',
                                    ' '.join('%s=%s' % (n, 'pass' if ok else 'fail') for n, ok, _ in results)))
    return 0 if verdict else 1, len(names)


def then_regression(runner_path, nlegs, workdir):
    argv = ['timeout', str(THEN_REGRESSION_TIMEOUT), 'bash', runner_path, '--regression']
    if workdir:
        argv += ['--workdir', workdir]
    p = subprocess.run(argv, capture_output=True)
    out = p.stdout.decode('utf-8', 'replace')
    sys.stdout.write(out)
    sys.stderr.write(p.stderr.decode('utf-8', 'replace'))
    if p.returncode == 124:
        print('TALLY_AUDIT_REGRESSION: SETUP (--then-regression timed out after %ds)' % THEN_REGRESSION_TIMEOUT)
        return 2
    m = re.search(r'^REGRESSION: (PASS|FAIL|SETUP) \(cases=(\d+)', out, re.M)
    if not m or int(m.group(2)) != nlegs:
        print('TALLY_AUDIT_REGRESSION: SETUP (REGRESSION line missing or cases != %d legs found)' % nlegs)
        return 2
    print('TALLY_AUDIT_REGRESSION: %s (cases=%s legs=%d exit=%d)' % (m.group(1), m.group(2), nlegs, p.returncode))
    return p.returncode


# ---------------------------------------------------------------- selftest

def selftest():
    runner = os.path.join(HERE, 'mutate-and-run.sh')
    with open(runner, encoding='utf-8') as f:
        text = f.read()
    loop = '  for st in ' + ' '.join('"$%s"' % n for n in REF_NAMES) + '; do\n'
    cmp_line = '    [[ $rc -eq $want_rc && "${out%%$\'\\n\'*}" == "$want_line" ]]\n'
    tally_case = '''    case $st in
      0) npass=$((npass + 1)) ;;
      1) nfail=$((nfail + 1)) ;;
      *) nsetup=$((nsetup + 1)) ;;
    esac
  done
'''
    start = '  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n'
    # round-32 held-out classes, replayed as selftest seeds (the held-out JSONs are committed evidence)
    mask_7bit = text.replace(start, start + '  st_kagi=$((st_kagi & 127))\n', 1)                      # HeldOutLoop-1
    wrapper = text.replace(start + loop, start + '  local tally_once\n  for tally_once in "$st_js"; do\n' + loop, 1) \
                  .replace(tally_case, tally_case + '  done\n', 1)                                     # HeldOutLoop-3
    precount = text.replace(start, start + '  local legs_counted=0\n  for leg in ' + ' '.join('"$%s"' % n for n in REF_NAMES) + '; do\n    legs_counted=$((legs_counted + 1))\n  done\n', 1)  # HeldOutRefactor-a4
    head_overwrite = text.replace('  st_claims=$?\n', '  st_claims=$?\n  st_claims=0\n', 1)         # head double-assignment
    # Round-35 wave-2 classes: a here-doc DECOY carrying a pristine copy of the block (the
    # first-match extractor audited the decoy), and a `read` second write to a leg name.
    _blk = tally_block(regression_body(text))
    _mut4 = text.replace('      1) nfail=$((nfail + 1)) ;;\n',
                         '      1) nfail=$((nfail + 1)) ;;\n      4) npass=$((npass + 1)) ;;\n', 1)
    heredoc_decoy = _mut4.replace(start, "  cat <<'EOF' >/dev/null\n" + _blk + "EOF\n" + start, 1)
    read_head_mask = text.replace('  st_js=$?\n', '  st_js=$?\n  read -r st_js <<< ""\n', 1)
    printf_swap = text.replace('      "$nlegs" "$npass" "$nfail" "$nsetup"\n', '      "$nlegs" "$npass" "$nsetup" "$nfail"\n', 1)  # HeldOutPrintf-1
    majority_guard = text.replace('  if [[ $nfail -gt 0 ]]; then\n',
                                  '  if [[ $nfail -gt 0 && $nsetup -le $((npass + nfail)) ]]; then\n', 1)  # HeldOutGuard-1
    double_count = text.replace('      1) nfail=$((nfail + 1)) ;;\n',
                                '      1) nfail=$((nfail + 1)); if (( nsetup > 1 )); then nfail=$((nfail + 1)); fi ;;\n', 1)  # HeldOutTallyArms-01
    harness_local = '  local tblock tgot tvec ti tj\n'
    second_extract = text.replace(harness_local,
                                  harness_local + '    tblock=$(awk \'/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f\' "$SELF")\n', 1)  # HeldOutRefactor-a3
    head_mask = text.replace('  st_kagi=$?\n', '  st_kagi=$(($? & 127))\n', 1)                        # out-of-block head masking
    cases = [
        ('pristine', text, 0, None),
        ('dup-drop operand', text.replace(loop, loop.replace('"$st_citecheck"', '"$st_js"')), 1, 'static'),
        ('nlegs wrong', text.replace('  local nlegs=9 ', '  local nlegs=8 ', 1), 1, 'static'),
        ('head masked', head_mask, 1, 'head'),
        ('status 4 passes', text.replace('      1) nfail=$((nfail + 1)) ;;\n',
                                         '      1) nfail=$((nfail + 1)) ;;\n      4) npass=$((npass + 1)) ;;\n', 1), 1, 'runtime'),
        ('guard undercount only', text.replace('npass + nfail + nsetup != nlegs', 'npass + nfail + nsetup < nlegs', 1), 1, 'runtime'),
        ('in-block 7-bit mask', mask_7bit, 1, None),
        ('arm pattern 00', text.replace('      0) npass=$((npass + 1)) ;;', '      00) npass=$((npass + 1)) ;;', 1), 1, 'runtime'),
        ('head overwrite', head_overwrite, 1, 'head'),
        ('printf count swap', printf_swap, 1, 'runtime'),
        ('majority-gated fail', majority_guard, 1, 'runtime'),
        ('keep-conjunct guard', text.replace('  if [[ $nfail -gt 0 ]]; then\n',
                                             '  if [[ $nfail -gt 0 && $KEEP -eq 1 ]]; then\n', 1), 1, 'runtime'),
        ('conditional double count', double_count, 1, 'runtime'),
        # Round-35 classes: the (auto,KEEP) (0,0)/(1,1) sweep hole and the full-stdout comparison.
        ('cfg-gated accept swap (0,0)', text.replace('  if [[ $nfail -gt 0 ]]; then\n',
                                                     '  if [[ $auto -eq 0 && $KEEP -eq 0 ]]; then nfail=0; fi\n  if [[ $nfail -gt 0 ]]; then\n', 1), 1, 'runtime'),
        ('cfg-gated pass mask (1,1)', text.replace('  if [[ $nfail -gt 0 ]]; then\n',
                                                   '  if [[ $auto -eq 1 && $KEEP -eq 1 ]]; then npass=0; fi\n  if [[ $nfail -gt 0 ]]; then\n', 1), 1, 'runtime'),
        ('workdir-branch condition swap', text.replace('if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then',
                                                       'if [[ $auto -eq 0 && $KEEP -eq 0 ]]; then', 1), 1, 'runtime'),
        # Round-35 false-kill classes: inert comment text must never move a verdict (accept).
        ('comment names a leg', text.replace('  st_js=$?\n', '  st_js=$?\n  # st_js is captured immediately above\n', 1), 0, None),
        ('comment brace in body', text.replace('  if [[ $nfail -gt 0 ]]; then\n',
                                               '  # a stray } must not close the body\n  if [[ $nfail -gt 0 ]]; then\n', 1), 0, None),
        ('comment esac in arm', text.replace('      0) npass=$((npass + 1)) ;;\n',
                                             '      0) npass=$((npass + 1)) ;;  # esac mention\n', 1), 0, None),
        # Round-35 real-root witness: the auto root is /tmp/tameshi-r4-2-regression.* and a
        # gate keyed on it must be KILLED; inert comment text naming it must stay ACCEPTED.
        ('real-root gated mask', text.replace(tally_case, tally_case + '  if [[ $auto -eq 1 && "$root" == /tmp/tameshi-r4-2-regression.* ]]; then nfail=0; npass=$((npass+1)); fi\n', 1), 1, 'runtime'),
        ('real-root shape-6 gated mask', text.replace(tally_case, tally_case + '  if [[ $auto -eq 1 && "$root" == /tmp/tameshi-r4-2-regression.?????? ]]; then nfail=0; npass=$((npass+1)); fi\n', 1), 1, 'runtime'),
        ('comment names real root', text.replace(start, start + '  # the auto root is /tmp/tameshi-r4-2-regression.* at runtime\n', 1), 0, None),
        ('heredoc block decoy (refused)', heredoc_decoy, 2, None),
        ('read second write to a leg', read_head_mask, 1, 'head'),
        ('harness exit-only', text.replace(cmp_line, '    [[ $rc -eq $want_rc ]]\n', 1), 1, 'harness'),
        ('harness swallowed', text.replace(cmp_line, cmp_line + '    rc=$?\n', 1), 1, 'harness'),
        ('harness position 8 skipped', text.replace('    for ti in 0 1 2 3 4 5 6 7 8; do', '    for ti in 0 1 2 3 4 5 6 7 7; do', 1), 1, 'harness'),
        ('harness position 0 skipped', text.replace('    for ti in 0 1 2 3 4 5 6 7 8; do', '    for ti in 6 1 2 3 4 5 6 7 8; do', 1), 1, 'harness'),
        ('harness position 1 skipped', text.replace('    for ti in 0 1 2 3 4 5 6 7 8; do', '    for ti in 0 3 2 3 4 5 6 7 8; do', 1), 1, 'harness'),
        ('aux wrapper loop', wrapper, 0, None),
        ('aux pre-count loop', precount, 0, None),
        ('second extraction line', second_extract, 0, None),
        ('reversed operands', text.replace(loop, '  for st in ' + ' '.join('"$%s"' % n for n in reversed(REF_NAMES)) + '; do\n', 1), 0, None),
    ]
    tmp = tempfile.mkdtemp(prefix='tally-audit-v3-selftest.')
    passed = 0
    try:
        for i, (name, body, want, check) in enumerate(cases):
            if name != 'pristine' and body == text:
                print('CASE %s FAIL (edit did not apply)' % name)
                continue
            path = os.path.join(tmp, 'c%d.sh' % i)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(body)
            p = subprocess.run([sys.executable, os.path.abspath(__file__), '--runner', path], capture_output=True, timeout=900)
            out = p.stdout.decode()
            ok = p.returncode == want and (check is None or re.search(r'^CHECK %s FAIL' % check, out, re.M))
            if not ok and p.returncode == 2 and want != 2:
                ok = False
            passed += bool(ok)
            print('CASE %s %s (exit %d)' % (name, 'PASS' if ok else 'FAIL', p.returncode))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print('TALLY_AUDIT_V3_SELFTEST: %d/%d pass' % (passed, len(cases)))
    return 0 if passed == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runner', default=os.path.join(HERE, 'mutate-and-run.sh'))
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--then-regression', action='store_true')
    ap.add_argument('--workdir')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    try:
        rc, nlegs = audit(os.path.abspath(a.runner))
    except (CannotAudit, OSError, UnicodeDecodeError, ValueError) as e:
        print('TALLY_AUDIT: SETUP (%s)' % e)
        return 2
    if rc == 0 and a.then_regression:
        return then_regression(os.path.abspath(a.runner), nlegs, a.workdir)
    return rc


if __name__ == '__main__':
    sys.exit(main())
