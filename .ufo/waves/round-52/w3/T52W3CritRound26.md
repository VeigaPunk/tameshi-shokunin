# T52W3CritRound26 — Round-26 registry section second read (critic)

Seat: T52W3CritRound26 (wave 3, lane tameshi). Scope: `### Round-26 gate/probe registry — report interop` (SKILL.md at CAND1 `7ff81a5b`, lines 2132–2171), all 31 rows, independently of the wave-3 reader. The wave-2 fix-read seat for this section produced no deliverable; the L1 applied 4 in-line fixes (diff base→CAND1 shows only rows 2136, 2149, 2157, 2158 changed), so 27 rows are inherited round-51 text checked here as-is.

Method: scratch clone `--shared` at `/fast/scratch/hyaku/tameshi-r52/T52W3CritRound26/clone`, checked out at CAND1 (`git rev-parse --show-toplevel` asserted). Static source review of every named tool plus live `--selftest`/usage probes run inside the scratch clone with `TMPDIR=$S/tmp`, `PYTHONDONTWRITEBYTECODE=1`. Probes are evidence, not verdicts. No tools were installed or upgraded (all required binaries already present: python3, git, jj, node, uv, strace); nothing written to PATH dirs.

## Findings (false statements)

1. **SKILL.md:2148 (mte report interop, Write scope) — TMPDIR-tree enumeration is incomplete.** The row states: "caller-chosen `--workdir`/`--emit` DIR plus isolated TMPDIR trees `tameshi-mte-selftest-*`, `tameshi-mte-fleet-*`, `tameshi-mte-regression-*`; lane read-only". The tool at CAND1 creates a fourth TMPDIR tree with prefix `tameshi-mte-` (bare) in `official_metrics()`, used on the live `--check` path (npm vendor extraction + node runner staging): `tools/mte-interop.py:199` `with tempfile.TemporaryDirectory(prefix='tameshi-mte-') as tmp:`, called from `check()` at `tools/mte-interop.py:318` `official = official_metrics(reports)`. Evidence: `grep -n "prefix='tameshi-mte" tools/mte-interop.py` → lines 199 (`tameshi-mte-`), 276 (`tameshi-mte-fleet-`), 309 (`tameshi-mte-regression-`), 386 (`tameshi-mte-selftest-`). The three named trees exist as stated; the enumeration omits the bare `tameshi-mte-*` tree, so the write-scope cell under-describes the tool's scratch writes (all TMPDIR-respecting; no /tmp hard-coding, no lane write).

## Statements verified true (31 rows, by category)

