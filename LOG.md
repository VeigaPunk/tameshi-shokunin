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
- 2026-10-14 — round 2: probation wave 2, planned as a ufo-round-plan
  (`plans/round-2.plan.md`, ufo-round-plan-v1 — axis set
  depth(mutation-craft) / calibration(suite honesty) / operability, primary
  move depth; falsifiable claim pre-registered with its anti-claim: a <50 %
  kill-rate still admits, recorded as the finding). Same dispatch shape as
  wave 1 — lane write-scopes left this LOG to the scribe; no
  `.ufo/waves/tameshi-r2-*` directory exists (the parent training wave
  `.ufo/waves/shokunin-train-20261014-w9` exists; its session material was
  kept shape-only by this scribe), so the lane deliverables in this repo ARE
  the wave record (observation, same as round 1). Content lanes:
  TAMESHI-R2-1 → `corpus/knowledge/mutation-case-kimi-census.md` (206
  `wc -l` lines, final line unterminated): the corpus's first measured
  kill-rate — kumitate `kimi-census.mjs`'s 43-case hermetic suite vs 10
  single-edit mutants (fresh /tmp copies, one exact edit each, driver
  asserts the old string unique; original byte-identical, sha256
  before=after `83016d45…`) → **8/10 killed (80 %)**; control 43/43, every
  mutant run still enumerated 43, no inconclusive run, 7.0 s sweep;
  survivors D2 (`findings.slice(0,6)`→`(0,5)` — truncation boundary never
  exercised: max findings in any suite run = 2 vs cap 6, DRIFT asserts
  prefix-only) and D10 (`FROZEN.K2 25`→`24` — only `frozen.K5` asserted),
  both "reported-but-unasserted surfaces"; per-kill failing-case labels
  (D4 = exactly the 3 root-enum cases, D8 = the 3 fail-closed cases,
  D1/D3 = 16 each incl. the exact green baseline); errata E1 — the author's
  D7-survivor expectation was wrong (the fixtures' modes share floor bits),
  kept as a calibration miss; scope honest: measures the suite, not
  substrate drift [I]; U1–U6.
  TAMESHI-R2-2 → append-only errata applied to all three wave-1 notes from
  the wave-1 review trail: kumitate K-R2-1…4 (six executed counts + sha256
  pins re-verified held; §7 meta-check anchor pair corrected to
  `claims-check.mjs:851-852` / `kimi-census.mjs:841-842`; mutation census
  stands minus SKILL false hits; carried items stay recorded-not-absorbed),
  kagi G-R2-1…6 (claim-ledger pin corrected to 79301 B /
  `93c5827202b9cdec` — the surveyed 79294/`357fb245` was an uncommitted
  dirty state, re-pinned by kagi's own round-18 `fecee87`; §9 citation
  corrected :53-56 → :26-28; denied verbs 22→23; 250 selftest cases +
  `--falsify` 16/18 held; §8.1 [UNK] discharged = kagi's own in-flight
  round-18 [INF]; F-2/live-verdicts stay sibling-owned), fleet V-R2-1…4
  (kaidoku 72 files / 468 vs 467 held; w6–w8 AGREE tallies held; U1/U2 stay
  open; U1 first reading = grep-shape artifacts). Nothing above any errata
  block was edited (append-only per QUALITY.md 4).
  TAMESHI-R2-4 → `verification-patterns-fleet.md` extension: the census's
  fourth pattern, from game-dev-2d-shokunin's verifier machinery (read-only,
  @ `9fb50aa9`) — D0–D10: committed-bytes replay (a commit lacking the
  change IS the finding, r64); scratch-only mutants + fault probes;
  sensitivity = guard-disable in a disposable copy (binary per guard, no
  kill-rate tally — U8); a detected mutant must survive spoof
  classification, engine errors never count as detection; opt-in probes
  proven inert unflagged; verifier-owned instruments + spec recompute;
  7-field regression fence vs prior receipts; falsification first-class
  (r64 DISAGREE → landed bytes; r69 verifier-seat death recorded);
  receipts located (lessons-JSON era → in-tree scratch); declared
  bounds/non-writes — plus U8–U13 and 2 predictions; explicitly
  single-lane, NOT general (PROVINCE.md). Lane-end newline repair proven by
  `head -c 16536 … | sha256sum` → `df4ab192…` (prefix byte-identical).
  Fourth write → `SKILL.md` round-2 distillation (+73 → 244 lines, no lane
  header; distillation lane inferred per round-1 precedent): the measured
  mutation-bar decision table — kill-rate bands >80 % / 50-80 % / <50 % with
  admission readings (bands are a report convention, not a pass/fail gate;
  8/10 admits, <50 % admits with the gap recorded), mutation-craft rules
  (copy-inject one exact edit per fresh copy, hash-proven restore, defect
  taxonomy with each class's kill sets, survivor-is-a-finding /
  a-kill-names-its-case-set, when-mutation-testing-is-not-worth-it), every
  rule citing its note line.
  Audits: the round's in-tree audit evidence is per-claim re-runnable —
  every errata entry carries its own command (re-executed by this scribe,
  below); R2-1 retained per-defect evidence under
  `/tmp/tameshi-r2-1-work/evidence/` (control + 10 mutants: stdout, exit
  code, meta); R2-4's lane-end state check with byte-proof.
  Scribe verification (this entry, all re-run 2026-10-14): `node
  kumitate-shokunin/scripts/kimi-census.mjs --selftest` →
  `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (kill-rate
  denominator held); `sha256sum …/kimi-census.mjs` →
  `83016d45049b009a…4f426`, kumitate tree clean for the path, HEAD still
  `175de6ba`; D2/D10 sensitivity probes re-run from the retained scratch →
  D2 five ids + `+23 more`, D10 `frozen=24` (both survivors observably
  different off-suite, as claimed); `grep -cF '**killed**'` → 8 /
  `'**survived**'` → 2; `grep -n` on both meta-check patterns →
  claims-check :851/:852, kimi-census :841/:842 (K-R2-2 exact);
  `sha256sum kagi-shokunin/corpus/claim-ledger.sh` → `93c5827202b9cdec…` +
  79301 B + `git -C kagi-shokunin log -1` → `fecee87` round-18 10:05:10
  (G-R2-1 exact); DENY_RE pipeline → 23 (G-R2-3); `sed -n '26,28p'` = the
  final-line rule vs `'53,56p'` = the usage paragraph (G-R2-2); claim-ledger
  `SELFTEST: PASS (97 cases)` + scope-gate `SCOPE_SELFTEST: PASS
  (61 cases)` exit 0; `--falsify` exit 1 → `SCOPE_FALSIFY: FAIL
  (caught=16/18 failed=2)` with 2× `SCOPE BREADTH-EXCEEDS`, kagi tree
  porcelain-empty before/after, `corpus/README.md:43` still `18/18`
  (G-R2-4); kaidoku 72 / 468 / 467 (V-R2-1); w6/w7/w8 AGREE grep → 3×5/5,
  3×5/5, 2×6/6+1×5/5 (V-R2-2).
  SCORECARD round-2 moves: depth improved (first measured kill-rate + SKILL
  bands), calibration improved (15 append-only errata entries: 14 R2 + E1;
  4 corrections applied to the record, nothing silently rewritten; counting
  commands in the move-log rows). Scribe erratum SC-1: this scribe repaired
  a stray trailing `|---|` left at SCORECARD.md EOF by the round-1 append
  (it rendered a phantom cell on the round-1 calibration row); repair noted
  here, not silently dropped (QUALITY.md 5).
  Carried to round 3 (recommendations, not absorbed): kumitate integration
  groups + round-gate `INTERNAL_ERROR` arm, and kagi live verdicts 5/6 +
  F-2's two-lines-per-path fix, stay sibling-owned; U1/U2 open (V-R2-3)
  with U1's first reading recorded (V-R2-4); mutation-note U1–U6
  (coordinated two-table edit, multi-site rewrites, other-gate survivor
  generality U4, node/host stability U5); SKILL's open U: the 50 %
  crossover is unmeasured and PROVINCE's ≥2-lane rule blocks calling the
  kill-rate method fleet-general — a second-gate sweep is the natural
  round-3 depth move; game lanes' binary guard-disable (fleet D3) vs this
  round's measured kill-rate give the mutation bar its two named tiers.
- 2026-10-14 — round 3: probation wave 3 (probation-completing), planned as a
  ufo-round-plan (`plans/round-3.plan.md`, ufo-round-plan-v1 — axis move
  depth(cross-language generality) + operability(first tool); falsifiable
  claim pre-registered with its anti-claim: a wild bash-vs-JS kill-rate
  divergence IS the finding). Same dispatch shape as rounds 1–2 — lane
  write-scopes left this LOG to the scribe; the lane deliverables in this
  repo ARE the wave record (observation, rounds 1–2 precedent). Content
  lanes:
  TAMESHI-R3-1 → `corpus/knowledge/mutation-case-kagi-census.md` (258
  `wc -l` lines, final line unterminated): the second measured kill-rate,
  first bash gate — kagi `surface-census.sh`'s 16-case selftest vs 10
  single-edit mutants (fresh /tmp copies, one exact edit each, count==1
  gate; kagi tree never written, restore proof sha `275d8294…53009f`
  before=after, mtime + porcelain clean) → **8/10 killed (80 %)**, no
  inconclusive run, suite count held on every run, 11.0 s for 11 runs;
  survivors B5 (deleted exec x-bit arm — **fixture-absent arm**, a survivor
  class round 2 did not have; non-equivalence probe: mutant prints
  `SURFACE OK … (exec 644)` where pristine prints `SURFACE DIVERGED`,
  exit 0 vs 1) and B10 (CLEAN-summary `ok=` arg swapped — reported-never-read,
  same family as round-2 D10); B4's kill is token-only (deleted symlink arm
  keeps exit=1, dies on the `SURFACE LINK` token assert); gate choice proven
  hermetic on this host (fixtures under `mktemp -d`; verbs cases 15/16
  `skip-case … substrate-absent` — `the-janitor` off PATH, kagi's own
  round-18 repair, kagi LOG.md:741-744); errata E1 — failing-case *counts*
  predicted 6/10 (case 04 is a second exit-0 green fixture, kept as a
  calibration miss, same shape as round-2 E1); cross-language §4 resolves
  the plan's anti-claim: same headline rate, narrower bash kill width
  (max 3/16 vs JS up to 16/43 — per-case fresh fixtures + exit+token asserts
  vs shared fixtures + exact-line asserts), shared survivor class
  reported-but-unasserted data (D2/D10, B10), bash-only unreached-arm class
  (B5); U1–U6.
  TAMESHI-R3-2 → `tools/mutate-and-run.sh` (611 lines, r3-2): tameshi's
  first tool — the method ships as a generic inject→run→restore runner:
  spec v1 fail-closed parsing (count==1 asserted before any suite run,
  no-op edit refused, escape allowlist `\n \t \r \\`, CR refused), pinned
  pristine + fresh byte-copy mutants, green-control gate before any mutant
  run, KILLED / SURVIVED / INCONCLUSIVE (124/126/127) per defect,
  `MUTATE_RESTORE: OK|DRIFT` byte-identity proof, evidence workdir, exit
  map 0/1/2/64; hermetic selftest (own fixture + mini-suite under
  `/tmp/tameshi-r3-2-selftest.*`, removed on PASS) — **24/24 pass**.
  TAMESHI-R3-3 → `SKILL.md` round-3 distillation (+421 → 665 lines, no lane
  header; lane id inferred from dispatch shape per round-1 precedent — its
  scratch holds `SKILL.draft.md` + a sha-poll script): the method as an
  executable recipe — 10 numbered steps pin→note (hermetic-control proof,
  committed-bytes pin, count==1 uniqueness gate, one-edit-per-fresh-copy
  runs, verdict adjudication incl. token-only kills, survivor
  non-equivalence probes, restore proof, note format), defect-entry
  template + 6 exact-string rules + a 12-row class catalog with per-class
  JS **and** bash evidence columns, restore-discipline checklist, the
  measured cross-language divergence section, and Appendix A/B — complete
  reproduce specs for both cases (driver + manifest + expected outputs);
  the claim "an executor with no oral context can run either case from this
  page alone" is pre-registered in the file header.
  TAMESHI-R3-4 → `corpus/knowledge/executor-test-sufficiency.md` (211
  `wc -l` lines, final line unterminated): the no-oral-context executor
  test (SHONEN box 3 evidence) — an executor with no tameshi context beyond
  `SKILL.md` @ `dd2f4dee…3753` reproduced one killed mutant end-to-end
  (D5: control green 43/43 first try, kill `42/43 FAIL` with exactly
  Appendix A's singleton failing case `MEMBER_MISSING … presence is gated`,
  all 10 manifest strings byte-exact and unique, restore pin held);
  per-step sufficiency verdicts recorded (7× SUFFICIENT, 2× SUFFICIENT
  (latitude), 1× ADDITIVE-IMPROVISATION — the single-mutant `--only`
  subset, 1× NOT EXERCISED, 1× ADAPTED); contamination statement §1 (read
  SKILL.md + target only; even skipped the generic AGENTS.md reminder to
  stay uncontaminated); U6 noted no independent re-verification at write
  time — closed below by the audit replays.
  Audits (round-3b batch, non-author verifiers, evidence retained under
  their scratch namespaces):
  TAMESHI-B1 — rebuilt bash mutants B1/B5/B10 from a pristine byte copy
  (`cmp`-verified) with its own driver (`mutate_b110.py`, count==1 asserts):
  control `SELFTEST: PASS (16 cases)`, B1 killed `SELFTEST: FAIL (1/16
  cases)`, B5/B10 green `PASS (16 cases)` — the note's kill rows and both
  survivor rows replay.
  TAMESHI-B2 — re-ran the executor's exact target through the shipped tool:
  spec = Appendix A's D5 entry, result `D5 KILLED` 42/43 with the same
  singleton failing case and mutant sha `b0dfe1a7…0668` identical to B3's
  sweep and the executor's note (R3-4 U6 closed).
  TAMESHI-B3 — full 10-defect sweeps on BOTH cases through the tool
  (`dsweep` + `bsweep`): `MUTATE: DONE (… killed=8 survived=2
  inconclusive=0 kill-rate=80 %)` on both targets, every per-defect verdict
  and failing-case count identical to both notes' tables (B1 1/16, B2 2/16,
  B3 3/16, B4 1/16, B6 2/16, B7 1/16, B8 2/16, B9 2/16; D1 27/43, D3 27/43,
  D4 40/43, D5 42/43, D6 41/43, D7 41/43, D8 40/43, D9 41/43),
  `MUTATE_RESTORE: OK` ×2, tool sha `d8abee52…eda68` = the committed
  revision.
  Scribe verification (this entry, TAMESHI-B4, all re-run 2026-10-14; logs
  under `/tmp/tameshi-b4-r3b-verify/`): both fleet selftests green (`bash
  kagi-shokunin/corpus/surface-census.sh --selftest` → `SELFTEST: PASS
  (16 cases)` exit 0 with skip-cases 15/16 substrate-absent, kagi tree
  porcelain-empty before/after; `node kumitate-shokunin/scripts/
  kimi-census.mjs --selftest` → `KIMI_CENSUS_SELFTEST: 43/43 pass` /
  `VERDICT: PASS` exit 0); pins held (`sha256sum` → SKILL.md
  `dd2f4dee…3753` = the executor's executed revision, tool `d8abee52…eda68`
  = the audited revision, kimi-census `83016d45…4f426`, surface-census
  `275d8294…53009f`); note tallies (`grep -cF '**killed**'` → 8,
  `'**survived**'` → 2, table rows → 11); anchors byte-exact (`sed -n
  '241p;214p;862p;85p'` on the pinned gate = the four cited edit sites);
  independent re-sweep through the tool from a spec cut from the pinned
  artifact (`python3` builder asserts every count==1) → `CONTROL: GREEN`,
  B1–B9 killed with failing counts 1/2/3/1/2/1/2/2 of 16 exactly as the
  note's table, B5+B10 `PASS (16 cases)`, `MUTATE_RESTORE: OK` before=after,
  `MUTATE: DONE (target=surface-census-b4 defects=10 killed=8 survived=2
  inconclusive=0 kill-rate=80 %)`, exit 0; tool selftest 24/24; executor
  evidence dir present (`results.json`: control_green true, D5 killed,
  node v24.21.0).
  SCORECARD round-3 moves: depth improved (second kill-rate on a second
  language — same 80 % headline, divergence finding in kill width +
  survivor composition; counting commands in the move-log row), operability
  improved (first tool, selftest 24/24, both fleet cases reproduced through
  it; counting commands in the move-log row).
  SHONEN.md boxes updated with the audit lanes as named non-author
  verifiers (`[x]` per PROTOCOL.md mark spec — each box cites its verifier's
  retained evidence): SKILL craft → TAMESHI-B3 (appendix manifests replayed
  end-to-end through the tool), end-to-end task → TAMESHI-B1 (independent
  driver replay of the bash case's control + kill + both survivors),
  no-oral-context → TAMESHI-B2 (the executor's D5 kill re-run through the
  tool, same verdict + same mutant sha), PROVINCE accuracy → TAMESHI-B3
  (`MUTATE_RESTORE: OK` ×2, both sibling trees porcelain-clean — read-only
  discipline held by every lane that touched a substrate).
  Carried to round 4 (recommendations, not absorbed): kumitate integration
  groups + round-gate `INTERNAL_ERROR` arm, kagi live verdicts 5/6 + F-2's
  two-lines-per-path fix — still sibling-owned; bash U2/U3 (verbs-path
  mutants are host-gated) and U4 (fallback `checklist-run.sh` unmeasured);
  both cases' U1 (coordinated multi-edit rewrites) and U5 (cross-host
  stability); the 50 % crossover remains unprobed — both measurements sit
  at 80 %, so the band interiors are still unmeasured; the executor's U3
  (full-sweep driver run from SKILL.md alone, survivor probes, Appendix B
  execution) is the natural no-oral-context completion; SKILL's band table
  still carries the ≥2-lane generality bar — a third gate (or a fleet
  lane adopting the tool) is the next depth move.
- 2026-10-14 — round 4 (training r3): arm-class matrix (JS+bash cases) + round-gate static projection (§13); mutate-and-run --regression mode; VER-T1 cross-verified row E CONFIRMED with 2 precision errata (chmod enumeration :608/:654, JS wording scope). Axis moved: calibration. Verifiers: VER-T1 | matrix disagree-where-it-disagrees is the finding; row E exactly 1 instance in 20 (B5, proven unreached by one-row probe). 32-lane wave (27+1+4 after an alibaba filter failure rerouted 4 lanes to hyper — recorded).
