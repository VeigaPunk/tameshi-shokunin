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
- 2026-10-14 — round 5 (training r4): 3rd mutation case (tsukuroi gate, cross-author): 6/10 killed, matrix amended per arm-class evidence (not smoothed); VER-T1 errata landed; fleet-suite census note. Axis: depth. Verifiers: 60% third profile vs 80/80 — divergence IS the finding; hardening-gap replay (S5-1 closed 1/4 survivors).
- 2026-10-14 — round 6 (training r5): the service round on mado's gate: 4/10 killed, in-surface 4/4 vs out-of-surface 0/6 — the co-extensive assertion/kill finding; own-tool meta-hardening (selftest 55/55; regression mode 2/2 within band). Axis: adjacency + operability. Verifiers: VER-T6 | independent re-sweep identical mutant shas.
- 2026-10-14 — round 7 (training r6): the leg ledger: --regression replays ALL 4 recorded cases at pinned git blobs (drift-immune; 4/4 PASS; expectation-flip fails loudly; selftest 67/67); fleet kill-rate ledger; opt-in protocol note; cross-lane audit confirmed git-show-only reads + zero working-tree writes. Axis: operability. Verifiers: AUD-X7 | VER-T7.
- 2026-10-14 — round 8 (training r7): cases 5+6: kagi checklist-run (47%, third co-extensive instance, 15/15 pre-registered predictions) + kumitate claims-check; ledger at 6 gates; the re-sweep cadence note. Axis: coverage. Verifiers: VER-T8 | AUD-T8.
- 2026-10-14 — round 9 (training r8): the cadence tick fired: 4/4 legs PASS; drift chains recorded (tsukuroi/mado r8 commits resolved the transients); the 4-vs-6 leg cut named for the tool owner; the service limits note (what tameshi refuses and why). Axis: operability. Verifiers: VER-T9 | peer pin-read corroboration.
- 2026-10-14 — round 10 (training r9): the operator runbook (511 lines, cold-readable, exercised receipts); the leg cut resolved (6-leg regression); the service standing-state boundary table. Axis: operability. Verifiers: VER-T10 cold-reader | AUD-T10.
- 2026-10-14 — round 11 (training r10, the arc's final round): the close — the
  pre-announced tick fired, the schedule is handed across, the ten-round
  record completes. Planned as a ufo-round-plan (`plans/round-11.plan.md`,
  300 L / `068578f1…`, committed inside round-10's landing `606716f` @
  21:28:23Z — the announcement, leg 1). ONE move, operability terminal, three
  legs: the pre-announced tick · the operator schedule · the 10-of-10 record +
  discharge. Same dispatch shape as rounds 1–10 — the lane deliverables in
  this repo ARE the wave record (no `.ufo/waves/tameshi-r11-*` directory);
  lane roles below from file credits + scratch names [U — the dispatch itself
  was not visible to this scribe].
  Tick (leg 1) — executed exactly as announced; five independent firings:
  T11-4 21:32:35Z (first; `--regression` `REGRESSION_DATE 21:32:40Z`) ·
  T11-3 (regression 21:33:55Z) · T11-1 21:35:54Z · SCR-T11 21:36:27Z ·
  AUD-T11 21:37:16Z — every read **4 current · 2 stale · 0 drift** (tsukuroi
  `084951be…` → live `10452443…` @ `af8adf1`; mado `d7edaab4…` → `93e43f8f…`
  @ `f7bfc9f`; all six = HEAD blobs, recorded revs ancestors of HEAD, trees
  clean at every read); tool pulse `--selftest` **80/80** rc 0 and six-leg
  `--regression` **`PASS (cases=6 passed=6; ledger legs exact:
  killed-delta<=0 flips<=0)`** at `75ed934d…` (**held** — the r10-2
  revision), every leg exact (`match=10/10` legs 1–4/6, `match=15/15` leg 5,
  `flips=0`). Appointment pair: announced `068578f1…` @ `606716f`
  (21:28:23Z) → first firing 21:32:35Z, **Δ +4 m 12 s** — announced, not
  unannounced; the committed bytes = the live bytes (AUD-T11 claim A
  CONFIRMED). AUD-T11's independent leg-check beyond the tool's own selftest:
  **`LEGCHECK: PASS (6/6 legs clean)`**, 65/65 mutants re-applied
  byte-identical.
  Schedule (leg 2) — `corpus/knowledge/closeout-r11.md` §2.5 (T11-1;
  `cea3352a…`, 420 L, untracked at close) carries the schedule as landed: the
  command set; fire classes (round boundary · opt-in request · owner-committed
  gate move · re-pin), each with who fires it + where the receipt lands;
  readings `current|stale|drift` · tool `held|moved`; triggers T1–T3 + the
  re-pin rule; the tick series 1–4 each with its own receipt (19:15:14Z ·
  20:00:34Z · 20:52:19Z · 21:32:35Z); the gap series **45 m 20 s · 51 m 45 s ·
  40 m 16 s** (boundary-bound, not clock-bound; recomputed exact by the
  audit); and the interval **`[U]` — set and kept by the seat the handoff
  names, not the lanes'** (`plans/round-11.plan.md:96-103`). No daemon, no
  timer; a table + receipts.
  Closeout (leg 3) — `corpus/knowledge/closeout-r11.md` (T11-1): the ten
  rounds restated with no cell re-adjudicated (§1, `:42-59`), the service as
  it stands (§2: tool · six-leg ledger · opt-in protocol · limits · schedule ·
  boundary), handed-across vs lane-owned (§3), the named debts each anchored
  (§4: the tsukuroi clause-site pattern; the 4-vs-6 → 6-leg resolution
  receipt; the rest of the ledger), three executed spot-checks (§5), sources
  (§6), unknowns (§7).
  Also landed: `plans/completion-evidence.md` (PACK-T; rounds 2–11 one line
  each + SHONEN status + the debt table — the parent's audit input;
  `:27-41`); `SKILL.md` final-pointers section (T11-4: +100/−1 → 1 461 L /
  `bfbdd2fd…` — the standing map, the boundary readings, what stays open);
  `corpus/lessons/round-10.md` (T11-2; the runbook lesson — the register's
  first entry).
  AUD-T11 (read-only) → `reports/r11-aud-t11.md` (**new**; `03b18ee4…`,
  194 `wc -l`): 12-row verdict table — **CONFIRMED ×12** (the closeout
  landed + stable ×4 samples; the appointment pair; the executed set = the
  announced set; the tick series; the six-leg re-run `cases=6 passed=6`
  21:34:12Z; the zero-debt check 9/9 open with no false closure; §2/§1/§6
  spot-checks), two minor findings recorded not repaired (F1: tick 1's cell
  renders `—` while its cited receipt carries the 4·2·0 reading; F2: §2.6's
  visibility counts restated without an as-of — re-run drift 17/27, direction
  holds); declared contamination; `reports/r10-ver-t10.md` still absent.
  Scribe (SCR-T11, this entry; scratch `/tmp/w11-scr-t11/`): re-ran the pulse
  and the six-case read itself — `--selftest` 80/80 rc 0; `--regression`
  `cases=6 passed=6` (`REGRESSION_DATE 21:34:27Z`, tool `75ed934d…`); pin
  read 21:36:27Z → 4 · 2 · 0, agreeing cell-for-cell with the four lanes;
  poll 60 s × 30 samples, `POLL DONE 2026-10-14T22:04:16Z` (`poll.log`);
  SCORECARD round-11 row + the ten-training-rounds verdict table (rounds
  2–11) completed — the final row anchored to the tick receipts + the
  closeout + the audit.
  Open at close (each anchored): the two `stale` successor rows — **no
  appended rows at this write**, the ledger byte-identical `2f25c51e…`
  (closeout §4.3; AUD-T11 debt-check #1); the ledger's §1 "cases 1 and 2
  only" text + the six-leg registry row; the runbook's four-leg lines (ER-R3
  open); the census §5 instrument re-pin errata; the coverage rows
  (`corpus/README.md`, 20 L); the fresh-executor sufficiency table
  (`reports/r10-ver-t10.md` absent); tsukuroi's 9 un-exercised clause sites
  (owner's; closure at its live revision `[U]`); the attestation leg (protocol
  U1) + the fleet-contributed case + third-lane adoption; the queue's ten
  surveyed-but-unmeasured gates; all registers' unknowns (ledger U1–U9,
  protocol U1–U6, limits U1–U5); the interval / adoption / driver `[U]`s.
  Axis: operability (terminal — the close). Verifiers: AUD-T11 (12-row
  verdict table, CONFIRMED ×12) | VER-T11 (poll lane; `reports/r11-ver-t11.md`
  not landed at this write — the state, not smoothed).

