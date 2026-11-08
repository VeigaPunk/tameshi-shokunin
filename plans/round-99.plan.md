# tameshi round 99 — frozen declarations (plan)

Lane `tameshi` (verification-fixture craft). Round 99, attempt 1. Base (lane tip at round
start): `ff93fa16a1f65e66385b7c7f564f03b218d91ea2`, branch `master`. Instruments commit:
`466510515d02759427158a9b16e9daa889d44907` (`tools/tally-reconcile.py`,
`tools/control-assertion-audit-v2.py`, the alias fixture, the S324/S325 snapshots). The
records revision R is the commit that carries the records run; it is named in
`.ufo/waves/round-99/records-rev.txt` when it lands.

Round 98 landed admitted; its non-author spot-check
(`corpus/lessons/round-98-verifier-spotcheck.md`) routed D1-D5 (status-neutral). D2 — the
round-98 report said the C1 selftest was `18/18` at the freeze while the cited receipt prints
`12/12` — is the same class the round-94 closure found (`DISPOSITION_SELFTEST: 8/8` beside a
`9/9` receipt). Both were found by eye. `considerthese/2026-11-08.md` idea 1 (frozen-tally
reconciler, "proposals only, not acted on") proposes the instrument. C1 builds it. C2 closes the
round-98 Planned limit "the new audit is blind to a driver that registers through a renamed
recorder".

Axes: depth + calibration (lane axes). C1 moves **calibration** (the lowest non-retired axis,
pinned 8): a committed counter of mismatches between the lane's recorded selftest tallies
(its self-assessment) and the receipts those lines cite (observed repo state). C2 moves
**coverage**: the control-assertion audit's site set gains a new edge class (recorder
aliases); the command that shows it unmoved is the round-98 audit on the same fixture.
The two are causally separable: C1 never reads a driver, C2 never reads a record.

The frontier step (§2b) rides inside this cap: S324 (Nuijten et al. 2016, statcheck
prevalence) and S325 (statcheck web FAQ) are opened this round and cited by C1's knowledge
entry; the mined mistake is the round-98 audit's `loop-site-count` selftest arm (it indexes
`SELFTEST_CASES[7]`, which is `augassign`, a fixture with no loop); the census runs before
and after.

---

## Claims (frozen before data)

### C1 — calibration: recorded selftest tallies reconciled with their cited receipts

- **Axis:** calibration (a recorded tally is compared with the committed receipt it cites;
  disagreement is counted, not found by eye).
- **Surface:** `tools/tally-reconcile.py` at R, reading the twelve committed records
  `corpus/lessons/round-NN.md` and `plans/round-NN.plan.md` (NN = 93…98) and every receipt they
  cite as blobs at R.
