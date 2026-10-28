# T56W1RevRound55Dispositions — R55.1–R55.7 disposition check

seat: T56W1RevRound55Dispositions (reviewer) · milestone: round-55 disposition check
lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` · base `981c5e8b` · freeze `c3e2ca9f`
sources: `corpus/lessons/round-55-verifier-spotcheck.md` (routed defects), `.ufo/evidence/round-56/contract.json`, the frozen instruments under `.ufo/evidence/round-56/`, wave-1 drafts (`w1/T56W1ScribeLesson.md`, `w1/T56W1ScribeScorecard.md`, `w1/T56W1ScribeQuality.md`, `w1/T56W1ScribeLog.md`), `spec-w1.json`/`spec-w2.json`/`build-spec-w3.py`.

## Verdict

One finding that blocks the round's own C2 target, one overclaim, five landings that hold.

- **F1 (blocking): R55.5's fix is wired so it cannot pass its own gate.** The frozen `controls.sh` emits each mutation control's `rev=` token as the *scratch-clone commit it just created* (`controls.sh:54–55` commits in `$D`, then `:35` passes `--rev "$(git -C "$repo" rev-parse HEAD)"`; the same for lines 72–73, 93–94, 110–111, 118–119). Those commits exist only in the clone. The deciding run's gate 0b (`deciding-run.sh:66–73`) and C2 arm 5 (`c2/measure.py:200–218`) gate `controls-a.stdout` as role `control`, which requires every `rev=` to resolve **in the lane** and be an ancestor of REV (`tools/receipt-revision-gate.py:60–69, 153–158`). Demonstrated below: lane revs only → PASS; one clone-commit rev → `RECEIPT_REV_UNRESOLVABLE`; resolvable but non-ancestor → `RECEIPT_CONTROL_NOT_ANCESTOR`. Every real phase-A mutation that *applies* creates exactly such a commit, so `controls-a.stdout` is refused iff the control set is meaningful. **Consequence: `own=PASS` is unreachable, `DECIDING_REFUSED receipt-binding` is guaranteed at the deciding run, and C2_R56_PASS can never be true.** The lesson draft's disposition row "R55.5 FIXED by C2" (T56W1ScribeLesson.md:151) is true of the rule and false of the round: the fix exists and cannot be satisfied under the frozen controls as written. Fix requires an amendment to `controls.sh` (emit `rev=$PIN` plus a non-`rev=` clone-commit field, demonstrated below) or to the gate's `control` role — either one must land via a new freeze commit **before** the deciding run, since `FROZEN_UNCHANGED` (`deciding-run.sh:79–80`) makes a post-freeze edit to either file a refusal of a different kind (rc=1 on the FROZEN line, not `DECIDING_REFUSED`).
- **F2 (overclaim): R55.4 "FIXED by construction".** `deciding-run.sh` refuses missing control *files* and missing `CONTROLS_*` verdict *lines* (control-receipt-missing, controls-*-verdict-missing); it never compares a report sentence to a receipt. A sentence like round-55's "`CTL_SKIP_c2` was still running at filing" can still be written over a committed `controls-a.stdout`. `T56W3RevRecord` audits "every number, commit hash and quoted verdict line" — a *status claim* is none of the three, so it has no falsifier either. Correct disposition is `carried` (order-of-operations improved, prose unguarded), or `T56W3RevRecord`'s table must be extended to cover status claims about receipts.
- R55.1, R55.2, R55.3, R55.6, R55.7 are disposed as the draft says; two have weak carriers noted below.

## Row per defect

| id | defect | disposition this round (recommended) | draft says | can the fix fail? | carrying receipt |
|---|---|---|---|---|---|
| R55.1 | no C2 verdict at the measured revision | **fixed-this-round** | FIXED | yes — gate 0c (`deciding-run.sh:100–108`) runs the gate on the verdicts the run just produced with a `C*_R56_PASS=` required line; a verdict naming another revision → `RECEIPT_REV_MISMATCH`/`RECEIPT_REV_ABSENT`, and round-55's own truncated receipt already refuses `RECEIPT_REV_ABSENT` (`before/c2.stdout` `red55=`). Residual: the receipts are produced in `$OUT` (working tree); committing them is L1's unenforced step | `.ufo/evidence/round-56/after/{c2.stdout,receipt-gate-verdicts.stdout,deciding-run.exit}`; counter `--explain` output contains no stray `rev=` (checked c1/measure.py:290–297, c2/measure.py:263–272 — only the verdict line carries `rev=`) |
| R55.2 | a quoted total its own receipt contradicts | **carried** — draft already honest ("no instrument exists") | "FIXED by record discipline, carried" | the audit is a seat (`T56W3RevRecord`, build-spec-w3.py:91–92), not a falsifier; ScribeQuality demonstrated the quote half is unmined (`107-scope-gap-fabricated-line.txt`, a fabricated line passed, exit 0). It can *be shown wrong* only by the seat's table | `w3/T56W3RevRecord*` record-versus-receipt table; the round-55 anchor: `w1/T55W1ScribeSkill-receipts/c2-integrated.out:44` (`total=1 C2_R55_PASS=false` vs the report's quoted `total=0`) |
| R55.3 | instrument regressed, row still asserts 8 | **fixed-this-round** | FIXED | yes — C1 arm 6 (`c1/measure.py:267–285`) takes the last `calibration` row and requires score == monitor reading at the named commit, with CTL_RESTATE_c1 (row asserts 9 → false) as its kill control and MutCounterArms M7/M8 as mutant probes. Scorecard draft (w1/T56W1ScribeScorecard.md:44) already writes 6 at base | `after/c1.stdout` (`restate=` arm, `total=0`), `control/controls-a.stdout` `CTL_RESTATE_c1`, `after/coldread-precheck.stdout` |
| R55.4 | stale control sentence | **carried** — overclaimed in draft ("FIXED by construction", F2) | FIXED by construction | no falsifier covers report prose; order of operations prevents a missing receipt, not a stale sentence | only `w3/T56W3RevRecord*` if its scope is extended to status claims; otherwise prose |
| R55.5 | deciding gate cannot compare the revision it certifies | **blocked — fix exists, cannot pass as wired** (F1) | FIXED by C2 | yes, and that is the problem: it refuses the round's *own* controls | today: `DECIDING_REFUSED receipt-binding` + `C2_R56 ... own=REFUSED`; after a controls amendment: `receipt-gate.stdout` PASS |
| R55.6 | uncommitted round work at closure | **fixed this round, partially** — sweep done, forward gate partial | FIXED for inherited + gated going forward | dirty-tree refusal exists (`deciding-run.sh:75–77`) but only at the deciding moment — files created after it (the report, wave-3 seats' late receipts) are ungated; the class already recurred this round: `.ufo/evidence/round-56/before/` and the wave-1 dir are untracked now (`git status` shows `?? .ufo/evidence/round-56/before/`, `?? .ufo/waves/round-56/`) | `after/clean-tree-{before,after}.txt` at the deciding run; closure-time cleanliness has **no receipt** — no w1–w3 seat runs `git status` at the tip (0 hits for `porcelain\|git status` in build-spec-w3.py) |
| R55.7 | closure-seat contamination | **partially disposed** — draft correct | PARTIALLY DISPOSED | lane side is a revert, not a fence; not lane debt | `git show 6efd2a1 --stat` (reverted files); contract `base_note`; T56W1RevInherited seat audit |

## F1 — the demonstrated blocker (commands and outputs)

Setup (scratch only; the lane was never mutated — `git clone --shared` reads it, the fixture commit lives in the clone):

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r56/T56W1RevRound55Dispositions
git clone --quiet --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
git -C "$S/clone" checkout --quiet --detach c3e2ca9f020776b3d66c7af854fb82c834674fcf
git -C "$S/clone" rev-parse --show-toplevel   # asserted == $S/clone before any commit
printf 'mutation\n' >> "$S/clone/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout"
git -C "$S/clone" -c user.name=control -c user.email=control@invalid add -A
git -C "$S/clone" commit --quiet -m 'control: probe mutation'
C=$(git -C "$S/clone" rev-parse HEAD)        # 9f139d42dc137ddadc3b670b44e095fcea5230fa
```

