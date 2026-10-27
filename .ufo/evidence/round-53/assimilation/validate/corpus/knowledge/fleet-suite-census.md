# Fleet suite census — all six gates, suite-vs-arm completeness (TAMESHI round 5, T5-4)

Census date 2026-10-14 · Lane: `tameshi-shokunin` · Assignment T5-4 (round-5
dispatch), quoted: "survey ALL SIX fleet gates' suite-vs-arm completeness in one
note (static, the matrix vocabulary): which gates have meta-checks, mutation
controls, integration groups; the fleet-wide kill-rate-harness gap as tameshi's
standing service offer."

Provenance: this note extends the round-4 static projection (`arm-class-matrix.md`
§13 — one gate) to all six gates, and it is the *census half* of the round-4
carry list where that list touches the fleet: matrix U4 ("no third gate/
language … the band interiors", `arm-class-matrix.md:267-268`)
and the round-4 record's "§13 projection awaits its measured sweep"
(`plans/round-4-record-draft.md:153`). The measurement half stays open (§8 U4).

**Scope decision (O).** "The six gates" = `kumitate-shokunin/scripts/*.mjs` —
cite-check, surface-probe, round-gate, proxy-check, claims-check, kimi-census —
the set `PROVINCE.md:8-9` calls "six gates with selftest suites + mutation
controls" and the set of the wave-1 survey (`gates-survey-kumitate.md`). The
three asked columns re-use that survey's §7 vocabulary; the matrix vocabulary is
`arm-class-matrix.md` §0 (classes A–G) and §9 (admission statuses). Kagi's six
gates are the fleet's *second* six-gate family; they keep their own survey note
(`gates-survey-kagi.md`) and appear here only as cross-reference (§4–§6) — not
re-surveyed. A reader who meant kagi's six should transfer these column
headings; §6 names what moves and what does not.

**Static-ness (O).** Every cell below is a read of pinned bytes (`sha256sum`,
`wc -l`, `grep -n`, `sed -n`). The census's only executions are one `--selftest`
"pin pulse" per gate — the suites' own hermetic runs (fixtures under `mkdtemp`
with `finally` cleanup, `gates-survey-kumitate.md:28-31`), taken because
executed counters, never source greps, are the honest case counts
(`gates-survey-kumitate.md:316-318`; same rule for kagi,
`gates-survey-kagi.md:58-64`). **No mutants were cut; no gate mode other than
`--selftest` was executed; `cite-check --integrations` was not run.** Cells on
surfaces no case exercises are labelled **projection** — a static reading in
§13's discipline: a probe candidate, never an admission
(`arm-class-matrix.md:298-309`).

Substrates read-only: `kumitate-shokunin` (`git status --porcelain` empty before
and after; HEAD `175de6b`), `kagi-shokunin` (two pins only, §6), tameshi's own
tool/SKILL pins (§5). Write scope: **this file only** — LOG.md / SCORECARD /
README appends are left to the lane record (dispatch write-scope precedent,
`verification-patterns-fleet.md:5-8`). Scratch: `/tmp/w5-tameshi-census/`.
Anchors: **O** observation · **I** inference · **U** unknown.

## 0. Headline

- O: all six suites green on the pinned bytes today, exit 0 each —
  **62 / 42 / 60 / 102 / 39 / 43** executed cases (cite-check / surface-probe /
  round-gate / proxy-check / claims-check / kimi-census) = 348 cases; kumitate
  tree porcelain-empty after (§1).
- O: **5 of 6 gates carry a completeness meta-check** over their declared
  finding kinds — surface-probe, round-gate, proxy-check, claims-check,
  kimi-census; **cite-check carries none** (`gates-survey-kumitate.md:283-286`,
  re-read today §2.2).
- O: **mutation controls: 1 of 6.** Cite-check's mutation copy is the only
  in-suite mutation-shaped case and it is integration-gated
  (`cite-check.mjs:2372-2383`; skipped under `--selftest`, `:2354-2356`).
  Claims-check's is deliberately externalized, not a case
  (`claims-check.mjs:819-822`). The other four gates: nothing (§2.3).
- O: **integration groups: exactly 1 of 6.** `cite-check --integrations`
  (`cite-check.mjs:73-85`), 9 `checkI(` sites (`:2363-2446`); never executed by
  this census, and skipped by `--selftest` by design.
- O: **0 of 6 gates ships a kill-rate harness or fault injection against its own
  code** (re-swept today: `mutant|mutation|kill` returns hits in two files
  only, both explained; `fault-inject|sabotage|kill-rate` → 0 in all six; §4).
- O: fleet-wide, exactly **two kill-rate tables exist, both cut by tameshi
  outside the gates**: kimi-census 8/10 (r2) and kagi surface-census 8/10 (r3);
  the matrix ledger is 16 killed / 4 survived / 0 inconclusive
  (`arm-class-matrix.md:30-31`). Five of these six gates — and five of kagi's
  six — remain unmeasured. §5 is tameshi's standing offer to close them.

## 1. The six gates, pinned + pulse

### 1.1 Identity and pins (all 2026-10-14; `scripts/` = `kumitate-shokunin/scripts/`)

| Gate | Lines | sha256 (first 16) | Executed cases (pulse) | Verdict line (verbatim, last of pulse) |
|---|---|---|---|---|
| cite-check | 2537 | `40573448330f52fb` | 62 | `62/62 cases passed (hermetic)` / `VERDICT: PASS` |
| surface-probe | 1506 | `148cbf85ce4c7682` | 42 | `42/42 cases passed` / `VERDICT: PASS` |
| round-gate | 1511 | `f890e277af83a78f` | 60 | `ROUND_GATE_SELFTEST: 60/60 pass` / `VERDICT: PASS` |
| proxy-check | 2354 | `a052ddb97a0b6f84` | 102 | `PROXY_SELFTEST: 102/102 pass` / `VERDICT: PASS` |
| claims-check | 925 | `e9a21b441f1216bf` | 39 | `CLAIMS_SELFTEST: 39/39 pass` / `VERDICT: PASS` |
| kimi-census | 896 | `83016d45049b009a` | 43 | `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS` |

Pins are byte-identical to the ones recorded in the round-2 errata
(`gates-survey-kumitate.md:350-356`) and re-verified at round 4
(`verification-patterns-fleet.md:246-249`); kumitate HEAD is still `175de6b`
(round-4 record `f890e277…` §13 anchor, `arm-class-matrix.md:301`).

### 1.2 Pulse method (O)