- **Wording (frozen):** at the records revision R,
  `python3 -I tools/tally-reconcile.py --repo . --rev R --record corpus/lessons/round-93.md --record plans/round-93.plan.md … --record corpus/lessons/round-98.md --record plans/round-98.plan.md`
  (the twelve records, in that order) prints
  `TALLY_RECONCILE records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19`
  and exits 1, and its one `TALLY mismatched` line is
  `corpus/lessons/round-94.md:66 token DISPOSITION_SELFTEST claimed=8/8 receipt=.ufo/evidence/round-94/pre-freeze/c2-selftest.out observed=9/9`
  (the round-94 closure's finding); the same command with only
  `--record corpus/lessons/round-94.md` prints `records=1 tallies=1 pairs=1 matched=0 mismatched=1 unbound=0 uncited=0`
  and exits 1; `--selftest` prints `TALLY_RECONCILE_SELFTEST: 17/17 pass` and exits 0. The tool
  reads records and receipts as blobs at `--rev` through `git cat-file` (never the worktree),
  recognises exactly the two tally forms and the same-line citation grammar its docstring
  declares (`TOKEN: N/M pass`; the word `selftest` followed within 12 non-digit characters by
  `N/M`; a path ending `.out`/`.txt`/`.log`/`.json` on the same line, not in a URL), resolves a
  citation as a tree path or under the record's own round dirs (`.ufo/evidence/round-NN`,
  `.ufo/waves/round-NN`), and grades a pair `matched` only when every line of the receipt
  carrying the claimed token (or the receipt's single `*_SELFTEST` token) shows the claimed
  N/M.
- **Counter:** the twelve-record command above.
- **Red arm:** the round-94-only command above (exit 1, mismatched 1); the selftest arms
  `token-mismatched-r94-shape`, `selftest-word-r98-d2-shape`, `mixed-observed-is-mismatch`,
  `two-tallies-one-line`, `worktree-edit-ignored`.
- **Predicate:** `TALLY_RECONCILE records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19`
  with the round-94 line as the only mismatched pair.
- **Before:** at the base `ff93fa16` no committed tool prints a `TALLY_RECONCILE` line
  (`git grep -c TALLY_RECONCILE ff93fa16 -- .` prints nothing, exit 1;
  `.ufo/evidence/round-99/pre-freeze/c1-before-token.out`); the round-94 tally mismatch was
  found by the non-author closure (`corpus/lessons/round-94-verifier-spotcheck.md:102`), the
  round-98 one by the round-98 closure (D2), neither by a lane instrument.
- **After:** the twelve-record line and exit, the single mismatched line, the round-94-only
  line, and the selftest tally, all at R.
- **Kill rules:**
  - a: a pair whose receipt shows a different N/M for the claimed token is graded `matched`;
  - b: a citation or receipt is read from the worktree instead of the blob at R;
  - c: the round-94 line 66 pair is not reported `mismatched`, or another pair is;
  - d: a tally on a line with no citation is graded (counted as a pair);
  - e: a citation that resolves to more than one path is graded;
  - f: the selftest cannot fail (a seeded wrong verdict still prints n/n).
- **Declared limits:** pairing is per line: a line citing several receipts for different
  figures pairs the tally with each (round-98 lesson lines 124 and 127 are such pairs and
  grade `unbound no-selftest-line`, not `mismatched`); a bare basename is resolved only at the
  top of the record's round dirs, so a receipt under a sub-directory cited by basename alone
  grades `unbound unresolved` (four of the six unbound pairs); tallies in other spellings
  (`6/6 killed`, `9 of 9`, table cells without `pass`) are not recognised; an append-only
  erratum elsewhere does not clear a record line; the tool reads one repository, so the
  round-98 report sentence (fleet repo) is reproduced only as the selftest shape
  `selftest-word-r98-d2-shape`. The counts measure the twelve records as committed; they are a
  calibration measurement of the lane's records, not a claim that every unbound pair is a
  record error.

### C2 — coverage: recorder-alias sites in the control-assertion audit

- **Axis:** coverage (a new edge class enters the audit's site set: a state registered
  through a renamed recorder).
- **Surface:** `tools/control-assertion-audit-v2.py` at R, reading committed driver blobs at
  R; the round-98 audit `tools/control-assertion-audit.py` stays byte-identical and is the
  unmoved comparison.
- **Wording (frozen):** at the records revision R,
  `python3 -I tools/control-assertion-audit-v2.py --repo . --rev R --driver .ufo/evidence/round-99/c2/alias-driver.py`
  prints `CONTROL_ASSERT_RECORDERS aliases=1 ambiguous=0 partial=0 names=add,record` and
  `CONTROL_ASSERT sites=4 measured=3 literal=1 unmeasured=1` and exits 1, naming the
  `alias-literal` site as `class=literal`; the round-98 audit on the same blob prints
  `CONTROL_ASSERT sites=2 measured=2 literal=0 unmeasured=0` and exits 0; on
  `.ufo/evidence/round-98/controls98.py` and `.ufo/evidence/round-97/controls97.py` at R, v2's
  fifteen `CONTROL_ASSERT_SITE` lines equal v1's byte-for-byte and its `CONTROL_ASSERT` line
  equals v1's (`sites=15 measured=15 literal=0 unmeasured=0`, exit 0; `sites=15 measured=14 literal=1 unmeasured=1`,
  exit 1); `--selftest` prints `CONTROL_ASSERT_V2_SELFTEST: 27/27 pass` and exits 0. v2 counts
  as sites the bare-name calls of `add` and of every name bound anywhere in the module only by
  a plain or annotated assignment from a recorder name (chains followed to a fixpoint), and
  grades them with v1's rules; a recorder alias with any other binding anywhere in the module
  is counted and graded `unresolved` (`ambiguous-recorder`), and a name bound by
  `partial(<recorder>, …)` or `functools.partial(<recorder>, …)` is counted and graded
  `unresolved` (`partial-recorder`).
