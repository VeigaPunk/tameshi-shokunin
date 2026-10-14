# Mutation case — kumitate `scripts/claims-check.mjs` member-claims gate (T8-2)

Run date 2026-10-14, sweep 19:12:43Z. Lane: **T8-2**, tameshi round 8 — the wave's
**sixth case** (the fifth, T8-1, was in flight at this write; §5 E4). Substrate
kumitate-shokunin **read-only**: the sweep target is a byte copy materialized from the
repo's git object store, every fleet tree is untouched, and **this note is the only fleet
file written by this run** (the corpus/README row and the `LOG.md` entry fold in at lane
review, as in rounds 5/6). No external site contacted; no secret file read; no live
substrate read — the gate's `--selftest` stats no live path at all (§0).

**Pin (the sweep revision is a git blob, not an mtime).** `kumitate-shokunin/scripts/
claims-check.mjs` @ sha256 `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b`,
48,265 B, 926 lines (925 newlines; the final line `if (isEntry) main();` carries no
trailing newline — `tail -c 1` = `;`), git blob `fae4bbcd158c527e70d8a69bcd3add372ed99c2e`
at kumitate HEAD `175de6bab` (short `175de6b`); `git show HEAD:scripts/claims-check.mjs |
sha256sum` = the pin; the live working-tree file `cmp`s identical to the materialized blob
and the tree is porcelain-empty before and after the whole run. The pin equals the
standing pin this fleet already records twice — `gates-survey-kumitate.md` K-R2-1
(`e9a21b441f1216bf`) and `fleet-kill-rate-ledger.md` §3 — so this sweep is at the gate's
unchanged revision: target `current`, no drift incident ([O]; contrast tsukuroi I1, mado I1).

