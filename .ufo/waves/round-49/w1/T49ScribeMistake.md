# Round 49 — `## Mistakes` rows (draft for the L1 to integrate)

Seat `T49ScribeMistake`, leaf, scribe. Read on lane tree `455b2cd` (base `8ca67421111fa354b47b803358391d0b07fc6db9`,
freeze `14d03ea4270c6904064022b62b6faf467e5c0968`), read-only. Nothing here is a verdict on a claim: the three rows are
mined mistakes from round 48, with the pointer and the showing command for each. Round 48 sources opened:
`corpus/lessons/round-48-verifier-spotcheck.md`, `corpus/lessons/round-48.md`, `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/tameshi.md`,
`corpus/QUALITY.md` criteria 86-98 (read first: criteria 90-98 end at `corpus/QUALITY.md:1442`, and none of them covers row 1 —
see §"Criterion 99").

Classes use the `mistakes.md` §5 vocabulary as the round-48 `## Mistakes` block does (`stale-premise`, `scope`, `landing`,
`reference-drift`, `provider`, `attribution`), with the fleet taxonomy class in brackets where the label is the lane's own.

## Rows

| # | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| 1 | `landing` (evidence-order; fleet C12-flavoured: a pre-registered obligation with no gate) — the pre-registered control order was not kept, and partial invocations of a claim counter at the deciding revision left no trace in the report (the spot-check names five seats; six reports carry the marker — F1) | `.ufo/evidence/round-48/contract.json:7` states the order in prose: controls are "scored and committed" at step 2, "before any deciding or control scoring". Observed clocks: C1 deciding run `2026-10-26T15:34:20Z`→`16:20:54Z` (`.ufo/evidence/round-48/after/c1-a3.start`, `.end`); CTL_B-CTL_E scored `16:21:02Z`→`19:35:25Z` (`.ufo/evidence/round-48/control/c1-controls-a3.start`, `.end`) — eight seconds after the deciding run ended. The partial invocations: the counter documents its own probe mode at `.ufo/evidence/round-48/calibration/measure.py:59` ("`--only ID[,ID]` and `--rounds N` (N != 3) are seat probes: the verdict line is `C1_R48_PARTIAL`") and implements it at `:1004`; six round-48 `a2w1` reports carry executed-format `C1_R48_PARTIAL:` lines (`T48A2ExecC1SerialA.md`, `T48A2ExecC1SerialC.md`, `T48W2ExecC1ProbeA.md`, `T48W2ExecC1ProbeB.md`, `T48W2ExecC1ProbeC.md`, `T48W2RevC1Separability.md`), and the report names none of them (`grep -c -- "--only" /home/vgpnk/Projects/shokunin/.ufo/reports/round-48/tameshi.md` → `0`). Found by `.ufo/evidence/round-48`-external reading; stated at `corpus/lessons/round-48-verifier-spotcheck.md:27` (defect 2) and `:28` (defect 3) | `none` — the clause lived only in the contract (`round-48/contract.json:7`) with no executable surface. The nearest criteria do not contain it: QUALITY 69 (`corpus/QUALITY.md:784-791`) orders the *binding conditions of a data wave* against their controls, not a claim counter against its deciding run; QUALITY 88 (`:1291-1315`) binds the *no-harm* monitors at the base; no criterion names a partial/`--only` invocation at all | two halves. (a) Order: gate 0 of `.ufo/evidence/round-49/deciding-run.sh:22-29` refuses (exit 3, nothing run) when a control receipt is absent at REV, when its last-touching commit does not descend from FREEZE, and when the receipt directory already holds a start receipt. (b) Partial runs: both round-49 counters delete the mode — `--only`/`--rounds` are absent from `.ufo/evidence/round-49/c1/measure.py:549-554` and from `.ufo/evidence/round-49/c2/measure.py:429-435` — so a preview cannot print a verdict line; the residual (a probe launched from another work dir, invisible to gate 0) needs a declaration clause, which the round-49 contract does not yet carry (`grep -n preview .ufo/evidence/round-49/contract.json` → `:77` only, the `mistake` field). The three-condition battery on a scratch clone, with the executed blob pinned by `freeze.json:15` (sha256 `31e9838e…`), is `.ufo/waves/round-49/w1/T49ExecMistakeGate.md`; this seat independently observed (a) and the second-invocation condition (§Red states d6). Proposed as QUALITY 99 below |
| 2 | `scope` — a claim's own record edits moved a pre-registered no-harm monitor, and the first check that could see it was the deciding run | `.ufo/evidence/round-48/after/coldread-sections.stdout:1` → `COLDREAD_SECTIONS_CREDITED=57 (base 60)`; the C2 entry re-pointing is what the counter names as drifted: `.ufo/evidence/round-48/quality/coldread-precheck-red-c7586b9.stdout` carries `LOST ## Repeated controls and gate registry — round 12 | drifted=…corpus/knowledge/repeated-control-precondition.md…`, the same for the round-13 and round-14 headings, and the closing line `COLDREAD_PRECHECK floor=473336d9d789 floor_credited=60 cand=c7586b9a10ef cand_credited=57 lost=3 RED`, `.exit` = `1`. Mined already at `corpus/lessons/round-48.md:400-404` | **QUALITY 98** (`corpus/QUALITY.md:1436-1442`) — and this is the point of the row. 98 captures exactly three things: the precheck is run on the candidate content revision *before* it is named the deciding revision; a `RED` is "never first discovered by the deciding run"; and a `RED` may stand only if "declared beside the claim that causes it as a trade on a pre-registered no-harm monitor". It does **not** capture (i) restoration — declaring the loss satisfies it, so credit may be traded away once per round indefinitely; (ii) late or pre-existing loss — it binds the candidate `CAND` against `BASE`, so an edit after `CAND`, or a drop already present at `BASE`, is invisible; (iii) durability — nothing in 98 requires the lapsed inputs to stop being volatile, which is the only change that ends the recurrence | the durable half, in flight this round and not yet evidence: `.ufo/evidence/round-49/contract.json:32` re-keys the seven lapsed sections with trace-bound inputs that are the sections' cited **non-record** files (the five record files are read through git blobs), and the C1 predicate requires the monitor to still credit every section after one line is appended to each of the five record files. Detection stays 98's; repair is claim-scoped to those seven sections, so the other 57 keep 98's exposure |
| 3 | `reference-drift` (fleet C01) — a record's statement about its own evidence does not match the bytes it cites | `SCORECARD.md:2326` prints "Every evidence cell below is the counter's own `--emit` output, pasted byte-exact". Counted at the revision it describes (`c7586b9a`): 19 capability rows (`SCORECARD.md:2332-2350`) do match, and the 3 axis rows (`:2354-2356`) cannot, because the emit prints a placeholder for them — `.ufo/evidence/round-48/calibration/emit-15b1521.stdout:115-117`: `EMIT_AXIS | depth | 9 | see the evidence pointer in the round-48 SCORECARD block, tool sha256 … , runs 3 stable |`. Stated at `corpus/lessons/round-48-verifier-spotcheck.md:30` (defect 5) and corrected append-only at `SCORECARD.md:2382-2384` (in round 49) | `none` — QUALITY 91 (`corpus/QUALITY.md:1355-1361`) binds a *lesson's located quote* byte-exact; QUALITY 87 (`:1223` block) binds a quote's length; neither binds a record's prose description of how its own evidence was produced, so a self-description can be false while every cell it describes is individually checkable | a verbatim checker, not a wording patch: compare each round-48 standing evidence cell to its `EMIT_CAP`/`EMIT_AXIS` field, byte-exact, and require 22/22. Receipt `.ufo/waves/round-49/w1/T49ScribeMistake.emit-verbatim.stdout` reads `EMIT_VERBATIM ok=19 mismatch=3 rev=c7586b9a10ef` — the check is red today on exactly the three rows the overstatement covers, and green on the 19 that hold. The SCORECARD correction already says what is true; the checker is what stops the next record from re-asserting it |

