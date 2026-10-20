# Arm-class matrix — JS (r2) × bash (r3) (TAMESHI-R4-1)

Run date 2026-10-14. Lane: tameshi (round 4; plan `tameshi-shokunin/plans/round-4.plan.md`,
axis: calibration — suite-vs-arm completeness across the two worked cases). Sources: the two
mutation-case notes in this corpus — `knowledge/mutation-case-kimi-census.md` (r2, kumitate
`kimi-census.mjs`, mutants D1–D10) and `knowledge/mutation-case-kagi-census.md` (r3, kagi
`surface-census.sh`, mutants B1–B10). Substrates kumitate-shokunin + kagi-shokunin
**read-only**: three anchor re-reads plus two hermetic `--selftest` pulses on the pinned
bytes (§12); both trees porcelain-empty after; this note is the only file written by the run
(the corpus/README row and the `LOG.md` entry fold in at lane review).

Anchors: **O** = observation (file:line, command output, or a re-quoted measured table cell);
**I** = inference; **U** = unknown. `kimi-census.mjs:NNN` =
`kumitate-shokunin/scripts/kimi-census.mjs` @ sha256 `83016d45…4f426`, kumitate `175de6ba`;
`surface-census.sh:NNN` = `kagi-shokunin/corpus/surface-census.sh` @ sha256 `275d8294…53009f`,
kagi `fecee87`. Both pins re-verified held 2026-10-14 (§12).

Method (O): this note runs no new mutants. It re-cuts the two notes' measured tables by **arm
class** — a surface the suite either reads through an assert or does not — and states per
class where the cases agree and where they disagree (the plan's anti-claim: a disagreement is
the finding, never averaged). Ledger verdicts and failing-case counts are O (re-quoted from
the note tables; the round-3b audit independently re-swept both cases end-to-end through
`tools/mutate-and-run.sh`, per-defect verdicts identical to both tables — `LOG.md` round-3b
`TAMESHI-B3`). **Class membership is I** — a reading of measured cells, not a new
measurement. Classes are surfaces, not a partition: D2 and B10 are (deliberately) listed
under two rows each.

## 0. Headline

- O: 20 mutants (10 JS + 10 bash), every one a single exact-text edit on a fresh `/tmp`
  copy; **16 killed, 4 survived, 0 inconclusive**; both suites 8/10 (80 %).
- O: all four survivors fall in exactly two classes — **reported-but-unasserted surfaces**
  (JS D2, JS D10, bash B10) and **unreached arm** (bash B5). No survivor is a wrong
  *behavior*: every single-edit behavior/count/exit mutant died in both cases.
- Summary matrix (rows carry the detail):

| # | Arm class | JS case (D1–D10) | bash case (B1–B10) | Pair verdict |
|---|---|---|---|---|
| A | Verdict paths | prefix-asserted DRIFT, one exact CLEAN line; **D2 survives on the tail** | exit + one substring token, no full-line pin; **B10 survives on the summary fields** | agree on the phenomenon (asserted stem protected, unasserted remainder not); **disagree on pin style** (§2) |
| B | Fail-closed arms | D8 killed on 3 environment-failure cases; token enum + coverage meta-check | B8 killed on 2 malformed-input exit-2 cases | exit-map (2→1) protection agrees; **arm species differ** (§3) |
| C | Counts | D1/D6/D7 killed (16/2/2); whole-line + literal-count asserts | B2/B7 killed (2/1); one exact-count substring | protected where asserted; **width and assert exactness differ** (§4) |
| D | Reported-but-unasserted surfaces | D2, D10 survive | B10 survives | **agree: not protected** — 3 of 4 survivors (§5) |
| E | Unreached arms | none — D4/D5 arms reached and killed | B5 survives (fixture-absent); B4 killed token-only | **disagree 2/2 vs 1/2 — the disagreement is the finding** (§6) |
| F | Coordinated edits | U1 unprobed | U1 unprobed | agree only that the method stops here — unknown (§7) |
| G | Behavior predicates *(added row)* | D3, D9 killed | B1, B3, B6, B9 killed | agree: 6/6 killed (§8) |

## 1. Ledger — all 20 mutants, one line each

Classes per row letters above. Verdicts (O: both notes' §1 tables; audit-replayed in round
3b). Failure evidence is the notes' failing-case labels, abbreviated.

