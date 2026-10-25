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

## Round 12 — coverage and frontier resolution

| Note / frontier | Lane-asserted scope; outside admission pending | Source / evidence |
|---|---|---|
| `knowledge/repeated-control-precondition.md` / F3 | A standalone exact-tuple repeated-control gate; a clean result is finite sample agreement, not proof of determinism or a flaky-test cure | S004, S026; `tools/repeat-control.py`; `.ufo/evidence/round-12/verification-final.json` |
| `knowledge/witness-scoped-kill-verdict.md` / F2 | Historical source-semantics corrections E2/E3; the existing bash leg's declared-witness study is retained separately, not a new recorded gate | S006; `.ufo/evidence/round-12/BashWitness/summary.json`; `lessons/round-12.md` |

F3's original next move is the repeated-control capability, not the stronger
word “determinism” in its heading. F2 keeps the partial-blindness limitation:
source/spec exposure was inherited, and a before-run hash does not erase it.
F1 remains partly held; the old freshness and provenance-header debts remain
open. The earlier absent-bash sentence at lines 115–118 is a round-1
snapshot, superseded only for the round-12 evidence above.
F2 remains partly held in the broad sense of bash mutation tooling; this
study does not add selector-based execution or certify assertion-level
causality. F3's named finite-sample capability is the claimed advancement,
not a universal determinism guarantee. Neither row changes province Core
by self-attestation.

The newest outside review remains `lessons/round-1-verifier-spotcheck.md`.
Round-12 lane-dispatched review is not its replacement. Full-page box-3
sufficiency is still unearned; historical cold-read receipts apply only to
their pinned SKILL bytes. The append-only round-12 registry adds no
full-page cold-read or promotion credit.

## Round 13 — F7 content disposition and outside-review correction

| Note / frontier | Scope | Source / evidence |
|---|---|---|
| `knowledge/incremental-pin-disposition.md` / F7 | Structured six-leg pinned/HEAD/worktree content observation and the explicit boundary `result_reuse=not_established`; no target gate runs and no new rate | S003, S041, correction S047; `.ufo/evidence/round-13/pin-dispositions.json` |
| Frozen bash provenance correction / calibration | New companion metadata normalizes the exposed declaration's kind without rewriting round-12 evidence; original null stays historical | `lessons/round-13.md`; `.ufo/evidence/round-13/witness-metadata.json`; QUALITY14 |

F7 advances from pin-cadence prose to a bounded machine-readable
disposition method, not a full incremental result cache. Environment,
dependencies, invocation and fixture inputs are not certified by content
identity. The stale-successor **mutation re-sweeps** remain open; a new
pin reading does not discharge them. F1 interop, legacy provenance headers,
runbook corrections and current full-page cold-read/box3 remain debt.
No frontier is moved wholesale to province Core.

The “newest outside review” sentence in the round-12 block is superseded:
`lessons/round-12-verifier-spotcheck.md` is now the latest outside admit/reject
sample and admits bounded C1/C2 of that round. It is not a round-13 sample
or promotion authority. Its lane-routed null-kind defect and brittle planner
citation are corrected in this round's new evidence and named-heading
lesson; operator-owned orchestration defects remain routed to the operator.

Final round-13 evidence is executed, not predicted:
`verification.json`, `producer-oracle-repair.json`, `verification-verdict.json`.
The content observation is changed3/unchanged3/unavailable0 at the recorded
HEADs (`pin-dispositions.json`); the historical two-successor debt now also
includes kimi's changed target (`fleet-kill-rate-ledger.md`, ER-5).
The full F7 per-leg **reuse-decision** frontier remains open; only the
content-disposition prerequisite is acquired. PIT row S048 supersedes
S047's object-specific wording without claiming a new opened source.
Both new registry rows are corrections to the same PIT URL.

## Round 14 — effective evidence, not rewritten history

| Maintained ground | Addition / correction | Evidence |
|---|---|---|
| calibration of retained expectations | Complete twelve-row effective/superseded ledger; the failed raw setup observation remains visible rather than being granted mechanism credit by exit code | `lessons/round-14.md`; `../tools/evidence-disposition.py`; `../.ufo/evidence/round-14/dispositions.json` |
| `knowledge/incremental-pin-disposition.md`, empirical correction8 | Final round13 receipt backlink and S048 object-neutral guidance supersede only the dated pre-integration status; original section6 remains historical | existing mined S003/S048, new S049; prior outside `lessons/round-13-verifier-spotcheck.md` |
| explicit invocation context | Prospective GIT_DIR experiment and runner/manifest mapping receipt; no invented historical injection setup | `../.ufo/evidence/round-14/capture-context.py`; completed runtime evidence is appended to the round14 lesson |

