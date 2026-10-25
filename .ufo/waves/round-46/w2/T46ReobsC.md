seat: T46ReobsC
item: C1 independent re-observation at CONTENT `6f2168e0` — ran all 22 frozen statement argv once each in a CONTENT clone/mirror, re-read the restated standing rows from the CONTENT `SCORECARD.md` blob with the counter's own `last_rows`/`claim_of`, re-ran the three named selftests a second time for stability, and attacked the restated rows' `What`/`First-working round` cells against what each command actually proves (22/22 MATCH; 2 HIGH findings are in the row prose, not in the evidence cells)

Read-only on the lane: no lane file written except this report. No `git add/commit/stash/checkout/switch/reset/pull/push` in the lane, no `jj` command, no write to `/home/vgpnk/Projects/shokunin` or a sibling lane, no write to `/home/vgpnk/Projects/shokuknow`. All scratch under `/tmp/tameshi-r46-T46ReobsC/`. No tool installed or upgraded (no pacman transaction attempted).

## Setup (exact commands, as the item prescribes)

```
W=/tmp/tameshi-r46-T46ReobsC; rm -rf $W; mkdir -p $W/fleet && for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
```

Verification:
```
git -C $W/clone rev-parse HEAD                  -> 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git -C $W/fleet/tameshi-shokunin rev-parse HEAD -> 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
ls $W/fleet | wc -l                             -> 21   (20 sibling-lane symlinks + the tameshi mirror)
sha256sum $W/clone/.ufo/evidence/round-46/calibration/statements.json
  -> a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9   (== contract statements_sha256)
```

Pins recomputed by hand at CONTENT (the counter's own three conditions):
```
self_pin=1    (lane .ufo/evidence/round-46/calibration/measure.py sha256 ad5f85df21b1… == blob at 6f2168e0)
stmts_pin=1   (blob sha256 a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9)
append_only=1 (683eedd:SCORECARD.md 207916 bytes is a byte prefix of 6f2168e0:SCORECARD.md 225496 bytes;
               both base and freeze blobs hash to 4b730384fb3924ec0fda5a76f357683e698c93a737b02f51c9d5c38e691741c1)
```

## Method

`/tmp/tameshi-r46-T46ReobsC/run.py` imports `.ufo/evidence/round-46/calibration/measure.py` by path and reuses its own
`env()`, `pick_line()`, `last_rows()` and `claim_of()`, so neither the picked line nor the claim parse is re-derived by
eye. Each statement's frozen argv ran **once** (`cwd` = `$W/clone`, except `six-leg regression ledger` = `$W/fleet/tameshi-shokunin`;
`REV=6f2168e028ce7ff6e82ac92093ac05dd1f147c32` in the env; `{work}`→`$W`, `{clone}`→`$W/clone`, `{rev}`→CONTENT), 22
statements fanned out concurrently the way the counter does it. Each run's stdout/stderr/exit/wall is in `$W/obs/<id>.{out,err,meta}`.

Claims were read from the **CONTENT blob**, not the worktree:
`git -C <lane> show 6f2168e0:SCORECARD.md` → `last_rows()` → 22 `cap` rows + 3 `axis` rows
(`depth`→`9`, `calibration`→`6`, `freshness`→`9`); `claim_of()` per statement.
No statement id is shadowed by another recognised table: the 22 `cap` keys are the 19 statement ids plus the three new
round-46 rows (`declared-mutant driver with neutral controls`, `no-harm-at-base gate and seat-name collision gate`,
`standing-statement counter`).

## Per-statement result (claimed | observed | verdict)

