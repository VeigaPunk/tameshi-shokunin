# T48A2CritLessonCorrections — the two appended corrections at `c7586b9a`

Seat: `T48A2CritLessonCorrections` (critic, leaf). Read-only on the lane; no counter was run (no
`--selftest`, no `--emit`, no probe); every statement below is a `git show` / `sha256sum` /
`grep` fact at a named revision. No verdict is claimed for C1 or C2.

Target: `corpus/lessons/round-48.md` at content revision
`c7586b9a10effc63b4bd327f976edc094c1bdc17` (39533 B, sha256 `a6d5fd94e0933610…`; the worktree
copy is byte-identical, `git status --porcelain` shows only `?? .ufo/waves/round-48/a2w1/`), sections
`## Correction C1-R48-1` (`:108-204`) and `## Correction C1-R48-2` (`:207-282`).

## What holds (checked, no finding)

Every fenced quote in both corrections is byte-identical to its cited line, checked by exact
string equality against `git show REV:path` (not by eye):

| quote block at | source | revision | result |
|---|---|---|---|
| `round-48.md:116` | `corpus/lessons/round-47.md:117-118` | `8b0e15d2` | exact |
| `:127` | `SCORECARD.md:2270` | `473336d9` and `c7586b9a` | exact in both |
| `:133` | `SCORECARD.md:2276` | `473336d9` and `c7586b9a` | exact in both |
| `:143` | `.ufo/evidence/round-47/after/c1.stdout:5` | `c7586b9a` | exact |
| `:149` | `…/after/c1.stdout:17` | `c7586b9a` | exact |
| `:155` | `…/after/c1.stdout:45` (last) | `c7586b9a` | exact |
| `:163-164` | `before/c1-at-freeze.stdout:5,17` **and** `control/emit-observed-pre-freeze.out:5,17` | `c7586b9a` | exact for both files (two non-adjacent lines quoted as one fenced pair; the caption says "lines 5 and 17") |
| `:217` | `corpus/lessons/round-47.md:81` | `c7586b9a` | exact |
| `:223` | `.ufo/waves/round-47/w1/T47RevProvince.md:30` | `c7586b9a` | exact |
| `:229` | `T47RevProvince.md:436-439` (§6.5, `:428+`) | `c7586b9a` | verbatim contiguous fragment |
| `:240` | `PROVINCE.md:14-18` | `c7586b9a` | exact |
| `:256` | `corpus/lessons/round-47-verifier-spotcheck.md:90` (tail cell) | `c7586b9a` | verbatim fragment |
| `:262` | `…spotcheck.md:106` | `c7586b9a` | exact |

Both elided inline quotes are verbatim and in order on the cited line: `SCORECARD.md:2314`
(`473336d9`) contains "its dependence set was {env, node} in one run and {bwrap, node} in another"
before "a deciding run that observes a different set … not re-run until it agrees";
`T47CritC1Control.md:253` contains the quoted `quiet:` fragment verbatim (the statement name in the
quote comes from `:252`; the "…" marks the elision). `QUALITY.md:27-30` and `:4-5` are verbatim at
`c7586b9a` (the round-48 `+8` lines are appended after them). Both greps in the corrected row
reproduce: `git show c7586b9a:corpus/SOURCES.md | grep -c '1810.05286'` → `0`;
`… | grep -c 'S205'` → `0`; worktree identical. Package copy digest and size correct:
`sha256sum /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r8-predictive-test-selection-cost.md`
→ `af5bef5fa75f6e1a…`, 2770 B, head line 1 = `source: S205 — https://arxiv.org/abs/1810.05286 …`.
Integration is faithful to the wave-1 draft: `diff` of the correction bodies
(`.ufo/waves/round-48/w1/T48ScribeLessonCorrection.draft.md`) against the appended sections shows
only heading/fence/bounds rewording — every finding below was already in the draft.

---

## Finding 1 — three provenance digests resolve only to *pre-round-48* blobs, and one is labelled "lane worktree" (the class the correction is about)

Impacted axis: C1 (provenance of the round record), C2 (the SOURCES digest at `:248` attests a
registry-wide grep).