- 2026-10-15 — fleet round-1, calibration baseline (separate from the
  completed historical training arc). Motivating evidence: at
  `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d`, `SCORECARD.md` has a move log
  but no current numeric axes table; `SHONEN.md:5-34` marks every box `[x]`
  using tameshi-dispatched B1/B2/B3/B4 evidence and temporary paths.
  Canonical `PROTOCOL.md:63-73,340-343,413-431` requires lane-dispatched
  agents to count as the lane, durable evidence, and canonical box wording.
  Added bounded current-axis rubrics and commands to `SCORECARD.md`:
  command D observed `recorded_cases=6 depth_score=6`; command C observed
  `boxes=4 checked=4 asserted=0 untouched=0 calibration_score=0`.
  Selected the lower axis, calibration. One intended improvement: truthful,
  source-linked promotion assertions, not promotion or a tool-code change.

- 2026-10-15 — fleet round-1 interactive continuation, **blocked at
  dispatch; no completed-round credit**. Motivation: inherited HEAD
  `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` closes the historical
  training arc, while this separate fleet calibration round left six
  tracked paths dirty plus an untracked lesson/audit. The entry inventory
  and inherited diff are retained under `.ufo/evidence/fleet-round-1/`;
  native session bodies were neither opened nor committed.
  The current WWKD is `.ufo/plans/fleet-round-1-interactive-wwkd.md`.
  Re-read canonical UFO run-logic §§0/4.3/5 and shokunin's ordered
  protocol/appendix/mission/axes/corpus/learning inputs. Operator
  exact-32, no-push and repo-local report directions supersede the old
  headless prompt. Driver counter 1 is not a completed-round count.

  Lowest LIVE axis: calibration, selected from SCORECARD's current
  assigned baseline, not historical terminal rows. Reconciled inherited
  SHONEN/skill/audit/lesson/pack corrections: four unsupported promotion
  marks become three bounded lane assertions and an unchecked
  cold-reader box. Historical LOG/pack/round-11 independence claims
  remain byte-preserved and are explicitly superseded by the audit's
  authority correction. No promotion or outside spot-check is claimed.
  Direct source reads supported the table/error/checklist, historical
  task and method/product boundary; the historical one-JS-mutant note
  explicitly does not support a current full-sweep/bash cold-read.

  Dispatch prerequisite failed without a model probe: the global
  routing metadata and live `cfg://task/agentModelOverrides` retain
  generic `@m_mid/@m_fast/@m_strong` seats instead of the required
  content `@m_composer`, audit `@m_grok`, connector `@m_antigravity`
  bindings; the connector chain lacks the configured `@m_zfl` target.
  Exact role-by-role observation:
  `.ufo/evidence/fleet-round-1/route-bindings.json` and
  `live-seat-bindings.txt`. No config changes, route substitutions or
  new routing overlays. The canonical planner validated exactly 32
  distinct, substantive scopes with exit 0, saved under
  `.ufo/waves/fleet-round-1-interactive/`. No rendered `run`, registry,
  task batch or specialist completion is claimed. The predecessor's
  nine-seat narrative is not compliance with this dispatch.

  Own verification, not recalled output:
  `calibration-acceptance.json` records baseline FAIL
  (`canonical=false marks=["x","x","x","x"] durable-links=0/4`)
  versus candidate PASS
  (`canonical=true marks=["~","~"," ","~"] durable-links=4/4`);
  comparison exit 0. `selftest.json` captures all 80 case lines and
  `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, exit 0.
  `cli-smoke.json` captures the real mutation CLI at 05:10:40Z:
  green control, `wrong-value` KILLED (exit 1), `unread-value` SURVIVED
  (exit 0), `MUTATE_RESTORE: OK` with identical full hashes, and
  `MUTATE: DONE (target=fleet-round-1-interactive-smoke defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%)`,
  exit 0. These files retain commands, complete output and exit codes.
  This is a bounded fixture task, not a new fleet rate, whole cold-read,
  live-gate census or native judgment. The owned runner is unchanged at
  `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`;
  no sibling regression was run. The reported red Phase 0 was not
  rerun merely to confirm it.

  Local candidate axes: calibration improved; depth, coverage,
  operability, freshness and adjacency unchanged. Learning: expansion
  unchanged, quality improved, discernment unprovable-but-better.
  Formal admission is **blocked**, not a scalar pass or a completed
  round: exact-32 route realization and outside evidence remain debt.
  `corpus/lessons/round-1.md` ER-I1 corrects stale line references and
  the old invalid `unprovable` token append-only. Route owner must bind
  the requested existing aliases before authorized fresh-session
  redispatch; an independent reviewer must check at least one admit
  and one reject; a scoped fresh executor must separately establish
  current full cold-read sufficiency. All are named, not closed by
  prose. Shared ledgers and source/host remediation stay owner-only.


  Receipt/interactive-surface observation for this same attempt:
  `.ufo/evidence/fleet-round-1/receipt-applicability.json` records own
  Sighting mission `m_53a61cfda7e640978585bebb05a4686a`, run/session
  `shk-tameshi-interactive-20261015T050057Z`, status running,
  dispatch kind `argv` with only `argv/kind` keys, and no taskKey or
  receiptPath in its metadata. Launch metadata contains only lane/cwd/
  run/session/mission/pane/time, not a receipt acceptance bag. The
  canonical receipt CLI requires real task identity and dispatch-time
  prompt/config/report bindings; no arbitrary task key or global-config
  digest was substituted. No receipt was minted or validated and no
  Sighting completion was invoked. Integrator must supply an applicable
  dispatch contract before mint/expected-field validation. The direct
  pane-shape command returned `%6 node /dev/pts/6 0`, exit 0: an alive
  interactive pane, not round-completion evidence. Owned smoke scratch
  was removed after its full output was persisted. Corpus index and
  completion pack now point explicitly to this admission hold.


  Scratch-policy correction before commit (same attempt): the 05:10:40Z
  `.ufo/scratch` CLI run contradicted `SKILL.md:25-28`. Its complete
  output remains in `cli-smoke.json` as **nonconforming**, not accepted
  craft proof; later deletion did not cure the error. Corrected only the
  namespace and repeated the real CLI in a fresh
  `/tmp/tameshi-r1-interactive-4oejhl9z/`, 05:14:49Z, at the same
  runner SHA. `cli-smoke-canonical.json` retains the self-contained
  reproduction and full output: control green; `wrong-value` KILLED
  exit 1; `unread-value` SURVIVED exit 0; `MUTATE_RESTORE: OK` with
  identical hashes; `MUTATE: DONE (target=fleet-round-1-interactive-canonical-smoke defects=2 killed=1 survived=1 inconclusive=0 kill-rate=50%)`;
  runner exit 0, assertion-driver exit 0. Temporary files removed after
  capture. The audit's scratch erratum, lesson ER-I2 and SCORECARD
  explicitly supersede the earlier run for admission. No repeat of the
  valid selftest or the reported Phase 0 failure. This correction does
  not remove the dispatch or receipt blockers.


- 2026-10-15 — fleet round-1 blocked handoff publication. Owned content
  landed as `cd31c6b7e4ee6becf32f1eedf874f1bdda8d5ac6` with explicit
  pathspecs and the tameshi lane identity, no push. Only after that
  landing, wrote `.ufo/reports/round-1/tameshi.md` with the exact
  measured content commit, complete gate/operative-smoke verdict lines
  and exits, all six local axis verdicts, three learning verdicts,
  SHONEN assessment and owner-specific unblocks. Wrote the fresh-session
  handoff `.ufo/continuation/fleet-round-1.md` and `.json`.
  Report and handoff retain the initial nonconforming scratch run and
  identify `cli-smoke-canonical.json` as operative evidence. They
  explicitly withhold verified-round credit, native judgment, receipt
  acceptance and Sighting completion: required role aliases are absent,
  and the direct interactive launch exposes no applicable receipt task
  contract. The operator's at-least-100 verified-round target is
  unchanged. This is one observed blocked attempt, not saturation or a
  proven three-consecutive-block stop. No second round was started;
  current pane and native session runtime remain preserved for the
  operator. Shared ledgers/reports and route/receipt setup remain the
  fleet integrator's responsibility.

## 2026-10-16 — protocol conformance: SCORECARD contract fields

Operator amendment rollout (fleet-root `84bade0`, 2026-10-16): appended
the standalone SCORECARD contract sections the file did not already carry
as recordable sections.

Already present: axes — the real score table under `## Current axes —
fleet round-1 baseline`; `planned` and `retired` existed only as nested
inline labels (`**Planned:**` / `**Retired:**`) inside the historical and
blocked-state sections, so standalone `## Planned` and `## Retired`
sections were appended too.

Added: `## Capabilities` (repertoire-table scaffold, no rows — none enter
through this rollout) and `## Saturation` (the lane declares its
saturation line + stagnation window N on its next round per `AXES.md`
§The stagnation nudge); neither is asserted by this conformance change.

No axis claim was made by this change and no score moved; nothing was
re-measured, re-adjudicated, or back-filled — purely additive.

## 2026-10-17 — repository README

- **Trigger.** The repository root had no `README.md`.
- **Evidence.** Method-versus-product boundary is `PROVINCE.md`. Recipe and the measured-case limit are the opening of `SKILL.md`. Runner contract is the header of `tools/mutate-and-run.sh`. Ran `bash tools/mutate-and-run.sh --selftest` on 2026-10-17: `MUTATE_SELFTEST: 80/80 pass`, exit 0.
- **Action.** Added `README.md`. Corpus indexes were not edited. No Devin wiki URL was present.
- **Outcome.** No axis claim; no score moved.