| # | id | kind | claimed (CONTENT row) | observed (my run) | verdict |
|---|---|---|---|---|---|
| 1 | sources-registry | cap | `rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` \| 0 | `rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)` \| 0 | **MATCH** |
| 2 | mutation sweep runner | cap | `MUTATE_SELFTEST: 106/106 pass` \| 0 \| `a7d3f2dd7d47` | same | **MATCH** |
| 3 | six-leg regression ledger | cap | `REGRESSION: PASS (cases=9 passed=9` \| 0 | same | **MATCH** |
| 4 | repeated pristine-control gate | cap | `SELFTEST: PASS (29 cases)` \| 0 \| `296fe566dc59` | same | **MATCH** |
| 5 | six-leg content-disposition probe | cap | `SELFTEST: PASS (19/19)` \| 0 \| `331529eadafe` | same | **MATCH** |
| 6 | exposed witness provenance correction | cap | `SELFTEST: PASS 39/39` \| 0 \| `df3390682a04` | same | **MATCH** |
| 7 | effective expectation reconciliation | cap | `SELFTEST: PASS (66/66)` \| 0 \| `39ee5c5effd9` | same | **MATCH** |
| 8 | retained invocation-context gate | cap | `SELFTEST: PASS (49/49)` \| 0 \| `7e4519d9a0ea` | same | **MATCH** |
| 9 | hermetic env-differential probe | cap | `ENVDIFF_SELFTEST: 9/9 pass` \| 0 \| `e8b47ab7cf23` | same | **MATCH** |
| 10 | callback-authoritative wave accounting | cap | `ACCOUNTING_SELFTEST: 8/8 pass` \| 0 \| `96b3038a77f8` | same | **MATCH** |
| 11 | required-command-receipt-binding | cap | `COMMAND_BINDING_SELFTEST: 44/44 pass` \| 0 \| `9230c68e53a5` | same | **MATCH** |
| 12 | refusing-registry-replay | cap | `REGISTRY_REPLAY_SELFTEST: 10/10 pass` \| 0 \| `9fcd2dbba737` | same | **MATCH** |
| 13 | mutation report interop | cap | `MTE_SELFTEST: 17/17 pass` \| 0 \| `193ea6e32f89` | same | **MATCH** |
| 14 | tally-audit-v2 runner audit | cap | `TALLY_AUDIT_V2_SELFTEST: 22/22 pass` \| 0 \| `7b11ba25aead` | same | **MATCH** |
| 15 | tally-audit-v3 runner audit | cap | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| 0 \| `da8c1ef4b30c` | same | **MATCH** |
| 16 | bounded ANSI-C code_view | cap | `TALLY_AUDIT_V3_SELFTEST: 35/35 pass` \| 0 \| `da8c1ef4b30c` | same | **MATCH** (shares argv 15) |
| 17 | write-path-census-v2 | cap | `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` \| 0 \| `402285329588` | same | **MATCH** |
| 18 | write-path census destination resolution | cap | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` \| 0 \| `095924a7a165` | same | **MATCH** |
| 19 | staged-id adoption guard | cap | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` \| 0 \| `03a796c5726c` | same | **MATCH** |
| 20 | depth | axis | `9` | `9` | **MATCH** |
| 21 | calibration | axis | `6` | `6` | **MATCH** |
| 22 | freshness | axis | `9` | `9` | **MATCH** |

Tally: **MATCH 22, MISMATCH 0, UNPARSED 0, UNOBSERVABLE 0 → non-match total 0** (`/tmp/tameshi-r46-T46ReobsC/run.log`).
Every exit code 0; stderr 0 bytes for all 22; every non-special `obs` regex matched exactly one line
(`regex_matches=1` for all 19 unique regex argv, covering 20 statements); the `census` anchors occur once each
(`grep -c '^== A rows$'` = 1, `grep -c '^SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)$'` = 1) and the `monitor`
key occurs once (`calibration_restraint_score` → `6`, `coldread.box3_full_page` → `False`).

Exit/wall/timeout (22-way fan-out, `/tmp/tameshi-r46-T46ReobsC/summary.json`); longest four:
```
tally-audit-v3 runner audit       exit=0 wall=681.53s timeout=1800
bounded ANSI-C code_view          exit=0 wall=681.43s timeout=1800
six-leg regression ledger         exit=0 wall=384.04s timeout=2700
tally-audit-v2 runner audit       exit=0 wall=323.42s timeout=900
```
All others ≤ 32.7 s; nothing near its timeout, nothing timed out.

