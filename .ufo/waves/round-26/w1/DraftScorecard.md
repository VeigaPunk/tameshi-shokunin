# DraftScorecard — two append-only SCORECARD blocks for round 26

Seat: `TameshiR26.DraftScorecard` (scribe, leaf member). Wave 1 of round 26.
Judged on: calibration, depth.
Frozen contract: `.ufo/evidence/round-26/contract.json`, committed at lane
revision `622d31d90b1fbc55c56e91a2b012bc18d6f1421a` (base
`d4140796f4e48e8ec81b793facba73fbd03b4443`).
Scope note: the L1 TameshiR26 is the sole integrator of lane files. This seat
drafted the text only; it did **not** append anything to `SCORECARD.md`, did not
edit any production file, and did not run any gate inside the lane.

## Verdict

1. **Both blocks are drafted and both are append-only** (zero deletions), in the
   house style of the round-24 and round-25 sections (claim bullets with counter,
   before value, target and bounds; a routed-item table; a capabilities table; a
   measured-results table whose after cells are `<AFTER>`).
2. **The draft demonstrably closes the C2 counter's item R25-SPOT-2.** With the
   draft appended to a scratch clone at the integration revision, the frozen
   counter reads `C2_ITEM R25-SPOT-2: RESOLVED` and `C2_RECORD: mismatches=0/3`,
   exit 0. Without the draft, the same clone reads
   `C2_ITEM R25-SPOT-2: MISMATCH (SCORECARD after round-25 results lacks
   'amendment 3'; SCORECARD after round-25 results lacks
   'before_any_after_measurement')` and `mismatches=1/3`, exit 1. The three
   required literals — "amendment 3", "77302fa", "before_any_after_measurement" —
   are present in the appended text and in the SCORECARD tail after the round-25
   measured-results heading, which is exactly the region the counter reads.
3. **The C1 counter is unaffected by this seat's text** (it reads only
   `tools/mutate-and-run.sh`). It reads `recorded_cases=9 wired_legs=9
   depth_score=9`, exit 0, at the integration revision `a08e85c`, and
   `recorded_cases=8 wired_legs=8 depth_score=8`, exit 1, at the base. Both
   before values are byte-identical to the frozen receipts
   `.ufo/evidence/round-26/c1-before.stdout` and `c2-before.stdout`.
4. **Every number in the draft is read from an artifact, not asserted.** The
   "before" values come from the frozen `c1-before.stdout` / `c2-before.stdout`;
   the sweep figures from `sweep/sweep.txt` and `sweep/results.tsv`; the
   regression and interop companion figures from the committed
   `cite-check/regression-worktree.stdout` and `after/mte-check-a08e85c.stdout`.
   The 10/10 prediction hold was recomputed here from `predictions.json` against
   `results.tsv`, not copied from a commit message.
5. **The L1 integrated its own wording of both blocks before this draft was
   finished, so the drafted text was never integrated.** The lane's
   `SCORECARD.md` is the L1's, not this seat's; `git status --porcelain
   SCORECARD.md` is empty for this seat. The landed text at `d2206cd` does
   satisfy the same requirement: the frozen counter reads `mismatches=0/3`,
   exit 0, and all three required literals are present in the SCORECARD tail
   after the round-25 measured-results heading. Two smaller differences between
   the landed text and this draft are recorded under *Landing status observed
   after this draft was written*, because the drafted text would otherwise be
   lost with them.

## The two blocks (fenced text, as requested)

### Block 1 — `## Round 26 — ninth recorded case and round-25 record repair (2026-10-22)`

