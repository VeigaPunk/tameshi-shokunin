# T50Disp40 — C1 disposer, round-40 spot-check (items R40.1–R40.5)

Seat: `T50Disp40` (C1 disposer, round 40). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
read at base `e3729de862f73ae080d98fcf522a7081ce16e40a`; routed items from
`corpus/lessons/round-40-verifier-spotcheck.md` (`routed_at` `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`),
keys and text from the frozen `.ufo/evidence/round-50/c1/defects.json` (sha256 pin verified by the
counter: `defects_pin=0`). Dispositions: **2 fixed, 2 open, 1 declined**. Both fixes predate base
(`b37ce974`), so this seat contributes 0 to the `fixed_after_base_min=5` floor. Deliverable rows:
`.ufo/waves/round-50/w1/T50Disp40.rows.json`; receipts: `T50Disp40.receipts.md`. Scratch clone
`/fast/scratch/hyaku/tameshi-r50/T50Disp40/lane`, removed before yield.

## R40.1 — quarantine summary contradicts its own table → **fixed**

The ask (spot-check `:293-301`) is that `corpus/lessons/round-40.md` closes the Gate with "One row
adopted, seven refused (…), nine present-but-not-appended" while its own table and the report say one
adopted, six refused, ten present; the prescribed fix is "an appended correction in the round-41
lesson — do not rewrite the closed round-40 file in place". That correction exists:
`corpus/lessons/round-41.md:51-58` ("### Correction — the round-40 quarantine summary" … "counts one
adopted, six refused, ten present-but-not-appended. The table is the record; the summary sentence is
the drift"), added by `b37ce974b6efb8c465626d7346149549a3300a4b`
(`git log -S'counts one adopted, six refused, ten present-but-not-appended' e3729de8 -- corpus/lessons/round-41.md`);
`git log -1 -- corpus/lessons/round-40.md` → `46781274`, so the closed file was not rewritten. I
recounted the table instead of trusting the correction: `awk '/^### Quarantine/{f=1;next} f&&/^\| S[0-9]/{print}' corpus/lessons/round-40.md | wc -l` → 17, verdicts 1 Adopted (S132), 6 refuse
(S109, S131, S137, S140, S141, S143), 10 present-but-not-appended (11 present rows minus the adopted
one; S118 `misbound` counts present); the three "prose class is stale" rows are S113/S123/S134, so the
old sentence's "two prose-class rows" is superseded by the correction's declaration that the table is
the record. Freshness holds by the counter's own scan (`fixed_bad=0`): at `routed_at` the round-41
file does not exist, the commit touches it, and lines 53-58 carry no acknowledgement word.

## R40.2 — wave grant pointer does not resolve at closure → **open**

The ask (spot-check `:303-307`) is that the round-40 report stop citing the seat-ledger line
`1792889233 64 tameshi round-40-w1` in `~/.local/state/shokunin-hyaku/wave-slots` (deleted by design)
and cite a durable artefact instead. The report still cites only the transient line:
`git show e3729de8:.ufo/waves/round-40/w1/dispatch-outcome.md | sed -n '12,16p'` prints "The grant is
recorded in the seat ledger as `1792889233 64 tameshi round-40-w1` / (`~/.local/state/shokunin-hyaku/wave-slots`), taken at …"
(`wave-slots` occurs only at line 13 of that file). The file's last touch is `46781274` — before
`routed_at` — so no errata was appended; `grep -rn wave-slots LOG.md SCORECARD.md` is empty, and the
only other tracked hit is round-41's own critic report. The durable artefact the routing names does
exist at base: `.ufo/waves/round-40/settlement-receipt.json:277-279` ("registry_members": 64,
"seat_exits": 64, "reports_present": 64; sha256 `659e39bb…f89a3`), with `settlement-receipt.stdout`
beside it. Verdict: open — the report text was never corrected, and round-41 itself re-routed the item
(`.ufo/waves/round-41/w1/CriticR40Discharge.md`, verdict 2 "route again"). `fix_plan` (in the rows
file): one errata line in `corpus/lessons/round-50.md` naming the receipt, its three counts and its
digest, and stating that the wave-slots line is transient and not re-cited.

## R40.3 — the 105-id list was never pasted into the report → **open**

The ask (spot-check `:308-311`) is that item 10's both id lists be pasted into the report text, not
only committed as wave evidence. They are still file-only: `git show e3729de8:.ufo/waves/round-40/assimilation/reg-ids | wc -l`
→ 105 (sha256 `b11c9413…6e91`), `staged-ids` → 2 (sha256 `d77a652a…9fce`), and the report carries no
ids at all: `git show e3729de8:.ufo/waves/round-40/w1/dispatch-outcome.md | grep -c 'S1[0-9][0-9]'` → 0.
`grep -rn "reg-ids\|staged-ids" .ufo/reports` is empty; round-41's `w1/ReviewIdLists.md:8` recorded
"the lists are MISSING everywhere", and no later round pastes the round-40 lists (round-47 pastes its
own 120-id registry in `w1/T47ExecIdGuard.receipts.md:30`, a different round's list). Verdict: open —
round-41 re-routed it too (`CriticR40Discharge.md`, verdict 3). `fix_plan`: paste both lists verbatim
with their digests in a `corpus/lessons/round-50.md` corrections block (`paste -sd' '` on the
committed files), ~525 characters, leaving the closed round-40 report untouched.

## R40.4 — the S152 quote was labelled "11 words"; it has 13 tokens → **fixed**

The ask (spot-check `:312-313`) is that the label be corrected; the quote itself is verbatim. The
mislabel is still in the closed lesson (`corpus/lessons/round-40.md:14`: "Quote (11 words), English
abstract: …"), and the count is confirmed: `printf '%s' 'drawbacks such as fragility and lack of
context can lead to false positives' | wc -w` → 13. The lane's erratum is
`corpus/lessons/round-41.md:75` ("the round-40 closure's routed defect 4 (a quote labelled \"11
words\" that has 13 tokens) — the same class, one round later, caught by re-counting instead of
trusting the label"), added by `b37ce974` (same `-S` lookup); the counter accepts it as a fix
(`fixed_bad=0`: new since `routed_at`, path touched by the commit, no acknowledgement word in the
cited line). Verdict: fixed as an appended erratum, matching routed item 1's "do not rewrite the closed
round-40 file" rule; residual disclosed — the primary label inside `round-40.md:14` still reads "11
words", so a reader who never reaches the round-41 Mistakes table still sees the slip.

## R40.5 — the round-38 vacuous depth guard (`^\s*leg`) → **declined**

The item (spot-check `:314-316`) records that `.ufo/evidence/round-38/contract.json:58`'s
`no_harm_guard.depth_command_d` uses `^\s*leg`, which matches 0 lines of `tools/mutate-and-run.sh`, and
says "the round-38 routing stays open until a guard that can fail replaces it". Two facts decide the
status. (a) The vacuous pattern sits in a frozen round-38 control, and its successor record says so
explicitly: `git show e3729de8:.ufo/evidence/round-39/contract.json | sed -n '12p'` → "The round-38
regex ^\\s*leg remains a vacuous control (0 hits) and is not rewritten." (b) The can-fail replacement
already exists and is the lane's operative depth check: `.ufo/evidence/round-39/contract.json:36`
carries `depth_command_d` with the command-D pattern, its counter "fails a missing guard, the vacuous
regex, and a constant 9" (`SCORECARD.md:1859`, control receipts `SCORECARD.md:1862`), and every later
round's numeric depth line cites command D verbatim. No contract after round 39 carries a
`depth_command_d` key at all (`for f in $(git ls-tree -r --name-only e3729de8 .ufo/evidence | grep
contract.json); do …grep -c depth_command_d…` → only round-38 (1) and round-39 (2)), `git grep -n
"depth guard" e3729de8 -- ':!corpus/lessons/*spotcheck*'` finds only pre-round-40 wave files, and
`corpus/QUALITY.md` has no criterion naming it. So the live tree has nothing broken to repair; the only
literal remedy left is editing a pinned historical control, which the lane must not do. I therefore
record `declined` with a ≥40-character reason (rows file), and flag the residual rather than hide it:
retirement-by-omission means a future contract could re-add `depth_command_d` with the vacuous pattern
unnoticed; a QUALITY criterion ("FAIL if any contract's `depth_command_d` matches 0 lines of
`tools/mutate-and-run.sh`") is the smallest guard against that and is not required by this item's own
condition.

## Gates observed

Counter (self-check, scratch only): `git clone -q --shared … $S/lane`, toplevel verified, ledger
written from `T50Disp40.rows.json`, committed `13b2ab7662c0446750659d4b2b3fed1cd638f29d` with a scratch
identity, then
`python3 …/.ufo/evidence/round-50/c1/measure.py --lane $S/lane --rev HEAD --explain` →
`fixed=2 open=2 declined=1 fixed_this_round=0 missing=44 extra=0 duplicate=0 spotcheck_changed=0
defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=2 declined_bad=0
fixed_short=18 declined_over=0 this_round_short=5 total=69 C1_R50_PASS=false` (exit 1). Every EXPLAIN
line naming a round-40 id is explained: `R40.2` and `R40.3` are `open-unplanned` because the newest
`**Planned (round 50):**` paragraph (`SCORECARD.md:2410`) is the L1's to write and does not yet name
them — the L1 must add both ids there or the two rows must change status; the 44 `missing` lines are
R41.1–R49.6, other seats' items; `fixed_short`/`this_round_short` are fleet floors. No probe was run
against the lane checkout itself; `--selftest` was not needed. Nothing was installed (python3 and git
sufficed; the host-wide pacman pause was not exercised).

## Findings and limits

- **Status conflict with round 41, reported verbatim for the canonical judge.** Round 41's own
  disposition seat discharged all five: `CriticR40Discharge.md` verdicts 1 and 4 "discharge" (I agree),
  2 and 3 "route again" (I agree: open), and 5 "discharge — the vacuous contract guard is retired …
  residual: retirement by omission — re-adding `depth_command_d` with `^\s*leg` re-breaks it". I record
  R40.5 as `declined` rather than fixed because the item's literal object sits in
  `.ufo/evidence/round-38/contract.json`, which is a pinned control the lane must not edit, while the
  can-fail successor it asks for already exists. Either reading (fixed-by-successor, or
  declined-as-frozen-observation) is defensible against the tree; the counter cannot certify
  `fixed` here because no keyed excerpt for this item is new since `routed_at`.
- **Underclaim risk disclosed**: both round-40 fixes predate base (`b37ce974`), so they cannot satisfy
  `fixed_after_base_min=5`; the round-50 L1 must land ≥5 fixes after `e3729de8` from other rows.
- **Out of scope / untouched**: the lane checkout (read-only; no `git add/commit/checkout` there), the
  fleet repo, sibling lanes, `/home/vgpnk/Projects/shokuknow`, the lane's jj state and Git index,
  `~/.local/state/` (including the hidden C2 panel), and `control/c2-*.stdout`. No model was routed,
  `agent://all` was not messaged, no subagent was dispatched.
- **Touched surfaces (all mine)**: `.ufo/waves/round-50/w1/T50Disp40.md`,
  `T50Disp40.rows.json`, `T50Disp40.receipts.md`.

## Summary

- R40.1 fixed: `corpus/lessons/round-41.md:51-58` states the table-derived 1 adopted / 6 refused / 10 present; commit `b37ce974`; round-40 file untouched.
- R40.2 open: `.ufo/waves/round-40/w1/dispatch-outcome.md:13` still cites `wave-slots`; last touch `46781274` (pre-routing); receipt `:277-279` exists but is never cited.
- R40.3 open: report has 0 `S1xx` tokens; `reg-ids` (105) and `staged-ids` (2) remain file-only; round-41 also re-routed it.
- R40.4 fixed: erratum `corpus/lessons/round-41.md:75` gives the true 13-token count against `round-40.md:14`'s "11 words"; residual: the closed label is unchanged.
- R40.5 declined: the vacuous `^\s*leg` sits in a pinned round-38 control ("is not rewritten", r39 contract `:12`); the can-fail command-D successor already exists (`SCORECARD.md:1859-1862`).
- Self-check: `fixed=2 open=2 declined=1`, zero `evidence_bad/key_miss/fixed_bad/declined_bad`; the only round-40 EXPLAIN lines are `open-unplanned R40.2/R40.3` (Planned paragraph is the L1's).
- Neither fix counts toward `fixed_after_base_min=5`; both predate base `e3729de8`.
