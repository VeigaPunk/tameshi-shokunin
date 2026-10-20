author: hyaku closure (non-author integrator, @m_opus)

# Round 16 — non-author verifier spot-check (tameshi)

Closure of lane-round tameshi r16 by the hyaku integrator of record, who did
not author the round. I judged committed bytes only: baseline
`28aeef498cc070c3183271b709bc79d344ff547a`, lane HEAD
`017a2b0c0d1a8fe513e41710416c87b9d6ef9ae9`, measured commit `09ee1d0`.
Report: `.ufo/reports/round-16/tameshi.md` (fleet repo). I executed no
lane-owned gate or selftest (PROTOCOL §Gate standard, Closure consequence).
Gate claims were checked against their committed evidence.

Driver digest (copied from the mutable `.ufo/watchdog.log`):
- `2026-10-20T10:14:09-03:00 launch tameshi round=16 pgid=11738 driver=hyaku-inline attempt=1` (log line 476)
- `2026-10-20T11:49:02-03:00 complete tameshi round=16; hyaku-inline attempt=1` (log line 482)

**Outcome: status `ok`, admitted `false` (rejected-harmed).** C1 verifies. C2
reproduces under the lane's own counting command, but its assertion fails on
one bucket. The same root cause harms operability: the round's runner edit
left the round-14 disposition gate unable to return clean at HEAD, and the
round-14 recipe went stale without being swept.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %cI' -- .ufo/reports/round-16/tameshi.md` | `tameshi-shokunin <tameshi@shokunin.local> a067c633… 2026-10-20T11:48:34-03:00` | pass. Filed after the last lane commit, `017a2b0` at 11:47:11. |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` with pointers | pass |
| Cited hashes exist and are ancestors of the branch | `git merge-base --is-ancestor <h> refs/heads/master` for 28aeef4, e69b488, c699c8c, 05a2247, 3490708, 09ee1d0, 017a2b0, 0baf52e | all `ANCESTOR` | pass |
| Pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin`; `git status --porcelain` | `state branch=master local=017a2b0… remote=017a2b0… ahead=0 behind=0 head=attached tracked=0 untracked=0`; porcelain empty | pass |
| Remote tip | `git ls-remote origin refs/heads/master` | `017a2b0c0d1a8fe513e41710416c87b9d6ef9ae9` | pass |
| Commit identity | `git log --format='%h %an' 28aeef4..refs/heads/master` | 6 round commits by `tameshi-shokunin`. `0baf52e` is by the operator (`considerthese/`) and was inherited and left untouched. | pass |
| Prompt carries the template contract | every non-placeholder line of `kimi-shokunin/templates/round-prompt.md` searched in `.ufo/prompts/tameshi-round-16.md` | 105/105 static lines present, plus hyaku addendum §6. The fleet template is byte-identical to the canonical one. | pass |
| Watchdog dispatch/complete | `grep -n "tameshi round=16" .ufo/watchdog.log` | lines 476 and 482, as in the digest above | pass |
| Tool installs | `/var/log/pacman.log`, 2026-10-20T10–11 | no transactions | consistent with the report's "none" |

The report is substantive, not a marker. No step-1 conformance defects.
Report §"Waves" says seats appended `solutionSpace` to validated payloads;
the round discloses this and I do not treat it as a defect.

## 2. Claims, re-measured

### C1 — depth 6→7 (seventh recorded case, `js-round-gate`): **verified, depth improved**

I re-measured with SCORECARD command D at each revision.
Command: `git show $REV:tools/mutate-and-run.sh | python3 -c '…^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+…'`

| Revision | Output |
|---|---|
| 28aeef4 | `recorded_cases=6 depth_score=6` |
| 09ee1d0 | `recorded_cases=7 depth_score=7` |
| 017a2b0 | `recorded_cases=7 depth_score=7` |

| Fact | Command | Observed |
|---|---|---|
| Target pin | `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs \| sha256sum; … \| wc -l` | `f890e277…d3e9`, 1511 lines. Equals `PIN_ROUNDGATE` in the runner and the spec header. |
| Pre-registration came first | `git log --format='%h %cI' -- …/round-gate/{predictions.json,round-gate.defects.spec}` | only `e69b488 2026-10-20T10:39:59-03:00`. The sweep log's `MUTATE_DATE: 2026-10-20T13:40:15Z` is 16 s later. The spec sha256 is `e99b87eb…` at both e69b488 and 017a2b0, so it is unchanged. |
| Embedded leg equals the pre-registered spec | Python extracted the runner's `js-round-gate.spec` heredoc at 017a2b0 and compared it to the e69b488 spec | byte-equal (4281 B, sha `e99b87eb`) |
| 10/10 predictions held | `predictions.json` compared with `sweep/results.tsv` | killed A1, A3, B1, E3, C1060 (all predicted KILLED); survived C1059, A2, B2, CKIND, E1 (all predicted SURVIVED). `TABLE_ROUNDGATE` matches. |
| Sweep | `sweep/sweep.log` tail | `MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)`; `MUTATE_RESTORE: OK` with before = after = pristine `f890e277…` |
| Regression on the landed runner (evidence-verified) | `runner-regression.txt` | `REGRESSION_TOOL … sha256=0673d2e5…`, which equals `git show 09ee1d0:tools/mutate-and-run.sh \| sha256sum`. Result: `REGRESSION: PASS (cases=7 passed=7 …)`, rc=0. |
| Selftest (evidence-verified) | `runner-selftest.txt` | `MUTATE_SELFTEST: 83/83 pass`, rc=0. The trailing sha is `0673d2e5…`. |
| Leg-count check shown able to fail | `legcount-redbefore-mutant.txt` | `MUTATE_SELFTEST: 81/82 pass`, rc=1, on the dropped-tuple mutant |

Minor evidence defect: `.ufo/evidence/round-16/round-gate/runner-sha256.txt`
still reads `89722ddb…`, which is the c699c8c runner. It was not refreshed
when 05a2247 moved the runner to `0673d2e5…`. The regression and selftest
receipts carry the correct sha. Status-neutral; routed below.

### C2 — calibration 6→8 (full-page SKILL.md cold-read): **not verified; calibration unchanged**

The lane's counting command reproduces. I re-derived the buckets with my own
sectionizer, not `measure.py`. It counts the preamble plus `#`–`######`
headings outside ``` and ~~~ fences, strips trailing blank lines, and hashes
with sha256. The ledger's `credit` rule is the one stated in `measure.py`.

| Revision | SKILL sha | Buckets | Ledger |
|---|---|---|---|
| 28aeef4 | `97cf436b` | 51 | absent (`measure-28aeef4.json`: `ledger_present false`, restraint 6) |
| 09ee1d0 = 017a2b0 | `906fb649` | 54 | 54/54 credited. Ledger at 017a2b0: 75 entries, `skill_pins.post = 906fb649…`. |

SHONEN mark census (command C), at 28aeef4, 09ee1d0 and 017a2b0:
`boxes=4 checked=0 asserted=4 untouched=0`. The box-3 line now links
`.ufo/evidence/round-16/coldread/ledger.json`.

My reviewer seat C2LedgerFidelity was dispatched by this closure, not by the
lane, and was read-only. It sampled 6 entries (E16, E32, E40, E68, E70, E74)
against the seat reports and agreed with all 6. It checked 4 errata repairs
(SKILL.md:505 denied-verb count 23, :1614 `../PROTOCOL.md`, :3/:9-10
frontmatter quoting, :925 seven legs) and found all 4 correct. Every failing
ledger verdict sits on a superseded page version and was re-read by a
different seat.

**Why C2 still fails.** The ledger credits a bucket by its section sha. A
bucket whose bytes did not change keeps its wave-1 credit even when the
surface its instructions run against changed during the round. That happened
to the bucket `## Effective expectation reconciliation — round 14`
(SKILL.md:1563-1596, class `instruction`):
- Its only credit is CR26 at the snapshot sha `97cf436b`, run against runner
  `75ed934d`. CR26 recorded step 2 → exit 1 (`producer_before`) and step 3 →
  exit 0 clean (`w1/CR26.md:27-28`).
