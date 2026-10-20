source: S003 — https://stryker-mutator.io/docs/stryker-js/incremental/ — §Incremental mode, §Limitations, §Forcing reruns; fetched 2026-10-20T04:46:12Z, sha256 9054e311a0569231aa2a1427a4137729c8180d7f2687dfd450322e855cc9ad90 (33,898 B); S041 — https://pitest.org/quickstart/incremental_analysis/ — §Incremental analysis; fetched 2026-10-20T04:46:12Z, sha256 e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db (8,892 B); S047 — the same URL and the same fetched bytes as S041, cited as the round-13 precision-correction row that supersedes S041's teaches cell (numbered optimisations 1–5 and the dependency paragraphs; page version unstated); S031 — tools/mutate-and-run.sh:80-89, 540-553 @ 4eb4cf3, sha256 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 (own-work: the six-leg pins and recorded tables). The quoted excerpts in §1 are the retained location; the full-page digests make each fetch reproducible.
verified-at: 2026-10-20
recheck: 90d — the tighter of S003's 180d and S041's 90d registry cadences, re-opened together. `curl -fsSL https://stryker-mutator.io/docs/stryker-js/incremental/ | grep -c 'The dry run remains required'` → 1 and `grep -c 'Any other changes to your environment are not detected'` → 1; `curl -fsSL https://pitest.org/quickstart/incremental_analysis/ | grep -c 'all these optimisations introduce a degree of potential error'` → 1 and `grep -c 'it is currently'` → 1 (each ran 2026-10-20T04:47Z against the fetched copies; 0 = drift)
ground: F7 — incremental re-sweep granularity (`corpus/README.md` frontier F7: "pin-level cadence only → per-leg reuse decisions classified")
source-correction: S048 — https://pitest.org/quickstart/incremental_analysis/ — same reopened bytes and numbered items 4–5 as S041/S047; supersedes S047's test-versus-mutation paraphrase with the object-neutral prioritisation distinction used below.

# Pin match is not a reuse licence: six-leg content disposition vs a fresh re-sweep

Scope: this entry supports one bounded method step — how a *content* disposition
of the six recorded legs must be read. It does not adopt incremental mutation
testing, does not re-measure any leg, and does not claim the pattern general
across lanes.

## 1. Sources, located (O)

**S003 §Incremental mode.** The page states its reuse predicate as two
conditions (quoted verbatim apart from joining the bullets; the quote marks
around `"Killed"` are as served in the page's HTML):

> Reuse is possible when: A mutant was "Killed"; the culprit test still exists, and it didn't change. A mutant was not "Killed"; no new test covers it, and no tests changed.

and names the comparison it actually makes:

> StrykerJS will do a git-like diff of your code and test files to the previous version it finds in the incremental report file in order to match the mutants and tests to the current version of the code.

The dry run is not skipped:

> The dry run remains required; as it discovers tests, mutation coverage per test, and ensures Stryker runs successfully when no mutant is active.

**S003 §Limitations.** The declared blind spots, verbatim:

> Stryker will not detect any changes you've made in files other than mutated files and test files.

> Any other changes to your environment are not detected, such as updates to other files, updated (dev) dependencies, changes to environment variables, changes to .snap files, readme files, etc.

> Static mutants don't have test coverage; thus, Stryker won't detect test changes for them.

Its runner-support table adds that a command-style runner detects nothing about
tests: "All test details are unknown incremental mode will only detect changes in
mutants, not their tests." (page wording as printed). `--force` is the page's
escape hatch: "With these limitations in mind, you can probably imagine a
scenario where you want to force specific mutants to run while using incremental
mode." It reruns "all mutants in scope, regardless of the incremental file."
The causal reading that it exists *because* detection is incomplete is [I]; the
page does not state a reason.

**S041 §Incremental analysis.** PIT calls the feature experimental and frames
reuse as inference:

> PIT will track changes to the code and tests and store the results from previous runs. It will then use this information to avoid re-running analysis when the results can be logically inferred.

Its skip rules vary by item: rule 1 conditions on the class, rule 2 on the class
and the killing test, rule 3 on the covering tests:

> If a mutation was killed in the last run and neither the class under test or the killing test has changed, then it can be assumed that this mutation is still killed.

> If a mutation survived in the last run, no new tests cover it, and none of the covering tests have changed, then it must still survive.

It then bounds its own claims:

> With the exception of 4), all these optimisations introduce a degree of potential error into the analysis.

