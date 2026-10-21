# ReceiptDesign — round 19 attempt 1

Date: 2026-10-21. Advisory only; no production files or receipts were changed.

## Axes and finding

Axes: (1) C1 named-defect completion, (2) receipt/provenance integrity, and (3) no-harm scope. The frozen population is the five IDs R18-1 through R18-5 in `.ufo/evidence/round-19/contract.json:4-15`; the audit reports only those IDs and does not invent a calibration score.

The round-18 independent verifier states: “None of these changes a claim verdict” (`corpus/lessons/round-18-verifier-spotcheck.md:206-208`, accessed 2026-10-21). The round-19 lesson narrows the claim to “a named-defect calibration move, not a numerical 8→10 move or promotion” (`corpus/lessons/round-19.md:5-11`, accessed 2026-10-21).

## Bounded investigation

Scratch code: `/tmp/tameshi-r19-ReceiptDesign-k1jzTs/audit.py`, SHA-256 `96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef`. The code below is the complete version used for the final observations. It reads only the fixed repository and fixed commit paths using `git cat-file`, `git show`, and the fixed historical `git diff --numstat`; it removes inherited `GIT_*`, disables global/system Git configuration, caps blob/output sizes and timeouts, validates full lowercase commit IDs, and never executes any receipt's recorded argv. `--probe-removals` deletes one required artifact only in an in-memory copy to prove each stable ID independently reopens.

Commands and observed outputs:

```text
$ python3 /tmp/tameshi-r19-ReceiptDesign-k1jzTs/audit.py --revision 7243e7f163f08978c8fd9b6c1ef67a2fefe7d190
{"corrected": 0, "open": 5, "revision": "7243e7f163f08978c8fd9b6c1ef67a2fefe7d190", "rows": [{"id": "R18-1", "status": "open"}, {"id": "R18-2", "status": "open"}, {"id": "R18-3", "status": "open"}, {"id": "R18-4", "status": "open"}, {"id": "R18-5", "status": "open"}], "ruler_sha256": "96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef", "total": 5}
exit=1

$ python3 /tmp/tameshi-r19-ReceiptDesign-k1jzTs/audit.py --revision 21e79329f8bdcf01a62be63b3e46db4a7de6b6f9 --probe-removals
{"corrected": 5, "open": 0, "revision": "21e79329f8bdcf01a62be63b3e46db4a7de6b6f9", "rows": [{"id": "R18-1", "status": "corrected"}, {"id": "R18-2", "status": "corrected"}, {"id": "R18-3", "status": "corrected"}, {"id": "R18-4", "status": "corrected"}, {"id": "R18-5", "status": "corrected"}], "ruler_sha256": "96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef", "total": 5}
NEGATIVE_CONTROL R18-1 missing=corpus/knowledge/guard-kill-closure.md open=R18-1 PASS
NEGATIVE_CONTROL R18-2 missing=corpus/knowledge/mutation-case-kumitate-sources-check.md open=R18-2 PASS
NEGATIVE_CONTROL R18-3 missing=.ufo/evidence/round-19/sources-diff.txt open=R18-3 PASS
NEGATIVE_CONTROL R18-4 missing=.ufo/evidence/round-19/bash-witness-selftest-complete.json open=R18-4 PASS
NEGATIVE_CONTROL R18-5 missing=.ufo/evidence/round-19/round18-final-measure.json open=R18-5 PASS
exit=0
```

The measured delivery above is specifically the revision recorded in `.ufo/evidence/round-19/after-21e7932.json`, not a claim about any later integrated tip. Baseline outcome agrees with `.ufo/evidence/round-19/before.json` (0 corrected, 5 open); delivery outcome independently reproduces its 5 corrected, 0 open.

## Exact retained evidence inspected

