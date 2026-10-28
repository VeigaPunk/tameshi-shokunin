# Tameshi round 55 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-10-28
lane_round: 55
lane HEAD verified: `tameshi-shokunin@875bb75693bd659c5c9794a09a1137c689778390` (branch `master`, local = remote, ahead=0)
base: `0a2010acd1e92e4e332774050825e21bcfc7e079`
measured revision: `4c04c1d33377e5b6a3636199c5fdda197fc670d5`
freeze pointer of record: `4f7a7040a57e7aed17db941be9c27b300aafb783` (nine amendments, `freeze.json` `amendments` length 9)
report: `.ufo/reports/round-55/tameshi.md` (fleet `06b80635`, author `tameshi-shokunin <tameshi@shokunin.local>`)
verdict: **not admitted — `rejected-harmed`.** C1 re-measured true at the measured revision; C2's
substance re-measured true from committed bytes but its counter has **no verdict at the measured
revision** and one cited seat receipt is red where the report quotes it green; and the round's own
edits dropped the calibration instrument from 64/64 (score 8) to 46/64 (score 6) with the re-key
never landed, so an owned axis is harmed. The round is a real, honest partial — it is rejected on
the harness's own register (r52's rule), not on its candour.

This file is a non-author artifact. Nothing in the lane was edited; the only lane write is this file,
committed through `scripts/hyaku/jj-lane.sh commit -- corpus/lessons/round-55-verifier-spotcheck.md`.

---

## Step-1 conformance

| check | command (observed) | result |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-55/tameshi.md` (fleet) → `tameshi-shokunin e4b4190270…`, `tameshi-shokunin ac77f50eb7…`; last two report commits `e4b41902` 14:54:14, `06b80635` 14:55:53 −03 | pass |
| report lands last | lane tip `875bb756` authored 14:54:02; the report's final commit 14:55:53 is after it | pass |
| dispatch evidence / prompt contract | `.ufo/prompts/tameshi-round-55.md` (689 lines): claims 1–3 on distinct axes + lowest-non-retired rule (:14), L2 floor ≥8 in one batched call (:82) matching `MISSION.md:55`, commit-then-push (:131), push scope (:132), L0 side channel (:138), report path (:101), `## SHONEN` one line per box (:118), commit-hash citation (:103), lane write scope (:1, :324), plus the run-11 addendum §6 | pass (all five child-lane items and the round-level items verbatim) |
| cited lane commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `9cf0146b 51d1f0eb 4c04c1d3 631cd645 4f7a7040 133b2ce` → exit 0 six times; `git log 0a2010ac..875bb756` lists the same commits | 6/6 pass |
| lane pushed, nothing ahead | `scripts/hyaku/jj-lane.sh state …/tameshi-shokunin` → `local=875bb756 remote=875bb756 ahead=0 behind=0` | pass |
| SHONEN heading | report `## SHONEN`, 4 × `[~]`; `SHONEN.md` holds 4 boxes (`grep -c '^- \['` → 4) | pass (4/4, box 3 declared *not restored*) |
| report is real, not a marker | names two claims, revisions, three waves, receipts, trends, residuals, and a self-declared *partial* | pass (real report) |
| wave shape | `swarm-registry.json` member counts 75 / 34 / 32 = 141; attack roles (reviewer+critic+mutation-tester per the v2 policy): w1 18+6+4=28 → 37.3 %, w2 13+7+4=24 → 70.6 %, w3 6+3+1=10 → 31.2 % | pass as reported; total 141 over the 64–128 band by 13, disclosed by the lane |
| uncommitted round work | `git status --porcelain` at closure → 83 entries, all under `.ufo/`; **7 of them are round-55 files created 13:55:47–14:34:53, i.e. before the lane tip 14:54:02** | **fail** → R55.6 below. The remaining dirt is post-filing (see R55.7) |
| prompt identity / attribution | prompt file committed in the fleet repo for this round; report committed by the lane | pass |

## Per-claim re-check

All measurements are plain greps/counts over committed bytes at `4c04c1d3` (or `875bb756` where the
receipt lives there). The lane's counters were **not executed** (`§Gate standard`, Closure
consequence); its committed verdict lines were read.

### C1 — calibration: the ten routed record defects agree with the tree (re-measured: true)