```text
## Round 26 — ninth recorded case and round-25 record repair (2026-10-22)

Attempt 1, L1 TameshiR26 (fresh identity). Two claims on distinct axes, frozen in
`.ufo/evidence/round-26/contract.json` at `622d31d90b1fbc55c56e91a2b012bc18d6f1421a`
before any mutant of the ninth leg ran and before any edit to the files the C2
counter reads; base `d4140796f4e48e8ec81b793facba73fbd03b4443`.

- **C1 depth, learning (ninth recorded mutation case).** The ninth recorded
  mutation-ledger leg `js-cite-check` is kumitate
  `scripts/cite-check.mjs` at rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`
  (blob sha256 `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`,
  2537 lines). The pre-registered spec
  (`.ufo/evidence/round-26/cite-check/cite-check.defects.spec`) and the
  predictions (`.ufo/evidence/round-26/cite-check/predictions.json`, 5
  kill-aimed and 5 hole-aimed) were committed before the first mutant ran. The
  suite is the gate's own hermetic group, `env -i` `node "$MUTANT" --selftest`
  (62 hermetic cases at the pin). Counter
  `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE_AT_REV`; before
  `C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8`, exit 1, at base
  (`.ufo/evidence/round-26/c1-before.stdout`, `before-rev.txt`); target
  `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`, exit 0. Scorecard
  command D (`SCORECARD.md:72-73`) then reads `recorded_cases=9 depth_score=9`,
  so numeric depth moves 8 → 9 by one recorded case. The runner now carries nine
  legs and `tools/mte-interop.py` now judges nine.
- **C2 calibration, record repair (round-25 record mismatches).** The population
  is the three routed items 1-3 of the round-25 outside spot-check
  (`corpus/lessons/round-25-verifier-spotcheck.md:189-199`), three fixed labels
  `R25-SPOT-1..3`; each label is a mismatch between what the lane's own record
  says and the repo bytes at the revision. Counter
  `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE_AT_REV`; before
  `C2_RECORD: mismatches=3/3`, exit 1, at base
  (`.ufo/evidence/round-26/c2-before.stdout`); target `C2_RECORD: mismatches=0/3`,
  exit 0. Numeric calibration stays 8 (lane cap): this is a record repair, not a
  numeric move.

Routed-item rows for C2 (one per label; read by the counter):

| Label | Item | State | Repair | Evidence |
|---|---|---|---|---|
| R25-SPOT-1 | `tools/mte-interop.py` returns verdicts but has no registry row | dispositioned | two active registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9) naming the tool in `argv`, plus a `tools/mte-interop.py` row in the `SKILL.md` tool table | `tools/registry.json`; `SKILL.md`; landed `a08e85c5d7f899e8a5992e20517edb1a380d79eb` |
| R25-SPOT-2 | the round-25 SCORECARD record and the round-25 lesson omit amendment 3 | dispositioned by this wave's appends | the Round 25 correction below names amendment 3, `77302fa` and `before_any_after_measurement`; the lesson gains the same correction after its `## Claims` heading | this section; `corpus/lessons/round-25.md` `## Correction (round 26)` |
| R25-SPOT-3 | `corpus/knowledge/mte-report-interop.md` `verified-at` names a run of a different tool build | dispositioned | the `verified-at` line now names the tool sha256 at the measured revision and a named selftest receipt carrying the same N/N | `corpus/knowledge/mte-report-interop.md`; `.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout` |

| capabilities addition | What it can now do | Evidence | First-working round |
|---|---|---|---|
| none added in round 26 | no new capability: the round-25 `mutation report interop` capability is unchanged. What round 26 adds is its registration — the tool `tools/mte-interop.py` now has active registry rows `mte-interop-selftest` (17/17) and `mte-interop-check` (9/9) in `tools/registry.json` and its own row in the `SKILL.md` tool table, which closes routed item R25-SPOT-1 | `tools/registry.json`; `SKILL.md`; `corpus/lessons/round-25-verifier-spotcheck.md:189-192` | 25 (row unchanged; the registration is the round-26 repair) |

Measured results are appended below only after execution.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 ninth recorded case `js-cite-check` | depth | `recorded_cases=8 wired_legs=8 depth_score=8`, exit 1 at `d414079` | `<AFTER>` | `<AFTER>` (numeric depth 8 → 9, one recorded case) | `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE_AT_REV` | `<AFTER>` | `.ufo/evidence/round-26/c1-before.stdout`; `after/` | `<AFTER>` |
| C2 round-25 record repair | calibration | `mismatches=3/3`, exit 1 at `d414079` | `<AFTER>` | `<AFTER>` (numeric calibration stays 8; record repair) | `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE_AT_REV` | `<AFTER>` | `.ufo/evidence/round-26/c2-before.stdout`; `after/` | `<AFTER>` |

