# DraftProvinceReadme — round 26 wave 1: PROVINCE Core append + corpus README round-26 block

Seat: `TameshiR26.DraftProvinceReadme` (scribe, leaf — no subagent dispatch). Date: 2026-10-22.
Scope: two **fenced drafts** for the L1 (the sole integrator) to land:
(1) `PROVINCE.md` — `## Core — round 26 append (2026-10-22)`, in the shape of its round-18 append;
(2) `corpus/README.md` — `## Round 26 — ninth recorded case, round-25 record repair`, carrying the
coverage-map row for the ninth leg and the per-row frontier disposition.
Nothing else in the lane was edited: no production file, no registry row, no `jj` command anywhere,
no git write command. My report file is the only file I wrote.

## Verdict

**Both blocks are already landed** by the L1 at `40a12bf` (HEAD is now `2b064cf`). My drafts below are
therefore delivered as **corrections to the landed text**, not as new appends: they are the same two
blocks re-cut with (a) the house `Corrections to lines N and M above, appended:` shape, (b) the
coverage-map row shape rounds 16/18 used for a new note, (c) the F1b survivor denominator that the
landed text leaves at 35, (d) per-row frontier dispositions the landed text collapses to one
sentence, and (e) the kill-rate ledger debt the landed text calls "superseded" while the ledger file
is unedited.

Verified at HEAD `2b064cf` (clone, read-only): `C1_DEPTH: recorded_cases=9 wired_legs=9
depth_score=9`, exit 0; `C2_RECORD: mismatches=0/3`, exit 0; `MTE_INTEROP: PASS
legs_conforming=9/9`, exit 0; `REGRESSION: PASS (cases=9 passed=9)`. **Nine recorded legs** is the only
count that moves, and **no `corpus/README.md` frontier row moves to Core**.

Three things the L1 must still decide (details in *Findings*):

- **F1b's denominator is 40, not 35.** `corpus/README.md:393` still prints "the 35 recorded
  survivors"; the nine committed `TABLE_*` rows of `tools/mutate-and-run.sh` sum to **40** (the
  eight-leg sum reproduces the published 35 exactly).
- **The kill-rate ledger is unedited** while its own cite-check cells still read "probe only, 1/4 …
  full sweep open". Rounds 16 and 18 each appended a ledger section for their case.
- **The landed README block folds a routed defect into F1's status sentence** — routed item 4 (emitted
  reports carry no lane/revision pin) is a defect of `tools/mte-interop.py`, not a condition of F1 or
  F1b.

---

## 1. Draft A — `PROVINCE.md`, the round-26 block re-cut

The L1's block is landed at `PROVINCE.md:107-118` (commit `40a12bf`). This is the same block with the
file's own round-16 correction shape restored (`PROVINCE.md:59-64`) and the two stale anchors it
leaves (`PROVINCE.md:29`'s "six recorded mutation legs", `:33`'s `tools/mutate-and-run.sh:84-89`)
carried into it. Shape follows `PROVINCE.md:73-83` (round-18 append) plus that corrections shape.

