# T53W1Read12 — cold-read of `### Reading a receipt — the discipline`

- Section heading: `### Reading a receipt — the discipline`
- Content commit (C\*): `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Section line range at C\*: `SKILL.md:967-1010` (next heading, `## The re-sweep cadence and the six-case confidence statement (round 8, measured)`, at `:1012`; blank line `:1011` stripped as trailing whitespace)
- `section_sha256` = `09151f506e87add7fcf41ad5bff76c92c371e870b53b2cc1eec26d9db14431c5` (UTF-8, surrogateescape; heading line through last non-blank line, joined with `\n`, no trailing newline)
- Findings: **1** (stale count)

All reads below are of git objects at C\* (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C*:SKILL.md`), never the working tree; the two selftest executions used copies of the blobs written into scratch (`/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read12`, removed after the run).

## Checks run

Split reproduction (fence-aware heading scan, `^#{1,3}(\s|$)` outside ``` fences):

```
matches: [(967, '### Reading a receipt — the discipline')]
range: 967 1011 lines_incl: 44 sha: 09151f506e87add7fcf41ad5bff76c92c371e870b53b2cc1eec26d9db14431c5
lastline: '   fixture-mode default and is exercised by the selftest only.'
```

Cross-check against the raw object (`sed -n '960,1015p' | nl`): heading at 967, next heading at 1012, last non-blank section line at 1010 — the split matches the heading's line range.

Instrument at C\*:

```
git show C*:tools/mutate-and-run.sh | sha256sum
977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
```

C\* `--selftest` (exact C\* bytes in scratch, `TMPDIR` under scratch, cwd = scratch):

```
MUTATE_SELFTEST: 107/107 pass
VERDICT: PASS
rc=0   (5.5 s)
```

Round-7 tool blob `9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh` (content sha256 `cf41efaa…`), same run shape:

```
MUTATE_SELFTEST: 67/67 pass
VERDICT: PASS
rc=0   (5.0 s, 67 `PASS` lines)
```

Both runs were hermetic: `git -C <lane> status --porcelain` snapshots taken before/after the second run are identical (`NO_REPO_CHANGE`); only pre-existing L1/other-seat entries were present.

## Finding 1 — stale selftest tally (class: stale count)

Verbatim quote from the section (item 7), byte-exact including leading spaces:

```
`bash tools/mutate-and-run.sh
   --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 at tool
   sha256 `cf41efaa…`
```

Asserted as an exact substring of the section bytes at C\* (single occurrence).

Why it fails at C\*: the arrow names the command a reader runs at C\* (`bash tools/mutate-and-run.sh --selftest`). At C\* that file's content sha256 is `977de470…` (not `cf41efaa…`) and the command prints `MUTATE_SELFTEST: 107/107 pass` — measured above. `67/67` is a genuine receipt for the round-7 blob (`9f1d3c3`, content sha `cf41efaa…`, rc 0, 67 `PASS` lines), so the figure is history, not fabrication; the failure is that the arrow is undated and the only qualifier is a content sha a cold reader cannot map to "not the tree's file", while the section's own round-52 parenthetical (`107/107` at `977de470…`) already contradicts the primary tally. A reader who runs the section's command therefore sees a disagreement with the section's first receipt. (Same defect round 52 measured as its F3; that round's fix annotated the figure instead of updating it, so the primary tally is still stale at C\*.)

## Holds (pointers verified against C\* bytes / objects)

1. **Block field list (item 1).** All named fields are emitted at C\*: `REGRESSION_TOOL` (`tools/mutate-and-run.sh:1442`), `REGRESSION_DATE` (`:1443`), `REGRESSION_BAND` (`:1444`), `REGRESSION_EXPECT` (`:1446`), `REGRESSION_PIN` per leg (`:1302`/`:1305`), `REGRESSION_SWEEP` per leg (`:1324`), `REGRESSION_TABLE` (`:1392`), `REGRESSION_CASE` (`:1396`/`:1400`), `REGRESSION_DEFECT` (`:1357`, `:1360`, `:1371`), `REGRESSION_WORKDIR` (`:1394`), closing line (`:1540`).
2. **PASS is exact for ledger legs (item 2).** `regression_case_git` passes tolerance `0 0` to every ledger leg (`:1411-1414`); the case PASS line is `printf 'REGRESSION_CASE %s: PASS (band: killed-delta<=%s flips<=%s inconclusive=0 defects=%s)'` (`:1396`), and the table line carries `match=%s/%s … flips=%s` (`:1392`). `D is 15 for checklist-run, 10 for other current legs` matches the tables at C\*: `TABLE_CHECKLIST` holds 15 entries (`:638`), every other `TABLE_*` holds 10 (`:634-637`, `:639-643`); the leg inventory is ten (`:1459-1504`, `nlegs=10` at `:1510`), consistent with the milestone chain `N=8/9/10` (runner comment `:2013`: "r16 adds leg 7, r18 leg 8, r26 leg 9 and r51 leg 10"). The T7-1 instance is explicitly dated (`2026-10-14`, four legs, `match=10/10`), matching `reports/r7-aud-t7.md` §3 F3 (all 4 PASS) and `plans/round-7.plan.md:11-15`.
3. **FAIL names its rows (item 3).** Emitter at C\*: `REGRESSION_TABLE … match=… flips=…` (`:1392`), `REGRESSION_DEFECT <leg> <id>: measured=… recorded=…` including the `ABSENT` arms (`:1357`, `:1371`), case FAIL at `:1400`. Note the exact FAIL text carries a log tail — `REGRESSION_CASE %s: FAIL (out of band:%s; log: %s)` — so the section's js-kimi-census row is a truncation of the emitted line (the source report writes the tail as `flips=1…`); the rows it quotes (`D1: measured=KILLED recorded=SURVIVED`, `match=9/10 … flips=1`, `killed-delta=1 flips=1`) are internally consistent with the arithmetic at `:1382-1387`, so I record this as a hold, not a finding. The bracketed round-52 correction of the volatile `/tmp/w7-tameshi-1/flip-run.out` path is accurate: that path is not present, `reports/r7-aud-t7.md` §3 F4 (line 111 at C\*) carries the flip mechanism and rows, and `tools/mutate-and-run.sh:2010` at C\* is the selftest assertion `grep -qF 'REGRESSION_CASE fixture: FAIL (out of band: killed-delta=1 flips=1;'` — the mechanism the bracket claims is corroborated there.
4. **SETUP is not a verdict (item 4).** C\* selftest asserts pin mismatch → SETUP exit 2 (`:1730`, `:1848`), unresolvable revision → SETUP exit 2 (`:1856`), missing target → SETUP exit 2 (round-52 receipt line `PASS regression missing target is SETUP (exit 2)`), and the SETUP closing line is separate from FAIL (`:1526`, `:1535`).
5. **The ledger proves the instrument (item 5).** `corpus/knowledge/fleet-kill-rate-ledger.md` exists at C\* and states the pin discipline (`:14` at C\*: "and a rate is never implied to hold at a later revision."), consistent with the section.
6. **Attesting a sibling's claim (item 6).** `plans/round-7.plan.md:11-15` at C\* is the round-7 attestation leg: "is ATTESTED read-only: reproduced by tameshi from its pins, or its missing piece named. The lane operates; tameshi attests." — the pointer and the "sibling's note is never edited" rule hold.
7. **Selftest coverage claims of item 7.** Beyond the tally, every named arm exists at C\*: git-materialized replay at exact tolerance (`:1830`), drifted working tree not moving a git-pinned leg (`:1840`), pin mismatch / unresolvable revision as SETUP (`:1848`, `:1856`), single flipped entry failing loudly (`:2007`).
8. **Fixture-mode tolerance sentence.** `BAND_KILLED=1` / `BAND_FLIPS=1` (`:196-197`) are the defaults applied only when the tolerance args are absent (`:1240-1241`), while ledger legs pass `0 0` (`:1413`) — "remains the fixture-mode default and is exercised by the selftest only" holds.
9. **Round-52 parenthetical.** `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out` exists at C\* (`:108-109`: `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS`) and the runner sha `977de470…` is the C\* tool content sha (verified above); the parenthetical is a live receipt.

No scratch-directive violation: the only `/tmp` mention in the section is inside the historical negative-run quote and is explicitly bracketed as gone at round 52.

## Tooling notes

No installs or upgrades were performed. Everything used (`git`, `python3`, `bash`, `sha256sum`, `diff`) was already present. Scratch `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read12` was used for the section extraction and both selftest runs, and removed before yielding; no writes were made outside `.ufo/waves/round-53/w1/T53W1Read12.{json,md}` and that scratch dir.
