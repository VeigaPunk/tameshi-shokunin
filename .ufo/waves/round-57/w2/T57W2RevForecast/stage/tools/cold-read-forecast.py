#!/usr/bin/env python3
"""cold-read-forecast.py — price a round's planned edits in cold-read headings.

Question answered: if a round edits these paths (and these SKILL.md sections),
which headings of the round-21 cold-read monitor lose credit, and how many
fresh readers must re-read them before the deciding run? (considerthese
2026-10-28 proposal 3: rounds 48 and 52 were rejected for cold-read harm their
plans did not price.)

Usage:
  cold-read-forecast.py --lane LANE --rev REV --paths P1 [P2 ...]
        [--skill-section "## Heading"]... [--skill-lines A-B]... [--strict] [--json]
  cold-read-forecast.py --lane LANE --rev REV --diff-to REV2 [--json]
        retrospective calibration: the planned set is what changed REV -> REV2.
        MEASURED, not simulated: the credit rule is evaluated at BOTH revs
        (the ledger, SKILL.md and the tree of each), and the lost headings are
        those the monitor covers at REV but not at REV2. A heading added at
        REV2 (no ledger entry) is lost; a heading removed at REV2 is gone from
        the page and costs no reader; a heading whose SKILL.md text changed is
        lost with reason `section-sha-void`.
  cold-read-forecast.py --selftest

Reads only git blobs at REV (never the worktree): the lane's SKILL.md and the
round-21 ledger `.ufo/evidence/round-21/coldread/ledger.json` (entries:
heading, start/end, sha256, inputs{path: sha256}, traces). It re-evaluates the
frozen monitor's credit rule (`.ufo/evidence/round-18/measure.py`, run through
`.ufo/evidence/round-21/coldread/measure.py`) twice per heading -- once as the
tree stands (base) and once with every planned path treated as changed -- and
reports the headings covered at base but not after. The monitor's per-section
reason strings are reused: `input-drift:<path>` (a pinned input changed),
`live-lane-read:<path>` (a trace's live-lane read changed), and
`section-sha-void` (a planned SKILL.md section edit; the section's own sha256
no longer matches any ledger entry, `no-ledger-entry`).

Rules carried from the monitor:
  * an entry credits when its class/verdict gate passes, commands>0, every
    non-ignored input still hashes to the recorded sha256, and its traces
    validate; a heading is covered when >=1 entry credits and no failing
    (veto-eligible) entry still has all inputs verifying.
  * SKILL.md is DROPPED from input drift (the monitor ignores it as an input,
    each section is keyed by its own sha256), so a SKILL.md path prices only
    through --skill-section / --skill-lines: the named section's sha changes
    and the section is voided. Every later `:NNN` page-local anchor shifts when
    an edit changes SKILL.md's line count (not priced here; the monitor keys
    on section bytes, readers key on line numbers).
  * the unit of cost is one fresh reader per lost heading (readers == headings).

Path classes in the output:
  PRICED      pinned as an input by an entry that matches a current section
  STALE-ONLY  pinned only by entries whose section sha no longer exists in
              SKILL.md (their pins price nothing at REV)
  UNPINNED    tracked at REV, pinned by no ledger entry anywhere (0 headings)
  NEW         absent from the tree at REV (an added file cannot drift a pin)
  UNPRICED    the monitor reads it DIRECTLY yet no entry pins it: SKILL.md
              without a section, the ledger itself, the round-18/21 monitor
              scripts. A change there moves the score or the credit set in a
              way this forecast cannot see -> exit 2, loudly. --strict also
              turns UNPINNED and STALE-ONLY paths into exit 2.

Exits: 0 forecast printed; 2 UNPRICED path (the forecast is still printed), an
unresolvable REV/blob, a section that names no heading, or an unusable TMPDIR
(could-not-evaluate, never a silent /tmp fallback); 64 usage (option-like REV,
non-canonical path). Stdlib only. Writes nothing outside --selftest fixtures
under TMPDIR.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

LEDGER_PATH = '.ufo/evidence/round-21/coldread/ledger.json'
ROUND18_LEDGER_PATH = '.ufo/evidence/round-18/coldread/ledger.json'
ROUND17_LEDGER_PATH = '.ufo/evidence/round-17/coldread/ledger.json'
SKILL = 'SKILL.md'
# Inputs the frozen monitor ignores as pins (its own IGNORED_INPUTS in the
# round-21 selector): the page is keyed by section sha, ledgers are outputs.
IGNORED_INPUTS = frozenset((SKILL, ROUND17_LEDGER_PATH, ROUND18_LEDGER_PATH,
                            LEDGER_PATH))
# Paths the monitor reads directly (not through an entry's pins): its own
# scripts and ledger, SKILL.md (sectionized), and the four REQUIRED_BLOBS.
DIRECT_READS = frozenset((
    SKILL, LEDGER_PATH,
    '.ufo/evidence/round-18/measure.py',
    '.ufo/evidence/round-21/coldread/measure.py',
    'tools/mutate-and-run.sh', 'SHONEN.md', 'corpus/SOURCES.md',
))
# The monitor's own constant (round-18 measure.py LIVE_LANE_ROOT): a trace's
# read of a file under it counts as a read of REV only when sha-bound.
LIVE_LANE_ROOT = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
TRACE_SCHEMA = 'tameshi-trace-inputs-v1'
HEADING_RE = re.compile(r'^#{1,3}(?:\s|$)')
COMMIT_RE = re.compile(r'^[0-9a-f]{40}$')
BLOB_MODES = frozenset(('100644', '100755'))
FAIL_VERDICTS = frozenset(('gap-blocking', 'wrong-expectation', 'not-executed'))
EXEC_VERDICTS = frozenset(('executed-ok', 'gap-minor'))
REC_VERDICTS = frozenset(('verified-record', 'gap-minor'))
VALID_VERDICTS = frozenset(('executed-ok', 'verified-record', 'gap-minor',
                            'gap-blocking', 'wrong-expectation', 'not-executed'))
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


class Usage(Exception):
    pass


class CouldNotEvaluate(Exception):
    pass


def git(repo, *args, stdin=None):
    return subprocess.run(['git', '-C', repo] + list(args), input=stdin,
                          capture_output=True, env=GIT_ENV)


def resolve_commit(repo, value):
    if not isinstance(value, str) or not value or value.startswith('-'):
        return None
    if '\x00' in value or '\n' in value:
        return None
    result = git(repo, 'rev-parse', '--verify', '--quiet', '--end-of-options',
                 '%s^{commit}' % value)
    if result.returncode != 0:
        return None
    sha = result.stdout.decode('utf-8', 'surrogateescape').strip()
    return sha if COMMIT_RE.match(sha) else None


def canonical_path(path):
    if not isinstance(path, str) or not path or '\x00' in path:
        return False
    if path.startswith('/') or path.startswith('./'):
        return False
    return not any(p in ('', '.', '..', '.git') for p in path.split('/'))


def tree_modes(repo, rev):
    """{path: (mode, blob sha)} for every tracked file at REV (one ls-tree)."""
    result = git(repo, 'ls-tree', '-r', '-z', '--full-tree', rev)
    if result.returncode != 0:
        raise CouldNotEvaluate('git ls-tree failed at %s' % rev)
    out = {}
    for chunk in result.stdout.split(b'\x00'):
        if not chunk:
            continue
        meta, _, name = chunk.partition(b'\t')
        mode, _kind, sha = meta.decode('ascii').split(' ')
        out[name.decode('utf-8', 'surrogateescape')] = (mode, sha)
    return out


def read_blobs(repo, shas):
    """{blob sha: bytes} through one `git cat-file --batch`."""
    wanted = sorted(set(shas))
    if not wanted:
        return {}
    result = git(repo, 'cat-file', '--batch',
                 stdin=('\n'.join(wanted) + '\n').encode('ascii'))
    if result.returncode != 0:
        raise CouldNotEvaluate('git cat-file --batch failed')
    data, pos, out = result.stdout, 0, {}
    for sha in wanted:
        eol = data.index(b'\n', pos)
        header = data[pos:eol].split(b' ')
        if len(header) != 3 or header[1] != b'blob':
            raise CouldNotEvaluate('blob %s unreadable' % sha)
        size = int(header[2])
        out[sha] = data[eol + 1:eol + 1 + size]
        pos = eol + 1 + size + 1
    return out


def sectionize(raw):
    """The monitor's sectionizer: preamble + every #/##/### heading outside ``` fences."""
    lines = raw.decode('utf-8', 'surrogateescape').split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    heads, in_fence = [], False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence and HEADING_RE.match(line):
            heads.append(i)
    pairs = []
    if heads:
        if heads[0] > 0:
            pairs.append((0, heads[0]))
        pairs.extend(zip(heads, heads[1:] + [len(lines)]))
    else:
        pairs.append((0, len(lines)))
    head_set, sections = set(heads), []
    for s, e in pairs:
        body = list(lines[s:e])
        while body and body[-1].strip() == '':
            body.pop()
        sections.append({
            'start': s + 1, 'end': e,
            'heading': lines[s] if s in head_set else '',
            'sha256': hashlib.sha256('\n'.join(body).encode(
                'utf-8', 'surrogateescape')).hexdigest()})
    return sections