### Red states (commands as run; outputs as observed)

```
d1  cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
    cat .ufo/evidence/round-48/after/c1-a3.start .ufo/evidence/round-48/after/c1-a3.end \
        .ufo/evidence/round-48/control/c1-controls-a3.start .ufo/evidence/round-48/control/c1-controls-a3.end
    # 2026-10-26T15:34:20Z / 2026-10-26T16:20:54Z / 2026-10-26T16:21:02Z / 2026-10-26T19:35:25Z
d2  grep -l 'C1_R48_PARTIAL:' .ufo/waves/round-48/a2w1/*.md | wc -l
    # 6      (the spot-check names five seats as runners; see F1)
d3  grep -c -- '--only' /home/vgpnk/Projects/shokunin/.ufo/reports/round-48/tameshi.md
    # 0
d4  grep -n '^COLDREAD_SECTIONS_CREDITED' .ufo/evidence/round-48/after/coldread-sections.stdout ; \
    tail -1 .ufo/evidence/round-48/quality/coldread-precheck-red-c7586b9.stdout ; \
    cat .ufo/evidence/round-48/quality/coldread-precheck-red-c7586b9.exit .ufo/evidence/round-48/quality/coldread-precheck-ok-freeze.exit
    # COLDREAD_SECTIONS_CREDITED=57 (base 60) ; … lost=3 RED ; 1 ; 0
d5  python3 -  # emit-verbatim check; the script is the header of the receipt it writes
    # .ufo/waves/round-49/w1/T49ScribeMistake.emit-verbatim.stdout → ok=19 mismatch=3
d6  # gate 0, in a scratch clone at its own toplevel ($S/lane, git rev-parse --show-toplevel == $S/lane)
    bash .ufo/evidence/round-49/deciding-run.sh "$L" 14d03ea4270c6904064022b62b6faf467e5c0968 14d03ea4270c6904064022b62b6faf467e5c0968 "$L/out-a"   # → DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c1-controls.stdout ; exit 3
    bash .ufo/evidence/round-49/deciding-run.sh "$L" 455b2cd66fd9f237146a5355ca8bbc84f3071c50 14d03ea4270c6904064022b62b6faf467e5c0968 "$L/out-c"   # with out-c/c1.start → DECIDING_REFUSED second-invocation c1 ; exit 3
    # .ufo/waves/round-49/w1/T49ScribeMistake.gate0-{a,c}.stdout and .exit
```

