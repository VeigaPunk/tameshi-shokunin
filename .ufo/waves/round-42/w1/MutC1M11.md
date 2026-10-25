# MutC1M11 — C1 counter mutants (wave 1)

Seat: L1Tameshi42.MutC1M11 (mutation tester)
Date: 2026-10-25
Source: `.ufo/evidence/round-42/calibration/measure.py` (contract `counter_sha256` 9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e)
Scratch: `/tmp/tameshi-r42-MutC1M11-0/` (pristine `m.py` + one mutant per copy)

## Findings

Detector: `--selftest` (9 fixture cases T1–T5). Baseline on pristine `m.py`: all 9 OK, exit 0. The live lane checkout was never edited; all runs were on copies under /tmp scratch.

### M1 — drop merge-base `--is-ancestor` check → KILLED
- Mutation: `m1.py:119` `return self.git('merge-base', '--is-ancestor', sha, self.rev).returncode == 0` → `return True` (any existing commit object passes).
- Command: `python3 /tmp/tameshi-r42-MutC1M11-0/m1.py --selftest` → `C1_R42_SELFTEST: cases=9 failed=1`, exit 1; `SELFTEST T3_unreachable_counts FAIL`.
- Mechanism: `ancestor_commit` now returns True for every existing commit object, so T3's unreachable-but-fetched lane commit (c1beba88…) stops counting; m11 = 1 instead of expected 2.

### M2 — remove `(?<!staged:)` lookbehind → KILLED
- Mutation: `m2.py:78` `S_CITE_RE = re.compile(r'(?<!staged:)\bS(\d{3,})\b')` → `re.compile(r'\bS(\d{3,})\b')`.
- Command: `python3 /tmp/tameshi-r42-MutC1M11-0/m2.py --selftest` → `C1_R42_SELFTEST: cases=9 failed=1`, exit 1; `SELFTEST T4_staged_skipped_bare_counted FAIL`.
- Mechanism: `staged:S159` now becomes a citation; registry holds no S159 → m7 = 2 (S159 + S777) instead of expected 1.

### M3 — drop `blob:`/`tree:` skip in HEX40_RE → SURVIVED
- Mutation: `m3.py:80` `HEX40_RE = re.compile(r'(?<![0-9a-f:])(?<!blob:)(?<!tree:)([0-9a-f]{40})(?![0-9a-f])')` → `re.compile(r'(?<![0-9a-f:])([0-9a-f]{40})(?![0-9a-f])')`.
- Command: `python3 /tmp/tameshi-r42-MutC1M11-0/m3.py --selftest` → `C1_R42_SELFTEST: cases=9 failed=0`, exit 0. All cases pass.
- Coverage finding (survivor): the remaining guard `(?<![0-9a-f:])` still suppresses `blob:<hex>`/`tree:<hex>` because `:` immediately precedes the hex run; verified `HEX40_RE.findall` on the T3 text returns only the reachable head and the f×40 run — the e×40 after `blob:` is never matched even without the `(?<!blob:)` lookbehind. Also, no selftest fixture exercises `tree:` at all. The blob:/tree: skip removal is undetectable by the current selftest; a fixture with a hex run preceded by a non-colon context would be needed to observe it.

## Evidence

| File | sha256 | bytes | diff vs pristine |
|---|---|---|---|
| m.py (pristine) | 9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e | 17359 | — |
| m1.py (M1) | 07ed11e38ebdc74340faa6e637dc6e6523ede66b355413ef01912f33e31d3ffd | 17293 | line 119 only |
| m2.py (M2) | ede5c35b38118e7809db6d6a6fb192d40ce6b55af1d032515856078e15eaa718 | 17347 | line 78 only |
| m3.py (M3) | 7f46590af9370f54d53bcb5522d16c05897c6524ef186e6f7bb9a766809af74d | 17339 | line 80 only |

Commands run: baseline `python3 …/m.py --selftest` (0 failed); per-mutant `python3 …/m{1,2,3}.py --selftest` (outputs above). Diff verification: `diff m.py m{1,2,3}.py` shows exactly the one targeted line each.

## Verdict

- M1: KILLED (T3).
- M2: KILLED (T4).
- M3: SURVIVED — coverage finding: `(?<![0-9a-f:])` makes the `blob:`/`tree:` lookbehinds redundant for the current fixtures, and `tree:` is untested.

Could not check: only `--selftest` was run (authorized detector); no deciding-run or live-repo counter run was performed. Live lane checkout untouched; scratch copies retained as evidence at `/tmp/tameshi-r42-MutC1M11-0/` (disposable). No tool installs/updates performed.