Bounds. The C1 counter checks that the leg is recorded and wired in the runner
(spec heredoc, replay call, leg-check tuple, and the named table's defect and
KILLED counts); it does not read the embedded spec, the pinned blob or the sweep
result, and it does not run the runner. Whether the recorded table equals a real
sweep is carried by the regression companion, not by the counter. The C2
population is three fixed labels; items 4 and 5 of the same routing are
dispositioned in the lesson and the report, not counted here. The C1 learning
claim rests on the recorded leg and its sweep, not on a score: 5 of 10 killed is
a kill rate, and the five survivors are recorded holes in the gate's suite, not
defects in the lane's own gates.

No-harm companions for the ninth leg, both observed at the integration revision
`a08e85c5d7f899e8a5992e20517edb1a380d79eb`: the runner's own regression replay
is `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0
flips=0)` with the `js-cite-check` row `REGRESSION_CASE js-cite-check: PASS`
(`.ufo/evidence/round-26/cite-check/regression-worktree.stdout`), and the interop
counter is `MTE_INTEROP: PASS legs_conforming=9/9`, exit 0, with every leg
`per_mutant=ok failed=none`
(`.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`; selftest 17/17 in
`.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout`). The standalone sweep
of the pre-registered spec against the pinned blob killed 5 of 10 and held all 10
verdict predictions (`.ufo/evidence/round-26/cite-check/sweep/sweep.txt`,
`results.tsv`).
```

### Block 2 — `### Round 25 — correction (appended in round 26)`

```text
### Round 25 — correction (appended in round 26)

Appended 2026-10-22; the Round 25 section above is not rewritten. Routed by
`corpus/lessons/round-25-verifier-spotcheck.md:193-196`.

The Round 25 header above names amendments 1 (`c9ff09f`) and 2 (`09dc114`) only.
Amendment 3 also precedes the recorded after-measurement: amendment 3 is
`.ufo/evidence/round-25/contract-amendment-3.json`, committed in `77302fa`
(`77302fa8f79144d06c1d2d2e2d2898c44b459bda`, 06:26 −03), and the recorded after
receipts arrive in `154bf4d` (06:35 −03) — they were produced by the
amendment-3 bytes, because the `MTE_WORKDIR` line, the seventeenth selftest case
`narrow-score-delta`, and c1-pins P5's exact row shape are all amendment-3
additions (`corpus/lessons/round-25-verifier-spotcheck.md:82-95`).

What amendment 3 added, read from
`.ufo/evidence/round-25/contract-amendment-3.json`:

- `c1-pins.py`: "P5 requires the exact row shape `| R23-ROUTED-n | dispositioned |`".
- `tools/mte-interop.py`: the leg set and table set must equal the eight ledger
  legs (else SETUP); tar members must be relative regular files or directories
  under `package/`; a node timeout gives SETUP; node presence is checked before
  the sweep; `MTE_WORKDIR` is printed; selftest case `narrow-score-delta`
  (17 cases).
- Pinned bytes: `c1-pins.py` sha256 `7bc1929fd4c291bbc7b37ae6a40dc3f80a5491a1b5bc08f5dceb72c29752f440`,
  `tools/mte-interop.py` sha256 `8269b82f213e094ffd30adc20b20e28b1f67764d2eccb089983eb9dc546eb02c`.
- It amends `.ufo/evidence/round-25/contract.json` and changes no target, no
  claim population and no byte of the frozen counter (`c1_input_sha256_unchanged:
  true`); each change only adds a refusal or a selftest case, which makes a pass
  harder, not easier.

Limit on the flag `before_any_after_measurement: true` in that JSON: it is true
for the L1's recorded after receipts, and it does not cover seat probes. Wave
seats had already run the C2 counter at PASS 8/8 at `c9ff09f` and `09dc114`,
under the weaker ruler and before amendments 2 and 3
(`.ufo/waves/round-25/w1/C2LiveCheck.md`; `corpus/lessons/round-25-verifier-spotcheck.md:82-95`).
Neither amendment moved a target, a population or the frozen counter's bytes, so
those earlier passes are not post-hoc narrowing of the recorded
after-measurement; the flag is read as scoped to the L1's receipts, and the seat
probes are named here so the record does not overstate it.
```