| command | observed |
|---|---|
| `git show 4c04c1d3:SCORECARD.md \| grep -n 'ER-R54-' \| wc -l` | `14` occurrences = 10 headings `ER-R54-1…10` (lines 2631–2698) + 4 cross-references |
| corrections section boundary | `grep -n '^## Round 55 - round-54 record corrections'` → line `2621` |
| stale tokens outside that section (`7883e0e5`, `fe70474d`, `097985c1`, `CTL_POS_c1 true`, `total=14`, `rekeyed=0/30`, `84 staged`) | lines `2643 2643 2644 2632 2650 2699 2701 2693` — every hit at or after 2621, i.e. inside the erratum section only |
| `git show 4c04c1d3:corpus/lessons/round-54.md \| grep -n '84 staged'` | none; the corrected sentence is `:51` **"The other 80 staged `merge/tameshi` entries"** |
| the ten receipts the corrections name | all exist at `875bb756`: `round-54/control/controls-b.stdout`, `round-54/after/frozen.stdout`, `round-54/before/c2.stdout`, `round-54/freeze.json`, `waves/round-54/w1-registry.json`, `…/T54W2Sent01-receipts/forged-reader.json`, `…/T54W1ExecStraceNoise.md`, `round-54/control/r53-counter-at-88afa941.stdout`, `…/T54W2Sent03.md`, `round-54/control/controls-a.stdout` (10/10 EXISTS) |
| ER-R54-8 withdrawal | the section states the operator turn exists (`history.db` row 690) and withdraws *fabricated* while keeping the incident; `T54W1ExecStraceNoise.md` carries a `SUPERSEDED` block (`M` in `0a2010ac..875bb756`) |
| lane's own committed verdict | `git show 875bb756:.ufo/evidence/round-55/after/c1.stdout` → `C1_R55: rev=4c04c1d33377 classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true` |
| before receipt | `before/c1.stdout` → `C1_R55: rev=0a2010acd1e9 … premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` — matches the report |
| controls | `control/controls-a.stdout`: `CTL_0_c1`, `CTL_0_c2`, `CTL_SKIP_c1` (total=6), `CTL_FAB_c1` (total=10), `CTL_SKIP_c2` (total=4), `CONTROLS_A: 5/5 as pre-registered` — all false as designed |

**Ruling: C1 verifies.** Re-measured by the closure, agreeing with the committed counter at the named
revision.

### C2 — operability: one exit class, one stderr line, every documented allocating mode (re-measured: true; lane evidence at the measured revision: absent)

| command | observed |
|---|---|
| `git grep -l 'strict_scratch_root' 4c04c1d3 -- tools/` | 7 tools: `bash-witness-study.py`, `context-capture.py`, `env-diff.py`, `evidence-disposition.py`, `pin-disposition.py`, `registry-check.py`, `repeat-control.py` |
| identical grammar in all seven | `git grep -n 'clone scratch' 4c04c1d3 -- tools/*.py` → one hit per tool, all `cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)` (repeat-control:165, context-capture:313, env-diff:46, evidence-disposition:205, pin-disposition:175, registry-check:770, bash-witness-study:219) |
| distinct class, not bare `RuntimeError` | `repeat-control.py:148`, `context-capture.py:~301`, `registry-check.py:757` define `class ScratchRootUnusable(RuntimeError)` and raise it at the refusal (base `0a2010ac` raised `RuntimeError` in all three) |
| exit 2 on every documented allocating mode | `repeat-control`: `EXIT_BY_ID["setup_error"]=2` and `could_not_evaluate()` prints one stderr line then returns it (:228-235, main `except ScratchRootUnusable` first :925); `context-capture`: `run_selftest` `except ScratchRootUnusable` writes one stderr line, `return 2` (:2217-2229); `registry-check`: `--selftest` `except RuntimeError → print … return 2` (:1851-1857), `--rev` `except ScratchRootUnusable → (json: machine report) + one stderr line, return 2` (:1936-1952); `env-diff`: `--selftest` and `--contract` both `ENVDIFF_SETUP: could-not-evaluate: …`, `return 2` (:233-236, :263-264); `bash-witness-study:1789`, `pin-disposition:1400`, `evidence-disposition:3232` unchanged |
| seven registry cells | `git show 4c04c1d3:tools/registry.json \| jq '[.. | objects | select(has("scratch_root"))] \| length'` → `7`; each cell quotes the prefix its tool really prints: `repeat-control:`, `WITNESS_STUDY:`, `pin-disposition.py:`, `evidence-disposition.py:`, `context-capture.py:`, `registry-check:`, `ENVDIFF_SETUP:` |
| note `## One line, every mode` | `corpus/knowledge/scratch-root-contract.md:71`; names exactly nine allocating modes (`env-diff --selftest`, `env-diff --contract`, `repeat-control --selftest`, `registry-check --selftest`, `registry-check --rev`, `bash-witness-study selftest`, `pin-disposition --selftest`, `evidence-disposition --selftest`, `context-capture --selftest`) and five lazy ones; no longer claims stdout is empty |
| SKILL.md drift | `git diff --stat 0a2010ac 4c04c1d3 -- SKILL.md` → `1 file changed, 7 insertions(+), 3 deletions(-)`, a single hunk inside `## Standing rules` |
| **lane's own counter at the measured revision** | **absent**: `git grep -n 'rev=4c04c1d3' 875bb756` returns only the C1 line. Committed `after/c2.stdout` stops mid-run (last line `EXPLAIN usable repeat-control --selftest rc=0 ok`) |
| committed green C2 receipts name other revisions | `C2_R55 … total=0 C2_R55_PASS=true` at `rev=9cf0146b94dd` (11 receipts, C0), `06bead3ee102`, `f9a19c4117d7`, `913cdfca57a3`, `7cc824b4ecdb`, `25b1333d41b3`, `9de7deac0d72` (demo/amendment snapshots) |
| the report's second cited receipt | cited as `grammar=9/9 … note=9/9 skill=1/1 total=0`; committed `T55W1ScribeSkill-receipts/c2-integrated.out:44` reads `rev=08d64e946006 … total=1 C2_R55_PASS=false`, and `c2-integrated-verdict.txt` says "every arm is green and total is still 1 -> PASS=false from bookkeeping only" |

