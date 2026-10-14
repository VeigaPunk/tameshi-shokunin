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