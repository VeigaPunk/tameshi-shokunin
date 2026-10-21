# FinalClaimOrigin — round-19 w1 findings (final-revision claim provenance, R18-5)

Date: 2026-10-21. Seat: read-only investigator, lane `tameshi-shokunin`.
Serves C1 (calibration) verification boundary only: recover the exact provenance of
the round-18 fleet report's final-revision 60/60 sentence and the correction text.
No production edits, no report edits, no lane gate/selftest/measure tool executed,
no installs. All paths absolute or lane-relative under
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

## 1. The claim (exact location and wording)

Fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/tameshi.md`,
committed once as fleet `a85e4d87f48c5f2f6bb885f2e09176e8f5fc9756`
(2026-10-20T18:50:39-03:00, "tameshi report — depth8, eleven bounded defect
closures, strict60/60"). `git log -- <report>` shows exactly one commit; the file
has never been amended.

- Line 53, "Before → after measurements" item 3: "…Strict `measure.py --rev
  a85f710… --explain` → **60/60, box3 true, restraint8, overrides_used=false**,
  exit0 (`final/measure-final-60.json`); **the same no-override count at final
  `4b7c682…` returned 60/60,8, exit0.**" — the final-revision claim (defect R18-5).
- Line 77, SHONEN Box3: "strict60/60 at `a85f710…` **and final tip**" — same
  assertion in compressed form.

Reading of "60/60,8": sections_covered 60/60 and calibration_restraint_score 8,
no overrides, strict gate — matches the receipt schema of
`.ufo/evidence/round-18/final/measure-final-60.json`.

## 2. Backing state at round-18 time (observed)

- The only committed measurement receipts in the round-18 bundle:
  `final/measure-final.json` (revision `a134a09…`, 59/60, box3 false, restraint 6)
  and `final/measure-final-60.json` (revision `a85f710…`, 60/60, restraint 8).
  `final/checks.json` has eight argv rows, all pinned at tool revision
  `921ef807…`; it contains no measure row.
- Tree-level absence, first-hand: `git grep -n 4b7c682 4b7c682 -- .ufo/ SCORECARD.md
  SHONEN.md LOG.md` → **zero hits**. The cited revision's own committed tree named
  itself nowhere — no receipt, no LOG/SCORECARD mention. Grep over the working
  tree's `.ufo/evidence/round-18/`, `.ufo/waves/round-18/`, and coldread also
  returns zero `4b7c682` hits: no seat report or L1 trace records a run either.
- Timing: lane tip `4b7c682` created 18:49:16-03:00; fleet report committed
  18:50:39-03:00. An unrecorded run inside that 83-second window was physically
  possible [INFERENCE], but no retained artifact records any such run.
  The watchdog log records missions, not commands (only a `chousa` launch line at
  18:49:48 in that window).

**Verdict: the sentence was unbacked at landing.** Its values, however, were
tree-true: the round-19 replay (§3) reproduces exactly the declared fields
(60/60, restraint 8, overrides false, strict; sources 76 rows, mined 48, queued
23, rejected 5 — identical in the `a85f710` receipt).

## 3. Repair provenance (observed; lane HEAD moved during this session)

Lane commit sequence (all `git log` verified; `7243e7f` is ancestor of both):

| Time (−03:00) | Commit/event | Content |
|---|---|---|
| 10-20 18:47:45 | `a85f710` | T2 refresh; strict 60/60 receipt created at that rev |
| 10-20 18:49:16 | `4b7c682` | lane tip; carries `measure-final-60.json`; no self-naming receipt |
| 10-20 18:50:39 | fleet `a85e4d8` | report with the unbacked sentence |
| 10-21 02:28:10 | `78b99dd` | freeze: `.ufo/evidence/round-19/contract.json`, population R18-1…R18-5; R18-5 = "fleet round-18 report final-rev claim — no committed 60/60 receipt at 4b7c682…" |
| 10-21 02:28:25 | replay run | `.ufo/evidence/round-19/round18-final-measure.json`: argv `python3 .ufo/evidence/round-18/measure.py --repo …/tameshi-shokunin --rev 4b7c6823a462f5ea2eafcb262275300a545f3ed7 --explain`, exit 0, `recorded_at 2026-10-21T05:28:25.715990+00:00`, GIT_*-stripped env; stdout sha `55c530bb…`, empty stderr |
| 10-21 02:48:27 | `21e7932` | corrections land: knowledge-entry errata, lesson errata, replay receipts, `before.json` (baseline `7243e7f`: corrected 0 / open 5 / exit 1), ruler blob sha `c538c33d…` (== `ruler_sha256` pinned in both receipts) |
| 10-21 02:53:30 | file created | `round18-final-measure-instrument.json` — companion identity metadata, initially uncommitted |
| 10-21 02:58:18 | `7af123b` | "harden correction predicates…": hardened ruler (worktree/HEAD sha `e9b44cad…`), `after-21e7932.json` (corrected 5 / open 0 / total 5, `ruler_sha256 c538c33d…`, 13 input digests), instrument file committed |

Digest identity, re-computed by me with `sha256sum` (not trusted from prose):
- `round18-final-measure.json` content sha `a9536bfb…` == instrument
  `receipt_sha256` == after-receipt input pin.
- replay stdout content sha `55c530bb…` == receipt `stdout_sha256` == after-receipt
  pin; stderr is the empty-file sha `e3b0c442…`.
- `.ufo/evidence/round-18/measure.py` content sha `7ca87a7c…` == instrument
  `instrument_sha256` == ruler constant `MEASURE_SHA18`; identical via
  `git cat-file blob` at **both** `4b7c682` and `21e7932` — the replay instrument
  bytes equal the tool committed at the measured revision.
- replay stdout fields: revision==rev_input==`4b7c682…`, sections 60/60,
  box3_full_page true, restraint 8, overrides_used false, trace_gate strict,
  ledger guardrail 8/8/8/8.

Failure-capability (from the committed ruler bytes, read not executed): the R18-5
predicate requires exact argv, revision==REV18, exit==0, `recorded_at ≥ FREEZE_TIME`
(2026-10-21T02:28:10-03:00 — so no pre-freeze artifact can satisfy it), bound
stream digests, 60/60 + restraint 8 + overrides false, instrument identity pins,
and the lesson phrase "does not claim the receipt existed in round 18". At
baseline `7243e7f` all five inputs are absent (`null` pins in `before.json`) →
open=5, exit 1.

## 4. Divergences and residual precision (all observed unless marked)

1. **Timeliness is not repaired and is not claimed to be.** The replay proves the
   measured content of `4b7c682` as blobs; it does not evidence that the count was
   executed at report time. Whether an actual run happened in the 83-second window
   is [UNKNOWN] — no retained record either way. Lane texts say exactly this:
   LOG round-19 entry "Neither new receipt is represented as having existed in
   round18"; lesson errata "repairs missing evidence, not its original timeliness".
2. **`after-21e7932.json` is a weak-ruler artifact.** Its `ruler_sha256` is the
   `21e7932`-era ruler `c538c33d…`; it first landed at `7af123b` together with the
   hardened ruler `e9b44cad…`, so no committed receipt is pinned to the hardened
   ruler. The hardened predicate additionally requires the instrument file, which
   at `21e7932` was not in the tree (committed only at `7af123b`). A re-run of the
   hardened ruler at HEAD should pass (all pins committed), but no such receipt
   exists yet — a precise, non-blocking gap for whoever re-audits C1.
3. **Under-pinned inputs map.** `frozen-runs.json` promises sha pins "for every
   observed blob", yet `after-21e7932.json`'s inputs omit the instrument file the
   hardened ruler observes (it is pinned only transitively via its own committed
   content). Minor specification drift, not a digest failure.
4. Instrument file `recorded_at` 05:53:30Z postdates the replay it describes and
   the landing commit; its own `scope` field discloses this ("added round19 after
   replay; not a rewritten historical receipt"). Consistent with its 02:53:30
   mtime; noted so no one reads it as a round-18 or at-landing artifact.

## 5. Correction text (identified; report unchanged)

Already landed lane-side (verified in tree):
- `corpus/lessons/round-18.md`, "## Errata R18-4 / R18-5 — receipt attribution
  (2026-10-21, round 19)" (landed `21e7932`): R18-5 paragraph names the missing
  receipt, the replay receipt, exit 0 / 60-of-60 / restraint 8 / no overrides,
  and closes: "This repairs missing evidence, not its original timeliness: it does
  not claim the receipt existed in round 18, nor that 60/60 holds at any round-19
  revision. The fleet report is not rewritten."
- `LOG.md` round-19 entry (line ~1147) and `SCORECARD.md` round-19 block
  (lines ~685+) record the same, with the R18-5 defect named in
  `.ufo/evidence/round-19/contract.json`.

Proposed fleet-side errata text (append-only, dated, named) — **not applied by
this seat**; the report must stay byte-identical:

> ## Errata (2026-10-21, round 19 — receipt attribution, verifier §5.5)
>
> "Before → after measurements" item 3 and SHONEN Box3 stated a 60/60,
> restraint-8 no-override count at final `4b7c682` with exit0. At landing
> (fleet `a85e4d87`, lane `4b7c682`) no receipt named that revision; the only
> committed strict receipts were `final/measure-final.json` (`a134a09`, 59/60)
> and `final/measure-final-60.json` (`a85f710`, 60/60). A historical replay now
> exists — `.ufo/evidence/round-19/round18-final-measure.json` (rev `4b7c682`,
> exit0, 60/60, restraint 8, `overrides_used=false`, recorded
> 2026-10-21T05:28:25Z; population item R18-5 frozen at `78b99dd`) — confirming
> the values but not contemporaneity: it does not claim the measurement was
> executed at report time, nor that 60/60 holds at any round-19 revision.

## 6. Verification commands (all read-only)

`git log/show/grep/ls-tree/cat-file/diff --stat/merge-base --is-ancestor/
rev-parse/status --porcelain`; `grep`, `sha256sum`, `stat`, `ls`, `cat`.
Lane state check at session start: HEAD `21e7932`, later observed `7af123b`
(the L1 landed the hardening commit mid-investigation). No lane-owned
gate/selftest/monitor/measurement tool was executed; `measure.py --check` was
deliberately not run (receipt-argv execution is out of my bounds). No installs,
no production or report edits; this Report trailer is my only write.