| # | Defect class (note label) | Row(s) | Verdict | Measured kill evidence |
|---|---|---|---|---|
| D1 | off-by-one count (counted table) | C | killed | 16 cases incl. the exact green baseline; count-string `'19 children, 18 declared'` |
| D2 | off-by-one count (findings cap) | A, D | **survived** | 43/43; max findings in any suite run 2 vs cap 6; non-equiv: 5 ids + `+23 more` |
| D3 | inverted condition (child predicate) | G | killed | 16 — inversion flags every declared child of the green fixture, baseline catches |
| D4 | dropped arm (root-stray loop) | E | killed | exactly the 3 root-enumeration cases; no other case moves |
| D5 | dropped arm (chain presence) | E | killed | 1 — the singleton `MEMBER_MISSING … presence is gated` case |
| D6 | wrong mode pin (`0o600`→`0o644`) | C | killed | 2 — the two loose-mode cases (+ FIFO case collateral) |
| D7 | weakened predicate (floor semantics) | C | killed | 2 — both loose-mode cases (partial-overlap fixtures) |
| D8 | wrong exit-code mapping (`failClosed 2`→`1`) | B | killed | exactly the 3 fail-closed cases |
| D9 | weakened secrecy pin (leaf kind) | G | killed | 2 — FIFO token + dangling-symlink anti-read fixtures |
| D10 | wrong reported constant (`FROZEN.K2`) | D | **survived** | 43/43; only `frozen.K5` asserted; non-equiv `frozen=24` vs `25` |
| B1 | wrong `-eq` (scan guard inversion) | G | killed | 1 — case 05 `undeclared-file` (`want exit=1 token=SURFACE UNLISTED got exit=0`) |
| B2 | numeric boundary off-by-one (rows floor) | C | killed | 2 — cases 01 `clean` + 04 `runtime-absent` |
| B3 | inverted test (CROSSCHECK `!=`→`==`) | G | killed | 3 — 01, 04 + 06 `crosscheck-disagree` |
| B4 | dropped branch (symlink arm) | E | killed | 1 — case 07; **exit still matched, the token assert carried the kill** |
| B5 | dropped branch (exec x-bit arm) | E | **survived** | 16/16; no case strips +x; non-equiv: `SURFACE OK … (exec 644)` exit 0 |
| B6 | off-by-one (magic length) | G | killed | 2 — cases 01 + 04 |
| B7 | off-by-one (UNVERIFIED count) | C | killed | 1 — case 10 demands the exact substring `unverified=3` |
| B8 | wrong exit mapping (`die` 2→1) | B | killed | 2 — cases 13 `malformed-row` + 14 `fused-shape-row` |
| B9 | inverted class select (runtime→asset) | G | killed | 2 — cases 03 `asset-gone` + 04 `runtime-absent` |
| B10 | reported-but-unasserted count (summary `ok=`) | A, D | **survived** | 16/16; no case reads summary fields; non-equiv `ok=0` vs `ok=1` |

## 2. Row A — Verdict paths (exit + verdict line as read by callers)

**JS.** O: the DRIFT verdict is asserted by prefix plus kind plus a `members=` substring
(`kimi-census.mjs:498-499`); the **only** whole-verdict-line equality anywhere is the CLEAN
line (`lastLine(r) === 'KIMI_CENSUS: CLEAN (members=49 checked=49 chain=3 info=4)'`,
`:511-512`), with `startsWith('KIMI_CENSUS: CLEAN')` at `:642` and `includes(…)` tiers
elsewhere (`:535-536`). Positive controls: D3 and D1 each die on 16 cases *because* the exact
baseline line breaks under them — the equality assert is load-bearing. Measured gap: **D2
survives** (43/43) with the tail past the prefix changed — one fewer listed id and `+23 more`
instead of `+22 more` on a ≥6-finding input; the max findings any suite run reaches is 2
against the cap of 6, and because the DRIFT assert is prefix-based, even a 6-finding case
would not pin the tail.

**bash.** O: every case asserts `exit + one substring token` (`run_case`, `surface-census.sh:747-760`;
the token may be empty). There is **no** whole-line or prefix assert anywhere in the selftest
— B4's exit code matched its expectation and only the `SURFACE LINK` token killed the
deletion; B1 dies on case 05's token plus exit. Measured gap: **B10 survives** (16/16) with
the CLEAN line's `ok=` field moved (`:862`); off-suite: `ok=0` vs pristine `ok=1`, both
exit 0.

**Agreement (stated as one finding):** in both cases the verdict surface's *asserted stem*
(exit + the pinned token/prefix) is protected — all 16 kills are read through it — and both
lose a mutant confined to the verdict line's *unasserted remainder*. **Disagreement (stated,
not averaged):** the pin styles differ — JS pins one entire verdict line by equality and
tiers down through prefix/substring for others; bash pins no line weight above a substring,
anywhere. The two gap shapes are therefore different in kind: JS's is truncation arithmetic
inside a verdict line (`+N more`), bash's is a field of a summary line read by no case.

## 3. Row B — Fail-closed arms

**JS.** O: D8 (`failClosed` `return 2` → `return 1`, `:396`) is killed by exactly the three
fail-closed cases, and those cases assert more than the exit: `--root /nonexistent` and the
unreadable root assert exit 2 **and** the `KIMI_CENSUS: FAIL-CLOSED (KIMI_ROOT_MISSING`
prefix (`:777-779`, `:789-790`), the `--json` case asserts `j.verdict === 'FAIL-CLOSED'` +
`j.fatal.kind` + empty totals (`:800-802`); the suite also declares its arm enum
(`FAIL_CLOSED_KINDS = ['KIMI_ROOT_MISSING']`, `:148`) and meta-checks that every declared arm
fired (`:840-842`). The measured species here is **environment failure** (root missing,
unreadable, json variant).

**bash.** O: B8 (`die` exit 2 → 1, `:85`) is killed by cases 13 `malformed-row` (wants
exit=2 + token `bad kind`) and 14 `fused-shape-row` (rc==2 + `too many fields`). The exit-2
species here is **malformed committed data** — the census's own taxonomy calls it "not a
verdict". The "cannot measure" species sits elsewhere by design: `sqlite-unavailable` exits
**1** with the verdict-shaped `SHAPE UNVERIFIED` line, and case 10 pins it with substrings
plus the exact count `unverified=3` (`:782`) — the count that also killed B7.

**Agreement (narrow, measured):** a 2→1 exit-map edit dies in both cases. **Disagreement
(stated, not averaged):** the two cases' exit-2 case sets guard different arm species
(environment failure in JS; malformed-input refusal in bash), and bash's environment-class
condition is deliberately *not* an exit-2 arm at all — it is an exit-1 verdict pinned by
substrings/count. So "fail-closed arms are protected" is true of the pair only for the shared
exit-map property; the arm inventories behind it are not the same inventory.

