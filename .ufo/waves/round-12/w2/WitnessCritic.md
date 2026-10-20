# WitnessCritic — C2 accidental-kill attribution and denominator critic (round 12, w2)

Seat: critic, leaf, read-only. This report is advisory and lane-internal. It is not a non-author admission or promotion, and it is not a pass.
Tool installs: none. Scratch: `/tmp/tameshi-r12-witnesscritic/` holds a copy of the tool for synthetic classifier probes (`PYTHONDONTWRITEBYTECODE=1`). I did not run any spec defect or sweep, and I did not run the tool's own selftest.

Snapshots:
- First full read of `tools/bash-witness-study.py`: sha `bb4181aa…`.
- Current tool: tag AEFA, sha `1e9f2d05…`. **Line refs below are to this one.**
- Runner: `tools/mutate-and-run.sh`, sha `75ed934d…`.
- Target: `pristine.sh`, sha `275d8294…`.

## Outcome hygiene and my own exposure

- **What the executor received from me.** I sent nothing to WitnessFinish before the declaration.
- **Declaration timing.**
  - `declared.tsv` was frozen at 2026-10-20T03:45:36Z, sha `0def0d3b…`, according to `declaration.json` `created_at` and `declare.out`.
  - `declaration-before-run.txt` is stamped 03:46:12Z.
  - The sweep began at 03:46:20Z (`MUTATE_DATE` in `crashed-*-sweep.cli.log`).
  - All three times are self-attested (inherited T8). None is external.
- **My exposure.** At about 03:44Z, before that freeze, a context-line grep showed me `tools/mutate-and-run.sh:555` (`TABLE_BASH`). Nothing I sent depended on it.
- **Outcome content.** The outcome analysis below appears only because the declaration now exists. It relies on retained raw logs under `.ufo/evidence/round-12/BashWitness/crashed-20261020T034646Z-sweep/`.

## Axes
- **depth (C2):** does the split into killed-on-witness / accidental / survived / inconclusive show which assertion killed each defect?
- **calibration:** is every denominator complete and the one that actually ran? This covers defects, cases and runs.
- **provenance:** is everything that classifies covered by the frozen declaration?

## Static audit of the declared witnesses (observed, done against `pristine.sh`)

I traced each rationale against the target and found no bogus witness. The declared case names match the 16 selftest labels at `pristine.sh:767-842`.

| defect | mechanism I checked | finding |
|---|---|---|
| B1 | `:241`, scan dirs at `:721-723` | only `undeclared-file` (`:771`) asserts UNLISTED; correct |
| B2 | fixture part=1 (`:712`), floor=1 (`:740`) | boundary sits on the clean path; **no specific case exists** |
| B3 | baseline 600 (`:745`) equals census 600 (`:724`) | `clean` and `crosscheck-disagree` are correct. The declaration **omits `runtime-absent`**, which also carries baseline 600 and wants exit 0 (`:770`) |
| B4 | `:200-204`, then `:210-212` | `symlink-swap` turns from a LINK token into DIVERGED; correct |
| B5 | `:214-217`; exec fixture is 755 (`:707`) | NONE is mechanically correct |
| B6 | `:371`, 16-byte expectation | clean path only; **no specific case exists** |
| B7 | `:405-406`; three sqlite rows; `:782` | `sqlite-unavailable`; correct |
| B8 | `:85`; dies at `:169` and `:337` | `malformed-row` and `fused-shape-row`; correct |
| B9 | `:191` | `asset-gone` and `runtime-absent`; correct |
| B10 | `:862`; no case asserts the CLEAN line | NONE is correct |

## Post-declaration outcome audit (raw logs in `crashed-…-sweep/evidence/`)

Failing labels come from line-anchored `^bad-case` only:
- Every run has 16 case lines and a terminal `SELFTEST:` line.
- Every run has 14 exercised cases and 2 skipped (`verbs-*`).
- The control is `SELFTEST: PASS (16 cases)`.

