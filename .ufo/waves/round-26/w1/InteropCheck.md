# Round 26 wave 1 — InteropCheck (MTE report interop verification)

Seat: `TameshiR26.InteropCheck` (executor, leaf). Report date: 2026-10-22.
Scope: run `tools/mte-interop.py --check` and `--selftest` in a private clone and
verify every mutant location of the `js-cite-check` report against the unique
`@old` string in the pinned file.

**Verdict: PASS.** `MTE_INTEROP: PASS legs_conforming=9/9` (exit 0) and
`MTE_SELFTEST: 17/17 pass` (exit 0). All ten `js-cite-check` mutant locations
(start/end line and column) match an independent recomputation from the pinned
bytes exactly. No defect found; no production file touched.

---

## 1. Environment and provenance

Private clone (no writes to the lane repo, no `jj` command anywhere):

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/interopcheck-r26
git -C /tmp/interopcheck-r26 checkout -q --detach a08e85c5d7f899e8a5992e20517edb1a380d79eb
git -C /tmp/interopcheck-r26 log --oneline -1
a08e85c round-26: ninth ledger leg js-cite-check (5/10, 10/10 verdict predictions), runner and interop wired to nine legs, mte-interop registry rows and SKILL row, sweep evidence
```

The lane working tree at `a08e85c5d7f899e8a5992e20517edb1a380d79eb` still holds the
same tool bytes as the clone, so the run exercised the committed tool, not a
drifted copy:

```
$ diff -q /tmp/interopcheck-r26/tools/mte-interop.py   /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mte-interop.py   && echo IDENTICAL
MTE_TOOL_IDENTICAL_TO_LANE_WORKTREE
$ diff -q /tmp/interopcheck-r26/tools/mutate-and-run.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh && echo IDENTICAL
RUNNER_IDENTICAL_TO_LANE_WORKTREE
```

Lane repo state left untouched by this seat (read-only `git status`, `GIT_OPTIONAL_LOCKS=0`):

```
 M corpus/knowledge/mte-report-interop.md
?? .ufo/evidence/round-26/after/
?? .ufo/waves/round-26/
```

The entries above are other seats' / the L1's work in flight (the tracked-file
list grew to two modified files by the end of the run, as concurrent seats landed
their edits); this seat added only this report file and changed no tracked file.
Re-checked at the end of the run: ` M corpus/knowledge/mte-report-interop.md`,
` M corpus/lessons/round-25.md`, `?? .ufo/evidence/round-26/after/`,
`?? .ufo/waves/round-26/` — no new tracked change from this seat.

Tool versions used: node v24.21.0, uv 0.13.0, Python 3.14.8, jsonschema 4.25.1.
No package was installed to the system: `jsonschema==4.25.1` is fetched into the
uv cache by the prescribed `uv run --no-project --with jsonschema==4.25.1`
incantation (ephemeral environment, no system or global site-packages change).
Nothing was upgraded, and no host service was touched.

---

## 2. `--check` run (the required command, verbatim)

```
cd /tmp/interopcheck-r26 && uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin --emit /tmp/interopcheck-mte
```

Exit status: **0**. Observed output, every `MTE_LEG` line and the verdict:

```
MTE_WORKDIR: /tmp/tameshi-mte-regression-30ei3okp (removed on PASS)
MTE_LEG bash-checklist-run: CONFORMS (schema=ok official_score=46.666666666666664 official_killed=7 official_survived=8 official_invalid=0 recorded=7/15 per_mutant=ok failed=none runner_pct=47 official_rounded_half_up=47)
MTE_LEG bash-mado-verify: CONFORMS (schema=ok official_score=40 official_killed=4 official_survived=6 official_invalid=0 recorded=4/10 per_mutant=ok failed=none runner_pct=40 official_rounded_half_up=40)
MTE_LEG bash-surface-census: CONFORMS (schema=ok official_score=80 official_killed=8 official_survived=2 official_invalid=0 recorded=8/10 per_mutant=ok failed=none runner_pct=80 official_rounded_half_up=80)
MTE_LEG bash-tsukuroi-census: CONFORMS (schema=ok official_score=60 official_killed=6 official_survived=4 official_invalid=0 recorded=6/10 per_mutant=ok failed=none runner_pct=60 official_rounded_half_up=60)
MTE_LEG js-cite-check: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_LEG js-claims-check: CONFORMS (schema=ok official_score=70 official_killed=7 official_survived=3 official_invalid=0 recorded=7/10 per_mutant=ok failed=none runner_pct=70 official_rounded_half_up=70)
MTE_LEG js-kimi-census: CONFORMS (schema=ok official_score=80 official_killed=8 official_survived=2 official_invalid=0 recorded=8/10 per_mutant=ok failed=none runner_pct=80 official_rounded_half_up=80)
MTE_LEG js-round-gate: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_LEG js-sources-check: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_INTEROP: PASS legs_conforming=9/9
```

Nine legs, nine `CONFORMS`, no `FAILS`, no `MTE_INTEROP: SETUP`. The ninth leg
`js-cite-check` reads official score 50, official killed 5, official survived 5,
official invalid 0, recorded 5/10, `per_mutant=ok`, `failed=none`. The runner's
integer percentage and the official score rounded half up agree on every leg.

The `--emit` directory `/tmp/interopcheck-mte` holds nine `*.mte.json` reports,
nine `*.spec` copies, and `official-metrics.json`.

---

## 3. `--selftest` run

```
cd /tmp/interopcheck-r26 && uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest
```

Exit status: **0**, final line `MTE_SELFTEST: 17/17 pass`. All 16 judge cases
plus the emitter-location case pass; each case was expected to fail for its
stated reason, e.g. `CASE tameshi-vocabulary-status PASS (schema=invalid:'KILLED'
is not one of ['Killed', 'Survived', ...] ... failed=ledger,per_mutant,schema,score)`
and `CASE emitter-locations PASS ({'D1': (1, 1, 1, 6), 'D2': (2, 1, 3, 9), 'D3': (3, 5, 3, 9)})`.

---

## 4. `js-cite-check` mutant locations against the pinned file

The pinned target was re-read from the sibling lane's object store, not from a
working tree:

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/interopcheck-cite-check.mjs
$ sha256sum /tmp/interopcheck-cite-check.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/interopcheck-cite-check.mjs
$ wc -l /tmp/interopcheck-cite-check.mjs
2537 /tmp/interopcheck-cite-check.mjs
```