## 4. Row C — Counts (declared↔live, floors, tallies, exact-count strings)

**JS.** O: D1 (counted `18`→`17`, `:105`) killed on 16 cases — the edit desyncs a duplicate
table (`ENUMERABLE.childCount` `:137`) and breaks the green fixture itself; the tripwires
include the exact baseline counts and the literal `'19 children, 18 declared'`. D6 (declared
floor `0o600`→`0o644`, `:124`) killed on the two loose-mode cases, with the FIFO case as
collateral (the fixture's own `modeFloor`-driven chmods). D7 (floor predicate `!== floor` →
`=== 0`, `:306`) killed on the same two cases — the fixtures use partial-overlap modes
(`0o500` vs `0o700`; `0o400` vs `0o600`), which discriminate "contains the floor" from
"intersects the floor". Surviving count-shaped surface: D10 (row D).

**bash.** O: B2 (rows floor `-ge`→`-gt`, `:435`) killed on both exit-0 green fixtures (the
fixture's part table sits exactly at the floor); B7 (`N_UNVERIFIED + 1` → `+ 2`, `:405-406`)
killed on case 10 by the exact substring `unverified=3` — the suite's only exact-count string
with a case behind it. Surviving count-shaped surface: B10 (row D).

**Agreement:** a count edit that an assert reads dies in both cases, floors included.
**Disagreement (stated, not averaged):** (O) width — a count edit in JS kills up to 16/43
(shared in-memory fixtures + exact-line asserts), in bash at most 2/16 (fresh fixture per
case + exit/token asserts; the note's §4 mechanism (I)). (O) assert exactness — JS reads
counts through whole-line equality and literal count strings; bash reads one exact-count
substring plus floor-token cases (`rows part 0`). (O) both cases nevertheless lose one
count-shaped mutant to the same place: a count the suite never reads (D10/B10 → row D).

## 5. Row D — Reported-but-unasserted surfaces

**JS survivors.** O: D2 — the verdict line's tail past the asserted prefix (row A). D10 —
the `FAMILY … frozen=${FROZEN[f]}` line (`:415`) and `totals.frozen` in `--json` (`:365`);
the only assert touching the frozen block is `j.totals.frozen.K5 === 3` (`:526`), verified by
grep on the pinned bytes (§12). Off-suite non-equivalence for both, measured in the note.

**bash survivor.** O: B10 — the CLEAN summary fields (`:862`). Grep on the pinned bytes shows
`N_OK`/`N_ABSENT`/`N_SKIP` appear only at their init (`:148-149`), at increment sites
(`:193`, `:235`, `:346`, `:403`, `:413`), and at the two summary arg lists (`:862`, `:866`);
no case reads them. Reaching across both summary lines: the **only**
summary-field reader anywhere is case 10's `unverified=3` substring; every other field
(`ok=`, `absent=`, `skipped=`, the CLEAN assets/runtime/scanned counts) is reported-unread.

**Agreement: this class is NOT protected in either case** — 3 of the 4 survivors of the 20
sit here. Both suites' assert vocabulary is exit + selected substrings/exact lines, so a
mutant confined to displayed report data survives by construction. The two notes reached
this class independently (JS §2, bash §2/§4), so per PROVINCE's two-lane bar it is admitted
as a general property of these suite styles. No disagreement on the row's verdict; the loci
differ (JS: verdict tail + frozen block; bash: summary fields) — both are places where a
downstream consumer of `--json`/the verdict line is protected by nothing.

## 6. Row E — Unreached arms

**JS: no instance.** O: both probed arm-deletion mutants were **reached and killed** — D4
(root-stray reporting loop deleted) died on exactly the three root-enumeration cases with no
other case moving (arm isolation), D5 (chain presence gate) died on a singleton. Nothing in
the JS case is an arm no fixture reaches.

**bash: one instance.** O: B4 (symlink arm deleted) killed on case 07 — but the exit code
still matched and the token assert carried the kill (a reached arm pinned by one token). B5
(exec x-bit arm deleted, `:214-217`) **survived** 16/16: no case ever exercises a row
declared `exec` whose file lost its x bit — the fixture creates that row at `chmod 755` and
no case strips it (the only chmod sites are `:521-588`, `:704-717`, `:768`; `-x ` occurs once
in the file, inside the deleted arm; §12). Off-suite non-equivalence: the mutant reports
`SURFACE OK … (exec 644)` exit 0 where pristine reports `SURFACE DIVERGED … no execute bit`
exit 1. Nothing reaches the arm, so no implementation of it — right or wrong — can move the
suite.

**Disagreement (the anti-claim's finding, stated not averaged):** same defect class — a
deleted arm — yields 2/2 kills in JS and 1/2 in bash; across the four dropped-arm mutants of
the 20, 3/4 died, and the survivor is the one arm with no case behind it. The unit that
disagrees is the **arm**, not the language: JS's suite reached both arms it was handed;
bash's suite reached one of two. Reachability is per-arm and must be measured per-arm
(B5's shape matches kagi's own F-2 refusal-path-without-a-case hole, cited in `SKILL.md:451-456`).
**Confidence:** one measured instance (B5) in one lane → proposed, not general; JS's D4/D5
are counter-instances that bound the class rather than contradict it.

Boundary remark (case-side, different species): bash cases 15/16 `skip-case …
substrate-absent` performed no execution yet sit inside `PASS (16 cases)` (O §12) — a
*declared, counted* abstention, not an unreached arm; the hermetic case set on this host is
14+2. The JS recorded runs abstained from nothing. Do not conflate skipped cases with
unreached arms: the skip is loud in the case grammar, the unreached arm is silent.

## 7. Row F — Coordinated edits

**No mutants in either case.** JS U1: a coordinated edit of both count tables (`:105` **and**
`:137`) was not probed; the note's (I) — the literal-count asserts would still kill it. bash
U1: both summary arg sets (`:862` + `:866`) or a count increment plus its summary field are
outside the single-edit experiment; the note infers no residual tripwire. My own (I), from
B7/B10: besides the lone `unverified=3` reader, a coordinated report-region edit sits behind
no case. Either way: **U — unmeasured in both**, the row cannot be filled from these two
experiments, and the pair's only agreement is that the method stops here (JS U2 / bash scope:
single-text edits, no reordering, no timing mutants). Not admitted; not averaged.

## 8. Row G — Behavior predicates (added row)

Not one of the assignment's six classes; added so that all 20 mutants have a row (without it
D3, D9, B1, B3, B6, B9 are unplaced). These are single-edit logic/invariant mutants that are
neither counts, verdict-content, exit-map, nor arm-deletion: JS D3 (child-predicate
inversion, `:332`; killed 16), JS D9 (secrecy leaf pin, `:292`; killed 2 — the FIFO token and
dangling-symlink fixtures double as leaf-pin guards); bash B1 (scan-guard inversion, `:241`;
killed 1), B3 (CROSSCHECK `!=`→`==`, `:229`; killed 3 — fires on agreement in 01/04 and
cannot fire on disagreement in 06), B6 (magic length `len+1`→`len`, `:371`; killed 2), B9
(missing-branch class select `runtime`→`asset`, `:191`; killed 2).

**Agreement: 6/6 killed in both cases** — every predicate mutant the suites were handed is
caught, in both languages. Disagreement (width only): JS 16 on the fence-predicate edit vs
bash's near-singletons (1–3), the structural width gap again.

## 9. Admission status (PROVINCE two-lane bar)

| Class | Instances | Lanes | Status |
|---|---|---|---|
| Reported-but-unasserted surfaces | D2, D10, B10 | 2 | **admitted** (general for these suite styles) |
| Verdict-stem protected / remainder unasserted | D2, B10 (+16 kills as channel evidence) | 2 | **admitted** as a phenomenon; pin-style divergence recorded, not normalized |
| Fail-closed exit-map (2→1 edit dies) | D8, B8 | 2 | **admitted (narrow)**: arm species behind it differ by case |
| Asserted counts protected | D1, D6, D7, B2, B7 | 2 | **admitted** with the width divergence recorded |
| Behavior predicates caught | D3, D9, B1, B3, B6, B9 | 2 | **admitted** |
| Unreached-arm survivor | B5 | 1 | **proposed** — single instance; JS counter-instances D4/D5 bound it |
| Coordinated edits | none | 0 | **unknown** |

## 10. Calibration and errata (append-only)

E1 — the author's pre-write expectation was that the cross-case disagreements would sit in
"unreached arms" and "coordinated edits" only. Measured while building the matrix: the
disagreement set is wider — pin style within verdict paths (exact line vs substring), arm
species under fail-closed (environment vs malformed-input; plus bash's deliberate exit-1
"cannot measure" verdict), and assert exactness + width within counts. Recorded as a
calibration miss of the pre-write model, not a correction of any measured cell.

E2 (deliberate, recorded so it is not read as double-counting) — D2 and B10 are listed under
both row A (verdict paths) and row D (reported surfaces). The classes are surfaces a mutant
can touch at once; the ledger's total remains 20 mutants, 16 killed, 4 survived.

## 11. Unknowns

- U1 — coordinated multi-edit rewrites (both count tables JS; both summary arg sets or a
  count+field pair bash) are unmeasured in both cases (row F).
- U2 — the D2 boundary is bounded, not closed: max findings observed in any suite run = 2 vs
  the cap of 6, and the DRIFT assert is prefix-based, so even a 6-finding fixture would not
  pin the `+N more` tail (JS U3 scope: text-mode verify runs only).
- U3 — bash verbs-path mutants were excluded (cases 15/16 skip on this host; on a
  handler-present host their verdicts would be host-gated) — an entire arm class with no
  case executed here, distinct from B5's unreached arm.
- U4 — no third gate/language: the matrix is two artifacts, two languages, one host,
  2026-10-14. Nothing here moves the 50 % band or the band interiors (both cases sit at 80 %).
- U5 — nothing here measures either suite against substrate drift (hermetic by
  construction), nor cross-host/toolchain stability (JS U5, bash U5).
- U6 — class membership (which row a mutant "hits") is (I) by reading; a different reader
  could move borderline cells (D6/D7 sit on the counts/predicate seam). The measured
  verdicts and failing-case labels the rows rest on are (O).

## 12. Spot-checks (live, 2026-10-14, on the pinned bytes)

All three re-run during this write; both trees porcelain-empty after; scratch under
`/tmp/tameshi-r4-1-tmp/` only.

1. **JS pin + assert tiers** — `sha256sum kumitate-shokunin/scripts/kimi-census.mjs` →
   `83016d45…4f426`; `sed -n '498,499p'` → the prefix-based DRIFT assert
   (`lastLine(run).startsWith('KIMI_CENSUS: DRIFT')`); `sed -n '511,512p'` → the exact CLEAN
   equality; `sed -n '526p'` → `j.totals.frozen.K5 === 3`; `grep -n frozen` → only `:365`
   (JSON totals), `:415` (FAMILY text) and `:526` (the single assert) touch the block in code.
2. **bash pin + assert grammar** — `sha256sum kagi-shokunin/corpus/surface-census.sh` →
   `275d8294…53009f`; `sed -n '747,760p'` → `run_case` = exit + one substring token
   (`[[ "$rc" != "$want_exit" ]] || { [[ -n "$token" ]] && [[ "$out" != *"$token"* ]]; }`);
   `sed -n '862p;866p'` → the CLEAN and DRIFT summary arg lists; `grep -n 'N_OK\|N_ABSENT\|N_SKIP'`
   → init (`:148-149`) + the five increment sites + the two printf arg lists only (no case
   reads them); `grep -n -- '-x '` → exactly one hit, `:214`, inside the arm B5 deletes.
3. **Live pulses + case grammar** — `bash kagi-shokunin/corpus/surface-census.sh --selftest` →
   `SELFTEST: PASS (16 cases)` exit 0, with `ok-case 10 sqlite-unavailable exit=1 UNVERIFIED,
   unverified=3`, `ok-case 13/14 … exit=2`, and `skip-case 15/16 substrate-absent`;
   `node kumitate-shokunin/scripts/kimi-census.mjs --selftest` → `KIMI_CENSUS_SELFTEST: 43/43
   pass` / `VERDICT: PASS` exit 0; `FAIL_CLOSED_KINDS` enum `:148` and the "every fail-closed
   arm fired" meta-check `:840-842` present. Both artifact pins still held after the runs.

## 13. Projection — kumitate `round-gate.mjs`: declared arms vs its suite's meta-check (TAMESHI-R4-4)

**Projection, not measurement.** This section is a static read of
`kumitate-shokunin/scripts/round-gate.mjs` @ sha256 `f890e277…a834d3e9` (kumitate `175de6ba`,
both read 2026-10-14, §13.10): no mutant was cut, no gate mode was executed, no `--selftest`
pulse was taken, and no scratch file was written. Cells are **O** (pinned-byte reads,
`file:line`) or **I** (readings of them); every behavioral claim is a projection. Nothing here
amends §§0–12: the two measured cases stay the only evidence behind §9, and a projection cell
is a probe candidate for a future round, never an admission. The artifact is deliberately a
**third gate** — a second JS suite from kumitate's tree (the lane's own round-close pre-check),
outside the mutation envelope. Check shorthand: `rN` = the suite's numbered checks, `fcA–fcF`,
`u1–u5`, `rt1–rt8`, `jClean/jDrift/jFc` as named in the suite (`:874-1493`).