`sha_file` statements, item step 2 form, all 16 unique files at CONTENT
(`git -C $W/clone show HEAD:<file> | sha256sum | cut -c1-12`), each equal to the claimed prefix:
```
tools/mutate-and-run.sh          a7d3f2dd7d47    tools/wave-accounting.py        96b3038a77f8
tools/repeat-control.py          296fe566dc59    tools/command-binding.py        9230c68e53a5
tools/pin-disposition.py         331529eadafe    tools/registry-replay.py        9fcd2dbba737
tools/witness-metadata.py        df3390682a04    tools/mte-interop.py            193ea6e32f89
tools/evidence-disposition.py    39ee5c5effd9    tools/tally-audit-v2.py         7b11ba25aead
.ufo/evidence/round-15/verify.py 7e4519d9a0ea    tools/tally-audit-v3.py         da8c1ef4b30c
tools/env-diff.py                e8b47ab7cf23    tools/write-path-census-v2.py   402285329588
                                                 tools/write-path-census-v3.py   095924a7a165
                                                 tools/staged-id-guard.py        03a796c5726c
```

## The three statements this seat names

All three: `cwd=clone`, `sha_file` set, `timeout` 900, exit 0, stderr 0 bytes. Each was run a **second** time
(`python3 tools/<tool>.py --selftest` in `$W/clone`, `REV=6f2168e0…`) and the stdout is byte-identical to the first run:

| id | run 1 line | run 1 bytes / sha256 | run 2 | byte-identical |
|---|---|---|---|---|
| repeated pristine-control gate | `SELFTEST: PASS (29 cases)` | 2936 / `09f432706cf05e43…` | `SELFTEST: PASS (29 cases)` | yes (`cmp -s`) |
| six-leg content-disposition probe | `SELFTEST: PASS (19/19)` | 1409 / `1f39911c34eb1555…` | `SELFTEST: PASS (19/19)` | yes |
| exposed witness provenance correction | `SELFTEST: PASS 39/39` | 6002 / `c4f371609f34fe9a…` | `SELFTEST: PASS 39/39` | yes |

`What` cell judgement (item: "a cell that overstates what the command proves is a finding"):

- **repeated pristine-control gate** — What: *"observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from
  unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots"*. **Accurate, not overstated.**
  The 29 printed cases cover exactly that split: `stable`, six `mismatch-*` (stdout, run-3-only, newline-only, stderr,
  exit, nonzero-exits), `nonzero-baseline`/`child127-baseline`, three `command-unavailable-{enoent,eacces,enoexec}`,
  four `invalid-runs-{2,1,0,abc}` (N≥3 enforced), and nine `snapshot-*` cases including five tamper classes
  (byte, missing, unlisted, duplicate-key, manifest-symlink, observation-symlink). First-working `round 12` matches the
  tool header (`round 12`).
- **six-leg content-disposition probe** — evidence cell is true (`SELFTEST: PASS (19/19)`, sha `331529eadafe`), but the
  What cell **overstates**: see finding **F1 (HIGH)**.
- **exposed witness provenance correction** — What: *"validate a new digest-anchored non-blind companion without
  rewriting frozen observations"*. **Accurate.** The 39 cases include `corrected-companion-green`, `old-null-red`,
  `prior-exposure-missing-red`, `blind-upgrade-red`, `frozen-flag-rewritten-red`, `nested-null-rewritten-red`,
  `tamper-{summary,declaration,rerun}-red`, `symlink-{input,companion}-red`, and the docstring states the frozen bytes are
  never rewritten. First-working `round 13` matches the tool header.

## What / First-working-round cells for the other restated rows

