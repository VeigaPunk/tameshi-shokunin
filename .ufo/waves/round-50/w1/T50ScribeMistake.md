# T50ScribeMistake — round-50 `## Mistakes` draft (wave 1, seat of the L1 TameshiR50)

Item: draft the round-50 `## Mistakes` rows for `corpus/lessons/round-50.md`, primary candidate
round 49's counter selftests never reaching `measure()`, plus a second class swept from the
round-47..49 spot-checks that no `## Mistakes` table has mined. Lane tip read:
`4afb060c1d6e994d1bbb9095493b1f6b2b8344f2`. Counters probed (frozen bytes, copied, never edited):
c1 `ceee320c9ad84c89a7846fd746a072a60758a465d25ff80343fb95e0bd88ae29`,
c2 `c3da7e59abf279db2ebf165d1a8d8298295ca234cd83b49027b9cb0b1823dfe3`.
Every command and every output quoted below is in `T50ScribeMistake.receipts.txt` beside this file
(probes P0-P15, P14 corrected by P14b). Scratch `/fast/scratch/hyaku/tameshi-r50/T50ScribeMistake` deleted before yield;
no tool installed or upgraded (pacman transactions are paused host-wide and nothing was needed).

These are draft rows for the L1 to integrate; I do not decide the claim. The last column, `how the fix is
shown able to fail`, is the one the item names and round 49's four-column table did not carry.

## Draft table

| # | class | evidence pointer | captured-by | fix | how the fix is shown able to fail |
|---|---|---|---|---|---|
| 1 | `verification-blindspot` — both frozen counters' `--selftest` exercised only pure helpers, so the code that decides the round (pins, floors, score gate, total arithmetic) was certified by nothing | `.ufo/waves/round-49/w1/T49MutC1Counter.md:60` (`28 mutants — 14 killed, 14 survived`) and `:103` (`--selftest` never calls `measure()`); `.ufo/waves/round-49/w1/T49MutC2Counter.md:21` (`15 mutants: 6 killed, 9 survived`) and `:74` (`selftest()` exercises only the pure helpers … `measure`, `witness` and the frozen constants are `--selftest`-invisible); my own count at the r49 bytes: `python3` span scan of `.ufo/evidence/round-49/c1/measure.py:417-546` and `:392-426` finds 0 occurrences of `measure(`/`run_monitor`/`FLOORS`/`MONITOR_SHA` | QUALITY 17 (`corpus/QUALITY.md:77-83`, clause at `:80`: "helper-only controls are not a standalone selftest") — written in round 15 and not applied to either round-49 counter | both round-50 counters' selftests build fixture repos and call `measure()` end to end: `.ufo/evidence/round-50/c1/measure.py:289-290` names the finding in the comment, `:304` `def selftest(work)`, `:359` and `:420` call `measure(...)` (25 cases, each asserting a term/floor/cap of the returned counts and `total`); `.ufo/evidence/round-50/c2/measure.py:372-373` names it, `:421` `def selftest(lane, work)` builds a fixture lane holding the real guard and frozen generator, `:490` calls `measure(...)` against four fixture shrinkers (9 cases). Receipts committed before any seat: `.ufo/evidence/round-50/control/c1-selftest.stdout:26` `C1_R50_SELFTEST: cases=25 failed=0`, `c2-selftest.stdout:10` `C2_R50_SELFTEST: cases=9 failed=0`, both at `f87910f` | the wave-1 mutation seats `T50MutC1Counter` and `T50MutC2Counter` re-run the r49 survivor classes against the new selftests (their items name "floors, total arithmetic … panel sha pins"); credit is bound by QUALITY 93 (`corpus/QUALITY.md:1371-1381`: a kill is a `FAIL ` line, not a crash) and QUALITY 89 (`:1317-1334`: neutral mutants must survive). My wave-1 probes of the two r49 survivor classes show the fix is not decorative: `counts['fixed_short'] = 0` (r49 M11) is now killed (`SELFTEST fixed floor counted FAIL`, exit 1) and `counts['records_bad'] = 0` (c2 `records()`) is killed (`SELFTEST missing F6 records counted FAIL`, exit 1), while five analogs still survive — see Residual risks |
| 2 | `misclassification` — the round-49 generator prints a setup fault as a finding: an existing-but-unreadable guard produces `VIOLATION index=0` and `violations=1` on exit 1, the same exit a real guard violation uses, where the docstring says exit 2 | `tools/pbt-staged-id.py:41` (`2 = setup problem (bad arguments, unwritable dump, unreadable guard)`), `:982` (`if not os.path.isfile(guard):` — existence only), `:842` (`# selftest: the oracle and the classifier, without the guard (no subprocess)`); routed, never mined, at `corpus/lessons/round-49-verifier-spotcheck.md:122` (= defect R49.1 in `.ufo/evidence/round-50/c1/defects.json`); observed by my probe P11 | QUALITY 17 (`corpus/QUALITY.md:77-83`, clauses at `:79-81`: "asserts literal exits and stable finding IDs" and "Explicitly classify every nonzero exit, including usage") — the same criterion, a different clause: this is a classification fault, not a blind spot | in flight this round as routed item R49.1, seat `T50ExecGenFix` (`.ufo/waves/round-50/spec-w1.json`, milestone "C1 fix R49.1"), whose item requires "F1 (an unreadable guard must exit 2 as the docstring says …), F2 and F3 … each with a new `--selftest` case; prove each new case FAILS on the base b…"; the generator is in the round's declared tools scope (`A tools/shrink-case.py`, `M tools/pbt-staged-id.py`, `.ufo/evidence/round-50/no-harm.sh:30`) and `.ufo/evidence/round-50/no-harm.sh:32-35` pins the capability line byte-equal, so an error-path-only edit is both legal and bounded | the same command before and after, on a guard that exists and is mode 000: before, `VIOLATION index=0 exit 2, oracle expects 1` + `violations=1 counterexample=0` and exit 1 (P11); after, exit 2 with the `pbt-staged-id: …` setup line and no `VIOLATION` line — the shape P12 already produces for a missing guard; the new `--selftest` case must fail on the base bytes (the seat's own requirement) and `no-harm.sh:32-35` must still print the base capability line byte-equal (an error-path fix may not move the classes). QUALITY 17's last clause ("retain the unsupported old invocation alongside the same-command repaired result") makes the P11 output the retained half of the receipt |