**Declared surface (O).** The script declares its behavioral surface in three shapes: one
*enum* — `FINDING_KINDS`, 14 kinds (`:171-176`); two *prose inventories* — finding kinds and
severities (`:66-98`) and the fail-closed token list (`:115-117`); and *literals* — contract
id `kumitate-round-gate-v1` (`:140`), exit map `0 · 1 · 2 · 64` (`:63-64`), usage (`:177-185`),
defaults (`:50-61`).

**Meta-check coverage (O).** The suite (60 `check(` registrations) carries exactly one
meta-check of arm coverage: *"every declared finding kind fires in at least one fixture"*
(`:1487-1493`), testing `FINDING_KINDS ∖ observed = ∅`; `observed` is fed only by
`parseFindings` (`:857-860`), which parses text-mode `ROUND_GATE␣␣error|warning␣␣KIND␣␣detail`
lines off suite-run stdout. No other declared family has a meta-check.

| Declared family | Declared as (O) | Meta-checked | Static coverage (I) |
|---|---|---|---|
| 14 finding kinds | enum `:171-176` | **yes**, `:1487-1493` | 14/14 have ≥1 text-mode fixture (§13.1) |
| 7 fail-closed tokens | prose `:115-117` | no | 6/7 hand-asserted; 1 token + 2 call-site species uncovered (§13.3) |
| exit map 0/1/2/64 | prose `:63-64` | no | 4/4 exercised (`2`: fcA–F, jFc, rt3, rt5; `64`: u1–u5, rt4) |
| 4 modes + precedence | prose `:23-48` | no | 4/4 modes exercised; selftest-wins pinned indirectly (`:1396`); `--selftest --json` unpinned (§13.6) |
| flags + 4 env keys | usage `:177-185`, `:50-61` | no | all flags exercised; `UFO_SRC` set-value branch uncovered (§13.6) |
| JSON contract | const `:140` | partly | top-level key-set equality + check shape (`:1254-1262`); nested `citations` fields partly unread (§13.5) |

