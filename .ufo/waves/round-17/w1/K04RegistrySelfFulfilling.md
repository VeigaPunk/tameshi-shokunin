# K04 — Is contract B / C2 self-fulfilling? (critic, round 17 wave 1)

Scope: contract B (`tools/registry.json` and `tools/registry-check.py`) and C2's
counting command `registry-check.py --rev REV --registry <after> --json`.
I also checked contract A's v2 manifest, because C2's single repaired row
depends on it.

Method: I made a fleet-mirror clone at `98bea7da…` in
`/tmp/tameshi-r17w1-K04RegistrySelfFulfilling-5Q3SIL`. In it I ran 24
registered commands, taking each argv and each expected outcome from
**committed source cells**, not from any author's registry. I ran them twice:
once on the pristine tip, and once with this wave's staged
`tools/mutate-and-run.sh` and `tools/pin-disposition.py` overlaid.

`tools/registry.json` did not exist yet, so for that file I can only state
rules. I could not inspect its actual rows. `tools/registry-check.py` was being
edited while I worked (one copy failed with `IndentationError` at :331). I ran a
parseable snapshot with sha256 `60b0f503…7b51`.

No tool installs.

## 1. Independent baseline (my own derivation, not the lane's registry)

Each expected value below is quoted from the source line, at `98bea7d`.

| Row (source) | argv | expect (source) | got @98bea7d | got +staged |
|---|---|---|---|---|
| r12 selftest (SKILL:1503) | `repeat-control.py --selftest` | 0 | 0 `SELFTEST: PASS (29 cases)` | 0 |
| r12 snapshot (SKILL:1503; fill: ControlGate) | `--snapshot .ufo/evidence/round-12/ControlGate` | 0 | 0 | 0 |
| r12 snapshot mismatch (fill) | `--snapshot …/ControlGate/mismatch` | 1 | 1 | 1 |
| r12 witness count / selftest (SKILL:1504) | `bash-witness-study.py count` / `selftest` | 0 / 0 | 0 / 0 | 0 / 0 |
| r13 pin-disposition live / selftest (SKILL:1552) | `--manifest …/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 / 0 | 0 / 0 (18/18) | 0 / 0 |
| r13 witness-metadata check / selftest (SKILL:1553) | `--check --companion …` | 0 / 0 | 0 / 0 (39/39) | 0 / 0 |
| r15 context check / missing-env / selftest (SKILL:1680) | `--check`; `--receipt …/context-missing-env/receipt.json --expected …` | 0 / 1 + `missing_injected_environment` / 0 | 0 / 1 ✓ / 0 (49/49) | same |
| **r15 disposition (SKILL:1681, as first committed)** | `evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | **0** | **2 `expected_input_digest_mismatch`** | **2** |
| **r14 recipe step 2 (SKILL:1581-1583)** | same, `dispositions-before.json` | **1, and the producer_before assertion must fail; "a matching exit1 is insufficient"** | **2 `expected_input_digest_mismatch`** | **2** |
| r14/15 disposition selftest | `--selftest` | 0 | 0 (34/34) | 0 |
| **runner selftest (SCORECARD:241)** | `mutate-and-run.sh --selftest` | 0 + `MUTATE_SELFTEST: 80/80 pass` | 0, but prints `83/83` (**marker differs**) | 0, but prints `88/88` |
| **regression (SCORECARD:242; SKILL:1810)** | `--regression` | 0 + `REGRESSION: PASS (cases=6 passed=6` | 0, but prints `cases=7 passed=7` (**marker differs**), 120 s | 0, cases=7, 116 s |
| r16 measure selftest / `--rev 98bea7d` (SKILL:1811) | | 0 / 0 | 0 / 0 | 0 / 0 |
| r16 assemble / reattribute selftests (SKILL:1812-1813) | | 0 / 0 | 0 / 0 | 0 / 0 |
| sources census v2 (SCORECARD:240) | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | 0 + `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` | 0 ✓ | 0 ✓ |
| r15 verify (SCORECARD:247) | `.ufo/evidence/round-15/verify.py --rev 7650fe4…` | 0 | 0 | 0 |