**Method.** `tameshi-shokunin/tools/mutate-and-run.sh` @
`cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` (1,341 L; the r7-1 leg-ledger
revision; its `MUTATE_TOOL` line carries the pin), suite command
`node "$MUTANT" --selftest`, target `/tmp/w8-t8-2-claims/claims-check.pinned.mjs` (the
materialized blob; the harness's own restore proof is over that copy, and the fleet file
was re-hashed after the run). Ten single-edit defects; `count(@old)==1` for all ten asserted
before any suite run (this lane's `t8_2_check.py` → `all unique`, then again by the
harness's preparation step); control run first. Scratch `/tmp/w8-t8-2-claims/`; host: node
v24.21.0, bash 5.3.15, python 3.14.7, kernel 7.2.3-arch1-3.

Anchors: **O** = observation (command output, file:line, re-quoted measured cell); **I** =
inference; **U** = unknown. `claims-check.mjs:NNN` = the pinned bytes above.

## 0. Gate choice, method, headline

**Why this gate.** The assignment names it, and the ledger's §3 queue entry sits at
`claims-check | 39 | e9a21b441f1216bf | unmeasured; hermetic; expect low survivor count`
(one of the ledger's five unmeasured kumitate gates; the dispatch's framing is "the one
kumitate gate not yet measured"). The artifact is a
925-line (926-line) JS gate (`contract kumitate-claims-v1`, `:69`) that re-derives each
covered SCORECARD row's claim against the origin tree: it resolves the row's corpus notes,
derives member sections, and fails on 12 finding kinds (`:109-115`) and 5 fail-closed arms
(`:117-120`); exit map `0 MATCH · 1 DRIFT · 2 fail-closed · 64 usage` (`:55`, `:139`).

**Hermeticity (O).** The suite builds all fixtures under
`mkdtempSync(join(tmpdir(), 'kumitate-claims-selftest-'))` (`:600`) and removes them in the
`finally` (`:853-855`); every case **spawns the gate itself** as a subprocess
(`runClaims` `:581-586`, `TOOL_FILE = fileURLToPath(import.meta.url)` — so the mutant is
exercised end-to-end, CLI included); `--selftest` wins before the `--src` default is ever
resolved (`:903`), and the suite's own case asserts every fixture root is under `tmpdir()`
(`:823-826`). Re-run here as the gate's documented outside-in acceptance: `UFO_SRC=
/nonexistent node claims-check.pinned.mjs --selftest` → `CLAIMS_SELFTEST: 39/39 pass` /
`VERDICT: PASS`, rc 0 — an env-poisoned run changes nothing.

**Method (the r2/r3/r5/r6 replica, through the tool).** Control first; each defect = ONE
exact replacement on a fresh copy of the pinned pristine; per-mutant evidence is the full
suite output (`work/evidence/D*.out`), the aggregate `work/results.tsv` records verdict,
exit, duration and the mutant sha256. The suite prints FAIL lines only (`:857-862`), so
per-case evidence is the mutant's FAIL lines plus the source anchors.

- O: control — `CLAIMS_SELFTEST: 39/39 pass`, `VERDICT: PASS`, exit 0, 673 ms.
- O: **kill rate 7/10 (70 %)**; survivors D7, D8, D9; **0 inconclusive** — all 11 runs
  produced a definitive suite verdict, and the executed count held at `39` on every run
  (`CLAIMS_SELFTEST: n/39 pass` in all eleven).
- O: cost — 11 runs in 8.0 s wall (control 673 ms; mutants 668–775 ms) against a 300 s
  per-run timeout; ~0.73 s/run. The suite spawns itself once per case, so a run is 39 node
  processes; fast enough that a re-sweep is a sub-10-second operation.
- O: restore — `MUTATE_RESTORE: OK (target-sha256 before=e9a21b44… after=e9a21b44…
  pristine-sha256=e9a21b44…)`; the fleet file re-hashed after the run = `e9a21b44…`,
  kumitate `git status --porcelain` empty.
- Composition, stated before the run: **6 kill-aimed** (D1–D6, aimed at asserted
  surfaces) + **4 hole-aimed** (D7–D10, aimed at seams predicted unasserted). Measured:
  **6/6 and 1/4**. The rate is composition-bound (tsukuroi E3) — the 70 % is six
  asserted-surface kills (6/6) plus one hole-aimed probe that turned out to be enforced
  (D10).
- O: **pre-registration** (`/tmp/w8-t8-2-claims/predictions.txt`, written before any run):
  9/10 verdicts and 8/10 failing-case counts (§5 E1 — the miss is D10, recorded, not
  smoothed).

## 1. Kill-rate table

| # | Defect class | Injected defect (site on the pinned rev) | Exit | Suite line | Verdict | Failing cases |
|---|---|---|---|---|---|---|
| — | control | unmutated pristine copy | 0 | `39/39 pass` / PASS | green | 0 |
| D1 | verdict token | `CLAIMS: MATCH (` → `CLAIMS: OK (` (`:426`) | 1 | `30/39 pass` | **killed** | 9 |
| D2 | exit map | `return verdict === 'MATCH' ? 0 : 1;` → `return 0;` (`:538`) | 1 | `25/39 pass` | **killed** | 14 |
| D3 | predicate (strict) | `drift: errors > 0 \|\| (Boolean(strict) && warnings > 0)` → `… \|\| warnings > 0` (`:421`) | 1 | `35/39 pass` | **killed** | 4 |
| D4 | boundary (reached) | `else if (hits.length > 1 &&` → `> 2` (`:248`) | 1 | `37/39 pass` | **killed** | 2 |
| D5 | inverted condition | anchor liveness requires *blank* endpoints: both `!== ''` → `=== ''` (`:378`) | 1 | `18/39 pass` | **killed** | 21 |
| D6 | reported field | JSON `schema: CONTRACT` → `'claims-check-v0'` (`:523`) | 1 | `38/39 pass` | **killed** | 1 |
| D7 | cap unreached | `shown.slice(0, 6)` → `slice(0, 5)` (`:431`) | 0 | `39/39 pass` | **survived** | 0 |
| D8 | assert-blind threshold | symbol floor `t.length >= 3` → `>= 2` (`:382`) | 0 | `39/39 pass` | **survived** | 0 |
| D9 | unreached arm | guard drops `unresolved` from the sum (`:315`) | 0 | `39/39 pass` | **survived** | 0 |
| D10 | candidate order | `SRC_CANDIDATES` entries swapped (`:79-80`) | 1 | `37/39 pass` | **killed** | 2 |

By class: verdict token 1/1 · exit map 1/1 · predicate 2/2 · boundary (reached) 1/1 ·
reported field 1/1 · candidate order 1/1 · cap unreached 0/1 · assert-blind threshold 0/1 ·
unreached arm 0/1.

Kill mechanisms (O, verbatim from `work/evidence/D*.out`; failing counts = `grep -c '^FAIL '`):

- **D1** (9): the five exact-equality green/MATCH verdict lines (`:630`, `:759`, `:763`,
  `:769`, `:832`) plus the four `includes('CLAIMS: MATCH')` cases all move — e.g. green
  reads `last=CLAIMS: OK (rows=2 yes=2 notes=2 sections=2 adv=0)`. The verdict token is
  the suite's most-shared assert.
- **D2** (14): every DRIFT case asserts `status === 1`; with `return 0` the suite reads
  e.g. `exit=0 last=CLAIMS: DRIFT (MEMBER_COUNT_DRIFT row=S1 declared 2 members, found 1
  distinct sections)` — the mutant prints DRIFT while exiting 0. The widest kill after D5.
- **D3** (4): the three warn-only cases (`MEMBER_COUNT_SUSPECT`, `SECTION_FILE_NOT_MEMBER`,
  `ROW_NO_SECTIONS`) expect MATCH exit 0 and now read `exit=1 last=CLAIMS: DRIFT ()` (the
  non-strict display filter shows no error parts), plus the row/verdict agreement case.
  The `--strict` promotion is a one-line arm guarded from both sides.
- **D4** (2): the two-hit ambiguity fixture now falls through to the bare-stem arm —
  `last=CLAIMS: DRIFT (NOTE_MISSING row=S1 fx-a does not resolve to a corpus note)`,
  kinds `[NOTE_MISSING,ROW_NO_SECTIONS]` where `[NOTE_AMBIGUOUS,ROW_NO_SECTIONS]` was
  asserted — **and the kind-coverage meta-check fires**: `FAIL every finding kind fired by
  the suite / unfired=[NOTE_AMBIGUOUS]`. The meta-check is a kill channel, not just a
  census (survey §8.1 said arm-coverage detectors are not mutation controls; measured: it
  killed a mutant too).
- **D5** (21): the widest kill measured on this gate. With liveness inverted, every
  non-blank endpoint reads dead: `green` becomes
  `last=CLAIMS: DRIFT (SECTION_DEAD_ANCHOR row=S1 scripts/a.mjs — own-file anchors 3-3 are
  dead; …)`, and even the boundary case (`lastline exit=1 past-eof exit=1`) loses its
  one-directional discrimination.
- **D6** (1): only the `--json` case reads the schema id — `json=1/1 text=1/1
  verdict=DRIFT` fails on `j.schema === CONTRACT`.
- **D10** (2): the swapped candidate order is caught twice — (a) the "new path wins when
  BOTH exist" case, because its legacy candidate is an **empty** directory
  (`mkdirSync(join(home,'Projects','origin-work','ufo-fsd-alpha'))`, `:767`), so resolving
  it first yields `SECTION_FILE_UNRESOLVED row=S1 scripts/a.mjs does not resolve under
  --src`; (b) the "both absent" case, whose FAIL-CLOSED detail now names the
  `origin-work` path where the new path was asserted (`--src …/Projects/origin-work/… is
  absent`). The case *name* claims an order property the byte-identical-fixture reading
  could not see — measured, the suite does discriminate.

## 2. Survivor analysis and non-equivalence probes

All three survivors are real behaviour differences, each demonstrated on an input the
suite's own fixtures never build (`probe/probes.py` → `probe/non-equivalence.txt`):

- **D7 — cap unreached: `shown.slice(0, 6)` → `5`.** O: 39/39 PASS. No in-suite run shows
  more than **3** findings (max kinds-array length across all eleven evidence runs = 3),
  so the cap is never reached in-suite; the `+N more` tail is asserted by nothing. Probe
  P7 (one live section + seven unresolved headings = 7 error findings): pristine
  `CLAIMS: DRIFT (… miss1 … miss6; +1 more)` vs D7 `(… miss1 … miss5; +2 more)` — the
  truncation point moves and the survivor count in the tail is wrong by one. This is the
  kimi-D2 shape (`findings.slice(0, 6)` → `5`) reproduced on a sibling gate, same cap
  value, same seam, independently measured.
- **D8 — assert-blind threshold: symbol floor `>= 3` → `>= 2` chars.** O: 39/39 PASS. The
  case is *named* `symbol threshold: a 2-char backticked token does not count as a symbol`
  (`:790-794`) but asserts only `status === 1` and `kinds === 'SECTION_NO_SYMBOL'`; its
  fixture's `AB` token is absent from the file, so under both floors `SECTION_NO_SYMBOL`
  still fires — the floor semantics are invisible to the case. Probe P8 (2-char `AB`
  *present* in the section's file): pristine `exit=1 CLAIMS: DRIFT (SECTION_NO_SYMBOL row=S1
  scripts/probe-sym.mjs — no backticked symbol is verbatim in the file)` vs D8 `exit=0
  CLAIMS: MATCH (rows=1 yes=1 notes=1 sections=1 adv=0)` — a **verdict flip**. New shape
  for the arm-class matrix: not "cap unreached", not "fixture-absent arm", but a
  *threshold an existing case is named for and cannot see*.
- **D9 — unreached arm: the sum drops `unresolved` (`:315`).** O: 39/39 PASS. The guard
  `claimed + explicit + unresolved === 0 → NOTE_MISSING 'the covered cell names no
  resolvable corpus note'` is never entered by any fixture (every case's covered cell
  yields a claimed note, an explicit path, or has sections). Probe P9 (covered cell
  `yes — round-11-reading`, one bare stem that resolves nowhere): pristine `exit=1 CLAIMS:
  DRIFT (NOTE_MISSING row=S1 round-11-reading does not resolve to a corpus note)` (1
  error) vs D9 `… ; NOTE_MISSING row=S1 the covered cell names no resolvable corpus
  note)` (2 errors; `--json` `"errors": 1` → `2`). Same verdict, contradictory duplicate
  finding — the shape the guard's own comment says it exists to prevent
  (`:313-314`: "double-reporting muddies the verdict").

Shared class: two of the three (D7, D8) change a claim no assertion reads (a truncation
tail, a threshold's semantics), and one (D9) is a branch no fixture reaches — the matrix's
two admitted survivor families (§4). D8 is the first measured instance of its sub-shape.

## 3. What the 39-case suite protects — and does not

**3.1 Asserted surface (O: static read of the suite `:599-864`; the FAIL-only printing
means the case labels come from source, not stdout — survey §5.B).** 35 literal `check(`
sites (`grep -c "check('"` = 34 single-quoted + 1 template label in the 5-arm loop
`:743-749`) → **39 executed checks**. The vocabulary each check may assert:

- exit code, and the last stdout line through `ok()` (`:613-621`): `status === expected`
  **and** `verdictLine(run).includes(needle)` **and** — for most checks — the **kind list
  by `JSON.stringify` equality** (`kinds()` `:593-597` parses the `CLAIMS  ` finding
  lines). The kind-list equality is this suite's strongest and most-used channel.
- exact whole-line equality for the MATCH verdict in five checks (`GREEN_MATCH` `:756`,
  asserted `:630`, `:759`, `:763`, `:769`, and the totals line `:832`);
- fail-closed: `status === 2` + `includes('FAIL-CLOSED (TOKEN')` for all 5 declared arms
  (`:743-749`), one SRC-arm detail string (`:777-778`);
- usage: 64 + `usage:` for `--bogus`, `--row Z9`, missing `--self` value; `-h` → 0
  (`:785-817`);
- row lines partially: `ROW S1` presence (`:713`) and `form=topic` / `sections=0` /
  `adv=1` includes (`:830-834`);
- `--json` internal consistency: totals equal the text `SUMMARY:` regex (`:720-728`);
- the two coverage meta-checks over `FINDING_KINDS` / `FAIL_CLOSED_KINDS` (`:849-852`).

**3.2 Read by nothing (O/I).** The DRIFT line's `+N more` tail and its arithmetic (D7);
the symbol floor's semantics (D8, and probe P8 flips the verdict); the
`NOTE_MISSING` detail split — "an explicit path that resolves nowhere" vs "a bare stem
that resolves nowhere" produce the same kind, and no case reads the detail (unmeasured
mutant, U2); the per-row `ROW` line's padding/format beyond the two includes; the
`SUMMARY:` line itself is read only by the `--json` case's regex; no case runs
`--strict --json` together; `--scorecard` is exercised only as a *missing* relative path;
`--row` is never passed twice; `walkFiles`' prune list (`:157`) and `inFamily`'s glob/dir
arms (`:261-273`) have no fixture.

**3.3 Threshold/arm inventory.** Measured gaps: the `+N more` cap (D7), the symbol floor
(D8), the unresolved-sum guard (D9). Named, not measured: the fail-closed `return 2` → `1`
edit (the arms' cases assert exit 2, so it is expected to die; unmeasured, U1); the
member-count arms (dedicated cases exist: drift error, suspect warn, drop-one) — a count
mutant was not cut on this gate (U3); `MEMBER_COUNT_SUSPECT`'s boundary at
`distinct == declared` is unmeasured.

**3.4 Suite mechanics.** 0 abstentions (39/39 execute); every case spawns the gate as a
subprocess, so the mutation is exercised through the CLI, not by import; the two
meta-checks are live tripwires (D4 measured); the gate's own comment at `:819-822`
documents the outside-in acceptance (env-poisoning) and the only in-source mutation
mention is the case *name* at `:827` (`… (kind-blind mutants fail here)`), which is the
summarised probe this sweep supersedes with a measured table.

## 4. Cross-case comparison (arm-class matrix rows A–G, fleet axes)

Sequence: **80 % (kimi JS r2) · 80 % (kagi bash r3) · 60 % (tsukuroi bash r5) · 40 %
(mado bash r6) · 70 % (claims JS r8)**. Composition binding holds: this 70 % is 6/6
kill-aimed + 1/4 hole-aimed (tsukuroi E3).

- **Row A — Verdict paths.** Fifth gate measured: the asserted stem is protected again —
  D1 dies on 9 checks, D2 on 14. This gate pins the MATCH line by whole-line equality in
  five checks and the DRIFT line by prefix + kind-list equality; the only unread remainder
  is the `+N more` truncation tail. (O) **Convergence, independently measured:** kimi
  D2 and this case's D7 are the same edit (`slice(0, 6)` → `slice(0, 5)`) on the same cap
  value in two of kumitate's own gates, and both survive; two sweeps, four rounds apart,
  same hole. That is the strongest single datum in this note for row D and it is not a
  re-quote — both cells were measured.
- **Row B — Fail-closed arms.** Not probed in this sweep (U1): the 5 arms carry cases
  (exit 2 + token) and a coverage meta-check, but a 2→1 mapping mutant was not cut here.
  The suite's fail-closed shape is `token + detail` with the detail largely unread —
  the asserted-stem/unasserted-remainder property relocated, again, to the refusal path
  (kimi B / round-gate projection echo).
- **Row C — Counts.** D4 is a boundary mutant whose fixture sits exactly on the boundary
  (2 hits vs `> 1`) — killed, boundary-reached, both by the case and by the kind-coverage
  meta-check. D8 is a threshold mutant whose fixture cannot reach the threshold's
  semantics — survived, with a verdict-flipping probe. Cap reachability and threshold
  reachability stay per-site facts (tsukuroi row-C amendment holds).
- **Row D — Reported-but-unasserted surfaces.** Third JS instance (kimi D2/D10, this D7)
  plus D8/D9. The family's repair shape differs by site: D7 asserts the tail, D8 needs
  the threshold pinned by value (or a fixture that reaches it), D9 needs one fixture for
  the prose-only cell.
- **Row E — Unreached arms.** **First JS instance measured** (D9). The tsukuroi reading
  ("two bash instances, still zero JS instances, bash-weighted and proposed") is amended:
  the class now has a JS instance, in a suite whose arm-coverage meta-checks prove
  *reachedness* only for the kinds/arms tables that mutants D4/D8 sit outside of. The
  class is per-arm, as before — two of this gate's own arms (fail-closed mapping,
  member-count equality) are simply unprobed here.
- **Row F — Coordinated edits.** Unmeasured (single-edit experiment; U6).
- **Row G — Behavior predicates.** D5 (inverted liveness) killed 21/39 — the second
  widest measured bash/JS kill after tsukuroi B6's 21/26; D3 (predicate widening) killed
  4. Predicate edits that an assert reads die, again.

**Fleet axes table (fifth data point).**

| Axis | JS r2 (kimi) | bash r3 (kagi) | bash r5 (tsukuroi) | bash r6 (mado) | JS r8 (claims) |
|---|---|---|---|---|---|
| artifact | `kimi-census.mjs` 896 ln | `surface-census.sh` 886 ln | `tsukuroi-census.sh` 977 ln | `mado-verify.sh` 1,099 ln | `claims-check.mjs` 926 ln |
| suite grammar | `n/43 pass` + FAIL labels | `ok/bad-case` + `SELFTEST (n/16)` | `PASS/FAIL <label>` + `(26 cases…)` | `MADO_SELFTEST: n/28` scenarios | `CLAIMS_SELFTEST: n/39 pass`, FAIL-only printing |
| abstention | none | 2/16 skip | none | none | none (0/39) |
| kill rate (composition) | 8/10 (10 kill) | 8/10 (10 kill) | 6/10 (6+4) | 4/10 (4+6) | **7/10 (6+4)** |
| widest kill | 16/43 | 3/16 | 21/26 | 3 assertions (D2/D4) | 21/39 (D5) |
| survivors | D2 cap, D10 constant | B5 arm, B10 summary field | B7 cap, B8 usage exit, B9 fields, B10 arm | D3, D5, D7, D8, D9, R1 | D7 cap, D8 threshold, D9 arm |
| restore pin | before=after | before=after | moved by owner (I1) | before=after | **before=after `e9a21b44…`** |
| cost | 11 runs / 7.0 s | 11 runs / 11.0 s | 11 runs / 19.6 s | 11 runs / 5.26 s | 11 runs / 8.0 s |

## 5. Calibration and errata (append-only)

- **E1 — pre-registration: 9/10 verdicts, 8/10 failing-case counts.** Misses, recorded:
  (a) **D10 predicted SURVIVED, measured KILLED** — my reading assumed the "both
  candidates exist" fixture built identical source trees in both candidate paths; in fact
  the legacy path is an **empty** directory (`:767`), so the order is observable, and the
  both-absent case's SRC detail path adds a second failure. The case name's claim *is*
  enforced; the error was mine, in the safe direction (a hole-aimed probe turned out
  covered). (b) **D4 predicted 1 failing case, measured 2** — the kind-coverage
  meta-check (`every finding kind fired by the suite`) also fires; a calibration datum
  about the suite, not about the mutant. All other eight counts held exactly (9/14/4/21/1
  and 0/0/0).
- **E2 — new measured shape: the assert-blind threshold (D8).** The case named for the
  symbol floor cannot see the floor because its fixture's 2-char token is absent from the
  file — the assertion pins "a finding fired", not "the floor is 3". P8 turns it into a
  verdict flip. Distinct from the tsukuroi cap shape (unreached value) and the mado D9
  one-directional assert (a direction never exercised): here the *direction is exercised*
  and the boundary value is still unread. Accepted as a probe candidate family; not
  generalized beyond this instance.
- **E3 — embedding follow-up (not an edit from this lane).** The harness's `--regression`
  at `cf41efaa…` carries the four ledger legs (cases=4, all PASS; §6); this case's table
  and spec are **not** embedded. Per write scope (this file only) and PROVINCE
  (sibling-owned tools), embedding is recorded as a follow-up for the lane that owns
  `tools/mutate-and-run.sh`: target pin `e9a21b44…`, suite `node "$MUTANT" --selftest`,
  recorded table §1, spec §8.
- **E4 — position in the wave (O, no cell depends on it).** This is the wave's sixth
  case; the fifth (T8-1, kagi `checklist-run.sh`) was in flight at this write — its
  scratch `/tmp/w8-tameshi-t81/` held `pristine-checklist-run.sh` and a sweep log, with no
  note landed at my pin-check; by the end of this run it had landed as the untracked
  `corpus/knowledge/mutation-case-kagi-checklist.md` (365 L, self-identifying as "the fifth
  fleet mutation case") [O]. No cell of this note depends on it; any cross-check is lane
  review's. The ledger's §1 still carries four rows; its own cadence (round 7/8) appends
  the fifth and sixth — not this file.
- **E5 — composition binding (restated per tsukuroi E3).** 70 % with composition
  "6 kill-aimed (6/6) + 4 hole-aimed (1/4)" is not comparable to any prior rate without
  its split; the ledger's §3 projection for this gate ("expect low survivor count")
  measured 3 survivors — exactly the population's median (2, 2, 4, 6 behind it), so the
  projection is neither confirmed nor refuted: the count lands mid-population, stated as
  measured, alone.

## 6. REGRESSION status (the harness's own gate)

- O: `bash tools/mutate-and-run.sh --regression --workdir /tmp/w8-t8-2-claims/regression`
  at 19:14:16Z, tool `cf41efaa…` →
  `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0,
  46 s wall. Legs, materialized from their repos' object stores (pin verified inside the
  tool): `js-kimi-census` `83016d45…` @ kumitate `175de6b` 8/10 flips=0;
  `bash-surface-census` `275d8294…` @ kagi `fecee87` 8/10; `bash-tsukuroi-census`
  `084951be…` @ tsukuroi `165307fe` 6/10; `bash-mado-verify` `d7edaab4…` @ mado `eead56b2`
  4/10 — every leg `match=10/10 flips=0`.
- O: **this case's table is not embedded**, so the §1 kill-rate claim does not carry a
  `REGRESSION` line over itself; follow-up per E3. (This is the same state the mado note
  recorded at the pre-r7-1 tool: embedding needs an edit to the tool.)

## 7. Unknowns

- **U1** — the fail-closed exit-map edit (`return 2` → `1` at `:450`) was not cut; the 5
  arms' cases make it expected to die, but that is a reading, not a measurement. Same for
  the `--src` SRC-detailed arm beyond the one string asserted.
- **U2** — the `NOTE_MISSING` detail split (explicit unresolved path vs bare unresolved
  stem) is unmeasured; both produce the same kind, so a detail-only mutant is predicted to
  survive — predicted, not swept.
- **U3** — no count mutant on this gate: the member-count equality (`!==`) and the
  `MEMBER_COUNT_SUSPECT` boundary (`<` at equality) are unmeasured.
- **U4** — live-tree sensitivity is nil by construction (`--selftest` resolves no live
  path; the poison pulse confirms), and nothing here measures whether the gate's verdicts
  about the *real* origin tree are right.
- **U5** — one host, one toolchain (node v24.21.0, 2026-10-14); timings and the 70 % are
  not a cross-host claim.
- **U6** — coordinated edits (matrix row F) unmeasured; `--strict --json`, multi-`--row`,
  and relative `--scorecard` resolution combinations are unprobed.
- **U7** — this sweep's pin is the ledger's recorded pin today; whether the ledger's
  cadence re-verifies it later is its own mechanism, not measured here.

## 8. Reproduce

Scratch `/tmp/w8-t8-2-claims/` (all evidence lives here; the fleet holds only this note):

```
claims-check.pinned.mjs   byte copy of git blob fae4bbc… @ 175de6b (sha256 e9a21b44…)
predictions.txt           pre-registration, written 19:13Z before any suite run
spec/claims-check.defects.spec   the 10 exact edits
spec/t8_2_check.py        count==1 / unescape pre-check (mirrors the harness prep)
sweep.log                 full harness transcript; work/ = mutants + evidence/{control,D1..D10}.out
work/results.tsv          per-defect verdict/exit/duration/mutant-sha256 (all 10 lines)
probe/probes.py           the three survivor probes (+ P9b --json); probe/non-equivalence.txt
regression.log            the harness's own four legs (PASS, 19:14:16Z)
```

Commands (in order; O):

```
cd /home/vgpnk/Projects/shokunin
git -C kumitate-shokunin show 175de6b:scripts/claims-check.mjs > /tmp/w8-t8-2-claims/claims-check.pinned.mjs
sha256sum /tmp/w8-t8-2-claims/claims-check.pinned.mjs kumitate-shokunin/scripts/claims-check.mjs   # both e9a21b44…
python3 /tmp/w8-t8-2-claims/spec/t8_2_check.py /tmp/w8-t8-2-claims/spec/claims-check.defects.spec /tmp/w8-t8-2-claims/claims-check.pinned.mjs   # all unique
bash tameshi-shokunin/tools/mutate-and-run.sh \
  --target /tmp/w8-t8-2-claims/claims-check.pinned.mjs \
  --defects /tmp/w8-t8-2-claims/spec/claims-check.defects.spec \
  --suite 'node "$MUTANT" --selftest' \
  --workdir /tmp/w8-t8-2-claims/work --label claims-check.mjs --tail 14
python3 /tmp/w8-t8-2-claims/probe/probes.py
bash tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /tmp/w8-t8-2-claims/regression
sha256sum kumitate-shokunin/scripts/claims-check.mjs   # e9a21b44… (unchanged; tree porcelain-empty)
```

The ten edits, each applied once to a fresh copy (site line on the pinned bytes; mutant
sha256 for byte-identity; every mutant differs from the pristine in exactly the edited
line(s) — the harness's single-edit guarantee):

```
D1  :426   `CLAIMS: MATCH (rows=${totals.rows}            9f5b4b58f7efbd05…
D2  :538   return verdict === 'MATCH' ? 0 : 1;            4fd34e050f6ed02a…
D3  :421   drift: … || (Boolean(strict) && warnings > 0)  321e860721fb9a80…
D4  :248   else if (hits.length > 1 &&                    f7feb1fdd303e724…
D5  :378   && lines[a-1].trim() !== '' && lines[b-1].trim() !== ''   b38a5254d88ecb7d…
D6  :523   schema: CONTRACT, contract: CONTRACT,          1de6e95b65293abb…
D7  :431   shown.slice(0, 6)                              f694e2328902b7a9…
D8  :382   && t.length >= 3);                             4f1989fe9089ae0b…
D9  :315   && claimed.length + explicit.length + unresolved.length === 0)   7b011c9aa3a91516…
D10 :79-80 join(homedir(),'Projects','ufo-fsd-alpha'), + the legacy line, swapped   2c7fecd9ca8156ca…
```

Sensitivity checks expected from the note alone: P7 pristine `… miss6; +1 more` / D7
`… miss5; +2 more`; P8 pristine `SECTION_NO_SYMBOL` DRIFT exit 1 / D8 `CLAIMS: MATCH`
exit 0; P9 pristine 1 error / D9 2 errors (`--json` 1 → 2).

**Spot-checks (three cited refs re-read on the pinned bytes; sha re-verified `e9a21b44…`
before and after).** (1) `:421` → the strict-drift disjunction; `:426-427` → the MATCH
template (`rows/yes/notes/sections/adv`); `:538` → `return verdict === 'MATCH' ? 0 : 1;`.
(2) `:241-251` → the `asserts`/`isExplicit` split and the `hits.length` arms;
`:313-317` → the guard comment and the sum, D9's site; `:377-380` → the liveness predicate
with both `!== ''` endpoint tests, D5's site; `:382` → the symbol floor, D8's site;
`:431` → the cap, D7's site. (3) `:736-752` → the five fail-closed arms and their loop
(exit 2 + `FAIL-CLOSED (TOKEN`), `:756` → `GREEN_MATCH`, `:849-852` → the two
kind/arm-coverage meta-checks; hermeticity re-run from outside: `UFO_SRC=/nonexistent
node claims-check.pinned.mjs --selftest` → `39/39 pass` / `VERDICT: PASS` exit 0; live
file unchanged (`e9a21b44…`), kumitate tree `porcelain-empty` (0 lines).