| defect | runner verdict | failing labels | declared witnesses | hits / misses / undeclared extra |
|---|---|---|---|---|
| B1 | KILLED | undeclared-file | undeclared-file | 1/0/0 |
| B2 | KILLED | clean, runtime-absent | clean, runtime-absent | 2/0/0 (**generic only**) |
| B3 | KILLED | clean, runtime-absent, crosscheck-disagree | crosscheck-disagree, clean | 2/0/**1** |
| B4 | KILLED | symlink-swap | symlink-swap | 1/0/0 |
| B5 | SURVIVED | — | NONE | — |
| B6 | KILLED | clean, runtime-absent | clean, runtime-absent | 2/0/0 (**generic only**) |
| B7 | KILLED | sqlite-unavailable | sqlite-unavailable | 1/0/0 |
| B8 | KILLED | malformed-row, fused-shape-row | same | 2/0/0 |
| B9 | KILLED | asset-gone, runtime-absent | same | 2/0/0 |
| B10 | SURVIVED | — | NONE | — |

- The runner verdicts match `TABLE_BASH` at `mutate-and-run.sh:555`, with 0 flips.
- `B5.out`, `B10.out` and `control.out` are byte-identical: all three have sha `09c21ee2…`.

## Counterexamples

| # | Counterexample (evidence) | Axis | Kind |
|---|---|---|---|
| K1 | **Generic-only witness, so killed-on-witness is unfalsifiable at case level.** B2 and B6 have identical failing sets, `{clean, runtime-absent}` (`crashed…/evidence/B2.out` sha `879b7d8e…` and `B6.out` sha `06910090…`). The same set came from the synthetic, unrelated X3 and X4 (`w1/WitnessThreats.md` O4). Any defect that breaks the clean path would score "on-witness" for B2 and B6. The dumps do discriminate. B2.out shows `rows part 1 < floor 1`; B6.out shows `magic mismatch (not a 15-byte+ NUL header)`. But the tool never reads dump lines (`CASE_RE` `:172`), so that confirmation is **post-hoc and was not declared**. | depth | tradeoff, which must be disclosed |
| K2 | **The any-hit rule hides misses and extras.** `:429-431` classifies on `hit` being non-empty. Synthetic probe P2: with only `{clean, runtime-absent}` failing, B3 (declared `crosscheck-disagree, clean`) and B9 (`asset-gone, runtime-absent`) both return `killed-on-witness`, so a miss on the specific witness is invisible. In the real run there are 0 misses, but B3 has one undeclared extra (`runtime-absent`) that nothing reports. QUALITY.md criterion 6 needs misses as errata rows. | depth | fixable |
| K3 | **The NONE/witness split is not out-of-sample.** The disclosure (`:162-170`) says `TABLE_BASH` was seen. The NONE rows `{B5, B10}` equal the recorded and observed survivors, and every witness row was a recorded kill. So `survived=2` and `accidental=0` follow from that exposure; they are not evidence. The only new C2 information is **which cases failed among the 8 kills**. | depth / provenance | disclosure; the claim must narrow |
| K4 | **`witness_classified` counts inconclusive rows.** `:658` sets it to `len(rows)`. Probe P4: one inconclusive row plus one killed row gives `witness_classified=2`. This partial denominator is reported as complete. | calibration | fixable: `total - inconclusive` |
| K5 | **An undeclared defect id becomes "accidental (declared-NONE)".** `:577` calls `declared.get(ident)`, which returns None, and `:428` then classifies the defect as accidental. Probe P3 shows this. Duplicate result rows are not rejected either (the set at `:565`/`:601`). `missing` is computed from the code constant `DECLARED_WITNESSES` (`:602`), not from the frozen `declared.tsv`, so two authorities decide coverage. | calibration | fixable: refuse ids not in the TSV, refuse duplicates, and use the TSV id set |
| K6 | **The classifier is outside the frozen declaration.** `declaration.json` hashes the target, spec, runner and `declared.tsv` (`:773`ff), but not `tools/bash-witness-study.py`. The run crashed after the outcomes had printed (`run.out`: `KeyError: 'skip'` at old `:409`, because `control_record` returns `skip_labels`). The tool was then edited after the outcomes (sha `bb4181aa` became `1e9f2d05`; the shim is at `:562-564`). The edit looks mechanical, but nothing proves that the rule text at `:414-432` is unchanged. The selftest builds `control = {"skip": …}` (`:1049`), which hid the defect. The REV fixture with 64 `b`s hid the earlier 40-hex REV refusal (`declare.out` first attempt) in the same way. | provenance | fixable |
| K7 | **Partial run denominator.** The first sweep was moved to `crashed-…-sweep/` outside the tool: the tool has no `crashed` code, and the log still says `MUTATE_EVIDENCE …/sweep`. `write_manifest` (`:706-714`) covers only `sweep/` and `sweep.cli.*`. A second run's summary and manifest would therefore leave out run #1 and its raw outputs. | calibration / provenance | fixable |
| K8 | **`rerun` destroys the committed summary and never compares.** `_execute_sweep` writes `evidence/summary.json` and the manifest (`:851-852`). `cmd_rerun` then reads that overwritten file as `prior` (`:880`) and reads `rundir/summary.json` (`:881`), which no code path writes. The result is an exit-2 Cannot after the committed classification has already been replaced. | calibration / provenance | fixable |
| K9 | **`count` does not re-evaluate.** `declared` (`:897`) is parsed and never used. The rows and counts are echoed from `summary.json` (`:919`). A summary whose classifications were edited, but whose declaration sha is intact, still counts. This contradicts the docstring at `:18`. | depth | fixable (overlaps WitnessIntegrity) |
| K10 | **Smaller issues.** (a) The control `"exit": 0` is hard-coded (`:614`), not observed. (b) `failures` is never cross-checked against `len(bad)`; probe P5 gives `FAIL (5/16)` with 1 bad line → `killed-on-witness`. (c) If the control has no skips (`:407`, probe P6 → `[]`), the run is admitted. If `the-janitor` is on PATH, verbs cases run the real handler (`pristine.sh:818-819`), `DEEP` is not scrubbed (`:94`; it is read at `pristine.sh:584,604,626`), and the "14+2" claim in the docstring becomes false. (d) `env_facts()` is captured after the sweep (`:691`). | calibration | fixable |

## Honest split I would accept from this evidence

- **Defects:** 10 in the denominator, 0 inconclusive, 8 runner-KILLED, 2 SURVIVED.
- **Cases:** each run executed 14 of 16 printed cases, with 2 skips on this host.
- **killed-on-witness: 8/8 kills**, broken down as:
  - **specific-witness hits: 6** (B1, B3, B4, B7, B8, B9);
  - **generic-only: 2** (B2, B6). Their mechanism is confirmed only by a post-hoc dump read.
- **Declared witnesses:** 0 misses, 1 undeclared extra (B3 `runtime-absent`).
- **accidental 0 and survived 2:** these were shaped by the disclosed exposure (K3) and carry no C2 weight.
- **Ledger identity:** "leg 2 (bash-surface-census) reanalysis", never a new gate (inherited T9).

## Smallest safe corrections (not applied; WitnessFinish and L1 own them)

1. **`counts()` (`:658`):** `witness_classified = total - inconclusive`. Add `specific_hit`, `generic_only` (where the hits are a subset of `{clean, runtime-absent}`), and per-row `witness_hits`, `witness_misses` and `undeclared_failures`.
2. **`collect_results`:** refuse ids that are not in the parsed `declared.tsv`, refuse duplicate ids, and compute `missing` from the TSV keys.
3. **Inconclusive** if `failures != len(bad)`, or if the control skip set differs from `EXPECTED_SKIP_LABELS`. Add `DEEP` to `SCRUB_ENV`.
4. **Hash the classifier.** Record the sha of `tools/bash-witness-study.py` in `summary.json` next to the declaration hash. Disclose the post-outcome KeyError fix as an erratum whose diff is limited to `:562-564`, with `:414-432` byte-unchanged. Make the selftest fixtures use real shapes: `control_record()` output and a 40-hex REV.
5. **Runs:** record run #1 (`crashed-…`) and its raw-log hashes in the manifest and summary. Report that run 2 differs from run 1 in 0 rows, or name the rows that flip.
6. **`rerun`:** write the fresh summary into `rundir/`, never into `evidence/summary.json`.
7. **`count`:** re-classify from the raw logs plus `declared.tsv`, and refuse on any difference from the stored rows.
8. **Claim text:** "case-level witness; 6 specific, 2 generic-only; dump-level mechanism for B2 and B6 is post-hoc; NONE and survived rows are not out-of-sample given the disclosed `TABLE_BASH` exposure."

## Owned paths
- Written: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-12/w2/WitnessCritic.md` (this file) only.
- Scratch: `/tmp/tameshi-r12-witnesscritic/bws.py`, a copy of the tool used for probes P1–P6.
