# tameshi round 80 — lesson (hyaku run 15)

Lane: tameshi-shokunin. Round: 80 (attempt 1), 2026-11-04. Base:
`dd2b9e2c44df680174a829901829fe86a2185185` (= `origin/master`, the round-79
closure and spot-check tip). Frozen plan: `plans/round-80.plan.md`
(declaration `ae591d5a2cf5d08cafad68a4c6ffaa62e0d3f608`). Three claims on
distinct axes: R80-C1 calibration (the registry home's printed figures equal
the live figures), R80-C2 coverage (the four survivors the round-79 wave named
become arms), R80-C3 operability (the receipt population covers the declared
tree, design class included).

## What was measured — R80-C1

- Before (base `dd2b9e2c`): `REGISTRY_BIND: rows=7 match=0 stale=5 absent=2
  error=0 unexpected=7` exit 1 (`c1-before-sweep.txt`): SKILL.md and
  `tools/registry.json` both printed the round-76 figures for wave-record
  reconciliation (19/19 vs live 23/23) and self-state freshness (11/11 vs
  14/14), the registry sweep row printed `rows=20 match=18` (live 22/20), and
  `receipt-bytes binding sweep` had no row on either surface.
- Do-nothing control: the base reading itself; appending nothing cannot reach
  the after-state.
- Landed: `tools/registry-figure-bind.py` (declared 7-row manifest, doc
  `last-named-row` and registry-json surfaces, `match`/`stale`/`absent`/
  `error`, per-row `expect` as the standing red arm) plus the SKILL.md
  round-80 registry section and the refreshed `tools/registry.json` rows.
- After: `REGISTRY_BIND: rows=7 match=7 stale=0 absent=0 error=0 unexpected=0`
  exit 0 (`c1-after-sweep.txt`); `REGISTRY_BIND_SELFTEST: 11/11 pass`
  (`c1-selftest-folded.txt`).
- Sourced? No external row; the claim is a self-assessment-vs-repo-state
  count, per AXES.md calibration.

## What was measured — R80-C2

- Before (do-nothing control, base bytes): the 14-arm selfstate control tool
  (sha256 `ca8acdd9fc64…`) scored by the three new defects `defects=3 killed=0
  survived=3`; the 23-arm wave-reconcile control tool (sha256
  `d9336fcd8b17…`) by the one new defect `defects=1 killed=0 survived=1`;
  both `CONTROL: GREEN`, byte-identical restore (`c2-control-selfstate.txt`,
  `c2-control-wave.txt`).
- Landed: selfstate arm15 (both decode refusals: BOM → `bom-present`,
  non-UTF-8 → `not-utf8`), arm16 (two rows on one path/rev with different
  argv), arm17 (`sys.flags.utf8_mode` under an explicit UTF-8 locale);
  wave-reconcile arm24 (`record.root` refused by name, and a deleted guard
  FAILs the arm instead of crashing the suite). `SELFTEST_ARMS` 14 → 17 and
  23 → 24.
- After: `SELFSTATE_SELFTEST: 17/17 pass`, `WAVE_RECONCILE_SELFTEST: 24/24
  pass`; batteries `defects=4 killed=4 survived=0` and `defects=13 killed=13
  survived=0`, both `CONTROL: GREEN`, byte-identical restore
  (`c2-landed-selfstate.txt`, `c2-landed-wave.txt`, and the per-mutant logs
  under the evidence dirs). Kill matrix exact: `ss-bom-strip` arm15 only,
  `ss-cache-key-drops-argv` arm16 only, `python-utf8-dropped` arm17 only,
  `python-isolation-dropped` arm14 only, `record-unknown-root-check-removed`
  arm24 only; wave-reconcile defects 1–12 keep their round-79 arms.
- Sourced on **S308** (PEP 540: the `-X utf8` ground and the POSIX-locale
  caveat arm17 pins).

## What was measured — R80-C3

- Before (base instrument over `.ufo/evidence`): `RECEIPT_BIND: receipts=22
  bound=14 corrected=8 unbound=0` exit 0, no design field
  (`c3-before-sweep.txt`): seven round-79 design receipts were outside the
  recognised population, the class criterion 130 targets.
- Do-nothing control: the same base instrument; recognising nothing cannot
  see the seven.
- Landed: the design block as its own declared class (`design` when
  `design_base` resolves, `unbound` `design-base-unresolvable` otherwise; a
  missing marker, a duplicate marker, a mixed block and a raw prefix without a
  complete block are refused), summary carries `design=D`, and a standing
  `receipt-bytes-tree` registry row runs the whole-tree sweep.
- After: `RECEIPT_BIND: receipts=29 bound=14 corrected=8 design=7 unbound=0`
  exit 0 (`c3-after-sweep-folded.txt`); `RECEIPT_BIND_SELFTEST: 13/13 pass`
  (`c3-selftest-folded.txt`).
