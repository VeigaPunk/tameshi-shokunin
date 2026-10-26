# T47ExecMirror — C3 scratch mirror dry run

Seat: `T47ExecMirror` (executor leaf, L1 `TameshiR47`). Item: dry-run the C3 integration in a
scratch clone and report the exact recipe and every failure mode. Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` at freeze
`9acfbe21435e1976636a276448dee1d5e7155915`; contract read first, unedited.

Bounds honoured: the lane was touched only for this report file; no lane git/jj command ran; no
write to `/home/vgpnk/Projects/shokuknow`; every scratch file lived under
`/tmp/tameshi-r47-T47ExecMirror/` and was then re-created under
`/var/tmp/tameshi-r47-T47ExecMirror/` after the L1's disk directive (the `/tmp` tree is deleted);
no mutating `jj`; no `agent://all`. No tool was installed or upgraded (nothing was needed; no
pacman/uv/npx call was made). No counter run is a verdict: each run below is against a scratch
fixture revision, never against the lane.

## 1. Fixture

```
mkdir -p /tmp/tameshi-r47-T47ExecMirror
D=$(mktemp -d /tmp/tameshi-r47-T47ExecMirror/clone.XXXX)
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin "$D"
git -C "$D" rev-parse --show-toplevel        # == $D  (checked: OK)
git -C "$D" checkout -q --detach 9acfbe21435e1976636a276448dee1d5e7155915
```

`$D` = `/tmp/tameshi-r47-T47ExecMirror/clone.1l6t`, freeze HEAD `9acfbe2`. Integration commit
`8c934e0` (throwaway identity, only in `$D`):
`git -C "$D" -c user.name='tameshi mirror' -c user.email='mirror@example.invalid' -c commit.gpgsign=false commit`.

After the L1's disk directive (`/tmp` at 100 %) the same integration was re-created from scratch
under `/var/tmp` and re-measured, so the recipe below is confirmed on the new path:

```
R=/var/tmp/tameshi-r47-T47ExecMirror; mkdir -p "$R/files" "$R/receipts"
V=$(mktemp -d -p "$R" clone.XXXX)
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin "$V"
git -C "$V" checkout -q --detach 9acfbe21435e1976636a276448dee1d5e7155915
# the five files of 8c934e0 (SOURCES.md, README.md and the three entries), copied in
cp -r "$R/files/corpus" "$V/"
git -C "$V" add -A
git -C "$V" -c user.name='tameshi mirror' -c user.email='mirror@example.invalid' \
           -c commit.gpgsign=false commit -q -m 'round-47 C3 scratch mirror: rows, entries, index lines'
```

`$V` = `/var/tmp/tameshi-r47-T47ExecMirror/clone.X0R7`, integration commit
`ae1ac25254de3dd9fbcef4611c5d88f1a8e18ff0` (content-identical to `8c934e0`; only the commit object
differs). The `/tmp` tree, including the probe clone, is deleted; the quote checker and every
transcript were carried over to `$R/receipts/`.

## 2. The recipe (exact)

### 2.1 Registry rows — append four rows INSIDE `## Registry`, after the last row (S260 at freeze, line 135), before the blank line and `## Paths`

Each row has exactly 13 awk `|`-split fields (11 cells), no pipe anywhere inside a cell, no ASCII
space before `|` (0-3 leading spaces parse; 4+ are code and are ignored). Snapshot digests, computed
from the committed bytes at freeze:

| snapshot | bytes | sha256 | prefix used |
|---|---|---|---|
| `.ufo/evidence/round-47/coverage/sources/arxiv-2302.09330-abs.html` | 43549 | `2965343ceaac627ccf71f587d3108073c6b45e08b89db3bbe1521a5716e14bc6` | `2965343c` |
| `.ufo/evidence/round-47/coverage/sources/arxiv-2607.09345-abs.html` | 44459 | `16ecdefca1f247d3acef2439576ca380bd0bacdd2fa1215e16c71006547a925d` | `16ecdefc` |
| `.ufo/evidence/round-47/coverage/sources/s2-icst24-cost-of-flaky.json` | 3116 | `6ab5b3f58b27827c265422f958689bbeda4514286a532b3ce2f4a6b720bfde06` | `6ab5b3f5` |
| `.ufo/evidence/round-47/coverage/sources/lam-2020-reruns.txt` | 81725 | `bf52c9089e331f18bb65c3c03449de070723c7ec52725c0e6dc84ca249b025b9` | `bf52c908` |
| `.ufo/evidence/round-47/coverage/sources/lam-2020-reruns.pdf` | 565435 | `0b88045817f146db3eb26d305c864291010e5c083aa8d5cac480be3c5350895d` | `0b880458` |