## Row 1 — detail

**What happened.** Round 49 hardened two frozen counters and certified them by `--selftest`. Both
selftests stopped at the pure helpers. The r49 mutation seats measured that, in scratch, against the
lane's own bytes:

- `python3` scan of the r49 selftest spans (P14b in the receipts file): `.ufo/evidence/round-49/c1/measure.py:417-546`
  contains 0 occurrences of `measure(`, `run_monitor`, `durability_commit`, `FLOORS`, `VOLATILE`,
  `MONITOR_SHA`; `.ufo/evidence/round-49/c2/measure.py:392-426` contains 0 occurrences of `measure(`,
  `materialize`, `load_panel`, `run_generator`, `records(`.
- `.ufo/waves/round-49/w1/T49MutC1Counter.md:60` 14 of 28 mutants survive; `:103-129` lists the
  seven structural survivors (floor, VOLATILE, monitor pin, `not_holds` term, overrides gate, score
  gate) and `:120-123` names M14, dropping `+ res['not_holds']` from the total, as the one that "flips
  the claim while selftest stays green" (repeated in the summary at `:152`).
- `.ufo/waves/round-49/w1/T49MutC2Counter.md:21` 6 of 15 survive; `:74-78` says the survivors fall in
  `measure()` by construction and names `killtarget-arith` (:360), `dumplen-ge1` (:311) and
  `cx-index-ne` (:340) as load-bearing in the deciding invocation.
- The lane wrote it down as routed, not fixed: `corpus/lessons/round-49.md:101` "The C1 counter's
  selftest never calls `measure()`, so the pins, the durability probe, the floors and the total are not
  exercised by it", under "Found this round (wave-1 attacks), routed, not claimed as fixed".

**Why it is a class and not an item.** The instrument's own gate could not see the instrument's
deciding code. QUALITY 17 had named the failure mode in round 15 — "helper-only controls are not a
standalone selftest" (`corpus/QUALITY.md:80`) — and both round-49 counters, plus the round-49
generator (`tools/pbt-staged-id.py:842`, row 2 above), were built to that shape in one round. The
class returns whenever a tool's certifier is written from the same reading as the tool instead of from
its exits and its verdict.

**What closes it, and what does not.** The r50 selftests reach `measure()` through real git fixture
repos and assert the returned counts and total, so the r49 structural survivors are now inside the
detector. Measured, not assumed: P2 kills the r49 M11 analog (`fixed_short`), P8 kills the c2
`records()` check; P7 baseline 9/9 and P1 baseline 25/25.

**Residual risks the L1 must not over-claim** (all observed in wave-1 probes; the seats own the full
sweep):

