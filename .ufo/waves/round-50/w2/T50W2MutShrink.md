# T50W2MutShrink — C2 shrinker selftest mutation probe (round-50 wave-2)

Seat: `T50W2MutShrink` (leaf). Assignment: mutation-test `tools/shrink-case.py`
at `80ea77e99e239982ab0b93e416645ef2359725d3` against its own `--selftest`, run in a
directory holding `pbt-staged-id.py` and `staged-id-guard.py` copies from that revision
(real-guard leg runs). All runs: pristine/mutant `shrink-case.py` byte-restored per case
(sha256 verified after every run); selftest executed as
`python3 -I shrink-case.py --selftest` with `TMPDIR=$S/w`; per-run timeout 180 s.

## Baseline

Environment: `S=/fast/scratch/hyaku/tameshi-r50/T50W2MutShrink`; copies of
`tools/{shrink-case.py,pbt-staged-id.py,staged-id-guard.py}` extracted from
`80ea77e9` (`git -C LANE show 80ea77e9:tools/<f>`).
Shas: shrink-case `1ac31ae5…`, pbt `a6e1253a…`, guard `03a796c5…`
(= `GUARD_SHA256` in `.ufo/evidence/round-50/c2/measure.py`).

Pristine selftest: exit 0, `cases=20 failed=0` (all 20 checks ok; the M02
embedded-edit-vs-panel check reports `skip (panel not reachable)` because the panel
tree is not part of the mandated scratch layout — the real-guard M02 leg itself runs
end to end). Receipt: `T50W2MutShrink.baseline.log`.

## Mutants (15 single-edit; anchors at 80ea77e9)

| id | area | edit (anchor, line) | verdict | failing / differential evidence |
|----|------|---------------------|---------|--------------------------------|
| M01 | chunk split | partition: `1 if index < extra else 0` → `0` (L93) | SURVIVED | no case/exit diff in 150 seeds; run-cost diff in 109/150 (7 vs 5 on the seed-0 case; example `kill-M01.json`) |
| M02 | granularity refinement | `n = min(2*n, len(current))` → `n = 2*n` (L133) | SURVIVED | 60 randomized seeds: no divergence (exit, output case, runs all equal) |
| M03 | granularity refinement | `n = max(n-1, 2)` → `n = 2` (L120) | SURVIVED | 60 randomized seeds: no divergence |
| M04 | complement step | `if len(chunk) >= len(current):` → `… or len(chunk) == 1:` (L124) | SURVIVED | 60 randomized seeds: no divergence |
| M05 | fixpoint loop | single-unit pass condition `if kills(frozenset(candidate)):` → `… and False:` (L141) | KILLED | `core: an always-true predicate reduces to the empty set` FAIL (ddmin(items, True) no longer returns []) → exit 1 (`M05.log`) |
| M06 | fixpoint loop | `for item in list(current):` → `for item in current:` (L139) | SURVIVED | 150 randomized seeds: no divergence |
| M07 | cache key | `key = (role, case_key(case))` → `key = case_key(case)` (L164) | KILLED | `cli: the stub shrink exits 0` and `M02: the shrink exits 0 on the public mutant` FAIL, detail `the case carries no kill: …` (role-less cache conflates pristine/mutant verdicts) → exit 1 (`M07.log`) |
| M08 | run counter increment | `self.runs += 1` → `+= 2` (L168) | KILLED | run-count checks FAIL: stub `(26, 13)`, M02 `(14, 7)` → exit 1 (`M08.log`) |
| M09 | run counter increment | `self.runs += 1` → `+= 0` (L168) | KILLED | run-count checks FAIL: stub `(0, 13)`, M02 `(0, 7)` → exit 1 (`M09.log`) |
| M10 | unit enumeration of map entries | `units += [('map', key) for key in entries]` deleted in `shrink()` (L190–191) | SURVIVED | killing case = map-driven stub guard pair: see below |
| M11 | sub-case construction | `if ('registry', index) in keep` → `not in keep` (L195) | KILLED | `cli: the stub result is 1-minimal` and `M02: the result is 1-minimal` FAIL (result keeps droppable units) → exit 1 (`M11.log`) |
| M12 | exit codes | `return 2` → `return 0` on Unusable (L628) | SURVIVED | differential: missing case file → pristine exit 2 / mutant 0; bad-shape `{}` → pristine 2 / mutant 0 (`kill-M12.json`) |
| M13 | output fields | payload `'map': shrunk.get('map')}` → `…, '_x': 1}` (L265) | SURVIVED | differential: `out.case` carries extra `_x: 1`; all other fields identical (`kill-M13.json`) |
| M14 | input validation | `valid_case` final return → `True` (L82) | SURVIVED | differential: `map: [1,2]` case → pristine rejects cleanly exit 2; mutant proceeds and crashes `AttributeError: 'list' object has no attribute 'items'`, exit 1 (`kill-M14.json`) |
| M15 | cache key | `json.dumps(mapping, sort_keys=True)` → `sort_keys=False` (L73) | SURVIVED | 60 randomized seeds: no divergence |