`cd /tmp/w5-tameshi-census && node <gate>.mjs --selftest` for each of the six;
exit codes 0/0/0/0/0/0; wall time ~9.3 s for the six; `git -C kumitate-shokunin
status --porcelain` empty before and after (no write of any kind reached the
sibling tree). The pulse's only purpose here is to re-quote the executed
counters on the pinned bytes; it is not a measurement of any arm.

## 2. Census I — the three asked columns

### 2.1 The columns, one row per gate

| Gate | Meta-checks (declared-kind/arm completeness) | Mutation control | Integration group |
|---|---|---|---|
| cite-check | **none** | 1 — mutation copy, integration-gated (`:2372-2383`), skipped under `--selftest` (`:2354-2356`) | 1 — `--integrations` (`:73-85`); 9 `checkI(` sites (`:2363-2446`) |
| surface-probe | 1 — finding codes (`:1432-1435`); no fail-closed coverage | none | none |
| round-gate | 1 — finding kinds (`:1487-1493`); structurally blind to fail-closed tokens (§3.2) | none | none |
| proxy-check | 2 — kinds (`:2269-2271`) + fail-closed arms (`:2273-2276`) | none (substitutes: determinism `:1392-1395`, literal hand-arithmetic `:1368`) | none |
| claims-check | 2 — kinds (`:851`) + arms (`:852`; setup `:846-850`) | none in-suite; externalized env-poison probe (comment `:819-822`); a kind-blind-mutant detector case (`:827`) | none |
| kimi-census | 2 — kinds (`:841`) + arms (`:842`) | none | none |

### 2.2 Meta-check notes (O; anchors re-read today)

- The five meta-checks are the *"every declared … fires in at least one
  fixture"* family: surface-probe `check('every declared finding code fires in
  at least one fixture', …)` (`:1432-1435`, over `SUITE_CODES` `:217-218`,
  pulse detail `21 codes observed`); round-gate same name over `FINDING_KINDS`
  `:171-176` (14 kinds; pulse `14 kinds observed`); proxy-check both kinds and
  arms (`:2269-2276`; pulse `12 arms observed`); claims-check and kimi-census
  via `missingKinds`/`missingArms` filters (`claims-check.mjs:846-852`,
  `kimi-census.mjs:836-842`).
- Cite-check has **no** filter of this shape: `grep -inE "observed|every .*
  fires" cite-check.mjs` returns one prose hit (`:394`) and nothing else
  (re-check of the round-1 finding, `gates-survey-kumitate.md:62-64`).
- (I, standing round-1 reading): these checks prove each branch is *reached*,
  not that a wrong implementation would be *caught* — arm-coverage detectors,
  not mutation controls (`gates-survey-kumitate.md:308-311`). Claims-check's
  own case name states the local gap: "kind-blind mutants fail here" (`:827`).
- The fail-closed arm half is meta-checked in exactly 3 of 6 (proxy, claims,
  kimi-census). Round-gate's meta-check cannot see its fail-closed tokens by
  construction — fail-closed output never reaches `parseFindings`
  (`arm-class-matrix.md:396-402`).

### 2.3 Mutation-control notes (O; sweep re-run today)

- Command (K-R2-3 method, `gates-survey-kumitate.md:369-375`): per gate,
  `grep -inE "mutant|mutation|kill" <g>.mjs | grep -viE "skill"`. Result:
  cite-check hits at `:78` (header prose), `:2372-2383` (the mutation copy and
  its detail line); claims-check hits at `:827` (the detector case name);
  surface-probe, round-gate, proxy-check, kimi-census → nothing.
- Extra sweep for the same idea under other names: `grep -icE
  "fault.?inject|sabotage|kill.?rate"` → 0 in all six.
- The claims-check mutation control is a *comment*, not a case: "the
  acceptance run proves it from outside by poisoning the env (`UFO_SRC=
  /nonexistent … --selftest` → PASS). A case that re-entered `--selftest` here
  would recurse, so it is deliberately absent." (`:819-822`). It is a
  hermeticity probe, not a defect-detection harness.
- (I): the mutation-copy case in cite-check is the fleet's only *in-repo,
  in-suite* mutation-shaped artifact; its reach (integration group) is exactly
  the group a hermetic sweep cannot execute (§2.4).

### 2.4 Integration-group notes (O)