`d6`'s second line is also the positive datum: the refusal at the tip is the *later* gate, so the control-receipt loop passed
at a revision whose receipts descend from the freeze — gate 0 discriminates, it is not vacuous. Both probes ran in
`/fast/scratch/hyaku/tameshi-r49/T49ScribeMistake` (clone `--shared` of the lane), never in the lane; the clone is deleted
after this report. A probe is not a verdict.

## Proposed QUALITY criterion 99

Only row 1 lacks a capturing criterion, so only row 1 gets one. The text is one paragraph in the house form (predicate,
lesson, falsifier that must fail); the L1 decides whether to append it.

> ### Criterion 99 — a control's discrimination evidence is dated before the value it discriminates, and a non-deciding invocation at the deciding revision is declared
>
> Every pre-registered control of a claim counter is scored at the freeze bytes and its receipt is committed in a commit
> that descends from the contract freeze and precedes that counter's start receipt for the deciding run; the deciding
> script refuses with a nonzero exit and runs nothing when a control receipt is absent at the deciding revision, when its
> last-touching commit does not descend from the freeze, or when the receipt directory already holds a start receipt. Any
> other invocation of a claim counter at the deciding revision — a `--only`/`--rounds` probe mode, a seat preview, a run
> from a second receipt directory — is declared in the contract before data and listed in the report with its revision and
> its verdict line, and a counter that has no partial mode says so in the same place. The criterion binds the order and the
> declaration, never the values: a control scored after the deciding run at freeze bytes remains valid discrimination
> evidence, which is why the order is gated rather than the verdict re-read. It cannot see a probe launched outside the
> receipt directory it watches; that residual is exactly what the declaration clause covers.
>
> Lesson: `corpus/lessons/round-48-verifier-spotcheck.md` defects 2-3 (the round-48 contract stated the order in prose —
> `.ufo/evidence/round-48/contract.json:7` — and CTL_B-CTL_E were scored eight seconds after the deciding run ended, with
> five previews at the deciding revision absent from the report); `corpus/lessons/round-49.md` `## Mistakes` row 1.
>
> Falsifier that must fail: `.ufo/evidence/round-49/deciding-run.sh` at `14d03ea4270c6904064022b62b6faf467e5c0968` (freeze; no control receipts committed)
> prints `DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c1-controls.stdout` and exits 3 without
> running a counter (`.ufo/waves/round-49/w1/T49ScribeMistake.gate0-a.stdout`, `.exit` = `3`); at the lane tip with a
> `c1.start` already in the receipt directory it prints `DECIDING_REFUSED second-invocation c1` and exits 3
> (`…gate0-c.stdout`, `.exit` = `3`); at the lane tip with an empty receipt directory it passes the control loop (the
> observed refusal is the later gate) and its control receipts' last-touching commit `6885adb` descends from the freeze.
> QUALITY 69 (`corpus/QUALITY.md:784-791`) and 88 (`:1291-1315`) do not reach this object. The full three-condition battery on a scratch clone is `.ufo/waves/round-49/w1/T49ExecMistakeGate.md` (executed blob pinned at `freeze.json:15`, sha256 `31e9838e…`).