**Ruling: C2 verifies on the tree, not on lane evidence.** The target state is true of the committed
bytes at `4c04c1d3` and I re-derived every arm the counter names (9/9 grammar, 7/7 cells, 9/9 note,
1/1 SKILL) without running it; but no committed verdict names `4c04c1d3`, and the one seat receipt
the report quotes as `total=0` is committed as `total=1 / PASS=false` (R55.2).

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| calibration | **harmed** | C1's record surface improved (ten defects corrected, none stale outside the erratum), but the axis's own instrument — the round-21 cold-read monitor — reads `64/64 score=8 box3=True` at base `0a2010ac` and `46/64 score=6 box3=False` at C0 `9cf0146b` (`.ufo/waves/round-55/w2/T55W2RevNoHarm-receipts/coldread-summary.txt`; precheck `floor=0a2010acd1e9 floor_credited=64 cand=9cf0146b94dd cand_credited=46 lost=18 RED`). The 18-heading re-key never landed (only a fixture at `c94ad673` repays it), later commits change more gated inputs, and the standing axis row still records **8** with no restatement in the round-55 block — a score the tree no longer supports. Same rubric as round 52. |
| operability | **improved** | C2's seven-tool refusal class, the seven registry cells, the note and the SKILL bullet all re-derived from committed bytes (above); base read `grammar=6/9 docs=0/7 note=0/9 skill=0/1 total=20`. |
| depth | unchanged | no new mutation case; `recorded_cases=10 depth_score=10` unchanged (`coldread-floor-summary.txt`). |
| coverage | unchanged | no new surface admitted; the ninth allocating mode is a mode of an owned tool, not a new surface. |
| freshness | unchanged | no source row re-verified; `F1–F10` frontier statuses unchanged (report, and `SOURCES.md` rows untouched old→new = none). |
| adjacency | unchanged | the round read siblings read-only; no contested scope absorbed; `PROVINCE.md` untouched. |

## Discernment spot-check (LEARNING.md: checked from outside)