- Cite-check declares three group states: `--selftest` (hermetic only),
  `--integrations` alone, both (`cite-check.mjs:73-85`; "MUST PASS in any repo
  state" `:75`). The integration group "Run[s] only by `--integrations`"
  (`:78-80`), and under `--selftest` the mutation copy's group is recorded as a
  declared, counted skip (`:2354-2356`).
- The other five gates have **no integration group**: `grep -icE "integrat"`
  → 0 for surface-probe, proxy-check, claims-check, kimi-census; round-gate's
  4 hits are prose about the integrator role, not a group (`:13`, `:18`,
  `:39`, `:105`).
- U (round-1 carried, still open): the integration group was never executed by
  tameshi (it needs the live tree); its case count and pass state are
  unmeasured (`gates-survey-kumitate.md:322-325`, K-R2-4 `:377-382`).

## 3. Census II — matrix vocabulary, gate × class

Cells are the *static* state of each gate's suite against the arm classes of
`arm-class-matrix.md` §0. "Projection" = (I) reading of an unexercised surface
(§13 discipline); measured instances are named with their source note. No cell
is a new measurement.

### 3.1 A · B · C (verdict paths, fail-closed arms, counts)

| Gate | A — verdict paths (pin style) | B — fail-closed arms | C — counts |
|---|---|---|---|
| cite-check | substring: `text.includes('VERDICT: …')` + `'CITE_CHECK:'` + JSON twin (`:1956-1960`); no line-weight above substring | no token enum; one CLI arm asserted (`--src` absent, exit 2 + stderr, `:2334-2343`, pulse-observed pass); empty-scan `return 2` mapping uncovered (I, §3.4) | `byClass` JSON-string equality (`:1958-1960`); summary `n/m cases passed (group)` (`:2494`) |
| surface-probe | substring: checklist ballast `text.includes('CHECKLIST: 2/2 pass')` (`:1369`); conformance verdict via object checks (`:1024`) | no token enum — fail-closed reasons are assembled strings (`:437-438`, `:454-455`, `:464-465`, `:496`); fixtures assert `totals.failClosed !== null` (`:1031-1057`) | counts read inside summary substrings; summary `${n}/${m} cases passed` (`:1444`) |
| round-gate | **full-line anchored regex** with numeric capture (`:863-868`); fail-closed token-only (`:1188`, `:1193`…) | 7 tokens in prose (`:115-117`) over 10 call sites (`:460`, `:471`, `:488`, `:527`, `:531`, `:536`, `:644`, `:647`, `:652`, `:683`); 6/7 hand-asserted; meta-check blind (§2.2) | field reads off the parsed line (`checks === 10 …`, `:878-883`); summary shape+equality (`:1399-1400`) |
| proxy-check | **full-line literal equality** (`:1368`); fail-closed regex token (`:1283`); nested summary equality (`:2261-2263`) | 12 tokens (`:386-391`), all fired; meta-check `:2273-2276`; `INTERNAL_ERROR` fallback (`:1044`, `:1048`, `:2351`) asserted by no case (O: grep, §3.4) | literals with hand arithmetic (`:1368`); determinism case (`:1392-1395`) |
| claims-check | literal equality `GREEN_MATCH` (`:756`) + second literal with row/verdict agreement (`:827-835`); fail-closed substring (`:745`) | 5 tokens (`:117-120`), loop-built cases (`:736-752`), `--src` detail (`:776-779`); meta-check `:851-852` | literal counts inside both literals; row-vs-verdict agreement assert (`:833-835`) |
| kimi-census | exact CLEAN equality (`:511-514`); DRIFT prefix + kind + `members=` (`:498-499`); fail-closed `startsWith` (`:777-779`) | 1 token (`:148`), 3 cases (`:774-803`); meta-check `:841-842` | exact counts in the CLEAN line (`members=49 checked=49 chain=3 info=4`); `--json` agreement (`:531-538`) |

### 3.2 D · E · F · G (unasserted surfaces, unreached arms, coordinated edits, predicates)

| Gate | D — reported-but-unasserted | E — unreached arms | F — coordinated edits | G — behavior predicates |
|---|---|---|---|---|
| cite-check | not enumerated here; the empty-scan stderr text and report fields above the asserted set are candidates (I; §8 U7) | the empty-scan exit-2 *mapping* (`:2527-2533`): its trigger is asserted as an in-process condition (`:1964-1970`), the CLI `return 2` by no case (I, round-1 :77-81) | U (U1) | repair-regression cases assert before/after token resolution (round-1 §8.2, `:68`) |
| surface-probe | fail-closed reason strings: `totals.failClosed` is compared `!== null`, never to a token value (I) | no enum to enumerate (E is unenumerable statically, not provably empty) | U (U1) | fixtures assert failClosed presence and checklist-mode shapes (`:1408-1411`) |
| round-gate | §13.5 list (projection): FAIL-CLOSED detail tails + stderr diagnostic `:615`; selftest counts one-sided `:1489-1492`; `durationMs` `:1263`; JSON `citations` fields; unpinned text details | §13.6 list (projection): `INTERNAL_ERROR` `:683`; tracked `REPORTS_DIR_MISSING` site `:527`; main-repo `UPSTREAM_MISSING` site `:488`; env/usage branches; `UFO_SRC` set-value branch | §13.7 (projection): prose inventories parsed by nothing; site swaps invisible | §13.8 (projection): densest family; pinned both directions (round-name regex, plan window, hermeticity) |
| proxy-check | not enumerated; per-token case counts and detail strings are read at kind level only (I) | `INTERNAL_ERROR` fallback paths (`:1044`/`:1048`/`:2351`) — the declared-kind meta-check cannot see the undeclared-kind net (I) | U (U1) | arithmetic and determinism predicates (`:1368`, `:1392-1395`) |
| claims-check | not enumerated; the one detector case (`:827`) is the only guard on row-vs-verdict surfaces (I) | none identified statically (5/5 arms + kinds meta-checked) | U (U1) | row/verdict agreement predicate (`:833-835`) |
| kimi-census | **measured instances: D2** (DRIFT tail, cap 6 vs reached 2), **D10** (frozen block; only `frozen.K5 === 3` asserted `:526`) — `mutation-case-kimi-census.md`, killer table r2 | none measured (D4/D5 reached and killed, `arm-class-matrix.md:176-179`) | U (U1) | predicates measured killed (D3/D9, r2) |

### 3.3 Fail-closed arm inventory (the B column, detailed)

| Gate | Declared tokens | Declared at | Asserted by cases | Completeness meta-check | Static gap (I, projection) |
|---|---|---|---|---|---|
| cite-check | none (no enum) | CLI arms in `main()` `:2517-2533` | `--src` absent arm `:2334-2343` (observed in pulse) | none | empty-scan exit-2 mapping (`:2527-2533`) unexercised; condition-only case `:1964-1970` |
| surface-probe | none (free-text) | `:437-438` unreachable, `:454-455` unparsable, `:464-465` foreign kind, `:496` zero checks | presence asserts only `:1031-1057`; CLI arm case `:1341-1345` | none | reason strings cannot be arm-covered by construction |
| round-gate | 7 (`:115-117`) | emission `:596-617` (def `:596`) | 6/7 (fcA–fcF, rt3, rt5; §13.3) | none (blind, §2.2) | `INTERNAL_ERROR` `:683`; 2 uncovered call-site species (§13.3) |
| proxy-check | 12 (`:386-391`) | `failClosed` `:989` (token print) | meta-check fires all 12 (`:2273-2276`; pulse `12 arms observed`) | **yes** | undeclared-kind net `INTERNAL_ERROR` (`:1044`/`:1048`/`:2351`) not asserted |
| claims-check | 5 (`:117-120`) | `CLAIMS: FAIL-CLOSED (token)` `:449` | all 5 via loop `:736-752`; `--src` detail `:776-779` | **yes** (`:852`) | none static |
| kimi-census | 1 (`:148`) | `KIMI_CENSUS: FAIL-CLOSED (token)` `:393` | 3 cases (`:774-803`) | **yes** (`:842`) | none static |

### 3.4 Verdict-line exactness tiers (the A column, detailed; O)

(a) full-line literal equality — proxy-check `:1368`, claims-check `:756` +
`:827-835`, kimi-census `:511-514` (CLEAN only); (b) anchored regex with
numeric field capture — round-gate `:863-868` (tightest of the six); (c)
`startsWith` stem — kimi-census `:498` (DRIFT), `:777` (fail-closed); (d)
substring — cite-check `:1956-1960`, surface-probe `:1369`, claims-check `:745`,
round-gate fail-closed `:1188`. Nested self-checks of the summary shape exist in
round-gate `:1399-1400` and proxy-check `:2261-2263`. (I): tier (d) leaves the
verdict line's remainder unasserted by construction — the measured D2/B10
survivors of the two worked cases live in exactly that remainder
(`arm-class-matrix.md:75-101`); kimi-census tier (a) applies to CLEAN only.

## 4. The fleet-wide kill-rate-harness gap

- O: **no gate of the six ships a kill-rate harness or fault injection against
  its own code** — the sweep and its narrowing (§2.3), plus the extra terms
  (`fault-inject|sabotage|kill-rate` → 0/6).
- O: the fleet's other mutation-shaped artifacts, none of them a gate-harness:
  cite-check's integration-gated mutation copy (§2.3); claims-check's
  externalized env-poison probe (`:819-822`); kagi `scope-gate.sh --falsify`
  ("mutate shipped data in scratch", `scope-gate.sh:68`, mode `:110`) — kagi's
  own self-attack, 18 mutations, measured **16/18** on this host
  (`gates-survey-kagi.md:259-322`, held `:582-593`); game-dev-2d's
  `--probe-failing`/`--fault-injection` plus disposable guard-disable
  sabotage — binary per guard, "no survived/killed tally was found (U8)"
  (`verification-patterns-fleet.md:131-137`, `:189`).
- O: exactly **two kill-rate tables exist fleet-wide**, both cut by tameshi on
  `/tmp` copies, both 8/10: kimi-census (r2, `mutation-case-kimi-census.md`)
  and kagi surface-census (r3, `mutation-case-kagi-census.md`); the arm-class
  matrix re-cut both (16/4/0, `arm-class-matrix.md:30-45`), and the tool
  reproduces both (`--regression`, r4).
- I (the gap, stated plainly): for **five of these six gates** and five of
  kagi's six, the answer to "would this suite catch a single-edit regression in
  its own gate code?" is *unknown*. The meta-checks and coverage numbers above
  (14/14 kinds, 12/12 arms, 5/5 arms, 1/1 arm, 21/21 codes) are *reach*
  coverage; they do not measure detection (§2.2; round-1 I `:308-311`;
  claims-check's own case name `:827` is the local admission that a
  kind-blind mutant can pass an arm check).
- U: the 50 % band interior (between the two 80 % measurements and a
  hypothetical floor) is still unmeasured anywhere (§8 U4).

## 5. Tameshi's standing service offer

**The instrument (pinned 2026-10-14):** `tools/mutate-and-run.sh`
sha256 `597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b`,
1001 lines (r4-2) — inject→run→restore runner: spec v1 (one exact-text edit
per defect; `@old` must occur exactly once, asserted before any suite run;
no-op edit refused; escapes allowlisted), pinned pristine + fresh byte-copy
mutants, green-control gate first, per-defect `KILLED`/`SURVIVED`/
`INCONCLUSIVE` (timeout 124; 126/127 not runnable), byte-identity restore proof
(`MUTATE_RESTORE: OK|DRIFT`), evidence workdir, exit map 0/1/2/64; hermetic
selftest **37/37**; `--regression` re-runs the two recorded cases as the
tool's own kill-rate regression gate (round-4 measured:
`REGRESSION: PASS (cases=2 passed=2 …)`, both cases `match=10/10`,
`kill-rate=80%`, flips=0).
**The method (pinned):** `SKILL.md` sha256
`dd2f4dee9df7a422fe44da6709c35f472becf6b39ad7f37818e9114d512c3753`, 665 lines
— the 10-step sweep recipe, defect-class catalog with per-class JS *and* bash
evidence columns, restore-discipline checklist, and complete reproduce
appendices for both worked cases.