```markdown
## Core — round 26 append (2026-10-22)

Appended; lines above are unchanged. The recorded mutation legs are now
**nine**. The ninth is kumitate `scripts/cite-check.mjs` (rev
`1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`, blob sha256
`40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`), ledger leg
`js-cite-check`, probed read-only as a kumitate `scripts/*` primary surface
(lines 7-11); kumitate owns the gate and its registry row (kumitate
`SKILL.md:599`, `PROVINCE.md:15`). Not a service run; no opt-in needed.
Survivor recommendations travel to kumitate in the round report; tameshi never
edits the gate.

Corrections to lines 29, 33 and 101-102 above, appended:

- Line 29's "the six recorded mutation legs' gates" reads nine. The recorded
  legs are kumitate `scripts/kimi-census.mjs`, `scripts/claims-check.mjs`,
  `scripts/round-gate.mjs`, `scripts/sources-check.mjs` and
  `scripts/cite-check.mjs`; kagi `corpus/surface-census.sh` and
  `corpus/checklist-run.sh`; tsukuroi `tools/tsukuroi-census.sh`; mado
  `tools/mado-verify.sh`. The runner's ledger list now sits at
  `tools/mutate-and-run.sh:87-95` (its header at `:83` reads "r26 nine"), so
  line 33's round-1 anchor `:84-89` and the round-16 append's seven-leg list
  at `:85-91` are dated readings.
- Lines 101-102's "the eight recorded ledger legs" read nine from round 26 on:
  `tools/mte-interop.py` emits and checks all nine
  (`MTE_INTEROP: PASS legs_conforming=9/9`, exit 0;
  `.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`).
```

Shape notes for the L1:

- Round-18 names the owning lane's contract (`kumitate-sources-v1`). **cite-check has no contract
  id** in kumitate: its gate row (kumitate `SKILL.md:599`) says only "citations inside `SKILL.md` +
  `corpus/**`". So the draft cites the registry row it can cite and does not invent a contract name.
- Line 29's "six" and line 33's `:84-89` are dated by the append, not rewritten — same rule the
  round-16 append used when it corrected lines 8 and 35.
- "read-only" is exact: the runner materializes the target from kumitate's git object store
  (`tools/mutate-and-run.sh:9-10`, `:116`, `:1152-1156`), so kumitate's working tree is never read
  or written by this lane's sweep.

## 2. Draft B — `corpus/README.md`, the round-26 block re-cut

The L1's block is landed at `corpus/README.md:401-416` (commit `40a12bf`). This is the same block
with the coverage-map row shape rounds 16/18 used for a new note (`corpus/README.md:262-264`,
`:264-265`), the per-row frontier disposition, the F1b denominator, the F5 scope note and the ledger
debt made explicit. Shape follows the round-18 block (`corpus/README.md:258-276`). Read first:
`## Frontier` (`:78-87`), `## Frontier — status correction` (`:105-121`) and the round-25 block
(`:379-399`).

```markdown
## Round 26 — ninth recorded case, round-25 record repair

Appended; rows above keep their line numbers. QUALITY 7: the new note gets
its row in the same round.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/mutation-case-kumitate-cite-check.md` | case 9: kumitate `scripts/cite-check.mjs` @ `1205c662`, 5/10 killed, 10/10 pre-registered verdict predictions held, hermetic 62-case group only (the gate's 9 integration-group checks do not run under `--selftest`); four survivors are suite holes with off-suite hermetic witnesses, one is an equivalent mutant and stays a survivor in the recorded table; ledger leg `js-cite-check` | S088, S089, S052; `lessons/round-26.md` |

**Frontier — no row moves to Core.** The ninth leg is Core ground already: the
recorded mutation legs are the Core surface at `PROVINCE.md:28-38`. Row by row:

- **F1** stays held for its report-interop half and **F1b** stays open. The
  round-25 status correction above counts eight ledger legs where the interop
  check now covers nine (`MTE_INTEROP: PASS legs_conforming=9/9`, exit 0;
  `.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`), and F1b's survivor
  denominator moves from 35 to 40: the nine committed `TABLE_*` rows of
  `tools/mutate-and-run.sh` sum to 40 recorded survivors, and the eight-leg sum
  reproduces the 35 already printed at line 393. NoCoverage is still not
  claimed, so F1b stays open.
- **F2** stays open: the ninth leg is a JS gate with verdict predictions, not
  the bash witness split its next move names.
- **F3** stays open: the ninth sweep ran one control
  (`.ufo/evidence/round-26/cite-check/sweep/sweep.txt`, one `CONTROL:` line),
  not the N ≥ 3 byte-identical controls its next move asks for.
- **F4**, **F6**, **F7**, **F9** and **F10** are untouched by this round.
- **F5** keeps the round-21 admission of its finite method over the frozen
  nine-surface population (`.ufo/evidence/round-21/c2-contract.json`), which
  does not contain cite-check. The "not measured here" at line 336 is scoped to
  that differential; cite-check is measured as a mutation case from round 26 on.
- **F8** stays open: the ninth case adds hermetic off-suite witnesses for four
  survivors and a code-level equivalence proof for the fifth, but those
  witnesses are pristine-derived differentials, not a survivor classified
  against an independently anchored expectation.

**Round-25 record repair (C2).** The three routed items of
`corpus/lessons/round-25-verifier-spotcheck.md:189-199` are closed by this
round's landing: item 1 by the active registry rows `mte-interop-selftest` and
`mte-interop-check` (`tools/registry.json:1001-1013`) and the `SKILL.md:2101`
gate row; item 2 by the appended round-25 correction in `SCORECARD.md` and in
`corpus/lessons/round-25.md`; item 3 by the refreshed `verified-at:` line of
`corpus/knowledge/mte-report-interop.md` (tool sha256 `193ea6e3…` at
`a08e85c5`, selftest 17/17, receipts under `.ufo/evidence/round-26/after/`).
The frozen counter `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE`
reads `C2_RECORD: mismatches=0/3`, exit 0, on the round-26 tree (3/3 at base
`d414079`). Seat MutateC2Counter shows the counter can be defeated in 10 of 26
probes, so the after-value is read together with the wave-2 reviews of the
text itself.

**Kill-rate ledger — owed, not done here.** The ledger's cite-check cells still
read the round-5 probe: a four-defect probe at 1/4 (`:94`), a "probe only, 1/4"
queue row whose prerequisite reads "full sweep open" (`:107`), U4's "the
cite-check probe (1/4) is an indication, not a rate" (`:224-225`) and the
eight-row queue list (`:280`). This sweep supersedes all four; the ledger file
is not edited in this landing, so those cells stay as written until a
round-26 append in the shape of its round-16 and round-18 sections (`:403`,
`:424`) lands. Named debt, owner: the L1.

C1 is a same-ground depth claim (a ninth recorded leg on a kumitate gate); C2 is
a record repair of the round-25 spot-check's routed items 1–3, not new
coverage. No independent cold-read or promotion credit.
```

---

## 3. Gates I ran (exact commands, observed output)

All read-only git, `GIT_OPTIONAL_LOCKS=0`; all counters and checks run in `/tmp` clones or `/tmp`
scratch, never in the lane tree; no `jj` command was run anywhere.

**Pin re-read (read-only, kumitate):**
```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  -
$ … | wc -lc
   2537  126735
```
Matches the frozen contract pin exactly (`.ufo/evidence/round-26/contract.json` → `claims.C1.leg`).

**C1 counter on a clone at the integration commit `a08e85c5`:**
```
$ git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/r26clone
$ git -C /tmp/r26clone checkout -q --detach a08e85c5
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/c1-measure.py --repo /tmp/r26clone
C1_LEG js-kimi-census: WIRED
… (nine WIRED lines) …
C1_LEG js-cite-check: WIRED
C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9
exit=0
```

**C2 counter, three states:**
```
$ python3 …/c2-measure.py --repo /tmp/r26clone            # committed a08e85c5
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: MISMATCH (SCORECARD after round-25 results lacks 'amendment 3'; … 'before_any_after_measurement'; lesson after ## Claims lacks 'amendment 3')
C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=193ea6e32f89; no named .stdout receipt at the revision carries the verified-at selftest count)
C2_RECORD: mismatches=2/3
exit=1

$ python3 …/c2-measure.py --repo /tmp/r26wt2              # working-tree files (tools, SKILL.md, SCORECARD.md, corpus) but NO .ufo/ at all
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: RESOLVED
C2_ITEM R25-SPOT-3: MISMATCH (no named .stdout receipt at the revision carries the verified-at selftest count)
C2_RECORD: mismatches=1/3
exit=1

$ python3 …/c2-measure.py --repo /tmp/r26wt3              # same working-tree files PLUS .ufo/ (so .ufo/evidence/round-26/after/*.stdout is present)
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: RESOLVED
C2_ITEM R25-SPOT-3: RESOLVED
C2_RECORD: mismatches=0/3
exit=0
```

**Report interop at `a08e85c5` (clone, live fleet root for the sibling object stores):**
```
$ uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin
MTE_LEG js-cite-check: CONFORMS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=ok failed=none runner_pct=50 official_rounded_half_up=50)
… (nine CONFORMS lines) …
MTE_INTEROP: PASS legs_conforming=9/9
exit=0
```

**Survivor denominators (parsed from the committed runner at `a08e85c5`):**
```
nine-leg survivors: 40        (JS 2, BASH 2, TSUKUROI 4, MADO 6, CHECKLIST 8, CLAIMS 3, ROUNDGATE 5, SOURCESCHECK 5, CITECHECK 5)
eight-leg survivors: 35       ← reproduces the "35 recorded survivors" already printed at corpus/README.md:393
```

**Registry monitor at `a08e85c5` (clone):**
```
$ python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb
REGISTRY_CHECK: could-not-evaluate (registry invalid: rows[54].source must be <file>@<7-40 hex rev>:<line>, got 'corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)'; rows[55].source must be … )
exit=2
```

**Sweep receipt (committed at `a08e85c5`, `.ufo/evidence/round-26/cite-check/sweep/sweep.txt`):**
`MUTATE_DATE: 2026-10-22T10:02:07Z` · `CONTROL: GREEN (exit=0 …)` · `MUTATE_RESTORE: OK (target-sha256
before=after=40573448…c10c9f)` · `MUTATE: DONE (target=cite-check.mjs defects=10 killed=5 survived=5
inconclusive=0 kill-rate=50%)`. `results.tsv`: 5 KILLED / 5 SURVIVED, matching
`TABLE_CITECHECK` (`tools/mutate-and-run.sh:629`). Regression replay receipt:
`REGRESSION_CASE js-cite-check: PASS`, `match=10/10 … flips=0`, `REGRESSION: PASS (cases=9 passed=9)`.

## 4. Touched surfaces

Only `.ufo/waves/round-26/w1/DraftProvinceReadme.md` (this file). Lane `git status --porcelain` shows
the tracked modifications of other seats/L1 (`PROVINCE.md`, `SCORECARD.md`, `SKILL.md`,
`corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/mte-report-interop.md`, `corpus/lessons/round-25.md`, `tools/registry.json`) and
untracked `corpus/knowledge/mutation-case-kumitate-cite-check.md`,
`corpus/lessons/round-26.md`, `.ufo/evidence/round-26/after/`, `.ufo/waves/round-26/` — none of
them mine.

## 5. Out of scope (not mine, flagged only)

- `corpus/knowledge/fleet-kill-rate-ledger.md` — the ninth case's ledger row (§1 table row 9 and a
  round-26 append section). Round-16/18 precedent appends; finding 5 below.
- `tools/registry.json` rows 54/55 `source` format (finding 2).
- `corpus/SOURCES.md` rows S088/S089 (still uncommitted; the ninth entry's `source:` header cites
  them, QUALITY 10 wants a mined row at the landed revision).
- `corpus/knowledge/mutation-case-kumitate-cite-check.md` — the sibling seat's draft; finding 7
  (kumitate-gate ordinal).
- The C1 counter's weakness (seat MutateC1Counter: eight runner weakenings pass `depth_score=9`,
  including a duplicated leg that also passes the regression companion). Not a PROVINCE/README
  question, but the L1's SCORECARD wording should not read the counter as an independence check.

## 6. Findings for the canonical judge (verbatim where it matters)

1. **C2's `0/3` requires the untracked receipts.** The counter's item 3 demands a named `.stdout`
   receipt that *exists at the revision* with `MTE_SELFTEST: N/N pass`. `.ufo/evidence/round-26/after/`
   is untracked (`?? .ufo/evidence/round-26/after/`), so at any commit that omits it the counter
   reads `mismatches=1/3` (measured). Both receipts must land with the round.
2. **Registry rows 54/55 fail the registry monitor as committed.** At `a08e85c5`,
   `tools/registry-check.py --rev a08e85c5…` exits 2 with
   `registry invalid: rows[54].source must be <file>@<7-40 hex rev>:<line>, got 'corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)'`.
   The working tree already carries the conforming form
   (`corpus/lessons/round-25-verifier-spotcheck.md@d4140796f4e48e8ec81b793facba73fbd03b4443:189-192`);
   it must land with the round.
3. **F1b's denominator is 40, not 35, after the ninth leg** — derived from the nine committed
   `TABLE_*` rows; the same method reproduces the published 35 over the eight prior legs.
4. **F5's "not measured here" needs a scope note.** `corpus/README.md:335-336` reads as if cite-check
   is unmeasured; it is scoped to the round-21 differential population, which excludes cite-check.
   My draft adds the scope sentence rather than editing line 336.
5. **Kill-rate ledger debt.** `corpus/knowledge/fleet-kill-rate-ledger.md:94`, `:107`, `:224-225`,
   `:280` still describe cite-check as a 1/4 probe with "full sweep open". Rounds 16 and 18 appended
   ledger sections for their cases (`:403`, `:424`); round 26 appends none, so the standing view
   contradicts the round-26 sweep until it does. My README draft names it as owed debt, owner: L1.
6. **F8's bar is not met — this is the one frontier call where a second reading is defensible.**
   The round-26 witnesses separate pristine from mutant by observed behaviour — pristine-derived
   differentials, the same shape the round-16 note declined (`corpus/README.md:235-237`). The
   equivalence proof for the fifth survivor is an argument from the pinned source's own control flow
   (`filesScanned++` at `:1556` precedes `resolved++` at `:1583`), not an expectation anchored outside
   the pristine bytes. My draft therefore keeps F8 open. An outside reviewer could argue the
   equivalence classification is "one survivor classified" and so satisfies F8's next move
   (`corpus/README.md:85`); the L1's call, and the row's own wording ("independently anchored
   expectation") is what I weighed.
7. **Sibling entry ordinal (verbatim):** `corpus/knowledge/mutation-case-kumitate-cite-check.md:8`
   reads "The ninth recorded case and the fourth kumitate gate in the ledger."
   (`DraftEntry.md:249`, `:419` repeat it). By the runner's own nine-leg list
   (`tools/mutate-and-run.sh:87-95`) and by the ledger file's own kumitate rows
   (`fleet-kill-rate-ledger.md:45`, `:277`, `:410`, `:432`), cite-check is the **fifth** kumitate leg
   (kimi-census, claims-check, round-gate, sources-check, cite-check). The entry is the sibling
   seat's file; the L1 integrates it, so the ordinal needs the L1's call.
8. **Draft conflicts with the L1's own working-tree text.** The L1 has already staged blocks at
   `PROVINCE.md:107-118` and `corpus/README.md:401-416`. Differences, for the L1 to pick:
   (a) the staged PROVINCE block folds the correction into prose ("Line 101 above … reads nine from
   round 26 on") where the file's own round-16 shape is a `Corrections to lines N and M above,
   appended:` list; (b) the staged README block uses the round-21/25 `| Entry / ground | … |` table
   shape, not the `| Note | Holds | Sources |` coverage-map shape that rounds 16/18 used for a new
   note row, and QUALITY 7 asks for a coverage-map row; (c) the staged README block's sentence "F1
   stays held and F1b open: the emitted reports still name a target by basename with no lane or
   revision pin (routed item 4, open)" folds a routed defect into F1's status sentence — routed
   item 4 is an open defect of `tools/mte-interop.py` (seat ReviewMteLeg9), not a condition of F1
   or F1b.

## 7. Bounds and tooling

- Lane bounds honoured: leaf member, no subagent dispatch; read-only git with
  `GIT_OPTIONAL_LOCKS=0`; **no `jj` command anywhere** (not `jj log`, not `jj st`, not at the fleet
  root); no git write command in the lane repo; no production file edited; no gate, selftest or
  sweep executed inside the lane repo — every counter and check ran in a `/tmp` clone or `/tmp`
  scratch; the kumitate sibling was read only through `git show` / `git status --porcelain`.
- No tool was installed or upgraded; nothing was missing (git, python3, node v24.21.0, uv, jq were
  already present).

## 8. Artifact paths

- This report: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-26/w1/DraftProvinceReadme.md`
- Draft A → `PROVINCE.md` (append at end of file).
- Draft B → `corpus/README.md` (append at end of file).
- Evidence read: `.ufo/evidence/round-26/contract.json`, `.ufo/evidence/round-26/c1-measure.py`,
  `.ufo/evidence/round-26/c2-measure.py`, `.ufo/evidence/round-26/c1-before.stdout`,
  `.ufo/evidence/round-26/c2-before.stdout`,
  `.ufo/evidence/round-26/cite-check/cite-check.defects.spec`,
  `.ufo/evidence/round-26/cite-check/predictions.json`,
  `.ufo/evidence/round-26/cite-check/sweep/sweep.txt`, `…/sweep/results.tsv`,
  `.ufo/evidence/round-26/cite-check/regression-worktree.stdout`,
  `.ufo/evidence/round-26/after/mte-check-a08e85c.stdout`,
  `.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout`,
  `.ufo/evidence/round-21/c2-contract.json`, `corpus/README.md`, `PROVINCE.md`,
  `corpus/knowledge/fleet-kill-rate-ledger.md`, `corpus/knowledge/gates-survey-kumitate.md`,
  `corpus/knowledge/mutation-case-kumitate-cite-check.md`, `tools/mutate-and-run.sh`,
  `tools/mte-interop.py`, `tools/registry.json`, `SKILL.md`, `SCORECARD.md`,
  `corpus/lessons/round-25-verifier-spotcheck.md`.
- Sibling wave-1 reports consulted: `ScoutFrontier.md`, `CriticC1.md`, `CriticEquivalence.md`,
  `CriticC2.md`, `MutateC1Counter.md`, `MutateC2Counter.md`, `InteropCheck.md`, `ReviewMteLeg9.md`,
  `ProbeSUSAGE.md`, `ProbeSOOREDGE.md`, `ProbeSSTRICT.md`, `ProbeSPININCLUDES.md`,
  `ProbeIntegrations.md`, `DraftEntry.md`, `DraftLesson26.md`, `DraftLesson25Correction.md`,
  `DraftSourcesRows.md`, `DraftScorecard.md`, `DraftQuality.md`.