| cell | claims | actual at `c7586b9a` |
|---|---|---|
| `round-48.md:198` `\| SCORECARD.md (lane worktree) \| 954e057f9395ff06 \| 248883 \|` | worktree digest | `git show c7586b9a:SCORECARD.md \| sha256sum` → `4c99ac4be5ba1697…`, **263506 B**; worktree `sha256sum SCORECARD.md` → same. `954e057f9395ff06` / 248883 is the blob at `473336d9` **and** `7552984` |
| `round-48.md:279` `\| corpus/QUALITY.md \| 8fba0f5523f7eca8 \| 88755 \|` | digest + bytes | `1650ece0860d36f3…`, **94309 B** at `c7586b9a` (`8fba0f55` / 88755 at `8b0e15d2`, `473336d9`, `7552984`) |
| `round-48.md:280` `\| corpus/SOURCES.md \| bb8f0997b820b859 \| 112478 \|` | digest + bytes | `7e99c6a068521cf3…`, **116284 B** at `c7586b9a` |

`round-48.md:248` repeats the stale SOURCES digest *as the attestation* for the `→ 0` greps:
`` (`corpus/SOURCES.md` sha256 `bb8f0997b820b859…`) ``.

The labelled cell is false at the commit that publishes it: at wave-1 draft time the worktree
`SCORECARD.md` was `954e057f…`; the L1 appended the round-48 block to `SCORECARD.md` and committed
it with the correction (`c7586b9`, `SCORECARD.md | 49 +`), so the published label and digest no
longer describe the worktree. None of the three rows names a revision, so a reader cannot tell the
digests are pre-round-48. This is precisely the defect C1-R48-1 names ("no revision is named beside
them"), reproduced in C1-R48-1's own table, and the rule it appends at `:189-190` is not applied to
its own provenance.

Damage is bounded: **no quote or line number is damaged.** `SCORECARD.md:2262/2270/2276/2314` hold
the same text at `c7586b9a` (the round-48 block is appended at `:2324`, after them), and the
QUALITY/SOURCES quotes and grep results are unchanged.

Smallest safe correction: add a revision column to both tables and pin those three rows at
`473336d9` (or recompute at `c7586b9a`); at `:198` replace "(lane worktree)" with "as at
`473336d9`". No claim in the correction changes.

## Finding 2 — `:168` calls the cited probe "under load"; the line it quotes is labelled `quiet`

Impacted axis: C1 (provenance of the declared dependence set).

Command: `git show c7586b9a:.ufo/waves/round-47/w1/T47CritC1Control.md | sed -n '244p;252,253p'`

- `:244`: "Two `--emit` passes were made … one while the fleet was **busy** and one while it was **quiet**."
- `:252` (busy): ends `→ deps bwrap,env,fleet-root,node`
- `:253` (quiet): `quiet: P2=`REGRESSION: PASS (cases=9 passed=9`, exit 0   → deps env,fleet-root,node`

`round-48.md:168` states: "The declared `env,fleet-root,node` … traces to a wave-1 probe **under
load**, `…T47CritC1Control.md:253`: "six-leg regression ledger … quiet: … → deps
env,fleet-root,node"." The quoted label contradicts the descriptor; the busy pass at `:252` is the
one that carries `bwrap,…`, not the declared set. Smallest safe correction: delete "under load"
(e.g. "traces to the quiet pass of a wave-1 probe, `…:253`").

## Finding 3 — `:183-184` says the rows "restate the content-revision emission"; no receipt ever observed the declared six-leg set, and the next sentence says so

Impacted axis: C1 (the correction's central freeze/deciding distinction).

```
$ git show c7586b9a:corpus/lessons/round-48.md | sed -n '183,187p'
  The round-47 standing rows, which restate the content-revision emission, declare
  {env, fleet-root, node} (`SCORECARD.md:2270`) and {bwrap, node} (`SCORECARD.md:2276`); the
  deciding run at `8b0e15d2…` observed {fleet-root, node} and {bwrap, node} and scored the
  `six-leg` row `DEPS-MISMATCH`
```

Evidence that the attributive clause is unsupported for `six-leg`:

- `grep -rn "observed_deps=env,fleet-root,node" .ufo/evidence/round-47 .ufo/waves/round-47` → **no
  match**. The set occurs once only, as the *declared* side of
  `.ufo/evidence/round-47/after/c1.stdout:5` (`declared_deps=env,fleet-root,node
  observed_deps=fleet-root,node DEPS-MISMATCH`).
- `before/c1-at-freeze.stdout:5` and `control/emit-observed-pre-freeze.out:5` both observe
  `fleet-root,node`.
- Round 47's own cross-check already concluded exactly this:
  `.ufo/waves/round-47/w1/T47ConnCross.md:96-99` — "counter-emitted (freeze) `fleet-root,node` /
  landed in SCORECARD `env,fleet-root,node` / agree? **NO**"; `:465-469` — "The landed clauses are
  not the counter's output."

So the sentence repeats `SCORECARD.md:2314`'s framing ("The rows above restate the
content-revision `--emit`") as fact, two lines before reporting the `DEPS-MISMATCH` that refutes it
for that row — and it contradicts `:168`, which traces the same set to a wave-1 probe. The
correction's thesis is that the *provenance* of a set must be named; `:183` names the wrong one.
The operative content (the two declared sets and their cites) is correct; the fix is the clause.
Smallest safe correction: "The round-47 standing rows **declare** {env, fleet-root, node}
(`SCORECARD.md:2270`) and {bwrap, node} (`:2276`); only the second matches the content-revision
emission the file says they restate."

## Finding 4 — C1-R48-2's corrected row narrows the flip's subject to the staged id `S205` while `:268` says the flip is "kept"

Impacted axis: C1 (checkability of the corrected row's flip condition).

- `corpus/lessons/round-47.md:81` flip: "a row opened **by the lane** that ties selection to an
  own-leg F7 re-sweep decision (F7)".
- `corpus/lessons/round-48.md:270` flip: "a `S205` row opened `mined` in the writing round,
  carrying a committed round snapshot whose anchor the entry pins, **and** a named own-leg move
  that consumes change-level selection (F7 re-sweep)."

`S205` is the *staged package's* id, not a lane row (`grep -c 'S205' corpus/SOURCES.md` → 0 at
`c7586b9a`). Lane rows take lane-assigned ids (SOURCES.md carries `S001…S268`), so the normal
admission of this paper in a later round would land under a new id and could not satisfy the
literal condition "a `S205` row" — even though the intent ("a lane-opened row for that document")
is met. The claim at `:268` that "the flip condition is kept" is therefore not exact: the subject
was narrowed from *any lane row for the document* to *the staged id*.

Also at `:268`, "made checkable" holds for two of the three conjuncts (row status `mined`, committed
snapshot with the anchor pinned — both greppable under the SOURCES.md row grammar) but not for the
third, "a named own-leg move that consumes change-level selection (F7 re-sweep)", which has no
predicate in the lane.

Smallest safe correction: "a row opened for `S205`'s document (arXiv 1810.05286) — under the staged
id or a lane id — opened `mined` in the writing round, …"; and drop "made checkable" to "with the
row/snapshot/anchor part checkable".

## Finding 5 — `:248` says `PROVINCE.md:14-18` say nothing about "evidence admission"; line 16 is an admission rule

Impacted axis: C1 (the correction's characterization of the text it demotes).

`PROVINCE.md:16-17` (at `c7586b9a`, sha256 `b2875fe21f381d98…`):
"tameshi owns only the reusable craft (**a pattern is admitted from evidence in TWO independent
lanes** before it is claimed general)".

`round-48.md:248`: "They say nothing about test selection, cost baselines or **evidence
admission**". That list goes beyond the ruling it cites: `round-47-verifier-spotcheck.md:90` says
only "those lines refuse product domains and sibling gates, not test selection". What the lines do
not address is the *registry* admission of a source row (QUALITY 10), not evidence admission as
such. Smallest safe correction: replace "evidence admission" with "registry admission of a source
row" (or drop the term).

## Finding 6 — low: the appended rule's "named beside it" has no mechanical reading, and round 48 satisfies it only at block level

Impacted axis: C1 (the rule's own checkability).

`round-48.md:189-190`: "a dependence set is restated only from the deciding `--emit`, with that
receipt's path and revision named beside it". Round 48's own rows do not name a receipt or revision:
the naming lives only in the block header, `SCORECARD.md:2326`
(`… --rev 15b1521ea2e95d0d708059458c090e9f334adf32 --base 473336… --work EMPTY_DIR --emit`,
"receipt `.ufo/evidence/round-48/calibration/emit-15b1521.stdout`"), while the rows at
`SCORECARD.md:2334` (`six-leg`) and `:2340` (`hermetic`) end at `deps …, runs 3 stable`. A
block-level reading makes the round compliant, a per-row reading makes it a violation, and the rule
does not say which. Smallest safe correction: "… with that receipt's path and revision named beside
the row, or in the header of the block that declares it".

---

## Bounds of this review

- Attacked only the two corrections and the citations they rest on. No verdict on `C1_R48_PASS`,
  `C2_R48_PASS`, the deciding run or any control; no counter invocation, no probe, no mutation.
- Did not touch `corpus/`, `tools/`, `SCORECARD.md`, the jj state or the Git index; no `git`
  write command; no `agent://all` message.
- Scratch dir `/fast/scratch/hyaku/tameshi-r48/T48A2CritLessonCorrections` was created for the
  bounds check and removed before this report was written; nothing was left on disk. No `/tmp`
  file, no clone, no install or upgrade (no tool changed, so no tooling record).