1. The lane cannot see the clone commit — the object a `control`-role receipt would name does not resolve (`receipts/lane-resolve.txt`):
   `git -C "$LANE" rev-parse --verify --quiet "$C^{commit}"` → **exit 1**; `git -C "$LANE" cat-file -e "$C"` → `LANE_SEES=no`.
2. A `controls-a.stdout` whose CTL lines name only lane revisions (base + freeze) passes role `control` at the freeze (`receipts/gate-control-certified-freeze.txt`): `GATE OK ... verdict=PASS`, exit 0.
3. The same receipt with one mutation control's `rev=` being the clone commit → refused (`receipts/gate-control-with-clone-rev.txt`):
   `GATE REFUSED ... role=control ... code=RECEIPT_REV_UNRESOLVABLE rev=9f139d42dc...` exit 3.
4. Even where the control commit *is* resolvable (run the gate with `--lane "$S/clone"` — i.e., a universe where the lane could see it), it is the *child* of PIN, not an ancestor of the certified revision (`receipts/gate-control-lane-is-clone.txt`):
   `code=RECEIPT_CONTROL_NOT_ANCESTOR rev=9f139d42dc...` exit 3. Fetching the clone commits into the lane therefore cannot fix it either — they branch off PIN, they are not ancestors of REV.
