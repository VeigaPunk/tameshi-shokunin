# tameshi-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `knowledge/gates-survey-kumitate.md` | The six hermetic suites: executed case counts 62/42/60/102/39/43 (all `--selftest` exit 0; literal `check(` sites 62/42/60/71/35/41 — counts are loop-sensitive, so the executed summary line is the only honest count); uniform two-line close (`n/m` summary + `VERDICT:`, usage exit 64 everywhere); fail-closed arm inventories (proxy 12/12 arms fired, claims 5/5, kimi-census 1 token ×3 cases, round-gate 7 declared/6 fired with `INTERNAL_ERROR` uncovered, surface-probe + cite-check carry no token enum at all); verdict-line exactness tiers (full-line literal → anchored regex → startsWith → includes); mutation controls = cite-check's mutation copy (integration-gated, never under `--selftest`) + claims-check's external env-poison probe — no kill-rate harness or self-code fault injection anywhere in the corpus (I: the "every declared kind fires" meta-checks prove each branch is reached, not that a wrong implementation would be caught) | kumitate-shokunin/scripts/*.mjs read-only; six `node <gate>.mjs --selftest` runs with exit codes + verbatim summary lines (note §0); grep/wc censuses in-note |
| `knowledge/gates-survey-kagi.md` | The six kagi gates: 250 selftest cases green 6/6 from the suites' own counters (static `cases+1` site counts 6/1/0/1/6/2 are wrong — mutation and breadth loops register cases dynamically); one three-valued exit lattice, same meaning in all six; four distinct exit-2 classes (setup/cannot-measure; malformed committed data — "not a verdict", with two opposite resolutions across gates; POLICY — refused before the effect; zero-work — a gate that measures nothing must not exit 0); five evidence-discipline habits (verdict = expected exit AND expected ERE on the last non-empty line; verdicts carry their counts; count-only pins where a name would leak; abstention declared/counted/exit-neutral with a both-paths selftest; secret hygiene as a header prohibition, and the gate never echoes a claim's output); findings F-1 (`--falsify` measures 16/18 live vs README's unqualified 18/18 — adjudicated host-state dependence by the scratch-case discriminator, neither defect nor clean) and F-2 (3 of 6 `policy_check` refusal paths — `inline-shell`/`backslash`/`empty-quotes`, precisely round-11's bypass class — asserted by no selftest case); ER-1 keeps 16 self-caught wrong-line citations as evidence | kagi-shokunin @ `4e48b771` read-only; six `--selftest` runs + live `scope-gate.sh --falsify` (exit 1, verbatim lines) + `sed -n` line re-checks + stamps recompute `ok=56 stale=0` (note §2, §5–§7) |
| `knowledge/verification-patterns-fleet.md` | The shared verifier shape P1–P10, called general only on ≥2 independent lanes: declared falsifiable claim before the move; named non-author verifier replaying committed/retained state; byte-identity as the top verdict class with an explicit volatile-scrub list; prior-rows regression fence; verdict tallied to the verifier; falsification first-class; post-verification changes carry their own proof; the verifier catches author defects; scope-partitioned writers with retained receipts; a cross-lane adversarial layer audits and reports, never fixes siblings. Lane-specific (explicitly NOT general): kaidoku's audit-block grammar (`verify:`/`verified-at:`/`suggested:`, CONFIRMED/UNVERIFIABLE, ev-id identity domain `f(content,path,params)`, 3-run content-address proof) and the game lanes' AGREE-tally encoding (8-seat set, closeout.json schema, battery-row metrics, git-archive baseline freeze, Sol per-axis adjudication); 3 falsifiable predictions; unknowns U1–U7 named | kaidoku corpus + `.ufo/waves/kaidoku-r5/01–02` + `.ufo/waves/shokunin-train-20261014-w6..w8` (closeout/spec/tasks/xsentinel) + game-lane LOGs and round reports, all read-only; census commands (ls/grep/sort/uniq/wc) in-note §Verification |
| `knowledge/gates-survey-kumitate.md` — round-2 addendum (K-R2-1…4, append-only) | All six executed counts + artifact pins re-verified held on the current bytes (sha256 first16: cite-check `40573448…`, surface-probe `148cbf85…`, round-gate `f890e277…`, proxy-check `a052ddb9…`, claims-check `e9a21b44…`, kimi-census `83016d45…`; every `--selftest` exit 0 with verbatim summary lines — K-R2-1); §7 meta-check anchor pair corrected to `claims-check.mjs:851-852` and `kimi-census.mjs:841-842` — the wave-1 ranges started early / ended short of both `check(...)` lines (K-R2-2); mutation-control census re-checked with the SKILL.md false hits excluded — still no gate ships a kill-rate harness (K-R2-3); cite-check integration group + round-gate `INTERNAL_ERROR` arm stay recorded-not-absorbed, sibling-owned (K-R2-4) | kumitate-shokunin read-only; per gate `node scripts/<gate>.mjs --selftest` + `sha256sum scripts/<gate>.mjs`; `grep -n "every finding kind fired by the suite"` re-run 2026-10-14 (note "Errata (round 2)" block) |
| `knowledge/gates-survey-kagi.md` — round-2 addendum (G-R2-1…6, append-only) | §1 claim-ledger pin corrected: **79301 B / sha256 first16 `93c5827202b9cdec`** — the surveyed 79294/`357fb245` was an intermediate dirty-tree state never committed; substrate moved 09:58:55, kagi's own round-18 `fecee87` (10:05:10) re-pinned `stamps.tsv` (G-R2-1); §9 item 4's last-non-empty-line citation corrected `:53-56` → `:26-28` (G-R2-2); denied verbs 22 → **23** (G-R2-3); re-verified set held: six selftests 16/13/29/34/61/97 = 250, `--falsify` exit 1 `caught=16/18 failed=2` with the same two `SCOPE BREADTH-EXCEEDS` lines, F-1/F-2 standing and `corpus/README.md:43` still unqualified "18/18" (G-R2-4); §8.1 [UNK] discharged — the mid-survey writer was kagi's own in-flight round-18 [INF] (G-R2-5); live verdicts 5/6 + F-2 fix stay sibling-owned recommendations (G-R2-6) | kagi-shokunin read-only @ `fecee87`; `sha256sum`/`stat -c %s`, DENY_RE pipeline → 23, `sed -n` line checks, spot selftests + `--falsify` re-run 2026-10-14 |
| `knowledge/verification-patterns-fleet.md` — round-2 addendum (TAMESHI-R2-4 extension + V-R2-1…4, append-only) | Fourth pattern from game-dev-2d-shokunin's verifier machinery — D0–D10: replays committed bytes (a commit lacking the change IS the finding, r64); mutants/faults are scratch-only runner fixtures; sensitivity = guard-disable in a disposable copy (binary per guard, no kill-rate tally — U8); a detected mutant must survive spoof classification and engine errors never count; opt-in probes proven inert unflagged; verifier writes its own instruments and recomputes from spec; 7-field regression fence vs prior receipts; falsification/failed verification kept first-class (r64 DISAGREE → landed bytes; r69 verifier-seat death recorded); receipts located (lessons-JSON era → in-tree scratch); declared bounds/non-writes — plus U8–U13 and 2 predictions; explicitly single-lane, NOT general (PROVINCE.md); kaidoku census re-measured held (72 files; `verify:` 468 vs `verified-at:` 467, same four mismatched files), w6–w8 AGREE tallies held (3×5/5, 3×5/5, 2×6/6+1×5/5), U1/U2 stay open with U1's first reading = grep-shape artifacts (V-R2-1…4) | game-dev-2d-shokunin read-only @ `9fb50aa9` (LOG/SCORECARD/reports/corpus); census commands in-note "Verification (extension)"; kaidoku/wave re-greps re-run 2026-10-14 |
| `knowledge/mutation-case-kimi-census.md` | Tameshi's first measured kill-rate (round 2, TAMESHI-R2-1): kumitate `kimi-census.mjs`'s 43-case hermetic suite against 10 single-edit mutants — one exact edit per fresh /tmp copy, driver asserts the old string unique, original byte-identical (sha256 before=after `83016d45…`) → **8/10 killed (80 %)**, no inconclusive run, control 43/43 and every mutant still enumerating 43, 7.0 s sweep; survivors D2 (`findings.slice(0,6)`→`(0,5)`: truncation boundary never exercised — max findings in any suite run = 2 vs cap 6, DRIFT asserts prefix-only) and D10 (`FROZEN.K2 25`→`24`: only `frozen.K5` is asserted) — shared class "reported-but-unasserted surfaces"; per-kill failing-case labels (D4 = exactly the 3 root-enum cases, D8 = the 3 fail-closed cases, D1/D3 = 16 each incl. the exact green baseline); protected-arm inventory + measured gaps; errata E1 (author's D7-survivor expectation wrong — the fixtures' modes share floor bits); scope: measures the suite, not substrate drift [I]; U1–U6 | kumitate-shokunin `scripts/kimi-census.mjs` @ `175de6ba` read-only (sha256 `83016d45…`, 43273 B); mutants + per-defect evidence under `/tmp/tameshi-r2-1-work/` only; reproduce spec (10 edits + commands + D2/D10 sensitivity probes) in-note §4 |
| `knowledge/mutation-case-kagi-census.md` — round 3 (TAMESHI-R3-1) | Tameshi's second measured kill-rate, first bash gate: kagi `surface-census.sh`'s 16-case selftest vs 10 single-edit mutants — same method as round 2 (fresh `/tmp` copies, one exact edit each, count==1 gate, kagi tree never written; restore proof sha `275d8294…` before=after, mtime 09:47:15, porcelain clean) → **8/10 killed (80 %)**, no inconclusive run, suite count held `(<n>/16 cases)` on every run, 11.0 s for 11 runs; survivors B5 (deleted exec x-bit arm: **fixture-absent arm** — no case reaches it, so no implementation moves the suite; non-equivalence probe: mutant reports `SURFACE OK … (exec 644)` where pristine reports `SURFACE DIVERGED` exit 1) and B10 (CLEAN-summary `ok=` arg swapped: reported-never-read count, same family as round-2 D10); kill is token-only in B4 (deleted symlink arm keeps exit=1, dies on the `SURFACE LINK` token assert); per-kill failing-case labels (B1 = case 05 undeclared-file, B3 = 3 incl. crosscheck-disagree, B8 = the two exit-2 setup cases); gate choice proven hermetic on this host (fixtures under `mktemp -d`; the 2 verbs cases `skip-case … substrate-absent` — `the-janitor` off PATH, kagi's own round-18 repair, LOG.md:741-744); E1: failing-case *counts* predicted 6/10 (case 04 is a second exit-0 green fixture, kills every green-firing defect); cross-language §4: same headline as JS, narrower kill width (max 3/16 vs 16/43 — per-case fresh fixtures + exit+token asserts vs shared fixtures + exact-line asserts), shared survivor class reported-but-unasserted data, bash-only unreached-arm class; U1–U6 | kagi-shokunin `corpus/surface-census.sh` @ `fecee87` read-only (sha256 `275d8294…53009f`, 44212 B, 886 newlines, 887th line unterminated); mutants + evidence under `/tmp/tameshi-r3-1-work/` only; reproduce spec (10 edits + commands + B5/B10 probes) in-note §7 |
| `knowledge/executor-test-sufficiency.md` — round 3 (TAMESHI-R3-4) | The no-oral-context executor test (SHONEN box 3 evidence): an executor with no tameshi context beyond `SKILL.md` @ `dd2f4dee…3753` reproduced **one killed mutant end-to-end** — D5, killed exactly as Appendix A records (`42/43 FAIL`, singleton failing case `MEMBER_MISSING … presence is gated`), control green 43/43 first try, all 10 manifest strings byte-exact and unique at their cited lines (`--check` → every `count=1`, `CHECK: all unique`), restore pin held; per-step sufficiency verdicts S1–S10: 7× SUFFICIENT, 2× SUFFICIENT (latitude), 1× ADDITIVE-IMPROVISATION (single-mutant `--only` subset is not described — affordance, not repair), 1× NOT EXERCISED (survivor probe — D5 killed), 1× ADAPTED (note format); the SKILL's grammar rule was load-bearing (a red mutant still prints `… 42/43 pass`); contamination statement §1 (read SKILL.md + target only, no corpus/plans/AGENTS); scope honest: ONE mutant of the JS case, not the full sweep [U3–U6]; U6: no independent second lane had re-verified at write time — since closed by the round-3 audit replays (B2 re-ran D5 via the tool, same kill + same mutant sha) | `tameshi-shokunin/SKILL.md` @ `dd2f4dee…3753` (45644 B, 665 lines) + kumitate `kimi-census.mjs` @ `175de6ba` (sha `83016d45…` before=after); executor evidence under `/tmp/tameshi-r3-4-work/evidence/`; reproduce block in-note §8 |

## Quality bar

See `QUALITY.md` (admits only falsifiable, source-cited claims;
rejection kept as evidence of taste).

## Fleet round lessons

| Entry | Admitted / rejected | Evidence |
|---|---|---|
| `lessons/round-1.md` — fleet round-1, distinct from the historical training arc | Admitted: canonical, durable lane assertions; rejected: same-lane promotion authority and broad current cold-read credit from one historical JS mutant. Outside admit/reject review remains open. | `../reports/round-1-calibration.md`; `../LOG.md` fleet round-1 entries |

Fleet round-1 status: **local calibration correction retained; formal
admission blocked**, not a completed training round. The current exact-32
plan is validated but undispatched because existing role aliases do not
realize the operator contract. The lesson's ER-I1 and the audit's
`## Interactive continuation` distinguish inherited claims from fresh
local checks. Full outputs, exits and exact route/receipt prerequisites
are retained under `../.ufo/evidence/fleet-round-1/`; authoritative local
handoff: `../.ufo/continuation/fleet-round-1.md`.


## Coverage map — addendum (fleet round 1, appended 2026-10-19)

Appended, not inserted: the rows above keep their line numbers. Closes
the lagging-index debt (`lessons/round-1.md` MK-4, `QUALITY.md` 7):
before this addendum 13 of 19 notes had no row —
`for f in corpus/knowledge/*.md; do b=${f##*/}; grep -qF "knowledge/$b" corpus/README.md || echo "$b"; done | wc -l` → 13 at `4eb4cf3`.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/arm-class-matrix.md` | JS + bash mutation-case arm-completeness matrix (round 4) | `mutation-case-kimi-census.md`; `mutation-case-kagi-census.md` |
| `knowledge/closeout-r11.md` | the training arc's closeout: service boundary, handoff, carried debts; no new gate measurement | `plans/round-11.plan.md`; `SCORECARD.md`; `LOG.md` |
| `knowledge/fleet-kill-rate-ledger.md` | standing per-gate view: suite size, kill rate, survivor classes, sweep date, pin; stale successor rows open | the six mutation-case notes; S031 |
| `knowledge/fleet-suite-census.md` | static suite-vs-arm census of fleet gates (meta-checks, mutation controls, integration groups); the service offer | kumitate `scripts/`; kagi `corpus/*check*.sh` |
| `knowledge/mutation-case-kagi-checklist.md` | case 5: kagi `checklist-run.sh` 7/15 (47 %), copy-only harness | S036; `service-optin-protocol.md` |
| `knowledge/mutation-case-kumitate-claims.md` | case 6: kumitate `claims-check.mjs` 7/10 (70 %), byte copies only | S037 |
| `knowledge/mutation-case-mado-verify.md` | case 4: mado `mado-verify.sh` 4/10 (40 %), owner opt-in, in-surface vs out-of-surface | S035 |
| `knowledge/mutation-case-tsukuroi-census.md` | case 3: tsukuroi `tsukuroi-census.sh` 6/10 (60 %), cross-author; incident I1 | S034 |
| `knowledge/operator-runbook.md` | operator runbook for the runner, ledger, opt-in, limits, cadence, regression (four-leg lines: ER-R3 open) | S031; ledger; opt-in; limits notes |
| `knowledge/self-hardening-r6.md` | meta-sweep of the runner's own `--regression` comparator; selftest hardened | S031 |
| `knowledge/service-limits.md` | intake refusal table: what the service will not sweep, and why | `fleet-suite-census.md`; `SKILL.md` |
| `knowledge/service-optin-protocol.md` | engagement protocol: request, non-writes, owner responsibility, report shape | `fleet-suite-census.md`; case notes |
| `knowledge/service-standing-state.md` | artifact-boundary table, fleet-visible vs lane-owned; no measurement | `SCORECARD.md`; `LOG.md`; `SKILL.md` |
| `knowledge/mutation-score-semantics.md` — round 1, frontier F1 | verdict vocabulary map tameshi ↔ Stryker ↔ cargo-mutants ↔ mutmut ↔ shmutant; tameshi k/(k+s) vs Stryker detected/valid, equal iff no timeouts; all six recorded cases recomputed (t = 0 → identical rates); NoCoverage candidates left U; "timeout counts as a kill" rejected | S001, S002, S004, S005, S006 |
| `knowledge/witness-scoped-kill-verdict.md` — round 1, frontier F2 | shmutant's witness grammar vs tameshi's guards; pre-registered witness split of js-kimi-census: 8 killed-on-witness / 0 accidental / 2 survived, declaration hashed before the run (blindness partial, recorded) | S006; evidence `../.ufo/evidence/kaika-round-1/witness/` |

## Sources

Where this lane learns: `SOURCES.md` (registry per kaika contract v1 —
tiers, recheck cadence, paths, search log, unopened leads).

## Frontier

Ground not yet held. Zero-hit sweep (non-author ART dossier,
`fleet-ledger/.ufo/waves/kaika-w1/tameshi-art.md:44`, run 2026-10-19 at
`4eb4cf3`): all 12 patterns → `files=0 lines=0`. A ground moves to
`held` only through an admitted `knowledge/` entry with a `source:`
header citing a `mined` `SOURCES.md` row.

| id | ground | candidate sources | status | next falsifiable move (before → after) |
|---|---|---|---|---|
| F1 | external mutation-score semantics + report interop | S001, S002, S004, S005 | held (round 1) — `knowledge/mutation-score-semantics.md` | emit one ledger leg as schema JSON and validate it (validator unavailable this round: U) |
| F2 | witness-scoped kill verdicts / bash mutation tooling | S006 | held (round 1) — `knowledge/witness-scoped-kill-verdict.md` | the same split on a bash leg (surface-census): undefined → k_witness + k_accidental = 8 |
| F3 | determinism precondition, flaky-aware verdicts | S004, S011, S025, S026, S027, S040 | open | one control per sweep (`.ufo/evidence/kaika-round-1/capability-demo/README.md` H2) → N ≥ 3 byte-identical controls, or a named mismatch |
| F4 | golden / snapshot fixture discipline | S013, S014, S015, S016, S017, S045 | open | update paths that write expected values without an explicit flag: unmeasured → counted per surveyed gate |
| F5 | hermetic environment normalization | S015, S016, S028 | open | runner selftest host vs `env -i LANG=C TZ=UTC`: identical (H3, round 1) → the six gate selftests measured the same way |
| F6 | fixture minimization for survivors | S022, S023, S024 | open | B5 probe fixture size: unmeasured → reduced size + kill check |
| F7 | incremental re-sweep granularity | S003, S004, S005, S008, S041 | open | pin-level cadence only → per-leg reuse decisions classified |
| F8 | oracle anchoring as a survivor class | S012 | open | 0 test-oracle lines → one survivor classified against an independently anchored expectation |
| F9 | LLM-era mutant generation + equivalence | S007, S009, S043, S044 | open | no LLM-specific search run yet (U) → bounded pilot with an independent outcome check |
| F10 | PBT generators for gate fixtures | S018, S019, S020, S021 | open | no PBT fixture method → one generator against a named fixture gate |

## Known gaps

- **Provenance headers on the 19 pre-round entries** (`lessons/round-1.md`
  MK-7): 0 of 19 open with `source:`/`verified-at:`/`recheck:` —
  `for f in corpus/knowledge/*.md; do head -5 "$f" | grep -c '^source:'; done | sort | uniq -c` → `19 0` at `4eb4cf3`. Prepending
  would shift every `path:line` cite into them; left as named debt,
  route is an operator call. New entries carry the header (2 of 21 now).
- **Stale ledger successors** — tsukuroi and mado legs read `stale`
  (`knowledge/fleet-kill-rate-ledger.md`); re-sweeps owed (freshness).
- **Operator runbook four-leg lines** (ER-R3) still open.
- **`SKILL.md` status sentences stale** (`lessons/round-1.md` ER-K5):
  `SKILL.md:14-15` and `:133-135` still call full-sweep/bash
  sufficiency unverified; `../reports/round-1-kaika-coldread.md` has
  since measured Appendix A + B. Left unedited so the cold-read stays
  bound to the executed bytes; the next `SKILL.md` edit re-runs it.

## Frontier — status correction (fleet round 1, post-review, appended)

The `## Frontier` table above marks F1 and F2 `held (round 1)`;
superseded here (orchestrator adjudication, 2026-10-19) — both are
**partly held**:

- **F1 — partly held.** Score semantics and the six-case recomputation
  are admitted; report interop is not: no ledger leg was emitted as
  schema JSON or validated (`jsonschema` unavailable), and NoCoverage
  candidates stay U.
- **F2 — partly held.** One JS leg measured (8 on-witness / 0
  accidental); the witness declaration was partly contaminated
  (`knowledge/witness-scoped-kill-verdict.md` E1), and no bash leg was
  measured.

A ground reads `held` only when its next move in the table is
measured.
