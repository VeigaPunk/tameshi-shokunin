# CriticCalibration — round 42 wave 2 (FALSIFY): attack on C1 as a calibration improvement

Seat `L1Tameshi42.CriticCalibration` (critic, leaf). Read-only on the lane; the only lane write is
this report. Scratch clone `/tmp/tameshi-r42w2-CriticCalibration-1` (`git clone --shared`, branched
at freeze `322b5cd`) was deleted before return. No tools installed or updated. Access date 2026-10-25.

Counter (pinned, sha256 `9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e`,
verified by `sha256sum`): `.ufo/evidence/round-42/calibration/measure.py`.
I ran no default-mode lane run after `a21845f`. The one lane run is labelled PRE-RUN below.

## F1. A do-nothing control reaches the target: six non-repair commits score `C1_R42_PASS=true` (counterexample)

Setup: a scratch clone at the freeze. V0 adds only three-word round-42 records: the lesson is
`lesson\n`, and SCORECARD and LOG each get the heading plus `ok`. Each variant is one commit on top
of V0. Every run used:
`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/calibration/measure.py --lane /tmp/tameshi-r42w2-CriticCalibration-1 --rev HEAD --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`

| variant | single change on top of V0 | counter line (abridged) | exit |
|---|---|---|---|
| V0 records only (= contract `do_nothing_control` scenario 2) | none | `m10=1 total=1 records=6 C1_R42_PASS=false` | 1 |
| V1 corrupt the stale receipt | append one byte `x` to `.ufo/waves/round-41/residual/receipt.json` | `m10=0 total=0 records=6 C1_R42_PASS=true` | 0 |
| V2 delete the stale receipt | `git rm .ufo/waves/round-41/residual/receipt.json` | `total=0 … C1_R42_PASS=true` | 0 |
| V3 delete the seat report, so the tree now agrees with the false claim | `git rm .ufo/waves/round-41/residual/ResidualReceipts.md` | `total=0 … C1_R42_PASS=true` | 0 |
| V4 edit the receipt in place | flip `false`→`true` inside the committed receipt | `total=0 … C1_R42_PASS=true` | 0 |
| V5 rename the key | `"present"`→`"present_at_dispatch"` in the committed receipt | `total=0 … C1_R42_PASS=true` | 0 |
| V6 move it out of scope | `git mv` the receipt to `.ufo/evidence/round-41/residual/receipt.json` | `total=0 … C1_R42_PASS=true` | 0 |
| V7 the claimed repair (supersede JSON from `a21845f`) with three-word records | add `.ufo/waves/round-42/supersede/round-41-residual-receipt.json` | `total=0 … C1_R42_PASS=true` | 0 |

Every run printed `self_pin=1 sources_rows=109`.

Why these pass:
- `receipt_audit` drops any JSON that does not parse: `except Exception: continue` (measure.py:193-196).
- It scans only files currently tracked under `.ufo/waves` (measure.py:190).
- It compares each claim with the tree only at REV (measure.py:204). Nothing compares REV with the
  receipts or reports tracked at FREEZE.
- No append-only guard exists anywhere: `ls tools | grep -iE 'append|guard|immut|frozen'` returns
  nothing, and `.git/hooks` is empty.

Contract and record coverage:
- The contract's `do_nothing_control` (contract.json:23) covers only two cases: no superseding
  receipt, and a bad superseding receipt (selftest T2_*, measure.py:298-315). It does not cover
  destroying or rewriting the superseded receipt, or deleting the report.
- The round-42 lesson's "limits" list (corpus/lessons/round-42.md:125-140) discloses malformed
  *new* receipts and content-blind supersedes. It does not disclose V1–V6.

The prompt rule is at `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-42.md:364-368`:
"Before freezing, build the cheapest control that skips the claimed work … if it meets the target,
the counter or target is wrong". The cheapest control is the one-line `git rm` in V2, and it meets
the target. V3 is worse than a do-nothing: it is a harm path, deleting a 24 KB real seat report,
and it scores as a calibration pass.

## F2. The landed tip took the honest append route; the instrument just cannot tell it apart

