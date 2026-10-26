# T48A2ScribeReportSources — `## Sources & frontier` draft, round 48 attempt 2

Lane `tameshi-shokunin`, base `473336d9d789f6081195e7376d17836a24666bc3`, content revision
`c7586b9a10effc63b4bd327f976edc094c1bdc17` (lane HEAD at this reading `17cc5ce`). Contract
`.ufo/evidence/round-48/contract.json` read in full, all ten amendments included; not edited. I ran no claim counter,
scored no control, and took no deciding measurement. Every number below was re-derived by the command printed beside it.

## Deliverable

`.ufo/waves/round-48/a2w1/T48A2ScribeReportSources.draft.md` — the `## Sources & frontier` section, paste-ready. It
carries the six required elements in the round-47 report's order: rows before→after + counting command, rows added by
tier, rows touched old→new, frontier rows advanced, `Assimilation: none` with its reason, the considerthese line and the
mined mistakes.

## Behaviour observed (all first-hand, read-only)

### Rows before → after

```sh
git show 473336d9d789f6081195e7376d17836a24666bc3:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'   # 124
git show c7586b9a10effc63b4bd327f976edc094c1bdc17:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'   # 128
scripts/sources-census.sh census --file tameshi-shokunin/corpus/SOURCES.md
#   file rows 128 · tier.A 114 · tier.B 11 · tier.C 3 · status.mined 100 · queued 22 · rejected 6 · exit 0
```

Tier arithmetic closes both ways: base `111 A / 10 B / 3 C` = 124, rev `114 A / 11 B / 3 C` = 128
(`awk -F'|' '/^ *\| *S[0-9]/{gsub(/ /,"",$5); print $5}'` on each blob).

### Census receipts

| receipt | lines | codes | exit |
|---|---|---|---|
| start `.ufo/evidence/round-48/census-start.stdout` (05:33) | 12 | 1×W01 (S101), 10×W04 | `0`, stderr 0 bytes |
| end `.ufo/evidence/round-48/census-end.stdout` | — | — | **not written yet** |

The end receipt is not on disk because `.ufo/evidence/round-48/after/` does not exist yet: `deciding-run.sh:34` is what
copies `after/census.stdout` to `census-end.stdout`, and the deciding run has not landed at this reading. The end state
is therefore taken from two committed wave receipts for the same tree — `.ufo/waves/round-48/a2w1/T48W2ExecC2Run-census.out.txt`
(10:30:41 −0300) and `.ufo/waves/round-48/a2w1/T48W2CritC2Rows.census.out.txt` (10:34:56 −0300) — and from my own
read-only run. Verbatim output of my run (scratch dir, sha256 of the file `335ced1d1561c766…`, 1528 B, stderr 0 B):

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	W04	S104 duplicate url cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 across scopes
tameshi	W04	S160 duplicate url stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants across scopes
tameshi	W04	S265 duplicate url testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html across scopes
tameshi	W04	S266 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S267 duplicate url github.com/containers/bubblewrap/blob/v0.13.1/bwrap.xml across scopes
tameshi	W04	S268 duplicate url www.tensorflow.org/federated/golden_tests?hl=zh-cn across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
```

16 lines, 1×W01, 14×W04, 0 E codes (`grep -cE '\bE[0-9]{2}\b'` → 0), exit 0. Delta vs start: exactly the four W04 lines
S265–S268, the expected shape of a superseding row that repeats its predecessor's URL under a new scope; no E04/E03, so
`deciding-run.sh` step 3 (`[ census.exit = 0 ]`) is satisfied by the tree as it stands.

### Rows added by tier, and columns

`git show c7586b9a:corpus/SOURCES.md | awk -F'|' '$2 ~ /S26[5-8]/{…}'` →

| row | tier | kind | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|
| S265 | A | docs | mined | 2026-10-26 | 730d | `corpus/knowledge/repeated-control-precondition.md` |
| S266 | A | docs | mined | 2026-10-26 | 90d | `corpus/knowledge/incremental-pin-disposition.md` |
| S267 | A | docs | mined | 2026-10-26 | on-release | `corpus/knowledge/regression-tally-completeness.md` |
| S268 | B | docs | mined | 2026-10-26 | 180d | `corpus/knowledge/r8-golden-update-flag.md` |

A=3, B=1, C=0; all four sit at `corpus/SOURCES.md:140-143`.

### Rows touched old→new

`git diff --shortstat 473336d9 c7586b9a -- corpus/SOURCES.md` → `1 file changed, 4 insertions(+)`. No existing registry
row's cells changed. The pointer work is in the four knowledge entries (`git diff --stat 473336d9 c7586b9a --
corpus/knowledge corpus/lessons` → `5 files changed, 390 insertions(+), 8 deletions(-)`: the four entries plus the
lesson):

- `repeated-control-precondition.md` — `S026 — … sha256 ca1145fb…` → `S265 (supersedes S026) — … sha256 a4c5c46b…`;
  `verified-at: 2026-10-20` → `2026-10-26`
- `incremental-pin-disposition.md` — `…S047 — the same URL…` → `…; S266 — https://pitest.org/quickstart/incremental_analysis/ — §Incremental analysis`;
  `verified-at: 2026-10-20` → `2026-10-26`
- `regression-tally-completeness.md` — `…S093 — …; S094` → `…; S267 — the same bwrap.xml at tag v0.13.1…; S094`;
  `verified-at: 2026-10-23` → `2026-10-26`
- `r8-golden-update-flag.md` — `…S108 — …` → `…; S268 — the same zh-cn URL, re-anchored 2026-10-26`; `verified-at: 2026-10-24` → `2026-10-26`