This round does not complete whole-F7 verdict reuse, F1 interop, any successor
mutation sweep, legacy provenance-header repair, runbook repair or current
full-page cold-read/box3. New selftests and a checked context do not substitute
for an independent outside admit/reject sample or promotion.
The previous latest-review statement is superseded: round13's outside closure
is now the newest sample. It admits round13's bounded claims, not round14.

## Round 15 — context classification and standalone verdict boundary

The historical round14 capture script/receipt above remain frozen evidence,
not an active probe recipe. `lessons/round-14-verifier-spotcheck.md` Routed
defects5 correctly classifies persisted-expectation comparisons as a gate;
`lessons/round-15.md` and QUALITY17 record that correction. Maintained
`../tools/context-capture.py` checks retained receipts without executing
their argv or reading sibling trees. Its public isolated selftest and
digest-bound frozen runs are separate evidences, not a new live experiment.

This is same-ground calibration work, not a new uncovered knowledge entry,
whole-F7 result reuse, F1 interop or a successor mutation sweep. Legacy
provenance headers, runbook corrections and current-page cold-read/box3
remain open. The newest outside sample is now the round14 verifier note;
it admits round14's bounded C1, not round15 or promotion.

Effective round15 evidence is
`../.ufo/evidence/round-15/verification-3.json`, measured at
`7650fe4db89f3a706aed63d048ac47e02289cc72`: selftest49/49,
registered frozen0, explicit missing-env1/tamper2/usage64. The earlier two
failed harness receipts remain history; the lesson explains the copied-tool
layout and dropped-regex repairs. S051 enters as own-work support, and no
new `knowledge/` ground or external admission is inferred from this replay.

## Round 16 — seventh recorded case and full-page cold-read

Appended; rows above keep their line numbers. QUALITY 7: the new note gets
its row in the same round.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/mutation-case-kumitate-round-gate.md` | case 7: kumitate `round-gate.mjs` 5/10 (50 %), 10/10 pre-registered predictions held; projected floor interval [26,1059] confirmed at its edge (1059 survives, 1060 killed); guarded `env -i` suite; ledger leg `js-round-gate` (`--regression` cases=7) | S053, S052, S056, S057; `arm-class-matrix.md` §13 |

Superseded readings, dated, not rewritten: rows 47 and 49 above (the arm-class
matrix and the kill-rate ledger) describe six recorded cases; there are seven
since round 16. Row 15's prior box-3 evidence (partial) and the four
"full-page cold-read / box 3 open" sentences at lines 143-146, 160, 190 and 207
are superseded by `.ufo/evidence/round-16/coldread/ledger.json`, the full-page
cold-read ledger (lane assertion, no independent promotion review). No
frontier item moves to Core: the cold-read is calibration evidence, and F8
needs a mutant-side survivor probe tied to an independently anchored
expectation. Round 16 records mutant-side probes, but against SurvivorPrep's
pristine-derived expectations only.

## Round 17 — live-tree re-pin, entry-command monitor, input-keyed cold-read credit

Appended; rows above keep their line numbers. QUALITY 7: the new note gets
its row in the same round.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/input-keyed-coldread-credit.md` | a cold-read credit holds only while every input the read ran against keeps its sha256 as a blob at the measured rev; trace receipts bind executed commands to inputs; a failing read with verified inputs vetoes; red-before on the round-14 bucket (credited at `e69b488`, `input-drift:tools/mutate-and-run.sh` at `09ee1d0`); limits of an open trace | S058, S059, S060, S064; `lessons/round-16-verifier-spotcheck.md` §2, §6 |