**The offer (standing; no current commitment):** any lane may ask tameshi to
run a sweep on one of its gates. What a sweep needs from the owner: a pinned
revision (sha256) and a hermetic suite invocable on a copy (`--selftest`-like);
what it returns: a kill-rate table, per-defect verdicts with failing-case
labels, survivor non-equivalence evidence, and a restore proof — as a corpus
note plus a recommendation; absorption stays with the gate's owner
(`PROVINCE.md:16-18`: tameshi never edits a sibling's gate).

Queue (projection, ordered by expected yield — most static protection last):

| Gate | Static state | Why probe it | Sweep prerequisite |
|---|---|---|---|
| cite-check | 62 hermetic cases; **no** meta-check; substring verdict asserts; 1 mutation copy in the *integration* group | everywhere else self-checks at least its declared arms; also the suite with an unexecuted group | hermetic 62-case run on a copy; the integration group stays a declared skip in a hermetic sweep |
| surface-probe | 42 cases; arm meta-check for codes only; no token enum | fail-closed reasons unreachable by the suite's own coverage check; a free-text family with no assert shape | hermetic |
| round-gate | 60 cases; kinds meta-check; 1 uncovered token + 2 uncovered call sites; §13 interval hypothesis (`[26,1059]` floor) | the probe candidates are already named (§13.5–13.7) — a measurement would test them, and would be the third-gate test of matrix rows D/E | hermetic |
| proxy-check | 102 cases; 12/12 arms; literal arithmetic pins; determinism case | fewest static gaps; candidates: `INTERNAL_ERROR` net (`:1044`,`:2351`), per-token detail strings | hermetic; expect low survivor count |
| claims-check | 39 cases; 5/5 arms; one kind-blind detector case | fewest static gaps; candidates: row/verdict seams beyond the one detector | hermetic; expect low survivor count |
| kimi-census | 43 cases; 2 meta-checks | **already measured** 8/10 (r2) — serves as the tool's `--regression` reference case | n/a |

**Scope of the offer, stated so it is not over-claimed:** single-edit mutants
only (coordinated edits are unmeasured everywhere, matrix §7); hermetic suites
only (no substrate-drift claim, matrix U5); results are per-revision and
per-host (no cross-host stability claim, matrix U5).

## 6. Boundary — beyond the six

- Kagi's six gates: own survey note (`gates-survey-kagi.md`; 250 selftest cases
  6/6, F-1 `--falsify` 16/18 live vs README's 18/18, F-2 three refusal paths
  with no case). Their kill-rate state: surface-census measured 8/10 (r3);
  the other five unmeasured. Kagi pins re-read for this census:
  `surface-census.sh` `275d8294a94e9eb7…`, `scope-gate.sh`
  `078a260184e25282…` (unchanged, `gates-survey-kagi.md:562-566`).
- `tsukuroi-shokunin/tools/tsukuroi-census.sh` exists with a hermetic
  `--selftest` (header: "no host … touched", `tsukuroi-census.sh:119-126`);
  the sibling lane's own round-5 plan schedules its measurement
  (`tsukuroi-shokunin/plans/round-5.plan.md:3-9`) — the third data point is
  queued in the fleet, not delivered by this census.
- `mado-shokunin/tools/` and `tabi-shokunin/tools/` were empty at read; mado's
  round-5 plan schedules its first gate (`mado-shokunin/plans/round-5.plan.md:
  4-7`). Game lanes' verifier machinery and kaidoku's audit lanes are covered
  by `verification-patterns-fleet.md` (P1–P10, D0–D10) — adjacent, not gates.
