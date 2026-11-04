# tameshi round 82 — lesson (hyaku run 15)

Lane: tameshi-shokunin. Round: 82 (attempt 1), 2026-11-04. Base
`4dfc3181310088c2f32d51e87a4d82c047d05231` (= `origin/master`, the round-81
closure and its non-author spot-check tip). Declaration
`4005a48ac73a66c794ff8fd528e6926633fe2af3` (frozen plan, the declared
instrument, the mutant spec and the base controls). Landing
`b6658e7a90472d9c8c783067f2e5d16a98fc02c7` (the rows, the repertoire move, the
figures). Three claims on distinct axes: R82-C1 calibration (the register is
bound to declared bytes and reads object types), R82-C2 freshness (the three
round-81 capabilities are live rows), R82-C3 coverage (the newest instrument's
own assertion text is pinned).

## What was measured — R82-C1

- Before (base bytes, `.ufo/evidence/round-82/controls/`):
  `c1-before-flag.txt` → `error: unrecognized arguments: --manifest-rev HEAD`,
  exit 2; `c1-before-narrowed-certifies.txt` → the register with D6 deleted
  reads `DEFECT_BIND: rows=5 closed=5 open=0 unexpected=0`, exit 0;
  `c1-before-directory-closed.txt` → a `tree-paths` row naming
  `.ufo/evidence/round-81` reads `state=closed detail=paths-present`.
- Do-nothing control: the narrowed manifest under the base instrument. It
  MEETS a target phrased as "the counter runs green", which is why the frozen
  target is the **bound** line on the full six-row population.
- Landed: `--manifest-rev REV` (the manifest's bytes must equal
  `REV:<manifest path>`; `manifest-rev-mismatch` exit 2 before any row effect,
  `manifest-rev-unreadable` for a path absent at the revision) and the
  regular-file boundary in `tree-paths`/`tree-bytes` (`git ls-tree -z` mode
  100644/100755 and type blob; a tree or symlink measures `open`). Arms A12,
  A13 join the suite; `SELFTEST_ARMS` 11 → 14.
- After (`final/c1-bound.txt`, `c1-selftest.txt`, `c1-narrowed-refused.txt`,
  `c1-directory-open.txt`): `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0
  manifest=bound` exit 0; the narrowed clone at the tip is refused
  `manifest-rev-mismatch` exit 2; the directory reads `state=open
  detail=not-regular-file:.ufo/evidence/round-81=040000` exit 1;
  `DEFECT_BIND_SELFTEST: 14/14 pass`.
- Sourced on S103 (content-addressed identity) and S289 (blob at revision),
  with S291/S305 for the mode field and listing form; S311 for the limit.

## What was measured — R82-C2

- Before (`controls/c2-before.txt`): `SELFSTATE: rows=23 match=21 stale=2
  unexpected=0` exit 0 and `SELFSTATE_PINS: rows=23 settled=23 stale=0` exit 0
  — the three capabilities had no live row, so a stale figure in them was
  invisible.
