# T50W2ConnLedgerChains — cross-row pattern check of corpus/routed-defects.json at 80ea77e9

Seat: T50W2ConnLedgerChains (reviewer, leaf). Scope: the ledger at
`80ea77e99e239982ab0b93e416645ef2359725d3` (`git -C <lane> show 80ea77e9:corpus/routed-defects.json`)
read against the frozen statement set `.ufo/evidence/round-50/c1/defects.json`
(fields `text`/`keys`/`routed_at`), the spot-check routed texts, the tree at REV, and wave-1
`T50RevControls.md` H1. Read-only on the lane except this file. No tool installs, no scratch
created (all commands are read-only `git show`/`git grep`/`git ls-tree`/`git diff-tree` and
Python stdlib JSON extraction).

## Method (commands that reproduce the checks)

- Ledger at REV: `git -C <lane> show 80ea77e9:corpus/routed-defects.json`.
- Frozen asks/keys/routed_at: json load of `c1/defects.json` (ids below).
- Tree checks at REV: `git show 80ea77e9:<path>`; `git grep -n <pat> 80ea77e9 -- <paths>`;
  `git ls-tree -r --name-only 80ea77e9 -- .ufo/evidence/round-50/`; post-base test
  `git merge-base --is-ancestor e3729de <c>`; touched files `git diff-tree --no-commit-id
  --name-only -r --root -m <c>`.

## 1. Repeating-item groups: statuses and reasons

### 1a. R45.4 / R46.1 / R47.5 (anchor-refresh family) — consistent, differences explained by asks
- R46.1 (fixed): ask = pin S026/S093/S108 by quote **and** per-snapshot fetch receipt
  (defects.json text). Evidence resolves: `corpus/SOURCES.md:140,142,143` carry supersede rows
  S265/S267/S268 ("supersedes S026's anchor and quote only", S093, S108) plus
  `.ufo/evidence/round-48/freshness/sources/S093.receipt.json:2-4`; commit 50545328 (pre-base).