| probe | single edit to the r50 counter | r50 selftest | consequence |
|---|---|---|---|
| P2 | c1 `counts['fixed_short'] = 0` (`:265`) | killed, `SELFTEST fixed floor counted FAIL`, exit 1 | r49 M11 closed |
| P8 | c2 `counts['records_bad'] = 0` (`:319`) | killed, `SELFTEST missing F6 records counted FAIL`, exit 1 | c2 records check closed |
| P3 | c1 total drops the `evidence_bad` term (`:268`) | **survives** 25/25, exit 0 | a false PASS path: an evidence fault stops counting toward `total` |
| P4 | c1 total drops the `key_miss` term (`:268`) | **survives** 25/25, exit 0 | same class, second term |
| P5 | c1 `FIXED_FLOOR = 20` → `5` (`:50`) | **survives** 25/25, exit 0 | the claim bar can be lowered silently; `line()` (`:280-285`) prints the shortfall, never the floor |
| P6 | c1 `DEFECTS_SHA256` first hex digit (`:47`) | **survives**, exit 0 | fails closed at decide time (pin mismatch ⇒ total>0), so a denial, not a false pass |
| P9 | c2 `PUBLIC_SHA256` first hex digit (`:56`) | **survives**, exit 0 | denial at decide time (`panel_invalid`), not a false pass |
| P10 | c2 `HIDDEN_SHA256` first hex digit (`:57`) | **survives**, exit 0 | denial at decide time, not a false pass |

So the fix closes "the selftest never reaches the deciding code"; it does not close "the frozen
literals that set the bar are unasserted", and it covers 12 of the 14 `total` terms but not
`evidence_bad` or `key_miss` (I did not exhaust the other 12 — a mutation seat should). Row 1's
wording, as drafted, claims only the reach, and names these as follow-ups for `T50MutC1Counter` /
`T50MutC2Counter`; the L1 decides whether to route them or let the wave-2 seat list carry them.

## Row 2 — detail

**What happened.** The round-49 generator's `main()` (`tools/pbt-staged-id.py:982`) tests
`os.path.isfile(guard)`. A guard that exists but cannot be read therefore passes the check, every case
runs the guard subprocess, the subprocess dies with `[Errno 13] Permission denied`, the oracle's
expected exit (0 or 1) does not match the observed 2, and the generator reports the mismatch as a
**counterexample** and exits 1 — the exit a real violation uses. Observed (P11):

```
$ chmod 000 guard.py
$ TMPDIR=$S/g python3 -I $S/g/pbt.py --guard $S/g/guard.py --seed 4949 --cases 2 --dump $S/g/d.jsonl
VIOLATION index=0 exit 2, oracle expects 1
VIOLATION observed_exit=2 stdout= stderr=/usr/bin/python3: can't open file '…/guard.py': [Errno 13] Permission denied
PBT_STAGED_ID: cases=1 violations=1 counterexample=0 …
exit=1
```

Control (P12): the same command on a *missing* guard already reaches the documented class —
`pbt-staged-id: guard is not a regular file: …`, exit 2. So the ladder is half-built: one setup fault
is classified, the other is not, and `tools/pbt-staged-id.py:41` promises both.

**Why it is a class.** A "found a bug" line and a "could not run" line must not share an exit. Any
consumer that reads exit 1 as "the mutant was found" — and the round-49 contract's generator semantics
do read that way — can credit a finding from a guard it never ran. The round-49 spot-check recorded
only the number (`:122`: "an unreadable guard exits 1, where the docstring says 2"); the class is the
false `VIOLATION` line and the shared exit, and it is why `tools/pbt-staged-id.py:842` (a selftest
"without the guard (no subprocess)") could not see it.

**Not a claim risk this round, as observed.** The C2 counter runs the *pinned* generator bytes
(`.ufo/evidence/round-50/c2/measure.py:194`, `GEN_REV` + `GEN_SHA256`) against a guard it writes
itself, so this fault cannot reach `C2_R50_PASS`. I did not observe it in any deciding path; the row
is a quality row.

## Sweep of the round-47..49 spot-checks

Already mined, so not re-drafted: r47 conformance defect 1 (undispatched wave) → `corpus/lessons/round-48.md`
`## Mistakes` row 2; defect 2 (seat report rewritten after landing, HEAD behind the tree) → row 7;
defect 3 (selftest tallies cited, no receipt) → row 3; defect 4 (criterion-93 falsifier has no
receipt) → row 4; defect 5 (lesson dependence sets disagree with the rows) → row 5. r48 defects 2-3
(controls scored after the deciding run, undisclosed `--only` previews) → `corpus/lessons/round-49.md`
`## Mistakes` row 1; r48 defect 5 (`pasted byte-exact` wording, lesson pointer 140-141 vs 142-143) →
round-49 row 3 plus the r48 erratum. r49 defect 4 (stale standing axis table) is landed this round at
`4afb060` ("standing axis table restated with round-49 values (routed R49.4)"). r48 defect 6 (census
W04 on the four supersession rows) and the census warnings the r47 closure printed are expected
consequences of supersession rows, not mistakes.

Two classes are unmined. I drafted the first and left the second:

1. **Setup fault consumed as a finding** (row 2). Chosen: reproducible in the tree today, a named
   criterion, an owner this round, a falsifier I could run.