- (I) Scope rationale, restated: the asked three columns are the kumitate
  survey's vocabulary, so "the six" is kumitate's set; the same census
  questions transfer mechanically to the other gate families with the anchors
  above.

## 7. Spot-checks (all re-run 2026-10-14; scratch `/tmp/w5-tameshi-census/`)

- **S1 — pins + pulse.** `sha256sum` on the six scripts → the first-16 values in
  §1.1 (all match `gates-survey-kumitate.md:350-356`); six `--selftest` runs →
  exit 0 each with the verbatim summary lines in §1.1; `git -C
  kumitate-shokunin status --porcelain` empty after (and before).
- **S2 — meta-check anchors quoted on the bytes.** `sed -n '1432,1435p'
  surface-probe.mjs` → the "every declared finding code fires" check;
  `sed -n '863,868p' round-gate.mjs` → the full-line anchored verdict regex;
  `sed -n '846,852p' claims-check.mjs` and `sed -n '836,842p' kimi-census.mjs`
  → the `missingKinds`/`missingArms` filters and both check lines ("every
  finding kind fired by the suite" / "every fail-closed arm fired by the
  suite"); `grep -inE "observed|every .* fires" cite-check.mjs` → one prose
  hit only (`:394`) — cite-check's none stands.
- **S3 — mutation + harness sweep.** `grep -inE "mutant|mutation|kill" <g>.mjs |
  grep -viE "skill"` → cite-check `:78`/`:2372-2383`, claims-check `:827`,
  others empty; `grep -icE "fault.?inject|sabotage|kill.?rate" <g>.mjs` → 0 ×6;
  `grep -n "INTERNAL_ERROR" proxy-check.mjs` → `:211` (doc), `:1044`, `:1048`,
  `:2351` with no suite assert above `:1200` (the §3.3 gap).
- **S4 — cross-reference pins.** `sha256sum` on kagi `surface-census.sh` /
  `scope-gate.sh` → `275d8294a94e9eb7…` / `078a260184e25282…` (unchanged);
  tameshi `tools/mutate-and-run.sh` / `SKILL.md` → the §5 pins; kumitate HEAD
  `175de6b`.

## 8. Unknowns

- U1 — coordinated multi-edit rewrites (matrix class F) are unmeasured for all
  six gates and remain the method's stated boundary (`arm-class-matrix.md:206-215`).
- U2 — cite-check's integration group was never executed (needs the live tree);
  its case count and pass state are unmeasured (round-1 U1, K-R2-4 §9 carried).
- U3 — round-gate `INTERNAL_ERROR` reachability by *any* fixture is unknown
  (catch-all of last resort; §13 PU3) — and now the same question sits on
  proxy-check's `INTERNAL_ERROR` net (`:1044`/`:2351`).
- U4 — no kill-rate measured for five of the six gates; the 50 % band interior
  is unmeasured anywhere (matrix U4); §5's queue is an offer, not a schedule.
- U5 — class membership of the static D/E cells is (I) — a different reader
  could move borderline cells (matrix U6); projection cells are probe
  candidates, never findings.
- U6 — no drift or cross-host/toolchain stability reading for any suite here
  (hermetic by construction; matrix U5).
- U7 — the D/E "candidate" sets are not exhaustive: they name only anchored
  loci; the two measured cases found survivors (D2/D10, B5/B10) that a static
  read would not have flagged with certainty.
- U8 — whether kumitate's own closeouts run these six suites at these revisions
  is not checked here (round-1 U4).
- U9 — abstention shapes inside the six: cite-check's integration skip is
  declared and counted (`:2354-2356`); whether other gates carry skip-style
  cases at these revisions was not enumerated.

## Appendix A — exact commands (this census)

```
# pins + identity
cd /home/vgpnk/Projects/shokunin/kumitate-shokunin
git rev-parse --short HEAD && git status --porcelain
for f in cite-check surface-probe round-gate proxy-check claims-check kimi-census; do sha256sum scripts/$f.mjs; done
wc -l scripts/*.mjs

# pulse (cwd /tmp/w5-tameshi-census)
for g in cite-check surface-probe round-gate proxy-check claims-check kimi-census; do node .../scripts/$g.mjs --selftest; echo "exit=$?"; done

# census sweeps (anchors in §2, §7)
grep -n "every declared finding kind\|every finding kind fired\|every fail-closed arm\|every declared fail-closed arm\|every declared finding code\|codes observed\|kinds observed" scripts/*.mjs
for f in cite-check surface-probe round-gate proxy-check claims-check kimi-census; do grep -inE "mutant|mutation|kill" scripts/$f.mjs | grep -viE "skill"; done
for f in cite-check surface-probe round-gate proxy-check claims-check kimi-census; do grep -icE "fault.?inject|sabotage|kill.?rate" scripts/$f.mjs; done
for f in cite-check surface-probe round-gate proxy-check claims-check kimi-census; do grep -incE "integrat" scripts/$f.mjs; done
```

## Errata (append-only)

(none yet — new entries go below this line, never edits above per
`corpus/QUALITY.md` item 4)

## Service receipt (round 6, T6-2) — the mado engagement: outcome + queue update (append-only)

Appended 2026-10-14 by lane T6-2; scope: this file only; nothing above this
block is edited. This block is the receipt for the first engagement of §5's
standing offer — it is not an erratum, and it lands below the errata
placeholder line per that line's own instruction (no erratum entries yet).
The engagement: **mado opted in** (`mado-shokunin/plans/round-6.plan.md:(a)`);
tameshi ran the sweep **for** the lane (the service form §5 offers, as opposed
to round 5's tsukuroi self-service). Provider record:
`corpus/knowledge/mutation-case-mado-verify.md` (T6-1; 323 `wc -l`, sha256
`f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3`). Owner
record: `mado-shokunin/corpus/knowledge/gate-mutation-proof.md` (M6-1; 167
`wc -l`, sha256
`716836ca1bf3484a30cd9e08b9765398c804351efeffbde95c2863ab4ae95ddf`) plus the
two watch-arm notes (`omarchy-drift-watch.md`, `remaining-planes-census.md`).
Anchors O/I/U as §0; shas sha256, first-16 unless full.

### R.1 The service run — what the sweep found (O)

- **Target (pinned).** `mado-shokunin/tools/mado-verify.sh` @
  `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` — 45334 B,
  1098 newlines (the 1099th line carries no trailing newline), mtime
  `2026-10-14 14:08:57.107811568 -0300`; the round-5 gate as landed, unchanged
  through the run (sha before = after).
- **Suite.** `bash "$MUTANT" --selftest` — the gate's own hermetic selftest on
  the mutant copy; control output `MADO_SELFTEST: 28/28 assertions passed`,
  exit 0. Fixtures under `mktemp -d`; scenario C starves PATH so no live
  substrate or compositor is touched (note :44-49).
- **Tool (the revision the run is tied to).** `tools/mutate-and-run.sh` @
  `597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b` — §5's
  pin, carried by both run logs (`MUTATE_TOOL`, `REGRESSION_TOOL`); the tool
  has since moved (R.3 deviation 2).
- **Spec.** 10 single-edit defects, clause-mapped to the gate's declared
  contracts — A verdict token · B UNKNOWN-never-CLEAN · C exit map · D
  declared-plane census · E sha comparison · F reader fallback; every `@old`
  count==1 pre-verified; composition stated before the run: 4 defects at
  in-surface assertion sites (D1, D2, D4, D6), 6 at predicted-unasserted seams
  (D3, D5, D7, D8, D9, R1) (note :66-72).
- **Outcome.** `CONTROL: GREEN (exit=0)`; **killed 4 / survived 6 /
  inconclusive 0 → kill-rate 40 %**; `MUTATE_RESTORE: OK` (target sha before =
  after = pin); headline `MUTATE: DONE (target=mado-verify.sh defects=10
  killed=4 survived=6 inconclusive=0 kill-rate=40%)`. 11 runs in 5.26 s wall
  against a 300 s per-run timeout.

| # | clause | single edit (site on the pin) | verdict | suite evidence (tail) |
|---|---|---|---|---|
| D1 | A | `MADO_VERIFY: CLEAN` token → `OK` (`:1088`) | **KILLED** (exit 2) | `27 passed, 1 failed — A: CLEAN verdict (missing: MADO_VERIFY: CLEAN)` |
| D2 | B | UNKNOWN guard dropped from the verdict test (`:1086`) | **KILLED** (exit 2) | `25 passed, 3 failed`; `C: exit 1 (got '0' want '1')`; `C: no fake CLEAN (unexpected: … CLEAN)` |
| D3 | B | live-skip row `SKIP` → `PASS` (`:588`) | SURVIVED (exit 0) | `28/28 assertions passed` |
| D4 | C | DIVERGED path `exit 1` → `exit 0` (`:1099`) | **KILLED** (exit 2) | `26 passed, 2 failed`; `B/C: exit 1 (got '0' want '1')` |
| D5 | C | failing `--selftest` `return 2` → `1` (`:429`) | SURVIVED (exit 0) | green run never enters the failure path |
| D6 | D | `xdph` dropped from the 12-conf inventory (`:522`) | **KILLED** (exit 2) | `27 passed, 1 failed`; `B (want row hypr.local.inventory FAIL)` |
| D7 | D | include-count test `-ne` → `-lt` (`:484`) | SURVIVED (exit 0) | no fixture carries an 18th source line |
| D8 | E | sha-pin compare always "matches" (`:574`) | SURVIVED (exit 0) | row is a NOTE; no assert reads it |
| D9 | E | boundary compare always true (`:738`) | SURVIVED (exit 0) | asserted only in the PASS direction |
| R1 | F | tomllib arm `UNKNOWN` → `PASS` (`:651`) | SURVIVED (exit 0) | `PY_TOML=1` on this host; arm unreachable in-suite |

- **Reading the split (O/I).** In-surface 4/4 killed, out-of-surface 0/6 —
  the suite's assertion set and its kill set are co-extensive on this spec;
  the 40 % rate is composition, not a suite regression (note :66-72, §4). The
  highest-yield unasserted surface named: the live plane — 106 `row` sites,
  51 of them under `hypr-live`, of which the suite executes two guard rows and
  none of the body (note §3.2). D9 (boundary row asserted only in its PASS
  direction) is a new arm-class shape — no earlier tameshi case produced it.
- **Pre-registration held (O).** The predicted table — `predictions.txt`,
  written before the run — named 4 killed / 6 survived and six survivor
  classes; per-defect verdicts matched **10/10**, the four predicted kill
  mechanisms are the measured ones, and the six classes are the six survivors
  (note :73, :187-189).
- **Survivor non-equivalence probes (O; note §2, scratch `probe/`).** Six
  probes, each building an input the suite's fixtures do not: P3 (D3: fake
  PASS row read by a counts consumer), P5 (D5: no-op `sed` makes the selftest
  fail — pristine exit 2 vs mutant exit 1), P7 (D7: an undeclared 18th
  `source` line → **verdict flips to CLEAN**), P8 (D8: pin detail text claims
  a match it never checked), P9 (D9: a real mid-run change to a plane file →
  **reported byte-identical, CLEAN exit 0**), PR1 (R1: PATH wrapper without
  tomllib → UNKNOWN → PASS). Every survivor is a real behaviour change, not an
  equivalent edit.
- **REGRESSION status (O).** `REGRESSION: PASS (cases=2 passed=2; band
  killed-delta<=1 flips<=1)` at 17:44:28Z under the same tool revision — the
  harness's own gate over the two **embedded** cases (`js-kimi-census` 8/10,
  `bash-surface-census` 8/10, both `match=10/10`, flips=0). This engagement's
  table is **not** embedded, so its kill-rate claim does not yet carry a
  `REGRESSION` line over itself; embedding needs a tool edit and is recorded
  as a follow-up for the tool-owner lane (note §6).