Rule 4) is a *prioritisation*, not a reuse skip: a previously killed mutant
whose class or killing test changed "should therefore be prioritised above
others" (since 1.14.4); the pronoun's referent is left as written. Rule 5) is
"not yet implemented". So the live reuse skips are 1)–3), and PIT attributes
potential error to them. **S047 records this precision correction**: item 4 is
a prioritisation rather than a reuse skip, item 5 is only proposed, and the
potential-error sentence covers the optimisations rather than solely live
result-reuse skips. S041's earlier "all but one of its reuse optimisations"
cell is superseded by S047; the original row is retained. The dependency
limitation is explicit:

> The main issue is that class behaviour is defined not only by its bytecode, but also by its dependencies (i.e the classes it interacts with and the graph of classes that they interact with). PIT will only consider the strongest of these dependencies - changes to super classes and outer classes, when deciding if a class's behaviour might have changed.

> So the incremental feature is based on the assumption that it will be relatively rare for changes in the dependencies of a class to change the status of a mutation. Although this assumption seems reasonable, it is currently unproven.

The unimplemented meta-mutant rule carries a further unquantified risk, and
history provenance is the operator's job: with different history locations
"you will need to implement some mechanism to swap the values between runs".

Version state, recorded not smoothed: S003 says only "Available since Stryker
6.2"; S041 and S047 state no PIT version. Both are vendor documentation for
their own tools, and neither discusses content hashes or a gate-file pin.

## 2. What the sources license (O)

- Both tools reuse only under an **unchanged-inputs** predicate, with different
  units: S003 keeps a verdict when the mutant and its tests are unchanged (or
  no new test covers it); PIT keeps the infinite-loop verdict on an unchanged
  class, a killed verdict on an unchanged class and killing test, and a
  survivor on unchanged covering tests.
- Both declare their change detection incomplete. S003 lists environment,
  dependencies, `.snap` files and non-mutated/non-test files as undetected;
  PIT states its optimisations introduce "potential error", considers only the
  strongest class dependencies, and calls the underlying assumption "unproven".
- S047 supersedes S041's wider summary: PIT presents the feature as
  experimental, its dependency assumption is unproven, item 4 is a
  prioritisation exception, and item 5 is not implemented. Nothing there is a
  general reuse guarantee.
- Neither document discusses a content hash, a pin, or a gate artifact. Their
  reuse unit is source/test change against a stored report — not a hash of the
  tool or gate being run.

## 3. The lane's pin object is coarser than either reuse predicate (I)

The runner records, per leg, one blob path, one revision and one sha256
(`tools/mutate-and-run.sh:81-83, 540-553`). A replay materializes
`git show <rev>:<path>` and refuses on any pin mismatch — "a missing
repo/rev/blob or a pin mismatch is a SETUP refusal, never a pass"
(`:99-108`); the `REGRESSION_PIN` line reports exactly that git source and
pinned sha256 (`:119-120`, `:959`). The command that then runs is
`node "$MUTANT" --selftest` or `bash "$MUTANT" --selftest` over the
materialized copy (`:1113-1140`).

The lane's own reading vocabulary is narrower still: a **current** pin means
"recorded pin = live file = HEAD blob, tree clean"; the read is "hygiene and a
trigger reading, not a replay guard" (`fleet-kill-rate-ledger.md` §ER-3).
**stale** and **drift** are the other two readings.

From these observations:

1. [I] Byte identity of the pinned gate file is necessary to even consider
   reusing its recorded verdict table, but it cannot satisfy either source's
   reuse predicate. S003 requires the mutant and its tests to be unchanged
   (or no new covering test); PIT requires the class and the killing/covering
   tests unchanged. The pin names one file. It carries no mutant inventory, no
   test identity, no covering relation, and no dependency closure.