- Do-nothing control: adding no rows leaves `rows=23`; the target's `rows=26`
  is unreachable without them, and a row with a wrong figure measures
  `unexpected` (the tool's own arm-4 fixture is the standing demonstration).
- Landed: three rows in `tools/selfstate-freshness.json`
  (`closure-defect-bind`, `standing-pin-audit`, `selftest-text-pin`) and the
  three repertoire rows moved into the live `## Capabilities` table with
  refreshed evidence (`DEFECT_BIND_SELFTEST: 14/14 pass`, the bound sweep
  figure, `SELFSTATE_PINS: rows=26 settled=26 stale=0`).
- After (`final/c2-landed.txt`, `c2-pins.txt`): `SELFSTATE: rows=26 match=24
  stale=2 unexpected=0` exit 0 (the two `stale` rows are the declared red
  arms); `SELFSTATE_PINS: rows=26 settled=26 stale=0` exit 0 at the tip; the
  three new row lines each print `measured=match` with identical doc and
  measured figures.
- Pins: `tools/defect-bind.py` at the declaration commit (`4005a48a…`),
  `tools/selfstate-freshness.py` at its last change (`1b115ba0…`) — both
  settled at the landing.

## What was measured — R82-C3

- Before (base tool bytes, `controls/c3-before-mutant.txt`): the single
  test-text edit (arm A1's summary conjunct deleted, name and fixtures kept)
  leaves the suite at `11/11` and `MUTATE: DONE (target=c3-base-db defects=1
  killed=0 survived=1 inconclusive=0 kill-rate=0%)`, `CONTROL: GREEN`,
  byte-identical restore.
- Do-nothing control: the base bytes with the same single edit — survival.
- Landed: `SELFTEST_TEXT_SHA256` over `inspect.getsource(selftest)` and arm
  `A14_selftest_text_pin`; the spec `tools/defect-bind-mutants.spec` (5
  defects: the text mutant plus the four new C1 paths).
- After (`final/c3-battery.txt`): `MUTATE: DONE (target=defect-bind-arms-r82
  defects=5 killed=5 survived=0 inconclusive=0 kill-rate=100%)`, `CONTROL:
  GREEN`, `MUTATE_RESTORE: OK`; FAIL sets are singletons — `db-a1-assertion-weakened`
  → `A14_selftest_text_pin`, `db-manifest-binding-removed` and
  `db-manifest-mismatch-accepted` → `A13_manifest_rev_binding`,
  `db-regular-file-check-removed` and `db-tree-bytes-ignores-type` →
  `A12_regular_file_boundary`. No over-kill.
- Sourced on S310 (`inspect.getsource`), re-opened this round.

## Gate

No new row this round — and the refusal is the round's Gate evidence.

- **Rejected candidate: S311-candidate — Git, gitattributes documentation
  (https://git-scm.com/docs/gitattributes)**, fetched 2026-11-04 (HTTP date
  `Wed, 04 Nov 2026 13:12:12 GMT`, 131,174 B, sha256
  `ceb3351f931ae86283f51416cf0042fd78265eda59e5af7d09e17581ec0f77f7`, snapshot
  `.ufo/evidence/round-82/sources/gitattributes.html`, headers
  `gitattributes.headers`). `REJECTED: the document is already held as S294
  (same URL, same scope: the text/eol conversion layer), so a second row is a
  within-scope duplicate (CORPUS.md rule 2; the r81 S293 precedent); the
  candidate was caught by the census `W04 S311 duplicate url
  …/gitattributes` and never committed. flip: a page state whose scope differs
  from S294's (e.g. a version that changes the conversion contract).`
- **Admitted by re-open: S294 — Git, gitattributes documentation**, re-opened
  2026-11-04 (13:12:12 GMT). Located quote re-read this round: "converted from
  LF to CRLF depending on the `eol` attribute, the Git config, and the
  platform" (16 words, raw page line 2671). The re-open's fetch differs from
  S294's round-63 snapshot in page furniture (131,174 B vs 131,046 B), so the
  re-open is NOT byte-identical; the contract the row cites is unchanged, and
  the round's claim rests on S294's scope ("grounds byte-level
  receipt-normalization conventions"). `used-by` old → new:
  `corpus/lessons/round-63.md` → the same plus
  `corpus/knowledge/counter-population-binding.md, corpus/lessons/round-82.md`.
- **Rejected candidate: `git-ls-files` (https://git-scm.com/docs/git-ls-files)**,
  fetched 2026-11-04 (13:24:21 GMT, 61,758 B, sha256
  `c6970ba0c55a087d61b3ba09f00b273014c58f341e30b23fad3f9f068beaa34e`, raw line
  2210: "This command merges the file listing in the index with the actual
  working directory files"). `REJECTED: the page lists the index and the
  working tree, not the tree objects at a revision the binding reads; the mode
  surface is git-ls-tree's (S305) and index-format's (S291); no scope the claim
  reads. flip: a later counter that measures index-vs-worktree divergence (a
  different question).` No row; the fetch receipt is the evidence of the
  decision.

Re-opened rows (same round, old → new logged):

- **S289 — Git, git-cat-file documentation**, re-opened 2026-11-04
  (13:11:33 GMT): byte-identical to the round-79/81 snapshot (`cmp` exit 0),
  sha256 `91805d9aec858f88581552fc1fe105a40a649544f872e72e6daff210a113e910`;
  `used-by` old → new: the same set plus `corpus/lessons/round-82.md`.
- **S305 — Git, git-ls-tree documentation**, re-opened 2026-11-04
  (13:11:33 GMT): the scout compared the live page with the round-77 snapshot
  and reported byte identity; `used-by` old → new: `corpus/lessons/round-77.md,
  corpus/lessons/round-79.md` → the same plus `corpus/lessons/round-82.md`.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tameshi` → exit 0, verdict `tameshi	ok	…/corpus/SOURCES.md`
(`.ufo/evidence/round-82/final/census-after.txt`; before
`.ufo/evidence/round-82/controls/census-before.txt`). Rows 170 → 170;
status `mined 137`, `queued 22`, `rejected 11`; tiers `A 152`, `B 14`, `C 4`;
malformed rows 0. The census's role this round is the learn-by-doing one: it
refused the round's own first draft (W04) before the append landed.

## Mistakes

1. **A counter could certify a population it had never been bound to.**
   Class: `vacuous` (the verdict's denominator was an unbound input).
   Evidence pointer: the round-81 connector's D-CN3 and the round-81 reviewer's
   "a manifest without a digest cannot prove its own population"; measured at
   the base tip — the register with one row deleted reads `rows=5 closed=5`
   exit 0 (`controls/c1-before-narrowed-certifies.txt`). Captured-by: none —
   every standing instrument measured a tool's *figure*, and the kill rule's
   "no row removed" clause lived in prose. Fix: `--manifest-rev` (criterion
   80); shown able to fail — the base instrument refuses the flag (exit 2) and
   the declared instrument refuses the narrowed manifest
   (`manifest-rev-mismatch`, exit 2, no row effect), while the full register
   reads `manifest=bound`.
2. **A path row measured presence, not the object kind it meant.** Class:
   `scope` (the row's verdict covered a scope it did not declare — a directory
   or a symlink standing in for a file). Evidence pointer: round-81 reviewer
   §3 D1a/D5 and executor E1's symlink-`min_bytes` vector; measured at the base
   tip — a directory row reads `state=closed detail=paths-present`
   (`controls/c1-before-directory-closed.txt`). Captured-by: none in the lane
   (the two routed notes were prose). Fix: the type/mode boundary (criterion
   81); shown able to fail — the base row is closed, the declared row is
   `open detail=not-regular-file:…=040000`, and `A12` pins it.
3. **Three capabilities were recorded outside the repertoire table and carried
   no live monitor.** Class: `attribution` (a capability was recorded in a
   round snapshot while the contract's single list did not carry it, and no
   instrument read its figure). Evidence pointer: round-81 spot-check §6.6 and
   the lane's own `Planned (round 82)` line; measured before this round —
   `SELFSTATE: rows=23`, the three names absent from `tools/selfstate-freshness.json`.
   Captured-by: none — the standing sweeps read the *repertoire* table and a
   round-specific table is invisible to them. Fix: live rows plus the repertoire
   move (criterion 82); shown able to fail — a row whose figure drifts measures
   `unexpected` (the tool's arm-4 fixture), and the three new rows measure
   `match` only while their instruments print the quoted figures.

5. **The binding was a path, and a path can be a symlink.** Class:
   `reference-drift` (the path named and the path measured diverged). Evidence
   pointer: the critic's probe — an absolute-path symlinked manifest printed
   `manifest=bound` with five rows at `7e06a403`. Captured-by: none until the
   wave; the A13 arm did not exercise a symlinked manifest. Fix: no
   `realpath` and a `manifest-not-regular` refusal (criterion 83); shown able
   to fail — the probe that printed `bound` now reads
   `manifest-not-regular:<rev>:manifest-link.json` exit 2, and A13 carries it.
6. **The bound bytes and the parsed bytes were two reads.** Class: `vacuous`
   (a binding over bytes the measurement never parsed). Evidence pointer: the
   sentinel's line map — `bind_manifest` read the file at `:440-441` and
   `load_manifest` read it again at `:345`, with no link between them. Fix:
   one read shared by the binding and the parse (`read_manifest_bytes`), plus
   a path check before the read (criterion 83); the red-before is the removed
   second read at the pre-repair bytes, and no deterministic run can
   demonstrate the race — stated as the limit of this fix's proof.

## Wave findings

One v1 wave (`w1`), 13 seats, **all 13 returned a report and a terminal
summary; no seat died** (`.ufo/waves/round-82/w1-results.json`, `seats=13`,
`results=13`). Twelve seats measured the declaration bytes (`4005a48a`); the
round then landed five instrument repairs (`72832c94` survivor pins,
`ea618593` the shared type/mode gate in `blob_bytes`, `43fb2446` the
single-read sweep, `97f0186f` replace-ref immunity, `b37860b7` the
regular-file manifest), each re-pinned and re-measured, and the final receipts
name `b37860b7`.

1. **E1 (executor, C1 rebuild) — the before/after reproduced, plus two holes.**
   Its own harness (no tool code) reproduced all three base readings and the
   declared ones row for row. It found the record defect in the committed base
   control (S3 below) and one hardening defect: a `git replace` ref makes the
   declared revision resolve to OTHER bytes, so a narrowed register binds.
   Fixed in `97f0186f` (`GIT_NO_REPLACE_OBJECTS=1` on every git call). Its
   declared-limit note stands: `--manifest-rev HEAD` binds to whatever HEAD is
   — byte equality, not authorship.
2. **E2 (executor, C2 rebuild) — the split is true and three surfaces were
   missed.** `rows=26 match=24 stale=2 unexpected=0` is the exact split (24 =
   21 existing + 3 new; the 2 stale are the declared red arms), pins
   `26/26/0`, both before readings reproduced from a blob-identical base. It
   also named three surfaces the plan's no-harm list missed: SKILL.md's
   standing-pin audit row still said 23 rows (fixed, new row appended),
   `registry-figure-bind` binds only one of the three refreshed registry
   figures (routed to round 83, disclosed), and the registry source cells
   cited the 11-arm bytes (fixed).
3. **E3 (executor, C3 independent pin) — the class reproduces independently.**
   Its own domain-separated digest pins the same class, the base bytes survive
   the text mutant (`11/11`), the declared bytes kill it (`13/14`, pin arm
   only), and the 5-defect battery reads `5/5`. Its two-edit probe confirms
   the declared limit.
4. **E4 (executor, no-harm+surfaces) — two green-by-substring hazards.** The
   `defect-bind-sweep` registry row's token stopped before ` manifest=`
   (measured: a `manifest=unbound` run would pass), and it ran without the
   flag. Fixed: the row now runs `--manifest-rev HEAD` and expects the full
   bound line. It also measured that a bare `DEFECT_BIND:` figure regex is
   vacuous (falsified doc figures still matched); all four landed figures are
   full-line regexes.
5. **SC1 (scout, sources) — the duplicate was real.** It confirmed the
   gitattributes candidate is a within-scope duplicate of S294 (matching the
   census `W04` that refused it), confirmed S289 and S305 are byte-stable, and
   proposed the `git-check-attr` reject recorded in the Gate. It routed the
   S294 anchor staleness (the row's anchor names the round-63 bytes; the live
   page differs in furniture) — disclosed in the Gate.
6. **SC2 (scout, surface census) — four routed surfaces, all paid.** D1 the
   registry sweep row (fixed per E4), D2 the SKILL 23-row cell (fixed), D3 the
   registry source cells (fixed), D4 S310's `used-by` (fixed by re-opening
   S310). Its traps were confirmed: a tail-less figure regex certifies the old
   token; a capability absent from the live table is a setup refusal.
7. **S1 (scribe) — the record prose, drafted against the receipts.** Its
   draft was superseded by the measured record; its flagged sentences are the
   ones E1/E4/R2/SN1 independently routed (base-control exit, bare figures).
8. **R1 (reviewer, C1) — the guarantee covered two of five kinds.** It
   re-derived both states with its own harness and then measured that
   `receipt-tokens`, `sources-cell` and `doc-contains` called `cat-file blob`
   directly: a symlink doc/receipt read the link target, a tree was a setup
   refusal. Fixed in `ea618593` (the gate moved into `blob_bytes`; A12 probes a
   symlinked doc). Its other probes are the round's disclosed acceptance
   surface: lightweight/annotated tags and `rev^{commit}` accepted; tree/blob
   revs, escaping paths, a directory manifest, BOM/CRLF/empty manifests and
   untracked-at-rev paths refused; a conversion-attribute path refused (the
   S294 limit); gitlink 160000 and symlink 120000 open, 100755 closed.
9. **R2 (reviewer, C2+C3) — the record lagged the repairs.** At `7e06a403` it
   measured the claims green but found the measured-commit cells and receipt
   headers still naming `ea618593` (where the spec refused and C2 was red) —
   paid by re-measuring at each repair and pointing the cells at
   `b37860b7`; the FAIL-set sentence "type pair → A12 only" (corrected in
   SCORECARD: `db-regular-file-check-removed` fails A2/A7/A10/A12/A13); and the
   "row absent" limit (the two counting commands cannot see a deleted row —
   rotated to round 83, with `--manifest-rev` on the selfstate manifest as the
   fix). Its pointer correction (`ARM2_stale_measured`, not arm 4) is applied
   below.
10. **C1 (critic) — two counterexamples, both repaired.** (a) An absolute-path
    **symlinked manifest** printed `manifest=bound` with five rows: the binding
    resolved the link to its target and compared the wrong path. Fixed in
    `b37860b7` (no `realpath`; the manifest must be a regular blob at the
    declared revision; A13 probes it). (b) The binding and the parse were two
    reads (also found by SN1) — fixed in `43fb2446` (one read). Its third
    finding is a limit, not a defect: a committed narrowed register binds at
    its own revision, because binding proves bytes at a caller-named
    revision, not that the revision is the intended one — the population's
    identity stays with the declaration commit and the record. Its C2 finding
    (`rows=26` reachable with fabricated rows) is also a limit: the claim
    stands on the three named rows' measured lines, which the receipt shows.
11. **M1 (mutation-tester) — the battery, and two survivors the spec missed.**
    5/5 with singleton FAIL sets, `CONTROL: GREEN`, byte-identical restore;
    its custom r2 (a dropped `resolve_rev`) and r3 (the deleted empty-flag
    guard) both SURVIVED at `14/14`. Both are now pinned without changing the
    arm count: A13 exercises the unresolvable and non-commit revisions, A8
    drives `main()` for the CLI guards; the re-run reads `defects=2 killed=2`.
    Its r4 (arm-count edit) is killed by the return conjunct, not an arm —
    recorded as a structural kill.
12. **SN1 (sentinel) — no finding blocks a counted predicate.** S1 the double
    read (fixed), S2 unescaped `id`/`path` breaking the line-oriented counter
    and an unhashable `id` crashing instead of refusing (low, routed to round
    83), S3 the base-control exit (S3 below), S4 `./` normalisation
    (informational). Its path/rev probes match R1's acceptance surface.
13. **CN1 (connector) — prior art and a cross-lane note.** The binding devices
    in sibling lanes are souji's `--register-rev`, kumitate's frozen-revision
    gates and kaidoku's evidence-id replay; `--manifest-rev` is adoption plus
    one new binding *target* (a defect register), not a new kind. Two of
    tameshi's own instruments still carry the A12 class
    (`receipt-revision-gate.py::drifted_paths`, `receipt-bytes-bind.py::blob_at`)
    — routed to round 83. Cross-lane: souji's `input_snapshot` compares
    worktree to blob bytes without the conversion-attribute guard this round
    declares — reported to souji, never absorbed.

**Dead seats: none.** No seat was replaced, and no claim's verdict depends on
a seat that did not report.

## Corrections of record (append-only)

- **The plan's Before bullet for the directory control says "exit 0"; the
  committed receipt prints `exit=2`.** The control manifest carried a second
  `tree-bytes` row naming the same directory, which refuses as
  `blob-unresolvable` after the `tree-paths` row printed `state=closed`; the
  summary line is the verdict, never the row prefix. A one-row control under
  the same base instrument reads `rows=1 closed=1 open=0 unexpected=0` exit 0
  (`controls/c1-before-directory-only.txt`, re-issued in round 82). The
  directory-row reading the claim uses (`state=closed` at the base,
  `not-regular-file` after) is unchanged.
- **The stale-figure demonstration pointer is `ARM2_stale_measured`, not
  "arm 4"** (`tools/selfstate-freshness.py` arm 2).
- **The plan's C3 limit sentence is wrong about a comment.** It says a vacuous
  comment inside `selftest` "stays outside the class"; measured (R2): a
  comment edit inside the function FAILS A14 — it is over-kill, not a blind
  spot. The class's real blind spots are module-level code and the two-edit
  recompute, both re-measured this round.
- **S310's re-open is not byte-identical.** The page at 2026-11-04 13:31 GMT
  is 221,837 B, sha256 `76d96171…` (round 81: `7570b79d…`), same length,
  different bytes; the located quote is still at raw line 1193, so the row's
  anchor survives. The fetch receipt is committed under
  `.ufo/evidence/round-82/sources/`.
- **Five instrument repairs after the declaration, each re-pinned and
  re-measured**: `72832c94`, `ea618593`, `43fb2446`, `97f0186f`, `b37860b7`.
  The arm count (14) and every declared after-figure are unchanged; the
  selftest digest was recomputed deliberately at each change (the pin's
  maintenance path), and the mutant spec was re-derived twice for substrate
  movement (recipe step 1).

4. **A draft row duplicated a held document because the held-page sweep was
   run for the wrong URL.** Class: `reference-drift` (a new row written against
   a document the registry already held). Evidence pointer: the census reading
   `tameshi W04 S311 duplicate url git-scm.com/docs/gitattributes across
   scopes` (`.ufo/evidence/round-82/final/census-after.txt`), with S294 holding
   the same page since round 63. Captured-by: the census itself — the `W04`
   class fired before anything was committed, which is the gate working; the
   round-level lesson is that the pre-draft sweep was run for
   `git-hash-object` (held as S103) and not for `gitattributes`. Fix: the
   candidate row was removed, the claim re-pointed at the re-opened S294, and
   the Search log records both the refusal and the failed sweep. Shown able to
   fail: the same census line is the red-before, and after the removal the
   verdict is `ok` with no `gitattributes` W04.
