#!/usr/bin/env python3
"""tools/rekey-cost.py — planning-time rekey-cost forecast (round 72).

What it answers, before any byte changes: *if I edit these paths, which
cold-read sections lose their credit and how many re-read sections will the
rekey owe?* Round 52 lost admission to cold-read debt it discovered after the
edit; a round that prices the debt at plan time can size the payment.

The rule (O, measured — round 72 rehearsal, `.ufo/evidence/round-72/reh/`):

  A SKILL.md section is at risk for a planned edit set P when its **newest**
  ledger entry records a planned path inside that entry's `inputs` (the
  ledger's own input-keyed pin, `corpus/knowledge/input-keyed-coldread-credit.md`).
  The newest entry for a heading is the entry the rekey last wrote; older
  entries describe earlier pins and do not re-open the section by themselves.

The model is not asserted: the round-72 rehearsal re-drove the frozen
precheck in scratch clones against four single-edit counterfactuals at the
lane base and the forecast reproduces each measured loss exactly —
`corpus/SOURCES.md` 13, `PROVINCE.md` 6, `corpus/QUALITY.md` 6,
`SCORECARD.md` 0, `PROVINCE.md`+`corpus/SOURCES.md` 17
(`.ufo/evidence/round-72/reh/*.out`). Paths a section never pins (a tool file,
a new evidence file, `LOG.md`) forecast 0, which is why a round's own record
appends are free.

It is a forecast over the committed ledger, not a run: it reads no git
objects, runs no verification command, and never re-reads a section. The
guard (`tools/coldread-precheck-portable.py`) remains the only measurement.

Usage:

  python3 -I tools/rekey-cost.py --edit corpus/SOURCES.md --edit PROVINCE.md
  python3 -I tools/rekey-cost.py --edit-file planned-paths.txt --json-out cost.json
  python3 -I tools/rekey-cost.py --selftest

Exit 0 on a completed forecast; 2 on setup errors (no planned path, missing
ledger/skill, unreadable edit file, fixture failure).
"""

import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

LEDGER = '.ufo/evidence/round-21/coldread/ledger.json'
SKILL = 'SKILL.md'
FROZEN = '.ufo/evidence/round-18/measure.py'
# Self-referential keys the frozen credit rule already removes from a view:
# the section is keyed by its own bytes and the ledger is the output.
IGNORED = frozenset((SKILL, '.ufo/evidence/round-17/coldread/ledger.json',
                     LEDGER))
SELFTEST_ARMS = 8