2. [I] The unpinned closure is exactly what both sources name as their blind
   spot: environment variables, (dev) dependencies, sibling files, snapshot
   files, and the runner plugin's test-location support (S003); class
   dependencies beyond super/outer classes (S041). The leg invocation's
   toolchain and any sibling file its selftest reads are outside the pin.
3. [I] Therefore `result_reuse: not_established` is the only defensible reuse
   value for a content-only probe of these six legs. This is a **lane
   inference** from the dependency/environment blind spots S003 and S047 name,
   plus the pin's scope — not a sentence either document writes about pins, and
   not a measured outcome.
4. [O] A replay is not reuse. The harness's exact-band expectation — "0 verdict
   flips … killed-delta 0 … control green, MUTATE_RESTORE: OK"
   (`tools/mutate-and-run.sh:109-114`) — describes a re-execution at the
   recorded pin. It says nothing about what a stored table may be assumed to
   mean on a later, unexecuted run.
5. [O] Byte identity is over file contents only. The runner mirrors the git
   mode because a `100755` blob is required for a self-exec suite
   (`tools/mutate-and-run.sh:104-106`), and round 10 measured a SETUP when the
   materialized copy at the recorded pin lacked the exec bit
   (`plans/round-10-record-draft.md:84-88`). A content status that hashes
   worktree bytes therefore does not even establish that the artifact can run.

## 4. Six-leg content disposition vs a fresh re-sweep (O tameshi; I)

The six recorded legs are tameshi's own-work ground (S031); the runner defines
them exactly as follows (`tools/mutate-and-run.sh:84-89`, pins `:542-553`):

| leg | pinned path | recorded rev | pin sha256 | recorded expectation |
|---|---|---|---|---|
| js-kimi-census | `kumitate-shokunin/scripts/kimi-census.mjs` | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` | 8/10 (80 %) |
| bash-surface-census | `kagi-shokunin/corpus/surface-census.sh` | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` | 8/10 (80 %) |
| bash-tsukuroi-census | `tsukuroi-shokunin/tools/tsukuroi-census.sh` | `165307fe4746a8807b02ec4a7d7ecac0368454a6` | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` | 6/10 (60 %) |
| bash-mado-verify | `mado-shokunin/tools/mado-verify.sh` | `eead56b20ad2b28299ae4fa623d52a99b44c743c` | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` | 4/10 (40 %) |
| bash-checklist-run | `kagi-shokunin/corpus/checklist-run.sh` | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` | 7/15 (47 %) |
| js-claims-check | `kumitate-shokunin/scripts/claims-check.mjs` | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` | 7/10 (70 %) |

**A content disposition is a read-only classification.** Per leg it records the
recorded pin, the current committed blob, the current worktree content and a
status (unchanged / changed / unavailable), plus the reuse field fixed at
`not_established` by §3. It executes no leg, produces no control, no restore
proof, no table and no rate. Its whole product is "do the recorded bytes still
name the object in front of us".

**A fresh re-sweep is an execution.** It names the revision it measures, runs
the suite and a control, applies a single-edit spec whose expectations were
registered before the run, and lands a new row; the ledger's three triggers are
owner hardening, suite changes and substrate drift
(`fleet-kill-rate-ledger.md:306-310`). It is the only artifact that can produce
a new kill-rate.

The two differ in kind, not degree. A disposition row reading `unchanged`
neither re-verifies the recorded table nor authorizes its reuse. [I] A `current`
reading is not itself a re-sweep request: the ledger says a current pin means
"a re-sweep is a fresh reading, not a repair". [I] Because the unpinned
closure can always differ, no content disposition class implies safe reuse;
conversely, `changed`/`unavailable` only says the recorded table is bound to
bytes that are no longer here, which still is not a new measurement. A
`changed` row is the ER-3 trigger-3 condition (substrate drift): a request to
re-pin and re-sweep, never a successor measurement.