Rows as committed in the dry run (verbatim; the four counted/extra cells the counter actually reads
are `cells[2]` source URL, `cells[6]` anchor, `cells[8]` status `mined`, `cells[11]` used-by):

```
| S261 | Practical Flaky Test Prediction using Common Code Evolution and Test History Data (Gruber, Heine, Oster, Philippsen, Fraser; arXiv 2302.09330) — https://arxiv.org/abs/2302.09330 | paper | A | F3's measurement half — a published predictor of flaky tests built only from records a run already leaves behind | §Abstract @ arXiv:2302.09330v2 (v1 2023-02-18; last revised 2023-03-18), snapshot .ufo/evidence/round-47/coverage/sources/arxiv-2302.09330-abs.html 43549 B sha256 2965343c | F1 95.5% from three features (flip rates, source-file changes in the last 54 days, changed files in the most recent pull request) on 100 flaky and 100 non-flaky histories; the method needs no additional reruns | mined | 2026-10-25 | 365d | corpus/knowledge/flaky-aware-verdict-evidence.md |
| S262 | Understanding Reproducibility and Characteristics of Flaky Tests Through Test Reruns in Java Projects (Lam, Winter, Astorga, Stodden, Marinov; IEEE ISSRE 2020 camera-ready) — https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf | paper | A | F3's rerun budget and test-order axis — 4000 reruns per suite make NDOD versus NDOI separable, and five reruns still check a failure correctly ≥ 82% of the time (extra row: the round-47 C3 counter counts the three frozen documents only) | §Abstract and §Guidelines (RQ1 & RQ3; RQ2 & RQ3), p. 2 @ author-hosted camera-ready, text snapshot .ufo/evidence/round-47/coverage/sources/lam-2020-reruns.txt 81725 B sha256 bf52c908 (PDF 565435 B sha256 0b880458) | many tests called non-order-dependent actually depend on order: 107 flaky tests from 26 modules, each suite run 4000 times, and the majority of NOD tests are NDOD not NDOI | mined | 2026-10-25 | 365d | corpus/knowledge/flaky-aware-verdict-evidence.md |
| S263 | How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection (Gültekin, Berndt, Bell, Bach, Baltes; arXiv 2607.09345) — https://arxiv.org/abs/2607.09345 | paper | A | F7's counter-case — a published argument that flakiness is not a static property of test code and that code-based benchmark scores are inflated by shortcuts | §Abstract @ arXiv:2607.09345v1 (submitted 10 Jul 2026), snapshot .ufo/evidence/round-47/coverage/sources/arxiv-2607.09345-abs.html 44459 B sha256 16ecdefc | code-based detectors' benchmark F1 rests on a labeling shortcut and the evaluation protocol; on CI-mined flaky tests, code plus logs explain 42% and 58% need further execution evidence | mined | 2026-10-25 | 365d | corpus/knowledge/r8-flakiness-not-static.md |
| S264 | Cost of Flaky Tests in Continuous Integration: An Industrial Case Study (Leinen, Elsner, Pretschner, Stahlbauer, Sailer, Jürgens; IEEE ICST 2024; DOI 10.1109/ICST60714.2024.00037) — https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST60714.2024.00037?fields=title%2Cabstract%2Cyear%2Cvenue%2Cauthors%2CexternalIds | paper | B | F7's cost baseline — flaky tests cost at least 2.5% of developer time while an automatic rerun costs 0.02 cents against $5.67 for a manual investigation | §Abstract on the Semantic Scholar graph record (DBLP conf/icst/LeinenEPSSJ24), snapshot .ufo/evidence/round-47/coverage/sources/s2-icst24-cost-of-flaky.json 3116 B sha256 6ab5b3f5 | a rerun is nearly free and the failed pipeline is not: 0.02 cents versus $5.67, which is why the authors shift effort toward automatic rerunning | mined | 2026-10-25 | 180d | corpus/knowledge/r8-flaky-cost-baseline.md |
```

Two mandatory details in that text:

- **S264's URL must keep `%2C`.** `measure.py`'s `URL_RE = https?://[^\s;,)]+` stops at a literal
  comma, so an unencoded `fields=title,abstract,...` truncates the doc key and the row is silently
  dropped (probe 9 below).
- **The hex in the anchor must be the snapshot's own sha256 prefix.** There is no census code for a
  wrong digest; a stale prefix drops the row from the counter silently (probe 6).