The sha256 equals the pin declared in the runner (`PIN_CITECHECK=4057...c10c9f`,
`REV_CITECHECK=1205c662...`) and in the pre-registered spec header.

Locations were recomputed independently of `mte-interop.py` (own script,
`/tmp/interopcheck-loc.py`, re-deriving the offset of each unique `@old` string
and converting to 1-based line/column with end-exclusive end), then compared with
the emitted report `/tmp/interopcheck-mte/js-cite-check.mte.json`. Every `@old`
occurs exactly once in the pinned bytes (`occurrences=1` for all ten), and the
span `source[start:end] == @old` holds for all ten.

| defect | @old occurrences | expected start | expected end | emitted start | emitted end | status | match |
|---|---|---|---|---|---|---|---|
| K_UNRESOLVED_SEV | 1 | 221:1 | 221:89 | 221:1 | 221:89 | Killed | yes |
| K_PIN_KIND | 1 | 1127:1 | 1127:72 | 1127:1 | 1127:72 | Killed | yes |
| K_FENCE_TILDE | 1 | 471:28 | 471:43 | 471:28 | 471:43 | Killed | yes |
| K_MISSING_WORD | 1 | 2519:81 | 2519:135 | 2519:81 | 2519:135 | Killed | yes |
| K_EMPTY_VERDICT | 1 | 1590:1 | 1590:94 | 1590:1 | 1590:94 | Killed | yes |
| S_OOR_EDGE | 1 | 1312:1 | 1312:46 | 1312:1 | 1312:46 | Survived | yes |
| S_STRICT | 1 | 1589:1 | 1589:70 | 1589:1 | 1589:70 | Survived | yes |
| S_EMPTY_GUARD | 1 | 1590:1 | 1590:94 | 1590:1 | 1590:94 | Survived | yes |
| S_USAGE | 1 | 2512:1 | 2512:15 | 2512:1 | 2512:15 | Survived | yes |
| S_PIN_INCLUDES | 1 | 1195:1 | 1195:47 | 1195:1 | 1195:47 | Survived | yes |

`RESULT all_locations_match=True`.