| item | gate decision | source re-opened | agree/disagree | reason |
|---|---|---|---|---|
| S280 GNU Coding Standards §4.4 *Formatting Error Messages* (`https://www.gnu.org/prep/standards/html_node/Errors.html`) | **admit, mined** (tier A, grounds C2's one-line shape; explicitly says nothing about exit codes) | fetched 2026-10-28: "Error messages from other noninteractive programs should look like this" **FOUND**; the rule continues `… like this: program : sourcefile : lineno : message … or like this: program : message`; the no-capital/no-period rule **FOUND**; committed extraction `S280-gnu-errors.txt` sha256 `edcaf94b…` is the same text | **agree** | the standard's sentence is exactly the shape the note adopts, the row's quote is ≤25 words (14), and the row correctly refuses to source the exit-2 class from it. Minor notation: the live page renders the colons with spaces, the row quotes the collapsed form; the extraction carries the verbatim bytes, so the row is locatable, not misquoted |
| FreeBSD `sysexits(3)` (`https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3`) | **reject before append** (already held as S090; the page deprecates its own interface, so it cannot ground an "adopt sysexits" rule) | fetched 2026-10-28: "This interface has been deprecated and is retained only for compatibility. Its use is discouraged." **FOUND**; "The choice of an appropriate exit value is often ambiguous" **FOUND**; `corpus/SOURCES.md:99` is the S090 row for the same URL | **agree** | the duplicate-URL refusal is correct (CORPUS rule 2 / census W04), the flip is stated (a rule that actually adopts an `EX_*` code and records the deprecation as an accepted trade), and the rejection's evidence is committed as `S281-sysexits.txt` |
| census | — | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | **exit 0**, trailer `tameshi ok …/corpus/SOURCES.md` (warnings are pre-existing W01/W04 rows, none S280) | rows: `grep -cE '^ {0,3}\| S[0-9]{3,} \|'` → base `139`, HEAD `140` — matches the reported before→after |

## Trend verdicts

- **expansion — unchanged.** One tier-A row (S280) on ground the lane already owns; no frontier row
  advanced (`F1–F10` unchanged), no capability claimed, `capabilities` table untouched. Agrees with
  the lane.
- **quality — improved, with counter-signals.** Three tools moved from `RuntimeError` leakage to one
  parseable line with a distinct class and exit 2; seven registry cells, a nine-mode note and the
  SKILL bullet now state the contract (re-derived above); QUALITY 105 carries an erratum and 106 is
  appended. Counter-signals: the deciding run never executed, so no C2 verdict exists at the revision
  the round measures (R55.1), and the round's own edits cost the cold-read score (calibration harm).
- **discernment — improved, narrowly.** The external spot-check agrees with the gate on the one admit
  and the one reject it sampled, both re-opened against live bytes; the round also withdrew its own
  round-54 characterisation (*fabricated*) when a seat produced the operator turn — restraint that
  cost it an argument. Counter-signal: the R54.3 class (a quoted value no receipt contains) recurred
  in the C2 prose of the very round that fixed it (R55.2), so the gain is not yet a habit.

## Routed defects (lane owns the fix; all status-neutral for admission)

1. **R55.1 — no C2 verdict at the measured revision.** The round measures `4c04c1d3`; every green C2
   receipt names `9cf0146b` (C0) or a demo clone, and `after/c2.stdout` is committed truncated
   mid-run. Fix: run the frozen counter at the measured revision and commit the verdict, or measure
   the claim at C0 and say so (`§Gate standard`, "a verdict names the revision it was measured
   against").
2. **R55.2 — a quoted total its own receipt contradicts.** Report quotes `T55W1ScribeSkill` as
   `grammar=9/9 … note=9/9 skill=1/1 total=0`; the committed `c2-integrated.out:44` reads
   `total=1 C2_R55_PASS=false` (`rev=08d64e946006`). This is the R54.3 class recurring inside its own
   correction round. Fix: quote the receipt or name the run whose line you quote.
3. **R55.3 — the calibration instrument regressed and the axis row still says 8.** 64/64 → 46/64
   (score 8 → 6) at C0, unrepaired at HEAD, no SCORECARD restatement. Fix: land the 18-heading re-key
   (already planned as round 56's first item) **and** restate the row with the score the monitor
   actually reads until it does.
4. **R55.4 — a stale control sentence.** The report says `CTL_SKIP_c2` "was still running at filing";
   the committed `control/controls-a.stdout` (at `4c04c1d3`, 14:51:26 — before the report) already
   reads `CTL_SKIP_c2 … total=4 C2_R55_PASS=false` and `CONTROLS_A: 5/5 as pre-registered`.
5. **R55.5 — the deciding gate cannot compare the revision it certifies.** `deciding-run.sh` never
   compares a `CTL` line's `rev=` with the revision under test; row 1's defect is the same shape one
   level up. Declared by the lane as a residual; route it into QUALITY as a criterion with its lesson
   pointer when the frozen script is next allowed to change.
6. **R55.6 — uncommitted round work at closure.** Seven round-55 evidence files created before the
   lane tip were never committed: `w1/T55W1ExecRekeyPrep-receipts/{base,cand,floor}.json` (13:55:47),
   `…/rekey.json` (13:58:42), `w1/T55W1ExecNoHarm-receipts/coldread-at-base.json` (14:02:24),
   `w1/T55W1CritClaimShape-receipts/coldread-HEAD.json` (14:31:03),
   `w2/T55W2ScoutColdread-receipts/inputs.json` (14:34:53). Same class as R54.6, twice repeated.
7. **R55.7 — closure-environment contamination (not lane debt).** Concurrent non-author seats write
   inside the lane repo: `after/c2.stdout` was rewritten after the tip with `C2_R55: rev=4c04c1d33377
   … total=0 C2_R55_PASS=true` (uncommitted), and 14 tracked `T55W1MutC2-receipts` files were deleted
   from the working tree mid-closure. That green line is **not** lane evidence and is not cited above.
   Closure seats should work in scratch clones; operators of the closure harness should note it.

## What the closure did not do

It did not execute the lane's counters, gates or self-tests (`§Gate standard`), did not edit any
lane-authored file, did not check a SHONEN box, and did not promote or mint. SHONEN boxes remain
`[~]`: boxes 1, 2 and 4 have only lane assertions and box 3 the round itself declares unrestored, so
none is checkable by a non-author this round — promotion stays operator-owned.