### Frontier rows advanced

S265–S268 are the contract's `frontier_step`. Each anchor names a committed 2026-10-26 snapshot and its 12-hex digest:

| row | snapshot | bytes | sha256 (12) | receipt |
|---|---|---|---|---|
| S265 | `freshness/sources/S026.html` | 236387 | `a4c5c46b4af9` | 2026-10-26T08:40:51Z, 200 |
| S266 | `freshness/sources/S048.html` | 8892 | `e9cbc3e1ab7c` | 2026-10-26T08:40:42Z, 200 |
| S267 | `freshness/sources/S093.xml` | 33289 | `2cb77df2f4be` | 2026-10-26T08:41:10Z, 200 |
| S268 | `freshness/sources/S108.html` | 111409 | `04e4c091715a` | 2026-10-26T08:41:18Z, 200 |

(`sha256sum` on each named path — S108 begins `S1`, so an `S0*` glob lists three of four.) No frontier F-row changes
status: `grep -c 'S265\|S266\|S267\|S268' corpus/README.md` → `0`, and the candidate-source cells still name base ids
only (F3 `corpus/README.md:80`, F4 `:81`, F5 `:82`, F7 `:84`). F3/F4/F5/F7 stay `open` — a re-anchor repairs freshness
of ground already counted.

### Assimilation, considerthese, mistakes

- `Assimilation: none`, reason from `.ufo/waves/round-48/w1/T48ScoutPackage.md`: no claim needs a package row; every
  staged row touching the four targets is held or already adopted (S216→S260, S209=S107, S212/S210 are alternate
  carriers with no live-page snapshot); staged ids S153–S255 still collide with held S153–S160, so no map is needed.
- considerthese line `corpus/lessons/round-48.md:9` (`considerthese: idea 5 mined (section below)`); section at `:364`.
- Mistakes: 9 rows (`awk '/^## Mistakes/,/^## considerthese/' … | grep -cE '^\| \`'` → 9; 7 in the main table + 2
  appended blocks), classes `landing` 4, `attribution` 1, `provider` 1, `reference-drift` 1, `scope` 1, `stale-premise`
  1; seven red-state commands `d1`–`d7`.

## Gates this draft clears

- Section spec (round-47 report / round-35 skeleton): all six elements present, each with a command or receipt pointer.
- Census: start exit 0, end state exit 0, 0 E codes, no new warning class (W04 only), four expected W04s named.
- Arithmetic closure: 124→128 = +3 A +1 B, both by the blob count and the census `rows` metric.
- No placeholder text, no invented receipt: the one receipt not yet on disk is named as pending with the script line that
  writes it.

## Touched surfaces

- Written: `.ufo/waves/round-48/a2w1/T48A2ScribeReportSources.draft.md` (deliverable) and this report.
- Not written: `corpus/SOURCES.md`, `corpus/knowledge/*`, `corpus/lessons/round-48.md`, `tools/`, `SCORECARD.md`, any
  `.ufo/evidence/round-48/**` path, any counter, any Git index/jj state. All commands were `git show` / `git diff` /
  `grep` / `awk` reads, plus one `sources-census.sh validate` (stdout only, no `--out`).
- Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2ScribeReportSources/` deleted at the end of the seat (verified gone).
- No tool installed or upgraded; no pacman call; no model passed.

## Findings

- **F1 — the end receipt is the deciding run's, not a missing artefact.** `census-end.*` is written at
  `deciding-run.sh:34`; it is absent now only because `after/` does not exist. The report's final text must cite the
  deciding run's receipt when it lands; the draft says so explicitly instead of citing a file that does not exist. No
  contract change needed.
- **F2 — the four rows are insertions only, so `Rows touched old→new` is empty at the registry level.** Anyone reading
  the section expecting a modified-row count should read the knowledge-entry table; a naive `git diff --stat` on
  `SOURCES.md` shows `4 insertions(+)` and no deletions.
- **F3 — S026 is the only citation that is replaced rather than appended.** S093 and S108 keep their ids beside the
  successor; S026's slot becomes `S265 (supersedes S026)`, so its `source:` line still holds the token once
  (`grep -o 'S026' | wc -l` → 1 on both blobs) while the citing id changes.
  Legal under C2 (which binds the entry set, not the prose) but inconsistent; the section states it rather than
  smoothing it over.
- **F4 — the S108 glob trap.** `.ufo/evidence/round-48/freshness/sources/S0*` matches three snapshots, not four;
  a digest table built from that glob would silently drop S268's snapshot. The draft names each path.
- **F5 — `sources-registry` is a C1 statement** whose value is the rows metric (contract `separability`). The section
  states 128 as read at `c7586b9a`/HEAD `17cc5ce`; if any later seat writes `corpus/SOURCES.md`, both this number and
  the `sources-registry` standing row move together, and the section must be re-derived rather than edited.

## Out of scope / not done

C1/C2 counting and control scoring; the deciding run; the freshness counter's verdict; the report's other sections
(Work performed, Landed changes, Before → after measurements, Trend verdicts, SHONEN). No cure attempted for F1–F5
beyond wording the draft so it cannot be read as citing a receipt that does not exist.

## Provenance

Base `473336d9…`, content `c7586b9a…`, HEAD `17cc5ce`; contract and amendments read from
`.ufo/evidence/round-48/contract.json`; packages from `.ufo/waves/round-48/w1/`; census script
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (read-only, `--out` never passed). Scratch deleted; no tree
left on disk.