2. **Hidden-panel custody residue** — `.ufo/evidence/round-49-verifier-spotcheck.md:25`: after the
   round-49 panel was revealed and committed, its external copy "remains at
   `~/.local/state/tameshi-r49/`, outside the lane … redundant". Class: a custody copy outlives the
   reveal, so a later round cannot tell a leftover from a leak, and the custody root accumulates
   panels that were secret by construction. Not drafted, for three reasons: no QUALITY criterion
   covers post-reveal custody (captured-by would be `none`), no seat owns a fix, and the red state is
   unobservable to me — my bounds forbid reading under `/home/vgpnk/.local/state/`, so I could only
   repeat the closure's sentence. A fix that would be checkable without touching the root: a
   `CUSTODY_ROOT`-parameterised check that lists round directories and refuses a pre-freeze tree whose
   root still holds a prior round's directory, plus a reveal step that records the removal (path and
   time only). Falsifier: a planted directory in a scratch custody root is refused, the same root after
   removal passes.

## Findings

1. Round 49's finding is real and was routed, not fixed: `corpus/lessons/round-49.md:101`, with the
   measurements at `.ufo/waves/round-49/w1/T49MutC1Counter.md:60,103` and
   `.ufo/waves/round-49/w1/T49MutC2Counter.md:21,74`. Shown by: `grep -n 'selftest never calls'
   corpus/lessons/round-49.md`; the span scan recorded in the receipts file.
2. Round 50 closes the reach: `c1/measure.py:304,359,420` and `c2/measure.py:421,490` call `measure()`
   on fixture repos, 25 and 9 cases, receipts at `control/c{1,2}-selftest.stdout` committed at
   `f87910f` before wave 1. Shown by: `git log --oneline -1 -- .ufo/evidence/round-50/control/c1-selftest.stdout`;
   P1/P7 baselines.
3. The closure is not vacuous and not complete: two r49 survivors die (P2, P8), five analogs survive,
   including a false-PASS term drop (P3, P4) and the claim-bar literal (P5). The mutation seats must
   report these; the row must not say "the survivors are dead".
4. The round-49 generator misclassifies an unreadable guard as a violation (P11: `VIOLATION index=0 …
   violations=1`, exit 1) against its own docstring at `tools/pbt-staged-id.py:41`, with the existence-
   only check at `:982` and the helper-only selftest at `:842`; routed at
   `corpus/lessons/round-49-verifier-spotcheck.md:122`. Fix in flight at `T50ExecGenFix`, bounded by
   `no-harm.sh:30,32-35`.
5. Two classes are unmined in rounds 47-49; the second (hidden-panel custody,
   `.ufo/evidence/round-49-verifier-spotcheck.md:25`) is left for the L1 with the reason and the
   criterion-shaped gap recorded above.
6. Both counters' frozen-literal pins are outside the new selftests (P5, P6, P9, P10). Two of those
   four fail closed, so the live risk is the floor literal, not the digests — for the L1's routing, not
   for this row's wording.

## Out of scope

No lane file edited except this report and its receipts file; no counter, contract, tool or record
touched; no deciding invocation run; no tool installed (pacman paused; `uv`/`npx` not needed). Scratch
deleted.

## Summary

- Two draft `## Mistakes` rows, five columns as the item asks: `verification-blindspot` (r49 counters' selftests never reached `measure()`; QUALITY 17 at `corpus/QUALITY.md:80`) and `misclassification` (r49 generator prints an unreadable guard as `VIOLATION`, exit 1; `tools/pbt-staged-id.py:41,982,842`).
- Row 1's fix is landed and receipted before wave 1 (`c1/measure.py:304,359,420`; `c2/measure.py:421,490`; `control/c{1,2}-selftest.stdout`, commit `f87910f`) and is shown able to fail by my probes P2/P8 plus the seats `T50MutC1Counter`/`T50MutC2Counter` under QUALITY 89/93.
- Row 1 must not claim more than reach: P3/P4 (two `total` terms dropped) and P5 (`FIXED_FLOOR` 20→5) survive 25/25 — a false-PASS and a claim-bar gap for the mutation seats.
- Row 2's fix is in flight at `T50ExecGenFix` (spec item R49.1) and bounded by `no-harm.sh:30,32-35`; its red state is my P11 output, its green state is the P12 shape.
- Sweep: rounds 47-48 defect sets are already mined in the round-48/49 tables; r49 defect 4 is landed at `4afb060`; the unmined hidden-panel custody residue (`round-49-verifier-spotcheck.md:25`) is left to the L1 with its reason.
- All probe commands and outputs: `T50ScribeMistake.receipts.txt` (P0-P15; P14 failed on a relative path and is corrected by the appended P14b). Lane copies byte-identical after the probes; no tracked change; scratch deleted.
