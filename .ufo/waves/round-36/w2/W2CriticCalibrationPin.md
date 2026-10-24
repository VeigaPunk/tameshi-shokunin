# W2CriticCalibrationPin — attack on the calibration numeric-axis bookkeeping (6 vs 8)

Seat: critic (calibration). Read-only leaf; no subagents, no lane edits. Attack surface:
can a reader re-derive which calibration number is live — the r35-measured `6` or the
r36-measured `8` — and why? Target: `SCORECARD.md` at lane tip `fbb01cf`.

## Verdict line

**VERDICT: RE-DERIVABLE — live calibration is unambiguously `8` pinned at refresh commit
`b455001e`; the "why" is spelled out. One real defect: the `Current axes — re-stated at
round 31` table (SCORECARD.md:1528-1537) still presents calibration `8` measured at
`83c001a5`, "last-change 29; held 30" — a superseded duplicate authority that hands a
reader the right number for the wrong reason. Minor severity; does not defeat C1.**

## Commands run (all read-only; repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin`)

```
git log --oneline -14
git rev-parse / merge-base --is-ancestor over {34fa5b0, 796e08b, e423c41b, b455001e, HEAD}
git status --porcelain                          # only untracked .ufo/waves/round-36/w{1,2}/
git show --stat d9c496b fbb01cf e423c41b        # post-refresh deltas = receipts + 1 lesson
git diff --name-only b455001e..HEAD             # no cited input touched -> no re-drift
python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev HEAD
    # -> calibration_restraint_score 8, sections_covered 64, box3_full_page True (~31 s)
```

Plus `read`/`grep` of SCORECARD.md:1528-1537, :1695-1776, contract.json, the three
monitor receipts, `corpus/lessons/round-36-verifier-spotcheck.md`, and the w1 reports
`SimplifierSCORECARDRow.md`, `CriticC1Scope.md`.

## What the attack found — the live number and its chain

Commit topology: `34fa5b0` (r35 measured tip) → `5df962b` (r35 fold) → `796e08b` (r35
close, r36 base) → `e423c41b` (r36 content, do-nothing control) → `b455001e` (r36 refresh,
pin) → `d9c496b` (receipts) → `fbb01cf` (verifier spot-check) = HEAD.

Re-derivation path a reader walks:

1. `SCORECARD.md:1703-1711` — r35 measures `calibration 8 → 6` at tip `34fa5b0`; "the
   stale `8` this file carried from round 29-34 is superseded by the measured `6`".
2. `SCORECARD.md:1743,:1756-1765` — r36: monitor prints `6, 60/64` at `796e08b` and
   `8, 64/64` at the refresh commit; "the r35 numeric block's measured `6` is superseded
   by this measured `8` at the refresh commit … the pinned measurement commit is the
   refresh commit itself".
3. The "why" is also stated (:1763-1765): later record-keeping commits that touch the
   four headings' cited inputs re-trigger the input-drift rule by design — so the pin
   lives at `b455001e`, not at whatever HEAD happens to print. This preempts exactly the
   ambiguity the ticket probes.
4. Evidence agrees at every revision: receipts `after/monitor-at-796e08b.stdout` (6),
   `control/monitor-at-e423c41b.stdout` (6), `after/monitor-at-b455001e.stdout` (8);
   non-author closure `round-36-verifier-spotcheck.md:37-42` re-ran the monitor at all
   four revs including tip `d9c496b1` → 8, verdict "verified (re-measured)".
5. My own re-run at HEAD `fbb01cf` today: `8, 64/64` — the predicted re-drift did not
   fire (post-refresh commits touched only receipts + a new lesson file), so pin and tip
   currently agree. No 6-vs-8 divergence exists anywhere in committed history or live.

The strongest counterexample I could construct — "r35 pinned the *tip* measurement (6),
so by the same convention r36's pin should be a tip measurement, and post-refresh record
commits could make the tip read 6 again, leaving two live candidates" — fails on the
text: the r36 block explicitly declares the pin lives at the refresh commit *because* of
that drift mechanism, and at HEAD the monitor in fact still reads 8. The bookkeeping
names which number is live and why.

## Defect (minor, fixable) — stale duplicate authority for the same scalar

`SCORECARD.md:1528-1537`, `### Current axes — re-stated at round 31`, still presents the
calibration row as `8` with **Measured commit `83c001a5`** and **Last-change round
`29 (restored 6 → 8); held 30`**. That provenance is two supersessions stale:

- The `8` at `83c001a5` was voided by r35's measured `6` (`34fa5b0`); the current `8`
  comes from a different measurement event (`b455001e`), a different commit, and a
  different restoration. The correct live citation exists only in the r36 block.
- "Last-change 29; held 30" misstates history: the value changed at 35 (8→6) and 36
  (6→8). The companion saturation sentence (:1531-1532) is coincidentally true again,
  but its premise (8 held continuously since r29) is false.
- A reader who stops at the standing table — the file's designated "Current axes"
  authority — derives the right number for the wrong reason; the two authorities
  disagree on provenance for the same scalar. Calibration bookkeeping should not carry
  a silently superseded pin authority.

Smallest safe correction (append-only, one edit): append a `### Current axes — re-stated
at round 36` note/table pinning calibration `8` to `b455001e2589b3f4f471d94a3de7e5e549b9f54c`
with last-change "36 (restored 6 → 8); 35 (8 → 6 recorded)" — or a one-line marker under
the r31 table naming it stale-provenance, superseded in value-history by r35/r36.

## Secondary friction (not defects)

- "tip" denotes two commits across adjacent blocks: r35's block calls `34fa5b0` "the
  tip" (:1706); r36 calls `796e08b` "r35 tip" (:1743,:1757). Both were tips at their
  write time (`5df962b`, `796e08b` land after `34fa5b0`); reconcilable via `git log`,
  but "measurement tip" vs "closing tip" wording would remove the only real stumble.
- The measured-commit hash `b455001e` appears in SCORECARD only via the documented
  receipt-filename indirection (`monitor-at-<rev>.stdout`); it resolves to the real
  hash (receipts, LOG, spot-check `:5`, `git log`). Convention-consistent (round-12
  precedent); the hash would be stronger inline.
- Citation nits in the same block already filed by w1 `SimplifierSCORECARDRow.md`
  (control receipt named `monitor-at-content-commit.*` vs actual `…-e423c41b.*`;
  misquoted token `pub_kill_slots=0`); bookkeeping-adjacent, outside my axis slice.

## Scope honesty cross-check

The 8 is an input-keyed restoration, not a fresh blind cold-read — disclosed in the
receipts' scope line, the numeric paragraph, and the lesson `## Holds`
(w1 `CriticC1Scope.md` verdict: defensible). The bookkeeping claims exactly what the
instrument measured.

## Tooling / bounds

No tools installed or updated; `pacman` not run. No mutating git/jj commands; no writes
inside any checkout except this report. All paths used were absolute.