- PRE-RUN (labelled; not the deciding run):
  `python3 …/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
  printed `m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=113 … C1_R42_PASS=true`, exit 0.
- `git diff --stat c77c2b7… a21845f… -- .ufo/waves/round-41/` printed nothing, so the round-41
  receipt and reports are untouched.
- `git diff --stat --diff-filter=DMR 322b5cd… a21845f… -- .ufo/waves/` printed nothing, so no
  tracked wave file was deleted, modified or renamed between freeze and tip.
- Selftest: `C1_R42_SELFTEST: cases=9 failed=0`.

So the work wave 1 landed is not gamed. But a pass from the frozen counter is not evidence of that.
The evidence comes only from the history witness above, which is outside the predicate.

## F3. Real self-assessment improvement, or bookkeeping? Bookkeeping

- The stale claim was true when it was written. The receipt and the report both land in `b14ff11`
  (`git log -- <each path>` returns the same single commit). The lane's own records say the receipt
  "was written before that report landed" (corpus/lessons/round-42.md:113;
  corpus/lessons/round-41-verifier-spotcheck.md:70). The defect was a snapshot left stale by a late
  seat. It was never a wrong judgment by the lane about its own quality.
- The repair is a 40-line JSON whose eight booleans are exactly what
  `git cat-file -e REV:<path>` returns. It contains nothing that path resolution alone does not
  already give. CriticSupersedeGaming (w1) showed that path resolution is the only thing m10 checks.
- The lane's own SCORECARD says the calibration scalar does not move: "Neither claim edits the
  runner or a SHONEN box, so neither number is expected to move. C1's gain is record agreement"
  (SCORECARD.md:2008-2012). The lesson says "No box moves this round"
  (corpus/lessons/round-42.md:107).
- From base to target, C1 changes two things: one dispatch-receipt boolean (m10 1→0), and
  `records` 3→6 because the round writes its own records. V7 shows that three-word records satisfy
  the records gate. So the records half measures that files exist, not that they are accurate.

## F4. Does C1 satisfy "a calibration claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state"?

The full rule is at tameshi-round-42.md:360-361. C1 satisfies it in form only.

- It satisfies the form: it is a count (m6/m7/m8/m10/m11), not an assertion.
- SHONEN is never compared with repo state. `SHONEN.md` appears in the counter only as a
  resolvable path name (measure.py:83, `grep -n SHONEN` gives one hit).
- The only class that reads a SCORECARD claim is m6, the standing sources-registry row count
  (measure.py:224-233). It was already 0 at base (`before/c1-at-base.stdout`) and does not move.
- The class that moves, m10, audits wave-dispatch receipts about whether a seat's report file
  exists. That is orchestration bookkeeping, not the lane's SCORECARD/SHONEN self-assessment.
- m7, m8 and m11 audit whether citations in the round's own new records resolve. That is
  record hygiene, measured on text this round wrote.

The rule is met in letter, through m6, which is zero throughout. The moved quantity is outside the
self-assessment the rule names.

## Impacted axes

- calibration: the claim's validity as an axis move. F1 breaks the prompt's do-nothing-control
  rule; F3 and F4 make the gain bookkeeping.
- no-harm: V3, deleting a real report, scores as an improvement.

Wave 1 already covered the content-blind supersede spoofs (CriticSupersedeGaming) and the
key-schema gaps (ExecC1Falsify f1–f6). F1 is new: it attacks the *superseded* receipt and the
*report*, not an added receipt.

## Smallest safe correction

The counter is pinned, so it cannot be changed after data in round 42. Three steps:

1. **Round 42 (disclosure only, no rule change):** add V1–V6 to the lesson's C1 limits. Attach the
   F2 history witness (`git diff --stat --diff-filter=DMR <freeze> <measured> -- .ufo/waves/`
   empty) to the deciding receipt as a labelled non-predicate check. Restate C1 in the SCORECARD
   as a record-agreement repair whose instrument does not discriminate, not as a calibration gain.
2. **Round-43 successor counter:**
   - m10 counts every receipt or report tracked under `.ufo/waves/` at FREEZE that is deleted,
     renamed or modified at REV, except files under the round's own dir.
   - A tracked `.json` under `.ufo/waves/` that does not parse counts as m10, instead of being
     skipped.
   - Add selftest cases T2_delete_receipt, T2_corrupt_receipt and T2_delete_report.
3. **Tradeoff for the judge (not fixable in the counter):** a calibration claim whose moving class
   is dispatch receipts does not track the SCORECARD/SHONEN self-assessment the prompt names. A
   successor should move a class that reads SCORECARD/SHONEN claims, for example the three SHONEN
   boxes the lesson lists as having no standing check (corpus/lessons/round-42.md:100-105).

BROKEN: the frozen C1 target is reachable without the repair. Deleting, corrupting, editing in place, re-keying or moving the stale receipt, or deleting the report it disputes, each scores `total=0 C1_R42_PASS=true` with three-word records (do-nothing-control rule, tameshi-round-42.md:364-368). The moved quantity is one stale dispatch-receipt boolean, not a SCORECARD/SHONEN self-assessment mismatch, so C1 is bookkeeping and not a calibration improvement. The landed tip itself is honest (append-only witness empty).
