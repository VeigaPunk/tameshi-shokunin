# MutC1M8 — C1 counter mutation probe (round-42 wave 1)

**Seat**: L1Tameshi42.MutC1M8 (mutation-tester, leaf). **Date**: 2026-10-25.
**Scope**: C1 counter `.ufo/evidence/round-42/calibration/measure.py` (contract
`counter_sha256` = `9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e`).
**Detector**: `python3 <copy> --selftest` (9 built-in fixture cases, exit 0 iff all OK).
No lane revision was measured — the deciding run belongs to L1; only the counter's own
selftest and throwaway fixture repos were used.

## Findings

Pristine copy of `measure.py` (sha256 `9782a5a0…914c0e`, matches the contract pin) was
placed at `/tmp/tameshi-r42-MutC1M8-w1/m.py`; baseline `--selftest` exits 0, 9/9 OK.
Four single-point mutants were created as `m1.py`–`m4.py` (each differs from pristine in
exactly one line, verified by `diff -u`; scratch dir deleted after evidence capture).

| Mutant | Source point (pristine) | Mutation | Selftest | Verdict |
|---|---|---|---|---|
| M1 | `measure.py:79` `BACKTICK_RE = re.compile(r'`([^`\n]+)`')` | revert to `r'`([^`]+)`'` (spans may cross newlines) | 8/9, `T1_new_extractor_sees FAIL`, exit 1 | **KILLED** (T1_new_extractor_sees) |
| M2 | `measure.py:86` `FLEET_ONLY_PREFIXES` + `path_tokens` skip (`:168-169`) | drop the `FLEET_ONLY_PREFIXES` skip | 9/9 OK, exit 0 | **SURVIVED** |
| M3 | `measure.py:166` skip chars `'<>*{}|()…, $'` | drop `$` from skip chars | 9/9 OK, exit 0 | **SURVIVED** |
| M4 | `measure.py:135` section boundary guard | boundary condition → `if False:` (section runs to EOF) | 8/9, `T5_section_bounded FAIL`, exit 1 | **KILLED** (T5_section_bounded) |

### M1 — killed
Command: `python3 /tmp/tameshi-r42-MutC1M8-w1/m1.py --selftest` → `SELFTEST T1_new_extractor_sees FAIL`; `C1_R42_SELFTEST: cases=9 failed=1`; EXIT=1. Killer fixture `T1_new_extractor_sees` asserts `path_tokens('opens `here\nand `tools/missing.py` is cited\n') == ['tools/missing.py']`; with cross-newline spans the grouping is `["here\nand "]` and the dead path is hidden. (`T1_old_extractor_misses` still OK — expected, both extractors miss under the old regex.)

### M4 — killed
Command: `python3 /tmp/tameshi-r42-MutC1M8-w1/m4.py --selftest` → `SELFTEST T5_section_bounded FAIL`; exit 1. Killer fixture `T5_section_bounded` asserts `section('## Round 42\na `tools/x.py`\n## Round 43\n`tools/y.py`\n', '## Round 42')` excludes `tools/y.py`; running to EOF includes it.

### M2 — survived; killer fixture
Command: `python3 /tmp/tameshi-r42-MutC1M8-w1/m2.py --selftest` → 9/9 OK, exit 0
(no fixture cites a `.ufo/reports|prompts|state/` path). Demonstrated killer fixture
(harness `/tmp/tameshi-r42-MutC1M8-w1/kill_fixture.py`, run before cleanup): a round-42
lesson citing `.ufo/reports/x.md` absent at REV —
pristine `audit` → `m8=0`; mutant → `m8=1` (`m8 .ufo/reports/x.md cited in corpus/lessons/round-42.md does not resolve`).
**Fixture to add**: a selftest case (T6-style) building `base` + `corpus/lessons/round-42.md`
= `'cites ` .ufo/reports/x.md`\n'` and asserting `count(audit(Repo(root,'HEAD'), ''), 'm8') == 0`.

### M3 — survived; killer fixture
Command: `python3 /tmp/tameshi-r42-MutC1M8-w1/m3.py --selftest` → 9/9 OK, exit 0
(no fixture contains `$` in a backtick span). Demonstrated killer fixture: a round-42
lesson citing `corpus/$NAME.md` absent at REV —
pristine `audit` → `m8=0`; mutant → `m8=1` (`m8 corpus/$NAME.md cited in corpus/lessons/round-42.md does not resolve`).
**Fixture to add**: a selftest case asserting `count(audit(Repo(root,'HEAD'), ''), 'm8') == 0` on `base` + lesson `'cites `corpus/$NAME.md`\n'`.

## Evidence
- Baseline: `python3 /tmp/tameshi-r42-MutC1M8-w1/m.py --selftest` → 9/9 OK, `C1_R42_SELFTEST: cases=9 failed=0`, EXIT=0.
- Hashes (before/after): pristine `m.py` `9782a5a0…914c0e` (unchanged, == contract pin);
  `m1.py` `f168ee95…d62ed`; `m2.py` `3e634498…f2d914`; `m3.py` `b3910ac8…2e8e`;
  `m4.py` `82e165b6…375aae`.
- Diffs (each exactly one line): M1 `measure.py:79`; M2 `:168-169` removed; M3 `:166`;
  M4 `:135`.

## Not checked
- No lane/fleet measurement run (forbidden pre-deciding; L1 owns the deciding run).
- No live-tree behavior beyond the selftest fixtures and the two throwaway audit repos above.
- Killer fixtures for M2/M3 are demonstrated but not yet committed into `measure.py`'s
  selftest (the counter is read-only for this seat; recommendation only).