**13.1 The enum family — 14/14 statically covered.** (O) every declared kind has a text-mode
fixture; emission arms and pins:

| Kind | Emission (O) | Fixture pins (O) |
|---|---|---|
| REPORT_MISSING | `:342` | r3 `:898` — exit 1 · checks=5 · exact list |
| REPORT_THIN | `:345` | r4 `:908` — `(bytes=25)` exact; two-space format `:917` |
| REPORT_HEADINGS | `:347` | r6 `:925` — paired with SHONEN warning; `headings=0` |
| REPORT_ROUND_MISMATCH | `:349` | r7 `:934`; r8 `:942` (`round-1` vs N=10); r9 `:950` (`round-10` vs N=1) |
| REPORT_SHONEN_MISSING | `:352` | r6; r19 `:1048`; r20 `:1058` (strict); r21 `:1067` (lowercase negative) |
| COMMIT_CITED_UNRESOLVED | `:393` | r22 `:1078` — detail carries the token |
| COMMIT_CITED_NOT_ANCESTOR | `:394` | r23 `:1097` — 7-hex prefix in detail; 40-hex sha (`:1101`) |
| SCORECARD_ROW_MISSING | `:401`, `:404` | r10 `:958`; r10b `:968` (prose `\|` negative) |
| SCORECARD_PLAN_MISSING | `:409`, `:415` | r11 `:976`; r12 `:987` (past); r12b `:996` (far-future negative); r13 `:1002` (next); r14 `:1009` (strict) |
| LOG_ENTRY_MISSING | `:425`, `:428` | r15 `:1020` |
| COMMIT_MISSING | `:436`, `:441` | r16 `:1028`; r17 `:1034` (wrong N); r18 `:1040` (body marker negative) |
| TREE_DIRTY | `:451` | r26 `:1141` — `entries=6`, first-5-only |
| UNPUSHED | `:465` | r27 `:1157` — `ahead=1` exact |
| REPORT_UNTRACKED | `:477`, `:481`, `:495`, `:547`, `:551` | r28 `:1166` (untracked); r29 `:1176` (unpushed); rt2 `:1420` (tracked); rt6 `:1460` (outside, ×2 — duplicates pinned) |