## Evidence (every command observed in this session)

Read-only git everywhere (`GIT_OPTIONAL_LOCKS=0`); no `jj` command was run in
any repository; no git write command was run in the lane.

### 1. The two frozen before receipts (read, not recomputed)

`.ufo/evidence/round-26/c1-before.stdout` (verbatim, tail):

```
C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8
exit=1
```

`.ufo/evidence/round-26/c2-before.stdout` (verbatim, tail):

```
C2_ITEM R25-SPOT-1: MISMATCH (no active registry.json row runs tools/mte-interop.py; no SKILL.md table row for tools/mte-interop.py)
C2_ITEM R25-SPOT-2: MISMATCH (SCORECARD after round-25 results lacks 'amendment 3'; SCORECARD after round-25 results lacks 'before_any_after_measurement'; lesson after ## Claims lacks 'amendment 3')
C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=8269b82f213e; no named .stdout receipt at the revision carries the verified-at selftest count)
C2_RECORD: mismatches=3/3
exit=1
```

`.ufo/evidence/round-26/before-rev.txt`: "measured at
d4140796f4e48e8ec81b793facba73fbd03b4443 (lane working tree clean at that tip;
jj-lane.sh state ahead=0 tracked=0 untracked=0)".

### 2. Independent re-derivation of both before values (scratch clone at base)

```
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/DraftScorecard-r26-base
$ git -C /tmp/DraftScorecard-r26-base checkout -q --detach d4140796f4e48e8ec81b793facba73fbd03b4443
$ python3 .ufo/evidence/round-26/c1-measure.py --repo .
C1_LEG js-kimi-census: WIRED
C1_LEG bash-surface-census: WIRED
C1_LEG bash-tsukuroi-census: WIRED
C1_LEG bash-mado-verify: WIRED
C1_LEG bash-checklist-run: WIRED
C1_LEG js-claims-check: WIRED
C1_LEG js-round-gate: WIRED
C1_LEG js-sources-check: WIRED
C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8
EXIT=1

$ python3 .ufo/evidence/round-26/c2-measure.py --repo .
C2_ITEM R25-SPOT-1: MISMATCH (no active registry.json row runs tools/mte-interop.py; no SKILL.md table row for tools/mte-interop.py)
C2_ITEM R25-SPOT-2: MISMATCH (SCORECARD after round-25 results lacks 'amendment 3'; SCORECARD after round-25 results lacks 'before_any_after_measurement'; lesson after ## Claims lacks 'amendment 3')
C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=8269b82f213e; no named .stdout receipt at the revision carries the verified-at selftest count)
C2_RECORD: mismatches=3/3
EXIT=1
```

Byte-identical to the frozen receipts. (The counters were copied into the scratch
clone because `.ufo/evidence/round-26/` does not exist at the base revision.)

### 3. The draft closes R25-SPOT-2 (scratch clone at the integration revision)

```
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/DraftScorecard-r26-clone
$ git -C /tmp/DraftScorecard-r26-clone checkout -q --detach a08e85c5d7f899e8a5992e20517edb1a380d79eb
$ # sibling seats' uncommitted lesson + knowledge edits copied in; SCORECARD.md untouched
$ python3 .ufo/evidence/round-26/c2-measure.py --repo .
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: MISMATCH (SCORECARD after round-25 results lacks 'amendment 3'; SCORECARD after round-25 results lacks 'before_any_after_measurement')
C2_ITEM R25-SPOT-3: RESOLVED
C2_RECORD: mismatches=1/3
EXIT=1
$ # append the two drafted blocks
$ python3 .ufo/evidence/round-26/c2-measure.py --repo .
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: RESOLVED
C2_ITEM R25-SPOT-3: RESOLVED
C2_RECORD: mismatches=0/3
EXIT=0
```

The delta is caused by this seat's text alone: the two runs differ only in
`SCORECARD.md`. The `git diff --numstat` for the appended file reads `118  0`
— append-only, zero deletions.

Literal check on the region the counter reads (the SCORECARD tail after
`### Round 25 — measured results (TameshiR25)`):