class Model:
    """Everything the forecast needs from one REV: sections, ledger, tree, blobs."""

    def __init__(self, repo, rev):
        self.repo, self.rev = repo, rev
        self.tree = tree_modes(repo, rev)
        if SKILL not in self.tree or LEDGER_PATH not in self.tree:
            raise CouldNotEvaluate('%s or %s missing at %s' % (SKILL, LEDGER_PATH, rev))
        raw = read_blobs(repo, [self.tree[SKILL][1], self.tree[LEDGER_PATH][1]])
        self.skill_raw = raw[self.tree[SKILL][1]]
        try:
            self.entries = json.loads(raw[self.tree[LEDGER_PATH][1]])['entries']
            assert isinstance(self.entries, list)
        except Exception as exc:
            raise CouldNotEvaluate('ledger unreadable: %s: %s' % (type(exc).__name__, exc))
        self.sections = sectionize(self.skill_raw)
        by_sha = {}
        for entry in self.entries:
            if isinstance(entry, dict) and isinstance(entry.get('sha256'), str):
                by_sha.setdefault(entry['sha256'], []).append(entry)
        self.matches = [by_sha.get(sec['sha256'], []) for sec in self.sections]
        # Blobs for every pin of every matching entry and every trace they list.
        need = set()
        for group in self.matches:
            for entry in group:
                for path in self.view(entry) or ():
                    mode = self.tree.get(path)
                    if mode and mode[0] in BLOB_MODES:
                        need.add(mode[1])
                for path in entry.get('traces') or ():
                    mode = self.tree.get(path) if isinstance(path, str) else None
                    if mode and mode[0] in BLOB_MODES:
                        need.add(mode[1])
        self.blobs = read_blobs(repo, need)
        self._live_deps = None

    @staticmethod
    def view(entry):
        raw = entry.get('inputs')
        if not isinstance(raw, dict):
            return None
        return {p: v for p, v in raw.items() if p not in IGNORED_INPUTS}

    def blob_at(self, path):
        mode = self.tree.get(path) if isinstance(path, str) else None
        if not mode or mode[0] not in BLOB_MODES:
            return None
        return self.blobs.get(mode[1])

    def input_failures(self, entry, changed):
        view = self.view(entry) or {}
        fails = []
        for path in sorted(view, key=lambda p: (str(type(p)), str(p))):
            if not canonical_path(path):
                fails.append('input-not-blob:%s' % path)
                continue
            mode = self.tree.get(path)
            if mode is None:
                fails.append('input-missing:%s' % path)
            elif mode[0] not in BLOB_MODES:
                fails.append('input-not-blob:%s' % path)
            elif path in changed:
                fails.append('input-drift:%s' % path)
            elif hashlib.sha256(self.blob_at(path)).hexdigest() != view[path]:
                fails.append('input-drift:%s' % path)
        return fails

    def live_bound(self, path, digest, changed):
        if not isinstance(path, str) or not isinstance(digest, str):
            return False
        root = os.path.realpath(LIVE_LANE_ROOT)
        real = os.path.realpath(path)
        if not (real == root or real.startswith(root + os.sep)):
            return False
        rel = os.path.relpath(real, root).replace(os.sep, '/')
        if rel == '.git' or rel.startswith('.git/'):
            return True
        if not canonical_path(rel) or rel in changed:
            return False
        raw = self.blob_at(rel)
        return raw is not None and hashlib.sha256(raw).hexdigest() == digest

    def trace_reason(self, entry, changed):
        cmd = json_int(entry.get('commands_executed_count', 0))
        if cmd is None:
            return 'malformed-entry'
        traces = entry.get('traces')
        if traces is None or traces == []:
            return 'traces-unrecorded' if cmd > 0 else None
        if not isinstance(traces, list):
            return 'traces-unrecorded'
        if cmd <= 0:
            return None
        view = self.view(entry) or {}
        for path in sorted(traces, key=str):
            raw = self.blob_at(path) if canonical_path(path) else None
            if raw is None:
                return 'trace-missing:%s' % path
            try:
                receipt = json.loads(raw.decode('utf-8', 'surrogateescape'))
            except ValueError:
                return 'trace-invalid:%s' % path
            if not isinstance(receipt, dict) or receipt.get('schema') != TRACE_SCHEMA:
                return 'trace-invalid:%s' % path
            rec_inputs = receipt.get('inputs')
            if not isinstance(rec_inputs, dict):
                return 'trace-invalid:%s' % path
            for key in sorted(rec_inputs, key=str):
                if key in IGNORED_INPUTS:
                    continue
                if key not in view:
                    return 'trace-input-unrecorded:%s' % key
                if view[key] != rec_inputs[key]:
                    return 'trace-input-drift:%s' % key
            live = receipt.get('live_lane_reads')
            if isinstance(live, dict):
                for key in sorted(live, key=str):
                    if not self.live_bound(key, live[key], changed):
                        return 'live-lane-read:%s' % key
            ext = receipt.get('external')
            if isinstance(ext, dict):
                for key in sorted(ext, key=str):
                    if under_live_lane(key) and not self.live_bound(key, ext[key], changed):
                        return 'live-lane-read:%s' % key
        return None

    def entry_reason(self, entry, changed):
        reason = entry_failure(entry) or entry_credit_reason(entry)
        if reason is not None:
            return reason
        if json_int(entry.get('commands_executed_count', 0)) == 0:
            return 'commands-unrecorded'
        view = self.view(entry)
        if not view:
            return 'inputs-unrecorded'
        fails = self.input_failures(entry, changed)
        if fails:
            return ';'.join(fails)
        return self.trace_reason(entry, changed)

    def entry_stale(self, entry, changed):
        view = self.view(entry)
        return bool(view) and bool(self.input_failures(entry, changed))

    def covered(self, index, changed):
        """(covered, reasons) for section INDEX with CHANGED paths drifted."""
        credited, vetoes, reasons = 0, 0, []
        for entry in self.matches[index]:
            reason = self.entry_reason(entry, changed)
            if reason is None:
                credited += 1
            else:
                reasons.append(reason)
            if entry_failure(entry) is not None and not self.entry_stale(entry, changed):
                vetoes += 1
        return (credited > 0 and not vetoes), reasons

    def live_deps(self):
        if self._live_deps is None:
            self._live_deps = set()
            for group in self.matches:
                for entry in group:
                    self._live_deps |= self.deps(entry)
        return self._live_deps

    def deps(self, entry):
        """Paths whose change would fail this entry (pins + trace live reads)."""
        out = set(self.view(entry) or ())
        for path in entry.get('traces') or ():
            raw = self.blob_at(path) if isinstance(path, str) and canonical_path(path) else None
            try:
                receipt = json.loads(raw.decode('utf-8', 'surrogateescape')) if raw else None
            except ValueError:
                receipt = None
            if not isinstance(receipt, dict):
                continue
            keys = []
            for field in ('live_lane_reads', 'external'):
                if isinstance(receipt.get(field), dict):
                    keys.extend(k for k in receipt[field] if isinstance(k, str))
            root = os.path.realpath(LIVE_LANE_ROOT)
            for key in keys:
                real = os.path.realpath(key)
                if real.startswith(root + os.sep):
                    rel = os.path.relpath(real, root).replace(os.sep, '/')
                    if not (rel == '.git' or rel.startswith('.git/')):
                        out.add(rel)
        return out