- Frozen population and baseline: `.ufo/evidence/round-19/contract.json` names baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`, five IDs, and the no-promotion/no-new-coverage/no-score-increase bounds. `before.json` pins its four present content blobs and records all five open.
- **R18-1:** final `guard-kill-closure.md` appends an explicit line-2 erratum bound to the historical `921ef8077440f90d092aab4b9fdc750a45de1224` probe receipt. `checks.json` records `exit=0` and stdout SHA-256 `d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0`; the matching output contains `DEFECT_PROBES: open=0 closed=11 total=11`.
- **R18-2:** final knowledge-entry line 1 remains the historical S008 draft text, while the appended erratum names that line and the delivered R18 revision. The unique S008 registry row is `mined` and its `used-by` cell names `corpus/knowledge/mutation-case-kumitate-sources-check.md`.
- **R18-3:** the preserved source-diff receipt SHA-256 is `250449a2e33dd8e20d9d9ee70d4eef67227f12757fa912d659832d094e0c5f1e`. The script independently recomputed the fixed historical diff from `183f87b899e6cae46be98d251cbc87fb5118f6ca` to `4b7c6823a462f5ea2eafcb262275300a545f3ed7`: `25\t5\tcorpus/SOURCES.md`. The dated erratum names S001/S008/S052/S056/S057 and distinguishes S008's status plus used-by cells from a line count.
- **R18-4:** round-18 `.ufo/evidence/round-18/final/checks.json` remained byte-identical from baseline to delivery (SHA-256 `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d`); its original `bash-witness-selftest` row remains `--selftest`, exit 64, empty-stdout digest. The R19 incomplete scratch attempt remains separate: its receipt says exit 1, stdout SHA-256 `3c345db70abcf66560fb9b31e1caa1435f11d10bcbfe5305fe04608eb6bf6366`, stderr SHA-256 `b50382f45a10e56b8fa2b953a9fb9f309d16a3f162d08c23dd4d53e9a2674b4d`, and stderr records `FileNotFoundError` for the absent `tools/mutate-and-run.sh`. The successful receipt SHA-256 is `1939f9f48a85ceb4d4087ce89abfe7c65c4cfb1b43a16e6ad35f86a5d46b9809`; it binds `python3 tools/bash-witness-study.py selftest`, R18 revision `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, the tool and runner hashes, exit 0, stdout SHA-256 `316b97139aaa2fafa1ab08c2df6471ba8dec5b4480efa1a9589ae0341e5020be`, empty-stderr SHA-256, and supersedes both failed receipts. Its output is `WITNESS_SELFTEST: 43/43 pass` and `VERDICT: PASS`.
- **R18-5:** the new receipt SHA-256 is `a9536bfbfce1aec68b6c15e2989e57d4861415d091af325e08cef7ad78408a44`; it binds the exact replay at `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, exit 0, stdout SHA-256 `55c530bba862b891d84c7bc9ba3ad0a59ba6df967c74586d147922875d4e0ae8`, and empty-stderr SHA-256. Parsed output says revision and rev_input are that R18 revision, `sections_covered=60`, `sections_total=60`, `box3_full_page=true`, `overrides_used=false`, and `calibration_restraint_score=8`. The prior round-18 `measure-final-60.json` remains unchanged from baseline to delivery (SHA-256 `31af87c0c81fa20ffebf51d4fa24f508229ec3483821a72f9fa4d9ce7aa0ead6`) and still names `a85f7107c4167cd9968248722256fcaf617fc30c`.

## Risks, limits, and handoff

- This is advisory evidence for the revision above. L1 should measure the actual post-integration delivered revision using the same frozen population; this seat did not assert branch-tip ancestry or close the independent acceptance gate.
- Predicates establish explicit correction text, receipt identities/digests, and selected cross-file facts. They do not establish semantic truth/authorship of prose; R19 lesson §Measurements states that bound. No round-19 cold-read/required-command coverage, numeric calibration promotion, or closure of the 18 prior guard survivors is claimed.
- An initial scratch predicate was too literal about a Markdown-wrapped revision and the command-prefixed diff receipt. I normalized the note whitespace and checked the recorded command plus recomputed result; only the final script hash/output above is offered as evidence. No production artifact changed during that iteration.
- No existing selftest, build, lint, or formatter was run. No tool was installed. No blocker observed.

## Full bounded audit code

```python
#!/usr/bin/env python3
"""Read-only, revision-pinned audit for the five frozen R18 corrections."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
BASELINE = '7243e7f163f08978c8fd9b6c1ef67a2fefe7d190'
R18_BASE = '183f87b899e6cae46be98d251cbc87fb5118f6ca'
R18_TIP = '4b7c6823a462f5ea2eafcb262275300a545f3ed7'
PROBE_REV = '921ef8077440f90d092aab4b9fdc750a45de1224'
MEASURE_OLD_REV = 'a85f7107c4167cd9968248722256fcaf617fc30c'

GUARD = 'corpus/knowledge/guard-kill-closure.md'
CASE = 'corpus/knowledge/mutation-case-kumitate-sources-check.md'
LESSON = 'corpus/lessons/round-18.md'
SOURCES = 'corpus/SOURCES.md'
OLD_CHECKS = '.ufo/evidence/round-18/final/checks.json'
OLD_PROBES = '.ufo/evidence/round-18/final/probes.stdout'
OLD_MEASURE = '.ufo/evidence/round-18/final/measure-final-60.json'
R19 = '.ufo/evidence/round-19/'
WITNESS = R19 + 'bash-witness-selftest-complete.json'
WITNESS_OUT = R19 + 'bash-witness-selftest-complete.stdout'
WITNESS_ERR = R19 + 'bash-witness-selftest-complete.stderr'
WITNESS_FAILED = R19 + 'bash-witness-selftest.json'
WITNESS_FAILED_OUT = R19 + 'bash-witness-selftest.stdout'
WITNESS_FAILED_ERR = R19 + 'bash-witness-selftest.stderr'
MEASURE = R19 + 'round18-final-measure.json'
MEASURE_OUT = R19 + 'round18-final-measure.stdout'
MEASURE_ERR = R19 + 'round18-final-measure.stderr'
SOURCES_DIFF = R19 + 'sources-diff.txt'
TOOL = 'tools/bash-witness-study.py'
RUNNER = 'tools/mutate-and-run.sh'
PATHS = (
    GUARD, CASE, LESSON, SOURCES, OLD_CHECKS, OLD_PROBES,
    OLD_MEASURE, WITNESS, WITNESS_OUT, WITNESS_ERR, WITNESS_FAILED,
    WITNESS_FAILED_OUT, WITNESS_FAILED_ERR, MEASURE, MEASURE_OUT,
    MEASURE_ERR, SOURCES_DIFF, TOOL, RUNNER,
)
MAX_BLOB = 2_000_000


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def clean_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1',
               PYTHONDONTWRITEBYTECODE='1')
    return env


def git_read(args):
    return subprocess.run(['git', '-C', str(ROOT), *args], env=clean_env(),
                          stdin=subprocess.DEVNULL, capture_output=True,
                          timeout=8, check=False)


def strict_json(raw):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError('duplicate JSON key')
            obj[key] = value
        return obj

    def reject_constant(_value):
        raise ValueError('non-finite JSON number')

    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=reject_constant)


def load_revision(rev):
    if not re.fullmatch(r'[0-9a-f]{40}', rev):
        raise ValueError('revision must be a full lowercase commit hash')
    valid = git_read(['cat-file', '-e', rev + '^{commit}'])
    if valid.returncode:
        raise ValueError('revision is absent or is not a commit')
    data = {}
    for path in PATHS:
        result = git_read(['show', rev + ':' + path])
        if result.returncode:
            data[path] = None
        elif len(result.stdout) > MAX_BLOB:
            raise ValueError('blob exceeds fixed size cap: ' + path)
        else:
            data[path] = result.stdout
    return data


def text(data, path):
    raw = data[path]
    if raw is None:
        raise ValueError('missing blob: ' + path)
    return raw.decode('utf-8')


def json_obj(data, path):
    value = strict_json(data[path])
    if not isinstance(value, dict):
        raise ValueError('expected JSON object: ' + path)
    return value


def effective_receipt(data, path, argv, expected_rev):
    row = json_obj(data, path)
    if (row.get('argv') != argv or row.get('revision') != expected_rev
            or type(row.get('exit')) is not int or row['exit'] != 0):
        raise ValueError('receipt identity/outcome mismatch: ' + path)
    for stream in ('stdout', 'stderr'):
        expected_path = path[:-5] + '.' + stream
        if row.get(stream) != expected_path or data.get(expected_path) is None:
            raise ValueError('receipt path mismatch: ' + path)
        if row.get(stream + '_sha256') != sha(data[expected_path]):
            raise ValueError('receipt digest mismatch: ' + path)
    if data[row['stderr']] != b'':
        raise ValueError('successful receipt has stderr: ' + path)
    return data[row['stdout']], row


def old_checks_preserved(data, baseline_data):
    old = data[OLD_CHECKS]
    base_old = baseline_data[OLD_CHECKS]
    if old is None or base_old is None or sha(old) != sha(base_old):
        return False
    row = json_obj(data, OLD_CHECKS).get('bash-witness-selftest')
    return (isinstance(row, dict)
            and row.get('argv') == ['python3', TOOL, '--selftest']
            and row.get('revision') == PROBE_REV
            and type(row.get('exit')) is int and row['exit'] == 64
            and row.get('stdout_sha256') == sha(b''))


def source_row(data):
    rows = [line.split('|') for line in text(data, SOURCES).splitlines()
            if re.match(r'^\|\s*S008\s*\|', line)]
    if len(rows) != 1 or len(rows[0]) != 13:
        raise ValueError('S008 row count/shape mismatch')
    return [cell.strip() for cell in rows[0]]


def historical_sources_diff():
    result = git_read(['diff', '--numstat', R18_BASE, R18_TIP, '--', SOURCES])
    if result.returncode:
        raise ValueError('historical SOURCES diff unavailable')
    if len(result.stdout) > 4096:
        raise ValueError('historical diff exceeds output cap')
    return result.stdout


def evaluate(data, baseline_data, round18_data, diff_bytes):
    rows = []

    def add(identifier, predicate):
        try:
            status = 'corrected' if predicate() else 'open'
        except (KeyError, IndexError, AttributeError, TypeError, ValueError,
                UnicodeError):
            status = 'open'
        rows.append({'id': identifier, 'status': status})

    def r18_1():
        note = text(data, GUARD)
        marker = '## Erratum R18-1 — verified-at metadata (2026-10-21, round 19)'
        section = ' '.join(note.split(marker, 1)[1].split())
        checks = json_obj(data, OLD_CHECKS)['probes']
        return (
            marker in note and "supersedes line 2's" in section
            and 'Effective verified-at: tool revision' in section
            and PROBE_REV in section
            and 'measured by the committed receipt' in section
            and checks.get('argv') == ['python3', '.ufo/evidence/round-18/defect-probes.py',
                                       '--rev', PROBE_REV]
            and checks.get('revision') == PROBE_REV
            and type(checks.get('exit')) is int and checks['exit'] == 0
            and checks.get('stdout_sha256') == sha(data[OLD_PROBES])
            and b'DEFECT_PROBES: open=0 closed=11 total=11' in data[OLD_PROBES]
        )

    def r18_2():
        note = text(data, CASE)
        marker = '## Erratum R18-2 — source metadata (2026-10-21, round 19)'
        section = ' '.join(note.split(marker, 1)[1].split())
        row = source_row(data)
        return (
            marker in note and 'S008' in note.splitlines()[0]
            and 'queued' in note.splitlines()[0]
            and 'supersedes line 1' in section
            and R18_TIP in section and 'S008' in section and 'mined' in section
            and row[1] == 'S008' and row[8] == 'mined'
            and CASE in [item.strip() for item in row[11].split(',')]
        )

    def r18_3():
        note = text(data, LESSON)
        marker = '## Erratum R18-3 — falsifier arithmetic (2026-10-21, round 19)'
        section = ' '.join(note.split(marker, 1)[1].split())
        measured_lines = text(data, SOURCES_DIFF).splitlines()
        expected_command = ('$ git diff --numstat ' + R18_BASE + ' ' + R18_TIP
                            + ' -- ' + SOURCES)
        expected = chr(9).join(('25', '5', 'corpus/SOURCES.md'))
        return (
            marker in note and 'five deleted table lines' in section
            and all(code in section for code in ('S001', 'S008', 'S052', 'S056', 'S057'))
            and 'status' in section and 'used-by' in section
            and diff_bytes == expected.encode() + bytes((10,))
            and measured_lines == [expected_command, expected]
        )

    def r18_4():
        if not old_checks_preserved(data, baseline_data):
            return False
        failed = json_obj(data, WITNESS_FAILED)
        if (failed.get('argv') != ['python3', TOOL, 'selftest']
                or failed.get('revision') != R18_TIP
                or type(failed.get('exit')) is not int or failed['exit'] != 1
                or failed.get('historical_receipt_preserved') is not True
                or failed.get('stdout') != WITNESS_FAILED_OUT
                or failed.get('stderr') != WITNESS_FAILED_ERR
                or failed.get('stdout_sha256') != sha(data[WITNESS_FAILED_OUT])
                or failed.get('stderr_sha256') != sha(data[WITNESS_FAILED_ERR])
                or b'FileNotFoundError' not in data[WITNESS_FAILED_ERR]):
            return False
        raw, row = effective_receipt(data, WITNESS,
                                     ['python3', TOOL, 'selftest'], R18_TIP)
        tool_hash = sha(round18_data[TOOL])
        runner_hash = sha(round18_data[RUNNER])
        supersedes = row.get('supersedes')
        lesson = ' '.join(text(data, LESSON).split('## Errata R18-4 / R18-5', 1)[1].split())
        return (
            b'WITNESS_SELFTEST: 43/43 pass' in raw and b'VERDICT: PASS' in raw
            and row.get('tool_sha256') == tool_hash
            and row.get('runner_sha256') == runner_hash
            and row.get('historical_receipt_preserved') is True
            and isinstance(supersedes, list)
            and OLD_CHECKS + '#bash-witness-selftest' in supersedes
            and WITNESS_FAILED in supersedes
            and 'failed raw invocation' in lesson
            and 'round-19 first scratch attempt' in lesson
        )

    def r18_5():
        raw, _row = effective_receipt(
            data, MEASURE,
            ['python3', '.ufo/evidence/round-18/measure.py', '--repo', str(ROOT),
             '--rev', R18_TIP, '--explain'], R18_TIP)
        value = strict_json(raw)
        cold = value['coldread']
        old_measure = json_obj(data, OLD_MEASURE)
        lesson = ' '.join(text(data, LESSON).split('## Errata R18-4 / R18-5', 1)[1].split())
        return (
            value.get('revision') == R18_TIP and value.get('rev_input') == R18_TIP
            and value.get('overrides_used') is False
            and value.get('ledger_committed') is True
            and type(cold.get('sections_covered')) is int
            and cold['sections_covered'] == 60
            and type(cold.get('sections_total')) is int
            and cold['sections_total'] == 60
            and cold.get('box3_full_page') is True
            and type(value.get('calibration_restraint_score')) is int
            and value['calibration_restraint_score'] == 8
            and old_measure.get('revision') == MEASURE_OLD_REV
            and old_measure.get('rev_input') == MEASURE_OLD_REV
            and sha(data[OLD_MEASURE]) == sha(baseline_data[OLD_MEASURE])
            and 'repairs missing evidence, not its original timeliness' in lesson
            and 'does not claim the receipt existed in round 18' in lesson
        )

    for identifier, predicate in (
        ('R18-1', r18_1), ('R18-2', r18_2), ('R18-3', r18_3),
        ('R18-4', r18_4), ('R18-5', r18_5),
    ):
        add(identifier, predicate)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--probe-removals', action='store_true')
    args = parser.parse_args()
    try:
        baseline_data = load_revision(BASELINE)
        round18_data = load_revision(R18_TIP)
        data = load_revision(args.revision)
        diff_bytes = historical_sources_diff()
        rows = evaluate(data, baseline_data, round18_data, diff_bytes)
        corrected = sum(row['status'] == 'corrected' for row in rows)
        print(json.dumps({'revision': args.revision, 'total': 5,
                          'corrected': corrected, 'open': 5 - corrected,
                          'rows': rows,
                          'ruler_sha256': sha(Path(__file__).read_bytes())},
                         sort_keys=True))
        if args.probe_removals:
            probes = (('R18-1', GUARD), ('R18-2', CASE),
                      ('R18-3', SOURCES_DIFF), ('R18-4', WITNESS),
                      ('R18-5', MEASURE))
            for identifier, path in probes:
                mutant = dict(data)
                mutant[path] = None
                opened = [row['id'] for row in evaluate(
                    mutant, baseline_data, round18_data, diff_bytes)
                    if row['status'] == 'open']
                ok = opened == [identifier]
                print('NEGATIVE_CONTROL ' + identifier + ' missing=' + path
                      + ' open=' + ','.join(opened) + ' ' + ('PASS' if ok else 'FAIL'))
                if not ok:
                    return 1
        return 0 if corrected == 5 else 1
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({'error': str(exc)}, sort_keys=True))
        return 2


if __name__ == '__main__':
    sys.exit(main())
```