Counts / self-test tallies — all reproduced by running `--selftest` in the scratch clone at CAND1:
- Row 2136/2148 `MTE_SELFTEST: 17/17 pass`: `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`. Registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (`legs_conforming=10/10`) confirmed in `tools/registry.json` (cf. `.ufo/evidence/round-52/contract.json` C1, probe 49/49 at CAND1).
- Row 2142 `WITNESS_SELFTEST: 51/51 pass` + terminal `VERDICT: PASS`: ran `python3 tools/bash-witness-study.py selftest` → `WITNESS_SELFTEST: 51/51 pass`, `VERDICT: PASS` last line.
- Row 2143 `COMMAND_BINDING_SELFTEST:` in last stdout line: ran → `COMMAND_BINDING_SELFTEST: 44/44 pass`.
- Row 2144 `SELFTEST: PASS (49/49 cases)`: ran `python3 tools/context-capture.py --selftest` → `SELFTEST: PASS (49/49)`.
- Row 2145 `ENVDIFF_SELFTEST: 9/9 pass`: ran → `ENVDIFF_SELFTEST: 9/9 pass`.
- Row 2146 `SELFTEST: ... 66/66 cases`: ran → `SELFTEST: PASS (66/66)` (needs jj; jj present at `~/.local/bin/jj`).
- Row 2147 finding id `GOLDEN_VERDICT_SELFTEST:`: ran → `GOLDEN_VERDICT_SELFTEST: 3/3 pass`.
- Row 2149 `VERDICT: PASS` terminal after `MUTATE_SELFTEST` tally: ran `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS` last line.
- Row 2150 `PBT_STAGED_ID_SELFTEST: cases=35 failed=0`: ran → exact.
- Row 2151 `SELFTEST: PASS n/n`: ran → `SELFTEST: PASS (19/19)`.
- Row 2152 `RECEIPT_MEASURE_SELFTEST: 10/10 pass`: ran → exact; six `ITEM_IDS` in `tools/receipt-measure.py:37-44`.
- Row 2153 `RECEIPT_WINDOW_SELFTEST: 20/20 pass exit 0`: ran → exact; recorded `.ufo/evidence/round-20/final/receipt-window-selftest.json` has `"exit": 0`.
- Row 2154 `SELFTEST: PASS (51 cases)`: ran `python3 tools/registry-check.py --selftest` → `SELFTEST: PASS (51 cases)`.
- Row 2155 `REGISTRY_REPLAY_SELFTEST: 10/10 pass`: ran → exact.
- Row 2156 `SELFTEST: PASS (29 cases)`: ran → exact.
- Row 2157 `ROUND21_MEASURE_SELFTEST: 13/13 pass`: ran → exact; fleet-bound claim verified at `tools/round21-measure.py:77` (reads `FLEET` literal of `.ufo/evidence/round-21/c2-count.py`).
- Row 2158 `SHRINK_SELFTEST: cases=21 failed=0`: ran → exact.
- Row 2159 `STAGED_ID_GUARD_SELFTEST: cases=N failed=M`: `tools/staged-id-guard.py:398`.
- Row 2160 `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`: ran → exact.
- Row 2161 `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`: ran → exact.
- Row 2162 `TALLY_AUDIT_SELFTEST: 11/11 pass`: ran → exact.
- Row 2163 `SELFTEST: n/n`: ran `python3 tools/trace-inputs.py --selftest` → `SELFTEST: 30/30`, exit 0.
- Row 2164 `8/8 frozen plus 16/16 supplemental` + `FINDING: SELFTEST_PASS`: ran → `ACCOUNTING_SELFTEST: 8/8 pass`, `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`, `FINDING: SELFTEST_PASS`.
- Row 2165 `WAVE_PARENT_SELFTEST: 3/3 pass`: ran → exact.
- Row 2166 `ROUTEMIX_SELFTEST: 8/8 pass`: ran → exact.
- Row 2167 `SELFTEST: PASS 39/39`: ran → exact.
- Rows 2168–2171 census self-test counters: ran all four → `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`; `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`; `WRITE_CENSUS_V4_SELFTEST: cases=15 failed=0`; `WRITE_CENSUS_SELFTEST: planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 noflag_unchanged=1` — all exact.