```
amendment 3 True
77302fa True
before_any_after_measurement True
```

### 4. C1 counter at the integration revision (unaffected by the draft)

```
$ python3 .ufo/evidence/round-26/c1-measure.py --repo .
C1_LEG js-kimi-census: WIRED
…
C1_LEG js-cite-check: WIRED
C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9
EXIT=0
```

### 5. The pin, recomputed from the sibling repo's object store (read-only)

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | wc -l
2537
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  -
```

Matches the contract's `blob_sha256` and the `2537 lines` in the draft.

### 6. The sweep and its 10/10 prediction hold (recomputed here)

```
$ python3 -c "…"   # predictions.json vs sweep/results.tsv
predictions 10 held 10
```

and from `.ufo/evidence/round-26/cite-check/sweep/sweep.txt`:
`MUTATE: DONE (target=cite-check.mjs defects=10 killed=5 survived=5
inconclusive=0 kill-rate=50%)`, `CONTROL: GREEN (exit=0 … 62/62 cases passed
(hermetic))`, `MUTATE_RESTORE: OK`.

### 7. Round-25 amendment-3 facts (read from the artifact and the git history)

`.ufo/evidence/round-25/contract-amendment-3.json` (verbatim keys):
`"number": 3`, `"before_any_after_measurement": true`,
`"c1_input_sha256_unchanged": true`, `"amends":
".ufo/evidence/round-25/contract.json"`, the two `changes` entries and the two
`tool_sha256` pins quoted in the draft.

Commit ordering and clock times, from `git show -s --format='%ci %s'`:

```
c9ff09f -> 2026-10-22 05:18:39 -0300 round-25: mte-interop --fleet-root stages sibling lanes …
09dc114 -> 2026-10-22 05:35:24 -0300 round-25: contract amendment 2 — stronger rulers …
77302fa -> 2026-10-22 06:26:29 -0300 round-25: wave reports, dead-falsifier disposition, …, amendment 3
154bf4d -> 2026-10-22 06:35:54 -0300 round-25: after receipts, emitted reports, measured SCORECARD rows …
```

`git show --stat 77302fa` lists `.ufo/evidence/round-25/contract-amendment-3.json`
among the added files, so amendment 3 really is in `77302fa`; the recorded after
receipts are in the later `154bf4d`. This is what the draft asserts.

### 8. The seat probes the draft names

`.ufo/waves/round-25/w1/C2LiveCheck.md`, section "Verdict" item 1 and section 3:
the counter at the pinned lane revision `c9ff09fb…` (commit `c9ff09f`) printed
`MTE_INTEROP: PASS legs_conforming=8/8`, exit 0, twice, and the report's
"Nets:" paragraph names the same `8/8` at `c9ff09f`. The 09dc114 half is the
lesson's own statement, `corpus/lessons/round-25-verifier-spotcheck.md:88-95`:
"Wave seats had already run the C2 counter at PASS 8/8 at `c9ff09f` and
`09dc114`". Both are cited in the draft.

### 9. Registration facts behind the capabilities-table note

```
$ git show a08e85c:tools/registry.json | grep -c "mte-interop"
4
$ git show a08e85c:SKILL.md | grep -c '^| `tools/mte-interop\.py` |'
1
```

`tools/registry.json` at `a08e85c` carries `mte-interop-selftest`
(`MTE_SELFTEST: 17/17 pass`) and `mte-interop-check`
(`MTE_INTEROP: PASS legs_conforming=9/9`), both `status: active`, tagged
`new-r26`, sourced to `corpus/lessons/round-25-verifier-spotcheck.md:189-192
(routed item 1)`. `SKILL.md:2101` carries the `| \`tools/mte-interop.py\` |`
table row. The round-25 capabilities row is therefore unchanged and only its
registration is new — the draft's capabilities table says exactly that.

## Gates this seat exercised

- `python3 .ufo/evidence/round-26/c1-measure.py --repo .` at the base revision
  → `depth_score=8`, exit 1; at the integration revision → `depth_score=9`,
  exit 0. Run only in scratch clones.
- `python3 .ufo/evidence/round-26/c2-measure.py --repo .` at the base revision
  → `mismatches=3/3`, exit 1; in the scratch clone without the draft → `1/3`,
  exit 1; with the draft → `0/3`, exit 0.