- Sourced on **S289** re-opened (git-cat-file: the `blob <rev>:<path>` binding
  the measured block rests on).

## Gate

New row this round (opened 2026-11-04):

- **S308 — Add a new UTF-8 Mode (PEP 540)
  (https://peps.python.org/pep-0540/)**, fetched 2026-11-04 (HTTP date
  `Wed, 04 Nov 2026 07:14:40 GMT`, 32,969 B, sha256
  `c6ed71515dd2ba0c74eeccf94aa5f4097aed460c2c1cb291417ccb790a8ad7a2`,
  snapshot `.ufo/evidence/round-80/sources/pep540.html`, headers
  `pep540.headers`). Located quote: "This mode is disabled by default and
  enabled by the POSIX locale." (12 words, page line 220). Tier A, status
  `mined`, recheck on-release, `used-by corpus/lessons/round-80.md`.
- **S309 — Python 3.15, sys (https://docs.python.org/3.15/library/sys.html)**
  — the round-79 refused candidate, now recorded as a `rejected` row
  (round-79 closure defect 3). Fetched 2026-11-04 (HTTP date `Wed, 04 Nov 2026
  07:24:55 GMT`, 280,617 B, sha256
  `68094f11447531e5d7a4391ebcd4329f9a03434280013ffb2554f6d944671348`,
  snapshot `.ufo/evidence/round-80/sources/sys315.html`, headers
  `sys.headers`). Located quote: "Changed in version 3.4: Added isolated
  attribute for -I isolated flag." (11 words, page line 999) — the page maps
  the attribute to the flag and states no isolation semantics. Flip: the page
  gains prose defining isolated mode.

Re-opened row (same round, old → new logged):

- **S289 — Git, git-cat-file documentation**, re-opened 2026-11-04 (07:28:43
  GMT): `https://git-scm.com/docs/git-cat-file`, 79,488 B, sha256
  `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910`, byte-
  identical to the round-79 snapshot (`cmp` exit 0, and a cache-busted refetch
  returned an origin MISS with the same bytes). `used-by` old → new:
  `… corpus/lessons/round-79.md` → `… corpus/lessons/round-79.md,
  corpus/lessons/round-80.md` (no other cell changes). Scope nuance (scout
  `T80W1SC1` F1): cat-file(1) defines `<type>`/`<object>`; `:<path>` spelling
  lives in gitrevisions[7] (S091) — the row's quote stays the DESCRIPTION
  sentence, and the binding sentence in the report says so.

Census: `scripts/sources-census.sh validate --root … tameshi` exit 0 before
(`census-before.txt`) and after (`census-after-append.txt`).

## Mistakes

1. **The lane's own registry home carried stale figures and a missing row for
   a demonstrated capability.** Class: stale self-description (the
   self-assessment surface drifting from the instruments it describes).
   Evidence pointer: round-79 non-author closure defect 5 — SKILL.md's round-76
   section printed 19/19 and 11/11 while the tools printed 23/23 and 14/14,
   and `receipt-bytes binding sweep` had no row at all
   (`corpus/lessons/round-79-verifier-spotcheck.md` §6.5). Captured-by: none —
   `selfstate-freshness.py` binds capability figures in SCORECARD.md, but no
   criterion or tool re-derived a gate figure from the registry home. Fix:
   `tools/registry-figure-bind.py` + criterion 76; shown able to fail — the
   base sweep reads `rows=7 match=0 stale=5 absent=2` exit 1, and an injected
   stale/boundary row measures `stale` in the selftest.
2. **A declared non-committed receipt class was outside the recognised
   population.** Class: population gap (a verifier that declares its population
   narrowly enough to miss the class it exists to catch). Evidence pointer:
   round-79 non-author closure defect 4 — seven `.ufo/evidence/round-79/*`
   receipts carry a design block whose sha exists in no blob, and the
   instrument's header regex matched only `# tool_sha256:` so the whole class
   swept clean (`corpus/lessons/round-79-verifier-spotcheck.md` §6.4).
   Captured-by: criterion 130 was receipt-header-shaped (measured triple only),
   so a second declared block form had no rule. Fix: the design class + the
   uniform raw-prefix refusal + criterion 77; shown able to fail — the base
   instrument reads `receipts=22` where the tree carries 29, a design block
   without the marker is refused, and an all-malformed block is now
   `receipt-header-incomplete` instead of invisible.

## Wave findings

Thirteen seats settled, none died; every finding cites its committed seat
report under `.ufo/waves/round-80/w1/`. The wave changed the landed bytes in
five disclosed places, all re-measured after the change.

1. **Sentinel (T80W1SN1) — five adversarial findings, all folded into existing
   arms with the frozen counts unchanged.** F1: a CRLF receipt was invisible
   (`zero-receipts` alone, or silently absent beside a valid LF control); the
   parser now normalises CRLF (folded into ARM1). F2: a valid design block
   plus malformed measured lines, or a valid marker plus a second
   `# measured_bytes:`, was accepted as design; one uniform raw-prefix check
   over all eight prefixes now refuses both (ARM6/ARM12). F3: the live figure
   took `matches[-1]`, so a stale token printed first was out-voted; exactly
   one match is required (ARM8). F4: manifest `doc`/`registry` paths could
   escape the repo (`../`, absolute); both are now repo-relative and
   realpath-contained (ARM5). F5: Windows-style/drive-qualified design tool
   paths were accepted; `_repo_relative` refuses them on both branches
   (ARM10). The sentinel's report stays scoped to its pinned pre-remediation
   hashes and says so.
2. **Executor (T80W1E1) — counter cheats on the declaration bytes.** The
   longer-token cheat and the stale+live declaration list now measure `stale`
   (exactly one figure-shaped token equal to the live one); an empty registry
   declaration is `absent`, not a stale-shaped pass; the help text no longer
   says a per-row error is a pre-effect setup refusal (it is an `error` row
   plus exit 2).
3. **Executor (T80W1E3) — population blind spots.** An all-malformed design
   block was silently skipped (now `receipt-header-incomplete`) and a valid
   marker plus a bogus second `# measured_bytes:` was accepted (now
   `receipt-header-duplicate`). Documented limit: a complete header block that
   begins after the first 64 KiB is outside the declared population (the
   lane's receipts carry headers at the top).
4. **Critic (T80W1C1) — separability and the frozen counts.** The critic
   objected that C1's landed figures name the tools C2/C3 change, and that
   adding selftest arms would break the frozen 11/11 and 13/13 clauses. Both
   were resolved without a rule change: the new probes are folded into
   existing arms (the round-79 precedent), so both frozen counts hold exactly;
   and the coupling is reported as an authored-content coupling, not argued
   away — C1's predicate (figure equality) permits base tokens, its landed
   bytes carry the round's final figures. The critic's report records the
   disagreement for the closure.
5. **Mutation-tester (T80W1M1) — counter-mutation survivors.** `reg-superstring`
   and `reg-empty` are killed by the folds (`reg-empty` by a new empty-
   declaration leg in ARM3). Two survivors remain, both of the honest
   test-text class a selftest cannot guard about itself: `ss-bom-only` (only
   arm15's non-UTF-8 conjuncts deleted) and `wr-prefix` (arm24's
   `setup:unknown-root:` weakened to `setup:unknown`). Named for round 81 at
   the convention level, not hidden.
6. **Reviewer (T80W1R2) — C2 matrix fidelity.** Rebuilt both batteries from a
   base clone: 4/4 and 13/13, controls GREEN, restore byte-identical, the four
   singleton sets as frozen; only the spec comment (isolation → arm14 only)
   was wrong and is corrected.
7. **Scout (T80W1SC1) — sources.** All three pages re-fetched byte-identical
   (`c6ed7151…`, `68094f11…`, `91805d9a…`, the last origin-verified by a
   cache-busted MISS). S308's quote is 12 words (the Gate said 13; corrected).
   Scope nuance: cat-file(1) defines `<type>`/`<object>`; `:<path>` spelling
   lives in gitrevisions[7] (S091), so the binding sentence names both.
8. **Scout (T80W1SC2) — anchors and locale.** All 17 `@old` strings occur
   exactly once; the four new mutants are single-line edits with singleton
   FAIL sets as frozen. Under `LC_ALL=C` the POSIX locale auto-enables UTF-8
   mode, so arm17's pin of `en_US.UTF-8` is load-bearing and is asserted by
   the fixture it spawns.
9. **Connector (T80W1CN1) — overlap, assimilation, proposals.** kama's
   `tools/round43-registry-audit.py` already binds a documented gate figure to
   a live selftest; tameshi C1 is the distinct cross-surface seven-row
   population (last doc row + registry JSON, absent/stale/error), not a new
   primitive. No sibling holds the design receipt class. Staged package: 167
   lane rows (at the time), 103 staged, 8 id collisions (S153–S160) naming
   different documents, 95 id-disjoint staged rows — `Assimilation: none`.
   considerthese 2026-10-28: proposals 1–3 and 5 implemented; proposal 4's
   second point (backlog burn-down rate on the pinned 81-entry denominator)
   stays open as the bounded later-round move.
10. **Executor (T80W1E4) — controls.** Every before-state reproduced from
    pinned clones: C1 `rows=7 match=0 stale=5 absent=2 unexpected=7` exit 1
    (and the same aggregate at both base and declaration bytes, with the live
    tokens 23/14/10 vs 24/17/13 not interchangeable), C2 `0/3` and `0/1` with
    GREEN and identical restore, C3 `receipts=22` with no design field.

Assimilation: none (connector; the eight staged id collisions are unchanged).