- **Counter:** the alias-fixture v2 command above.
- **Red arm:** the same fixture under the round-98 audit (exit 0, two sites — the vacuous
  pass); the selftest arms `alias-literal`, `alias-chain-literal`, `alias-ambiguous`,
  `alias-shadowed-by-arg`, `partial-recorder`, `non-recorder-name-not-a-site`,
  `alias-and-bare-two-sites`.
- **Predicate:** `CONTROL_ASSERT sites=4 measured=3 literal=1 unmeasured=1` (exit 1) with
  `aliases=1`, and the two no-regression equalities.
- **Before:** at the base no committed tool prints a `CONTROL_ASSERT_RECORDERS` line
  (`git grep` exit 1, `pre-freeze/c2-before-token.out`); the round-98 audit counts two sites on
  the alias fixture and exits 0 (`pre-freeze/c2-v1-fixture.out`), the round-98 declared limit
  ("a differently named recorder is zero-site and passes vacuously").
- **After:** the v2 fixture lines and exit 1, the two v1/v2 equalities, and the selftest
  tally, all at R.
- **Kill rules:**
  - a: an aliased call site whose code is a literal is graded `measured`, or is not counted;
  - b: v2's site lines or summary line on either committed driver differ from v1's;
  - c: a name with any non-alias binding in the module is graded as a clean alias;
  - d: a call of a name never bound from a recorder is counted as a site;
  - e: the driver is read from the worktree instead of the blob at R;
  - f: the selftest cannot fail.
- **Declared limits:** attribute calls (`c.add(...)`, `self.rec(...)`), `getattr`/`globals()`/
  dict dispatch, a wrapper `def`/`lambda` that forwards to `add`, and a recorder passed as an
  argument and called under the parameter's name are not sites; alias detection is
  module-wide and scope-insensitive, so a name that is an alias in one function and bound
  otherwise elsewhere is `ambiguous` everywhere (conservative). The fixture is lane-authored:
  no committed lane driver registers through an alias today, so the claim is coverage of an
  edge class, not a defect found in history. v1's classification limits (call-name runner
  matching, provenance not command identity, the `want_code` tautology) carry over unchanged.

## Pre-registered controls (executed and committed before this freeze)

All under `.ufo/evidence/round-99/pre-freeze/`, run by the L1 with
`.ufo/evidence/round-99/pre-freeze-run.sh` against the instruments commit `46651051` before any
scored record exists. Every receipt starts with `# cmd:`, `# cwd:`, `# instrument_rev:`,
`# tool:` and `# tool_sha256_at_rev:` header lines (round-98 spot-check D3) and ends `rc=N`.

| state | attack | expected |
|---|---|---|
| `c1-population` | the twelve records at `46651051` | `records=12 tallies=28 pairs=9 matched=2 mismatched=1 unbound=6 uncited=19`, rc 1 |
| `c1-r94-only` | round-94 lesson alone | `pairs=1 matched=0 mismatched=1`, rc 1 |
| `c1-selftest` | 17 arms | `TALLY_RECONCILE_SELFTEST: 17/17 pass`, rc 0 |
| `c1-before-token` | `git grep -c TALLY_RECONCILE ff93fa16` | no output, rc 1 |
| `c2-v1-fixture` | round-98 audit on the alias fixture (do-nothing) | `sites=2 measured=2 literal=0 unmeasured=0`, rc 0 |
| `c2-v2-fixture` | v2 on the alias fixture | `aliases=1 … names=add,record`; `sites=4 measured=3 literal=1 unmeasured=1`, rc 1 |
| `c2-v1-controls98` / `c2-v2-controls98` | both audits on the round-98 driver | `sites=15 measured=15 literal=0 unmeasured=0`, rc 0 each |
| `c2-v1-controls97` / `c2-v2-controls97` | both audits on the round-97 driver | `sites=15 measured=14 literal=1 unmeasured=1`, rc 1 each |
| `c2-site-diff-controls98` / `-97` | `diff` of the two audits' site lines | empty, rc 0, `site_lines=15` |
| `c2-v2-selftest` | 27 arms | `CONTROL_ASSERT_V2_SELFTEST: 27/27 pass`, rc 0 |
| `c2-v1-selftest` | the round-98 audit's arms | `CONTROL_ASSERT_SELFTEST: 18/18 pass`, rc 0 |
| `c2-before-token` | `git grep -c CONTROL_ASSERT_RECORDERS ff93fa16` | no output, rc 1 |

