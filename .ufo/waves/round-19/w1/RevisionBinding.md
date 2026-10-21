# Revision binding — round 19 attempt 1

## Finding

- **Axis / scope:** C1 calibration, bounded to the five frozen R18 defects. The frozen contract names baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`, before 0, target 5 (`.ufo/evidence/round-19/contract.json:4-15`). This probe does not claim a numeric calibration increase; the recorded restraint score remains 8.
- **Observed:** the corrected measurement receipt `.ufo/evidence/round-19/round18-final-measure.json` records exact `--rev` / `revision` `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, exit 0, and stdout SHA-256 `55c530bba862b891d84c7bc9ba3ad0a59ba6df967c74586d147922875d4e0ae8` (receipt lines 2-18). Its stdout carries matching `revision` and `rev_input`, `overrides_used: false`, cold-read `sections_covered: 60`, `sections_total: 60`, `box3_full_page: true`, and restraint score 8 (`round18-final-measure.stdout:2-4,1920-1947`).
- **Scope boundary:** this confirms what the exact-revision receipt records, not round-19 final-tip cold-read coverage or current-input equivalence. The lesson explicitly bounds the historical replay: `corpus/lessons/round-19.md:67-70` (read 2026-10-21): “at 4b7c682, not at round19 tip.” No Git tip lookup or inference was made by this probe. This addresses the routed R18-5 gap (`corpus/lessons/round-18-verifier-spotcheck.md:201-204`) without backdating the receipt.

## Read-only bounded probe

Source files read: `.ufo/evidence/round-19/round18-final-measure.json`, `.ufo/evidence/round-19/round18-final-measure.stdout`, `.ufo/evidence/round-19/round18-final-measure.stderr`, `.ufo/evidence/round-19/measure.py:61-76,121-136`, `.ufo/evidence/round-19/contract.json`, and `corpus/lessons/round-19.md:56-70`. No receipt argv was executed. The round-19 measure implementation and its existing selftests were read only; no existing selftest, build, lint, formatter, or test was run.

I wrote this standalone read-only checker in unique scratch `/tmp/tameshi-r19-RevisionBinding-J23TNH/check_receipt.py`. It validates the fixed receipt/output paths, exact recorded invocation and revision, integer-zero exit, output digests, empty stderr, and the output's exact revision inputs and boolean no-overrides field. It never executes recorded argv, invokes Git, or inspects `HEAD`; its historical cold-read values are reported only as values present in the receipt.

Command: `python3 /tmp/tameshi-r19-RevisionBinding-J23TNH/check_receipt.py`

Observed output:

```text
PASS receipt revision=4b7c6823a462f5ea2eafcb262275300a545f3ed7 exit=0 stdout_sha256=matched
PASS output revision=4b7c6823a462f5ea2eafcb262275300a545f3ed7 rev_input=4b7c6823a462f5ea2eafcb262275300a545f3ed7 overrides_used=false
OBSERVED receipt coldread sections=60/60 restraint_score=8 box3_full_page=True
SCOPE round-19-final-tip-coverage=not-checked
```

## Checker code

```python
#!/usr/bin/env python3
"""Read-only binding check; never executes recorded argv or consults Git HEAD."""
import hashlib
import json
from pathlib import Path

ROOT = Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin')
BASE = '.ufo/evidence/round-19/round18-final-measure'
MEASURED_REV = '4b7c6823a462f5ea2eafcb262275300a545f3ed7'
EXPECTED_ARGV = [
    'python3', '.ufo/evidence/round-18/measure.py', '--repo',
    str(ROOT), '--rev', MEASURED_REV, '--explain',
]


def strict_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key: ' + key)
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError('non-finite JSON constant: ' + value)

    return json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    receipt_path = BASE + '.json'
    row = strict_json((ROOT / receipt_path).read_bytes())
    require(type(row) is dict, 'receipt must be an object')
    require(row.get('argv') == EXPECTED_ARGV, 'recorded invocation mismatch')
    require(row.get('revision') == MEASURED_REV, 'receipt revision mismatch')
    require(type(row.get('exit')) is int and row['exit'] == 0,
            'receipt exit is not integer zero')

    streams = {}
    for name in ('stdout', 'stderr'):
        expected_path = BASE + '.' + name
        require(row.get(name) == expected_path, name + ' path mismatch')
        raw = (ROOT / expected_path).read_bytes()
        require(row.get(name + '_sha256') == hashlib.sha256(raw).hexdigest(),
                name + ' digest mismatch')
        streams[name] = raw
    require(streams['stderr'] == b'', 'stderr is not empty')

    result = strict_json(streams['stdout'])
    require(type(result) is dict, 'measurement output must be an object')
    require(result.get('revision') == MEASURED_REV, 'output revision mismatch')
    require(result.get('rev_input') == MEASURED_REV, 'input revision mismatch')
    require(result.get('overrides_used') is False, 'overrides_used is not false')

    # Report the receipt's recorded historical cold-read values, but do not
    # infer or inspect coverage at a round-19/final tip.
    cold = result.get('coldread')
    require(type(cold) is dict, 'coldread record missing')
    require(type(cold.get('sections_covered')) is int, 'covered count is not integer')
    require(type(cold.get('sections_total')) is int, 'total count is not integer')
    require(type(result.get('calibration_restraint_score')) is int,
            'restraint score is not integer')
    print('PASS receipt revision=' + row['revision'] + ' exit=0 stdout_sha256=matched')
    print('PASS output revision=' + result['revision'] + ' rev_input=' + result['rev_input']
          + ' overrides_used=false')
    print('OBSERVED receipt coldread sections=' + str(cold['sections_covered']) + '/'
          + str(cold['sections_total']) + ' restraint_score='
          + str(result['calibration_restraint_score']) + ' box3_full_page='
          + str(cold.get('box3_full_page')))
    print('SCOPE round-19-final-tip-coverage=not-checked')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        raise SystemExit('FAIL ' + str(exc))
```

## Risks and blockers

- **Risk:** this pure consistency checker verifies the committed receipt bytes, revision binding and no-overrides result, but does not prove correctness/completeness of the underlying historical cold-read or make a current-tip coverage claim. It is advisory evidence, not the failure-capable five-defect audit or independent closure.
- **Blockers:** none for this scoped finding. No tools installed/updated. No production files, Git/JJ state, global configs, or siblings changed.
- **Files written:** this advisory report and `/tmp/tameshi-r19-RevisionBinding-J23TNH/check_receipt.py` only.