### 2.2 Entries — `corpus/knowledge/{flaky-aware-verdict-evidence,r8-flakiness-not-static,r8-flaky-cost-baseline}.md`

A fixed 3-line header, then prose:

- line 1 begins `source:`, cites the row id(s) (`CITE_RE = \bS\d{3,}\b`), contains the URL and the
  section/fetch date. Line 1 for `flaky-aware-verdict-evidence.md` cites **S261 and S262**; the
  other two cite S263 and S264.
- line 2 `verified-at: 2026-10-25` (ISO date, `>= 2026-10-25`).
- line 3 `recheck: <NNd|symbolic> — <command>` (the census judges the *cell value*: `365d` / `180d`).
- the entry must be named in the cited row's used-by cell and indexed in `corpus/README.md`.

Quote rules that decided the dry run (all verified against the counter's own `fold`/`norm_text`):

| entry | located quote | tokens | fresh vs package copy |
|---|---|---|---|
| flaky-aware | "when trying to deploy these in an industrial context, their reliance on instrumentation, test reruns, or language-specific artifacts was inhibitive" | 20 | fresh |
| flaky-aware | "our approach does not require additional reruns, since it gathers this data from existing test executions" | 16 | fresh |
| flaky-aware | "The best model was able to achieve an F1-score of 95.5% using only 3 features" | 15 | fresh |
| flaky-aware | "Non-deterministically behaving test cases cause developers to lose trust in their regression test suites" | 14 | fresh |
| flaky-aware (S262) | "we run each test suite exactly 4000 times" | 8 | fresh |
| r8-flakiness | "Flakiness is not a static property of test code, which often lacks the information needed to decide whether a test is flaky" | 21 | **in package** (not fresh) |
| r8-flakiness | "Our CodeBERT reimplementations of two published detectors scored far above its constant baselines" | 13 | fresh |
| r8-flakiness | "C-IDoFT is a controlled counterfactual, not a benchmark for reuse" | 10 | fresh |
| r8-flakiness | "The test code and CI log yielded a cause for 42% of them" | 13 | fresh |
| r8-flakiness | "the other 58% required further execution evidence" | 7 | fresh |
| r8-cost | "We analyze five years of development history, including CI test logs, commits from the Version Control System" | 17 | fresh |
| r8-cost | "This effort is divided into investigating potentially flaky test failures, which accounts for 1.1% of the total time" | 18 | fresh |
| r8-cost | "The insights gained from our case study have led to the decision to shift effort from investigation and repair" | 19 | fresh |
| r8-cost | "our case study provides a first step to better understand the costs of flaky tests" | 15 | fresh |

Each quote sits on ONE physical source line: `QUOTE_RE = "([^"\n]{10,400})"` forbids a newline and a
`"` inside the quote, and it also forbids curly-quote reuse of a passage whose original contains
quotation marks (e.g. the PDF's `“non-order-dependent”`).

### 2.3 Index — append a `## Round 47` block at the end of `corpus/README.md`, round-46 style

A `| Note | Holds | Sources |` table with one row per entry, backticking `knowledge/<name>.md`
(both `knowledge/x.md` and `corpus/knowledge/x.md` are accepted; the counter checks the backticked
path, not a table cell). The dry-run block is README lines 579-596 of `8c934e0`.

### 2.4 Runs

```
python3 "$D/.ufo/evidence/round-47/coverage/measure.py" --lane "$D" --rev HEAD
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$D/corpus/SOURCES.md"
bash "$D/.ufo/evidence/round-47/no-harm.sh" "$D" HEAD
```

## 3. Outputs at the dry-run commit `8c934e0`

### 3.1 C3 counter — exit 0

```
ENTRY corpus/knowledge/flaky-aware-verdict-evidence.md
ENTRY corpus/knowledge/r8-flakiness-not-static.md
ENTRY corpus/knowledge/r8-flaky-cost-baseline.md
C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S261,S263,S264 rev=HEAD C3_R47_PASS=true
```

`rows=3` is exactly the three frozen documents: S262 (Lam) is in the registry and cited, but the
counter ignores it — `row_ids=S261,S263,S264`. `covered=3` because every counted row is cited by an
admitted entry. The 23 pre-existing headerless entries print
`REFUSED corpus/knowledge/<x>.md no provenance trio`; that noise does not affect the verdict.

### 3.2 Census validate — exit 0, zero E codes

```
file	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
file	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
file	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
file	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
file	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
file	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
file	W04	S092 duplicate url bazel.build/remote/caching across scopes
file	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
file	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
file	W04	S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
file	ok	/tmp/…/clone.1l6t/corpus/SOURCES.md
```

Eleven warnings (10 × W04, 1 × W01), all pre-existing: `diff` of the `[EW]0x` lines against the
unmodified lane registry is empty (`WARNING-SET-IDENTICAL`). The four new rows add no code. The
`ok` line is emitted because no `E` code is present.

### 3.3 No-harm — exit 0, seven `ok` in 98 s wall

```
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-120 124 ok
NOHARM r46-coverage rows=3 entries=3 C3_R46_PASS=true ok
```

Registry rows 120 → 124. The script `cd`s into the lane argument and reads every counter from the
commit — it works unchanged on a clone.

### 3.4 Frozen id reservation

`corpus/SOURCES.md:478` already reads
`- Next unused id: S265 (S261–S264 are map-only reserved; staged ids S161–S255 stay reserved by document for the package).`
The four ids are therefore pre-reserved at the freeze and the append needs **no** edit to the
`## Id allocation` section. Writing a `Round 47:` paragraph there is lane convention but is not
checked by any of the three commands.

### 3.5 Re-run on the `/var/tmp` path (post-directive)

The same five files, committed fresh on a new clone of the lane at the freeze, reproduce all three
results at `ae1ac25`:

```
C3_R47: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S261,S263,S264 rev=HEAD C3_R47_PASS=true   (exit 0)
census: exit 0, 11 warnings (identical set), 0 E codes, `file  ok  …/clone.X0R7/corpus/SOURCES.md`
no-harm (86.8 s): commandD 9 · coldread 6 · r45-freshness 71/73 · r45-coverage 2/2 · S160 1 ·
                  registry rows 124 · r46-coverage 3/3 — seven ok, exit 0
```

Transcripts: `<R>/receipts/var-tmp-{measure,census,no-harm}.txt` with `R=/var/tmp/tameshi-r47-T47ExecMirror`.
The re-run is independent of the `/tmp` tree (deleted before it started), so the recipe carries no
`/tmp`-specific step.

## 4. Failure modes provoked on purpose

Each probe ran in a second clone `$F` (`/tmp/tameshi-r47-T47ExecMirror/fixture.aWfO`, clone of `$D`
detached at `8c934e0`), one commit per probe, restored with
`git -C "$F" checkout -q 8c934e0 -- corpus` between probes.

| # | provoked defect | census code / exit | C3 counter |
|---|---|---|---|
| 1 | a pipe inside a cell (`flip rates \| churn` in S261 teaches) | `E01 S261 fields=12`, exit **1** | `rows=2 entries=2 covered=2 C3_R47_PASS=false`, exit 1; the flaky-aware entry is refused **silently** (`why == 'cites no flaky row'` is not printed) |
| 2 | recheck prose cell (`90 days`) | `E09 S261 recheck=90 days`, exit **1** | **blind**: `rows=3 entries=3 C3_R47_PASS=true`, exit 0 |
| 3 | duplicate URL, same scope (S266) | `E04 S266 duplicate url arxiv.org/abs/2302.09330 within scope …`, exit **1** | rows counted per row id, not per document: `rows=5 … covered=3 PASS=false` |
| 3b | duplicate URL, other scope (S267) | `W04 S267 duplicate url arxiv.org/abs/2302.09330 across scopes`, exit **0** alone | same inflation (`rows=5`, PASS=false) |
| 4 | used-by path that does not exist (`…-typo.md`) | `E11 S263 missing used-by corpus/knowledge/r8-flakiness-not-static-typo.md`, exit **1** | `REFUSED … r8-flakiness-not-static.md not in used-by`, `entries=2`, exit 1 |
| 5 | entry not indexed (round-47 cost row deleted from README) | none, exit **0** | `ENTRY … r8-flaky-cost-baseline.md (not indexed)`, `indexed=2`, exit 1 |
| 6 | stale snapshot digest (`deadbeef` in S261 anchor) | none, exit **0** | `rows=2`, PASS=false, entry refused silently |
| 7 | package entry relabelled (only quotes already in the package copy) | none | `REFUSED … no quote fresh against the package copy`, `entries=2` |
| 8 | `verified-at: 2026-10-24` | none | `REFUSED … verified-at`, `entries=2` |
| 9 | S264 URL with literal commas (`fields=title,abstract,…`) | none, exit **0** | `rows=2`, PASS=false, refusal silent |

Cross-cutting reading of the matrix: the census and the counter are **complementary, not redundant**.
The census owns cell shape, id, URL duplication, status/kind/tier enums, dates and on-disk used-by —
and it is blind to digests, quote location, freshness and indexing. The counter owns digest + snapshot
path, quote location/freshness, `verified-at`, indexing and the covered==rows equality — and it is
blind to recheck format, cell count (it just drops the row), duplicate rows (they inflate `rows`) and
URL encoding. A green counter with a red census (probe 2) and a red counter with a green census
(probes 5, 6, 7, 8, 9) are both reachable, so both commands are required in the integration gate.

## 5. Defects found in the frozen artifacts (do not fix here; route to L1)

1. **S263 author line.** The package copy `.ufo/evidence/round-47/assimilation/package/r8-flakiness-not-static.md`
   attributes arXiv 2607.09345 to "Baltes, McKim, Zaidman, Wagner". The committed snapshot
   `arxiv-2607.09345-abs.html` lists **Ömer Oktay Gültekin, Alexander Berndt, Jonathan Bell, Thomas Bach, Sebastian Baltes**.
   The counter checks neither the author list nor the title, so a byte-copied attribution would pass.
   The dry-run row and entry follow the snapshot and say so in the entry's boundary section.
2. **S264 venue metadata.** The committed graph record's `venue` field reads
   "International Conference on Information Control Systems & Technologies", which is not ICST. The
   DOI and `conf/icst/LeinenEPSSJ24` identify the venue; the row and entry follow the DOI. Again
   counter-blind. Related: the package line 1 lists "Jürgens" while the record spells "Elmar Jurgens".
3. **Counter row identity.** `flaky_rows()` keys rows by **id**, so any second row naming a frozen
   document (duplicate, or a deliberate second carrier) raises `rows` and breaks `covered == rows`
   unless it is cited too — the contract's `covered==rows` equality is therefore only satisfiable by
   a one-row-per-document registry. Worth stating in the round-47 lesson.
4. **Noise.** 23 `REFUSED … no provenance trio` lines are printed on every run; the pass line is
   still unambiguous, but a reader can mistake volume for failure.

## 6. Risks for the real integration

- The four-row append changes the registry from 120 to 124 rows; `no-harm` needs ≥ 120 — fine.
- `no-harm` takes ~98 s because of its coldread and round-45/46 counter monitors; budget it.
- If the wave chooses a different *counted* mapping (e.g. `r8-flakiness-not-static.md` citing two
  rows), remember `covered == rows` must still hold, and every counted row needs exactly one row.
- The counter reads `corpus/README.md` and the package copies **at the rev under test**; an
  uncommitted README edit is invisible to it (`git show REV:path`). The dry run's first pass proved
  this implicitly: only committed state is scored.
- Everything above was measured in `/var/tmp` (and, before the disk directive, `/tmp`) clones;
  nothing here is a verdict on the lane.

## 7. Retained evidence

Everything lives under `/var/tmp/tameshi-r47-T47ExecMirror/` (the `/tmp` tree is deleted):

- `files/corpus/…` — the five dry-run files; copied over a fresh clone of the lane at the freeze
  they reproduce the integration commit (`git add -A`, throwaway-identity commit).
- `receipts/var-tmp-measure.txt` — counter transcript at `ae1ac25` (exit 0, `C3_R47_PASS=true`).
- `receipts/var-tmp-census.txt` — census transcript (exit 0, 11 warnings, 0 E codes, `ok` line).
- `receipts/var-tmp-no-harm.txt` — the seven-monitor transcript (exit 0).
- `receipts/out-measure.txt`, `out-census-dry.txt`, `out-census-lane.txt` — the first (`/tmp`)
  run's transcripts, carried over; `out-census-lane.txt` is the unmodified-lane baseline whose
  warning set is identical to the dry-run registry's.
- `receipts/work/qcheck.py` — the quote locator/freshness checker that reproduced `measure.py`'s
  `fold`/`norm_text`/`QUOTE_RE` before any entry file was written.
- `receipts/dryrun-commit.txt` — the `/tmp` integration commit id and message.

Both scratch clones are now deleted, as the L1's directive requires (`/tmp` tree and the
`/var/tmp` clone `clone.X0R7`); the directory above is 212 KB, files and transcripts only. The probe
clone (`fixture.aWfO`, nine failure probes) went with the `/tmp` tree; each probe is recorded in §4
with its exact command shape (`git -C "$F" checkout -q 8c934e0 -- corpus` between probes) and its
observed code, so any of them is one edit plus one commit to reproduce.

## 8. Blockers

None. The recipe above reproduces `C3_R47_PASS=true` with `rows=3 entries=3 indexed=3 covered=3`,
census exit 0 with zero new codes, and seven `ok` no-harm monitors.
