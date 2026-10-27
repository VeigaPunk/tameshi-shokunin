# T51CritExpectedB — C1 expectations F6..F10 vs. the lane's own later declarations

Seat: T51CritExpectedB (critic, F6..F10). Item: derive each ground F6..F10's latest
declared status from `corpus/README.md` (plus knowledge `ground:` lines, lessons,
SCORECARD), compare with the frozen `.ufo/evidence/round-51/c1/frontier-expected.json`,
cite; then check whether any ground beyond F10 exists (F11/F12 at README:548-555) and
whether the round-31 "executable self-assessment" ground (README:462) is a frontier row.

Method: read-only. All commands below are `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 9962033fd7a75aa2f2847e979dd687a5d28505a1:<path>` or `grep -n` over the working tree at base; no mutation, no counters run, no scratch used (no receipt cited was produced by this seat).

## Per-ground comparison (F6..F10)

### F6 — expected: `held`, round 50, basis `corpus/README.md:608`
- Latest lane declaration (README:608): "F6 (fixture minimization for survivors): open →
  **held (round 50)** for the method on killing cases — one shrinker that reduces a gate's
  killing case to a 1-minimal sub-case and states its run cost — conditioned on the round-50
  deciding receipt `.ufo/evidence/round-50/after/c2.stdout` printing `C2_R50_PASS=true`; …
  if that receipt prints anything else this line is void as of round 50".
- Condition holds: `.ufo/evidence/round-50/after/c2.stdout` (committed with the deciding
  receipts at `616dee6`) ends "C2_R50: … total=0 C2_R50_PASS=true".
- Corroboration: SCORECARD.md:2429 (round-50 C2 cell: "F6 held (round 50)") and :2440
  (deciding result "F6 open → held (round 50)"); `corpus/knowledge/fixture-shrinking-pilot.md:6`
  declares `ground: F6 (fixture minimization for survivors)`; `corpus/lessons/round-50.md:204`
  ("F6 is held for the method on killing cases").
- Verdict: **matches expected (held, round 50)**.