def json_int(value):
    return value if type(value) is int and value >= 0 else None


def under_live_lane(path):
    if not isinstance(path, str) or not path:
        return False
    real, root = os.path.realpath(path), os.path.realpath(LIVE_LANE_ROOT)
    return real == root or real.startswith(root + os.sep)


def entry_failure(entry):
    verdict = entry.get('verdict')
    if not isinstance(verdict, str) or verdict not in VALID_VERDICTS:
        return 'verdict:%s' % verdict
    if verdict in FAIL_VERDICTS:
        return 'verdict:%s' % verdict
    bg = json_int(entry.get('blocking_gaps', 0))
    we = json_int(entry.get('wrong_expectations', 0))
    if bg is None or we is None:
        return 'malformed-entry'
    if bg != 0:
        return 'blocking-gaps:%d' % bg
    if we != 0:
        return 'wrong-expectations:%d' % we
    return None


def entry_credit_reason(entry):
    verdict = entry.get('verdict')
    cls = entry.get('class')
    if cls == 'instruction':
        if verdict not in EXEC_VERDICTS:
            return 'verdict-class:%s/instruction' % verdict
        cmd = json_int(entry.get('commands_executed_count', 0))
        if cmd is None:
            return 'malformed-entry'
        if cmd <= 0:
            return 'commands-executed-count:%s' % entry.get('commands_executed_count')
        return None
    if cls == 'record':
        return None if verdict in REC_VERDICTS else 'verdict-class:%s/record' % verdict
    return 'class:%s' % cls