def load_sectionizer(repo):
    spec = importlib.util.spec_from_file_location(
        'tameshi_r18_measure_for_cost', Path(repo) / FROZEN)
    if spec is None:
        raise RuntimeError('frozen-module-unloadable:%s' % FROZEN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sectionize


def latest_entries(ledger, ignored=IGNORED):
    """heading -> newest entry inputs (append order is the ledger's order)."""
    latest = {}
    for entry in ledger.get('entries') or []:
        if not isinstance(entry, dict):
            continue
        heading = entry.get('heading')
        if not isinstance(heading, str):
            continue
        raw = entry.get('inputs')
        if not isinstance(raw, dict):
            continue
        latest[heading] = {p: v for p, v in raw.items() if p not in ignored}
    return latest


def forecast(repo, edits, ledger_path=None, skill_path=None):
    """Return {'sections', 'at_risk', 'unpinned', 'risk': [...]} or raise."""
    repo = Path(repo)
    ledger_path = Path(ledger_path) if ledger_path else repo / LEDGER
    skill_path = Path(skill_path) if skill_path else repo / SKILL
    if not ledger_path.is_file():
        raise SetupError('ledger-missing:%s' % ledger_path)
    if not skill_path.is_file():
        raise SetupError('skill-missing:%s' % skill_path)
    if not edits:
        raise SetupError('no-planned-path')
    try:
        ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    except (ValueError, OSError) as exc:
        raise SetupError('ledger-unreadable:%s:%s' % (ledger_path, exc))
    sectionize = load_sectionizer(repo)
    sections = sectionize(skill_path.read_bytes())
    latest = latest_entries(ledger)
    planned = sorted(set(edits))
    unpinned = [p for p in planned if not (repo / p).exists()]
    risk = []
    for sec in sections:
        pins = latest.get(sec['heading']) or {}
        hit = [p for p in planned if p in pins]
        if hit:
            risk.append({'heading': sec['heading'], 'start': sec['start'],
                         'end': sec['end'], 'pins': hit})
    return {'sections': len(sections), 'planned': planned, 'at_risk': len(risk),
            'predicted_lost': len(risk), 'unpinned': unpinned, 'risk': risk,
            'ledger': str(ledger_path), 'skill': str(skill_path)}


class SetupError(Exception):
    pass


def read_edit_file(path):
    text = Path(path).read_text(encoding='utf-8')
    out = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            out.append(line)
    return out


def run_forecast(repo, edits, ledger_path=None, skill_path=None, as_json=False):
    result = forecast(repo, edits, ledger_path, skill_path)
    if as_json:
        print(json.dumps(result, indent=1, ensure_ascii=True))
        return 0
    for row in result['risk']:
        print('RISK %s | pins=%s' % (row['heading'], ','.join(row['pins'])))
    for path in result['unpinned']:
        print('NOTE not-in-tree:%s (forecasts 0; a new file is in no union)'
              % path)
    print('REKEY_COST sections=%d planned=%d at_risk=%d predicted_lost=%d'
          % (result['sections'], len(result['planned']), result['at_risk'],
             result['predicted_lost']))
    return 0


# --- selftest -------------------------------------------------------------
FIXTURE_SKILL = (
    '# Fixture skill\n\nintro\n\n## Alpha section\n\n' + 'alpha body\n' * 3 +
    '\n### Beta subsection\n\n' + 'beta body\n' * 3 +
    '\n## Gamma section\n\n' + 'gamma body\n' * 3 +
    '\n## Delta section\n\n' + 'delta body\n' * 3)


def fixture_ledger(skill_sha):
    return {'schema': 'fixture', 'entries': [
        {'heading': '## Alpha section', 'sha256': skill_sha,
         'inputs': {'old-only.md': 'x', 'shared.md': 'y'}},
        {'heading': '## Alpha section', 'sha256': skill_sha,
         'inputs': {'shared.md': 'y'}},
        {'heading': '### Beta subsection', 'sha256': skill_sha,
         'inputs': {'beta.md': 'b', 'shared.md': 'y'}},
        {'heading': '## Gamma section', 'sha256': skill_sha,
         'inputs': {'gamma.md': 'g'}},
        {'heading': '## Delta section', 'sha256': skill_sha,
         'inputs': {'SKILL.md': 's', 'delta.md': 'd'}}]}


def build_fixture(root, with_frozen=True):
    root = Path(root)
    (root / SKILL).write_text(FIXTURE_SKILL, encoding='utf-8')
    for name in ('shared.md', 'beta.md', 'gamma.md', 'delta.md',
                 'old-only.md'):
        (root / name).write_text(name, encoding='utf-8')
    if with_frozen:
        src = Path(__file__).resolve().parent.parent / FROZEN
        dst = root / FROZEN
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    skill_sha = 'fixture-sha'
    led = root / LEDGER
    led.parent.mkdir(parents=True, exist_ok=True)
    led.write_text(json.dumps(fixture_ledger(skill_sha)), encoding='utf-8')
    return root


def selftest():
    work = tempfile.mkdtemp(prefix='rekey-cost-selftest-',
                            dir=os.environ.get('TMPDIR') or None)
    results = []
    try:
        repo = build_fixture(work)

        def arm(name, want, fn):
            try:
                got = fn()
                ok = got == want
            except SetupError:
                got = 'setup'
                ok = (want == 'setup')
            results.append((name, ok, got, want))

        arm('arm1-shared-two-sections', 2,
            lambda: forecast(repo, ['shared.md'])['at_risk'])
        arm('arm2-unpinned-zero', 0,
            lambda: forecast(repo, ['nowhere.md'])['at_risk'])
        arm('arm3-oldest-only-not-risk', 0,
            lambda: forecast(repo, ['old-only.md'])['at_risk'])
        arm('arm4-three', 1,
            lambda: forecast(repo, ['beta.md'])['at_risk'])
        arm('arm5-ignored-skill-zero', 0,
            lambda: forecast(repo, ['SKILL.md'])['at_risk'])
        arm('arm6-empty-set-setup', 'setup', lambda: (
            forecast(repo, []),
            'no-setup')[1])
        arm('arm7-missing-ledger-setup', 'setup', lambda: (
            forecast(repo, ['shared.md'],
                     ledger_path=repo / 'absent-ledger.json'),
            'no-setup')[1])
        # the union of two edits is not their sum: shared.md hits two
        # sections, beta.md one, together still two distinct sections
        arm('arm8-union-not-sum', 2,
            lambda: forecast(repo, ['shared.md', 'beta.md'])['at_risk'])
    finally:
        shutil.rmtree(work, ignore_errors=True)

    passed = 0
    for name, ok, got, want in results:
        print('SELFTEST %-28s %s (got=%s want=%s)'
              % (name, 'ok' if ok else 'FAIL', got, want))
        if ok:
            passed += 1
    print('REKEY_COST_SELFTEST: %d/%d pass' % (passed, len(results)))
    return 0 if passed == len(results) and len(results) == SELFTEST_ARMS else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--repo', default='.',
                    help='lane root the ledger and SKILL.md are read from')
    ap.add_argument('--ledger', default=None, help='ledger JSON path')
    ap.add_argument('--skill', default=None, help='SKILL.md path')
    ap.add_argument('--edit', action='append', default=[],
                    help='planned repo-relative edit path (repeatable)')
    ap.add_argument('--edit-file', default=None,
                    help='file with one planned path per line (# comments)')
    ap.add_argument('--json-out', default=None)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        try:
            return selftest()
        except OSError as exc:
            print('REKEY_COST error=selftest-setup:%s' % exc, file=sys.stderr)
            return 2
    edits = list(a.edit)
    if a.edit_file:
        try:
            edits.extend(read_edit_file(a.edit_file))
        except OSError as exc:
            print('REKEY_COST error=edit-file-unreadable:%s' % exc,
                  file=sys.stderr)
            return 2
    try:
        result = forecast(a.repo, edits, a.ledger, a.skill)
    except SetupError as exc:
        print('REKEY_COST error=%s' % exc, file=sys.stderr)
        return 2
    if a.json_out:
        Path(a.json_out).write_text(
            json.dumps(result, indent=1, ensure_ascii=True) + '\n',
            encoding='utf-8')
    return run_forecast(a.repo, edits, a.ledger, a.skill)


if __name__ == '__main__':
    sys.exit(main())