Result: **held 20/24 at `98bea7d`, and 20/24 with the staged tools overlaid.**
No pre-existing row changed outcome when the staged tools were overlaid. In
other words, the staged runner and pin-disposition changes do no harm to these
rows. The four rows that differ are the honest red-before:
- r15 disposition: expected 0, got 2.
- r14 recipe step 2: expected 1, got 2.
- Runner selftest: SCORECARD literal `80/80`.
- Regression: SCORECARD literal `cases=6`.

The two disposition commands use v1, which contract A keeps byte-identical,
and they read immutable round-14 manifests. **They therefore stay at exit 2 at
any after-rev.** C2 can reach N/N only by dropping these rows, re-pointing
their argv, or changing their expect.

## 2. Counterexamples (demonstrated)

### O1 — Demoting a row removes it from the count (registry-check.py:207-208, :318)

A row with any non-`active` status string is "validated but skipped". It is
counted in **neither** the numerator nor the denominator, and the trailer does
not show the skipped count.

I ran a two-row registry with the context gate and the r15 disposition row, at
the `98bea7d` clone:

| Registry variant | Output | Exit |
|---|---|---|
| A honest (r14 row active, expect 0) | `ROW r14 expect=0 got=2 differs` · `REGISTRY_CHECK: held=1/2` | 1 |
| B demoted (`status: "superseded"`) | `ROW r14 status=superseded skipped` · `REGISTRY_CHECK: held=1/1` | **0** |
| C weakened (expect 2) | `ROW r14 expect=2 got=2 held` · `held=2/2` | **0** |
| D weakened with a needle (`expected_input_digest_mismatch`) | `held=2/2` | **0** |

Contract B says `status: "active"`. The tool nonetheless accepts any non-empty
string (`:171`).

**Axes: operability and calibration.** The tool cannot tell a repair from an
excision.

### O2 — Precedent for in-place weakening

Commit `05a2247` (round-16 wave 2) rewrote the **round-15 registry row in
place**. It added "(since round 16 the runner input moved, so `--root .` returns
2 … by design; use `--root` on `git archive 28aeef4`…)". Compare
`git show 05a2247 -- SKILL.md` diff lines 64-65.