Superseded readings, dated, not rewritten: the round-16 block's statement that
the round-16 ledger is "the full-page cold-read ledger" was wrong at `09ee1d0`
on the round-14 bucket (sha-only credit); the round-17 ledger
`.ufo/evidence/round-17/coldread/ledger.json` replaces it under the
input-keyed rule. Line 95's header count ("2 of 21") is stale: at round 17,
6 of 25 knowledge notes open with `source:` (count:
`for f in knowledge/*.md; do head -1 "$f" | grep -q '^source:' && echo; done | wc -l`).
No frontier row moves: F7 stays open (the v2 disposition and the credit rule are
unchanged-input reuse predicates, not per-leg reuse classification).

## Round 18 — eighth recorded case, routed-defect closure

Appended; rows above keep their line numbers. QUALITY 7: each new note gets
its row in the same round.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/mutation-case-kumitate-sources-check.md` | case 8: kumitate `scripts/sources-check.mjs` @ `0acb775`, 5/10 killed, 10/10 pre-registered predictions held, deterministic control; ledger leg `js-sources-check` | S001, S008; `lessons/round-18.md` |
| `knowledge/guard-kill-closure.md` | a guard is covered only when its removal mutant is killed with a green pristine control; jj `HEAD` vs branch-tip anchoring; non-finite JSON refusal; descendant kill after `setsid`; `GIT_*` prefix scrub and pinned-tool migration | S065, S066, S068, S069, S070, S072, S073, S074 |

Superseded readings, dated, not rewritten: the round-16/17 blocks above say
seven recorded cases; there are eight since round 18. The round-17 entry's §5
exit sentence is corrected by its appended erratum (round 18). No frontier row
moves to Core: F3's determinism control is measured for case 8 only
(`.ufo/evidence/round-18/sources-check/control/`, 8 byte-identical runs), not
per surveyed gate.

Corrections appended after round-18 wave 2 (2026-10-20): the round-17 row
above ("trace receipts bind executed commands to inputs") means the receipts
record the inputs a recorded command opened; the rule never binds receipt
argv to the commands a bucket requires, so it is not command coverage
(QUALITY 33; `knowledge/input-keyed-coldread-credit.md` erratum). The
round-18 row's "knowledge/guard-kill-closure.md" also cites S077/S078, the
round-18 correction rows for S068's anchor and S072's teaches.

## Round 19 — explicit metadata corrections and effective receipt provenance

Same-ground calibration repair, not a new coverage-map admission. The two
round-18 notes now carry R18-1/R18-2 errata explicitly naming their stale
`verified-at:` / `source:` lines. The round-18 lesson's R18-3–R18-5 errata
correct five-line arithmetic and distinguish failed raw invocations from
the effective successful receipt. Round-19 exact-revision replays and the
five-item ruler live in `../.ufo/evidence/round-19/`; source S049 was reopened
for the explicit subprocess environment/observed-output distinction.

The newest independent review is `lessons/round-18-verifier-spotcheck.md`.
It admitted round 18's bounded claims and routed these five repairs; it does
not independently admit round 19. Historical input-keyed60/60 at4b7c682
is now backed by an exact-revision receipt. No current round-19 full-page
equivalence, required-command coverage, promotion, guard-survivor closure,
successor mutation sweep or F1–F10 frontier movement is claimed.

No-harm qualification: the first round19 delivered revision21e7932
actually measured49/60, restraint6 under the old ledger; its failed
current-monitor receipt is retained. The maintained round19 selector
`../.ufo/evidence/round-19/coldread/measure.py` reuses the frozen round18
algorithm with a new default ledger and explicitly L1-author source
re-anchoring for changed inputs. It does not retroactively upgrade
historical traces, authenticate external observations, or become an
independent promotion review. See round19 lesson `## No-harm repair`.

## Round 20 — receipt-window calibration on existing ground

Same-ground repair of round19's outside-routed QUALITY20 recurrence, not a
new knowledge entry or frontier move. `lessons/round-20.md` records the six
frozen predicates, the staged instrument identities and receipt-time window
boundary. QUALITY41 grounds the enforcement check in the repeated mistake.
The appended round19 erratum distinguishes each historical instrument SHA
and S049's local/UTC date bases; original evidence remains unchanged.

The latest independent review is now `lessons/round-19-verifier-spotcheck.md`,
which ADMITTED round19 and routed these three items. It is not a round20
admission or promotion authority. Round20's own dispatched reviews remain
advisory. No required-command coverage, blind cold-read, successor mutation
sweep, guard-survivor closure or F1–F10 movement is inferred.

