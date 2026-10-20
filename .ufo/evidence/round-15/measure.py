#!/usr/bin/env python3
"""Read-only committed-blob counts for the round-15 context-gate claim.

Every value below is counted from committed blobs at --rev. Nothing is
executed: no context gate, no selftest, no sibling instrument. The counts are
structural evidence that a gate is registered as a gate, that a standalone
selftest entry point and its pass marker exist, that both exit-64 classes are
stated explicitly, that sources grew, that historical round-12..14 bytes are
unchanged, and that the six-case runner and the box-3-excluded restrained
SHONEN census still hold. They are not a gate run, a selftest run or runtime
proof of the claim.

Byte-preservation comparisons use --baseline, defaulting to the round-15
claim baseline recorded in .ufo/evidence/round-15/claims.json.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASELINE = 'a9cf4da78f2514c7bedd91a850a88590009d7df0'

CONTEXT_TOOL = 'tools/context-capture.py'
DISPOSITION_TOOL = 'tools/evidence-disposition.py'
RUNNER = 'tools/mutate-and-run.sh'
FROZEN_SUMMARY = '.ufo/evidence/round-12/BashWitness/summary.json'
HISTORICAL_SCRIPT = '.ufo/evidence/round-14/capture-context.py'
HISTORICAL_RECEIPT = '.ufo/evidence/round-14/context-receipt.json'
HISTORICAL_DIGEST_PATHS = (
    HISTORICAL_SCRIPT,
    HISTORICAL_RECEIPT,
    FROZEN_SUMMARY,
    RUNNER,
)
HISTORICAL_EVIDENCE_DIRS = (
    '.ufo/evidence/round-12',
    '.ufo/evidence/round-13',
    '.ufo/evidence/round-14',
)
# Round-14 verifier spot-check, "Independent before -> delivered measurements".
PUBLISHED_ROUND14_RUNNER_SHA256 = (
    '75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5'
)
PUBLISHED_ROUND14_SUMMARY_SHA256 = (
    'acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9'
)
# Fixed adjudication: the round-1 outside review excludes box 3 from score
# credit (SCORECARD.md, round-1 corrections; round-12 measure.py precedent).
SCORED_BOXES = (1, 2, 4)
EXCLUDED_BOXES = (3,)
REGISTRY_KINDS = ('gate', 'probe')
SOURCES_ROW_RE = re.compile(r'^\|\s*S\d{3,}\s*\|')
CLASS_64_RE = re.compile(r'64\s*([^;|]*)')
# On a source line, "could-not-evaluate" must sit in the same exit-map clause
# as 64; a compact map mentioning both classes elsewhere on the line is not
# an explicit 64 mapping.
TOOL_64_NEAR_RE = re.compile(
    r'64[^;\n|]{0,60}could[- ]not[- ]evaluate|could[- ]not[- ]evaluate[^;\n|]{0,40}64')


def git(*argv):
    try:
        return subprocess.run(['git', '-C', str(ROOT), *argv], capture_output=True)
    except OSError as exc:
        sys.stderr.write('measure.py: could-not-evaluate: git unavailable: {}\n'.format(exc))
        raise SystemExit(2)


def resolve(rev):
    result = git('rev-parse', '--verify', '--quiet', rev + '^{commit}')
    if result.returncode != 0:
        return None
    return result.stdout.decode('ascii', 'replace').strip()


def blob(rev, path):
    result = git('show', '{}:{}'.format(rev, path))
    return result.stdout if result.returncode == 0 else None


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None


def as_text(data):
    return data.decode('utf-8', 'replace') if data is not None else ''


def digest_entry(revision, baseline, path):
    data = blob(revision, path)
    base = blob(baseline, path)
    return {
        'present': int(data is not None),
        'sha256': sha256_bytes(data),
        'baseline_sha256': sha256_bytes(base),
        'preserved_at_baseline': int(data is not None and base is not None and data == base),
    }


def tree_blobs(rev):
    result = git('ls-tree', '-r', rev, '--', *HISTORICAL_EVIDENCE_DIRS)
    if result.returncode != 0:
        return {}
    entries = {}
    for line in result.stdout.decode('utf-8', 'surrogateescape').splitlines():
        if not line:
            continue
        meta, _, name = line.partition('\t')
        fields = meta.split()
        if len(fields) == 3 and fields[1] == 'blob':
            entries[name] = fields[2]
    return entries


def source_rows(source_text):
    rows = []
    malformed = 0
    for line in source_text.splitlines():
        if not SOURCES_ROW_RE.match(line):
            continue
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if len(cells) == 11:
            rows.append(cells)
        else:
            malformed += 1
    return rows, malformed


def registry_rows(skill_text, needle):
    rows = []
    for line in skill_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith('|'):
            continue
        cells = [cell.strip() for cell in stripped.strip('|').split('|')]
        if len(cells) < 8:
            continue
        kind = cells[1].lower().strip('`*_ ')
        if kind not in REGISTRY_KINDS:
            continue
        if needle not in cells[2]:
            continue
        rows.append({
            'kind': kind,
            'entry': cells[2],
            'verdict': cells[3],
            'selftest': cells[4],
        })
    return rows


def classes_64(verdict):
    found = []
    for match in CLASS_64_RE.findall(verdict):
        item = match.strip()
        if item:
            found.append(item)
    return found


def states_could_not_evaluate(classes):
    for item in classes:
        normalized = item.lower().replace('_', '-')
        if 'could-not-evaluate' in normalized or 'could not evaluate' in normalized:
            return 1
    return 0


def tool_64_lines(tool_text):
    samples = []
    for line in tool_text.splitlines():
        normalized = line.lower().replace('_', '-')
        if TOOL_64_NEAR_RE.search(normalized):
            samples.append(line.strip()[:160])
    return samples


def main():
    parser = argparse.ArgumentParser(
        description='Read-only committed-blob counts for the round-15 context-gate claim.')
    parser.add_argument('--rev', required=True, help='committed revision to count')
    parser.add_argument('--baseline', default=DEFAULT_BASELINE,
                        help='revision whose historical bytes must be preserved')
    args = parser.parse_args()

    revision = resolve(args.rev)
    if revision is None:
        sys.stderr.write(
            'measure.py: could-not-evaluate: unknown revision {!r}\n'.format(args.rev))
        return 2
    baseline = resolve(args.baseline)
    if baseline is None:
        sys.stderr.write(
            'measure.py: could-not-evaluate: unknown baseline {!r}\n'.format(args.baseline))
        return 2

    skill_text = as_text(blob(revision, 'SKILL.md'))
    context_tool = blob(revision, CONTEXT_TOOL)
    context_tool_text = as_text(context_tool)
    disposition_tool_text = as_text(blob(revision, DISPOSITION_TOOL))
    sources_text = as_text(blob(revision, 'corpus/SOURCES.md'))
    runner_blob = blob(revision, RUNNER)
    runner_text = as_text(runner_blob)
    summary_blob = blob(revision, FROZEN_SUMMARY)
    shonen_text = as_text(blob(revision, 'SHONEN.md'))

    context_rows = registry_rows(skill_text, CONTEXT_TOOL)
    historical_context_rows = registry_rows(skill_text, 'capture-context.py')
    disposition_rows = registry_rows(skill_text, DISPOSITION_TOOL)
    context_classes = sorted({item for row in context_rows for item in classes_64(row['verdict'])})
    disposition_classes = sorted(
        {item for row in disposition_rows for item in classes_64(row['verdict'])})
    context_tool_64 = tool_64_lines(context_tool_text)
    disposition_tool_64 = tool_64_lines(disposition_tool_text)

    context_gate_rows = sum(row['kind'] == 'gate' for row in context_rows)
    context_probe_rows = sum(row['kind'] == 'probe' for row in context_rows)
    context_selftest_mentions = context_tool_text.count('--selftest')
    context_selftest_pass_marker = int('SELFTEST: PASS' in context_tool_text)
    context_selftest_case_mentions = context_tool_text.count('SELFTEST_CASE')
    context_selftest_self_invocation_lines = sum(
        1 for line in context_tool_text.splitlines()
        if 'sys.executable' in line and 'selftest' in line.lower())

    context64_registry = states_could_not_evaluate(context_classes)
    context64_tool = int(bool(context_tool_64))
    context64_explicit = int(bool(context64_registry or context64_tool))
    disposition64_registry = states_could_not_evaluate(disposition_classes)
    disposition64_tool = int(bool(disposition_tool_64))
    disposition64_explicit = int(bool(disposition64_registry or disposition64_tool))

    rows, malformed = source_rows(sources_text)
    tiers = dict(sorted(Counter(row[3] for row in rows).items()))
    statuses = dict(sorted(Counter(row[7] for row in rows).items()))

    runner_cases = len(re.findall(
        r'^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+', runner_text, re.M))
    runner_sha256 = sha256_bytes(runner_blob)
    summary_sha256 = sha256_bytes(summary_blob)

    marks = re.findall(r'^- \[([x~ ])\] ', shonen_text, re.M)
    restrained = sum(
        1 for box in SCORED_BOXES if len(marks) >= box and marks[box - 1] == '~')

    base_tree = tree_blobs(baseline)
    rev_tree = tree_blobs(revision)
    changed = sorted(path for path, oid in base_tree.items() if rev_tree.get(path) != oid)
    added = sorted(path for path in rev_tree if path not in base_tree)

    historical_digests = {
        path: digest_entry(revision, baseline, path) for path in HISTORICAL_DIGEST_PATHS
    }

    document = {
        'scope': ('committed-blob structural counts only; no gate or selftest execution, '
                  'no runtime proof'),
        'requested_revision': args.rev,
        'revision': revision,
        'baseline_revision': baseline,
        'context_capture_present': int(context_tool is not None),
        'context_capture_sha256': sha256_bytes(context_tool),
        'context_registry_rows': len(context_rows),
        'context_registry_kinds': dict(
            sorted(Counter(row['kind'] for row in context_rows).items())),
        'context_historical_registry_rows': len(historical_context_rows),
        'context_historical_registry_kinds': dict(
            sorted(Counter(row['kind'] for row in historical_context_rows).items())),
        'context_gate_kind_rows': context_gate_rows,
        'context_probe_kind_rows': context_probe_rows,
        'context_gate_active_classification': int(
            context_tool is not None and context_gate_rows >= 1 and context_probe_rows == 0),
        'context_registry_selftest_command': int(
            any('selftest' in row['selftest'].lower() for row in context_rows)),
        'context_selftest_flag_mentions': context_selftest_mentions,
        'context_selftest_pass_marker': context_selftest_pass_marker,
        'context_selftest_case_mentions': context_selftest_case_mentions,
        'context_selftest_self_invocation_lines': context_selftest_self_invocation_lines,
        'context_standalone_selftest_present': int(
            context_tool is not None
            and context_selftest_mentions > 0
            and context_selftest_pass_marker == 1),
        'context_64_classes': context_classes,
        'context64_registry_could_not_evaluate': context64_registry,
        'context_tool_64_class_lines': len(context_tool_64),
        'context_tool_64_samples': context_tool_64[:5],
        'context64_tool_could_not_evaluate': context64_tool,
        'context64_explicit_class': context64_explicit,
        'disposition_registry_rows': len(disposition_rows),
        'disposition_64_classes': disposition_classes,
        'disposition64_registry_could_not_evaluate': disposition64_registry,
        'disposition_tool_64_class_lines': len(disposition_tool_64),
        'disposition_tool_64_samples': disposition_tool_64[:5],
        'disposition64_tool_could_not_evaluate': disposition64_tool,
        'disposition64_explicit_class': disposition64_explicit,
        'explicit64_classes_declared': context64_explicit + disposition64_explicit,
        'source_rows': len(rows),
        'source_malformed': malformed,
        'source_tiers': tiers,
        'source_statuses': statuses,
        'sources_sha256': sha256_bytes(blob(revision, 'corpus/SOURCES.md')),
        'runner_recorded_cases': runner_cases,
        'recorded_cases': runner_cases,
        'runner_cases_six': int(runner_cases == 6),
        'runner_sha256': runner_sha256,
        'runner_sha256_matches_round14_published': int(
            runner_sha256 == PUBLISHED_ROUND14_RUNNER_SHA256),
        'frozen_summary_sha256': summary_sha256,
        'frozen_summary_sha256_matches_round14_published': int(
            summary_sha256 == PUBLISHED_ROUND14_SUMMARY_SHA256),
        'historical_script_sha256': historical_digests[HISTORICAL_SCRIPT]['sha256'],
        'historical_receipt_sha256': historical_digests[HISTORICAL_RECEIPT]['sha256'],
        'historical_digests': historical_digests,
        'historical_evidence': {
            'baseline_paths': len(base_tree),
            'revision_paths': len(rev_tree),
            'preserved_paths': len(base_tree) - len(changed),
            'changed_or_missing_count': len(changed),
            'changed_or_missing': changed[:20],
            'added_count': len(added),
            'added': added[:20],
            'all_baseline_bytes_preserved': int(not changed),
        },
        'shonen_marks_total': len(marks),
        'shonen_states': list(marks),
        'shonen_scored_boxes': list(SCORED_BOXES),
        'shonen_excluded_boxes': list(EXCLUDED_BOXES),
        'shonen_restrained_boxes_excluding3': restrained,
        'calibration_restraint_score': 2 * restrained,
    }
    print(json.dumps(document, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
