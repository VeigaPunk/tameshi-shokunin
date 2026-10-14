# tameshi-shokunin — Iteration Log

- 2026-10-14 — round 0: minted as shonen (operator directive; see MINT.md).
  Probation: >=3 verified rounds before any roster row.
- 2026-10-14 — round 1: probation wave 1 (4 content lanes + audits, dispatched
  from the mint session). Lane write-scopes left this LOG to the scribe lane —
  the dispatch-scope-overrides-append precedent
  (verification-patterns-fleet.md:5-8; kaidoku known-gap). No
  `.ufo/waves/tameshi-*` directory exists — the lane deliverables in this repo
  ARE the wave record (observation). Content lanes:
  TAMESHI-1 → `corpus/knowledge/gates-survey-kumitate.md` (335 L): six hermetic
  suites, all `--selftest` exit 0 — 62/42/60/102/39/43 executed cases vs
  62/42/60/71/35/41 literal `check(` sites (counts are loop-sensitive; quote
  the executed summary line, never a source grep); fail-closed arm inventories
  (proxy 12/12 fired, claims 5/5, round-gate 7 declared/6 fired with
  `INTERNAL_ERROR` uncovered, surface-probe + cite-check have no token enum);
  verdict-line exactness tiers; mutation-control census — only cite-check's
  integration-gated mutation copy + claims-check's external env-poison probe,
  no kill-rate harness anywhere (note §7-§9).
  TAMESHI-2 → `corpus/knowledge/gates-survey-kagi.md` (556 L): 250 selftest
  cases green 6/6 from the suites' own counters (static site counts
  6/1/0/1/6/2 are wrong); one three-valued exit lattice across all six gates;
  four exit-2 classes; five evidence-discipline habits; F-1: `--falsify`
  measures 16/18 live vs README's unqualified 18/18 — adjudicated host-state
  dependence (the same rule's scratch case passes inside 61/61), reported not
  fixed, sibling gate stays sibling-owned per PROVINCE.md (note §6);
  F-2: three bypass-class `policy_check` refusal paths (`inline-shell`,
  `backslash`, `empty-quotes`) asserted by no selftest case (note §6b); the
  substrate moved mid-survey → every line ref re-resolved by number, and the
  16 self-caught wrong-line citations are kept as ER-1 with the generator
  analysis (12/16 transcribed from a stripped header view; note §10).
  TAMESHI-3 → `corpus/knowledge/verification-patterns-fleet.md` (105 L): the
  shared verifier shape P1-P10, general only on >=2 independent lanes (game
  lanes + kaidoku audits); two explicitly lane-specific encodings (kaidoku
  audit blocks; game AGREE tally); 3 falsifiable predictions; unknowns U1-U7.
  Fourth content lane → `SKILL.md` distillation (the file carries no lane
  header; lane id inferred from dispatch shape): seed 22 → 171 lines —
  gate-shape decision table (hermetic vs live vs audit-lane), the mutation bar
  (nominal vs load-bearing), the 8-step no-permissiveness audit recipe, the
  fail-closed arm taxonomy — every rule citing its note line, refs re-resolved
  2026-10-14.
  Audits: the in-tree audit evidence is in-note self-audit — ER-1's 16-row
  table with per-line re-reads (gates-survey-kagi.md:508-543), the kagi access
  proof (git status byte-identical before/after every command,
  gates-survey-kagi.md:7-9), the fleet note's post-write `git status
  --porcelain` check showing exactly the assigned writes
  (verification-patterns-fleet.md:96). Whether audit lanes left artifacts
  outside this tree is unknown to this scribe (no wave directory found).
  Scribe verification (this entry): the SCORECARD round-1 counting commands
  re-executed with identical outputs (depth: 22 → 171 lines, 10 table lines,
  3 note cites; calibration: O:33/I:7, [OBS]28/[INF]18/[UNK]7, ER-1 ×16,
  U-rows 9). Spot re-runs of cited suites: `node
  kumitate-shokunin/scripts/claims-check.mjs --selftest` →
  `CLAIMS_SELFTEST: 39/39 pass` / `VERDICT: PASS`, exit 0 (matches
  gates-survey-kumitate.md:25); `bash kagi-shokunin/corpus/surface-census.sh
  --selftest` → `SELFTEST: PASS (16 cases)`, exit 0, with 2 cases abstaining
  `substrate-absent` — the abstention pattern observed live (matches
  gates-survey-kagi.md:55, :187-197); kagi's working tree byte-identical
  before/after the run. Coverage map seeded: 3 rows (corpus/README.md).
  SCORECARD round-1 moves: depth improved, calibration improved (counting
  commands in the move-log rows). Carried to round 2 as recommendations, not
  absorbed (sibling gates stay sibling-owned): kumitate integration groups
  unexecuted + round-gate `INTERNAL_ERROR` arm uncovered
  (gates-survey-kumitate.md:144-156, 320-331); kagi live verdicts unmeasured
  for 5/6 gates + F-2's two-lines-per-path fix candidate
  (gates-survey-kagi.md:442-465, 358-363); fleet census U1/U2 are decidable
  predictions for a round-2 audit (verification-patterns-fleet.md:86-88).
