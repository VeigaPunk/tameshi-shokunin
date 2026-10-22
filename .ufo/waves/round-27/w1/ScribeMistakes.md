# ScribeMistakes — candidate `## Mistakes` rows for round-27.md

Seat: TameshiR27.ScribeMistakes (scribe, leaf, read-only). Date: 2026-10-22.
Item: mine the round-26 closure and lesson for four defects and draft candidate
`## Mistakes` rows for `corpus/lessons/round-27.md`, in the four-field form
(class · evidence pointer · captured-by · fix). For each, say whether QUALITY 53
or QUALITY 54 (as landed at `2227d8338c02aa9a5fd7d95c1a41b76865ad7647`) captures
it, and how the fix was shown able to fail.
Tools installed or updated: none.

Scope note: this report drafts rows. It edits nothing. `corpus/lessons/round-27.md`
at lane HEAD `2abb01812933bf9f7044b188daae0f18c1c0f6c4` already carries three
`## Mistakes` rows (lines 55–79). Rows 1 and 3 below are candidate replacements
or additions to those; the exact wording is the L1's to choose.

## Verdict

Four defects mined, four candidate rows drafted. Two are captured by QUALITY 53,
one by QUALITY 54, and one by neither 53 nor 54 (it sits under pre-existing
QUALITY 8, 9, 25 and 39, and this round closed it by committing the receipt
rather than by a new rule).

| # | Defect | Captured by QUALITY 53 or 54? | Fix shown able to fail? |
|---|---|---|---|
| 1 | Harm-repair wave cancelled; harm carried over | **53**, and QUALITY 40 was already in force at round-26 base | Yes — `c1-measure.py` exits 1 at every revision measured |
| 2 | The "numeric 8 → 8" record | **53**, and QUALITY 40 was already in force at round-26 base | Yes — same counter, plus the appended correction is byte-visible |
| 3 | The unreceipted registry reading | **Neither 53 nor 54** | Yes — the no-mirror reading reads `held=46/49` where the mirror reads `49/49` |
| 4 | The counter that accepted unrelated receipts | **54** (QUALITY 51 carried only a bound) | Yes — I reproduced the old counter passing an unrelated receipt, and the new counter refuses moved bytes |

Two calibration corrections the L1 should weigh before the rows land:

- The drafted row 1 (`corpus/lessons/round-27.md:59`) says "Captured-by: none in
  round 26" for the cancelled-wave plus contradicted-record defect. For the
  record half that is too strong: QUALITY 40 was in force at the round-26 base
  `d4140796` (`corpus/QUALITY.md:364`) and requires that a lower current score be
  named before asserting unchanged calibration. Round 26 asserted unchanged
  calibration in the SCORECARD measured table while a wave-1 seat report in the
  same tree already named the lower score. "None in round 26" is defensible for
  the cancelled wave, not for the contradicted record.
- The drafted row 1 claims the SCORECARD row "is corrected by an appended entry".
  That append happened at `2227d833`, one round after the closure found it
  (`corpus/lessons/round-26-verifier-spotcheck.md:219-221`). QUALITY 26 (in force,
  `corpus/QUALITY.md:150`) says a stale receipt "gets a dated correction appended
  in the round that finds it". The lane did find it at the closure; the append
  came the next round. Whether that is a QUALITY 26 breach depends on whether a
  non-author closure counts as "the round that finds it" for the lane. I do not
  claim a breach; I record the ambiguity.

## Candidate rows for `corpus/lessons/round-27.md`