(I) Within the enum family the meta-check is a strong coarse net — a declared kind that never
fires fails it regardless of *which* emission arm broke — and REPORT_UNTRACKED is the only
multi-arm kind (5 arms) with every arm statically covered.

**13.2 Row A projection — verdict paths.** (O) Four gate verdict families, four pin styles in
the suite:

- audit/close `ROUND_GATE: CLEAN|DRIFT (round=N lane=L checks=C errors=E warnings=W)` —
  `parseVerdict` is a **full-line anchored equality** (`:862-868`); all 10 call sites
  (`:879`–`:1311`) assert `v !== null`, so the line must match exactly, and fields are read
  individually (`checks=10/5/13` at `:882`/`:901`/`:1134`). Verdicts are read as the last
  non-empty stdout line (`:861`). Tighter CLEAN/DRIFT pinning than either measured case
  (kimi-census equality-pinned only the CLEAN line; surface-census pinned no line above a
  substring).
- tracked `… (mode=tracked checked=… errors=… warnings=…)` — inline full-line regexes
  (rt1 `:1411`, rt2 `:1426`; rt8 prefix-matches only, `:1481`).
- FAIL-CLOSED `ROUND_GATE: FAIL-CLOSED (TOKEN) detail` — **token only**: fcA pins the
  parenthesized token (`:1188`), fcB–fcF a bare `/TOKEN/` (`:1193`, `:1198`, `:1206`, `:1212`,
  `:1218`), rt3/rt5 `:1435`/`:1450`; the detail tail is unread except fcE's `exit 128` probe
  (`:1212`). This is where the pair's admitted "asserted stem, unasserted remainder" (D2/B10,
  §9) has a static echo — relocated to the refusal path.
- selftest `ROUND_GATE_SELFTEST: …` / `VERDICT: PASS` — shape + exact equality only
  (`:1399-1400`); counts unread (§13.5).
- `--json` — the whole top-level **key set by equality** plus per-check entry shapes
  (`:1254-1262`), contract string pinned — stronger than the pair's JSON handling.

**13.3 Row B projection — fail-closed arms.** (O) 7 tokens over 10 literal call sites
(`:460`, `:471`, `:488`, `:527`, `:531`, `:536`, `:644`, `:647`, `:652`, `:683`; `:656`
re-emits what runChecks returned):

| Token | Sites (O) | Fixture (O) |
|---|---|---|
| REPORTS_DIR_MISSING | `:527` (tracked), `:647` (main) | fcA `:1187`, jFc `:1278` — main site only |
| NOT_A_GIT_WORKTREE | `:644` | fcB `:1192`, fcC `:1197` |
| NO_CLOSED_ROUND | `:652` | fcD `:1205` |
| NO_FILED_REPORTS | `:536` | rt3 `:1434` |
| UPSTREAM_MISSING | `:460` (lane repo), `:488` (main repo) | fcE `:1211` — lane site only |
| MAIN_REPO_NOT_GIT | `:471`, `:531` (tracked) | fcF `:1217`, rt5 `:1449` |
| INTERNAL_ERROR | `:683` (catch-all) | **none** |

(I) 6/7 tokens are hand-asserted; `INTERNAL_ERROR`'s token — or the catch block around it
(`:641-684`) — can change with no fixture moving (named probe candidate). Two tokens carry a
second, **uncovered call-site species** (tracked REPORTS_DIR_MISSING; main-repo
UPSTREAM_MISSING, whose only fixture candidates are audit-mode runs that return before the
close block, `:446`) — §3's "the arm inventories behind the shared property are not the same"
observed statically inside one artifact. (O) The meta-check is **structurally blind** to this
family: fail-closed text output is the verdict line (`:617`), which `parseFindings` cannot
match — adding the tokens to `FINDING_KINDS` would not put them in `observed`. Coverage is
hand regexes only, and the checks assert the token, not the species: fcE's
`/no upstream|exit 128/` probe (`:1212`) cannot tell the two UPSTREAM_MISSING sites apart. The
fail-closed stderr diagnostic (`:615`) is read by no check.