5. The escape: rewrite the emitted token so `rev=` names the lane revision the clone descends from, and record the actually-measured commit under a non-`rev=` field (RE does not see `clone=`). Demonstrated (`receipts/gate-control-amended.txt`): `CTL CTL_SKIP_c1 C1_R56: rev=c3e2ca9f0207 ... clone=9f139d42dc...` → `verdict=PASS`, exit 0.

Why "the counter must measure the clone commit" is not an objection: the control is evidence that the counter can go *false* on content derived from the certified revision — the lane-revision binding is semantically correct for role `control`, and the real measured commit stays recorded in the line. Proposed minimal change (to `emit`'s callers in `controls.sh` — a freeze amendment, diff below for the L1; do NOT apply post-freeze):

```diff
 emit() { # emit NAME EXPECTED ACTUAL VERDICT_LINE
-  local name=$1 want=$2 got=$3 line=$4
+  local name=$1 want=$2 got=$3 line=$4 clone_rev=${5:-}
+  [ -n "$clone_rev" ] && line="$(printf '%s' "$line" | sed "s/rev=[0-9a-f]\{7,40\}/rev=$(git -C "$LANE" rev-parse --verify "$PIN" | cut -c1-12)/") clone=$clone_rev"
   echo "CTL $name $line"
   ...
 }
```
with callers passing `$(git -C "$D" rev-parse HEAD)` for the five mutation controls. (Exact placement left to the L1's amendment; the mechanism is proved by receipts 2–5.)

## F2 — R55.4's overclaim, precise

`deciding-run.sh` checks *receipt existence* (blob, non-empty, committed after the freeze) and *verdict-line presence* (`CONTROLS_A:`/`CONTROLS_B:`). No instrument compares prose to receipt. Round-55's own R55.4 was a status sentence (`"still running at filing"` vs a committed `total=4` verdict) — the class is exactly `T56W3RevRecord`'s blind spot unless its table explicitly covers status claims. Recommend: carry the disposition as `carried`, with the receipt `w3/T56W3RevRecord*` listing each control-status claim in the records and the receipt line it must agree with.

## Sweep notes

- Instrument reads: `deciding-run.sh` (gates 0b/0c at :66–73, :100–108; dirty-tree :75–77; FROZEN :79–80), `controls.sh` (emit :20–25, mutation commits :54,72,93,110,118), `controls-b` emit path (:127–128 — phase B has **no** mutation commit, HEAD stays PIN, so `controls-b:positive` is satisfiable), `c2/measure.py` (arm 5 :200–218), `c1/measure.py` (arm 6 :267–285; explain emits no stray `rev=`), gate roles (:153–158), no-harm.sh (15 monitors, none for closure cleanliness or report quotes).
- Checked all 37 w1 items, all w2 item names, all w3 `add()` names: the only seat auditing report-vs-receipt is `T56W3RevRecord`; **no seat verifies committed cleanliness at closure**; `T56W3MutGate2`'s instruction "run the gate on the round's own receipts at PIN … confirm verdict=PASS" cannot hold under frozen controls.sh — that seat will report REFUSED and should be told to expect it.
- `.ufo/evidence/round-56/after` is absent at freeze and was a stray 0-byte file on disk when I started; it is now a directory (L1-created). `deciding-run.sh` requires `[ -d "$OUT" ]` — noted so the L1 doesn't hit `outdir-missing`.
- C1 side checks: `explain` notes carry no `rev=` token outside the verdict line (so gate 0c `verdict` role cannot trip on `RECEIPT_REV_AMBIGUOUS`); arm 6 picks the *last* calibration row, so the restated row must be the last one matching the 5-cell shape (the scorecard draft's proposed row at :44 satisfies: score 6, commit `981c5e8b`, evidence names the round-21 monitor command, last-change `56`).

## Residual risk and verification gaps

- **C2's own arm 5 + gate 0b are guaranteed REFUSED until the freeze is amended** — the single most important thing for the L1 to hear. If the wave runs to the deciding stage unamended, the round burns a deciding run on `receipt-binding`.
- The amendment needs a new freeze commit; `deciding-run.sh`'s freeze-integrity re-derives from `freeze.json` at the FREEZE argument, so a re-frozen `FREEZE2` with updated digests passes integrity — but the contract and prompt name `c3e2ca9f` as the freeze of record; any amendment must be disclosed in `freeze.json`'s `amendments` list and in the report.
- `verify` gap left intentionally: I did not run `controls.sh` end-to-end (needs a PIN that does not exist; ExecControls' synthetic-PIN dry run will hit the same wall); the mechanism is demonstrated component-wise instead.
- R55.6's closure-time arm has no instrument; the honest carrier is the next round's base sweep, as the scorecard draft itself proposes (:85–86).

## Receipts index (`-receipts/`)

`lane-resolve.txt` (lane can't see the clone commit, exit 1) · `controls-a-probe.stdout` (base+freeze+clone revs) · `controls-a-noclone.stdout` (base+freeze only) · `controls-a-amended.stdout` (rev=PIN + `clone=` field) · `gate-control-certified-freeze.txt` (lane revs → PASS) · `gate-control-certified-freeze-with-clone.txt` / `gate-control-with-clone-rev.txt` (clone rev → `RECEIPT_REV_UNRESOLVABLE`, exit 3) · `gate-control-lane-is-clone.txt` (resolvable clone rev → `RECEIPT_CONTROL_NOT_ANCESTOR`, exit 3) · `gate-control-lane-revs-only.txt` (same receipt certified at *base*: `RECEIPT_CONTROL_NOT_ANCESTOR` on the freeze rev — expected, freeze isn't an ancestor of base) · `gate-control-amended.txt` (amended form → PASS, exit 0).

## Dispositions table the L1 should file

| id | file as |
|---|---|
| R55.1 | fixed-this-round (gate 0c; receipt `after/receipt-gate-verdicts.stdout`) — carrier uncommitted until the L1 commits `after/` |
| R55.2 | carried — receipt `w3/T56W3RevRecord*`; QUALITY 107 scope sentence names the unmined half |
| R55.3 | fixed-this-round — receipts `after/c1.stdout`, `control/controls-a.stdout CTL_RESTATE_c1` |
| R55.4 | carried — no falsifier; extend `T56W3RevRecord` to status claims or admit prose |
| R55.5 | **blocked-as-wired** — needs a controls/gate amendment inside a new freeze commit before the deciding run; then fixed, receipt `after/receipt-gate.stdout` |
| R55.6 | fixed, partially — sweep + dirty-tree gate; closure-time arm stays carried |
| R55.7 | partially disposed — lane side reverted at `6efd2a1`; harness side is not lane debt |

No lane production files were edited; no frozen instrument touched; all git mutations (one fixture commit) were inside the scratch clone whose top-level was asserted; `rm -rf` on scratch per seat rules. Tools installed: none.