- **Independent re-run (O).** AUD-T6 re-cut the same 10 defects with its own
  driver (no harness) and reproduced the table: `AUD-T6 RE-RUN: defects=10
  killed=4 survived=6 inconclusive=0`, per-defect verdicts and mutant shas
  identical to the service table (`/tmp/w6-aud-t6-work/`: driver `mrun.py`,
  `presweep-independent-1743Z.txt`, formal D2/D9 `formal-rerun-175044Z.txt`,
  pinned-copy shas in `pre-hashes.txt`).
- **Evidence of record.** Provider scratch `/tmp/w6-tameshi-mado-verify/`:
  `sweep.log`, `sweep/results.tsv` (10 rows + mutant shas),
  `sweep/evidence/<id>.out`, `sweep/pristine.mado-verify.sh` (= the pin),
  `spec/mado-verify.defects.spec`, `predictions.txt`, `probe/` + `probe.log`,
  `regression/` + `regression.log`.

### R.2 The owner's half — its own 15-defect run, the hardening it landed, and the re-run (O)

- mado's own lane (M6-1) cut a **15-defect spec** on the same pinned revision
  in parallel (`/tmp/w6-mado-m61/sweep/`): control `28/28 assertions passed`;
  **killed 8 / survived 7** (D01–D04, D06, D07, D10, D11 killed; D05, D08,
  D09, D12–D15 survived).
