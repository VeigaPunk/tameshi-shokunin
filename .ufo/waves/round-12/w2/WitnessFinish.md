# WitnessFinish — pinned bash witness experiment, round 12 w2

Seat: `TameshiR12.WitnessFinish` (leaf executor). Advisory, lane-internal.
Not an independent non-author admission, not a promotion, not a blind
preregistration. The declared mapping was authored with prior exposure to
recorded aggregate outcomes (disclosure below); it was hashed before the
canonical sweep and never rewritten after results.

## Owned paths

- `tools/bash-witness-study.py` — repaired in place; final sha256
  `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`
  (1629 lines). Untracked before and after; no commit made.
- `.ufo/evidence/round-12/BashWitness/**` — declaration, target, spec,
  canonical sweep, retained crashed run, rerun, selftest transcripts,
  `summary.json`, `manifest.json`.
- This report only under `.ufo/waves/round-12/w2/`.

No repository files outside the owned paths were modified by this seat. No
commits, pushes, fleet writes, model or routing edits. Tooling: no installs or
upgrades; Python 3.14.7, `/usr/bin/sqlite3` present, `the-janitor` absent.

## Disclosure and declaration freeze

Kind recorded in `declaration.json:5`: **declared-witness mapping, not a blind
preregistration**. Before declaring, the author had seen the recorded kill-rate
header of `tools/mutate-and-run.sh`, the `corpus/README.md` coverage row for
`mutation-case-kagi-census.md`, the `SOURCES.md` S033 row, and the recorded
`TABLE_BASH` per-defect KILLED/SURVIVED entries surfaced by a pin grep. No
per-defect *witness* classification of this leg existed before this run. My own
pin read (`tools/mutate-and-run.sh:544-559`) also surfaced `TABLE_BASH` before
the declaration; that is within the disclosed exposure and did not change the
mapping. The `DECLARED_WITNESSES` rows were not edited.

Frozen inputs before the canonical sweep:

| input | sha256 |
|---|---|
| `declared.tsv` | `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3` |
| `declaration.json` | `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901` |
| `pristine.sh` (target) | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` = `PIN_BASH` |
| `bash-surface-census.spec` | `d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741` |
| `tools/mutate-and-run.sh` | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |
| `declaration-before-run.txt` | `d2343ddf7675c09313b02115453095969a285ed7cc3d85abd72b9c1e13b40042` |

`declared.tsv` header links target, spec and runner digests; rows are B1–B10,
with B5 and B10 declared `NONE`. `cmd_declare` refused to overwrite an existing
declaration; the mapping is frozen.

## Failed attempts (no hidden path)

1. **Declare attempt 1 (pre-fix, before any sweep):** exit 2 with
   `WITNESS_STUDY: CANNOT-EVALUATE (runner is missing pin constant(s): REV_BASH)`.
   Cause: the inherited `PIN_RE` demanded 64 hex for both constants, but
   `REV_BASH` is a 40-hex git id (`tools/mutate-and-run.sh:545`). Fixed by
   splitting `PIN_RE` (64-hex digest) from `REV_RE` (exact 40-hex revision) at
   `tools/bash-witness-study.py:197-198` and reading both in `runner_pins`
   (`:261`). The failed stdout was overwritten by the successful `declare.out`;
   `declaration-hash.txt` is its partial hash attempt (pristine only) and is
   superseded by `declaration-before-run.txt`. No sweep ran in this attempt.
2. **Run attempt 1 (post-declaration, pre-classifier-fix):** the sweep itself
   completed and `sweep/results.tsv` had all 10 rows, but classification crashed
   with `KeyError: 'skip'` because `control_record` exposes `skip_labels` and
   `run_problems` indexed `control["skip"]`. Raw retained:
   - `crashed-20261020T034646Z-run.out` sha256
     `56ca34615f6c2d84a1305c3435458e6bd0c1732dc11095eb4e8b5291deb1c102`
     (traceback ending `KeyError: 'skip'`);
   - `crashed-20261020T034646Z-sweep/` (full evidence, `results.tsv`
     header + 10 rows), `.cli.log`, `.cli.exit` (`0`).
   The normalization fix (`control.get("skip", control.get("skip_labels", []))`
   at `tools/bash-witness-study.py:635-637`) was made **after observing this
   crash**. It is not a pre-declared condition.
3. **Rerun pre-fix defect (repaired before execution):** inherited `rerun`
   called `_execute_sweep`, which overwrote `evidence/summary.json`, then read
   `rundir/summary.json`, which was never written. Repaired at
   `tools/bash-witness-study.py:942-990` (write to `outdir`) and
   `:1008-1039` (read prior summary before the sweep; compare with the fresh
   summary in the rerun directory; preserve the committed summary). The repaired
   rerun was then executed once; no failed rerun attempt exists.

No other failed commands were run.

## Repairs applied (path:line)

| item | change |
|---|---|
| pin/revision parsing | `PIN_RE` 64-hex, `REV_RE` exact 40-hex (`:197-198`); `runner_pins` (`:261`); `materialize_target` rejects non-40-hex and runs `git show --end-of-options` (`:332-340`) |
| control skip KeyError | normalized `skip` view in `collect_results` (`:635-637`) |
| runner exit / restore / DONE gates | `_execute_sweep` refuses exit ∉ {0,1}, missing/mismatched `MUTATE: DONE|DEGRADED`, anchored `CONTROL: GREEN`, and requires `MUTATE_RESTORE: OK (target-sha256 before=<pin> after=<pin>` (`:942-990`); `run_sweep` uses anchored regexes and keeps `cli.log`/`cli.exit` under the sweep dir (`:588-620`) |
| unknown verdict fall-through | `classify` returns `unknown-verdict:<v>` unless the verdict is exactly `KILLED` (`:475-486`) |
| PASS/bad/exit inconsistency | `run_problems` requires `failures == len(bad)`, `(failures>0) == (exit!=0)`, a duplicate-free case set equal to the pinned 16-label catalog (`:435-471`) |
| FAIL without denominator | `parse_case_lines` keeps `total=None` instead of `int(None)` (`:403-431`) |
| duplicate/unknown defect ids | `parse_spec` rejects duplicate ids (`:286-301`); `collect_results` rejects duplicate/unknown result ids, missing declared rows, wrong row count, non-integer fields, verdict/exit mismatch, and mutant-digest mismatch (`:624-705`) |
| non-UTF-8 logs | `read_text_lossy` for suite logs (`:231`); `read_text` catches `UnicodeDecodeError` (`:214-220`) |
| full manifest | `manifest_files` walks every regular file except `manifest.json`/`*.tmp` (`:811`); `write_manifest` hashes all of them (`:824`) |
| mandatory check | `cmd_check` requires `manifest.json`, the mandatory name set, exact present-vs-listed equality (unlisted/missing), unsafe-path refusal, malformed-digest refusal, summary linkage and frozen-mapping equality (`:1118-1216`) |
| count recomputation | `cmd_count` re-derives rows/classifications from `results.tsv`, mutants and raw logs, compares every row/count/status with `summary.json`, and refuses a mismatch (`:1041-1116`) |
| rerun preservation | fresh `summary.json` under `rerun-<stamp>/`, committed summary preserved, classification comparison, manifest re-anchor (`:1008-1039`, `:942-990`) |
| witness_classified | now excludes inconclusive rows (`:751-759`); with 0 inconclusive it is 10/10 |
| classifier digest | `summary.json` records the executing tool path + sha256 (`:780-783`) |
| environment | `DEEP` and `ONEPASSWORD_BROWSER_SUPPORT` scrubbed (`:116-117`); a `the-janitor` on `PATH` refuses the sweep (`:588-591`) |
| usage exit | `UsageParser` maps argparse errors to exit 64 (`:1570-1576`), matching the declared probe contract; verified by selftest |
| selftest coverage | added summary tamper, pruned/missing manifest, duplicate/unknown result ids, verdict/exit mismatch, mutant digest, FAIL-without-denominator, unknown verdict, duplicate labels, PASS+bad, KILLED+exit 0, usage 64, count mismatch (`:1339-1558`) |

## Canonical experiment

Commands, in order, on the frozen declaration:

```
python3 tools/bash-witness-study.py run
python3 tools/bash-witness-study.py count
python3 tools/bash-witness-study.py rerun
python3 tools/bash-witness-study.py check
```

### Run (tool sha 249d…, summary sha `acc01268…`)

```
WITNESS_RUN: complete — killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10
WITNESS_RUN: control denominator=16 exercised=14 skipped=2
WITNESS_RUN: summary /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness/summary.json
```

Raw canonical artifacts: `sweep/results.tsv` sha
`6399660d…`; `sweep/evidence/control.out` sha `09c21ee2…`;
`WITNESS_RUN` exit 0; `sweep.cli`/restore proof: `MUTATE: DONE
(target=bash-surface-census defects=10 killed=8 survived=2 inconclusive=0
kill-rate=80%)`, `CONTROL: GREEN`, `MUTATE_RESTORE: OK` with before/after
`275d8294…`.

### Denominator and skip accounting

The preserved control log has exactly 16 declared cases: 14 exercised
(`ok-case`/`bad-case`) and 2 skipped (`skip-case` `verbs-sandboxed`,
`verbs-break-injection`), because `the-janitor` is absent (summary environment:
`the_janitor_on_path: null`, `sqlite3_on_path: /usr/bin/sqlite3`). Every mutant
log has the same denominator 16, exercised 14, skipped 2. The two skips are
recorded, never counted as executed, and match the control skip set. A
`the-janitor` on `PATH` would now refuse the sweep by design, so this host
cannot exercise the two verbs cases.

### Results — case-level only

Each row states the declared case labels, the observed failing labels, and
hits/misses/extras. This is a selftest-case prediction, not a function- or
line-level coverage claim.

| defect | declared witnesses | observed failing cases | hits | misses | extras | class |
|---|---|---|---|---|---|---|
| B1 | `undeclared-file` | `undeclared-file` | 1 | 0 | 0 | killed-on-witness |
| B2 | `clean`, `runtime-absent` | `clean`, `runtime-absent` | 2 | 0 | 0 | killed-on-witness (generic-only) |
| B3 | `crosscheck-disagree`, `clean` | `clean`, `runtime-absent`, `crosscheck-disagree` | 2 | 0 | `runtime-absent` | killed-on-witness (specific + extra) |
| B4 | `symlink-swap` | `symlink-swap` | 1 | 0 | 0 | killed-on-witness |
| B5 | `NONE` | none | — | — | — | survived (declared NONE; not out-of-sample) |
| B6 | `clean`, `runtime-absent` | `clean`, `runtime-absent` | 2 | 0 | 0 | killed-on-witness (generic-only) |
| B7 | `sqlite-unavailable` | `sqlite-unavailable` | 1 | 0 | 0 | killed-on-witness |
| B8 | `malformed-row`, `fused-shape-row` | `malformed-row`, `fused-shape-row` | 2 | 0 | 0 | killed-on-witness |
| B9 | `asset-gone`, `runtime-absent` | `asset-gone`, `runtime-absent` | 2 | 0 | 0 | killed-on-witness |
| B10 | `NONE` | none | — | — | — | survived (declared NONE; not out-of-sample) |

Counts: `killed_on_witness=8`, `accidental=0`, `survived=2`,
`inconclusive=0`, `total=10`, `witness_classified=10`, `declared_none=B5,B10`,
`unresolved=none`. In the requested framing: **six specific hits** (B1, B3, B4,
B7, B8, B9) and **two generic-only hits** (B2, B6; their witnesses are the
generic baseline cases `clean`/`runtime-absent`). Every declared witness in
every killed row was observed; there are no misses. One extra failing case
exists: B3 also failed `runtime-absent`, which was not declared. B5 and B10
were declared `NONE` and survived; they are exclusions, not out-of-sample
predictions, and are not counted as witness hits.

### Count recomputation (read-only)

`count` re-read the raw results and printed the ten rows above; it returned 0
with `unresolved none` and the same counts. The stored `summary.json` matched
the recomputed rows, counts and status. This is now a recomputation, not the
old summary-trusting print.

### Rerun (repeat sweep, repaired path)

```
WITNESS_RUN: complete — killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10
WITNESS_RUN: control denominator=16 exercised=14 skipped=2
WITNESS_RUN: summary .../rerun-20261020T035435Z/summary.json
WITNESS_RERUN: committed summary preserved at .../summary.json
WITNESS_RERUN: agreement 10/10 rows; deviations=none
```

Fresh rerun summary sha `6726421f…`; all ten classifications identical to the
committed summary. The committed `summary.json` was not overwritten.

### Check (final full manifest)

```
WITNESS_CHECK: CLEAN (declared.tsv sha256=0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3, 96 files covered, 95 manifest entries)
```

Final `summary.json` sha `acc01268…`; `manifest.json` sha `273ffc39…`. The
manifest covers the canonical `sweep/**`, the rerun directory, the retained
crashed run (`crashed-20261020T034646Z-run.out`, `crashed-…-sweep/**`),
`selftest.prefix.out`, `selftest.out`, `declare.out`, the declaration pair,
target, spec, and the pre-run hash record. A missing manifest is now a
`Cannot`; a pruned manifest is a `FAIL` naming both the missing required entry
and the unlisted file; a modified summary is `TAMPER`.

## Selftest

- Final post-fix selftest: **40/40 pass**, `VERDICT: PASS`; output
  `selftest.out` sha `2cd01d5271fc017cdea9e5e62a197952a67fd7e676926ce8f97ddb4590ed461c`,
  executing tool sha `249d9dcd…`.
- Pre-fix selftest: 21/21 pass, retained as `selftest.prefix.out` sha
  `51d6cf72…`. It did not mirror the real 40-hex `REV_BASH` fixture and had no
  integrity/count/manifest cases; the final suite adds those bounded fixtures.
- Two selftest executions exist (one pre-fix exploratory, one final canonical).
  No loop or repeated rerun was used. No build/lint/test gate was run; the
  selftest is the experiment's own hermetic fixture suite, as assigned.

## Residual risks and limits

1. **History-bound declaration.** `declaration.json` was created at
   `2026-10-20T03:45:36Z`, before the post-outcome KeyError and parser/integrity
   repairs. The declared mapping itself was not edited. `declaration.json` does
   not pin the classifier; the executed classifier digest is recorded in
   `summary.json` (`tool.sha256=249d9dcd…`). A coordinated rewrite of
   `declaration.json` + `declared.tsv` + `manifest.json` (and the in-code
   mapping) would not be detected by `check`; the manifest is not self-anchored.
   This is documented, not adversarially solved.
2. **Environment delta after declaration.** `declaration.json` records three
   scrubbed variables (`THE_JANITOR_BIN`, `SQLITE3_BIN`, `CENSUS_BREAK`);
   `summary.json` records five (adds `DEEP`, `ONEPASSWORD_BROWSER_SUPPORT`).
   The additions were made from the WitnessParser/WitnessSecurity findings
   before the canonical sweep. `the-janitor` was absent, so the verbs cases were
   already skipped; no classification changed.
3. **Skipped verbs cases.** The two `the-janitor`-dependent cases were not
   executed. With the new refusal, a host that has `the-janitor` on `PATH`
   cannot run this sweep at all. The denominator is 16 declared / 14 exercised +
   2 skipped, not 16 executed.
4. **Case-label provenance.** Labels are parsed from the mutant's stdout. A
   mutant that prints a declared label while exiting nonzero could still be
   `killed-on-witness`; catalog equality, duplicate detection and
   failure/exit-count checks narrow but do not cryptographically prove
   provenance. This is a residual by design (WitnessParser L2).
5. **B3 extra and generic-only rows.** B3 hit both declared witnesses but also
   failed `runtime-absent`; B2/B6 rely on the generic baseline cases rather than
   a defect-specific case. They are reported as such, not upgraded.
6. **Cosmetic summary mirror.** `summary.json` `declaration.kind` is null
   because `build_summary` reads `declaration["declared"]["kind"]` while
   `declaration.json` stores `kind` at top level
   (`tools/bash-witness-study.py:784`). The disclosure string is present and
   correct; this field does not affect classification or the disclosure. Left
   unfixed after the canonical run to keep the recorded tool digest
   (`249d9dcd…`) exactly the executing tool.
7. **Control exit fact.** `control_record` records `exit: 0` by runner contract;
   `_execute_sweep` gates an anchored `CONTROL: GREEN` line and the control
   log's completeness. No separate control-exit re-read was added.
8. **Repeat comparison is classification-level.** The rerun compared
   classifications (10/10), not durations or byte-identical stdout; per-run
   timing varies.

## Bottom line

The inherited experiment is finished on the pinned blob: declaration frozen and
hashed before the sweep, canonical sweep complete with the exact 16-case
denominator (14 exercised + 2 declared skips), eight declared-witness kills,
two `NONE` survivors, zero accidental/inconclusive, a 10/10 repeat, and a
clean full-manifest check. The post-outcome KeyError crash and the repaired
rerun path are named above with retained raw evidence. This report is
advisory and case-level; it is not an independent non-author admission.