def parse_lines(spec):
    match = re.fullmatch(r'(\d+)(?:-(\d+))?', spec)
    if not match:
        raise Usage('--skill-lines wants A or A-B, got %r' % spec)
    lo = int(match.group(1))
    hi = int(match.group(2) or lo)
    if lo < 1 or hi < lo:
        raise Usage('--skill-lines range out of order: %r' % spec)
    return lo, hi


def skill_targets(model, headings, line_specs):
    """Indices of SKILL sections named by exact heading text or touched lines."""
    hit, problems = set(), []
    for text in headings:
        found = [i for i, s in enumerate(model.sections) if s['heading'].strip() == text.strip()]
        if not found:
            problems.append('SKILL_SECTION_NOT_FOUND: %r names no heading at %s' % (text, model.rev[:12]))
        elif len(found) > 1:
            problems.append('SKILL_SECTION_AMBIGUOUS: %r matches %d headings; use --skill-lines' % (text, len(found)))
        else:
            hit.add(found[0])
    for spec in line_specs:
        lo, hi = parse_lines(spec)
        found = [i for i, s in enumerate(model.sections) if s['start'] <= hi and s['end'] >= lo]
        if not found:
            problems.append('SKILL_LINES_OUTSIDE: %s lies outside SKILL.md (%d lines)' % (
                spec, model.sections[-1]['end']))
        hit.update(found)
    return hit, problems


def classify(model, path, skill_picked):
    if path == SKILL:
        return 'PRICED' if skill_picked else 'UNPRICED'
    if path in model.live_deps():
        return 'PRICED'
    if path in DIRECT_READS:
        return 'UNPRICED'
    if path not in model.tree:
        return 'NEW'
    if any(path in (e.get('inputs') or {}) for e in model.entries if isinstance(e, dict)):
        return 'STALE-ONLY'
    return 'UNPINNED'


def forecast(model, paths, skill_idx, strict=False):
    changed = {p for p in paths if p != SKILL}
    classes = {p: classify(model, p, bool(skill_idx)) for p in paths}
    lost, uncovered = [], []
    for i, sec in enumerate(model.sections):
        base_ok, _ = model.covered(i, set())
        if not base_ok:
            uncovered.append(sec)
            continue
        if i in skill_idx:
            lost.append({'start': sec['start'], 'end': sec['end'], 'heading': sec['heading'],
                         'reasons': ['section-sha-void']})
            continue
        ok, _ = model.covered(i, changed)
        if ok:
            continue
        reasons = set()
        for entry in model.matches[i]:
            if model.entry_reason(entry, set()) is None:
                reasons.update(r for r in (model.entry_reason(entry, changed) or '').split(';') if r)
        lost.append({'start': sec['start'], 'end': sec['end'], 'heading': sec['heading'],
                     'reasons': sorted(reasons)})
    by_path = {}
    for item in lost:
        for reason in item['reasons']:
            if ':' in reason:
                by_path.setdefault(reason.split(':', 1)[1], []).append(item['start'])
    exit_code = 0
    notes = []
    for path in paths:
        cls = classes[path]
        if cls == 'UNPRICED':
            exit_code = 2
            notes.append('FORECAST_UNPRICED: %s is read directly by the monitor and pinned by no entry; '
                         'its cost cannot be forecast%s' % (
                             path, ' (pass --skill-section/--skill-lines)' if path == SKILL else ''))
        elif strict and cls in ('UNPINNED', 'STALE-ONLY'):
            exit_code = 2
            notes.append('FORECAST_UNPINNED: %s is %s (strict)' % (path, cls))
    return {
        'rev': model.rev, 'paths': list(paths), 'classes': classes,
        'sections_total': len(model.sections),
        'base_covered': len(model.sections) - len(uncovered),
        'already_uncovered': [{'start': s['start'], 'heading': s['heading']} for s in uncovered],
        'skill_sections_edited': sorted(model.sections[i]['start'] for i in skill_idx),
        'lost': lost, 'headings': len(lost), 'readers': len(lost),
        'by_path': {p: sorted(v) for p, v in sorted(by_path.items())},
        'notes': notes, 'exit': exit_code}