## Round 21 — F5 finite environment differential

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/hermetic-env-differential.md` / F5 | source-headed method entry, S079 mined and S028 reopened; nine explicit pinned surfaces, seven profiles, raw tuple comparison and a clean repeat | `tools/env-diff.py`; `.ufo/evidence/round-21/c2-contract.json`, `f5/receipt-initial.json`; selftest9/9 |

F5's finite method moves to **Core** for the six fleet-ledger gates
(kimi-census, surface-census, tsukuroi-census, mado-verify, checklist-run,
claims-check), the H3 reference runner, and two explicit additions
(round-gate and sources-check). These are the nine files frozen before
dispatch, not a retrospectively chosen denominator.
The distinct six-suite kumitate survey also includes cite-check,
surface-probe and proxy-check: these three are **not measured here**.
This is finite method acquisition, not closure of every possible F5 surface
or proof of universal hermeticity. F3 universal determinism stays open.

Actual initial result: eight raw-tuple invariant, one raw-output-variable
(round-gate random fixture directories), all nine clean controls exit0.
Both repeated round-gate passes are green; raw variation is not flaky
pass/fail. `lessons/round-21.md` retains the gate decisions, provider deaths,
R02 re-anchoring and counter limits. C1's owning selftests discriminate the
eighteen old mutants; command/environment contract pins are distinguished
from reproduced malicious-configuration effects.

## Round22 — callback-authoritative accounting

| Entry | Ground | Evidence |
|---|---|---|
| `knowledge/callback-authoritative-accounting.md` | same-ground calibration repair, not a new frontier crossing | minedS082; `tools/wave-accounting.py`; frozen round22 bundle and expected digest |

Separate the eight synthetic rejection predicates from the actual146-seat
round21 denominator and the two historical partial-report false positives.
No report is deleted; callback-source integrity is not provider authentication.
All existing frontier statuses and independent promotion limits stay unchanged.

## Round23 — required-command receipt binding

| Entry | Ground | Evidence |
|---|---|---|
| `knowledge/required-command-binding.md` | same-ground calibration; explicit finite registry requirements, not full-page closure | minedS083; `tools/command-binding.py`; `.ufo/evidence/round-23/requirements.json` and frozen ten-case ruler |

The registry requirement compiler preserves exact argv/expect and its
source revision/digest. New replay observations retain full streams and
actual clone cwd; historical missing row metadata is never retrofilled.
Trusted bundle consistency is not producer/provider authentication.
No F1–F10 status changes, independent cold-read or promotion credit.

## Round24 — command-binding hardening

| Entry | Ground | Evidence |
|---|---|---|
| `knowledge/replay-projection-hardening.md` | same-ground calibration; routed round23 hardening gaps as falsifiable predicates | minedS084, S085; `tools/registry-replay.py`; `.ufo/evidence/round-24/{contract,measure}.py/json` |

No F1–F10 status changes, independent cold-read or promotion credit.

## Round 25 — F1 report interop, routed-item dispositions

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/mte-report-interop.md` / F1 | source-headed entry citing mined S086 and S087 (new) with S001 and S002; the tameshi-to-report mapping, what the official schema and metrics library check, the INCONCLUSIVE convention, ledger rounding, and an export decision table | `tools/mte-interop.py`; vendored `tools/vendor/*.tgz`; `.ufo/evidence/round-25/` |

**F1 status correction (supersedes lines 78 and 111–114 for the report-interop
half only).** Report interop is now held for the eight recorded ledger legs:
each leg is emitted as a mutation-testing-elements report that the official
3.9.0 schema accepts, and the official 3.9.0 metrics library reproduces its
killed, survived, invalid and total counts and every per-defect status in the
runner's committed tables. Score equality is a sanity check that holds by
construction. The `jsonschema` validator that round 1 lacked now runs through
`uv run --with jsonschema==4.25.1`. **F1b, open:** NoCoverage classification
of the 35 recorded survivors (no coverage data is recorded, so
`mutationScoreBasedOnCoveredCode` is not claimed); Stryker's own mutators and
other report formats are not covered.

C1 is same-ground calibration (record repair of three round-23 routed items),
not new coverage. No other F-row changes, no independent cold-read or
promotion credit.