**13.4 Row C projection — counts and floors.** (O) exact-count pins: `checks=10` (`:882`),
`checks=5` (`:901`), `checks=13` (`:1134`), `checked=2`/`excludedRound=5` (`:1414`,
`:1472-1473`); kind lists are compared by `JSON.stringify` equality (`:869-872`), so
membership, order, and multiplicity are pinned (rt6 expects the duplicate, `:1461`). (O/I) The
meta-check's own count is **one-sided**: `missing.length === 0` (`:1489`) with `observed.size`
only in a detail string (`:1491-1492`) that nothing asserts; since every kind literal the code
emits is an enum member (O: literal scan of the `add()` sites, `:342-551`), `observed ⊆ enum`
today — but the check cannot notice a stray emitted kind; only a fixture's exact kind list
could (I). (I) `REPORT_MIN_BYTES = 1024` (`:167`, read at `:345`): the suite straddles the
floor but never compares against the symbol — r4's `thinBytes < 1024` (`:913`) asserts the
fixture, not the constant. Static arithmetic (§13.10 #3): thin fixture 25 B; smallest non-thin
*read* report is r8's `fxMentions(10,'round-1')`, 1059 B. A single edit of the constant to any
integer in **[26, 1059]** changes no fixture verdict — the floor is *interval*-pinned, not
point-pinned. **Projected, not measured.** (I) `HISTORY_LIMIT = 1000` (`:168`): the cap
boundary needs >1000 commits — uncovered.

**13.5 Row D projection — reported, unread.** (O/I):

1. FAIL-CLOSED detail tails + stderr diagnostic (`:615`) — fcA–F pin the token (fcE also
   `exit 128`); the path/detail remainder and the stderr line are read by nothing.
2. Nested selftest summary — `ROUND_GATE_SELFTEST: \d+/\d+ pass` is shape-only and
   `VERDICT: PASS` equality (`:1399-1400`); the counts never.
3. `durationMs` — `typeof === 'number'`, value unread (`:1263`).
4. JSON `citations.mainProbeable`, `citations.unresolved`, `citations.notAncestor` — the
   text-side equivalents are pinned (r22/r23); these JSON fields are read by no check (reads:
   `checked` `:1264`; `external` `:1122`/`:1350`/`:1357`; `unverifiable`/`originProbeable`
   `:1374-1376`).
5. Text finding details are mostly kind-level: exact detail pins exist only where §13.1
   quotes them; r3's path, r7's message, r10's/r15's paths are unread.

**13.6 Row E projection — arms no fixture statically reaches.** (O fixture-set reads, (I)
classification; no run.)

1. `INTERNAL_ERROR` (`:683`) — the only declared token with zero fixture, and no meta-check
   to notice (§13.3).
2. tracked-mode `REPORTS_DIR_MISSING` site (`:527`) — token covered only via the main site.
3. main-repo `UPSTREAM_MISSING` site (`:488`) — no `--close` fixture pairs a lane upstream
   with a main repo lacking one.
4. env-lane invalid branch (`:277-279`) and input-validation siblings: `--round`
   non-safe-integer (`:256`), `dirValue`'s flag-like value (`:246`, e.g. `--repo --json`) —
   no fixture. The nested run's `KUMITATE_LANE: 'not-a-lane'` is a *valid* lane (hyphens
   allowed; §13.10 #2) and never reaches `parseArgs`' env validation because `--selftest`
   wins (`:635`).
5. `UFO_SRC` set-value branch (`:162-163`) — derived-origin fixtures force `UFO_SRC: ''`
   (`:1347`, `:1354`, `:1369`) and the nested run never resolves the default (`:294-296`); no
   fixture exercises a set env origin.
6. Documented readings with no pin: `--help`/`-h` as unknown flags (`:125-126`) — u1 pins
   `--bogus`, not `--help`; `--selftest` wins over `--json` (`:48`) — no fixture combines
   them; flag>env precedence is discriminated for reports-dir/lane (r45 `:1310`) but not for
   main-repo (an env-taken main repo would not move r45's audit verdict — I).
7. `citationTokens` range form (`:315-324`, split on `..`/`...`) — all fixture citations are
   single backticked tokens (`:1074`, `:1091`, `:1113`); the documented example range
   (`:106-107`) has no fixture behind it.

**13.7 Row F projection — coordinated edits.** Unmeasured, as §7: (I) a rename carried across
a kind literal + the enum + a fixture list keeps the meta-check and every check green; (O) the
prose inventories (`:66-98`, `:115-117`) are parsed by nothing, so code↔prose drift trips only
the fixtures that assert the drifted field (severity `warning` is asserted at `:981`, `:1053`;
the header's own table never); (I) a coordinated swap of which UPSTREAM_MISSING site emits the
token is invisible to every token-level assert (§13.3). The method still stops at single-edit
reads.

**13.8 Row G projection — behavior predicates.** (O) the densest family, as in both measured
cases: round-name regex pinned **both directions** (r8/r9); plan window three-sided (r12/r12b/
r13); strict promotion (r14 `:1009`, r20 `:1058`); tracked blindfold (rt8 `:1478`); hermeticity
under a polluted env + bogus dir flags (`:1381-1404`); 40-hex citation boundary (`:1101`).
(I) no predicate gap emerges from the static read — the uncovered set of §13.6 is refusal/usage
species and negative-branch combos, not predicates.

**13.9 Projection unknowns (PU).**

- PU1 — all of §13 is static; the interval statement (13.4) is a hypothesis until a mutant
  lane cuts it.
- PU2 — "no fixture reaches X" is a reading of the fixture set at this sha; fixtures grow, and
  any §13.6 item can retire without a code change.
- PU3 — whether `INTERNAL_ERROR` is reachable by *any* fixture is unknown (catch-all of last
  resort); its absence may be by design, not omission.
- PU4 — no width or kill-rate reading: nothing here estimates what the 14/14 coverage would
  survive under mutation (matrix §4's width caveats unchanged).
- PU5 — one artifact, one lane: nothing admitted anywhere; the PROVINCE two-lane bar is
  untouched.

**13.10 Projection spot-checks (live, read-only, 2026-10-14; no gate execution; kumitate tree
porcelain-empty after; no scratch files).**

1. **Pin** — `sha256sum kumitate-shokunin/scripts/round-gate.mjs` → `f890e277…a834d3e9`;
   `git -C kumitate-shokunin rev-parse --short HEAD` → `175de6ba`; `git status --porcelain`
   → empty; `wc -l` → 1511.
2. **Meta-check + branch map** — `grep -c "check('"` → 60; the enum at `:171-176` and the
   meta-check at `:1487-1493`; `grep -n` over the seven token names + `failClosed(` → the 10
   call sites of §13.3; `INTERNAL_ERROR` only at `:117` (doc) + `:683`; lane regex
   `^[A-Za-z][A-Za-z0-9-]*$` accepts `not-a-lane` (node, §13.6 #4).
3. **Floor arithmetic** — the suite's report templates re-evaluated with `Buffer.byteLength`
   via `node -` (no file written): `fxThin(5)` = 25 B; `fxMentions(10,'round-1')` = 1059 B
   (r8's report); all other read reports 1119–2100 B. Interval [26, 1059] stands (§13.4).## Errata (round 5) — VER-T1 cross-check landing (append-only)

Applied 2026-10-14 by lane T5-2; scope: this file only; nothing above this block
is edited. Source: **VER-T1**, the round-4 independent cross-check of row E
(verdict: row E CONFIRMED — exactly 1 unreached-arm instance of 20; scratch
`/tmp/w4-ver-t1-crosscheck/` + `/tmp/w4h-ver-t1-mut/`; cited in the round-4
`LOG.md` entry). Entry **E3**.

E3 (precision — §6 chmod enumeration completeness). §6's B5 paragraph states
"the only chmod sites are `:521-588`, `:704-717`, `:768`" (live line 185). That
enumeration is incomplete. O — re-measured live by T5-2 on the pinned bytes
(`kagi-shokunin/corpus/surface-census.sh` @ sha256 `275d8294…53009f`, held
before and after this append): `grep -n chmod` finds **15** sites — `:521`,
`:546`, `:571`, `:588`, `:608`, `:654`, `:704`, `:706`, `:707`, `:708`, `:709`,
`:713`, `:715`, `:717`, `:768`. The two omitted sites — `:608` (`chmod 600
"$S/op.env"`) and `:654` (`chmod 600 "$S/present.env"`) — sit inside the
`verbs()` probes (`:465-693`), between the cited ranges. Corrected enumeration:
**`:521-588`, `:608`, `:654`, `:704-717`, `:768`**. The load-bearing conclusion
is unchanged: no site touches the exec row's file or strips +x — the only
`exec`-kind census row is `$HOME/.local/bin/the-janitor` (built at `chmod 755`,
`:707`; `-x ` occurs once, `:214`, inside the arm B5 deletes) — so B5 stays
fixture-absent/unreached and every verdict cell in §0-§9 stands. (The same
incompleteness was independently reached by AUD-T1's audit of this file, its
finding F2 — cited for the record.) Recorded here per the append-only discipline
rather than editing §6; §12 unchanged.

Companion VER-T1 erratum ("unreached" JS wording scope) lands in
`knowledge/mutation-case-kimi-census.md` (E2 there).

## Errata — round 16: §13 projection measured (append-only)

§13 was a projection ("no mutant was cut", `:300-303`; PU1 `:475`). Round 16
cut ten mutants on the same bytes (`f890e277…d3e9`, rev `364f1d5`); see
`mutation-case-kumitate-round-gate.md`. Measured: §13.2 full-line vs prefix
pins (A1 and A3 killed, rt8 green under A3); §13.3 species asymmetry (B1
killed, B2 survived); §13.4 interval [26,1059] (1059 survived, 1060 killed);
§13.4 one-sided meta-check (CKIND survived); §13.5 #1 detail tail (A2
survived); §13.6 #5 `UFO_SRC` (E1 survived). The ten pre-registered
predictions all held.

Wave-1 re-reads of §13 at the same bytes (RGMatrix, RGSource1) found these
corrections; they stay readings, not measurements:

- The meta-check equality is at `:1490` (block `:1487-1493`), not `:1489`.
- §13.6 omits five arms that no fixture reaches: `:401`, `:425`, `:436`,
  `:477`, and the main-external citation branch `:377-378`. So §13.1's "every
  arm statically covered" for REPORT_UNTRACKED is false (`:477`).
- `:370` is false: rt3 (`:1436`) pins the NO_FILED_REPORTS detail tail.
- `:445-446` is false: `parseArgs` (`:630`) runs before the selftest dispatch
  (`:635`), so the nested `KUMITATE_LANE` does reach env validation.