- R45.4 (open): ask = the five anchor-refresh candidates of ConnDriftAnchors.md **and**
  S026/S093/S108 quote-pin. The candidates are S153/S154/S157/S159/S100 (the
  `.ufo/waves/round-45/w2/ConnDriftAnchors.md` summary table names exactly these five open
  candidates; S089 already superseded via S160). At REV none has a supersede row:
  `git grep -i -E 'supersedes S(100|153|154|157|159)' 80ea77e9 -- corpus/SOURCES.md` → no hits;
  SOURCES.md:108/123/124/127/129 still show the original pins. The S026/S093/S108 half is
  closed by the same fix that fixed R46.1 (R45.4's own evidence cites SOURCES.md:140/142/123).
  Open is correct: the five candidates remain.
- R47.5 (open): ask = S026/S093/S108 refresh (done, above) **plus** dead `brace_depth_at`
  helpers, C1-8/C3-10 survivor selftest cases, located-name check. At REV:
  `tools/tally-audit-v2.py:135` and `tools/tally-audit-v3.py:234` still define
  `brace_depth_at` with no caller (`git grep brace_depth_at 80ea77e9 -- tools/` → only the two
  definitions); no selftest case names `T47MutC1Counter`/`T47MutC3Counter` outside the round-47
  wave files; `git grep -i 'located-name' 80ea77e9 -- .ufo/evidence/round-48/ .ufo/evidence/
  round-49/ tools/` → no hits. Open is correct.

### 1b. R47.5 / R48.4 / R49.5 (carried-items family) — consistent (all open), overlapping asks unmet
- All three ask for the dead `brace_depth_at` helpers, survivor selftest cases and the located-name
  check (R48.4 adds S205/F7, six-leg class, append-only rule; R49.5 = still-carried). All verified
  unmet at REV (1a evidence; `git grep -E 'brace_depth_at|S205' 80ea77e9 -- corpus/lessons/
  round-49.md corpus/lessons/round-50.md` → no hits, so R49.5's note "none of the other five
  carried asks appears in round 49 or 50" holds). Statuses are mutually consistent.

### 1c. SHONEN: R42.4 / R46.5 / R47.7 / R48.6 / R49.6 — consistent (all declined, operator-owned)
- All five declined with reasons ≥ 40 chars and the same substance: promotion is operator-owned,
  the boxes are lane assertions with no independent promotion verifier, so no lane edit can close a
  box. `SHONEN.md:1-12` at REV still shows four `[~]` boxes. R49.6's reason's 8-item closure
  sample matches its routed text (defects.json R49.6 text). No status divergence; phrasing varies
  ("operator/closure-owned" in R42.4 vs "operator-owned" elsewhere) without a reason conflict.

### 1d. R41.6 / R42.3 — consistent, difference explained by asks
- R41.6 (fixed): ask = renumber by document in scratch before appending (round-41 routed text).
  Round 42 applied the renumber map (SOURCES.md:471: `staged:S159` → S155, `staged:S160` →
  S156) and appended S155-S158; commit 5f739acf.
- R42.3 (declined): ask = the recorded staged-collision hazard, with the routed text itself saying
  "No action required this round" (SOURCES.md:474-477). Decline reason ≥ 40 chars and matches the
  disposition. No conflict: R41.6 asked for an action that happened; R42.3 was a hazard record.
  The residual staged-id collision persists by design (staged package keeps S153-S255) and is
  consistently reflected in both rows' evidence.

### 1e. R47.1 / R48.4 — consistent; R48.4's six-leg sub-ask is stricter than what R47.1's fix delivered
- R47.1 (fixed): ask allowed stating the stable observation OR a declared-unstable form; evidence
  resolves — SCORECARD.md:2334 six-leg row states `runs 3 stable` with the declared value-class
  machinery in `.ufo/evidence/round-48/calibration/measure.py:7-20` (V = {stable}); commit
  c7586b9a.
- R48.4 (open): its six-leg sub-ask is "a pinned-leg successor or declared nondeterministic class".
  SCORECARD.md:2328 discloses the class is `stable` with one member and that "declaring the
  unobserved FAIL member would be refused as unattested by amendment 4", with the FAIL side
  documented in prose/wave files (`.ufo/waves/round-48/w1/T48ExecObs2.md` observed `REGRESSION:
  FAIL (cases=9 passed=8`). So R48.4's note ("six-leg states runs 3 stable with the FAIL member
  only disclosed in prose") is grounded on the tree, and the status difference is explained by the
  asks: R47.1's ask permitted the stable form; R48.4's later ask requires the nondeterministic
  class or a successor, which is not present. Both rows are internally consistent.

## 2. Open item's ask overlapping a fixed item's evidence

- R45.4 (open) and R47.5 (open) each contain the S026/S093/S108 quote-pin + fetch-receipt
  sub-ask, which is closed by R46.1's fix (SOURCES.md S265/S267/S268, S093.receipt.json). Neither
  is an underclaim: each stays open for its other, unmet asks (five candidates; helpers/survivors/
  located-name).
- R48.4 (open) contains the six-leg sub-ask addressed by R47.1's fix (1e). It stays open on the
  stricter reading and on its five other unmet asks.
- No open item has every ask satisfied by a fixed row's evidence. The three overlaps above are the
  ones closure sampling should watch: the S026/S093/S108 sub-ask is closed once (R46.1) while two
  open rows still name it; the six-leg sub-ask is addressed by R47.1 while R48.4 names it unmet.

## 3. Wave-1 H1 spurious-citation check (T50RevControls.md H1)

H1 flagged three citations as presumptively spurious: `cdbf24c0/.ufo/evidence/round-50/c2/
measure.py`, `4afb060c/SCORECARD.md:2423`, `4afb060c/.ufo/evidence/round-50/before/no-harm-at-base.stdout`.

- **R49.4 (fixed) matches H1's pattern #2 exactly**: evidence cites `SCORECARD.md:2423` (and
  :2416, the "### Standing axis table — re-stated at round 50" heading added by the same commit)
  with commit `4afb060c1d6e994d1bbb9095493b1f6b2b8344f2` (post-base). The appended standing
  table's own text cites `.ufo/evidence/round-50/before/no-harm-at-base.stdout` (H1 pattern #3),
  though the row itself does not cite that path. Semantic note: the ask literally demanded
  "append a restated standing table with the round-49 values", so the content matches the ask —
  but per H1 the counter cannot distinguish this from fabrication, and the closure should treat
  this row as presumptively spurious, not as independent fix evidence.
- **R45.2 and R47.2 (fixed) cite a new this-round receipt path**: `.ufo/evidence/round-50/routed/
  receipts/MANIFEST.md` (commit 79f44b55, post-base), absent at both routed_at revs
  (683eedde, 473336d9; `git ls-tree -r 683eedde/473336d9 -- .ufo/evidence/round-50/` → empty).
  This is the same "path absent at routed_at → fresh" mechanism H1 describes (c1/measure.py:241-243),
  on a different directory. The receipts behind it are real committed selftest stdout files
  (`.ufo/evidence/round-50/routed/receipts/r45-c1-freshness.selftest.stdout` etc.), so the rows
  are semantically aligned with the asks ("Commit selftest receipts"), but they use the same
  fabrication-attack surface.
- **R49.2 (fixed) cites new this-round successor instruments** `.ufo/evidence/round-50/successor/
  reads-v2.py:17` and `sandboxed-confirm.py:9` (commit 79f44b55). Same class; here the ask
  explicitly demanded the successor counter, so the citation is the direct deliverable.
- **R40.2/R40.3 (fixed) cite `corpus/lessons/round-50.md:124/126`**, a file created this round by
  79f44b55 that carries the keys — the H2-predicted "new allowed prose carries keys" satisfiability
  route (T50RevControls H2), the same lever as the fabrication route.
- No fixed row cites `.ufo/evidence/round-50/c2/measure.py` (H1 pattern #1) or
  `before/no-harm-at-base.stdout` directly.
- Post-base commit citations (this-round fixes, for the closure's floor reading): R40.2,
  R40.3, R45.2, R46.4, R47.2, R49.1, R49.2, R49.4 (8 rows). Of these, R46.4 (cites an appended
  block in the pre-existing `corpus/lessons/round-46.md:138-139`) and R49.1 (cites a code line in
  `tools/pbt-staged-id.py:887` fixed by 43bfa7ae) are code/errata changes rather than new-receipt
  citations.

## Verification gaps / residual

- Statuses here are judged against the tree as read at 80ea77e9; I did not run the C1 counter
  (probe only is permitted; not needed for these pattern checks).
- The R48.4 six-leg reading depends on interpreting "declared nondeterministic class" strictly;
  the counter's own terms (amendment 4) support the row's `stable` declaration. Flagged for the
  closure, not adjudicated.

## Summary

- Group consistency holds across all five repeating families; every open/declined status is explained by unmet or non-actionable asks, and each overlap sub-ask is reflected in the fixing row.
- The S026/S093/S108 sub-ask is closed once (R46.1) while R45.4 and R47.5 still name it among their open asks; both correctly stay open for their other asks — not underclaims.
- R48.4's six-leg sub-ask overlaps R47.1's fix; R48.4's stricter ask (nondeterministic class/successor) is unmet and its "FAIL member only disclosed in prose" assertion is grounded at SCORECARD.md:2328.
- H1 spurious-citation check: R49.4 is the exact `4afb060c/SCORECARD.md:2423` pattern; R45.2/R47.2 (routed/receipts/MANIFEST.md) and R49.2 (successor/) use new this-round paths with the same "absent at routed_at → fresh" mechanism; R40.2/R40.3 use new round-50 prose. No row cites c2/measure.py or before/no-harm-at-base.stdout directly.
- Post-base fixed citations: 8 rows (79f44b55 ×6, 43bfa7ae, 4afb060c); only R46.4 and R49.1 are code/errata changes rather than new-receipt citations.
- No tool installs; no scratch created; read-only lane access throughout.