def section_uncovered(model, index):
    """(covered, reasons) for one section at MODEL's own rev."""
    if not model.matches[index]:
        return False, ['no-ledger-entry']
    return model.covered(index, set())


def uncovered_sections(model):
    """Every section the monitor leaves uncovered at MODEL's rev."""
    out = []
    for i, sec in enumerate(model.sections):
        covered, reasons = section_uncovered(model, i)
        if not covered:
            out.append({'index': i, 'start': sec['start'], 'end': sec['end'],
                        'heading': sec['heading'], 'reasons': reasons})
    return out


def entry_causes(base, target, heading):
    """New failure causes for HEADING: entries that credited at base, fail at target.

    Only entries that CREDITED at base count: an entry already stale at base
    proves nothing about the change (the monitor's stale-does-not-veto rule).
    """
    causes = set()
    for i, sec in enumerate(base.sections):
        if sec['heading'] != heading:
            continue
        for entry in base.matches[i]:
            if base.entry_reason(entry, set()) is not None:
                continue
            reason = target.entry_reason(entry, set())
            if reason:
                causes.update(part for part in reason.split(';') if part)
    return sorted(causes)


def diff_forecast(base, target, paths, strict=False):
    """Retrospective calibration: covered at BASE, uncovered at TARGET.

    The target rev is measured with the tool's own credit rule -- the rule the
    frozen monitor runs -- so the lost set is exactly the monitor's uncredited
    set at the target, minus what was already uncredited at base. A SKILL.md
    section EDITED between the revs has no ledger entry at the target
    (`no-ledger-entry`): one fresh reader, reason `section-sha-void`. A
    section ADDED between the revs is uncovered at the target for the same
    reason and is a lost heading too. A section REMOVED between the revs is
    gone from the page: it costs no reader and is not a lost heading.
    """
    base_unc = uncovered_sections(base)
    target_unc = uncovered_sections(target)
    base_unc_headings = {u['heading'] for u in base_unc}
    lost = []
    for u in target_unc:
        if u['heading'] in base_unc_headings:
            continue
        if not target.matches[u['index']]:
            edited = any(s['heading'] == u['heading'] for s in base.sections)
            reasons = ['section-sha-void'] if edited else ['no-ledger-entry']
        else:
            reasons = entry_causes(base, target, u['heading']) or ['no-ledger-entry']
        lost.append({'start': u['start'], 'end': u['end'], 'heading': u['heading'],
                     'reasons': reasons})
    by_path = {}
    for item in lost:
        for reason in item['reasons']:
            if ':' in reason:
                by_path.setdefault(reason.split(':', 1)[1], []).append(item['start'])
    classes = {}
    for path in paths:
        if path == SKILL:
            classes[path] = 'PRICED'      # measured at the target rev
        elif path == LEDGER_PATH:
            classes[path] = 'UNPRICED'    # the credit SET itself changed
        else:
            classes[path] = classify(base, path, True)
    exit_code = 0
    notes = []
    for path in paths:
        cls = classes[path]
        if cls == 'UNPRICED':
            exit_code = 2
            notes.append('FORECAST_UNPRICED: %s is read directly by the monitor and pinned by no entry; '
                         'its cost cannot be forecast' % path)
        elif strict and cls in ('UNPINNED', 'STALE-ONLY'):
            exit_code = 2
            notes.append('FORECAST_UNPINNED: %s is %s (strict)' % (path, cls))
    target_shas = {s['sha256'] for s in target.sections}
    edited_starts = sorted(sec['start'] for sec in base.sections
                           if sec['sha256'] not in target_shas
                           and any(s['heading'] == sec['heading'] for s in target.sections))
    return {
        'rev': base.rev, 'target_rev': target.rev, 'paths': list(paths), 'classes': classes,
        'sections_total': len(base.sections),
        'target_sections_total': len(target.sections),
        'base_covered': len(base.sections) - len(base_unc),
        'target_covered': len(target.sections) - len(target_unc),
        'already_uncovered': [{'start': u['start'], 'heading': u['heading']} for u in base_unc],
        'skill_sections_edited': edited_starts,
        'lost': lost, 'headings': len(lost), 'readers': len(lost),
        'by_path': {p: sorted(v) for p, v in sorted(by_path.items())},
        'notes': notes, 'exit': exit_code}