**No new kill-rate and no seventh case.** The recorded expectations above are
the six legs' tables; this entry adds no leg, reruns none, and revises no rate.
A prior executed six-row pin read exists as a historical receipt —
`LEDGER: 6 cases in; target current=4 stale=2 drift=0` at 2026-10-14T19:58Z,
rows 3/4 `stale` (`fleet-kill-rate-ledger.md` §ER-4) — and bounds nothing about
current content.

## 5. The source-named blind spots, mapped to these legs (O / I)

| blind spot | source sentence | what it means for a leg disposition | status |
|---|---|---|---|
| environment variables | S003: "changes to environment variables" undetected | the pinned blob is one file; the `PATH`/`TMPDIR`/locale state of the selftest invocation is outside the pin | partial [O] — §5a |
| (dev) dependencies | S003: "updated (dev) dependencies" undetected | the leg command's interpreter and any package the selftest imports are not in the pin; PIT adds that only the strongest class dependencies are considered | partial [O] — §5a |
| snapshot files | S003: "changes to `.snap` files" undetected | any golden/snapshot fixture a selftest consults lives outside the pinned path; F4 (golden/snapshot discipline) is still unheld ground in `corpus/README.md` | unmeasured here [U] |
| test identity/locations | S003 table: command runner detects "Nothing" about tests; "Test names only" runners see only added/removed tests | the six legs invoke a command (`--selftest`), the shape S003's table rates as no test-change detection; importing the reuse rule would need test identity the pin does not carry | [I] analogue, not a Stryker run |
| static mutants | S003: "Static mutants don't have test coverage" | a claim about Stryker mutants, not about these bash/JS gates; no mapping attempted | out of scope |
| dependency graph | S041: only super/outer classes considered; assumption "unproven" | the analogous unpinned set for a bash gate is whatever its selftest sources; the pin does not enumerate it | partial [O] — §5a |
| history provenance | S041: history input/output locations must be swapped by the operator | any future reuse store needs its own read/write path discipline; no store exists in this lane | not applicable yet |

### 5a. Measured omitted inputs (O, read-only)

Three of the legs have concrete, anchored unpinned inputs; none requires a run
to observe, and none changes a recorded table.

- **bash-surface-census** — `JANITOR="${THE_JANITOR_BIN:-the-janitor}"` and
  `SQLITE3="${SQLITE3_BIN:-sqlite3}"`
  (`kagi-shokunin/corpus/surface-census.sh @ fecee874:82-83`).
  When the handler is absent the selftest records
  `skip-case … substrate-absent (handler not on PATH)` instead of executing the
  verb cases (`:817-823`), and the sqlite-backed fixtures call `sqlite3`
  directly (`:710`, `:789-790`). The recorded host was such a host: handler
  **MISSING**, control printed `skip-case 15` / `skip-case 16`
  (`mutation-case-kagi-census.md:24-30`). [I] Same blob, different `PATH`: the
  `:817` branch means the selftest records skips instead of executing those
  verb cases, so its executed case set differs.
- **bash-checklist-run** — the selftest of
  `kagi-shokunin/corpus/checklist-run.sh` re-execs `"$SELF"`
  (`@ fecee874:65, :416`), so the exec bit is part of the input. The round-10
  record measured the consequence: the materialized blob at the pin lacked
  `100755` and the control went red with every case exit 126 —
  `REGRESSION: SETUP (cases=6 passed=5 cannot-verify=1)` — fixed by mirroring
  the git mode (`mutate-and-run.sh:104-106`;
  `plans/round-10-record-draft.md:84-88`). **A sha256 of bytes does not include
  the mode**, so a content-only `unchanged` can coexist with an unrunnable
  artifact. Its row-timeout case also sets `CT=1` (`:438-439`), a timing input.
- **js-claims-check** — its selftest (`kumitate-shokunin/scripts/claims-check.mjs @ 175de6ba`)
  spawns `process.execPath` (`:582-583`)
  and creates a `mkdtempSync(join(tmpdir(), …))` workspace (`:600`): the
  interpreter path and `TMPDIR` are outside the blob pin. Its `$UFO_SRC` /
  homedir default is resolved lazily and "never in `--selftest`" (`:82-93`), so
  that input belongs to the gate's CLI mode, not to this leg.