Killed 5/15; survived 10/15. Baseline failure modes (timeout/hang/crash of the
selftest itself) did not occur for any mutant; killed = selftest exit ≠ 0 with the
named failing check.

## Killing cases for survivors (the 10)

- **M01** — observable difference is only the stated cost: same final case, honest
  run count differs (5 vs 7; 109/150 seeds differ in `runs` only). The C2 contract
  allows any honest cost (`runs` = logged guard invocations), so M01 cannot fail C2;
  selftest does not pin convergence cost (coverage gap).
- **M02 / M03 / M04 / M06 / M15** — no divergence in randomized differential probing
  (60 seeds each; 150 for M06) of exit code, output case, and runs on the stub
  oracle pair. No observable killing case exists under the counter's observations
  (search-path/caching equivalents).
- **M10** — killing case: stub generator (STUB_GENERATOR) + guard pair that differ
  **only** in map-key handling (mutant ignores the map); case
  `{"registry":"1\n2\n","staged":"3\n","map":{"map":{"S001":"S002","S003":"S004"}}}`.
  Pristine shrinks to the map-only 1-minimal sub-case (units 5→1, runs 7, exit 0);
  mutant (map units omitted from enumeration) finds no kill and exits 2 with
  `the case carries no kill: …` (`kill-M10.*`).
- **M12** — bad-input CLI differentials (missing case file; non-schema case JSON):
  exit 2 vs 0 (`kill-M12.json`).
- **M13** — output-shape differential: extra `_x: 1` field inside `out.case`
  (`kill-M13.json`), invisible to the counter's field reads.
- **M14** — `valid_case` weakening lets a list-valued map through; pristine exits 2
  with a clean reason, mutant crashes with an unhandled `AttributeError` (exit 1)
  (`kill-M14.json`).

## Evidence and receipts (all in `.ufo/waves/round-50/w2/`)

- `T50W2MutShrink.baseline.log` — pristine selftest (exit 0, 20/20).
- `T50W2MutShrink.M01.log` … `M15.log` — one per mutant (status line + full selftest transcript).
- `T50W2MutShrink.results-final.json` — consolidated verdict table.
- `T50W2MutShrink.probe-report.json`, `probe2-report.json` — differential probe logs
  (M01/M02/M03/M04/M06/M15 randoms; M10/M12/M13/M14 special cases).
- `T50W2MutShrink.kill-*.json` / `.txt` — killing-case inputs and both binaries' outputs.
- Probe/results code: scratch-only (`run_mutants.py`, `probe_diff.py`, `probe2.py`,
  `run_m10.py`); scratch dir deleted on completion.

Tooling: no installs made (system `python3` and `git` only; no pacman, no uv/npx).

## Summary

- Pristine `--selftest` passes (exit 0, 20/20) with the real guard copy beside the tool.
- 15 single-edit mutants across the demanded areas: **5 killed** (fixpoint disabled,
  cache role-drop, run counter ×2, sub-case inversion), **10 survived**.
- Killed mutants fail via the selftest's own checks (always-true reduction,
  no-kill Unusable, run-count honesty, 1-minimality).
- Survivors: M12/M13/M14 have concrete command-level differentials (exit codes,
  output shape, crash); M10 has a map-driven killing case (pristine 0 / mutant 2);
  M01 differs only in honest run cost; M02/M03/M04/M06/M15 showed no divergence in
  60–150 seed probes (equivalents).
- Coverage finding: selftest never pins convergence cost, and its 1-minimal/sub-case
  checks are property-based, so pure search-order defects survive — output properties
  and count honesty are what matter to C2.