## Do-nothing controls

- **C1:** write no reconciler — no `TALLY_RECONCILE` line exists at the base (`git grep` rc 1);
  the round-94 mismatch stays visible only to a reader. A reconciler that grades nothing (every
  tally `uncited`) prints `pairs=0 mismatched=0` and misses the round-94 line, failing the
  predicate.
- **C2:** keep the round-98 audit — on the alias fixture it prints `sites=2 measured=2 literal=0 unmeasured=0`
  and exits 0 (`pre-freeze/c2-v1-fixture.out`): the literal-coded aliased state is invisible.
  The target (`sites=4 … literal=1`, exit 1) is reachable only by widening the site set.

## Kills for the round

- C1 kill rules (a)–(f); C2 kill rules (a)–(f).
- Any `falsifies-wording` artifact of this round's own wave that contradicts a frozen sentence
  is amended **before the records run** in §Amendments (wording narrowed to the enforceable
  property, with the artifact cited); a sentence the instrument cannot enforce is an honest
  stop naming the narrowing, never a wider filing (Amendment 59 ledger).

## Amendments

Pre-data: rows are added only from this round's wave artifacts, before the records run.

| id | artifact | falsified sentence | amendment |
|---|---|---|---|
| A1 | `w1/R99R2.md` S5-S8 (`R99R2-hostile.txt`: walrus, tuple-target, alias-of-ambiguous, alias-of-partial-chain2, partial-from-import, global-del, match-capture); `w1/R99M1.md` v10/v11 (withitem and AugAssign arms unarmoured); `w1/R99E2.md` (`R99E2-probeF-del.txt`, `R99E2-probeF-ifexp.txt`) | C2's "every name bound anywhere in the module only by a plain or annotated assignment from a recorder name (chains followed to a fixpoint)", "a recorder alias with any other binding anywhere in the module is counted and graded `unresolved`", "a name bound by `partial(<recorder>, …)` or `functools.partial(<recorder>, …)`" | tool repaired (v2 records bytes): a binding is a plain or annotated assignment with a value, a walrus, an element of an equal-length tuple/list assignment without a starred element, or a two-name conditional value (binds from both); `del`, match captures, starred elements and value-less annotations join the OTHER bindings; an alias or partial bound from an ambiguous name is ambiguous (propagated); an alias of a partial is a partial; `functools.partial` import aliases are recognised. Selftest gains 11 arms (`walrus-alias-literal`, `tuple-alias-literal`, `del-makes-ambiguous`, `alias-of-ambiguous`, `alias-of-partial`, `partial-import-as`, `with-target-ambiguous`, `augassign-alias-ambiguous`, `match-capture-ambiguous`, `ifexp-alias-literal`, `ifexp-mixed-ambiguous`): 27/27 → **38/38**; nine of the eleven grade differently under the frozen v2 (`records/c2-a1-discrimination.out`), the two with/augassign arms armour live code M1 showed unkilled. Wording now states the binding set exactly as the tool's docstring; declared limits gain: rebinding the base name `add` (`add = print`) is not detected, exactly as in v1 (`w1/R99CN1.md` F5); a name bound from a recorder only by a match capture or starred unpacking is not a recorder; `global`/`nonlocal` are declarations, not bindings; a source-less cycle (`a = b; b = a`) is not a recorder. Fixture numbers and the two v1/v2 equalities are unchanged. |
| A2 | `w1/R99R1.md` F1 (`R99R1-attacks-batch5.txt` `gap-every-line-fail-suffix`, `gap-every-line-no-pass-suffix`) | C1's "grades a pair `matched` only when every line of the receipt carrying the claimed token … shows the claimed N/M" (a `TOKEN: 9/9 fail` line was invisible) | tool repaired: receipt lines are read as `TOKEN: n/m` whatever follows (`pass`, `fail`, nothing), and `*_SELFTEST: n/m` likewise; arms `receipt-fail-suffix-is-graded`, `receipt-no-suffix-is-graded`. The twelve-record numbers are unchanged (R99R1's grep control: every token N/M line under rounds 93-98 evidence carries `pass`). |
| A3 | `w1/R99R1.md` F3 (`cite-out-bak-chain`) | C1's citation "a path … ending `.out`/`.txt`/`.log`/`.json`" (`a.out.bak` was cited as `a.out`) | tool repaired: the suffix must end the path (a following path character, or `.` plus a path character, refuses the citation; a sentence-ending `.` is allowed); arms `suffix-must-end-path`, `sentence-end-period-cited`. |
| A4 | `w1/R99R1.md` F2 (`cite-url-www`, `cite-host-no-scheme`) | C1's "not in a URL" | narrowed: a citation is refused only within 12 characters after a `://` or anywhere after an `http(s)://` on the line; a scheme-less host path (`www.h.example/a.out`) is cited as a path and grades `unbound unresolved` (declared limit). |
| A5 | `w1/R99C1.md` F1 (`R99C1-forgery-f1-hardcode.py` meets the three frozen C1 invocations) and F2 (`R99C1-forgery-f2-record-specialcase.py` meets every frozen C2 conjunct by special-casing the name `record`) | §Do-nothing controls: "A reconciler that grades nothing … failing the predicate" read as forgery-proof; C2's "The target … is reachable only by widening the site set" | narrowed: the do-nothing sentences name only the all-`uncited` reconciler and the unwidened round-98 audit; neither the frozen inputs nor the conjunct set exclude a verbatim-print or name-special-cased forgery. Out-of-set controls are added to the records run (tightening, numbers unchanged): C1 `--record corpus/lessons/round-93.md` alone must print `records=1 tallies=1 pairs=1 matched=1 mismatched=0 unbound=0 uncited=0` exit 0; C2 on the committed renamed-alias fixture `.ufo/evidence/round-99/c2/alias-driver-renamed.py` (`log_entry = add`) must print `aliases=1 … names=add,log_entry` and `sites=4 measured=3 literal=1 unmeasured=1` exit 1, and on the chain fixture `alias-driver-chain.py` (`rec2 = record`) `aliases=2 … names=add,rec2,record` and the same summary, exit 1; the round-98 audit prints `sites=2 measured=2 literal=0 unmeasured=0` exit 0 on both. |
| A6 | `w1/R99M1.md` t4 (window 12→40 survives), t9 (token `{2,}`→`*` survives) | nothing — the grammar sentence is correct; the battery did not pin it | arms `selftest-window-13-not-a-tally`, `selftest-window-12-is-a-tally`, `two-char-token-not-a-tally` pin the declared boundaries. With A2/A3/A9: C1 selftest 17/17 → **25/25**. M1's t5 survivor (the second URL guard) is dead code by its own analysis and is left. |
| A7 | `w1/R99RV1.md` (`R99RV1-c2-loop-arm-history.txt`) | §Frontier step "it indexes `SELFTEST_CASES[7]`, which is `augassign` … so it never exercised its stated kill rule (d)" | narrowed with the temporal qualifier the history shows: at `6b1428c8`/`764aca97`/`d32043ec` index 7 **was** `loop-site`; the records commit `3b7ae127` inserted five cases before it, so from `3b7ae127` on the arm reads `augassign` — index drift, not a never-loop arm. The round-98 claim's selftest receipts at R (`3b7ae127`) are the ones affected. |
| A8 | `w1/R99CN1.md` F2-F4 | nothing — disclosure | the lane holds two citation-resolution grammars (`quoted-line-exists.py` bare-basename-anywhere vs the reconciler's round-dir roots) and two binding walkers (v1 `collect_scopes` grades, v2 `recorder_names` finds sites); they agree on every committed population measured this round. Neither new tool has a `tools/registry.json` row (the round-98 audit has none either) — routed, not claimed. |
| A9 | `w1/R99SN1.md` F3 (`R99SN1-nonutf8-digit-residual.txt`: a `\xff` inside `8/8` hid a contradicting line; the pair graded `matched`, rc 0, also after A2) and F4 (no timeout, per-pair re-read) | C1's "grades a pair `matched` only when every line of the receipt carrying the claimed token … shows the claimed N/M"; kill rule (a) | tool repaired: records and receipts are decoded strictly; a non-UTF-8 blob is refused at setup (`TALLY_SETUP blob-not-utf8:<path>`, exit 2), as v2 already refuses a non-UTF-8 driver; each blob is read once per run; every git call carries a 120 s timeout (`git-timeout`, exit 2). Arm `setup-receipt-not-utf8`. |
| A10 | `w1/R99SN1.md` F2 (`R99SN1-silent-verdict-injection.txt`: without `-I` a `PYTHONPATH` fake `subprocess` flips the round-94 pair to `matched`, exit 0) | nothing in the frozen wording (it runs `python3 -I`) — hardening | both new tools refuse to run without isolated mode (`TALLY_USAGE …` / `AUDIT_USAGE …`, exit 64); the counter commands are unchanged. |
| A11 | `w1/R99SN1.md` F1 (`R99SN1-tool-provenance-mismatch.txt`: the pre-freeze runner names the blob digest at `46651051` but executes the worktree file) and F5 (the twelve-record counts depend on the whole tree at the revision) | D3 closure "every … receipt carries its … tool digest" read as certifying the executed bytes | the pre-freeze receipts were produced while worktree = blob at `46651051` (the instrument commit was clean when they ran; their committed bytes match every seat's blob re-run), but the runner did not enforce it. The records runner `.ufo/evidence/round-99/records-run.sh` extracts each tool from R with `git show R:<tool>` into scratch and executes those bytes; each tool receipt carries the lane's round-78 triple `# measured_rev:` / `# tool:` / `# tool_sha256:` (so `tools/receipt-bytes-bind.py` can bind it) plus `# tree:` (R's tree id) and `# cmd:`. Tool-less receipts (`git grep`, `diff`) live in `records-aux/`. |

## Routed defect closures (round-98 spot-check, not claims)

| id | closure | evidence |
|---|---|---|
| D1 | append a named correction to SCORECARD restoring the round-94 `R94-C1` verdict text (`**verified under the amended wording**`; round 94 had A1-A8 only); the round-98 in-place cell stays as landed | `SCORECARD.md` round-99 section |
| D2 | erratum in the round-99 report and lesson: the round-98 freeze selftest receipt prints `12/12` (v1 audit), not `18/18`; the class is C1's | round-99 report §Errata; `corpus/lessons/round-99.md` |
| D3 | every round-99 pre-freeze and records receipt carries its command line, cwd, revision and tool digest as `# ` header lines | `.ufo/evidence/round-99/pre-freeze/*.out`, `pre-freeze-run.sh` |
| D4 | the round-98 registry red/green pairs re-run by a non-author wave seat (R99E3) | `.ufo/waves/round-99/w1/R99E3.md` |
| D5 | carried limits restated (battery 5/10 mutants alive; audit blind to `want=code` tautology); C2 narrows the renamed-recorder blind spot to the declared non-site spellings | this plan, C2 limits |

## Frontier step (§2b)

- Sources: S324 (paper, Europe PMC record of Nuijten et al. 2016) and S325 (statcheck web FAQ)
  are opened this round; one candidate is refused with reason and flip; census before and
  after must exit 0.
- Sourced claim: C1's knowledge entry `corpus/knowledge/tally-receipt-reconciliation.md`
  cites S324 and S325 — statcheck recomputes a reported figure from the reported inputs and
  flags disagreement; half of the NHST papers it read carried at least one inconsistency.
- Mined mistake: the round-98 audit's `loop-site-count` arm reads `SELFTEST_CASES[7]`
  (`augassign`, no loop), so it never exercised its stated kill rule (d); fix = v2 binds the
  arm by name and asserts the fixture loops, shown able to fail by a mutant.
- considerthese: `2026-11-08.md` idea 1 (frozen-tally reconciler) is mined as C1.