## Findings and limits

- **F1 — preview-seat count does not reproduce from my sweep.** The spot-check (`corpus/lessons/round-48-verifier-spotcheck.md:28`)
  names five seats as runners. My sweep, `grep -l 'C1_R48_PARTIAL:' .ufo/waves/round-48/a2w1/*.md | wc -l` → `6`, adds
  `T48W2RevC1Separability.md`; that file may be quoting a probe rather than running one, and nothing I read distinguishes the
  two. Reported as a difference, with no cause attributed (QUALITY 96): both figures support the row.
- **F2 — the "14 distinct statements" figure is not derivable from those files.** `C1_R48_PARTIAL:` lines carry
  `statements=N`, not ids (`.ufo/waves/round-48/a2w1/T48W2ExecC1ProbeA.md`), and the only `--only` id list my grep recovers
  from the six reports is `sources-registry,freshness,calibration` (3 ids). 3 is a lower bound on the probed statements; the
  14 is not checkable here. The row cites defect 3 for the *fact* of undisclosed previews, not for its counts.
- **F3 — the declaration half of row 1's fix is not in the round-49 contract.** `grep -n preview .ufo/evidence/round-49/contract.json`
  matches `:77` only (the `mistake` field). Gate 0 covers ordering and a *second invocation via the same receipt directory*;
  it cannot see a probe from another work dir (`deciding-run.sh:28-29`), so criterion 99's declaration clause has no built
  surface yet. Stated so the L1 can either build it or record the residual.
- **F4 — the round-49 no-harm cold-read monitor is weaker than the contract text it exists for.**
  `.ufo/evidence/round-49/contract.json:73` says the monitor "is re-run at the final tip and must still credit 64/64";
  `.ufo/evidence/round-49/no-harm.sh:13` gates `score>=6 and credited>=57`, and the committed base line reads
  `NOHARM coldread-floor score=6 credited=57 ok` (`.ufo/evidence/round-49/control/no-harm-at-base.stdout:2`). A tip that
  fell back to 57 would print the monitor green while the contract's own sentence is unsatisfied. Reading only — I do not
  edit the harness; the L1 owns whether 57 is the intended floor.
- **F5 — row 2 is not a new capture, and should not be filed as one.** QUALITY 98 already made the loss visible before the
  freeze (its own receipts: red `1` at `c7586b9a`, ok `0` at the freeze). The row's value is the statement of 98's residual
  (declaration without restoration; `CAND`-bounded), and round 49's durability work is in flight, not evidence.
- **Worktree note.** `git status --porcelain` in the lane at write time shows ` M SCORECARD.md` plus the wave-1 untracked files; the SCORECARD modification is not this seat's write (this seat wrote only its own files under `.ufo/waves/round-49/w1/`).
- **Tooling.** None installed or upgraded: this seat needed only `git`, `python3` and `bash`, all present.
- Not restated as rows: round-48's `stale-premise`, `provider`, `attribution` and prospective-record rows
  (`corpus/lessons/round-48.md:292-350`) already ship with their own red states; re-mining them would duplicate, not add.
  The S267/S268 pointer erratum (`corpus/lessons/round-48.md:396-398`) is already appended there.

## Summary

Three rows, one per mined round-48 mistake: (1) controls scored after the deciding run plus six reports carrying
`C1_R48_PARTIAL:` lines that `round-48/tameshi.md` never names — class `landing`, captured by `none`, fixed by gate 0 plus
two counters with no partial mode; (2) the C2 cold-read trade — class `scope`, captured by QUALITY 98, whose residual
(declaration without restoration, `CAND`-bounded) is stated, repair in flight; (3) `SCORECARD.md:2326`'s "pasted
byte-exact" — class `reference-drift`, captured by `none`, fixed by a verbatim checker that reads `ok=19 mismatch=3`.
Proposed criterion 99 covers only row 1, because 69 and 88 do not reach a claim counter's control order; its falsifier is
gate 0's two refusal lines, observed exit 3 in a scratch clone. Receipts: `T49ScribeMistake.gate0-{a,c}.{stdout,exit}`,
`T49ScribeMistake.emit-verbatim.stdout`. Findings F1-F5 record two unreproduced counts, one unbuilt declaration surface,
one monitor weaker than its contract text, and one row that is a residual rather than a new capture.