### F7 — expected: `open`, round null, basis `corpus/README.md:175, :255, :589`
- Latest declarations: README:175 ("The full F7 per-leg **reuse-decision** frontier remains
  open"), :255 ("No frontier row moves: F7 stays open"), :577 ("F7 stays `open`"), :589
  ("F3 and F7 stay `open`"). Rounds 30/31/32/35 state "No frontier row changes status this
  round (F1–F10 as above)" (README:456, :464, :472, :485); nothing later than :589 changes F7.
- Verdict: **matches expected (open, no round)**.

### F8 — expected: `partly held`, round 27, basis `corpus/README.md:424-429, :437`
- Latest declarations: README:424-429 ("F8 moves from open to **partly held**: its next move
  … is measured, on one gate at one pin"), :437 ("F8 stays partly held on that bound"). No F8
  mention exists after line 437; later "No frontier row changes status" statements stand.
- Verdict: **matches expected (partly held, round 27)**.

### F9 — expected: `open`, round null, basis `corpus/README.md:86` (table row) and `:555`
- Latest declaration: README:555 (round 43) "F9 (LLM-era mutant generation and equivalence)
  is not touched: no LLM was used to generate or classify a mutant here." No F9 mention after
  line 556. The coverage-map table row (:86) still reads open and is never superseded.
- Verdict: **matches expected (open, no round)**.

### F10 — expected: `held`, round 49, basis `corpus/README.md:599`
- Latest lane declaration (README:599): "F10 (PBT generators for gate fixtures): open →
  **held (round 49)** for its stated next move … conditioned on the round-49 deciding receipt
  `.ufo/evidence/round-49/after/c2.stdout` printing `C2_R49_PASS=true`; if that receipt prints
  anything else, this line is void as of round 49".
- Condition holds: `.ufo/evidence/round-49/after/c2.stdout` (committed at `143d91e`) ends
  "C2_R49: … total=0 C2_R49_PASS=true".
- Corroboration: SCORECARD.md:2393 (round-49 C2 cell: "F10 held (round 49)") and :2402
  (deciding result "F10 open → held (round 49)"); `corpus/knowledge/pbt-generator-pilot.md:5`
  declares `ground: F10 (PBT generators for gate fixtures)`; round-50 does not touch F10.
- Verdict: **matches expected (held, round 49)**.

## Beyond F10

### F11 / F12 (README:548-555) are fixture ids, not frontier grounds
- README:548 "the outflag mutant killed by F11" and :555 "the middle is what F12 documents"
  refer to the two round-43 resolving fixtures `F11_outflag_namespace` and
  `F12_method_two_returns` of the K/D/E/U survivor-resolution battery (`.ufo/evidence/round-43/mutants/measure.py:28-31,250-251`; contract `.ufo/evidence/round-43/contract.json:22,34,87`). They carry no status, no sources column, no next-falsifiable-move cell, and no `knowledge/` entry declares a ground or an F11/F12 status — they are fixture names in a battery, not coverage-map rows. The frontier table should **not** carry them.
- The round-46 hardening/freshness mutant ids F10-F15 (`.ufo/evidence/round-46/hardening/`) are likewise mutant ids in a selftest panel, not frontier grounds.

### Round-31 "executable self-assessment" ground (README:462) is not a frontier row
- README:462: "New lane ground (seat ScoutFrontier: not F1–F10, not held core): a standing
  SCORECARD capability or score row is a claim checked by running the row's own command…".
  It is explicitly not a frontier ground (not F1-F10, not held core), has no F-id, and no
  status cell; it is a calibration-side ground measured by round-31 C1. The frontier table
  should **not** carry it.

## Conclusion
All five expected rows F6..F10 state exactly the lane's latest self-declared status; both
conditional holds (F6 on C2_R50_PASS=true, F10 on C2_R49_PASS=true) are satisfied by the
committed deciding receipts; no ground beyond F10 exists that the table should carry (F11/F12
are fixture ids; the round-31 executable-self-assessment ground is explicitly non-frontier).
No correction to `.ufo/evidence/round-51/c1/frontier-expected.json` is indicated by the
evidence in this seat's scope.

## Evidence commands
- `grep -nE 'F6|F7|F8|F9|F10|F11|F12' corpus/README.md` (all F-ground mentions and their lines)
- `python3 -c "import json;json.load(open('.ufo/evidence/round-51/c1/frontier-expected.json'))"` (frozen expectations parse)
- `cat .ufo/evidence/round-50/after/c2.stdout | tail -1` → `C2_R50_PASS=true`
- `cat .ufo/evidence/round-49/after/c2.stdout | tail -1` → `C2_R49_PASS=true`
- `grep -n 'F6\|F10' SCORECARD.md | grep 'round 50\|round 49'` (scorecard rows 2393/2429/2402/2440)
- `grep -n '^ground:' corpus/knowledge/fixture-shrinking-pilot.md corpus/knowledge/pbt-generator-pilot.md`
- `grep -rn 'F11\|F12' .ufo/evidence/round-43/` (fixture/battery definitions)

## Summary
- F6: held (round 50) — README:608, condition satisfied by round-50 receipt (C2_R50_PASS=true); matches expected.
- F7: open — README:175/255/577/589, never changed; matches expected.
- F8: partly held (round 27) — README:424-429/437, never changed since; matches expected.
- F9: open — README:86/555, no later mention; matches expected.
- F10: held (round 49) — README:599, condition satisfied by round-49 receipt (C2_R49_PASS=true); matches expected.
- F11/F12 at README:548-555 are round-43 fixture ids (F11_outflag_namespace/F12_method_two_returns), not frontier grounds; no table row owed.
- Round-31 executable self-assessment (README:462) is explicitly "not F1–F10, not held core"; not a frontier row.
- No expected row is contradicted; the frozen frontier-expected.json stands as the L1's correct reading for F6..F10.