## Round 26 — ninth recorded case, round-25 record repair

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/mutation-case-kumitate-cite-check.md` / Core (recorded legs) | source-headed entry citing mined S088 (the pinned gate) and S089 (Stryker on equivalent mutants), new this round; ninth ledger leg `js-cite-check`, 5/10 killed on the 62-case hermetic group, 10/10 verdict predictions, four survivors with off-suite witnesses and one equivalent mutant | `.ufo/evidence/round-26/cite-check/`; `.ufo/waves/round-26/w1/Probe*.md`, `CriticEquivalence.md` |

Coverage map: the recorded legs are nine; `tools/mte-interop.py` judges all
nine (line 386 above reads nine from round 26 on). The kill-rate ledger's
cite-check cells (`knowledge/fleet-kill-rate-ledger.md`: a four-defect probe,
1/4, and a queue row "probe only") are superseded by this full sweep; the
ledger file itself is not edited this round.

No F-row changes. F3 stays open (one control per sweep). F1 stays held and
F1b open: the emitted reports still name a target by basename with no lane or
revision pin (routed item 4, open). C2 is a record repair of the round-25
spot-check routed items 1–3, not new coverage.

## Round 27 — frontier F8, oracle-anchored survivor classification

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/oracle-anchored-survivors.md` / F8 | source-headed entry citing S012 (re-opened and mined this round) and S090, S091 (new); the four round-26 cite-check hole survivors re-judged against expectations fixed outside the mutated code: 4 anchored holes, one of them held by convention only | `.ufo/evidence/round-27/f8/` (anchors committed before the run, receipt bound to probe and anchor digests); counter `.ufo/evidence/round-27/c2-measure.py` |

F8 moves from open to **partly held**: its next move (one survivor
classified against an independently anchored expectation) is measured, on
one gate at one pin. Hole calls on the other eight recorded legs stay
pristine-differential until anchored. Line 85's F8 row reads "open"; this
section supersedes its status cell, and lines 234-238 above (round 16,
pristine-derived expectations only) describe the state before this round.

## Round 29 — F8 wording correction, F6 pre-registration

F8 correction (round-27 spot-check routed item 4): the round-27 section
above says the F8 next move "is measured" against "an independently
anchored expectation". The entry `knowledge/oracle-anchored-survivors.md`
bounds that to 3 of the 4 survivors anchored in the gate's own header
contract and 1 held by convention only. F8 stays partly held on that
bound.

F6 (fixture minimization for survivors) is pre-registered for round 29,
before any data: survivor B5 of the kagi surface-census leg (exec x-bit arm
deleted), probe fixture reduced by delta debugging (S024) to a fixture that
still kills B5 and is 1-minimal at line and file granularity. Counter
`.ufo/evidence/round-29/c2-measure.py`; frozen predicate and controls in
`.ufo/evidence/round-29/contract.json`. The outcome is recorded in
`corpus/lessons/round-29.md` and in the entry the counter names, whether or
not the target is met; this section claims no status change for F6.

## Round 30 — regression tally completeness (exploratory), S092–S094

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/regression-tally-completeness.md` | Core ground (the lane's own runner, `tools/mutate-and-run.sh --regression`), not a frontier move. The tally refuses as SETUP when the counted leg statuses do not add up to the case count; `--selftest` runs the extracted tally block under 23 fixed status vectors and a guard stress case (97 → 106 cases). Claim C1 is exploratory: a static-model control met the frozen counter v4 before data | S087 (re-opened), S093, S094; `.ufo/evidence/round-30/contract-amendment-4.json` |
| S092 supersedes S059 | Anchor re-pin only. The markdown digest changed and the quoted known issue still stands | `.ufo/evidence/round-30/sources/S059-bazel-remote-caching.md` |

No frontier row changes status this round (F1–F10 as above).

## Round 31 — executable self-assessment rows (calibration), S055 re-opened, S095–S096

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/executable-self-assessment.md` | New lane ground (seat ScoutFrontier: not F1–F10, not held core): a standing SCORECARD capability or score row is a claim checked by running the row's own command at the same revision and comparing the stated values; a stale row is corrected by an appended, revision-named statement, never in place. The executable-example sources motivate this local inference; a matching tally is not full behavioral proof. Calibration claim C1 measures it over the 12 frozen rows. | S055, S095, S096; `.ufo/evidence/round-31/contract.json`; `.ufo/evidence/round-31/c1-measure.py`; `.ufo/evidence/round-31/before/c1-at-base.stdout` |