Checked against each command's actual output and the tool source at CONTENT. **Accurate:** mutation sweep runner
(selftest prints `PASS fixture target byte-identical after sweep/regression/r6 cases`, `PASS --regression refuses --target (exit 64)`),
six-leg regression ledger (nine `REGRESSION_CASE` legs; the What itself discloses "nine legs since round 26; the name is
kept as the row id"), effective expectation reconciliation (`exit-only-false-positive`, `missing-row-drop`,
`superseded-oracle-binding`), retained invocation-context gate, hermetic env-differential probe (7 `PROFILES` in
`tools/env-diff.py:29`; committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` has 9 surfaces = 8
`invariant` + 1 `nondeterministic`, matching the cell), callback-authoritative wave accounting
(`failed-with-report-counted-completed`, `registry-id-mismatch`, `snapshot-tampering`), required-command-receipt-binding,
refusing-registry-replay, mutation report interop (`official_score=` / `official_killed=` from the MTE library per case),
write-path-census-v2, write-path census destination resolution, staged-id adoption guard (`T1_indented_collision_seen`,
`T3_cascade_refused`, `T5_dedupe_to_registry_id`, `T4_valid_map_admitted`, `T12_whole_set_in_range_refused`).

Cells that state more than the run demonstrates: **sources-registry** (F3), **tally-audit-v2 / tally-audit-v3** (F6),
**bounded ANSI-C code_view** (F7), plus the three evidence-cell quoting caveats in F4 and the **calibration** axis row
(F2).

## Findings

**F1 — HIGH — `six-leg content-disposition probe`, What cell overstates coverage at REV.**
What: *"emit configured-pin, committed-HEAD and worktree SHA observations for **every recorded leg**, while explicitly
withholding verdict reuse"*.
```
$ sed -n '138,146p' $W/clone/tools/pin-disposition.py
CANONICAL_LEGS = (
    ("js-kimi-census", "kumitate-shokunin", "scripts/kimi-census.mjs"),
    ("bash-surface-census", "kagi-shokunin", "corpus/surface-census.sh"),
    ("bash-tsukuroi-census", "tsukuroi-shokunin", "tools/tsukuroi-census.sh"),
    ("bash-mado-verify", "mado-shokunin", "tools/mado-verify.sh"),
    ("bash-checklist-run", "kagi-shokunin", "corpus/checklist-run.sh"),
    ("js-claims-check", "kumitate-shokunin", "scripts/claims-check.mjs"),
)
$ grep -n 'six recorded legs only' $W/clone/tools/pin-disposition.py
623:                "leg entry {} names unknown leg {!r} (six recorded legs only)".format(index, leg),
$ sed -n '84,95p' $W/clone/tools/mutate-and-run.sh     # the runner ledger at REV: nine legs
#   js-kimi-census … bash-surface-census … bash-tsukuroi-census … bash-mado-verify …
#   bash-checklist-run … js-claims-check … js-round-gate … js-sources-check … js-cite-check
```
At REV the repo records **nine** legs (`grep -c 'REGRESSION_CASE' $W/obs/six-leg-regression-ledger.out` → 9, all nine
named above), the probe covers **six**, and its `NOT_COMPARED` list (`tools/pin-disposition.py:125-134`) does not name the
three unmeasured legs (`js-round-gate`, `js-sources-check`, `js-cite-check`). So the row claims dispositions for every
recorded leg while the command produces them for 6 of 9, and the row id ("six-leg …") contradicts its own What.
`claim_of` cannot see this: it compares only the printed line/exit/sha.

**F2 — HIGH — `calibration` axis row: a stale supporting value the counter cannot see.**
Row (CONTENT `SCORECARD.md`, axis table): *"(`box3_full_page=false`, **60 of 64 sections credited**)"*, with
"Measured commit: round-46 content revision".
```
$ python3 -c "import json;d=json.load(open('$W/obs/calibration.out'));c=d['coldread'];print(d['calibration_restraint_score'], c['sections_covered'], c['sections_total'], c['box3_full_page'])"
6 55 64 False
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo $W/clone --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
base: score=6 covered=60/64 box3_full_page=False
```
`60 of 64` is the **base**-rev value (and the round-27 record `covered=60/64`); at the content revision the monitor
credits **55 of 64**. The row's score (6) is right, so C1 passes, but the row states a figure its own command contradicts
at the revision the row claims to measure — the same stale-standing-value class C1 exists to remove, surviving in the
row's prose because `claim_of` compares only the integer.

**F3 — LOW — `sources-registry` What lists verbs the census does not exercise.**
What: *"curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated"*.
The frozen command (`.ufo/evidence/kaika-round-1/sources-census-v2.sh`) counts rows, enforces the 13-cell shape, the
`tier ∈ {A,B,C}` / `status ∈ {queued,mined,rejected}` / `kind` enums, duplicate ids, existence of every `mined` row's
used-by file and the B1/B2 id-or-path cite. "tiered" and "mined into admitted entries" are gated; "opened" is not, and
"rechecked" has no enum, column check or printed counter in the script (`grep -c recheck` → 0).

**F4 — LOW — three evidence cells quote something the command does not print as a line.**
```
$ sed -n '1,2p;41p' $W/obs/sources-registry.out
== A rows
120
SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)
$ grep -n 'selftest-new-full-count' $W/obs/retained-invocation-context-gate.out
21:selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)
$ tail -2 $W/obs/six-leg-regression-ledger.out
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /tmp/tameshi-r46-T46ReobsC/regression-wd (kept)
```
- `sources-registry`'s `rows=120 SOURCES_CENSUS: CLEAN (…)` is the counter's `census` **synthesis** (two separate
  output fields joined), not a printed line.
- `retained invocation-context gate` quotes the regex **capture** `SELFTEST: PASS (49/49)`; the line is
  `selftest-new-full-count: PASS summary SELFTEST: PASS (49/49)`.
- `six-leg regression ledger` quotes the truncated capture `REGRESSION: PASS (cases=9 passed=9` (unbalanced paren); the
  printed line continues `; ledger legs exact: killed-delta<=0 flips<=0)`.
Under the counter's predicate these are MATCH by construction (the contract's "what the command prints" is
`pick_line`'s capture). Reported because a human re-running the command sees a different line than the row states.

**F5 — LOW — `after/` receipts cited at the revision that carries the citations do not exist there.**
```
$ grep -o '\.ufo/evidence/round-46/after/[A-Za-z0-9._/-]*' $W/SCORECARD-content.md | sort | uniq -c
      1 .ufo/evidence/round-46/after/
      1 .ufo/evidence/round-46/after/c1.stdout
      1 .ufo/evidence/round-46/after/c2.stdout
      1 .ufo/evidence/round-46/after/c3.stdout