- **Outside the pin, effect not established** — kagi `SKILL.md` moved
  `+4/−2` between `fecee87` and HEAD. The checklist gate defaults
  `SKILL="$ROOT/SKILL.md"` (`:68`) but the selftest passes fixture `--skill`
  paths (`:416`); whether any leg reads the live file is not established by
  these reads. It is exactly the kind of sibling change the pin does not
  enumerate.

These rows are the method's required disclosure. A disposition receipt that
reports content status but omits the unpinned closure is partial, even when all
six statuses read `unchanged`.

## 6. Empirical section — the round-13 receipt (deferred, contents not claimed)

The round-13 lane produces `.ufo/evidence/round-13/pin-dispositions.json` from
`tools/pin-disposition.py`, fed by `.ufo/evidence/round-13/pin-manifest.json`.
This entry does not read that receipt, does not cite it, and asserts nothing
about its values. When this entry was written, no `pin-dispositions.json` was
present in that directory (it then held `before.json`, `claims.json`,
`measure.py` and `pin-manifest.json`); the manifest is an input, not a
disposition receipt, and is not summarized here.

Read the eventual receipt against these invariants, which follow from §3–§5:

- six rows, one per leg named in §4, no duplicates and no seventh;
- the receipt records `observed_at` (UTC) and each repo's current HEAD commit;
  a repo can move between the probe and its reader, so a row without both goes
  stale silently and cannot be located in time;
- each row's recorded pin equals the runner's `PIN_*` value (`:542-553`);
- each row separates the current committed blob from the current worktree
  content, and a missing repo/rev/blob/path is an explicit `unavailable`, never
  a silent pass;
- every row's reuse field is `not_established`; a row claiming established
  reuse is unsupported by S003/S041/S047 at this pin granularity;
- the receipt states which inputs it did **not** compare (environment,
  dependencies, test identity, snapshot files), or is read as partial.

What would falsify this method: a receipt that treats `unchanged` as a reused
verdict, a row that drops the reuse field, or a disposition count other than
six. A freshness failure is also falsifying: refreshing `PIN_*`/`REV_*` or
appending a ledger row at a new HEAD without an executed control, a
pre-registered spec and a table at that revision. That is a re-pin claim, not a
measurement, and no disposition row authorizes it. None of these has been
observed; the check belongs to the receipt's reader.

## 7. Boundaries and unknowns (U)

- **No generality claim.** S003 documents StrykerJS and S041/S047 document PIT.
  Two external tool docs are not two independent lanes; `PROVINCE.md` admits a
  pattern only from evidence in two independent lanes. The lane-level claim
  here (disposition ≠ re-sweep) rests on tameshi's own runner and ledger
  (S031 plus `tools/mutate-and-run.sh`), not on the two docs.
- **No promotion by this entry.** F7's frontier move is "pin-level cadence only
  → per-leg reuse decisions classified"; classifying six content dispositions
  as `not_established` is bounded detail, not the whole incremental-execution
  ground. Whether F7 reads held or open is L1's integration call.
- **Identity established; page versions not.** The opening fetches' digests are
  recorded at `.ufo/evidence/kaika-round-1/sources-opened.tsv:4` (S003,
  2026-10-19T21:43:50Z) and `:33` (S041, 2026-10-19T21:47:33Z); both equal this
  re-open's digests, so the two accesses served byte-identical pages. What
  remains unknown is the page *version*: S003 states only "since Stryker 6.2";
  S041 and S047 state no page version. S047 is a precision correction read from
  the same bytes as S041, not an independent fetch; its correction is
  interpretive and inherits the same version gap, while S041's original row is
  retained.
- **Partly measured, partly not.** §5a records three legs' unpinned inputs from
  read-only source reads (surface-census handler/sqlite, checklist-run exec
  bit, claims-check interpreter/tmpdir). The remaining legs' selftests,
  environment variables and snapshot fixtures are not measured here; the table
  in §5 marks those cells `[U]`.
- **Concurrent artifact.** `tools/pin-disposition.py` and its manifest were
  landing in the same wave; this entry names the invariants, not the
  implementation.
- **No errata** at this write.
