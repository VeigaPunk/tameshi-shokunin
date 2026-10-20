#!/usr/bin/env python3
r"""C1+C2 counting command for tameshi round 18 (hyaku phase 2), v2 hardened.

Round-17 evolution of .ufo/evidence/round-16/measure.py: the sectionizer,
SHONEN census, depth and sources fields are byte-compatible with v1; the
coldread credit rule is the hardened input-keyed rule (R16-C2b + K02/K06/R05
critique closures).

Reads blobs via `git cat-file`/`git show` at an explicit commit only (no
worktree access) and prints one JSON object:

  recorded_cases   count of `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+` lines
                   (multiline) in tools/mutate-and-run.sh — the ledger comment
  depth_score      min(10, recorded_cases)
  ledger_legs      leg names captured from those lines
  shonen           mark census from `^- \[([x~ ])\] ` in SHONEN.md (boxes 1-4
                   in file order)
  coldread         SKILL.md parsed into sections (preamble + every #/##/###
                   heading outside ``` fences; section text = heading line
                   through the line before the next heading with trailing
                   blank (whitespace-only) lines stripped, joined by \n, no
                   trailing newline) matched by sha256 against the cold-read
                   ledger. Default ledger: REV:.ufo/evidence/round-18/
                   coldread/ledger.json; --ledger-file reads a local file,
                   --ledger-rev REV:PATH reads any pinned blob.
  calibration_restraint_score
                   2 * count of boxes 1,2,4 marked `~` + 2 * (box3 is `~`,
                   box3_full_page, and the SHONEN box-3 block at REV contains
                   `.ufo/evidence/round-18/coldread/ledger.json`)
  sources          corpus/SOURCES.md census: rows matching
                   `^\\|\\s*S[0-9]{3,}\\s*\\|` (see sources_census)

Credit rule (v2, fail-closed), evaluated per ledger entry in order:

  1. shape/findings: verdict must be one of the six strings; `gap-blocking`,
     `wrong-expectation`, `not-executed`, blocking_gaps>0 or
     wrong_expectations>0 are failures (int fields must be JSON ints, not
     booleans/numeric strings). A failing entry is veto-eligible.
  2. class gate (unchanged from v1): instruction credits on
     executed-ok|gap-minor with commands_executed_count>=1; record credits on
     verified-record|gap-minor.
  3. commands gate, class-independent: an entry credits only when
     commands_executed_count>0 AND it lists >=1 committed trace; a
     zero-command record cannot credit (`commands-unrecorded`), closing the
     record-class free-read hole (K02 hole 2). Malformed counts are
     `malformed-entry`.
  4. input gate, class-independent and applied to EVERY credited entry:
     `inputs` minus the ignored keys (SKILL.md and both the round-17 and
     round-18 ledger paths, which the section sha and ledger outputs cover)
     must be non-empty; every key must be a canonical lane-relative path (no
     `/` or `./`, no empty/`.`/`..`/`.git` component, no NUL); `git ls-tree
     REV -- <path>` must name exactly one entry with mode 100644/100755
     (directory/symlink/gitlink → `input-not-blob:<p>`, absent/renamed/
     untracked → `input-missing:<p>`); and `sha256(git cat-file blob
     REV:<p>)` must equal the recorded value (`input-drift:<p>`).
  5. trace gate: each trace path listed must resolve at REV to a blob whose
     JSON schema is `tameshi-trace-inputs-v1`, whose `inputs` are a subset of
     the entry's inputs with equal sha256 (`trace-input-unrecorded:<p>` for a
     key absent from the entry; `trace-input-drift:<p>` for a shared key with
     a different digest), whose `external` names no path under the live lane
     root, and whose `live_lane_reads` are bound to REV (`.git/` reads, or a blob with the
     recorded sha at REV; else `live-lane-read:<p>`); a
     missing/blobless trace is `trace-missing:<p>`, an unparseable or
     wrong-schema one `trace-invalid:<p>`. An entry with commands>0 and no
     traces is `traces-unrecorded` in strict mode.
     Strict mode applies when no override flag was given (the cited number).
     With --ledger-file/--ledger-rev/--inputs-overlay the run is a measurement
     aid (`overrides_used: true`, `trace_gate: "legacy"`): declared traces are
     still validated, but absent traces do not block credit (this is what
     lets a legacy red-before run credit at its read rev). A claim must never
     use overrides.
  6. aggregation, fail-closed: a section is covered iff at least one entry
     credits AND no veto-eligible entry exists whose inputs still all verify
     at REV (an entry with drifted/missing inputs is stale and does not veto;
     absent/empty inputs cannot prove staleness, so they veto). A clean entry
     never launders a failing one.

Per-section output: coldread.sections[] = {start, heading, credited, vetoed,
reason} plus a `reasons` histogram. Uncovered reasons are the deterministic,
`;`-joined, sorted union of the entries' first failure.
With --explain, each coldread.sections item also reports end and a sorted,
deduplicated reason list for its section.

--inputs-overlay FILE takes a JSON list of items that may set ONLY
start/skill_sha256/heading/inputs/read_rev/traces; any other key exits 2
`overlay-field-forbidden`. Items merge into matching ledger entries keyed by
(skill_sha256, start); merged count is reported as inputs_overlay_merged.

All git invocations scrub GIT_* from the environment; --rev and the REV part
of --ledger-rev are rejected when option-like (exit 64) and resolved with
`git rev-parse --verify --quiet --end-of-options X^{commit}` (exit 2 when
unresolvable); `revision` reports the resolved 40-hex commit and every blob
read uses it. Default --repo is the git toplevel containing this file.

Exits: 0 measured (a missing default ledger is a measured `no-ledger` state,
not an error) · 2 rev/required-blob missing, explicit --ledger-file/
--ledger-rev unreadable, or overlay unreadable/forbidden-field · 64 usage.

`--selftest` builds synthetic git repos in mkdtemp (fixture git runs with a
GIT_*-free environment) and proves the ported v1 cases plus every hardening
above, including the round-14 red-before (X10 overlay shape: credited at the
read rev, input-drift:tools/mutate-and-run.sh at a later rev). Stdlib only.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

DEFAULT_LEDGER_PATH = '.ufo/evidence/round-18/coldread/ledger.json'
LEDGER_PATH = DEFAULT_LEDGER_PATH
REQUIRED_BLOBS = (
    'tools/mutate-and-run.sh',
    'SHONEN.md',
    'SKILL.md',
    'corpus/SOURCES.md',
)
LEG_RE = re.compile(r'^#   ((?:js|bash)-\S+)\s+\S+\s+\d+/\d+', re.M)
BOX_RE = re.compile(r'^- \[([x~ ])\] (.*)$', re.M)
SOURCE_ROW_RE = re.compile(r'^\|\s*S[0-9]{3,}\s*\|')
HEADING_RE = re.compile(r'^#{1,3}(?:\s|$)')
FAIL_VERDICTS = frozenset(('gap-blocking', 'wrong-expectation', 'not-executed'))
EXEC_VERDICTS = frozenset(('executed-ok', 'gap-minor'))
REC_VERDICTS = frozenset(('verified-record', 'gap-minor'))
VALID_VERDICTS = frozenset(('executed-ok', 'verified-record', 'gap-minor',
                            'gap-blocking', 'wrong-expectation', 'not-executed'))
BLOB_MODES = frozenset(('100644', '100755'))
BOX3_LINK = DEFAULT_LEDGER_PATH
# Inputs that can never be verified by themselves: the page is already keyed
# by its section sha, and either round's ledger is its own output.
ROUND17_LEDGER_PATH = '.ufo/evidence/round-17/coldread/ledger.json'
IGNORED_INPUTS = frozenset(('SKILL.md', ROUND17_LEDGER_PATH,
                            DEFAULT_LEDGER_PATH))
LIVE_LANE_ROOT = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
OVERLAY_FIELDS = frozenset(('start', 'skill_sha256', 'heading', 'inputs',
                            'read_rev', 'traces'))
TRACE_SCHEMA = 'tameshi-trace-inputs-v1'
COMMIT_RE = re.compile(r'^[0-9a-f]{40}$')
# Every git call runs without inherited GIT_* (a stray GIT_DIR must not redirect
# the measurement; K02 hole 10 / N01 F1).
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write('%s: error: %s\n' % (self.prog, message))
        raise SystemExit(64)


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args),
                          capture_output=True, env=GIT_ENV)


def resolve_commit(repo, value):
    """Resolve VALUE to a 40-hex commit; None when option-like or unresolved."""
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


def blob(repo, rev, path):
    """Return raw bytes of REV:path, or None when the blob does not resolve.

    `git show` is only used for whole-file evidence (ledger/page); input
    verification always goes through cat_file_blob so a directory key can
    never masquerade as a blob (K02 hole 4).
    """
    result = git(repo, 'show', '%s:%s' % (rev, path))
    if result.returncode != 0:
        return None
    return result.stdout


def cat_file_blob(repo, rev, path):
    """Return blob bytes for REV:path, or None (tree/gitlink/missing)."""
    result = git(repo, 'cat-file', 'blob', '%s:%s' % (rev, path))
    if result.returncode != 0:
        return None
    return result.stdout


def ls_tree_mode(repo, rev, path):
    """Return the mode ('100644', '040000', '120000', …) of REV:path, or None."""
    result = git(repo, 'ls-tree', '-z', rev, '--', path)
    if result.returncode != 0:
        return None
    entries = [chunk for chunk in result.stdout.split(b'\x00') if chunk]
    if len(entries) != 1:
        return None
    meta = entries[0].split(b'\t', 1)[0]
    fields = meta.split(b' ')
    if len(fields) < 3:
        return None
    return fields[0].decode('ascii', 'surrogateescape')


def sectionize(raw):
    r"""Split SKILL.md bytes into sections: preamble + heading blocks.

    A heading is a line matching ^#{1,3}(\s|$) outside ``` fences. Section
    text is the heading line through the line before the next heading, with
    trailing blank (whitespace-only) lines stripped, joined with \n and no
    trailing newline; lines before the first heading form a preamble section
    whose heading is ''. Byte fidelity is kept with surrogateescape so the
    sha256 is over the original blob bytes.
    """
    text = raw.decode('utf-8', 'surrogateescape')
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    heads = []
    in_fence = False
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence and HEADING_RE.match(line):
            heads.append(i)
    pairs = []
    if heads:
        if heads[0] > 0:
            pairs.append((0, heads[0]))          # preamble
        for s, e in zip(heads, heads[1:] + [len(lines)]):
            pairs.append((s, e))
    else:
        pairs.append((0, len(lines)))            # whole file = preamble
    head_set = set(heads)
    sections = []
    for s, e in pairs:
        body_lines = list(lines[s:e])
        while body_lines and body_lines[-1].strip() == '':
            body_lines.pop()
        body = '\n'.join(body_lines)
        sections.append({
            'start': s + 1,
            'end': e,
            'heading': lines[s] if s in head_set else '',
            'sha256': hashlib.sha256(
                body.encode('utf-8', 'surrogateescape')).hexdigest(),
        })
    return sections


def shonen_boxes(raw):
    """Return [(mark, block)] per `- [m] ` checklist box, in order.

    A box's block is its own line plus the indented continuation lines right
    under it (SHONEN.md carries each box's evidence link on the continuation
    line). Round-16 L1 repair: the first version returned the box line only,
    so a link on the continuation line was never seen.
    """
    out, open_box = [], False
    for line in raw.decode('utf-8', 'surrogateescape').split('\n'):
        match = BOX_RE.match(line)
        if match:
            out.append([match.group(1), line])
            open_box = True
        elif open_box and line[:1] in (' ', '\t') and line.strip():
            out[-1][1] += '\n' + line
        else:
            open_box = False
    return [tuple(b) for b in out]


def sources_census(raw):
    text = raw.decode('utf-8', 'surrogateescape')
    rows, malformed, tiers, status = 0, 0, {}, {}
    for line in text.split('\n'):
        if not SOURCE_ROW_RE.match(line):
            continue
        rows += 1
        fields = line.split('|')
        if len(fields) != 13:
            malformed += 1
            continue
        tier = re.sub(r'\s', '', fields[4])
        stat = re.sub(r'\s', '', fields[8])
        tiers[tier] = tiers.get(tier, 0) + 1
        status[stat] = status.get(stat, 0) + 1
    return {'rows': rows, 'malformed': malformed,
            'tiers': dict(sorted(tiers.items())),
            'status': dict(sorted(status.items()))}


def json_int(value):
    """Return VALUE when it is a JSON integer >= 0, else None (bool rejected)."""
    if type(value) is not int or value < 0:
        return None
    return value


def canonical_lane_path(path):
    """True for a canonical lane-relative path (deterministic reason strings)."""
    if not isinstance(path, str) or not path:
        return False
    if '\x00' in path:
        return False
    try:
        path.encode('utf-8')
    except UnicodeEncodeError:
        return False
    if path.startswith('/') or path.startswith('./'):
        return False
    if any(part in ('', '.', '..', '.git') for part in path.split('/')):
        return False
    return True


def inputs_view(entry):
    """Entry inputs minus the self-referential keys, or None when not a dict."""
    raw = entry.get('inputs')
    if not isinstance(raw, dict):
        return None
    return {path: value for path, value in raw.items()
            if path not in IGNORED_INPUTS}


def input_failures(repo, rev, view):
    """Per-input failure reasons for an inputs view, sorted deterministically."""
    fails = []
    for path in sorted(view, key=lambda item: (str(type(item)), str(item))):
        if not canonical_lane_path(path):
            fails.append('input-not-blob:%s' % path)
            continue
        mode = ls_tree_mode(repo, rev, path)
        if mode is None:
            fails.append('input-missing:%s' % path)
            continue
        if mode not in BLOB_MODES:
            fails.append('input-not-blob:%s' % path)
            continue
        data = cat_file_blob(repo, rev, path)
        if data is None:
            fails.append('input-missing:%s' % path)
            continue
        if hashlib.sha256(data).hexdigest() != view[path]:
            fails.append('input-drift:%s' % path)
    return fails


def input_reason(repo, rev, entry):
    """Class-independent input gate; None when every recorded input verifies."""
    view = inputs_view(entry)
    if view is None or not view:
        return 'inputs-unrecorded'
    fails = input_failures(repo, rev, view)
    return ';'.join(fails) if fails else None


def under_live_lane(path):
    if not isinstance(path, str) or not path:
        return False
    try:
        real = os.path.realpath(path)
    except OSError:
        return False
    root = os.path.realpath(LIVE_LANE_ROOT)
    return real == root or real.startswith(root + os.sep)


def trace_reason(repo, rev, entry, strict):
    """Bind recorded inputs to committed trace receipts (never argv to commands); None when satisfied/na.

    Strict mode (no overrides: the cited number) requires >=1 receipt for an
    entry with commands_executed_count>0. Legacy mode (measurement aid) skips
    absent receipts but still validates every declared one.
    """
    cmd = json_int(entry.get('commands_executed_count', 0))
    if cmd is None:
        return 'malformed-entry'
    traces = entry.get('traces')
    if traces is None or traces == []:
        return 'traces-unrecorded' if strict and cmd > 0 else None
    if not isinstance(traces, list):
        return 'traces-unrecorded'
    if cmd <= 0:
        return None
    view = inputs_view(entry)
    if view is None:
        view = {}
    for path in sorted(traces, key=str):
        if not canonical_lane_path(path):
            return 'trace-missing:%s' % path
        mode = ls_tree_mode(repo, rev, path)
        if mode is None or mode not in BLOB_MODES:
            return 'trace-missing:%s' % path
        raw = cat_file_blob(repo, rev, path)
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
        live_reads = receipt.get('live_lane_reads')
        if isinstance(live_reads, dict) and live_reads:
            for key in sorted(live_reads, key=str):
                if not live_read_bound(repo, rev, key, live_reads[key]):
                    return 'live-lane-read:%s' % key
        external = receipt.get('external')
        if isinstance(external, dict):
            for key in sorted(external, key=str):
                if under_live_lane(key) and not live_read_bound(
                        repo, rev, key, external[key]):
                    return 'live-lane-read:%s' % key
    return None


def live_read_bound(repo, rev, path, digest):
    """A read of the live lane counts as a read of REV only when it is bound.

    Round-17 wave-2 refinement: object-store/ref reads under the lane's
    `.git/` come from rev-addressed commands (`git show REV:path`) and are
    accepted as such; any other live file is accepted only when it is a
    regular blob at REV with exactly the recorded sha256 (the bytes read are
    the measured bytes). Everything else stays `live-lane-read:`.
    """
    if not isinstance(path, str) or not isinstance(digest, str):
        return False
    root = os.path.realpath(LIVE_LANE_ROOT)
    real = os.path.realpath(path)
    if not (real == root or real.startswith(root + os.sep)):
        return False
    rel = os.path.relpath(real, root).replace(os.sep, '/')
    if rel == '.git' or rel.startswith('.git/'):
        return True
    if not canonical_lane_path(rel):
        return False
    mode = ls_tree_mode(repo, rev, rel)
    if mode is None or mode not in BLOB_MODES:
        return False
    raw = cat_file_blob(repo, rev, rel)
    return raw is not None and hashlib.sha256(raw).hexdigest() == digest


def entry_failure(entry):
    """Veto-eligible failure (findings/shape); None when the entry is not failing."""
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
    """Class gate only; return None when the entry passes the v1 credit rule."""
    verdict = entry.get('verdict')
    if not isinstance(verdict, str) or verdict not in VALID_VERDICTS:
        return 'verdict:%s' % verdict
    if verdict in FAIL_VERDICTS:
        return 'verdict:%s' % verdict
    try:
        bg = entry.get('blocking_gaps', 0)
        we = entry.get('wrong_expectations', 0)
    except AttributeError:
        return 'malformed-entry'
    if json_int(bg) is None or json_int(we) is None:
        return 'malformed-entry'
    if bg != 0:
        return 'blocking-gaps:%d' % bg
    if we != 0:
        return 'wrong-expectations:%d' % we
    cls = entry.get('class')
    if cls == 'instruction':
        if verdict not in EXEC_VERDICTS:
            return 'verdict-class:%s/instruction' % verdict
        cmd_count = json_int(entry.get('commands_executed_count', 0))
        if cmd_count is None:
            return 'malformed-entry'
        if cmd_count <= 0:
            return 'commands-executed-count:%s' % (
                entry.get('commands_executed_count'))
        return None
    if cls == 'record':
        if verdict in REC_VERDICTS:
            return None
        return 'verdict-class:%s/record' % verdict
    return 'class:%s' % cls


def entry_reason(repo, rev, entry, strict):
    """Full per-entry reason: findings, class, inputs, traces (first failure)."""
    reason = entry_failure(entry)
    if reason is not None:
        return reason
    reason = entry_credit_reason(entry)
    if reason is not None:
        return reason
    if json_int(entry.get('commands_executed_count', 0)) == 0:
        return 'commands-unrecorded'
    reason = input_reason(repo, rev, entry)
    if reason is not None:
        return reason
    return trace_reason(repo, rev, entry, strict)

def entry_is_stale(repo, rev, entry):
    """True when at least one recorded input fails to verify at REV.

    Absent/empty/non-dict inputs prove nothing, so such an entry is NOT stale
    and its failure vetoes credit (fail-closed).
    """
    view = inputs_view(entry)
    if view is None or not view:
        return False
    return bool(input_failures(repo, rev, view))


def section_record(sec, credited, vetoed, reason, reasons, explain):
    result = {'start': sec['start'], 'heading': sec['heading'],
              'credited': credited, 'vetoed': vetoed, 'reason': reason}
    if explain:
        result['end'] = sec['end']
        result['reasons'] = sorted(set(reasons))
    return result


def coldread(repo, rev, skill_raw, ledger_raw, overlay=None, strict=True,
             explain=False):
    sections = sectionize(skill_raw)
    out = {'sections_total': len(sections), 'sections_covered': 0,
           'box3_full_page': False, 'missing': [], 'uncovered_headings': [],
           'sections': [], 'reasons': {}, 'external_inputs': {},
           'inputs_overlay_merged': 0}
    if ledger_raw is None:
        out['ledger_present'] = False
        for sec in sections:
            out['missing'].append({'start': sec['start'],
                                   'heading': sec['heading'],
                                   'reason': 'no-ledger'})
            out['uncovered_headings'].append(sec['heading'])
            out['sections'].append(section_record(
                sec, False, False, 'no-ledger', ['no-ledger'], explain))
        out['reasons']['no-ledger'] = len(sections)
        return out
    out['ledger_present'] = True
    try:
        ledger = json.loads(ledger_raw.decode('utf-8', 'surrogateescape'))
        entries = ledger['entries']
        assert isinstance(entries, list)
    except Exception as exc:
        out['ledger_error'] = '%s: %s' % (type(exc).__name__, exc)
        for sec in sections:
            out['missing'].append({'start': sec['start'],
                                   'heading': sec['heading'],
                                   'reason': 'invalid-ledger'})
            out['uncovered_headings'].append(sec['heading'])
            out['sections'].append(section_record(
                sec, False, False, 'invalid-ledger', ['invalid-ledger'],
                explain))
        out['reasons']['invalid-ledger'] = len(sections)
        return out
    if overlay:
        index = {}
        for item in overlay:
            if isinstance(item, dict):
                index[(item.get('skill_sha256'), item.get('start'))] = item
        merged = []
        for entry in entries:
            key = None
            if isinstance(entry, dict):
                key = (entry.get('skill_sha256'), entry.get('start'))
            if key in index:
                new_entry = dict(entry)
                new_entry.update(index[key])
                merged.append(new_entry)
                out['inputs_overlay_merged'] += 1
            else:
                merged.append(entry)
        entries = merged
    by_sha = {}
    for entry in entries:
        if isinstance(entry, dict):
            ext = entry.get('external_inputs')
            if isinstance(ext, dict):
                for path, sha in ext.items():
                    out['external_inputs'][path] = sha
            if isinstance(entry.get('sha256'), str):
                by_sha.setdefault(entry['sha256'], []).append(entry)
    for sec in sections:
        matches = by_sha.get(sec['sha256'], [])
        if not matches:
            reason = 'no-ledger-entry'
            out['missing'].append({'start': sec['start'],
                                   'heading': sec['heading'],
                                   'reason': reason})
            out['uncovered_headings'].append(sec['heading'])
            out['sections'].append(section_record(
                sec, False, False, reason, [reason], explain))
            out['reasons'][reason] = out['reasons'].get(reason, 0) + 1
            continue
        reasons = []
        explanation_reasons = []
        credited = 0
        vetoes = []
        for entry in matches:
            reason = entry_reason(repo, rev, entry, strict)
            if reason is None:
                credited += 1
                explanation_reasons.append('credited')
            else:
                reasons.append(reason)
                explanation_reasons.append(reason)
            if entry_failure(entry) is not None and not entry_is_stale(
                    repo, rev, entry):
                vetoes.append(reason)
        covered = credited > 0 and not vetoes
        if covered:
            reason = 'credited'
            out['sections_covered'] += 1
        else:
            if not reasons:
                reasons = ['no-ledger-entry']
            reason = ';'.join(sorted(set(reasons)))
            out['missing'].append({'start': sec['start'],
                                   'heading': sec['heading'],
                                   'reason': reason})
            out['uncovered_headings'].append(sec['heading'])
        if not explanation_reasons:
            explanation_reasons = ['no-ledger-entry']
        out['sections'].append(section_record(
            sec, covered, bool(vetoes), reason, explanation_reasons, explain))
        out['reasons'][reason] = out['reasons'].get(reason, 0) + 1
    out['box3_full_page'] = out['sections_covered'] == out['sections_total']
    return out


def measure(repo, rev, ledger_raw, overlay=None, overrides_used=False,
            ledger_source='rev', ledger_committed=False, rev_input=None,
            explain=False):
    runner = blob(repo, rev, 'tools/mutate-and-run.sh')
    boxes = shonen_boxes(blob(repo, rev, 'SHONEN.md'))
    marks = [mark for mark, _line in boxes]
    skill = blob(repo, rev, 'SKILL.md')
    sources = sources_census(blob(repo, rev, 'corpus/SOURCES.md'))
    legs = LEG_RE.findall(runner.decode('utf-8', 'surrogateescape'))
    rtext = runner.decode('utf-8', 'surrogateescape')
    # Guardrail (round-16 w2 DepthCritic): command D counts header comment
    # lines only; report whether the header, the regression call sites and
    # the selftest leg tuples agree, and how many distinct gate paths the
    # header names. These fields do not change depth_score.
    leg_calls = len(re.findall(r'^  regression_case_git (?:js|bash)-', rtext, re.M))
    leg_tuples = len(re.findall(r"^    '(?:js|bash)-[^:]+:[^:]+\.spec:TABLE_", rtext, re.M))
    gate_paths = re.findall(r'^#   (?:js|bash)-\S+\s+(\S+)\s+\d+/\d+', rtext, re.M)
    strict = not overrides_used
    cr = coldread(repo, rev, skill, ledger_raw, overlay=overlay, strict=strict,
                  explain=explain)
    box3_marked = len(marks) >= 3 and marks[2] == '~'
    box3_link = len(boxes) >= 3 and BOX3_LINK in boxes[2][1]
    box3_points = box3_marked and box3_link and cr['box3_full_page']
    restraint = 2 * sum(len(marks) >= b and marks[b - 1] == '~'
                        for b in (1, 2, 4)) + 2 * box3_points
    return {
        'revision': rev,
        'rev_input': rev_input,
        'recorded_cases': len(legs),
        'depth_score': min(10, len(legs)),
        'ledger_legs': legs,
        'ledger_guardrail': {
            'header_legs': len(legs), 'regression_calls': leg_calls,
            'selftest_tuples': leg_tuples,
            'lists_agree': len(legs) == leg_calls == leg_tuples,
            'unique_recorded_gates': len(set(gate_paths)),
        },
        'shonen': {
            'boxes': len(marks),
            'marks': marks,
            'checked': marks.count('x'),
            'asserted': marks.count('~'),
            'untouched': marks.count(' '),
            'box3_marked': box3_marked,
            'box3_ledger_link': box3_link,
            'box3_points': box3_points,
        },
        'coldread': cr,
        'calibration_restraint_score': restraint,
        'sources': sources,
        'overrides_used': bool(overrides_used),
        'trace_gate': 'strict' if strict else 'legacy',
        'ledger_source': ledger_source,
        'ledger_committed': bool(ledger_committed),
    }


SKILL_LINES = [
    '---',
    'name: syn-skill',
    '---',
    '',
    'Intro line before first heading.',
    '',
    '# Alpha',
    '',
    'alpha body',
    '',
    '## Beta',
    '',
    '```',
    '# hidden-heading-inside-fence',
    '```',
    '',
    'beta body',
    '',
    '### Gamma',
    '',
    'gamma body',
]
SHONEN_BOX3 = '- [~] box three — evidence .ufo/evidence/round-18/coldread/ledger.json'
SHONEN_TEXT = '\n'.join([
    '# syn promotion checklist',
    '',
    '- [~] box one',
    '- [~] box two',
    SHONEN_BOX3,
    '- [~] box four',
]) + '\n'
SHONEN_NOLINK_TEXT = SHONEN_TEXT.replace(SHONEN_BOX3, '- [~] box three')
SHONEN_CONT_TEXT = SHONEN_TEXT.replace(
    SHONEN_BOX3, '- [~] box three\n  [lane assertion](.ufo/evidence/round-18/coldread/ledger.json)')
SHONEN_WRONGBOX_TEXT = SHONEN_NOLINK_TEXT.replace(
    '- [~] box four', '- [~] box four\n  [link](.ufo/evidence/round-18/coldread/ledger.json)')
SHONEN_OLDLINK_TEXT = SHONEN_TEXT.replace(
    DEFAULT_LEDGER_PATH, ROUND17_LEDGER_PATH)
RUNNER_TEXT = '\n'.join([
    '#!/bin/sh',
    '# ledger legs:',
    '#   js-syn-aaa   repo/a.mjs   8/10 (80 %)',
    '#   bash-syn-bbb repo/b.sh   4/10 (40 %)',
]) + '\n'
SOURCES_TEXT = '\n'.join([
    '# syn sources',
    '',
    '| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |',
    '|---|---|---|---|---|---|---|---|---|---|---|',
    '| S001 | x | docs | A | s | a | t | mined | 2026-10-20 | 90d | — |',
    '| S002 | y | paper | B | s | a | t | queued | 2026-10-20 | 90d | — |',
]) + '\n'
INPUT_FILE = 'corpus/inputs/obs.txt'
INPUT_V1 = 'observed value v1\n'
INPUT_V2 = 'observed value v2\n'
INPUT_V1_SHA = hashlib.sha256(INPUT_V1.encode()).hexdigest()
INPUT_V2_SHA = hashlib.sha256(INPUT_V2.encode()).hexdigest()
INPUT_MISSING = 'corpus/inputs/absent.txt'
TRACE_PATH = '.ufo/evidence/round-17/coldread/traces/syn.json'
TRACE_BAD_PATH = '.ufo/evidence/round-17/coldread/traces/bad.json'
TRACE_EXTRA_PATH = '.ufo/evidence/round-17/coldread/traces/extra.json'
TRACE_LIVE_PATH = '.ufo/evidence/round-17/coldread/traces/live.json'
TRACE_EXT_PATH = '.ufo/evidence/round-17/coldread/traces/live-ext.json'
TRACE_LIVE_BOUND_PATH = '.ufo/evidence/round-17/coldread/traces/live-bound.json'
TRACE_DRIFT_PATH = '.ufo/evidence/round-17/coldread/traces/drift.json'
SYMLINK_PATH = 'link-syn'


def trace_receipt(inputs, external=None, live_lane_reads=None,
                  schema=TRACE_SCHEMA):
    return json.dumps({
        'schema': schema,
        'argv': ['cat', INPUT_FILE],
        'cwd': '.',
        'root': '/tmp/synthetic-root',
        'rev': 'f' * 40,
        'exit': 0,
        'inputs': inputs,
        'external': external or {},
        'live_lane_reads': live_lane_reads or {},
    }) + '\n'


# Section texts for the ledger, sliced literally from SKILL_LINES with
# trailing blank lines stripped, so the selftest does not reuse sectionize()
# to produce its own expectation.
def _strip_tail(slice_lines):
    while slice_lines and slice_lines[-1].strip() == '':
        slice_lines.pop()
    return '\n'.join(slice_lines)


SYNTH_SECTIONS = [
    (1, '', _strip_tail(SKILL_LINES[0:6])),
    (7, '# Alpha', _strip_tail(SKILL_LINES[6:10])),
    (11, '## Beta', _strip_tail(SKILL_LINES[10:18])),
    (19, '### Gamma', _strip_tail(SKILL_LINES[18:21])),
]


def synth_entry(index, inputs_mode='default', commands=1, traces=True,
                cls='instruction', verdict='executed-ok'):
    start, heading, text = SYNTH_SECTIONS[index]
    entry = {
        'skill_sha256': 'deadbeef',
        'start': start,
        'end': start + len(text.split('\n')) - 1,
        'heading': heading,
        'sha256': hashlib.sha256(text.encode()).hexdigest(),
        'class': cls,
        'verdict': verdict,
        'blocking_gaps': 0,
        'wrong_expectations': 0,
        'commands_executed_count': commands,
        'read_rev': 'f' * 40,
    }
    if inputs_mode == 'default':
        entry['inputs'] = {INPUT_FILE: INPUT_V1_SHA}
    elif inputs_mode == 'missing':
        entry['inputs'] = {INPUT_MISSING: INPUT_V1_SHA}
    elif inputs_mode == 'dir':
        entry['inputs'] = {'tools': INPUT_V1_SHA}
    elif inputs_mode == 'symlink':
        entry['inputs'] = {SYMLINK_PATH: INPUT_V1_SHA}
    elif inputs_mode == 'skill-only':
        entry['inputs'] = {'SKILL.md': 'a' * 64}
    elif inputs_mode == 'ledger-only':
        entry['inputs'] = {DEFAULT_LEDGER_PATH: 'a' * 64}
    elif inputs_mode == 'skill-and-file':
        entry['inputs'] = {'SKILL.md': 'a' * 64, INPUT_FILE: INPUT_V1_SHA}
    elif inputs_mode == 'stale-file':
        entry['inputs'] = {INPUT_FILE: INPUT_V2_SHA}
    if traces:
        entry['traces'] = [TRACE_PATH]
    return entry


def ledger_json(entries=None, drop=None, blocking=None, changed=None,
                inputs_mode='default', commands=1, traces=True):
    if entries is not None:
        return json.dumps({'schema': 'tameshi-coldread-ledger-v2',
                           'entries': entries}, indent=2) + '\n'
    built = []
    for i, (start, heading, text) in enumerate(SYNTH_SECTIONS):
        if i == drop:
            continue
        entry = synth_entry(i, inputs_mode=inputs_mode, commands=commands,
                            traces=traces)
        if i == blocking:
            entry['blocking_gaps'] = 1
        if i == changed:
            entry['sha256'] = hashlib.sha256((text + ' CHANGED').encode()).hexdigest()
        built.append(entry)
    return json.dumps({'schema': 'tameshi-coldread-ledger-v2',
                       'entries': built}, indent=2) + '\n'


def dupe_ledger(second_overrides, first_overrides=None, index=3):
    """Ledger with two entries for one section sha (aggregation cases)."""
    first = synth_entry(index, **(first_overrides or {}))
    second = synth_entry(index, **second_overrides)
    entries = [synth_entry(i) for i, _s in enumerate(SYNTH_SECTIONS)
               if i != index]
    entries.extend([first, second])
    return ledger_json(entries=entries)


def selftest():
    script = os.path.abspath(__file__)
    tmp = tempfile.mkdtemp(prefix='tameshi-r17-MeasureV2-')
    base_env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env = dict(base_env, HOME=tmp)

    def run(*args, cwd=None, extra_env=None):
        run_env = dict(env)
        if extra_env:
            run_env.update(extra_env)
        return subprocess.run(args, capture_output=True, text=True,
                              cwd=cwd, env=run_env)

    def git_in(repo, *args):
        return run('git', '-C', repo, *args)

    def write_file(repo, rel, content):
        path = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

    def commit(repo, label):
        git_in(repo, 'add', '-A')
        res = git_in(repo, 'commit', '-qm', label)
        assert res.returncode == 0, res.stderr
        return git_in(repo, 'rev-parse', 'HEAD').stdout.strip()

    def call_measure(repo, rev, *extra, cwd=None, extra_env=None):
        return run(sys.executable or 'python3', script,
                   '--rev', rev, '--repo', repo, *extra,
                   cwd=cwd, extra_env=extra_env)

    repo = os.path.join(tmp, 'synrepo')
    os.makedirs(repo)
    init = git_in(repo, 'init', '-q')
    assert init.returncode == 0, init.stderr
    git_in(repo, 'config', 'user.name', 't')
    git_in(repo, 'config', 'user.email', 't@t')

    checks = []

    def check(name, cond, detail=''):
        checks.append((name, bool(cond), detail))
        print('%s %s %s' % ('PASS' if cond else 'FAIL', name, detail))

    write_file(repo, 'tools/mutate-and-run.sh', RUNNER_TEXT)
    write_file(repo, 'SHONEN.md', SHONEN_TEXT)
    write_file(repo, 'SKILL.md', '\n'.join(SKILL_LINES) + '\n')
    write_file(repo, 'corpus/SOURCES.md', SOURCES_TEXT)
    write_file(repo, INPUT_FILE, INPUT_V1)
    write_file(repo, TRACE_PATH, trace_receipt({INPUT_FILE: INPUT_V1_SHA}))
    write_file(repo, TRACE_BAD_PATH, '{"schema": "other", "inputs": {}}\n')
    write_file(repo, TRACE_EXTRA_PATH, trace_receipt(
        {INPUT_FILE: INPUT_V1_SHA, 'corpus/SOURCES.md': 'b' * 64}))
    write_file(repo, TRACE_DRIFT_PATH, trace_receipt(
        {INPUT_FILE: INPUT_V2_SHA}))
    write_file(repo, TRACE_LIVE_PATH, trace_receipt(
        {INPUT_FILE: INPUT_V1_SHA},
        live_lane_reads={os.path.join(LIVE_LANE_ROOT, 'SKILL.md'): 'c' * 64}))
    write_file(repo, TRACE_EXT_PATH, trace_receipt(
        {INPUT_FILE: INPUT_V1_SHA},
        external={os.path.join(LIVE_LANE_ROOT, 'SKILL.md'): 'c' * 64}))
    write_file(repo, TRACE_LIVE_BOUND_PATH, trace_receipt(
        {INPUT_FILE: INPUT_V1_SHA},
        live_lane_reads={os.path.join(LIVE_LANE_ROOT, INPUT_FILE): INPUT_V1_SHA,
                         os.path.join(LIVE_LANE_ROOT, '.git/HEAD'): 'd' * 64}))
    os.symlink(INPUT_FILE, os.path.join(repo, SYMLINK_PATH))
    rev_base = commit(repo, 'base, no ledger')

    # --- case: no ledger -> box3 false, restraint 6 ------------------------------
    res = call_measure(repo, rev_base)
    check('exit0-no-ledger', res.returncode == 0, res.stderr.strip()[:200])
    out = json.loads(res.stdout) if res.returncode == 0 else {}
    check('no-ledger-depth', out.get('recorded_cases') == 2
          and out.get('depth_score') == 2
          and out.get('ledger_legs') == ['js-syn-aaa', 'bash-syn-bbb'])
    check('no-ledger-marks', out.get('shonen', {}).get('marks') == ['~'] * 4)
    check('no-ledger-sections', out.get('coldread', {}).get('sections_total') == 4,
          'fence-hidden heading excluded, preamble counted')
    check('no-ledger-box3-false',
          out.get('coldread', {}).get('box3_full_page') is False
          and out.get('coldread', {}).get('ledger_present') is False)
    check('no-ledger-score-6', out.get('calibration_restraint_score') == 6)
    check('no-ledger-sources', out.get('sources') == {
        'rows': 2, 'malformed': 0,
        'tiers': {'A': 1, 'B': 1},
        'status': {'mined': 1, 'queued': 1}})
    check('no-ledger-reasons',
          out.get('coldread', {}).get('reasons') == {'no-ledger': 4})
    check('no-ledger-strict', out.get('trace_gate') == 'strict'
          and out.get('overrides_used') is False
          and out.get('ledger_committed') is False)

    # --- case: complete ledger -> 8 --------------------------------------------
    write_file(repo, LEDGER_PATH, ledger_json())
    rev_full = commit(repo, 'complete ledger')
    res = call_measure(repo, rev_full)
    out = json.loads(res.stdout)
    check('full-ledger-covered', out['coldread']['sections_covered'] == 4
          and out['coldread']['sections_total'] == 4
          and out['coldread']['missing'] == [])
    check('full-ledger-box3', out['coldread']['box3_full_page'] is True)
    check('full-ledger-score-8', out['calibration_restraint_score'] == 8)
    check('full-ledger-section-reasons',
          out['coldread']['reasons'] == {'credited': 4}
          and all(s['credited'] and s['reason'] == 'credited'
                  for s in out['coldread']['sections']))
    check('full-ledger-committed', out['ledger_committed'] is True
          and out['ledger_source'] == 'rev')
    # A round-17 ledger link does not satisfy the round-18 box-3 requirement.
    write_file(repo, 'SHONEN.md', SHONEN_OLDLINK_TEXT)
    rev_oldlink = commit(repo, 'box3 still links round-17 ledger')
    out = json.loads(call_measure(repo, rev_oldlink).stdout)
    check('old-link-does-not-credit-box3',
          out['shonen']['box3_ledger_link'] is False
          and out['calibration_restraint_score'] == 6)
    write_file(repo, 'SHONEN.md', SHONEN_TEXT)

    # --explain reports each synthetic section's bounds and credit reasons.
    res = call_measure(repo, rev_full, '--explain')
    out = json.loads(res.stdout)
    detail = out['coldread']['sections'][2]
    check('explain-section-shape',
          res.returncode == 0 and detail['credited'] is True
          and detail['reasons'] == ['credited']
          and detail['start'] == 11 and detail['end'] == 18
          and detail['heading'] == '## Beta')

    # --- case: one section missing -> 6 ----------------------------------------
    write_file(repo, LEDGER_PATH, ledger_json(drop=3))
    rev_miss = commit(repo, 'gamma entry absent')
    out = json.loads(call_measure(repo, rev_miss).stdout)
    check('missing-section-covered3', out['coldread']['sections_covered'] == 3)
    check('missing-section-box3', out['coldread']['box3_full_page'] is False)
    check('missing-section-heading',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma', 'reason': 'no-ledger-entry'}])
    check('missing-section-score-6', out['calibration_restraint_score'] == 6)

    # --- case: one gap-blocking -> 6 (veto) ------------------------------------
    write_file(repo, LEDGER_PATH, ledger_json(blocking=3))
    rev_block = commit(repo, 'gamma blocking')
    out = json.loads(call_measure(repo, rev_block).stdout)
    check('blocking-covered3', out['coldread']['sections_covered'] == 3)
    check('blocking-reason',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma', 'reason': 'blocking-gaps:1'}])
    check('blocking-vetoed', out['coldread']['sections'][3]['vetoed'] is True)
    check('blocking-score-6', out['calibration_restraint_score'] == 6)

    # --- case: one section byte changed -> 6 -----------------------------------
    write_file(repo, LEDGER_PATH, ledger_json(changed=3))
    rev_byte = commit(repo, 'gamma sha over changed bytes')
    out = json.loads(call_measure(repo, rev_byte).stdout)
    check('bytechange-covered3', out['coldread']['sections_covered'] == 3)
    check('bytechange-reason',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma', 'reason': 'no-ledger-entry'}])
    check('bytechange-score-6', out['calibration_restraint_score'] == 6)

    # --- case: uncredited verdict also fails coverage ---------------------------
    bad = json.loads(ledger_json())
    bad['entries'][3]['verdict'] = 'gap-blocking'
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    rev_verdict = commit(repo, 'gamma gap-blocking verdict')
    out = json.loads(call_measure(repo, rev_verdict).stdout)
    check('badverdict-score-6', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason'] == 'verdict:gap-blocking')

    # --- case: unknown verdict is failing too -----------------------------------
    bad = json.loads(ledger_json())
    bad['entries'][3]['verdict'] = 'probably-fine'
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'gamma odd verdict')).stdout)
    check('oddverdict-vetoed', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason'] == 'verdict:probably-fine')

    # --- case: instruction entry with zero commands -> no credit ----------------
    bad = json.loads(ledger_json())
    bad['entries'][3]['commands_executed_count'] = 0
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    rev_nocmd = commit(repo, 'gamma zero commands')
    out = json.loads(call_measure(repo, rev_nocmd).stdout)
    check('nocmd-score-6', out['calibration_restraint_score'] == 6)
    check('nocmd-reason',
          out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma',
               'reason': 'commands-executed-count:0'}])

    # --- case: instruction class + verified-record verdict -> no credit ---------
    bad = json.loads(ledger_json())
    bad['entries'][3]['verdict'] = 'verified-record'
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    rev_misverd = commit(repo, 'gamma instruction verified-record')
    out = json.loads(call_measure(repo, rev_misverd).stdout)
    check('instr-verified-nocredit',
          out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason']
          == 'verdict-class:verified-record/instruction')
    # --- case: record + verified-record + zero commands -> commands-unrecorded --
    # The commands gate is class-independent: a zero-command record can no
    # longer credit (K02 hole 2 / LessonReview F1), even with verified inputs.
    rec = json.loads(ledger_json(commands=0, inputs_mode='default'))
    for e in rec['entries']:
        e['class'] = 'record'
        e['verdict'] = 'verified-record'
    write_file(repo, LEDGER_PATH, json.dumps(rec) + '\n')
    rev_rec = commit(repo, 'record verified-record zero commands with input')
    out = json.loads(call_measure(repo, rev_rec).stdout)
    check('record-zero-cmd-commands-unrecorded',
          out['calibration_restraint_score'] == 6
          and out['coldread']['reasons'] == {'commands-unrecorded': 4}
          and out['coldread']['sections_covered'] == 0)

    # --- case: record + verified-record + zero commands + NO inputs -> 6 --------
    rec = json.loads(ledger_json(commands=0, inputs_mode='none'))
    for e in rec['entries']:
        e['class'] = 'record'
        e['verdict'] = 'verified-record'
    write_file(repo, LEDGER_PATH, json.dumps(rec) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'record no inputs')).stdout)
    check('record-zero-cmd-no-input-uncredited',
          out['calibration_restraint_score'] == 6
          and out['coldread']['reasons'] == {'commands-unrecorded': 4})

    # --- case: record + verified-record + commands + trace + input -> 8 ---------
    rec = json.loads(ledger_json())
    for e in rec['entries']:
        e['class'] = 'record'
        e['verdict'] = 'verified-record'
    write_file(repo, LEDGER_PATH, json.dumps(rec) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'record with commands')).stdout)
    check('record-with-commands-credited',
          out['coldread']['sections_covered'] == 4
          and out['coldread']['box3_full_page'] is True
          and out['calibration_restraint_score'] == 8)

    # --- round-16 w2 MutateMeasure survivors -----------------------------------
    # (a) an unknown class is never credited
    unk = json.loads(ledger_json())
    unk['entries'][3]['class'] = 'frobnicate'
    write_file(repo, LEDGER_PATH, json.dumps(unk) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'unknown class')).stdout)
    check('unknown-class-nocredit', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason'] == 'class:frobnicate')
    # (b) a record cannot pass as executed-ok
    rx = json.loads(ledger_json())
    rx['entries'][3]['class'] = 'record'
    write_file(repo, LEDGER_PATH, json.dumps(rx) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'record executed-ok')).stdout)
    check('record-executed-ok-nocredit', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason']
          == 'verdict-class:executed-ok/record')
    # (c) whitespace-only trailing lines are stripped before hashing
    a = sectionize(b'# A\nbody\n   \n\t\n')[0]['sha256']
    check('trailing-whitespace-stripped',
          a == hashlib.sha256(b'# A\nbody').hexdigest())
    # (d) booleans / numeric strings are malformed, not counts
    bad = json.loads(ledger_json())
    bad['entries'][3]['commands_executed_count'] = True
    write_file(repo, LEDGER_PATH, json.dumps(bad) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'bool command count')).stdout)
    check('bool-count-malformed', out['calibration_restraint_score'] == 6
          and out['coldread']['missing'][0]['reason'] == 'malformed-entry')

    # --- case: SHONEN box-3 line lacks the ledger link -> 6 ---------------------
    write_file(repo, LEDGER_PATH, ledger_json())
    write_file(repo, 'SHONEN.md', SHONEN_NOLINK_TEXT)
    rev_nolink = commit(repo, 'box3 without ledger link')
    out = json.loads(call_measure(repo, rev_nolink).stdout)
    check('nolink-fullpage', out['coldread']['box3_full_page'] is True)
    check('nolink-flag', out['shonen']['box3_ledger_link'] is False
          and out['shonen']['box3_points'] is False)
    check('nolink-score-6', out['calibration_restraint_score'] == 6)

    # --- case: link on box 3's indented continuation line -> 8 -----------------
    write_file(repo, 'SHONEN.md', SHONEN_CONT_TEXT)
    rev_cont = commit(repo, 'box3 link on continuation line')
    out = json.loads(call_measure(repo, rev_cont).stdout)
    check('contlink-score-8', out['shonen']['box3_ledger_link'] is True
          and out['calibration_restraint_score'] == 8)

    # --- case: link only under box 4 -> box 3 not credited (6) -----------------
    write_file(repo, 'SHONEN.md', SHONEN_WRONGBOX_TEXT)
    rev_wrong = commit(repo, 'link under box 4 only')
    out = json.loads(call_measure(repo, rev_wrong).stdout)
    check('wrongbox-score-6', out['shonen']['box3_ledger_link'] is False
          and out['calibration_restraint_score'] == 6)
    write_file(repo, 'SHONEN.md', SHONEN_TEXT)

    # --- hardening: inputs-unrecorded / input-missing / input-not-blob ----------
    write_file(repo, LEDGER_PATH, ledger_json(inputs_mode='none'))
    rev_norecord = commit(repo, 'ledger without inputs')
    out = json.loads(call_measure(repo, rev_norecord).stdout)
    check('unrecorded-score-6', out['calibration_restraint_score'] == 6
          and out['coldread']['box3_full_page'] is False)
    check('unrecorded-reasons',
          out['coldread']['reasons'] == {'inputs-unrecorded': 4}
          and all(m['reason'] == 'inputs-unrecorded'
                  for m in out['coldread']['missing']))

    write_file(repo, LEDGER_PATH, ledger_json(inputs_mode='missing'))
    rev_imiss = commit(repo, 'ledger pins absent input')
    out = json.loads(call_measure(repo, rev_imiss).stdout)
    check('input-missing-score-6', out['calibration_restraint_score'] == 6)
    check('input-missing-reasons',
          out['coldread']['reasons']
          == {'input-missing:%s' % INPUT_MISSING: 4})

    for mode, key in (('dir', 'tools'), ('symlink', SYMLINK_PATH)):
        write_file(repo, LEDGER_PATH, ledger_json(inputs_mode=mode))
        out = json.loads(call_measure(
            repo, commit(repo, 'ledger pins %s input' % mode)).stdout)
        check('input-not-blob-%s' % mode, out['calibration_restraint_score'] == 6
              and out['coldread']['reasons']
              == {'input-not-blob:%s' % key: 4})

    for raw_path in ('../outside.txt', '/abs/file.txt', './dotted.txt',
                     'tools/.git/config', 'tools//double.txt'):
        entries = [synth_entry(i) for i, _s in enumerate(SYNTH_SECTIONS)]
        for e in entries:
            e['inputs'] = {raw_path: '1' * 64}
        write_file(repo, LEDGER_PATH, ledger_json(entries=entries))
        out = json.loads(call_measure(
            repo, commit(repo, 'non-canonical input key')).stdout)
        check('noncanonical-%s' % raw_path.replace('/', '_'),
              out['coldread']['reasons']
              == {'input-not-blob:%s' % raw_path: 4})

    # --- hardening: SKILL.md and both ledger paths are ignored -----------------
    write_file(repo, LEDGER_PATH, ledger_json(inputs_mode='skill-only'))
    out = json.loads(call_measure(repo, commit(repo, 'only SKILL.md input')).stdout)
    check('skill-only-unrecorded', out['coldread']['reasons']
          == {'inputs-unrecorded': 4})
    write_file(repo, LEDGER_PATH, ledger_json(inputs_mode='ledger-only'))
    out = json.loads(call_measure(repo, commit(repo, 'only round-18 ledger input')).stdout)
    check('ledger-only-unrecorded', out['coldread']['reasons']
          == {'inputs-unrecorded': 4})
    old_only = json.loads(ledger_json())
    for entry in old_only['entries']:
        entry['inputs'] = {ROUND17_LEDGER_PATH: 'a' * 64}
    write_file(repo, LEDGER_PATH, json.dumps(old_only) + '\n')
    out = json.loads(call_measure(
        repo, commit(repo, 'only round-17 ledger input')).stdout)
    check('round17-ledger-only-unrecorded',
          out['coldread']['reasons'] == {'inputs-unrecorded': 4})
    # A carried round-17 entry remains subject to current input-digest checks.
    carried = json.loads(ledger_json())
    carried['entries'][3]['inputs'][INPUT_FILE] = INPUT_V2_SHA
    carried['entries'][3]['carried_from'] = ROUND17_LEDGER_PATH
    write_file(repo, LEDGER_PATH, json.dumps(carried) + '\n')
    out = json.loads(call_measure(
        repo, commit(repo, 'carried input has drifted')).stdout)
    check('carried-round17-input-drift-uncredited',
          out['coldread']['sections_covered'] == 3
          and out['coldread']['missing'] == [
              {'start': 19, 'heading': '### Gamma',
               'reason': 'input-drift:%s' % INPUT_FILE}])
    write_file(repo, LEDGER_PATH, ledger_json(inputs_mode='skill-and-file'))
    out = json.loads(call_measure(repo, commit(repo, 'SKILL.md plus file')).stdout)
    check('skill-plus-file-credited',
          out['coldread']['reasons'] == {'credited': 4}
          and out['calibration_restraint_score'] == 8)

    # --- hardening: trace binding (strict) -------------------------------------
    write_file(repo, LEDGER_PATH, ledger_json(traces=False))
    rev_notrace = commit(repo, 'ledger without traces')
    out = json.loads(call_measure(repo, rev_notrace).stdout)
    check('traces-unrecorded', out['coldread']['reasons']
          == {'traces-unrecorded': 4}
          and out['calibration_restraint_score'] == 6)

    bad_trace = json.loads(ledger_json())
    for e in bad_trace['entries']:
        e['traces'] = ['no/such/trace.json']
    write_file(repo, LEDGER_PATH, json.dumps(bad_trace) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'trace blob absent')).stdout)
    check('trace-missing', out['coldread']['reasons']
          == {'trace-missing:no/such/trace.json': 4})

    bad_trace = json.loads(ledger_json())
    for e in bad_trace['entries']:
        e['traces'] = [TRACE_BAD_PATH]
    write_file(repo, LEDGER_PATH, json.dumps(bad_trace) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'trace wrong schema')).stdout)
    check('trace-invalid', out['coldread']['reasons']
          == {'trace-invalid:%s' % TRACE_BAD_PATH: 4})

    bad_trace = json.loads(ledger_json())
    for e in bad_trace['entries']:
        e['traces'] = [TRACE_EXTRA_PATH]
    write_file(repo, LEDGER_PATH, json.dumps(bad_trace) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'trace extra input')).stdout)
    check('trace-input-unrecorded', out['coldread']['reasons']
          == {'trace-input-unrecorded:corpus/SOURCES.md': 4})

    bad_trace = json.loads(ledger_json())
    for e in bad_trace['entries']:
        e['traces'] = [TRACE_DRIFT_PATH]
    write_file(repo, LEDGER_PATH, json.dumps(bad_trace) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'trace digest mismatch')).stdout)
    check('trace-input-drift', out['coldread']['reasons']
          == {'trace-input-drift:%s' % INPUT_FILE: 4})

    bad_trace = json.loads(ledger_json())
    for e in bad_trace['entries']:
        e['traces'] = [TRACE_LIVE_PATH]
    write_file(repo, LEDGER_PATH, json.dumps(bad_trace) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'trace live lane reads')).stdout)
    check('live-lane-read', out['coldread']['reasons']
          == {'live-lane-read:%s' % os.path.join(LIVE_LANE_ROOT, 'SKILL.md'): 4})

    bad_trace = json.loads(ledger_json())
    for e in bad_trace['entries']:
        e['traces'] = [TRACE_EXT_PATH]
    write_file(repo, LEDGER_PATH, json.dumps(bad_trace) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'trace external live lane')).stdout)
    check('live-lane-read-external', out['coldread']['reasons']
          == {'live-lane-read:%s' % os.path.join(LIVE_LANE_ROOT, 'SKILL.md'): 4})

    # A live read bound to REV (same bytes as the blob, or a .git/ object/ref
    # read by a rev-addressed command) is accepted (round-17 wave-2 refinement).
    bound = json.loads(ledger_json())
    for e in bound['entries']:
        e['traces'] = [TRACE_LIVE_BOUND_PATH]
    write_file(repo, LEDGER_PATH, json.dumps(bound) + '\n')
    out = json.loads(call_measure(repo, commit(repo, 'trace live reads bound')).stdout)
    check('live-lane-read-bound', out['coldread']['sections_covered'] == 4,
          str(out['coldread'].get('reasons')))

    # --- hardening: fail-closed aggregation ------------------------------------
    # (a) a clean entry never launders a failing one, in either order.
    for label, first, second in (
            ('clean-first', {}, {'verdict': 'gap-blocking'}),
            ('fail-first', {'verdict': 'gap-blocking'}, {})):
        write_file(repo, LEDGER_PATH,
                   dupe_ledger(second, first_overrides=first))
        out = json.loads(call_measure(
            repo, commit(repo, 'dupe ' + label)).stdout)
        check('dupe-veto-%s' % label,
              out['coldread']['sections_covered'] == 3
              and out['coldread']['missing'][0]['reason'] == 'verdict:gap-blocking'
              and out['coldread']['sections'][3]['vetoed'] is True)
    # (b) a failing entry with drifted inputs is stale and does not veto.
    write_file(repo, LEDGER_PATH, dupe_ledger(
        {'verdict': 'wrong-expectation', 'inputs_mode': 'stale-file'}))
    out = json.loads(call_measure(repo, commit(repo, 'dupe stale failure')).stdout)
    check('dupe-stale-no-veto', out['coldread']['sections_covered'] == 4
          and out['coldread']['reasons'] == {'credited': 4})
    # (c) a failing entry with verified inputs vetoes even with a clean twin.
    write_file(repo, LEDGER_PATH, dupe_ledger(
        {'verdict': 'wrong-expectation', 'inputs_mode': 'default'}))
    out = json.loads(call_measure(repo, commit(repo, 'dupe live failure')).stdout)
    check('dupe-live-veto', out['coldread']['sections_covered'] == 3
          and out['coldread']['missing'][0]['reason'] == 'verdict:wrong-expectation')

    # --- hardening: legacy red-before with an X10-shaped overlay ---------------
    # Ledger pinned without inputs; overlay supplies the e69b-style pins.
    write_file(repo, LEDGER_PATH, ledger_json(inputs_mode='none', traces=False))
    rev_read = commit(repo, 'red-before read rev, overlay supplies inputs')
    overlay = [{
        'start': start, 'heading': heading, 'skill_sha256': 'deadbeef',
        'read_rev': rev_read, 'inputs': {INPUT_FILE: INPUT_V1_SHA},
    } for start, heading, _text in SYNTH_SECTIONS]
    overlay.append({'start': 999, 'heading': '# Ghost',
                    'skill_sha256': 'deadbeef', 'read_rev': rev_read,
                    'inputs': {INPUT_FILE: INPUT_V1_SHA}})
    overlay_path = os.path.join(tmp, 'overlay.json')
    with open(overlay_path, 'w') as f:
        f.write(json.dumps(overlay))
    res = call_measure(repo, rev_read, '--inputs-overlay', overlay_path)
    out = json.loads(res.stdout)
    check('overlay-redbefore-credits-at-read-rev',
          out['calibration_restraint_score'] == 8
          and out['coldread']['inputs_overlay_merged'] == 4
          and out['coldread']['reasons'] == {'credited': 4}
          and out['trace_gate'] == 'legacy'
          and out['overrides_used'] is True,
          'ghost overlay item must not merge')
    # The same ledger + overlay at a rev where the input changed -> drift.
    write_file(repo, INPUT_FILE, INPUT_V2)
    rev_drift = commit(repo, 'input file changed after read')
    out = json.loads(call_measure(repo, rev_drift,
                                  '--inputs-overlay', overlay_path).stdout)
    check('overlay-redbefore-drift',
          out['calibration_restraint_score'] == 6
          and out['coldread']['reasons']
          == {'input-drift:%s' % INPUT_FILE: 4})
    # Strict mode (no overrides) on the same ledger never credits: traces and
    # inputs are missing at the measured rev.
    out = json.loads(call_measure(repo, rev_drift).stdout)
    check('strict-no-overrides-unrecorded',
          out['coldread']['reasons'] == {'inputs-unrecorded': 4}
          and out['trace_gate'] == 'strict')

    # --- hardening: --ledger-file / --ledger-rev plumbing ---------------------
    good_ledger = ledger_json()
    noinput_ledger = ledger_json(inputs_mode='none', traces=False)
    ledger_file = os.path.join(tmp, 'ledger-local.json')
    with open(ledger_file, 'w') as f:
        f.write(good_ledger)
    res = call_measure(repo, rev_drift, '--ledger-file', ledger_file)
    out = json.loads(res.stdout)
    check('ledger-file-drift', res.returncode == 0
          and out['coldread']['reasons'] == {'input-drift:%s' % INPUT_FILE: 4}
          and out['ledger_committed'] is False
          and out['overrides_used'] is True)
    res = call_measure(repo, rev_full, '--ledger-rev',
                       '%s:%s' % (rev_full, LEDGER_PATH))
    out = json.loads(res.stdout)
    check('ledger-rev-committed', res.returncode == 0
          and out['calibration_restraint_score'] == 8
          and out['ledger_committed'] is True)
    res = call_measure(repo, rev_drift, '--ledger-rev',
                       '%s:%s' % (rev_full, LEDGER_PATH))
    out = json.loads(res.stdout)
    check('ledger-rev-cross-rev-drift', res.returncode == 0
          and out['coldread']['reasons']
          == {'input-drift:%s' % INPUT_FILE: 4})

    # --- hardening: overlay field whitelist -----------------------------------
    inject = [dict(item, verdict='executed-ok', wrong_expectations=0)
              for item in overlay]
    inject_path = os.path.join(tmp, 'overlay-inject.json')
    with open(inject_path, 'w') as f:
        f.write(json.dumps(inject))
    res = call_measure(repo, rev_drift, '--inputs-overlay', inject_path)
    check('overlay-field-forbidden', res.returncode == 2
          and 'overlay-field-forbidden' in res.stdout, res.stdout[:200])
    verdict_only = [{'start': 19, 'skill_sha256': 'deadbeef',
                     'verdict': 'executed-ok'}]
    verdict_path = os.path.join(tmp, 'overlay-verdict.json')
    with open(verdict_path, 'w') as f:
        f.write(json.dumps(verdict_only))
    res = call_measure(repo, rev_drift, '--inputs-overlay', verdict_path)
    check('overlay-verdict-only-forbidden', res.returncode == 2
          and 'overlay-field-forbidden' in res.stdout, res.stdout[:200])
    trace_overlay = [{'start': 19, 'skill_sha256': 'deadbeef',
                      'traces': [TRACE_PATH]}]
    trace_overlay_path = os.path.join(tmp, 'overlay-trace.json')
    with open(trace_overlay_path, 'w') as f:
        f.write(json.dumps(trace_overlay))
    res = call_measure(repo, rev_drift, '--inputs-overlay', trace_overlay_path)
    check('overlay-traces-allowed', res.returncode == 0
          and json.loads(res.stdout)['coldread']['inputs_overlay_merged'] == 1,
          res.stdout[:200])

    # --- hardening: revision identity, env scrub, default repo ----------------
    head = git_in(repo, 'rev-parse', 'HEAD').stdout.strip()
    res = call_measure(repo, 'HEAD')
    out = json.loads(res.stdout)
    check('revision-40hex', COMMIT_RE.match(out.get('revision', '')) is not None
          and out['revision'] == head and out.get('rev_input') == 'HEAD',
          out.get('revision'))
    res = call_measure(repo, rev_full,
                       extra_env={'GIT_DIR': '/nonexistent',
                                  'GIT_WORK_TREE': '/nonexistent',
                                  'GIT_INDEX_FILE': '/nonexistent'})
    check('git-env-scrubbed', res.returncode == 0
          and json.loads(res.stdout)['calibration_restraint_score'] == 8,
          res.stderr.strip()[:200])
    copy_dir = os.path.join(repo, '.ufo', 'evidence', 'round-17')
    os.makedirs(copy_dir, exist_ok=True)
    with open(script, 'rb') as src, open(os.path.join(copy_dir, 'measure.py'),
                                         'wb') as dst:
        dst.write(src.read())
    res = run(sys.executable or 'python3',
              os.path.join(copy_dir, 'measure.py'), '--rev', rev_full, cwd=tmp)
    check('default-repo-is-script-toplevel', res.returncode == 0
          and json.loads(res.stdout)['coldread']['sections_covered'] == 4,
          res.stderr.strip()[:200])

    # --- literal expected exits -------------------------------------------------
    os.remove(os.path.join(repo, 'SHONEN.md'))
    rev_noshonen = commit(repo, 'drop SHONEN.md')
    res = call_measure(repo, rev_noshonen)
    check('exit2-blob-missing', res.returncode == 2,
          'stderr=%r' % res.stderr.strip()[:120])
    res = call_measure(repo, '0' * 40)
    check('exit2-bad-rev', res.returncode == 2)
    res = run(sys.executable or 'python3', script, '--repo', repo)
    check('exit64-no-rev', res.returncode == 64)
    res = run(sys.executable or 'python3', script, '--rev', rev_base,
              '--bogus')
    check('exit64-unknown-arg', res.returncode == 64)
    res = call_measure(os.path.join(tmp, 'no-such-repo'), rev_base)
    check('exit2-no-repo', res.returncode == 2)
    res = call_measure(repo, rev_drift, '--rev', '--all')
    check('exit64-option-like-rev', res.returncode == 64)
    res = call_measure(repo, rev_drift, '--ledger-file', ledger_file,
                       '--ledger-rev', '%s:%s' % (rev_full, LEDGER_PATH))
    check('exit64-both-ledger-flags', res.returncode == 64)
    res = call_measure(repo, rev_drift, '--ledger-rev', 'no-colon-here')
    check('exit64-ledger-rev-malformed', res.returncode == 64)
    res = call_measure(repo, rev_drift, '--ledger-rev=--all:%s' % LEDGER_PATH)
    check('exit64-ledger-rev-option-like', res.returncode == 64)
    res = call_measure(repo, rev_drift, '--ledger-rev',
                       '%s:%s' % (rev_full, 'no/such/ledger.json'))
    check('exit2-ledger-rev-blob-missing', res.returncode == 2)
    res = call_measure(repo, rev_drift, '--ledger-file',
                       os.path.join(tmp, 'absent.json'))
    check('exit2-ledger-file-missing', res.returncode == 2)
    res = call_measure(repo, rev_drift, '--inputs-overlay',
                       os.path.join(tmp, 'absent-overlay.json'))
    check('exit2-overlay-missing', res.returncode == 2)
    bad_overlay = os.path.join(tmp, 'bad-overlay.json')
    with open(bad_overlay, 'w') as f:
        f.write('{"not": "a list"}')
    res = call_measure(repo, rev_drift, '--inputs-overlay', bad_overlay)
    check('exit2-overlay-invalid', res.returncode == 2)
    res = call_measure(repo, rev_drift, '--ledger-rev', 'no-such-rev:%s'
                       % LEDGER_PATH)
    check('exit2-ledger-rev-bad-rev', res.returncode == 2)

    passed = sum(1 for _, ok, _ in checks if ok)
    print('MEASURE_SELFTEST: %d/%d pass (scratch %s)' % (passed, len(checks), tmp))
    return 0 if passed == len(checks) else 1


def default_repo(script_path):
    """Git toplevel containing this file, so a clone measures itself."""
    here = os.path.dirname(os.path.abspath(script_path))
    result = subprocess.run(['git', '-C', here, 'rev-parse', '--show-toplevel'],
                            capture_output=True, env=GIT_ENV)
    if result.returncode == 0:
        top = result.stdout.decode('utf-8', 'surrogateescape').strip()
        if top:
            return top
    return here


def main(argv=None):
    parser = UsageParser(
        description='C1+C2 counting command: depth legs, SHONEN marks, '
                    'input-keyed cold-read ledger coverage, SOURCES census.')
    parser.add_argument('--rev', help='git revision to measure')
    parser.add_argument('--repo', default=None,
                        help='repository path (default: the git toplevel '
                             'containing this script)')
    parser.add_argument('--ledger-file',
                        help='read the ledger from a local file instead of '
                             'REV:%s' % DEFAULT_LEDGER_PATH)
    parser.add_argument('--ledger-rev', metavar='REV:PATH',
                        help='read the ledger from blob PATH at REV instead '
                             'of REV:%s' % DEFAULT_LEDGER_PATH)
    parser.add_argument('--inputs-overlay', metavar='FILE',
                        help='JSON list of {start, skill_sha256, inputs, '
                             'read_rev, traces} merged into matching ledger '
                             'entries by (skill_sha256, start); any other '
                             'item key exits 2')
    parser.add_argument('--explain', action='store_true',
                        help='include per-section bounds and credit reasons')
    parser.add_argument('--selftest', action='store_true',
                        help='build synthetic repos and self-check')
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.rev:
        parser.error('--rev is required')
    if args.ledger_file and args.ledger_rev:
        parser.error('--ledger-file and --ledger-rev are mutually exclusive')
    if args.rev.startswith('-'):
        parser.error('--rev must not be option-like')
    ledger_rev = ledger_blob = None
    if args.ledger_rev is not None:
        if ':' not in args.ledger_rev:
            parser.error('--ledger-rev expects REV:PATH')
        ledger_rev, ledger_blob = args.ledger_rev.split(':', 1)
        if not ledger_rev or not ledger_blob:
            parser.error('--ledger-rev expects REV:PATH')
        if ledger_rev.startswith('-'):
            parser.error('--ledger-rev REV must not be option-like')
    repo = args.repo or default_repo(__file__)
    if not os.path.isdir(repo):
        print(json.dumps({'error': 'repo-not-found', 'repo': repo},
                         indent=2, sort_keys=True))
        return 2
    rev = resolve_commit(repo, args.rev)
    if rev is None:
        print(json.dumps({'error': 'rev-missing', 'rev': args.rev,
                          'repo': repo},
                         indent=2, sort_keys=True))
        return 2
    missing = [p for p in REQUIRED_BLOBS if blob(repo, rev, p) is None]
    if missing:
        print(json.dumps({'error': 'blob-missing', 'rev': rev,
                          'missing': missing},
                         indent=2, sort_keys=True))
        return 2
    overrides_used = bool(args.ledger_file or args.ledger_rev
                          or args.inputs_overlay)
    if args.ledger_file:
        try:
            with open(args.ledger_file, 'rb') as f:
                ledger_raw = f.read()
        except OSError as exc:
            print(json.dumps({'error': 'ledger-file-unreadable',
                              'path': args.ledger_file,
                              'detail': str(exc)},
                             indent=2, sort_keys=True))
            return 2
        ledger_source = 'file'
    elif args.ledger_rev:
        pinned = resolve_commit(repo, ledger_rev)
        if pinned is None:
            print(json.dumps({'error': 'ledger-rev-missing',
                              'ledger_rev': ledger_rev},
                             indent=2, sort_keys=True))
            return 2
        ledger_raw = blob(repo, pinned, ledger_blob)
        if ledger_raw is None:
            print(json.dumps({'error': 'ledger-blob-missing',
                              'ledger_rev': args.ledger_rev},
                             indent=2, sort_keys=True))
            return 2
        ledger_source = 'rev'
    else:
        ledger_raw = blob(repo, rev, DEFAULT_LEDGER_PATH)
        ledger_source = 'rev'
    committed_blob = blob(repo, rev, DEFAULT_LEDGER_PATH)
    ledger_committed = (ledger_raw is not None
                        and committed_blob is not None
                        and ledger_raw == committed_blob)
    overlay = None
    if args.inputs_overlay:
        try:
            with open(args.inputs_overlay, 'rb') as f:
                overlay = json.loads(f.read().decode('utf-8'))
        except (OSError, ValueError) as exc:
            print(json.dumps({'error': 'overlay-unreadable',
                              'path': args.inputs_overlay,
                              'detail': str(exc)},
                             indent=2, sort_keys=True))
            return 2
        if not isinstance(overlay, list):
            print(json.dumps({'error': 'overlay-not-a-list',
                              'path': args.inputs_overlay},
                             indent=2, sort_keys=True))
            return 2
        for item in overlay:
            if not isinstance(item, dict):
                print(json.dumps({'error': 'overlay-item-not-object',
                                  'path': args.inputs_overlay},
                                 indent=2, sort_keys=True))
                return 2
            forbidden = sorted(set(item) - OVERLAY_FIELDS)
            if forbidden:
                print(json.dumps({'error': 'overlay-field-forbidden',
                                  'path': args.inputs_overlay,
                                  'fields': forbidden},
                                 indent=2, sort_keys=True))
                return 2
            if 'inputs' in item and not isinstance(item['inputs'], dict):
                print(json.dumps({'error': 'overlay-field-invalid',
                                  'path': args.inputs_overlay,
                                  'field': 'inputs'},
                                 indent=2, sort_keys=True))
                return 2
            if 'traces' in item and not isinstance(item['traces'], list):
                print(json.dumps({'error': 'overlay-field-invalid',
                                  'path': args.inputs_overlay,
                                  'field': 'traces'},
                                 indent=2, sort_keys=True))
                return 2
    print(json.dumps(measure(repo, rev, ledger_raw, overlay=overlay,
                             overrides_used=overrides_used,
                             ledger_source=ledger_source,
                             ledger_committed=ledger_committed,
                             rev_input=args.rev, explain=args.explain),
                     indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