The pinned source text at each location was printed and confirmed to contain the
`@old` string at exactly that column, e.g. line 471 column 28 is
`` (`{3,}|~{3,})/; `` inside `const FENCE_LINE_RE = /^\s*(`{3,}|~{3,})/;`, and
line 2519 column 81 is `kind = e.code === 'ENOENT' ? 'missing' : 'unreadable';`.

The report's `source` field is byte-identical to the pin:

```
EMIT source file=cite-check.mjs identical_to_pin=True sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
```

(126 478 characters / 126 735 bytes — the file contains multi-byte UTF-8, so the
character count and byte count differ; the sha256 over the UTF-8 encoding is the
pin.)

Note that `K_EMPTY_VERDICT` and `S_EMPTY_GUARD` share the same `@old` line
(1590) but differ in the `@new` replacement; their locations are identical by
construction and their statuses differ (`Killed` vs `Survived`), which is the
expected behaviour for two mutants of the same site.

---

## 5. Independent re-validation of the nine emitted reports

The `--emit` output was re-checked without `mte-interop.py`'s own `judge()`
(own script `/tmp/interopcheck-validate.py`, official schema + official
`mutation-testing-metrics` 3.9.0 library re-run, spec-copy cross-check):

```
LEG bash-checklist-run     schema_errors=0 spec_mismatches=0 official_score=46.666666666666664 official_killed=7 official_survived=8 official_invalid=0 total=15 official_file_agrees=True verdict=PASS
LEG bash-mado-verify       schema_errors=0 spec_mismatches=0 official_score=40 official_killed=4 official_survived=6 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
LEG bash-surface-census    schema_errors=0 spec_mismatches=0 official_score=80 official_killed=8 official_survived=2 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
LEG bash-tsukuroi-census   schema_errors=0 spec_mismatches=0 official_score=60 official_killed=6 official_survived=4 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
LEG js-cite-check          schema_errors=0 spec_mismatches=0 official_score=50 official_killed=5 official_survived=5 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
LEG js-claims-check        schema_errors=0 spec_mismatches=0 official_score=70 official_killed=7 official_survived=3 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
LEG js-kimi-census         schema_errors=0 spec_mismatches=0 official_score=80 official_killed=8 official_survived=2 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
LEG js-round-gate          schema_errors=0 spec_mismatches=0 official_score=50 official_killed=5 official_survived=5 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
LEG js-sources-check       schema_errors=0 spec_mismatches=0 official_score=50 official_killed=5 official_survived=5 official_invalid=0 total=10 official_file_agrees=True verdict=PASS
TOTAL legs=9 fails=0
```

`spec_mismatches` covers three things per mutant: the emitted `description`
equals the spec `@defect` text, the emitted `replacement` equals the spec `@new`
string, and the emitted `status` equals the mapped verdict of the same id in the
runner's committed `TABLE_*` string. All zero mismatches.

---

## 6. Cross-checks against the committed round-26 evidence

- Committed check stdout vs this independent re-run: the `MTE_LEG`/`MTE_INTEROP`
  lines are **identical** (only the temporary workdir path differs):
  `diff <(grep -E '^(MTE_LEG|MTE_INTEROP)' .ufo/evidence/round-26/after/mte-check-a08e85c.stdout) <(grep -E '^(MTE_LEG|MTE_INTEROP)' /tmp/interopcheck-check.log)` → no differences.
- Committed selftest stdout vs this re-run: the `CASE`/`MTE_SELFTEST` lines are
  **identical** (`SELFTEST_IDENTICAL`).
- The emitted `js-cite-check.spec` copy is byte-identical to the pre-registered
  spec `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`
  (`SPEC_IDENTICAL`), so the runner's embedded copy and the evidence copy agree.
- Per-defect verdicts: the committed sweep
  `.ufo/evidence/round-26/cite-check/sweep/results.tsv`, the runner's
  `TABLE_CITECHECK` and the emitted report statuses agree on all ten ids
  (5 KILLED → Killed, 5 SURVIVED → Survived), `ALL_AGREE True`.
- Pre-registered predictions: all 10 predictions in
  `.ufo/evidence/round-26/cite-check/predictions.json` held against the measured
  sweep verdicts (`predictions held 10/10`), matching the declared
  `predicted_kill_rate` 5/10.
- The registry note `corpus/knowledge/mte-report-interop.md:174-180` states that
  round 26 adds the ninth leg and that all nine conform at `a08e85c`; the
  measured run agrees with that claim.

---

## 7. Findings, risks, blockers

**Findings: none.** No defect to correct; the smallest safe correction is "no
change". Nothing in the lane's tracked files was modified by this seat.

Risks / notes for the integrator:

1. `--check` performs a **live** regression: it re-runs all nine legs against the
   sibling lanes under `--fleet-root`. It resolves siblings through symlinks into
   a private staged fleet, so the sibling repos are read but the run reads the
   siblings' *working trees* for anything not pinned by rev, and it depends on
   `node`, `bash`, `git` and the vendored tarballs in `tools/vendor/`. It must be
   run from a clone, never from the lane checkout itself (as done here).
2. The check is sensitive to the *number* of legs: `mte-interop.py` refuses to
   report when the leg set or table set differs from the nine in `LEG_TABLE`
   (`MTE_INTEROP: SETUP (...)`). Adding a tenth leg later requires updating
   `LEG_TABLE` and the runner's table strings in the same change.
3. The `--check` path prints `MTE_WORKDIR` with a random temp path; the
   committed evidence file therefore differs in that one line between runs.
   Harmless, but a byte-diff of two check stdouts will show it.
4. `js-cite-check` has two mutants on the same source line (1590) — legal for
   the schema, but a future reader must not treat the equal locations as a
   duplicate-row bug.
5. The emitted `source` character count (126 478) differs from the file's byte
   count (126 735) because of multi-byte UTF-8; any future check that compares
   `len(source)` to `wc -c` will produce a false mismatch. Compare the sha256.

Blockers: none.

---

## 8. Reproduce

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/interopcheck-r26
git -C /tmp/interopcheck-r26 checkout -q --detach a08e85c5d7f899e8a5992e20517edb1a380d79eb
cd /tmp/interopcheck-r26
uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin --emit /tmp/interopcheck-mte   # exit 0, 9/9
uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest                                                                  # exit 0, 17/17
python3 /tmp/interopcheck-loc.py /tmp/interopcheck-mte/js-cite-check.mte.json                                                                             # all_locations_match=True
```

Report: `.ufo/waves/round-26/w1/InteropCheck.md`
