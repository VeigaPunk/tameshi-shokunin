# T50Cross44 — C1 independent cross-coder, spot-check round 44

Seat: T50Cross44. Items coded: R44.1, R44.2 (the only round-44 items in the frozen set
`.ufo/evidence/round-50/c1/defects.json`). Coded against the lane tree at base
`e3729de862f73ae080d98fcf522a7081ce16e40a`. No `T50Disp*` file was read. No tool was
installed (nothing needed). No scratch dir was created.

## R44.1 — cosmetic label correction ("20 words" → true token count)

Ask (spot-check file line 73): correct the label of the line-15 quote in
`corpus/lessons/round-44.md`; the quote tokenizes to ~28 (24 letter/digit words).

Findings:

- `git -C <lane> show e3729de:corpus/lessons/round-44.md | sed -n '26p'` → the label is
  **unchanged at base**: `  - line 15, 20 words: “Notice that 10 ** 0 = 1, …”`
  (round-44.md:26).
- `git -C <lane> log 5891bdb77aba8489683533ae4cdd3b49b5e2626b..e3729de --oneline -- corpus/lessons/round-44.md`
  → **empty**: no commit after `routed_at` (5891bdb, the commit that added the round-44
  spot-check) touches the lesson. The counter's `fixed` requirements (keyed excerpt new
  since routing, in a path the post-routing commit touched) cannot be met for any path.
- `git -C <lane> grep -n -i "24 letter\|20 words" e3729de -- corpus` → the only "20 words"
  label on the quote is round-44.md:26; round-45.md:158 (number-drift mistake row) and
  corpus/QUALITY.md:1235/1277 restate the measurement but do **not** correct the label
  (round-45.md:158 records the disposition as `none (routed by …round-44-verifier-spotcheck.md:73)`).
- `git -C <lane> show e3729de:SCORECARD.md | sed -n '2410p'` → the newest `**Planned (round
  50):**` paragraph does not name R44.1, so `open` is unsupported at base
  (counter rule: open requires the id in the newest Planned paragraph).

Verdict: **declined** (reason ≥ 40 chars). The ask is unmet in the tree; neither `fixed`
(no correction text exists; no post-routing commit touches any candidate file) nor `open`
(not planned at base) is valid. Doubt (strongest counter-reason): the token-count
measurement exists elsewhere → resolved: measuring/restating a defect is not correcting the
label; the counter's fixed-path conditions fail for every file.

## R44.2 — observation (not a defect): wave shape

Item text (spot-check line 74): wave shape was one v1 wave of 32 seats with 14 attack-role
seats; no wave 2 or residual call, "as reported in `w1/summary.md`". Self-declared
observation, no ask.

Findings (tree matches every stated fact at base):

- `git -C <lane> show e3729de:.ufo/waves/round-44/w1/summary.md | sed -n '3p'` → one v1
  wave `round-44-w1`, `counts.spawn=32`, `counts.resume=0` (summary.md:3).
- `git -C <lane> show e3729de:.ufo/waves/round-44/w1/summary.md | sed -n '6p'` → 14
  attack-role seats; distinct fresh attack inventory below 32 → no wave 2 dispatched; no
  unassigned residual check remained; no ordinary residual call was needed (summary.md:6).
- `git -C <lane> ls-tree -r --name-only e3729de -- .ufo/waves/round-44/` → only `w1/`
  exists; **no `w2/` directory**, consistent with "no wave 2".
- `git -C <lane> show e3729de:SCORECARD.md | sed -n '2410p'` → newest Planned paragraph does
  not name R44.2 → `open` unsupported.

Verdict: **declined** (reason ≥ 40 chars): the item is an observation, not a defect; there
is no ask to satisfy, so `fixed` cannot hold, and the item is not planned. Doubt (strongest
counter-reason): the observation is recorded verbatim in the summary → resolved: an accurate
record of an observation is not a fix; the tree supports only declined.

## Summary

- R44.1: declined — label still "20 words" at round-44.md:26 at base; no post-routing commit
  touches the lesson; not in newest Planned paragraph; measurement records elsewhere do not
  correct the label.
- R44.2: declined — observation, not a defect; all stated facts verified in
  .ufo/waves/round-44/w1/summary.md (spawn=32, 14 attack-role seats, no wave 2, no residual
  call); no w2 dir exists; not planned.
- Evidence records included in the JSON for both rows resolve at base and carry a key
  (R44.1 excerpt contains "20 words"; R44.2 path ends with the key "w1/summary.md") per the
  frozen counter's rules.
- Deliverables: `.ufo/waves/round-50/w1/T50Cross44.json`, `.ufo/waves/round-50/w1/T50Cross44.md`.