Format follows `corpus/lessons/round-26.md:70-73`: class · evidence pointer ·
captured-by · fix (with the fix's ability to fail).

### Row A — the cancelled harm-repair wave

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| A planned harm-repair wave cancelled, leaving the calibration harm carried into the next round | `corpus/lessons/round-26.md:113-116` (wave-2 spec validated, not dispatched, request cancelled) and `:134-140` (restraint 8 at base → 6 at `a08e85c`/`d2206cd`/`2b064cf`, "Harmed and not restored"); `corpus/lessons/round-26-verifier-spotcheck.md:132-135` ("calibration — harmed … the wave-2 repair was cancelled") and `:216-218` (routed item 1) | QUALITY 53 (`corpus/QUALITY.md:591-601`, landed at `2227d833`): a round that edits a traced input either has those sections cold-read again by independent seats at its content revision before it lands, or declares calibration harmed among its measured results. QUALITY 40 (`corpus/QUALITY.md:364-372`, in force at the round-26 base `d4140796`) is the closest prior capture: refresh affected inputs through actual recorded source reads, with independent provenance labeled. No criterion in force at round-26 base named a cancelled wave, so the cancellation itself was captured by nothing before QUALITY 53 | QUALITY 53 plus the frozen counter `.ufo/evidence/round-27/c1-measure.py`, which runs the strict monitor with no override and compares SHONEN box 3 against `box3_full_page`. Shown able to fail: it exits 1 with `box3_mismatch=1` at round-26 head `e08444d3` and at round-27 base `91edf9cd` (I ran both; §Commands below), and it exits 0 at `d4140796` (62/62, restraint 8), so it discriminates rather than always failing. **Open at the head I can see:** at lane HEAD `2abb018` the counter still reads `covered=25/64 restraint=6 box3_mismatch=1`, exit 1 — the wave-1 cold-read traces are still untracked in the working tree (0 of them committed) and `.ufo/evidence/round-21/coldread/ledger.json` is byte-identical to the base. The C1 target is not met yet, so this row's fix is a method, not a landed result |

### Row B — the "numeric 8 → 8" record

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| A calibration no-harm reading that does not name the strict monitor at the landed head, and that the lane's own in-tree reviewer report already contradicted | `SCORECARD.md:1309` at `2227d833` (round-26 C2 row, delta cell "numeric 8 → 8") against the strict monitor's `restraint=6` at the same revisions (`.ufo/evidence/round-26/after/monitor-harmed-{a08e85c,d2206cd,2b064cf}.json`); the same lane had `restraint 6` on record before that row landed — `.ufo/waves/round-26/w1/ReviewMonitorHarm.md`, committed at `40a12bf` (08:09:51), one minute before the SCORECARD row landed at `d2206cd` (08:10:32); closure `corpus/lessons/round-26-verifier-spotcheck.md:109` and `:219-221` (routed item 2) | QUALITY 53, second sentence (`corpus/QUALITY.md:594-595`): a calibration no-harm reading names the strict monitor at the landed head, never an earlier revision. **QUALITY 40 (`corpus/QUALITY.md:364-372`) was already in force at the round-26 base and covers the same class**: a lower current score is named before asserting unchanged calibration. So "captured-by: none in round 26" is too strong for this half; the record was already covered and the lane did not apply it. QUALITY 26 (`:150-152`) requires the dated correction to be appended in the round that finds it — the append came one round later | The append-only correction `SCORECARD.md:1319-1333` (landed at `2227d833`), naming base `d4140796` and the four head revisions with restraint 8 → 6, plus the re-measurement at `91edf9cd`; the original row is left as written. Shown able to fail: the correction is falsifiable by the same counter — `c1-measure.py` exits 1 with `box3_mismatch=1` at `e08444d3` and `91edf9cd` (§Commands), and the round-26 row's claim is contradicted by the committed receipts it cites. The row is the same shape QUALITY 26 requires: a dated append, never a rewrite |

### Row C — the unreceipted registry reading

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| An operability reading asserted in prose with no committed receipt at the revision it names | `corpus/lessons/round-26-verifier-spotcheck.md:137-141` ("The lane's `--only … held=1/1` reading at `2b064cf` and any full-registry run at head have no committed receipt") and `:222-224` (routed item 3); `corpus/lessons/round-26.md:125-130` ("A full registry run at the final revision was not repeated"). I confirmed the gap is real: `.ufo/evidence/round-26/after/` holds `registry-40a12bf.json` and nothing for `2b064cf` or for the head | **Neither QUALITY 53 nor QUALITY 54.** 53 is about cold-read credit and calibration readings; 54 is about a counter that accepts a run receipt. This defect is a reading with no receipt at all. It sits under pre-existing QUALITY 8 (`:24-26`, an executed-but-unreported verification is named debt, never cited as a pass), QUALITY 9 (`:27-29`, evidence is copied into `.ufo/evidence/…` before the commit that cites it), QUALITY 25 (`:143-149`, the no-harm monitor runs every active registered entry command) and QUALITY 39 (`:352-363`, a final-success claim names one effective receipt with matching argv, revision, exit, streams and digests). No new criterion is needed; the gap was that QUALITY 8/9/39 were not applied to this row | Round 27 commits a full registry run at the content revision: `.ufo/evidence/round-27/after/registry-2227d83.json` — `exit 0`, `held 49`, `total 49`, `superseded 7`, `rev 2227d833…`, registry sha256 `c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c` — plus the run's stderr. Shown able to fail: the same tool run from a clone with no sibling `*-shokunin` symlinks reads `REGISTRY_CHECK: held=46/49 superseded=7` with `repo_identity_mismatch` refusals (committed at `.ufo/evidence/round-27/after/registry-2227d83-no-mirror.stderr`), so the receipt is only a claim about a mirror-shaped environment. Caveat: this receipt landed at `2abb018`, **after** the content revision `2227d833`; at `2227d833` the `after/` directory holds no tracked file |

### Row D — the counter that accepted unrelated receipts

| Class | Evidence pointer | Captured-by | Fix / shown able to fail |
|---|---|---|---|
| A frozen counter that resolves a defect from a receipt not bound to the bytes that produced it | `corpus/lessons/round-26-verifier-spotcheck.md:225-228` (routed item 4: "`c2-measure.py` is gameable by prose tokens and unrelated receipts"; QUALITY 51's receipt check "does not tie a receipt to the tool bytes"); `corpus/lessons/round-26.md:96-100` (seat MutateC2Counter: `mismatches=0/3` with all three defects still present, via prose tokens, a stale or unrelated receipt, and a registry row that names only the path). **I reproduced the unrelated-receipt half independently** (§Commands): the round-26 counter reads `mismatches=0/3`, exit 0, against a synthetic repo whose only "receipt" is a file containing one line of unrelated output | QUALITY 54 (`corpus/QUALITY.md:603-611`, landed at `2227d833`): a counter that accepts a run receipt checks that the receipt names the sha256 of the tool bytes and of the input bytes at the measured revision; a receipt from other bytes counts as absent. QUALITY 51 (`corpus/QUALITY.md:560-574`) carried only the bound ("the receipt check does not tie a receipt to the tool bytes that produced it"), so 54 is the first rule that binds receipts to bytes | The new counter `.ufo/evidence/round-27/c2-measure.py:86-88` compares `receipt.probe_sha256` to sha256 of `anchor-probe.py` at the measured rev and `receipt.anchors_sha256` to sha256 of `anchors.json` at the measured rev, and its `:90-94` re-reads the pinned kumitate blob and checks it against `anchors.json`'s `blob_sha256`. Shown able to fail: I moved the bytes in a scratch clone and the counter printed `receipt not bound to probe and anchors bytes` and exited 1 with `classified=0` — once for a whitespace change in `anchors.json`, once for an added comment line in `anchor-probe.py` (§Commands). The base reading at `91edf9cd` prints the same message and exits 1. **Bound worth recording:** the receipt's own `target` block (repo, rev, path, blob_sha256 of the mutated file) is never read by the counter — I rewrote it to a dead revision and a zero digest and the counter still read `classified=4`, exit 0. The input bytes are pinned through `anchors.json`, not through the receipt, so QUALITY 54's "the receipt names the sha256 of the input bytes" holds only through the anchors file. Closing that would mean one more comparison in the counter |

## Evidence and commands

All commands ran read-only inside a scratch clone `/tmp/r27-scribe` (and
`/tmp/r27-scribe2`) made with `git clone --no-hardlinks`; the lane was never
written to, and no `jj` command was run anywhere. Lane inspection used
`GIT_OPTIONAL_LOCKS=0` git reads only.

### QUALITY 53 and 54 as landed at `2227d833`

```
$ GIT_OPTIONAL_LOCKS=0 git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:corpus/QUALITY.md | grep -n -E "^53\.|^54\."
591:53. Round 27. A round that edits a file traced as an input of a credited
603:54. Round 27. A counter that accepts a run receipt checks that the receipt
```

QUALITY 53 (`:591-601`) names `lessons/round-26-verifier-spotcheck.md:112-135` as
its capture and the round-27 counter as its falsifier. QUALITY 54 (`:603-611`)
names `lessons/round-26-verifier-spotcheck.md:225-228` (routed item 4) and the
round-27 C2 counter as its falsifier.

### QUALITY 40 was already in force at the round-26 base

```
$ GIT_OPTIONAL_LOCKS=0 git show d4140796f4e48e8ec81b793facba73fbd03b4443:corpus/QUALITY.md | grep -n "^40\."
364:40. A historical calibration receipt is not a current no-harm monitor.
```

Same line number at `e08444d3`. Text: "run the input-keyed ruler at the delivered
revision; a lower current score is named before asserting unchanged calibration."

### The lane knew the harm before the SCORECARD row landed

```
$ GIT_OPTIONAL_LOCKS=0 git log --oneline --diff-filter=A -- .ufo/waves/round-26/w1/ReviewMonitorHarm.md
40a12bf round-26: content landing …
$ GIT_OPTIONAL_LOCKS=0 git log -1 --format='%h %ci' d2206cd
d2206cd 2026-10-22 08:10:32 -0300
$ GIT_OPTIONAL_LOCKS=0 git log -1 --format='%h %ci' 40a12bf
40a12bf 2026-10-22 08:09:51 -0300
$ GIT_OPTIONAL_LOCKS=0 git show d2206cd:.ufo/waves/round-26/w1/ReviewMonitorHarm.md | head -12
… | calibration_restraint_score | 8 | 6 | …
```

The reviewer report (restraint 8 → 6) is in the tree one minute before the
SCORECARD measured row that reads "numeric 8 → 8".

### QUALITY 53 falsifier: the counter fails at the head, passes at the base

```
$ python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/r27-scribe --rev d4140796f4e48e8ec81b793facba73fbd03b4443
C1_MONITOR: covered=62/62 restraint=8 box3_mismatch=0 depth_score=8 rev=d4140796…      exit=0
$ python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/r27-scribe --rev e08444d3f2b40fc6734be4f1c57a56639add9c2d
C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1 depth_score=9 rev=e08444d3…      exit=1
$ python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/r27-scribe --rev 91edf9cd82ccc72e10f62f81d37181f549d593b8
C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1 depth_score=9 rev=91edf9cd…      exit=1
$ python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/r27-scribe --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647
C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2227d833…      exit=1
```

Committed base reading: `.ufo/evidence/round-27/c1-before.stdout` (exit 1) with
`C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1 depth_score=9 rev=91edf9cd…`.

C1 is not yet met at the head I can see:

```
$ GIT_OPTIONAL_LOCKS=0 git diff --stat 91edf9cd HEAD -- .ufo/evidence/round-21/coldread/ledger.json
(empty — ledger byte-identical to base)
$ GIT_OPTIONAL_LOCKS=0 git ls-tree -r --name-only HEAD -- .ufo/evidence/round-27/coldread/traces/ | wc -l
0
$ python3 .ufo/evidence/round-27/c1-measure.py --repo /tmp/r27-scribe2 --rev 2abb01812933bf9f7044b188daae0f18c1c0f6c4
C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1 depth_score=9 rev=2abb018…      exit=1
```

### Row C: the registry gap and its fix

```
$ find .ufo/evidence/round-26 -name "*registry*"
.ufo/evidence/round-26/after/registry-40a12bf.json        # nothing for 2b064cf or the head
$ python3 -c "import json;d=json.load(open('.ufo/evidence/round-27/after/registry-2227d83.json'));print({k:d[k] for k in ('exit','held','total','superseded','rev')})"
{'exit': 0, 'held': 49, 'total': 49, 'superseded': 7, 'rev': '2227d8338c02aa9a5fd7d95c1a41b76865ad7647'}
$ tail -1 .ufo/evidence/round-27/after/registry-2227d83-no-mirror.stderr
REGISTRY_CHECK: held=46/49 superseded=7
```

### Row D: the old counter accepts an unrelated receipt

Synthetic repo, `unrelated.stdout` contains only `MTE_SELFTEST: 17/17 pass`
(produced by nothing related to `tools/mte-interop.py`):

```
$ python3 .ufo/evidence/round-26/c2-measure.py --repo /tmp/r26-c2-demo/repo
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: RESOLVED
C2_ITEM R25-SPOT-3: RESOLVED
C2_RECORD: mismatches=0/3
exit=0
```

### Row D: the new counter refuses moved bytes

In `/tmp/r27-scribe` (scratch clone only), whitespace added to `anchors.json`:

```
C2_F8: survivors=4 classified=0 anchored_holes=0 rev=4e2a8da4…      exit=1
  S_OOR_EDGE: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
  S_STRICT: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
  S_USAGE: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
  S_PIN_INCLUDES: UNCLASSIFIED (receipt not bound to probe and anchors bytes)
```

A comment line added to `anchor-probe.py`: same message, `classified=0`, exit 1.

The receipt's `target` block rewritten to a dead revision and a zero digest, in
`/tmp/r27-scribe2`:

```
C2_F8: survivors=4 classified=4 anchored_holes=4 rev=f5073807…      exit=0
```

The counter never reads `target` (`grep -n target .ufo/evidence/round-27/c2-measure.py`
returns nothing). The unpinned field is `receipt['target']`.

## Touched surfaces

- Read only: `corpus/lessons/round-26.md`, `corpus/lessons/round-26-verifier-spotcheck.md`,
  `corpus/QUALITY.md`, `corpus/lessons/round-27.md`, `SCORECARD.md`,
  `.ufo/evidence/round-27/**`, `.ufo/evidence/round-26/**`,
  `.ufo/evidence/round-21/coldread/measure.py`, `tools/registry.json` (via receipts only).
- Written: this report only, `.ufo/waves/round-27/w1/ScribeMistakes.md`.
- Scratch: `/tmp/r27-scribe`, `/tmp/r27-scribe2`, `/tmp/r26-c2-demo`.

## Out of scope

- No edit to `corpus/lessons/round-27.md` or any other product file; the rows
  above are drafts for the L1 to take or leave.
- No run of `tools/registry-check.py` (the receipts are read from the lane's
  committed evidence; the registry is not mine to run).
- The round-27 F8 claim, the S012/S090/S091 rows and the kumitate pin were not
  re-judged here; only the receipt-binding rule is in scope for row D.
- The four open items the round-26 closure routed that are not in my item
  (leg-sum check, drift sentinel, kumitate holes) are untouched.

## Findings the judge should weigh

1. **Row A's fix is a method, not a landed result.** At lane HEAD `2abb018` the
   C1 counter still exits 1 at `covered=25/64 restraint=6 box3_mismatch=1`. The
   ledger is byte-identical to the base and no wave-1 trace is committed. A
   round-27 lesson that records the harm-repair as done would overstate it.
2. **The drafted row 1's "Captured-by: none in round 26" is too strong for the
   record half.** QUALITY 40 was in force at the round-26 base and covers
   asserting unchanged calibration without naming the lower current score.
3. **QUALITY 54 is only half implemented in the new counter.** It binds the
   receipt to the probe and anchors bytes, and pins the mutated blob through
   `anchors.json`, but never compares `receipt['target']` (repo, rev, path,
   blob_sha256). A receipt naming a dead target still passes.
4. **Row C needs no new criterion.** It is a QUALITY 8/9/25/39 application gap,
   now closed by committing the registry receipt at `2abb018` — one commit after
   the content revision, so at `2227d833` the receipt does not yet exist.
5. **The QUALITY 26 timing question is ambiguous.** The stale SCORECARD row was
   found by a non-author closure at round 26's close and corrected by the lane
   in round 27. I record it, I do not rule on it.