$ git -C <lane> ls-tree -r --name-only 6f2168e0 -- .ufo/evidence/round-46/ | cut -d/ -f4 | sort -u
assimilation before calibration census-start.exit census-start.stderr census-start.stdout contract.json control coverage deciding-run.sh hardening no-harm.sh quality selftest
```
(plus `after/no-harm.stdout` named without the `.ufo/` prefix in the depth row and the round-46 block). No `after/`
directory at CONTENT. This is the contract's landing rule working as designed (deciding runs, then a receipts-only
commit), but at CONTENT every one of these pointers dangles, and the C1 claim row's `Measured commit` cell says "the
content revision (deciding receipts …)" while its `After` cell states `total=0` at **records revision
`e630ae791a831828f51b8f192996a907ff8ed78d`** (`git merge-base --is-ancestor e630ae7 6f2168e0` → ancestor, i.e. an earlier
commit, not CONTENT).

**F6 — INFO — the tally-audit rows state corpus counts the frozen command does not print.**
`tally-audit-v2`: What claims "18 public + 8 sealed must-kill … 8 public + 6 sealed must-accept"; the run prints 22 case
lines (`grep -c '^CASE .*exit 1)$'` → 17, `exit 0` → 5). `tally-audit-v3`: claims "6/6 public + 4/4 sealed must-kill …
3/3 + 3/3 must-accept"; the run prints 35 lines (23 `exit 1`, 9 `exit 0`, 1 `exit 2`, 2 without an exit code — the two
`code_view` cases). The sealed split is not visible in either output, so the printed line evidences `22/22` / `35/35`
only.

**F7 — INFO — 22 statements, 21 unique commands.**
`bounded ANSI-C code_view` and `tally-audit-v3 runner audit` share argv and tool sha; the counter caches one observation
for the shared key (`measure.py` `cache[(argv,cwd,obs,sha_file,kind)]`), so the two rows cannot fail independently. The
`code_view` capability is evidenced by 2 of the 35 cases (`code_view ANSI-C escaped quote trailing comment`,
`code_view ANSI-C literal hash`); its closing clause ("nested substitutions and unquoted backslash-newline remain
unsupported") is a limitation and is not asserted by any case.

**F8 — INFO — wave-1 comparison.**
- Only one observed value differs from wave 1's freeze observations, and it is the intended one: `sources-registry`
  printed `rows=117` at `745a583` (ExecStmt01/ExecStmt02) and prints `rows=120` at CONTENT — the three rows S258/S259/S260
  added at `a6892b1` (`+3`). The restated row states 120, consistent.
- The other 21 statements' observed tuples are identical to wave 1 (same printed line, exit 0, same sha prefix):
  freeze `total=21` was entirely statement-side, and the restatement closed it.
- Wall-clock differs from wave 1 under the same fan-out (v3 681 s vs 381/314 s; regression 384 s vs 155/176 s); load,
  not value — the picked lines are unchanged.
- Wave-1 report arithmetic error, not a statement value: ExecStmt01 states `SCORECARD.md` is 206619 bytes at
  `683eedd`/`745a583`; both blobs are 207916 bytes (`git show <rev>:SCORECARD.md | wc -c` → 207916 for each, sha256
  `4b730384…`), so 206619 is wrong by 1297 bytes.

**F9 — INFO — stability and side effects.**
The three named selftests are byte-reproducible (second run identical, above). The `six-leg regression ledger` statement
reads **live** sibling lanes through the `$W/fleet/*-shokunin` symlinks, so its `REGRESSION: PASS (cases=9 passed=9` line is
a function of concurrent sibling state, not of the lane clone. The `retained invocation-context gate` statement writes
untracked receipts into its cwd: after my sweep `git -C $W/clone status --porcelain` →
`?? .ufo/evidence/round-15/attempt-4/`, `?? .ufo/evidence/round-15/verification-4.json` (harmless in the counter's throwaway
clone; the statement is not read-only on its cwd).

## Cross-check with the counter itself at CONTENT (observed, not a verdict)

`python3 .ufo/evidence/round-46/calibration/measure.py --lane <lane> --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
--base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --work /tmp/tameshi-r46-T46ReobsC/work-c1` → exit 0, all 22 lines
MATCH, summary:
```
C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 append_only=1 total=0 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C1_R46_PASS=true
```
Identical to my independent tally (22/22 MATCH) and to the SCORECARD's `total=0` after cell. The deciding run remains
the L1's.

## Not run (out of this seat's item)

- The deciding run of any counter as a verdict; the C2/C3 counters; `no-harm.sh`; any build/lint/format gate (the parent
  owns post-integration gates).
- I did not edit `statements.json`, `SCORECARD.md`, the counter or any other lane file; this report is the only write.

## Retained evidence

`/tmp/tameshi-r46-T46ReobsC/`: `run.py`, `run.log`, `summary.json`, `obs/<id>.{out,err,meta}` (22 statements),
`rerun-{repeat-control,pin-disposition,witness-metadata}.{out,err}`, `counter-at-content.stdout`, `calibration-at-base.out`,
`SCORECARD-content.md`, `SCORECARD-freeze.md`, `regression-wd/`, `work-c1/` (counter's own clone), `clone/` and
`fleet/tameshi-shokunin` (detached at CONTENT).