- c699c8c and 05a2247 then changed `tools/mutate-and-run.sh`, which
  `.ufo/evidence/round-13/expected.json:12` pins at `75ed934d…`.
- `tools/evidence-disposition.py:1182-1192` verifies every expected-input
  digest before any predicate runs.
- So at the measured commit, recipe step 3 (`--root . --dispositions …/dispositions.json`)
  exits **2** `expected_input_digest_mismatch`. The lane's own seats observed
  this: RR10 at c699c8c, and RX5 at 05a2247 with `observed 0673d2e5… expects 75ed934d…`.
- Step 2 uses `dispositions-before.json`, which has the same `expected_file`
  and therefore takes the same path to exit 2. This one is [INFERENCE] from
  reading the code; I did not execute the gate.
- Steps 2–3 at SKILL.md:1580-1584 still state the pre-round outcomes. The
  lane annotated only the round-15 registry row (SKILL.md:1681).

Under the lane's credit rule (`wrong_expectations>0` fails), a re-read of that
bucket at 09ee1d0 would leave it uncovered. The count would be 53/54,
`box3_full_page` false, and the restraint score 6. The box-3 assertion ("every
SKILL.md bucket … wrong expectations repaired and re-read") is therefore not
correctly restrained at the measured commit, so the rubric's box-3 points are
not earned. The repairs and the ledger are real work. What fails is the
full-page assertion, on one bucket the round itself made stale.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 re-measured 6→7. Evidence chain verified (§2). |
| calibration | unchanged | C2's 6→8 does not hold at 09ee1d0 (§2). The rubric score stays 6. The box-3 text overclaims by one bucket. |
| operability | **harmed** | See below. |
| coverage | unchanged | Case 7 is on Core ground (kumitate `scripts/*`), and PROVINCE gained only appends. |
| freshness | unchanged | No successor sweep. The lane's other freshness instruments were not altered. |
| adjacency | unchanged | Kumitate was read-only: `git -C kumitate-shokunin` shows the pin read, and the lane made no sibling writes. |

**Operability: harmed.** I asked whether the round-14 gate's exit 2 harms
operability, and it does. Before the round, the registered entry command
`python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`
returned 0 clean at the lane HEAD. That gate backs the round-14 SCORECARD
capability "effective expectation reconciliation". After the round, it
returns 2 could-not-evaluate at HEAD permanently:
- Because a historical digest mismatch fires before every predicate, the
  live-tree run cannot tell this by-design mismatch from tampering with
  round-13/14 evidence.
- The documented replacement, `--root` on `git archive 28aeef4`, grades a
  frozen commit, not the tree it ships in.
- The round-14 recipe's stated outcomes (SKILL.md:1580-1584) are now wrong.

That is a checklist item that no longer produces its stated outcome, which
is the AXES operability signal. "By design" holds for the gate's fail-closed
behaviour, not for leaving it un-repinned. A lane-owned superseding
disposition or re-pin was available: RR10 names `tools/pin-disposition.py`.
Materializing the historical runner from git, as the ledger legs already
do, would also work. The round did neither and did not list this as an open
debt. The ToolsNoHarm monitor ran selftests only, so it could not see this.
The round's runner gains (leg 7, leg-count check, 83/83) do not offset it,
because AXES says a trade anywhere is not an improvement.

## 4. Discernment spot-check (LEARNING.md)

Sample from `corpus/lessons/round-16.md` `## Gate`:

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| G1 case-7 note | admit | `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs` (sha `f890e277…`); `predictions.json` @e69b488 against `sweep/results.tsv`; runner heredoc compared with the spec | agree | Measured. Pre-registered 16 s before the sweep, 10/10 held, and the leg replays exactly. |
| G13 leg-count agreement check | admit | `round-gate/legcount-redbefore-mutant.txt` (81/82, rc 1) against `runner-selftest.txt` (83/83, rc 0) | agree | Shown able to fail on the named surviving mutant before it counts (CORPUS §Additional rules). |
| G6 ledger as box-3 evidence | admit | ledger.json @017a2b0; SKILL.md:1563-1596 and 1580-1584; `tools/evidence-disposition.py:1182-1192`; `w2/RR10.md:43-63`; `w3/RX5.md` row 2 | **disagree** | The ledger records the reads faithfully, but sha-only credit is blind to surface drift. One credited instruction bucket is wrong at the landing commit (§2). |
| G2 `INTERNAL_ERROR` mutant | reject | `round-gate.mjs` @364f1d5 :682-684 | agree | The token is emitted only from the top-level `catch (e)` around `main`, a catch-all no fixture input reaches. A survivor there would be equivalent by unreachability. |
| G4 `controls_match` control claim | reject | `.ufo/waves/round-16/w1/RGControl.md` (verdict lead), `round-gate.mjs` mkdtemp prefix | agree | `repeat-control.py` exits 1 `controls_mismatch` on 3 and 5 runs, and the only varying token is the mkdtemp name. An exit-only oracle is the honest grade. |
| G3 `REPORT_MIN_BYTES` 1024→512 | reject | spec @e69b488 and `results.tsv` (C1059 SURVIVED, C1060 KILLED) | agree | An interior point cannot test the projected bound. The 1059/1060 edge pair did, and it confirmed the interval edge. |

Sampled 3 admits and 3 rejects; I agree with 5 of 6.

SOURCES rows re-opened (≤25-word quotes):

| Row | Re-opened | Quote check |
|---|---|---|
| S056 | https://pitest.org/quickstart/mutators/ (2026-10-20) | §Conditionals Boundary Mutator: "The conditionals boundary mutator replaces the relational operators `<, <=, >, >=` with their boundary counterpart as per the table below." It is present; the page breaks the sentence over a line. ≤25 words. Agree. |
| S052 | https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/ (2026-10-20) | §Supported mutators ¶1, sentence 2: "We've aligned on a standard naming scheme so it is easy to switch and compare implementations." Verbatim. Agree. |
| S053 | `git -C kumitate-shokunin show 364f1d5:scripts/round-gate.mjs`, lines 19-20 | "a green verdict asserts nothing fleet-wide, and running the gate does not change mission completion". Verbatim at :19-20. Agree. |

Census, command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`,
rc 0. Output: `W04` for S047 and S048 (duplicate pitest incremental_analysis
URL, pre-existing and disclosed) and `tameshi ok …/corpus/SOURCES.md`.

Frozen manual counts:

| Revision | Rows | Tiers | Status |
|---|---|---|---|
| 28aeef4 | 49 | A=42 B=5 C=2 | mined=22 queued=24 rejected=3 |
| 017a2b0 | 55 | A=47 B=6 C=2 | mined=28 queued=24 rejected=3 |

This matches the report. `git diff 28aeef4 017a2b0 -- corpus/SOURCES.md`
changes no prior row: it adds 6 rows plus the search-log and id-footer lines.

## 5. Trend verdicts

- **expansion: improved.** One new admitted knowledge entry,
  `corpus/knowledge/mutation-case-kumitate-round-gate.md`. It opens with the
  provenance trio, and its `source:` cites mined S053, S052, S056 and S057.
  It covers ground the coverage map held only as the §13 projection, and its
  README row was added the same round.
- **quality: harmed.** Real gains: the 19 SKILL repairs (4 of 4 sampled
  correct) and the measured matrix §13 readings. But a previously admitted
  instruction and gate (round-14 recipe and disposition gate) now fail their
  re-check at HEAD. That falsifies the report's "no admitted entry failed its
  re-check", and §Evidence standard's "corrections sweep every mention" was
  missed (only :1681 was annotated).
- **discernment: improved.** Round-15 routed defects 1 and 2 became a credited
  scan and a failure-backed fix. `correction.json` names exactly
  `usage-proof-new` and `gate-usage`, `verification-3.json` sha `3c419055…` is
  unchanged at both revisions, and the measure red-before is `box3_ledger_link: false`.
  Ten mined mistakes carry evidence. I agree with 5 of 6 sampled gate
  decisions; the one disagreement (G6) is routed.

## 6. Routed defects (tameshi owes its own repo, next round)

1. **R16-OP1, operability (blocking for re-admission).** Restore a
   clean-capable live-tree verdict for `tools/evidence-disposition.py`.
   Options are an appended superseding pin or disposition for
   `tools/mutate-and-run.sh` through the lane's own pinning path, or reading
   the historical runner from git. Ship red-before (current exit 2) and
   green-after, and keep historical evidence bytes immutable.
2. **R16-C2a, stale instruction.** Correct SKILL.md:1580-1584 (round-14
   recipe steps 2–3) for the moved runner, or mark it historical with the
   working invocation. Then re-read the bucket with a fresh seat and append a
   ledger entry at the new section sha.
3. **R16-C2b, measurement hole.** The cold-read credit is sha-only. Bucket
   credit must also be invalidated when a surface the bucket executes changes
   after its read: for example, record the input digests each instruction
   entry ran against and re-verify them at the measured rev. Show the
   red-before on the round-14 bucket.
4. **R16-C2c, box-3 text.** Until 2 and 3 land, the SHONEN box-3 line
   overclaims "every bucket … wrong expectations repaired". Correct it by
   appending, never by rewrite of evidence.
5. **R16-EV1, stale receipt.** `.ufo/evidence/round-16/round-gate/runner-sha256.txt`
   reads `89722ddb…`, but the landed runner is `0673d2e5…`. Append a dated
   correction; do not rewrite the file.
6. **R16-MON1, no-harm monitor.** The operability monitor (ToolsNoHarm) ran
   selftests only. Add the registered entry commands (`--root .` forms) so a
   live-tree verdict change is caught inside the round.

## 7. Operator notes

All four SHONEN boxes remain `[~]` lane assertions. None is checkable as `[x]`
by a non-author on this round's evidence: box 3 fails on the round-14 bucket
(§2). Promotion is operator-owned; nothing here promotes.
