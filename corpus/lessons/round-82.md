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

## Wave findings

_Written after the wave's results handoff._

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