def render(result):
    total = result.get('target_sections_total', result['sections_total'])
    out = ['FORECAST: paths=%d headings=%d readers=%d of %d' % (
        len(result['paths']), result['headings'], result['readers'], total)]
    out.append('BASE: covered=%d of %d at %s' % (
        result['base_covered'], result['sections_total'], result['rev'][:12]))
    for path in result['paths']:
        cls = result['classes'][path]
        n = len(result['by_path'].get(path, ()))
        out.append('PATH %-10s %s%s' % (
            cls, path, ' -> %d headings' % n if cls == 'PRICED' and path != SKILL else ''))
    for item in result['lost']:
        out.append('LOST L%d-%d %s [%s]' % (
            item['start'], item['end'], item['heading'] or '(preamble)', ';'.join(item['reasons'])))
    if result['already_uncovered']:
        out.append('NOTE: %d heading(s) already uncovered at base (not counted): %s' % (
            len(result['already_uncovered']),
            ', '.join('L%d' % s['start'] for s in result['already_uncovered'])))
    if result['skill_sections_edited']:
        out.append('NOTE: SKILL.md is dropped from input drift; edited sections are voided by their own '
                   'sha256. A line-count change also shifts every later page-local :NNN anchor (unpriced).')
    out.extend(result['notes'])
    return '\n'.join(out)


def diff_inputs(repo, base, other):
    names = git(repo, 'diff', '--name-only', '-z', '--no-renames', base, other)
    if names.returncode != 0:
        raise CouldNotEvaluate('git diff failed')
    paths = [n.decode('utf-8', 'surrogateescape') for n in names.stdout.split(b'\x00') if n]
    return sorted(paths)


def run(args):
    scratch = os.environ.get('TMPDIR')
    if scratch and (not os.path.isdir(scratch) or not os.access(scratch, os.W_OK)):
        raise CouldNotEvaluate('TMPDIR is not a usable directory: %r (could-not-evaluate)' % scratch)
    repo = args.lane
    rev = resolve_commit(repo, args.rev)
    if rev is None:
        if isinstance(args.rev, str) and args.rev.startswith('-'):
            raise Usage('--rev must not be option-like: %r' % args.rev)
        raise CouldNotEvaluate('--rev %r does not resolve in %s' % (args.rev, repo))
    model = Model(repo, rev)
    headings, lines = list(args.skill_section), list(args.skill_lines)
    if args.diff_to:
        other = resolve_commit(repo, args.diff_to)
        if other is None:
            raise CouldNotEvaluate('--diff-to %r does not resolve' % args.diff_to)
        paths = diff_inputs(repo, rev, other)
        other_model = Model(repo, other)
        result = diff_forecast(model, other_model, paths, strict=args.strict)
        text = json.dumps(result, indent=1, sort_keys=True) if args.json else render(result)
        try:
            print(text)
            sys.stdout.flush()
        except BrokenPipeError:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return result['exit']
    else:
        if not args.paths:
            raise Usage('--paths (or --diff-to) is required')
        paths = list(dict.fromkeys(args.paths))
    for path in paths:
        if not canonical_path(path):
            raise Usage('path is not a canonical lane-relative path: %r' % path)
    skill_idx, problems = skill_targets(model, headings, lines)
    if problems:
        raise CouldNotEvaluate('; '.join(problems))
    if skill_idx and SKILL not in paths:
        paths.append(SKILL)
    result = forecast(model, paths, skill_idx, strict=args.strict)
    text = json.dumps(result, indent=1, sort_keys=True) if args.json else render(result)
    try:
        print(text)
        sys.stdout.flush()
    except BrokenPipeError:
        # A reader that stops early (`| head -1`) is not an error of the forecast.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    return result['exit']


# --------------------------------------------------------------------------- selftest