- `git diff --numstat -- SCORECARD.md` in the scratch clone → `118 0`
  (append-only).
- Read-only `git show`/`git log` in the lane and in the kumitate sibling; one
  `git clone --no-hardlinks` of the lane into `/tmp` for the two scratch clones.

Not run by this seat (out of scope, and each would be a lane-level or
wave-2 job): the runner's own `--regression`, the `mte-interop.py --check`
live counter, the registry check, the sources census, and the cold-read monitor.
Their figures quoted in the draft are read from the committed receipts named in
the draft, not from a run of mine.

## Touched surfaces

- Written by this seat: `.ufo/waves/round-26/w1/DraftScorecard.md` (this file)
  only.
- Not written by this seat: `SCORECARD.md`, `corpus/lessons/round-25.md`,
  `corpus/knowledge/mte-report-interop.md`, `corpus/SOURCES.md`,
  `tools/*`, `SKILL.md`, and every other lane file. The three corpus files
  listed show as modified in the lane's working tree; those edits belong to
  sibling seats (DraftLesson25Correction and the sources/knowledge seats), and
  this seat copied them read-only into a scratch clone to test the counter.
- Scratch, outside the repo, disposable: `/tmp/DraftScorecard-r26` (working copy
  of the lane tree + the drafted append text at `append.md`),
  `/tmp/DraftScorecard-r26-clone` (clone at `a08e85c` + draft appended),
  `/tmp/DraftScorecard-r26-base` (clone at `d414079`).

## Landing status observed after this draft was written (recorded verbatim)

While this seat was drafting, the L1 integrated **its own** wording of the two
blocks. The lane's `SCORECARD.md` was therefore **not** edited by this seat at
any point; `git status --porcelain SCORECARD.md` is empty and the file's
content is the L1's.

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -3
d2206cd round-26: SCORECARD measured results for C1 and C2 at 40a12bf, after receipts
40a12bf round-26: content landing — ninth-case entry, S088/S089, SKILL survivor table and count updates, registry source fix, QUALITY 51-52, PROVINCE/README appends, round-25 amendment-3 corrections, refreshed verified-at, SCORECARD/LOG/lesson, wave-1 evidence
a08e85c round-26: ninth ledger leg js-cite-check (5/10, 10/10 verdict predictions), runner and interop wired to nine legs, mte-interop registry rows and SKILL row, sweep evidence
```

Counters at the L1's landing commit, in a scratch clone:

```
$ git -C /tmp/DraftScorecard-r26-landing checkout -q --detach d2206cd
$ python3 .ufo/evidence/round-26/c2-measure.py --repo .
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: RESOLVED
C2_ITEM R25-SPOT-3: RESOLVED
C2_RECORD: mismatches=0/3
EXIT=0
$ python3 .ufo/evidence/round-26/c1-measure.py --repo . | tail -1
C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9
```

The required literals are present in the landed SCORECARD tail after
`### Round 25 — measured results (TameshiR25)`:
`amendment 3` True, `77302fa` True, `before_any_after_measurement` True.
The landed record also carries the measured after-values at `40a12bf` with the
receipts `after/c1-measure-40a12bf.stdout`, `after/commandD-40a12bf.stdout` and
`after/c2-measure-40a12bf.stdout`, all present in the tree.

Two differences between the landed text and this draft, recorded as observed and
not edited by this seat:

- The landed `### Round 25 — correction (appended in round 26)` block does
  **not** cite `.ufo/waves/round-25/w1/C2LiveCheck.md`
  (`git show d2206cd:SCORECARD.md | grep -c C2LiveCheck` → `0`); it cites
  `round-25-verifier-spotcheck.md:88-95` instead of `:82-95`. This draft cites
  both the seat report and the wider `:82-95` span, which is the span the
  assignment named.