No frontier row changes status this round (F1–F10 as above).

## Round 32 — runner tally audit (operability, capability acquisition), S097 and S099, S094 re-opened

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/runner-tally-audit.md` | Core ground (the lane's own runner, `tools/mutate-and-run.sh --regression` and its tally selftest harness), not a frontier move (seat ScoutFrontier). A new versioned tool, `tools/tally-audit.py`, audits the runner without editing it: per-leg presence of the tally loop, the tally block against an oracle over every status 0–255 with overcount/undercount stress, and the runner's own harness against a panel of faulty tally blocks. It closes the per-leg item and the eight MutateHead survivors routed since round 30, while the runner stays byte-identical. The measured result is in SCORECARD.md's round-32 block | S097, S099, S094 (re-opened); `.ufo/evidence/round-32/contract.json`, `.ufo/evidence/round-32/v2/` |

No frontier row changes status this round (F1–F10 as above).

## Round 35 — index repair: three entries the coverage map never carried

Appended 2026-10-23 (round 35, C2). The three rows below close the lagging-index debt the round-35
C2 counter found (QUALITY.md criterion 7): every `corpus/knowledge/*.md` entry now has a row here.

| Entry / ground | Admission and exact scope | Evidence |
|---|---|---|
| `knowledge/runner-tally-audit-v2.md` | Core ground, landed round 33: the four held-out classes that defeated `tools/tally-audit.py` and the v2 answers (runtime vector sweep, every status at every leg, dataflow-identified tally loop, extraction tolerance). Its own header trio already named S097 + S099; this row closes the index gap only | S097, S099; `tools/tally-audit-v2.py`; `.ufo/evidence/round-33/` |
| `knowledge/survivor-fixture-minimization.md` | Frontier F6 attempt (round 29), honest stop: the frozen target was not reached; the note records the survivor-B5 finding and the delta-debugging reading of S024. Index gap only — no verdict changes | S024; `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html` |
| `knowledge/witness-equivalence-rule.md` | Core ground, landed round 34: the set-aware witness rule for sealed held-out copies (kill/accept × head/vector branches), the rule the round-34 C1 deciding run verified. Header trio added the same round (C2 m1) | S097, S101; `.ufo/evidence/round-33/c1/c1-measure.py` |

No frontier row changes status this round (F1–F10 as above).

## Round 38 — F4 golden comparison: the three-outcome verdict (round 38)

| `knowledge/golden-comparison-verdict.md` | F4 golden / snapshot fixture discipline, landed round 38: a golden comparison has three outcomes (match / differ / error), POSIX `diff` exit 0/1/>1, and the expected-value write path sits behind an explicit update flag. Admitted from the corpus-expansion-1 package for this lane and re-grounded by this round on S105 and S106. Indexed under the round-38 coverage move below. |

**Coverage-map move (F4).** Before: F4 read "golden / snapshot fixture discipline — open;
update paths that write expected values without an explicit flag: unmeasured". After: F4
partly held — the *verdict lattice* is now held (three outcomes, with the error class
separated from the difference class) and the *write-path census* over the surveyed gates is
still unmeasured and stays the next falsifiable move. Sources: S105 (spec, tier A), S106
(code, tier A). The lane's own fixtures were not converted to golden comparisons this round,
and no claim is made about any sibling gate.

## Round 39 — F4 write-path census (round 39)

| `knowledge/r8-golden-update-flag.md` | F4 explicit update flag, re-grounded this round on S107 (upstream golden_tests.md at 4d3a89c9) and S108 (the zh-cn page). The entry states the flag rule. It does not state the census count. |

**Coverage-map move (F4 census).** The round-38 section left the write-path census unmeasured. This round counted the lane's own 21 gate tools under a frozen pattern: `live_write_sites=99`, `live_unflagged=0`, with planted controls that a constant 0 and a constant 1 both fail, and a fixture that writes `case.expected` only when the update flag is set. The 0 is the pattern's count, not a claim that no unflagged write exists: seats found `expected.json` via `.write_bytes` and an `os.replace` path the pattern does not see. Those limits stay open. Sources: S107 (tier A), S108 (tier B).