The verdict-map cell still says "0 clean". If X04 follows "use the registered
verdict maps", the cell's own text now licenses expect=2. That is variant C
above, and it is self-fulfilling. The non-author spot-check already rejected
this "by design" reading (spot-check §3, "By design holds for the gate's
fail-closed behaviour, not for leaving it un-repinned").

### O3 — Before-reds are inflated by rows whose files are missing

Grading `98bea7d` against the after registry makes every new row red, but the
cause is a missing file, not the defect being repaired:
- `evidence-disposition.py … round-17/dispositions.json` gives 2 `dispositions_missing`.
- `tools/registry-check.py --selftest` gives 2 (no such file).
- `.ufo/evidence/round-17/measure.py --selftest` gives 2.

A before→after delta over the whole registry therefore counts every
instrument this round adds as an operability repair. The only genuine red→green
is the disposition row. Its genuine before-red is `expected_input_digest_mismatch`
on the **original** argv, and the registry is set to replace that argv.

### O4 — An exit-only before row repeats the round-14 anti-pattern

SKILL:1581-1583 requires the before command to fail the producer_before
assertion, and says "a matching exit1 is insufficient". The contract-B row for
`round-17/dispositions-before.json` is planned as expect 1, with
`stdout_contains` only "where the registry names a literal marker" (X04 brief).

I ran the round-14 pair at a `git archive 28aeef4` root. Several obvious needles
appear in both outcomes, so they cannot discriminate:

| Needle | before (exit 1) | after (exit 0) |
|---|---|---|
| `producer_before` | 6 | 6 |
| `expected_contains_missing` | 2 | 1 |
| `"expectation": "producer_before"` | **1** | **0** |
| `"failed": 1` / `"status": "failed"` | **1 / 1** | **0 / 0** |
| `"status": "clean"` / `"effective": 11` / `"superseded": 1` | 0 / 0 / 0 | **1 / 1 / 1** |

SCORECARD:246 already names these discriminators as literals: "before
FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded". So they
are admissible needles.

### O5 — The v2 manifest's `historical_inputs` is wider than the drift and cites a false reason

`.ufo/evidence/round-17/dispositions.json` (X02, written this wave) makes
**all four** `tools/` inputs historical at `4acc607…`.

At `98bea7d`, only `tools/mutate-and-run.sh` differs from its pin (live
`0673d2e5…` vs pin `75ed934d…`). The other three match their pins live:
`pin-disposition.py 29725397…`, `witness-metadata.py df339068…`,
`bash-witness-study.py 49e9e5e2…`.

A key read from a fixed rev's blob passes as long as history exists. **Each
historicalized key is therefore a permanent removal of a live check**, so this
row holds no matter what happens to those tools later.

- `pin-disposition.py` has a staged change (X06), so its inclusion is
  forward-justified, but the reason must say "staged", not "landed later".
- `witness-metadata.py` and `bash-witness-study.py` have no staged change.

The `mutate-and-run.sh` reason is false provenance. It says the file "drifted
after the round-16 jj repo-identity guard fix". The actual drift is:
- `c699c8c` (case 7, `75ed934d…` → `89722ddb…`)
- `05a2247` (leg-count check, → `0673d2e5…`)

`git show 98bea7d:tools/mutate-and-run.sh | grep -c repo_identity` returns `0`.
The guard exists only as the staged round-17 copy. The `pin-disposition.py`
reason "branch-tip resolution repair landed later" is likewise unlanded: it is
staged only.

**Axes: calibration** (false provenance) **and operability** (the gate is
silently weakened).

### O6 — The registry's provenance cannot be re-derived

- **`source` is free text and never checked.** `registry-check.py` validates
  only that it is non-empty.
- **`--registry PATH` takes any file.** The JSON report records the path, not
  the sha256 and not the commit. "held=N/M" can therefore be produced from an
  uncommitted or later-edited registry.
- **Placeholder fills are the author's choice.** Examples: `DIR`/`COMMAND` for
  repeat-control, `REV` for measure, `FILE` for context.
- **Some rows depend on state outside the lane, not on REV:**
  - pin-disposition reads the live fleet: `--root /home/vgpnk/Projects/shokunin`
    is absolute, so the clone is irrelevant.
  - The regression replays legs through symlinked siblings.
  - pin-disposition's verdict map is "0 observations, including
    changed/unavailable", so it holds whatever the siblings do. It cannot
    discriminate.

## 3. Required provenance rules (smallest safe corrections)

**P1. Every pre-existing row is bound to its source line.**
- `source` must be `<file>@<40-hex rev ≤ 98bea7d>:<line>`.
- `argv` joined by spaces must appear verbatim in that line's backticked
  command, after placeholder substitution.
- Each fill goes in `fills: {PLACEHOLDER: value, "why": <source line>}`.
- `expect.exit` is the class the cell names clean, or the outcome that line or
  its recipe states ("→ exit 0", "must fail").
- In-place amended text such as the `05a2247` "by design" clause is **not** an
  admissible source for `expect`.
- A non-author re-derives a row with `git show 98bea7d:SKILL.md | sed -n '<line>p'`.

**P2. Completeness is checked against an independent enumeration.**
- Pre-existing rows must equal S01's enumeration plus the r14 recipe steps 2-3.
  S01's enumeration covers the r12/13/15/16 registry tables and SCORECARD:240-247.
  My 24-row list in §1 is a lower bound.
- A row may stop being active only as `status: "superseded"` with:
  - `superseded_by: <active row name>`;
  - `superseded_at: SKILL.md@<after rev>:<line>`, an **appended** registry line
    that names the replacement;
  - the row still **executed**, with its `got` reported.
- Fix in registry-check: an enum `{active, superseded}`, a check that
  `superseded_by` exists, and a trailer `REGISTRY_CHECK: held=N/M superseded=K (got: …)`.

**P3. `expect` and needles are never edited in place.**
- A changed `expect` or `stdout_contains` must cite an appended, dated
  correction that was committed before the run.
- Admissible example: SKILL:1740's "seven since round 16" supports
  `REGRESSION: PASS (cases=7 passed=7`.
- `MUTATE_SELFTEST: 80/80 pass` has no such correction. The staged runner prints
  88/88. The fix is either a SCORECARD appended correction, or a recorded
  `differs`. Silently dropping the count is not allowed.

**P4. C2 counts only the pre-existing partition, at both revs.**
- Report `pre-existing held@before / held@after` over **identical argv**,
  separately from new rows.
- A new row's before result is `absent`, not red, when its failure is a missing
  file (`dispositions_missing`, ENOENT).
- A red-before claim is valid only where before and after run the same argv, or
  where the superseding row's before-failure id equals the defect
  (`expected_input_digest_mismatch`).
- The honest before figure is **pre-existing 20/24 (or 20/22 excluding the two
  SCORECARD-marker rows)**.

**P5. Rows that expect a nonzero exit or emit JSON carry discriminating needles.**
- The needle must be shown absent in the opposite outcome. Use the §2-O4 table:
  - before row: `"expectation": "producer_before"` and `"status": "failed"`;
  - after row: `"status": "clean"`, `"effective": 11`, and `"superseded": 1`.
- Context missing-env keeps `missing_injected_environment`.

**P6. The registry is pinned.**
- C2 grades the registry read from the **committed** after rev:
  `git show AFTER:tools/registry.json > tmp`.
- registry-check's JSON must print `registry_sha256` and the resolved 40-hex
  rev. Without these, a non-author cannot tell which registry produced "held=N/M".

**P7. Rows that depend on outside state are flagged.**
- Mark them `external: true`: pin-disposition live, regression, and any row
  whose argv names an absolute path outside the clone.
- Report them separately from the C2 delta, because their outcome is not a
  function of REV.
- Mark rows whose verdict map cannot fail (pin-disposition live)
  `discriminating: false`.

**P8. The v2 `historical_inputs` set is minimal and its reasons are true.**
- Each key must be either:
  - live-digest ≠ pin at the manifest's commit, cited with
    `git show <rev>:<path> | sha256sum`; or
  - staged for change this round, cited with the staged path.
- Drop `tools/witness-metadata.py` and `tools/bash-witness-study.py`.
- Correct the two reason texts (c699c8c/05a2247 drift; X06 staged, not landed).
- The tool payload should add `live_sha256` and `live_matches_pin` per
  historical key, so drift stays visible instead of being bypassed.

## 4. What a non-author needs to re-derive C2

1. `git show 98bea7d:SKILL.md` lines 1503-1504, 1552-1553, 1581-1583, 1601,
   1680-1681, 1740, 1810-1813, and `SCORECARD.md` 240-247. These are the only
   expectation authority.
2. The after rev's committed `tools/registry.json`, with its sha256, and each
   row's `source`/`fills`, checked against item 1.
3. Two runs:
   - `registry-check.py --rev 98bea7d --registry <committed after registry> --json`;
   - `registry-check.py --rev AFTER --json`.
   Diff them over the pre-existing partition only. The expected honest shape at
   before is the 20/24 table above.
4. For the disposition row:
   - the before-red id `expected_input_digest_mismatch` on the original argv;
   - the after-green on the v2 argv with `"status": "clean"`, `"effective": 11`,
     `"superseded": 1`;
   - the superseded v1 row still listed with `got=2`.

## Impacted axes

- **Operability:** O1, O3, O6 (the count can be inflated or narrowed without
  any tool change).
- **Calibration:** O2, O4, O5 (outcomes or provenance are claimed, not measured).
- **Depth:** untouched.

These are fixable defects (P1-P8), not a tradeoff the judge must reject. The
real repair exists: v2 on the round-17 manifest gives the clean outcome that
SCORECARD:246 promises. As specified, however, contract B cannot distinguish
that repair from excising the row.

Verdict: **falls.** As specified and as built so far, held=N/N is
self-fulfilling. O1 is demonstrated: `held=1/2` becomes `held=1/1` (exit 0)
after a status flip. O5 is present in the landed v2 manifest. C2 becomes
falsifiable under P1-P8.