def fx_git(repo, *argv):
    env = dict(GIT_ENV, GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    result = subprocess.run(['git', '-C', repo, '-c', 'user.name=fixture',
                             '-c', 'user.email=fixture@example.invalid'] + list(argv),
                            capture_output=True, env=env)
    if result.returncode != 0:
        raise RuntimeError('fixture git %s: %s' % (argv, result.stderr.decode()))
    return result.stdout.decode().strip()


FX_SKILL = '\n'.join([
    '# Top', '', 'intro', '', '## Alpha', '', 'alpha body', '', '## Beta', '', 'beta body', '',
    '## Gamma', '', 'gamma body', '', '## Delta', '', 'delta body', '', '## Epsilon', '', 'eps body', ''])


def fx_entry(section_text, inputs, verdict='executed-ok', cls='instruction', traces=None):
    return {'sha256': hashlib.sha256(section_text.encode()).hexdigest(), 'class': cls,
            'verdict': verdict, 'blocking_gaps': 0, 'wrong_expectations': 0,
            'commands_executed_count': 1,
            'inputs': {p: hashlib.sha256(c.encode()).hexdigest() for p, c in inputs.items()},
            'traces': traces if traces is not None else ['t/ok.json']}


def build_fixture(root):
    files = {
        'a.txt': 'file a\n', 'b.txt': 'file b\n', 'c.txt': 'file c\n', 'never.txt': 'pinned by nobody\n',
        'old.txt': 'stale pin\n', 'top.txt': 'top pin\n', 'SHONEN.md': '- [~] box\n', 'tools/mutate-and-run.sh': '#!/bin/sh\n',
        'corpus/SOURCES.md': 'sources\n',
        't/ok.json': json.dumps({'schema': TRACE_SCHEMA, 'inputs': {}, 'external': {},
                                 'live_lane_reads': {}}),
        SKILL: FX_SKILL,
    }
    secs = {s['heading']: s for s in sectionize(FX_SKILL.encode())}

    def text(heading):
        lines = FX_SKILL.split('\n')
        s = secs[heading]
        body = lines[s['start'] - 1:s['end']]
        while body and body[-1].strip() == '':
            body.pop()
        return '\n'.join(body)

    entries = [
        fx_entry(text('# Top'), {'top.txt': files['top.txt']}),
        fx_entry(text('## Alpha'), {'a.txt': files['a.txt']}),
        fx_entry(text('## Beta'), {'a.txt': files['a.txt']}),
        fx_entry(text('## Beta'), {'b.txt': files['b.txt']}),           # second reader
        fx_entry(text('## Gamma'), {'c.txt': files['c.txt'], 'a.txt': files['a.txt']}),
        fx_entry(text('## Delta'), {'b.txt': files['b.txt']}, verdict='gap-blocking'),  # base-uncovered
        fx_entry(text('## Delta'), {'b.txt': files['b.txt']}),          # clean reader, vetoed by the line above
        fx_entry('stale section text', {'old.txt': files['old.txt']}),  # matches no section
        fx_entry(text('## Epsilon'), {'SHONEN.md': files['SHONEN.md']}),
    ]
    files[LEDGER_PATH] = json.dumps({'schema': 'fx', 'entries': entries})
    for rel, content in files.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as handle:
            handle.write(content)
    fx_git(root, 'add', '-A')
    fx_git(root, 'commit', '-q', '-m', 'base')
    base = fx_git(root, 'rev-parse', 'HEAD')
    fx_git(root, 'checkout', '-q', '-b', 'edited')
    with open(os.path.join(root, 'a.txt'), 'a') as handle:
        handle.write('more\n')
    sk = FX_SKILL.replace('gamma body', 'gamma body CHANGED')
    with open(os.path.join(root, SKILL), 'w') as handle:
        handle.write(sk)
    fx_git(root, 'add', '-A')
    fx_git(root, 'commit', '-q', '-m', 'edit')
    tip = fx_git(root, 'rev-parse', 'HEAD')
    # a heading ADDED after base: no ledger entry matches its sha256
    fx_git(root, 'checkout', '-q', '-b', 'added', base)
    with open(os.path.join(root, SKILL), 'a') as handle:
        handle.write('\n## Zed\n\nzed body\n')
    fx_git(root, 'add', '-A')
    fx_git(root, 'commit', '-q', '-m', 'add heading')
    added = fx_git(root, 'rev-parse', 'HEAD')
    # a heading REMOVED after base: the page shrinks, no heading is lost
    fx_git(root, 'checkout', '-q', '-b', 'removed', base)
    with open(os.path.join(root, SKILL), 'w') as handle:
        handle.write(FX_SKILL.replace('## Epsilon\n\neps body\n', ''))
    fx_git(root, 'add', '-A')
    fx_git(root, 'commit', '-q', '-m', 'remove heading')
    removed = fx_git(root, 'rev-parse', 'HEAD')
    # SKILL.md deleted after base: the target rev cannot be measured at all
    fx_git(root, 'checkout', '-q', '-b', 'noskill', base)
    fx_git(root, 'rm', '-q', SKILL)
    fx_git(root, 'commit', '-q', '-m', 'delete SKILL')
    noskill = fx_git(root, 'rev-parse', 'HEAD')
    return base, tip, added, removed, noskill


def selftest():
    outcomes = []
    scratch = os.environ.get('TMPDIR')
    if scratch and (not os.path.isdir(scratch) or not os.access(scratch, os.W_OK)):
        print('COLDREAD_FORECAST_SCRATCH_UNUSABLE: TMPDIR is not a usable directory: %r (could-not-evaluate)' % scratch,
              file=sys.stderr)
        return 2
    me = os.path.abspath(__file__)
    with tempfile.TemporaryDirectory(prefix='cr-forecast-') as tmp:
        repo = os.path.join(tmp, 'repo')
        os.mkdir(repo)
        fx_git(repo, 'init', '-q')
        if fx_git(repo, 'rev-parse', '--show-toplevel') != os.path.realpath(repo):
            raise RuntimeError('fixture toplevel mismatch')
        base, tip, added, removed, noskill = build_fixture(repo)

        def cli(*argv, env=None):
            e = dict(os.environ, **(env or {}))
            r = subprocess.run([sys.executable, me, '--lane', repo] + list(argv),
                               capture_output=True, text=True, env=e)
            return r.returncode, r.stdout, r.stderr

        def jcli(*argv):
            code, out, err = cli(*argv, '--json')
            return code, (json.loads(out) if out.strip().startswith('{') else None), err

        def case(name, ok):
            outcomes.append((name, bool(ok)))

        code, res, _ = jcli('--rev', base, '--paths', 'a.txt')
        case('pinned edit: Alpha, Gamma lost; Beta survives on its second reader',
             code == 0 and [l['heading'] for l in res['lost']] == ['## Alpha', '## Gamma']
             and res['readers'] == 2 and res['base_covered'] == 5 and res['sections_total'] == 6)
        code, out, _ = cli('--rev', base, '--paths', 'a.txt', 'b.txt')
        case('both readers of Beta drift: Beta joins; header line grammar',
             code == 0 and out.splitlines()[0] == 'FORECAST: paths=2 headings=3 readers=3 of 6')
        code, res, _ = jcli('--rev', base, '--paths', 'never.txt', 'old.txt', 'brand-new.md')
        case('unpinned / stale-only / new path: 0 headings, exit 0, classes named',
             code == 0 and res['headings'] == 0 and res['classes'] == {
                 'never.txt': 'UNPINNED', 'old.txt': 'STALE-ONLY', 'brand-new.md': 'NEW'})
        code, res, _ = jcli('--rev', base, '--paths', 'never.txt', '--strict')
        case('--strict: unpinned tracked path exits 2', code == 2 and res['headings'] == 0)
        code, out, _ = cli('--rev', base, '--paths', SKILL)
        case('SKILL.md without a section: exit 2 FORECAST_UNPRICED, forecast still printed',
             code == 2 and 'FORECAST_UNPRICED: SKILL.md' in out and out.startswith('FORECAST: paths=1 headings=0'))
        code, res, _ = jcli('--rev', base, '--paths', SKILL, '--skill-section', '## Beta')
        case('SKILL.md + section: that heading voided by its own sha, exit 0',
             code == 0 and [l['heading'] for l in res['lost']] == ['## Beta']
             and res['lost'][0]['reasons'] == ['section-sha-void'])
        code, res, _ = jcli('--rev', base, '--paths', SKILL, '--skill-lines', '14')
        case('--skill-lines resolves to the covering section', code == 0 and [
            l['heading'] for l in res['lost']] == ['## Gamma'])
        code, out, err = cli('--rev', base, '--paths', SKILL, '--skill-section', '## Nope')
        case('unknown section heading: exit 2 SKILL_SECTION_NOT_FOUND',
             code == 2 and 'SKILL_SECTION_NOT_FOUND' in err)
        code, out, _ = cli('--rev', base, '--paths', LEDGER_PATH)
        case('the ledger file itself is a direct read nobody pins: exit 2', code == 2)
        code, res, _ = jcli('--rev', base, '--paths', 'SHONEN.md')
        case('direct-read path that an entry also pins is priced (Epsilon), exit 0',
             code == 0 and [l['heading'] for l in res['lost']] == ['## Epsilon'])
        code, res, _ = jcli('--rev', base, '--paths', 'b.txt')
        case('veto-eligible failing entry: Delta is already uncovered, never counted as lost',
             code == 0 and [d['heading'] for d in res['already_uncovered']] == ['## Delta']
             and all(l['heading'] != '## Delta' for l in res['lost']))
        code, res, _ = jcli('--rev', base, '--diff-to', tip)
        case('--diff-to: a.txt drift + edited Gamma section priced together',
             code == 0 and sorted(l['heading'] for l in res['lost']) == ['## Alpha', '## Gamma']
             and res['classes']['a.txt'] == 'PRICED')
        code, res, _ = jcli('--rev', base, '--diff-to', tip)
        case('--diff-to: the target rev is measured, not simulated (base vs target counts)',
             code == 0 and res['base_covered'] == 5 and res['target_covered'] == 3
             and res['target_sections_total'] == 6
             and res['target_rev'] == tip)
        code, res, _ = jcli('--rev', base, '--diff-to', added)
        case('--diff-to: a heading ADDED at the target has no ledger entry and is lost',
             code == 0 and [l['heading'] for l in res['lost']] == ['## Zed']
             and res['lost'][0]['reasons'] == ['no-ledger-entry'])
        code, res, _ = jcli('--rev', base, '--diff-to', removed)
        case('--diff-to: a heading REMOVED at the target is gone, not lost',
             code == 0 and res['lost'] == []
             and res['target_sections_total'] == 5)
        code, out, err = cli('--rev', base, '--diff-to', noskill)
        case('--diff-to with SKILL.md deleted at the target: exit 2, no traceback',
             code == 2 and 'Traceback' not in err and 'Traceback' not in out)
        code, _, err = cli('--rev', '--evil', '--paths', 'a.txt')
        case('option-like rev: exit 64', code == 64)
        code, _, err = cli('--rev', base, '--paths', '../x')
        case('non-canonical path: exit 64', code == 64)
        code, _, err = cli('--rev', 'deadbeef' * 5, '--paths', 'a.txt')
        case('unresolvable rev: exit 2', code == 2)
        code, _, err = cli('--rev', base, '--paths', 'a.txt', env={'TMPDIR': os.path.join(tmp, 'absent')})
        case('set-but-unusable TMPDIR: exit 2, never a silent /tmp fallback', code == 2 and 'TMPDIR' in err)
    for name, ok in outcomes:
        print('CASE', name, 'PASS' if ok else 'FAIL')
    passed = sum(ok for _, ok in outcomes)
    print('FORECAST_SELFTEST: %d/%d pass' % (passed, len(outcomes)))
    return 0 if passed == len(outcomes) else 1


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write('%s: error: %s\n' % (self.prog, message))
        raise SystemExit(64)


def main(argv):
    parser = Parser(description=__doc__.split('\n')[0])
    parser.add_argument('--lane', default=os.getcwd())
    parser.add_argument('--rev')
    parser.add_argument('--paths', nargs='+')
    parser.add_argument('--skill-section', action='append', default=[])
    parser.add_argument('--skill-lines', action='append', default=[])
    parser.add_argument('--diff-to')
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev:
        parser.error('--rev is required')
    try:
        return run(args)
    except Usage as exc:
        print('COLDREAD_FORECAST_USAGE: %s' % exc, file=sys.stderr)
        return 64
    except CouldNotEvaluate as exc:
        print('COLDREAD_FORECAST_COULD_NOT_EVALUATE: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
