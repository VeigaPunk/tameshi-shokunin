# K02 — C1 depth-value attack: does leg 8 `js-sources-check` add depth or only count?

Reviewer: TameshiR18.K02CaseDepthValue (critic). Target pinned at
`kumitate-shokunin/scripts/sources-check.mjs` @ rev
`0acb7752d19058b953ebbeba253b1e35f6548de5`, blob sha256
`6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` (897 lines,
verified by `git show` + `sha256sum` in /tmp, never touching the substrate).
Baseline: `tools/mutate-and-run.sh` + `corpus/knowledge/arm-class-matrix.md` +
`corpus/knowledge/mutation-case-kumitate-round-gate.md` at
`183f87b899e6cae46be98d251cbc87fb5118f6ca`. Staged leg (X02) read at
`.ufo/waves/round-18/staged/tools/mutate-and-run.sh`.

## 0. What I measured myself (cheap falsifiers, not a sweep)

Materialized the pinned blob to
`/tmp/tameshi-r18w1-K02CaseDepthValue-jpLOFC/sources-check.mjs`, then:

| probe | command | measured |
|---|---|---|
| Control determinism | `node sources-check.mjs --selftest` ×2 | exit 0 both, `diff` → stdout **and** stderr byte-identical; `SOURCES_SELFTEST: 46/46 pass` |
| Bare `env -i` | `env -i node … --selftest` | exit 127 — node lives at `/run/user/1000/fnm_multishells/…/bin/node`, not /usr/bin. Suite strings must keep `$PATH` (leg 7's does: staged :1302 `env -i PATH="$PATH"`) |
| Bad TMPDIR | `TMPDIR=/nonexistent node … --selftest` | exit 1 — `mkdtempSync(join(tmpdir(),…))` (:565) throws **before** any check runs. Control is TMPDIR-fragile |
| M1 verdict-tail reorder (`countsVerdict` :437-439, tiers↔status swap) | `node m1.mjs --selftest` | **SURVIVED** (46/46, exit 0) |
| M2 legacy rename of the fixture-tested entry | `node m2.mjs --selftest` | KILLED (check 'frozen base identity remains legacy and counted', :760-771) |
| M2b legacy rename of a non-tested entry (`dispatch-shapes.md`) | `node m2b.mjs --selftest` | **SURVIVED** (46/46, exit 0) |
| M3 `monthDays` March 31→30 (:149) | `node m3.mjs --selftest` | **SURVIVED** — unreached arm inside the calendar table |
| M4 cadence boundary `<`→`<=` (:333) | `node m4.mjs --selftest` | KILLED on 'opened + Nd exactly due today is not overdue' (:747) — first measured strict `<` boundary among JS legs |
| M5 `--strict` promotion deleted (:434) | `node m5.mjs --selftest` | KILLED on '--strict promotes warnings to drift' (:807) |
| M6 `FINDING_KINDS` shrink (drop `RECHECK_OVERDUE`, :70-75) | `node m6.mjs --selftest` | **SURVIVED** — one-sided meta-check replicates (measured, not projected) |
| M7 traversal guard `'..'` terms deleted (:164) | `node m7.mjs --selftest` | **SURVIVED** — path-escape arm with no fixture |

All mutants were single exact-text edits with `count==1` asserted in the probe
script; pristine left untouched. These are seat probes, not the recorded case —
X01/X02 own the real spec and sweep.

## 1. Arm-class inventory vs the seven legs and the matrix

The suite has 46 checks (`SOURCES_SELFTEST: 46/46 pass`), 21 finding kinds +
3 fail-closed kinds, two meta-checks (:785 finding-kind coverage, :804
fail-closed coverage). Assert grammar: verdict **prefix** (`startsWith(
'SOURCES_CHECK: CLEAN (rows=1 ')` :588), sparse verdict **substrings**
(`entries_with_source=0 legacy=1` :768), fail-closed **token equality**
(`finalLine(run) === 'SOURCES_CHECK: FAIL-CLOSED (kind)'` :799), kind-list
membership via `textKinds` (:552-558), two exact-count regex tallies (:702-712,
:721-728), one in-process parity check calling `runCheck` directly (:840-871).

**Already-admitted classes present (replays, not new):** G predicates
(most fixtures), B fail-closed exit-map + token pins (verdict line is
exact-equality `finalLine(run) === 'SOURCES_CHECK: FAIL-CLOSED (kind)'`
:799-801, but the detail text rides the earlier `SOURCES  fail-closed` line
:449 read by nothing — same hole family as case-7's A2), C counts
(`rows=4` :685, `rows=2` S1000 :824), D reported-unasserted (verdict tail —
measured M1; `LEGACY_NO_HEADER` info line :480-481 read by nothing; JSON
`findings[].detail`, `totals.warnings`, `info` all unread — only
`schema`/`verdict`/`counts.rows` asserted :819-821), E unreached arms
(monthDays M3; traversal guard M7; `catch { /* large cadence */ }` :337;
`SELF_NOT_A_DIR`'s non-dir branch never distinguished from stat-throw since
both return the same kind :175-177).

**New / near-new surfaces this artifact offers (the depth budget):**

1. **Cross-implementation parity check** (:840-871) — the fleet awk census is
   re-derived and compared (`rows`, `malformed`, `duplicates`). No prior leg
   grades a gate against an independent implementation. First of its kind in
   the ledger; host-gated (awk absent → `skip`, :861).
2. **Calendar/date arithmetic** — `isoDay` leap rules (:140-151), `monthDays`
   table (:149), `--today` boundary semantics (:301-303, :333). Measured: a
   `<` boundary mutant dies (M4), a March-length mutant lives (M3). New arm
   species; legs 1-7 contain no date logic.
3. **Severity tiering** — `effectiveSeverity`/`--strict` (:434) promotion and
   the `totals.warnings` reporting split. No prior leg has a warning tier;
   M5 killed on the promotion arm.
4. **Frozen allowlist membership** — `LEGACY_KNOWLEDGE_FILES` (:51-92). Not
   enum-shrink (M6): the 38-length + 38-unique check (:753-758) is
   cardinality-only, so a *content* rename of a non-tested entry survives
   (M2b measured) while the tested one dies (M2). A finer hole shape than
   round-gate's CKIND.
5. **Delimited-table parser with section state machine** — `|`-split arity
   `!==13` (:261), `##` section tracking (:201-203) + `#` reset (:204-205),
   `normalizeMarkdownIndent` (:136-139). The `#` reset (:204-205) has
   no fixture → predicted survivor (unprobed).
6. **Path-escape guard** — `repoPathExists` `..` rejection (:164). M7
   measured SURVIVED; first security-guard-shaped arm in the ledger.
7. **Pin-style data point** — verdict stem pinned by prefix + sparse
   substrings, weaker than round-gate's full-line equality and kimi-census's
   CLEAN-line equality. M1 (tail reorder) survived; a `members=`-style
   middle-substring mutation is the predicted next survivor family.


## 2. Depth verdict vs. "only count"

The axis counts `recorded_cases 7→8` either way (command D regex needs only a
`\d+/\d+` header line — the staged runner's `0/10 (PLACEHOLDER)` at :93
already satisfies it; the L1 must replace it with the measured table for the
claim to be true, not just counted). But the case is *capable* of real depth:
three surface families (parity, dates, severity-tier) exist here that no leg
has measured, plus second-instance data on the admitted one-sided meta-check
(measured M6, replicating CKIND) and reported-tail (M1, replicating D2/B10/A2).
Whether the *delivered* case adds depth is entirely a spec-composition
question — 10 all-KILLED defects in G/C would add nothing but the tally.

## 3. Falsifiable conditions for the L1 (apply to X01's spec before commit)

**Shallow — reject/reshape the spec if:**

- S1. ≥7 of 10 defects land in already-admitted classes (G predicates, C
  counts, B exit-map/token) AND zero defects touch §1 items 1-6. Composition
  of round-gate (5 kill / 5 hole) is the precedent; a 10/0 kill-aimed spec is
  a counting exercise.
- S2. Zero predicted SURVIVEDs, or survivors chosen so the meta-checks make
  them *self-evident* (e.g. a defect that simply makes a check throw —
  that's a control-red mutant, killed by the control run, not a defect).
- S3. Any defect whose only kill channel is the awk parity check (:840-871) —
  its verdict is host-gated (awk absent → skip → survivor-by-skip on some
  hosts), so the leg table is non-portable. Parity defects must carry a
  second, non-host-gated check as witness.
- S4. Any predicted survivor with no off-suite witness or equivalence
  argument planned (round-16 procedure, case-7 §4). `monthDays` M3 *has* a
  cheap witness (mutant accepts `opened=2026-03-31` as invalid → probe
  `runCheck`/`isoDay` directly); unwitnessed survivors downgrade the case.
- S5. `@old` strings that aren't `count==1` — mechanical failure: e.g.
  `'corpus/knowledge/cost-and-profile.md',` occurs twice (:52 and inside the
  fixture kwarg :763); defects on the legacy list need longer
  anchors or the spec refuses at setup.
- S6. Leg suite string left unguarded. Staged :1307 currently runs bare
  `node "$MUTANT" --selftest` while leg 7 (:1302) uses the `env -i` sandbox.
  Measured hazards: bad `TMPDIR` → exit 1 control failure (mkdtempSync :565
  throws pre-check); ambient `NODE_OPTIONS` unscrubbed. No git hazard (tool
  is git-free) but `env -i PATH="$PATH" HOME=… TMPDIR=…` costs nothing and
  matches the ledger's own convention.
- S7. Control drift: if X10's repeat-control shows stdout variance, the
  case must record exit-graded verdicts only (round-16 precedent) — but my
  two-run diff showed byte-identical output, so a variance finding would
  itself need explanation.
- S8. Predictions without failing-check specificity. `expectKind`-style
  fixtures make misattribution likely (a mutant killed by the *wrong* check
  still records KILLED); case-7 recorded per-check failure lists — leg 8
  must too.
- S9. A defect on `spawnSync` timeout (:549, :861) or `mkdtemp` — flaky
  kills/INCONCLUSIVEs corrupt the byte-pinned leg table (exact 0-flip
  expectation, runner header :104-107).

**Depth-bearing — the case earns its point if the spec contains ≥2 of:**

- D1. A parity-check defect (first independent-implementation channel in the
  ledger) with a second witness check (per S3).
- D2. A date-boundary defect (leap rule, `monthDays`, or `<` boundary :333)
  — new arm species; M3/M4 already measured the class is real.
- D3. A severity-tier defect (`--strict` promotion :434 or warn→error
  severity swap) — new species; M5 killed.
- D4. A frozen-allowlist content defect (rename a non-tested
  `LEGACY_KNOWLEDGE_FILES` entry, predicted SURVIVED — M2b measured) —
  finer-grained than the CKIND enum-shrink replication (M6, also measured).
- D5. A verdict-tail or `#`-reset defect (predicted SURVIVED) extending the
  admitted reported-unasserted class to prefix+substring pin style — M1
  measured; `#` reset (:204-205) unprobed, probe first.

## 4. Defects already measured by this seat (usable as spec candidates with
independent re-derivation)

M1 SURVIVED (verdict-tail reorder :437), M2 KILLED / M2b SURVIVED (legacy
rename, tested vs untested entry), M3 SURVIVED (monthDays March :149), M4
KILLED (cadence boundary :333), M5 KILLED (--strict :434), M6 SURVIVED
(FINDING_KINDS shrink), M7 SURVIVED (`..` guard :164). Note M2b/M6/M7 are all
reported/survivor-class — a spec taking all of them would invert to
hole-heavy (3+ predicted survivors); balance per S1.

## 5. Non-blocking observations

- `LEGACY_KNOWLEDGE_FILES` contains `'corpus/knowledge/cost-and-profile.md'`
  once at :52; the string appears twice in the file (also the fixture kwarg
  `knowledgeName: 'cost-and-profile.md'` at :763). Spec authors must anchor on
  the list context (S5).
- The fail-closed detail text is read by nothing (measured parallel to
  case-7 A2); a detail-tail defect here is a third-instance replication —
  count credit, not new depth. Prefer M2b/M3/M7-style novel survivors.
- `spawnSync('sh', …)` parity invokes `sh` on PATH — under the leg's
  `env -i PATH="$PATH"` (if adopted per S6) this still resolves.

Verdict: **partial → holds if constrained** — leg 8 is count-only *unless* the
pre-registered spec contains ≥2 defects on this artifact's unmeasured surfaces
(parity/date/severity-tier/allowlist-content — §3 D1-D5); S6's unguarded
suite string and S3's host-gated parity kills are the two mechanical
corrections the L1 must enforce before the sweep.