- Cross-check of the two specs on shared edit sites (O): verdicts agree where
  the edits coincide — CLEAN-token rename killed in both (T6-1 D1 / M6-1 D01,
  identical mutant sha `ec60ae5c8f82…`); DIVERGED→exit 0 killed in both (D4 /
  D03); census drop killed in both (D6 / D07); tomllib arm survived in both
  (R1 / D09). Where the edits differ the verdicts differ honestly: the
  boundary compare as always-true survived (T6-1 D9) while its flip `=`→`!=`
  was killed (M6-1 D10, `A: zero FAIL rows (got '1' want '0')`) — different
  edits, not a contradiction. The two rates (40 % vs 8/15) cover different
  defect sets and are not averaged here.
- **Hardening landed (O).** The owner hardened its own gate in-round — the
  live `mado-shokunin/tools/mado-verify.sh` is
  `c4c1afb75dd1c8aa4d8ff9b808ddbeb2a05ac0e3ab1095dd7d067cff1a625171` —
  1186 lines / 50126 B, mtime `2026-10-14 14:55:16 -03`, working tree ` M`
  (uncommitted at write time) — a **+88 / −0 line addition** to the pin, all
  inside `selftest()` (`git diff --numstat`; no verify-path edit), landed from
  the owner's final candidate (`/tmp/w6-mado-m61/final/mado-verify-final.sh`;
  the live file differs from it by one blank line). Added asserts aim at
  exactly the survivor classes: row-detail + counts-agreement helpers
  (`st_row_detail`, `st_counts_agree`, counting PASS/FAIL/UNKNOWN/SKIP/NOTE),
  the scenario-A `live.plane SKIP` row, the `hypr.file.sha_pin` NOTE detail
  (measured prefix + the round-1 pin), counts agreement in A/B/C, the
  scenario-D usage contract, and four new scenarios — E (python3 absent →
  UNKNOWN, never CLEAN), F (a failing selftest must exit 2, nested guard),
  H (an undeclared extra `source` → include graph FAIL, exact census),
  I (a plane change mid-run → `boundary.readonly` FAIL). Selftest count per the
  owner: 28 → 53 (this receipt ran no selftest against the revision — a third
  concurrent run was deliberately not started; note U4's scratch-namespace
  incident is the precedent).
- **Re-run of tameshi's exact spec on the hardened revision (O,
  owner-measured).** Spec = byte copy of the provider's, sha256
  `c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8` (this
  lane re-verified the equality); harness `b56c6e57…`; control `MADO_SELFTEST:
  53/53 assertions passed`; **killed 10 / survived 0 / inconclusive 0 →
  kill-rate 100 %**; `MUTATE_RESTORE: OK` (target sha `c4c1afb7…` before =
  after). The six survivors of R.1 are each killed by a newly added case; the
  four already-killed defects stay killed and fire in more scenarios (D2 ×6,
  D4 ×5). Reading: this is a **directed repair** — the suite was extended
  against exactly these defects, so 100 % is expected, not an independent
  rate (the tsukuroi hardening precedent, tested from the strong side).
- **Residuals recorded unabsorbed (O; owner note §3).** rc-6 arm dead code
  (`row_from_rc` `6) … UNKNOWN`, reachable by no check; an equivalent edit
  survives by construction); the **exit-flatten family** (a suite-failure exit
  flattened to 0 runs red in-suite but is green to an exit-only harness — a
  harness boundary, stated as such); the live-plane body (51 sites,
  provider recommendation #1) still unexercised; two out-of-band usage exits
  (`--root` without value, bad `MADO_VERIFY_LIVE`) still read-through at the
  hardened revision. No widening ships unproven.
- The round's widening (b)/(c) landed as *notes* gated on the proof by their
  own §0 (`omarchy-drift-watch.md`: ships as "a companion note + arm spec, not
  as a gate edit from this lane"; `remaining-planes-census.md`: "adds no gate
  rows"), and the owner's note re-pins the gate for downstream stages to the
  hardened identity (§5 there).

### R.3 The cross-lane service protocol, as it actually ran (O/I)

- **Opt-in (O).** The customer lane's own plan pre-registers the engagement
  (harness read-only; defect spec per declared clause; suite = the gate's own
  selftest exercising `$MUTANT`; evidence = per-defect verdicts + kill-rate +
  control + restore), and the provider note opens by quoting that opt-in
  (`mutation-case-mado-verify.md:3-11`). No lane was drafted; no queue
  position was assigned. The contract this run formalized now sits on the
  SKILL page: "The mutation service — running a sweep for an opting-in lane
  (round 6, measured)" (`SKILL.md:794-918`; the page was still being written
  while this receipt was drafted — sha is point-in-time, see S3) — opt-in
  items, ordered fail-closed protocol, boundaries, report shape.
- **Read-only (O).** Provider writes stayed in scratch; the harness ran on
  byte copies only; `MUTATE_RESTORE: OK` proves target bytes unmoved; the
  gate's selftest reads no live path. The provider note also records the
  service's provable negative: its writes never touched the substrate; a
  shared selftest scratch namespace showed foreign
  `/tmp/w5-mado-m52-selftest.*` directories from concurrent writers (≥37 seen
  by the provider, 44 at the owner's cleanup — attribution unknown; untouched
  by the provider, its own 8 paths removed; the owner removed its 90).
- **Owner-hardens (O).** All six survivors returned as recommendations, ranked
  by yield with the measured mutant each would kill (note §8, 7 items); the
  provider wrote no patch. The owner then hardened its own gate *and re-ran
  the same spec* (R.2): 10/10 killed, residuals listed unabsorbed. Gate repair
  stayed the owner's own act (PROVINCE.md:16-18); the service's tables are
  tied to the pre-hardening pin and none of them is overwritten by the
  owner's re-run.
- **Deviations from §5's text and the round plan, recorded not smoothed.**
  1. The first engagement was **not** the queue head (cite-check). mado — a
     gate that did not exist when §5 was written (§6: mado `tools/` empty at
     census) — opted in first. The queue's expected-yield ordering was not
     tested by this engagement; the provider note says the same
     (`mutation-case-mado-verify.md:219-222`).
  2. **The harness drifted mid-round, by a concurrent (sanctioned)
     self-hardening lane.** The sweep and the regression run are tied to tool
     `597e1419…` (both logs pin it); re-pin at 17:46:15Z: `b56c6e57…`, 46850 B,
     mtime 14:46:08. Cause (O, in-repo): T6-4's own-gate hardening —
     `self-hardening-r6.md`, `git diff --stat` vs R1 = +83/−4 lines in three
     hunks, comparator behaviour proven identical (probe identity R1 ≡ R2).
     Every number in the service run is tied to R1; the owner's re-run is tied
     to R2 (its note pins both).
  3. The provider ran a 10-defect service sweep; the owner ran its own
     15-defect sweep on the same revision in parallel, then re-ran the
     provider's 10-defect spec on its hardened revision; §5's one-table-per-
     sweep shape held per sweep, not per engagement.
  4. Method-page revision: §5's quoted pin `dd2f4dee…` / 665 lines is the
     round-3/4 revision (`git show 53e74a8:SKILL.md` = `dd2f4dee…`),
     superseded by the round-5 commit `e0c453e` and again in this round (the
     service section above). This receipt re-measures rather than re-quotes.

### R.4 The updated offer queue (O, ordered by §5's rule — most static protection last)

Measured fleet-wide to date (one row per sweep; not averaged across
compositions): kimi-census (kumitate) **8/10** (r2) · surface-census (kagi)
**8/10** (r3) · tsukuroi-census **6/10** (r5; the owner hardened 26 → 35
selftest cases afterward, its own revision) · mado-verify **4/10** on the r5
pin (r6, service, this receipt) + **10/10 on the hardened r6 revision** (owner
re-run of the same spec — directed repair) + 8/15 on the owner's own 15-defect
pre-sweep. The mado r5-pin point is the first below the 50–80 % band; cause
per the provider's §4 is composition (4 in-surface defects — all killed; 6
out-of-surface — none), which is the tsukuroi band amendment tested from the
other side. Bands stay as amended; no floor is claimed.