- The landed block names the amendment-3 additions in prose ("the interop leg
  set must equal the ledger legs; tar members are contained; a node timeout is
  SETUP; `narrow-score-delta` makes the selftest 17 cases") without the two
  pinned sha256 values this draft quotes from
  `.ufo/evidence/round-25/contract-amendment-3.json`, and it does not state the
  `c1_input_sha256_unchanged: true` key.

The two differences are additions of detail, not corrections: the landed text
satisfies the counter and the three required literals. They are recorded here
because the drafted text was never integrated and would otherwise be lost.

## Findings for the L1

1. **The `<AFTER>` cells are the integrator's to fill.** The draft's measured
   table carries `<AFTER>` in the After, Delta, Measured commit and Verdict
   columns, as instructed. The after-measurement must be taken at a real
   measured commit and the values then pasted verbatim; the draft does not
   pre-fill them. **This has since been done by the L1**: the landed
   `### Round 26 — measured results (TameshiR26)` table at `d2206cd` fills both
   rows with the measured commit `40a12bf34f34977a5789e81b930303b97c4038d1`
   and the receipts `after/c1-measure-40a12bf.stdout`,
   `after/commandD-40a12bf.stdout` and `after/c2-measure-40a12bf.stdout`.
2. **The C2 counter's item 3 depends on the knowledge-entry refresh and the
   after receipts.** At the time of this draft, `corpus/knowledge/mte-report-interop.md`
   was modified in the working tree (not committed) to name the tool sha256
   `193ea6e32f89…` at `a08e85c` and the receipt
   `.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout`, and that receipt
   was untracked. Item 3 read `RESOLVED` in the scratch clone only because both
   were copied in. **Both have since landed** — `git show d2206cd:corpus/knowledge/mte-report-interop.md`
   carries the refreshed `verified-at` line and
   `.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout` is in the tree —
   and the counter at `d2206cd` reads `R25-SPOT-3: RESOLVED`.
3. **`corpus/knowledge/mutation-case-kumitate-cite-check.md` was absent at the
   integration revision and now exists.** `git show a08e85c:corpus/knowledge/mutation-case-kumitate-cite-check.md`
   fails ("ABSENT at a08e85c") while `SKILL.md` and the new `SOURCES.md` rows
   S088/S089 already pointed at it; `git show d2206cd:corpus/knowledge/mutation-case-kumitate-cite-check.md`
   succeeds, and `corpus/SOURCES.md` at `d2206cd` carries both S088 and S089.
   The dangling pointer existed for the span between `a08e85c` and `40a12bf` and
   is now closed.
4. **The C1 counter is a textual wiring check, not a measurement of the sweep.**
   Seat `MutateC1Counter` reports eight weakenings of the `js-cite-check` leg
   that the counter still calls WIRED at `depth_score=9`. The draft's "Bounds"
   paragraph states this limit in the record itself, so a reader of the
   SCORECARD cannot mistake `depth_score=9` for a verified sweep. Nothing in
   the draft claims the counter runs the runner.
5. **Minor discrepancy, reported verbatim rather than smoothed: the standalone
   sweep receipt names a different runner build than the regression receipt.**
   `sweep/sweep.txt` records `MUTATE_TOOL: … sha256=d22c4025e8ce…` (the runner
   at `622d31d`), while `cite-check/regression-worktree.stdout` records
   `REGRESSION_TOOL: … sha256=fb91ef7621f5…` (the runner at `a08e85c`). The
   sweep was therefore run against the pre-integration runner bytes and the
   replay against the post-integration ones; both reproduce the same table
   (`5/10`, `match=10/10`, `flips=0`). The draft cites both receipts without
   asserting they were produced by the same build.

## Out of scope (not done by this seat)

- Appending the blocks to `SCORECARD.md` — the L1 integrates.
- Filling the `<AFTER>` cells, choosing the measured commit, and running the
  after-measurement.
- The round-26 lesson, QUALITY, PROVINCE, README, SOURCES rows, the knowledge
  entry, and the `corpus/lessons/round-25.md` correction (sibling seats).
- Any gate run inside the lane; any `jj` command; any git write command in the
  lane, in a sibling lane, or in the fleet root.

## Tooling

- Installed or updated: **nothing**. No pacman transaction (pacman is paused
  host-wide), no `uv tool install`, no release binary fetched, no service
  restarted. The tools used were the pre-installed `python3` (3.14.8) and `git`;
  no interpreter or package was added.
- Hosts touched: none.
