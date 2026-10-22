# C2LiveCheck — live check of the round-25 C2 MTE-interop counter

Seat: TameshiR25.C2LiveCheck (executor, leaf). Judged on: coverage.
Frozen contract: `.ufo/evidence/round-25/contract.json` (lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df, base 1f7315732e0cfe0ba9dfe0fff2ef36d1c8481bb5).
Mode: private clone at the pinned lane revision; nothing run inside the lane; no git/jj write commands; no production file edited; no installs (see *Tooling*).

## Verdict

1. **The mandated counter passes at the pinned lane revision, twice, with identical output.** `MTE_INTEROP: PASS legs_conforming=8/8`, exit 0, wall 143.252 s (run 1) and 123.296 s (run 2, same stdout). The selftest passes 10/10, exit 0, wall 0.159 s. The C2 target line is met as written.
2. **The coverage behind "8/8" is complete against the recorded ledger, and I re-verified it out-of-tool.** 8 legs = the 8 recorded mutation-case notes (`corpus/knowledge/mutation-case-*.md`); 85 mutants = the 85 recorded defects (15 + 7×10); every emitted report's `source` is byte-identical to the pinned blob materialised from the sibling repo's own git object store (sha256 == the runner's `PIN_*` for all 8 legs); every mutant's line/column resolves to a non-empty source segment distinct from its replacement; my own jsonschema validation and my own invocation of the vendored official metrics library reproduce the tool's numbers exactly.
3. **At the pinned revision c9ff09f the judge cannot see a swapped verdict.** A doctored leg whose per-defect verdicts are exchanged in pairs (K_KIND↔S_KIND, counts unchanged) is reported `CONFORMS`, `MTE_INTEROP: PASS legs_conforming=1/1`, exit 0. The `score` check is a tautology there (it compares the tool's own 1:1 status mapping against the official library's count of the same statuses) and the `ledger` check only compares counts. The lane's **working tree** already carries a stricter tool (sha256 8c24255c…, uncommitted) that adds a `per_mutant` check against the runner's committed per-defect `TABLE_*` verdicts; on the same doctored leg it prints `FAILS … failed=per_mutant` and exits 1, its selftest is 16/16, and on the live fleet it reports `PASS legs_conforming=8/8` with `per_mutant=ok` on every leg (exit 0, 116.346 s). The C2 claim as worded ("killed/valid counts equal the recorded ledger table") is satisfied at c9ff09f; the stronger per-defect identity is satisfied only by the uncommitted tree version.
4. **The counter's denominator is discovery-based, not ledger-pinned.** A one-leg workdir yields `MTE_INTEROP: PASS legs_conforming=1/1`, exit 0. In the live path this is not exploitable, because the runner exits non-zero when any leg is out of band or cannot be set up, and the tool then reports `MTE_INTEROP: SETUP (regression exit 2)`, exit 2 (observed, 0.108 s, with a fleet root that has no sibling repos). The exposure is the `--workdir` replay path, where a truncated workdir reports a smaller N/M and still passes.
5. **The claim's "before" state is confirmed by the file system, not only by the receipt.** `git cat-file -e 1f73157:tools/mte-interop.py` → "exists on disk, but not in 1f73157…", matching `c2-before.json` (exit 2, "No such file or directory").

Net: **C2 is satisfied at the pinned revision as written** (8/8, exit 0, independently re-verified). Two coverage notes belong in the after-record: the pinned-revision judge has no per-defect identity check, and the tool digest that any receipt names must be the tree version actually run (the lane's tree is at 8c24255c…, the contract's frozen pin 58a5ae92… and amendment-1's 311448d9… are both earlier bytes).

## Evidence

### 1. Clone and revisions (read-only)

```
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/C2LiveCheck-r25
$ git -C /tmp/C2LiveCheck-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
$ git -C /tmp/C2LiveCheck-r25 log --oneline -1
c9ff09f round-25: mte-interop --fleet-root stages sibling lanes so clones can run the C2 counter
$ sha256sum tools/mte-interop.py tools/vendor/*.tgz
311448d92c10891e2fd9513586c203d4d245f94559ab7843de48bef4de1db422  tools/mte-interop.py
ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548  tools/vendor/mutation-testing-metrics-3.9.0.tgz
adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280  tools/vendor/mutation-testing-report-schema-3.9.0.tgz
```

The two vendor digests equal the contract's `vendor_sha256` exactly. The tool digest is the post-amendment value already recorded in `contract-amendment-1.json` (`tool_sha256_now: 311448d9…`); the contract's frozen `tool_sha256: 58a5ae92…` is the bytes of the freeze commit 2a97ec1 (verified: `git show 2a97ec1:tools/mte-interop.py | sha256sum` → 58a5ae92…).

### 2. Mandated selftest — `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest`

Exit **0**, wall **0.159 s**. Verbatim:

```
CASE conforming PASS (schema=ok official_score=66.66666666666666 tameshi_score=66.66666666666667 official_killed=2 recorded_killed=2 official_valid=3 recorded_defects=3)
CASE tameshi-vocabulary-status PASS (schema=invalid:'KILLED' is not one of ['Killed', 'Survived', 'NoCoverage', 'CompileError', 'RuntimeError', 'Timeout', 'Ignored', 'Pendi official_score=50 tameshi_score=66.66666666666667 official_killed=1 recorded_killed=2 official_valid=2 recorded_defects=3)
CASE line-zero-location PASS (schema=invalid:0 is less than the minimum of 1|0 is less than the minimum of 1 official_score=66.66666666666666 tameshi_score=66.66666666666667 official_killed=2 recorded_killed=2 official_valid=3 recorded_defects=3)
CASE missing-thresholds PASS (schema=invalid:'thresholds' is a required property official_score=66.66666666666666 tameshi_score=66.66666666666667 official_killed=2 recorded_killed=2 official_valid=3 recorded_defects=3)
CASE bad-schema-version PASS (schema=invalid:'3' does not match '^([1-2])(\\.(([1-9]\\d*)|0)){0,2}$' official_score=66.66666666666666 tameshi_score=66.66666666666667 official_killed=2 recorded_killed=2 official_valid=3 recorded_defects=3)
CASE status-flipped-vs-verdict PASS (schema=ok official_score=33.33333333333333 tameshi_score=66.66666666666667 official_killed=1 recorded_killed=2 official_valid=3 recorded_defects=3)
CASE inconclusive-leaves-denominator PASS (schema=ok official_score=50 tameshi_score=50.0 official_killed=1 recorded_killed=1 official_valid=2 recorded_defects=3)
CASE timeout-is-not-a-tameshi-kill PASS (schema=ok official_score=66.66666666666666 tameshi_score=33.333333333333336 official_killed=1 recorded_killed=1 official_valid=3 recorded_defects=3)
CASE ledger-count-mismatch PASS (schema=ok official_score=66.66666666666666 tameshi_score=66.66666666666667 official_killed=2 recorded_killed=3 official_valid=3 recorded_defects=3)
CASE no-ledger-row PASS (schema=ok official_score=66.66666666666666 tameshi_score=66.66666666666667 official_killed=2 recorded_killed=None official_valid=3 recorded_defects=None)
MTE_SELFTEST: 10/10 pass
```

### 3. Mandated check — `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin --emit /tmp/C2LiveCheck-mte`

Exit **0**, wall **143.252 s** (run 1). Verbatim:

```
MTE_LEG bash-checklist-run: CONFORMS (schema=ok official_score=46.666666666666664 tameshi_score=46.666666666666664 official_killed=7 recorded_killed=7 official_valid=15 recorded_defects=15)
MTE_LEG bash-mado-verify: CONFORMS (schema=ok official_score=40 tameshi_score=40.0 official_killed=4 recorded_killed=4 official_valid=10 recorded_defects=10)
MTE_LEG bash-surface-census: CONFORMS (schema=ok official_score=80 tameshi_score=80.0 official_killed=8 recorded_killed=8 official_valid=10 recorded_defects=10)
MTE_LEG bash-tsukuroi-census: CONFORMS (schema=ok official_score=60 tameshi_score=60.0 official_killed=6 recorded_killed=6 official_valid=10 recorded_defects=10)
MTE_LEG js-claims-check: CONFORMS (schema=ok official_score=70 tameshi_score=70.0 official_killed=7 recorded_killed=7 official_valid=10 recorded_defects=10)
MTE_LEG js-kimi-census: CONFORMS (schema=ok official_score=80 tameshi_score=80.0 official_killed=8 recorded_killed=8 official_valid=10 recorded_defects=10)
MTE_LEG js-round-gate: CONFORMS (schema=ok official_score=50 tameshi_score=50.0 official_killed=5 recorded_killed=5 official_valid=10 recorded_defects=10)
MTE_LEG js-sources-check: CONFORMS (schema=ok official_score=50 tameshi_score=50.0 official_killed=5 recorded_killed=5 official_valid=10 recorded_defects=10)
MTE_INTEROP: PASS legs_conforming=8/8
```

Second live run (same command, `--emit /tmp/C2LiveCheck-mte-run2`): identical eight MTE_LEG lines and the same `MTE_INTEROP: PASS legs_conforming=8/8`, exit **0**, wall **123.296 s**. The two runs are independent (fresh regression workdir each time, live mutant execution in the four sibling repos' pinned bytes).

Emitted artifacts: `/tmp/C2LiveCheck-mte/{bash-checklist-run,bash-mado-verify,bash-surface-census,bash-tsukuroi-census,js-claims-check,js-kimi-census,js-round-gate,js-sources-check}.mte.json` plus `official-metrics.json`.

### 4. Independent re-verification (out-of-tool)

`/tmp/C2LiveCheck-verify.py` (my own script; it never calls `mte-interop.py`): it re-validates each emitted report against the vendored official schema with the `jsonschema` package, re-computes the official metrics by invoking the vendored `mutation-testing-metrics` 3.9.0 library with my own node runner, re-derives each leg's verdict counts from `statusReason`, re-resolves every mutant's line/column back into the report's own `source`, and re-materialises each leg's pinned target from the sibling repo's git object store to compare bytes. Exit 0, output verbatim:

```
VERIFY legs_in_emit=8
VERIFY_LEG bash-checklist-run schema=ok official_score=46.666666666666664 tool_score=46.666666666666664 metrics_match=True mutants=15 verdicts={'SURVIVED': 8, 'KILLED': 7} tameshi_score=46.666666666666664 source_sha==pin:True loc_ok=True
VERIFY_LEG bash-mado-verify schema=ok official_score=40 tool_score=40 metrics_match=True mutants=10 verdicts={'KILLED': 4, 'SURVIVED': 6} tameshi_score=40.0 source_sha==pin:True loc_ok=True
VERIFY_LEG bash-surface-census schema=ok official_score=80 tool_score=80 metrics_match=True mutants=10 verdicts={'KILLED': 8, 'SURVIVED': 2} tameshi_score=80.0 source_sha==pin:True loc_ok=True
VERIFY_LEG bash-tsukuroi-census schema=ok official_score=60 tool_score=60 metrics_match=True mutants=10 verdicts={'KILLED': 6, 'SURVIVED': 4} tameshi_score=60.0 source_sha==pin:True loc_ok=True
VERIFY_LEG js-claims-check schema=ok official_score=70 tool_score=70 metrics_match=True mutants=10 verdicts={'KILLED': 7, 'SURVIVED': 3} tameshi_score=70.0 source_sha==pin:True loc_ok=True
VERIFY_LEG js-kimi-census schema=ok official_score=80 tool_score=80 metrics_match=True mutants=10 verdicts={'KILLED': 8, 'SURVIVED': 2} tameshi_score=80.0 source_sha==pin:True loc_ok=True
VERIFY_LEG js-round-gate schema=ok official_score=50 tool_score=50 metrics_match=True mutants=10 verdicts={'KILLED': 5, 'SURVIVED': 5} tameshi_score=50.0 source_sha==pin:True loc_ok=True
VERIFY_LEG js-sources-check schema=ok official_score=50 tool_score=50 metrics_match=True mutants=10 verdicts={'KILLED': 5, 'SURVIVED': 5} tameshi_score=50.0 source_sha==pin:True loc_ok=True
VERIFY total_mutants=85
VERIFY legs_in_runner=8
```

What that establishes, beyond the tool's own printout:

- **Ledger completeness.** The runner carries exactly 8 embedded per-defect verdict tables (`tools/mutate-and-run.sh` `TABLE_JS/BASH/TSUKUROI/MADO/CHECKLIST/CLAIMS/ROUNDGATE/SOURCESCHECK`) totalling 85 defects (15 + 7×10). The 8 emitted reports carry 85 mutants (15 + 7×10) — no defect dropped, no extra mutant. The fleet's recorded corpus agrees: `corpus/knowledge/mutation-case-*.md` is exactly 8 notes, one per leg.
- **Recorded expectations equal the measured ones.** Recomputed from the runner's committed `TABLE_*` strings: kimi-census 8/10, surface-census 8/10, tsukuroi-census 6/10, mado-verify 4/10, checklist-run 7/15, claims-check 7/10, round-gate 5/10, sources-check 5/10 — identical to the `recorded-killed` values the tool printed and to the live `REGRESSION_TABLE` lines. Aggregate 50 killed of 85 valid = 58.82 %; the eight per-leg official scores (40–80 %) are the same numbers.
- **Source bytes are the pinned bytes.** For all 8 legs, `sha256(report.files[<name>].source)` equals the runner's `PIN_*`, and `git -C <sibling> show <REV>:<path> | sha256sum` equals the same value. The emitted report therefore describes the recorded revision's bytes, not the sibling repo's current working tree (the sibling repos have uncommitted modifications in their own lanes; the legs are byte-pinned replays).
- **Locations are real.** Every mutant's `location.start/end` re-resolves, in the report's own `source`, to a non-empty segment different from the mutant's `replacement` — i.e. the report's coordinates point at code that exists and would actually change.
- **The official score formula matches tameshi's denominator.** In the vendored library (`mutation-testing-metrics` 3.9.0, `dist/src/calculateMetrics.js`, `toMetrics`): `totalDetected = timeout + killed`, `totalUndetected = survived + noCoverage`, `totalValid = totalUndetected + totalDetected`, `totalInvalid = runtimeErrors + compileErrors`, `mutationScore = totalDetected / totalValid × 100`. The tool's `INCONCLUSIVE → RuntimeError` mapping is what keeps the official denominator equal to tameshi's `killed + survived`; a `Timeout` would inflate the official score. This is the same conclusion the lane already reached in `corpus/knowledge/mutation-score-semantics.md` (F1, round 1).

### 5. Failure paths (falsifiable, observed)

- **No fleet root → fail closed.** In the clone (whose parent is `/tmp`, so no sibling repos) the check prints `MTE_INTEROP: SETUP (regression exit 2)`, exit **2**, wall 0.108 s. The same shape the amendment recorded at the freeze revision.
- **Empty workdir → fail closed.** `--check --workdir <empty dir>` prints `MTE_INTEROP: SETUP (no leg results under /tmp/C2LiveCheck-nofleet)`, exit **2**.
- **Truncated workdir → passes with a smaller denominator (the one real gap).** A workdir holding a single well-formed leg yields `MTE_LEG js-sources-check: CONFORMS …` and `MTE_INTEROP: PASS legs_conforming=1/1`, exit **0**. The tool's denominator is `len(legs)` — the legs it discovered — not the ledger's 8. In the live path the runner's non-zero exit prevents this (see the SETUP case above), so the gap is confined to the `--workdir` replay path.
- **A swapped verdict is invisible to the pinned judge.** Doctored leg: `js-sources-check` with `K_KIND` and `S_KIND` verdicts exchanged in `results.tsv` (counts unchanged: 5 killed / 5 survived; the fabricated `REGRESSION_TABLE` line is byte-identical to the honest one apart from a `flips=0` field the pinned tool does not read).
  - pinned tool c9ff09f: `MTE_LEG js-sources-check: CONFORMS (schema=ok official_score=50 tameshi_score=50.0 official_killed=5 recorded_killed=5 official_valid=10 recorded_defects=10)` and `MTE_INTEROP: PASS legs_conforming=1/1`, exit **0**.
  - lane working-tree tool (8c24255c…, uncommitted): `MTE_LEG js-sources-check: FAILS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=mismatch failed=per_mutant runner_pct=unavailable)` and `MTE_INTEROP: FAIL legs_conforming=0/1`, exit **1**.
  The pinned `score` check is a tautology (it compares the tool's own 1:1 status mapping with the official library's tally of those same statuses) and the pinned `ledger` check compares counts only; the tree version adds `per_mutant` (statuses vs the runner's committed per-defect table) and also reads the runner's `flips=` field.

### 6. The lane's working tree differs from the pinned revision

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain` lists `M tools/mte-interop.py`; the live file's sha256 is `8c24255c9e482751772e958e5ba9a615891ca7e5dfc9426d2fb5667ceae65552`, i.e. neither the contract's frozen `58a5ae92…` nor the committed `311448d9…`. The tree version adds the `per_mutant` check, the runner's `flips` field, a `runner_pct` vs official-rounded-half-up print, `spec.copy` copies in `--emit`, and six more selftest cases. I copied that file read-only into a second scratch clone (`/tmp/C2LiveCheck-live-r25`, base c9ff09f + the tree's tool) and ran it there: selftest `MTE_SELFTEST: 16/16 pass`, exit **0**, wall 0.095 s. Its live `--check --fleet-root /home/vgpnk/Projects/shokunin` result is in the section below.

### 7. Fleet and lane state left untouched

The runner materialises every leg with `git show` / `git ls-tree` / `git cat-file` inside the four sibling repos and writes mutants only under its own workdir (`tools/mutate-and-run.sh`, `regression_case_git` / `regression_case`); no sibling working tree is written. All my runs wrote to `/tmp` only. No git/jj write command was issued in the lane; the only lane writes in this seat are this report file.

## Live check against the lane's working-tree tool (read-only copy, scratch clone)

Command (run in `/tmp/C2LiveCheck-live-r25`, i.e. the pinned clone with the lane tree's `tools/mte-interop.py` copied in; nothing run inside the lane):

```
$ uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check \
      --fleet-root /home/vgpnk/Projects/shokunin --emit /tmp/C2LiveCheck-mte-live
```

Exit **0**, wall **116.346 s**. Verbatim:

```
MTE_LEG bash-checklist-run: CONFORMS (schema=ok official_score=46.666666666666664 official_killed=7 official_survived=8 official_invalid=0 recorded=7/15 per_mutant=ok failed=none runner_pct=47 official_rounded_half_up=47)
MTE_LEG bash-mado-verify: CONFORMS (schema=ok official_score=40 official_killed=4 official_survived=6 official_invalid=0 recorded=4/10 per_mutant=ok failed=none runner_pct=40 official_rounded_half_up=40)
MTE_LEG bash-surface-census: CONFORMS (schema=ok official_score=80 official_killed=8 official_survived=2 official_invalid=0 recorded=8/10 per_mutant=ok failed=none runner_pct=80 official_rounded_half_up=80)
MTE_LEG bash-tsukuroi-census: CONFORMS (schema=ok official_score=60 official_killed=6 official_survived=4 official_invalid=0 recorded=6/10 per_mutant=ok failed=none runner_pct=60 official_rounded_half_up=60)
MTE_LEG js-claims-check: CONFORMS (schema=ok official_score=70 official_killed=7 official_survived=3 official_invalid=0 recorded=7/10 per_mutant=ok failed=none runner_pct=70 official_rounded_half_up=70)
MTE_LEG js-kimi-census: CONFORMS (schema=ok official_score=80 official_killed=8 official_survived=2 official_invalid=0 recorded=8/10 per_mutant=ok failed=none runner_pct=80 official_rounded_half_up=80)
MTE_LEG js-round-gate: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_LEG js-sources-check: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
MTE_INTEROP: PASS legs_conforming=8/8
```

`per_mutant=ok` on all 8 legs means the tree version's fourth check — every one of the 85 emitted mutant statuses equals the mapped verdict of the same defect id in the runner's committed per-defect `TABLE_*` — holds leg by leg, not only in aggregate. The `runner_pct` column is the runner's own integer kill rate next to the official score rounded half up; they agree on all 8 legs (7/15 → 47 %, 4/10 → 40 %, 8/10 → 80 %, 6/10 → 60 %, 7/10 → 70 %, 8/10 → 80 %, 5/10 → 50 %, 5/10 → 50 %).

Emitted artifacts: 8 `.mte.json` reports + 8 `.spec` copies (the tree version also copies each leg's `spec.copy`) + `official-metrics.json` (17 files).

## Coverage assessment (what the 8/8 does and does not cover)

**Covered by the live check**
- All 8 recorded ledger legs, 85 of 85 recorded defects, each executed live against its pinned target bytes in 4 sibling repos.
- Official schema validation of 8 emitted reports (vendored 3.9.0, draft-07, required `schemaVersion`/`thresholds`/`files`).
- Official score recomputation for all 8 legs by the vendored official metrics library, matching tameshi's kill rate exactly.
- Per-leg agreement between the runner's recorded table, the runner's measured table, and the official library's counts.
- Two independent live runs, identical results, plus a 10/10 (pinned) / 16/16 (tree) negative-control selftest that can fail.
- With the lane's working-tree tool, per-defect identity on all 85 mutants (`per_mutant=ok` on all 8 legs, live) and the runner's integer kill rate against the official score rounded half up (agree on all 8 legs).

**Not covered by the live data (only by the selftest)**
- `INCONCLUSIVE → RuntimeError`: no leg produced an inconclusive verdict (all 8 tables: 0 inconclusive), so the mapping is exercised only by the selftest (`inconclusive-leaves-denominator` at c9ff09f; `emitter-inconclusive-to-runtimeerror` in the tree version, which drives the real `leg_report()`).
- `Timeout` and `NoCoverage` statuses: unreachable from tameshi's three verdicts; the official library would score them differently (`Timeout` counts as detected). Selftest-only.
- Multi-file reports, `testFiles`, `projectRoot`, `framework.version`: absent from the emitted reports and not exercised; the tool's own docstring states it does not validate HTML report elements.

**Not covered by the counter**
- The 8/8 denominator is not pinned to the ledger (§5, truncated workdir).
- At c9ff09f, per-defect verdict identity is not checked (§5, balanced flip).
- The HTML/mutation-testing-reporting consumer of these reports is out of scope by the tool's own documentation; F1 is claimed as report-format + score-semantics interop only.

## Risks and blockers

1. **Receipt pinning.** Any C2 after-receipt should name the tool digest that was actually run. The lane's tree is at `8c24255c…`, which no existing contract document pins (contract `58a5ae92…`, amendment-1 `311448d9…`). If the tree version is the one integrated, a second amendment (or a commit) is needed so the receipt's `tool_sha256` matches the bytes that produced the 8/8.
2. **Denominator.** If the L1 wants the counter to be self-pinning, the smallest safe correction is to compare the discovered leg set against the runner's own 8-leg list and fail when a leg is missing (one added check in `check()`; the live path already fails closed, so this only hardens the `--workdir` path). I did not make this change: it is a production-file edit outside this seat's write scope.
3. **Live-fleet race.** Two concurrent live runs of the same counter by different seats were visible in `/tmp` during my run; the fleet's sibling repos are shared and their working trees carry other lanes' uncommitted work. The legs are byte-pinned replays (`git show` at recorded revisions), so this does not affect the verdict, but receipts should not be read as "the sibling repos were clean at the time".
4. **Blockers: none.** The mandated commands ran to completion in the private clone, both exits and every MTE_LEG/CASE line are above, and the wall times are recorded.

## Tooling

- Installed or updated: **nothing**. No pacman transaction, no `uv tool install`, no release binary was fetched. `jsonschema==4.25.1` was resolved ephemerally by `uv run --no-project --with` (uv 0.13.0) into the uv cache; `node` v24.21.0 and `python3` 3.14.8 were already present and were used as-is. (Pacman transactions are paused host-wide; the uv/`--with` channel was sufficient and no strict upgrade was needed.)
- Hosts touched: none. No service restarted.

## Files

- Written: `.ufo/waves/round-25/w1/C2LiveCheck.md` (this report) — the only file this seat created.
- Scratch (outside the repo, disposable): `/tmp/C2LiveCheck-r25` (clone at c9ff09f), `/tmp/C2LiveCheck-live-r25` (clone at c9ff09f + the tree's tool), `/tmp/C2LiveCheck-verify.py` (my independent verifier), `/tmp/C2LiveCheck-mte*` (emitted reports), `/tmp/C2LiveCheck-subset`, `/tmp/C2LiveCheck-balanced` (doctored workdirs), `/tmp/C2LiveCheck-nofleet`.