Still unmeasured, kumitate's five, order unchanged from §5:

| Gate | State now | Sweep prerequisite |
|---|---|---|
| cite-check | **probe only** — PREP-T6 cut 4 defects (1 killed: drift-gate drop → 61/62; 3 CLI-accounting survivors: aggregate-verdict collapse, n/n summary counts, CLI exit fail-open), `MUTATE_RESTORE: OK`, kumitate tree clean; a full sweep is not recorded at this write | hermetic 62-case run on a copy; the integration group stays a declared skip |
| surface-probe | unmeasured | hermetic |
| round-gate | unmeasured | hermetic |
| proxy-check | unmeasured | hermetic |
| claims-check | unmeasured | hermetic |

Cross-refs beyond the six (§6 scope, refreshed read-only today): kagi — five
of six still unmeasured (surface-census 8/10; pins unchanged `275d8294…` /
`078a2601…`); tsukuroi — measured (r5), gate since hardened by the owner; mado
— measured across two revisions (this receipt), downstream pins re-pointed to
the hardened identity by the owner's note §5; tabi `tools/` still absent (`ls
tabi-shokunin/tools` → No such file or directory, rc=2). Out of the census
universe (sightings only, not queued, not surveyed): kake
`scripts/{freshness-sweep,probe-delta}.mjs`, kama
`tools/{kama-probe,test-snapshot}.sh`, kotoba `verifiers/*` — file existence
is O; their gate-ness and measurement state are U until a survey admits them.

### R.5 Pins and spot-checks (this append; scratch `/tmp/w6-tameshi-t62/`)

- S1 — target pin and its hardening: the sweep's copies
  (`sweep/pristine.…`, the owner's scratch copy) all hash to `d7edaab4…d0e13`,
  45334 B; the live `mado-verify.sh` is the owner's hardened `c4c1afb7…625171`,
  50126 B / 1186 lines (re-measured at write time).
- S2 — tallies on the evidence of record: `grep -c KILLED` → 4,
  `grep -c SURVIVED` → 6 on `sweep/results.tsv`; `sweep.log` carries
  `MUTATE_RESTORE: OK (… before=d7edaab4… after=d7edaab4… pristine-sha256=
  d7edaab4…)` and the `kill-rate=40%` headline; `predictions.txt` names the
  same 10 defect ids; `regression.log` carries `REGRESSION: PASS (cases=2
  passed=2 …)`; provider note sha re-measured = `f2d53d49…`; owner note sha
  re-measured = `716836ca…`, and its re-run spec sha = the provider's
  (`c7ee75b9…`, re-verified); the audit's reproduction file ends `AUD-T6
  RE-RUN: defects=10 killed=4 survived=6 inconclusive=0`.
- S3 — drift and queue anchors: tool re-pin now `b56c6e57…` (R2) vs the run's
  `597e1419…` (R1, both logs); `ls kumitate-shokunin/scripts/` → the six
  `.mjs`; `sha256sum kagi-shokunin/corpus/{surface-census,scope-gate}.sh` →
  `275d8294a94e9eb7…` / `078a260184e25282…` (unchanged); tabi tools absent;
  the owner's final candidate exists at `/tmp/w6-mado-m61/final/`; `SKILL.md`
  sha re-measured at write time (point-in-time — the page was still being
  written; the round record carries its final revision).
- S4 — this append: `sha256sum` before = `adeb3070cf7ed705…` (28842 B, 385
  `wc -l`); after-write sha and the re-read head/tail of this block are
  reported in the lane's report (self-reference impossible inside the file);
  nothing above this block is edited.

### R.6 Unknowns and landing state at write time

- Provider note `mutation-case-mado-verify.md`: **landed** (323 lines, sha
  `f2d53d49…`; the R.1 numbers are read from it and its scratch).
- Owner proof `gate-mutation-proof.md`: **landed** (167 `wc -l`, sha
  `716836ca…`, 14:59 -03) — it carries the owner's 15-defect table, the
  hardening, the 10/10 re-run, the residuals, and the re-pin. The hardened
  gate revision is uncommitted at write time.
- AUD-T6 independent re-run: reproduced 4 killed / 6 survived with verdicts
  and mutant shas identical (R.1); the lane's own report not read here.
  VER-T6 verification artifacts exist (`/tmp/w6-ver-t6/evidence/`,
  D5-focused); no verdict read at write time.
- Tool drift (R.3 deviation 2): reproduction of the R.1 table under R2
  (`b56c6e57…`) was measured by the owner on the hardened revision (10/10),
  but tameshi's own R.1 table was not re-cut under R2 — remains U here.
- The hardened revision is measured only against the same spec it was
  hardened against (directed repair, 10/10); an independent defect set
  against it, and its committed state, are U at this write.
- §8 U4–U7 stand: the 50 % band interior, cross-host stability, and
  coordinated multi-edit rewrites remain unmeasured fleet-wide; this receipt
  adds no rate beyond the rows named in R.4.