Write scope (prioritised) — verified against source:
- Hard-coded /tmp (TMPDIR ignored): bash-witness-study selftest `tools/bash-witness-study.py:1240-1241` (`dir="/tmp"`); context-capture `tools/context-capture.py:1624-1625` (`dir="/tmp"`, prefix `context-capture-selftest-`, removed in `finally` at :2204-2206); env-diff sandboxes `tools/env-diff.py:61` (`prefix="tameshi-r21-envdiff.", dir="/tmp"`) with TMPDIR-respecting selftest trees at :167; evidence-disposition `tools/evidence-disposition.py:2351` (`dir="/tmp"`), removed on pass / kept on failure (:3121-3128); pin-disposition `tools/pin-disposition.py:706` (`dir="/tmp"`), removed on PASS (:1328-1329); registry-check clone + selftest `tools/registry-check.py:766`,`:916` (`dir="/tmp"`), removed afterwards (:822, :1810 `finally`); repeat-control `tools/repeat-control.py:597` (`dir="/tmp"`). All match their rows.
- TMPDIR-respecting: mte-interop (`:276`,`:309`,`:386` — see Finding 1 for the omitted `:199` tree); command-binding (`:174`, one bundle/expected pair); golden-verdict (`:47`); mutate-and-run.sh (`${TMPDIR:-/tmp}` mktemp defaults :491,:1432,:1555); pbt-staged-id (`:807`,`:1028`); receipt-measure (`:251` + delegated `.ufo/evidence/round-20/stage/measure.py:82` `tameshi-r20-measure.`); receipt-window (`:327`); registry-replay (`:149`,`:208`, TMPDIR clone + live-sibling fleet symlinks :166-168); round21-measure (`:43`); shrink-case (`:260`,`:452`,`:540`); tally-audit (`:364`,`:419`, `finally` removal :372,:435); tally-audit-v2 (`:562`,`:656`, `finally` :570-571; `/tmp/tally-audit-work` literal in CONFIGS :265); tally-audit-v3 (`:766`,`:887` + auto-root `/tmp/tameshi-r4-2-regression.XXXXXX` allocated :417-431, `atexit` rmtree); trace-inputs (`:593` `trace-inputs-run-*` deleted on exit :695, selftest :703, `--out` parent dirs created :689); wave-accounting (`:156`); witness-metadata (`:1122`, `finally` removal :1185-1186); census v1 TMPDIR-only (`tools/write-path-census.py` TemporaryDirectory fixture).
- Lane writes / `__pycache__`: shrink-case row's `tools/__pycache__` exception verified — `load_generator()` (`tools/shrink-case.py:221-228`) `exec_module`s `tools/pbt-staged-id.py` with no bytecode suppression (grep for `dont_write_bytecode`/`PYTHONDONTWRITEBYTECODE` in the tool: none); demonstrated in the scratch clone: after `importlib` exec, `tools/__pycache__/pbt-staged-id.cpython-314.pyc` exists. staged-id-guard (:426 sole `open` is `'rb'`), wave-parent-settle (:75 read-only receipt open), wave-route-mix (no write calls; docstring line 13 "Never writes anything"), census v2/v3/v4 (pure scanners, no mkdtemp/open-for-write) — all match "no writes" claims. registry-check live `--root` warning text "rows may write into the root" verbatim at `tools/registry-check.py:1928-1933`. env-diff writes only sandboxes + `--out` (`tools/env-diff.py:11`, :238-239). repeat-control `--out` refused if existing, never deleted (:317, :315).
- Verdict maps / usage exits: sampled `python3 <tool>`/unknown-flag probes — mte-interop 64; command-binding 64; context-capture 64; trace-inputs 64; wave-accounting 64; wave-route-mix 64; registry-replay 64; repeat-control 64; round21-measure 64; registry-check 64; receipt-window 64 (missing args) and 2 (invalid contract/receipts files); receipt-measure 2-on-usage (missing `--repo`, unknown `--check`, `--selftest` mixed) as its row states; shrink-case 2 and pin-disposition 2 as their rows state (no 64 claimed). mutate-and-run run-mode DEGRADED → exit 1 (`tools/mutate-and-run.sh:81`).

Pinned values: every file path named in the Pinned values cells exists at CAND1 (checked: 45 paths including `tools/vendor/*.tgz`, the four mutate-and-run defect specs, `panel.json`, settlement receipts, census fixtures — full list in probe log). Literal pins verified in source: context-receipt digest `05cb55b8…` (`tools/context-capture.py:153`), mte "ten ledger legs" message (`tools/mte-interop.py:318`), wave-parent-settle red/green literals (`tools/wave-parent-settle.py:50-52`).

## Summary

1 finding: SKILL.md:2148 omits the bare `tameshi-mte-*` TMPDIR tree (`tools/mte-interop.py:199`, live `--check` path) from its write-scope enumeration.
All other row statements verified true: 24 distinct self-test counts reproduced exactly by running the selftests at CAND1 in a scratch clone.
Write-scope claims hold: 8 hard-coded-/tmp rows match source; TMPDIR-respecting rows match; shrink-case `tools/__pycache__` exception confirmed by import test.
Usage exits match every verdict map sampled (64 vs 2 where claimed).
All 45 pinned-value paths exist at CAND1; in-source literal pins (digest, ten-legs message, settle literals) confirmed.
Only 4 of 31 rows differ from BASE (L1's partial fixes); the other 27 inherited rows still check out except the one enumeration gap.
No lane, fleet, or jj state touched; probes ran in a scratch clone (since deleted); no tools installed.
