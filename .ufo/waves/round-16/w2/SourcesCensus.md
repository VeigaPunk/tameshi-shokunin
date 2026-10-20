# Sources census — wave 2 falsifier (TameshiR16.SourcesCensus)

Target: lane `tameshi-shokunin` at `c699c8c36d6e4eca4b796b81a8247904aa145ec8`;
fleet validator `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
and the seven frozen manual census commands in `CORPUS.md` §SOURCES.md.
No tool installed or upgraded.

Method: `git -C <lane> archive c699c8c… | tar -x -C <scratch>/wt` (read-only copy of the
committed tree; no lane write), then all manual commands run from that copy's root.
Scratch: `/tmp/tameshi-r16w2-SourcesCensus-1iqG09` (kept for inspection).
The live lane's `corpus/SOURCES.md` is byte-identical to the committed blob
(sha256 `881a86ad7ec136606b33a453a565c0aac2f24547d49f1e7b89eccfe23ab7bc98` for the
worktree file, `git show c699c8c:corpus/SOURCES.md`, and the /tmp copy), so results
transfer either way.

## Findings (by severity)

**Blocking — none.** **Defect — none.**

**Minor observation (pre-existing, not introduced by S052–S057).**
`corpus/SOURCES.md:62` (S053) is `kind=code` but its `source` cell is a repo path
(`kumitate-shokunin/scripts/round-gate.mjs`), while the frozen shape rule allows
"a repo path or command for `own-work`". The same shape already exists for S032–S037
(round-1/earlier fleet-gate rows: `corpus/SOURCES.md:43-48`), so round 16 follows an
established lane convention; I record the contract-reading tension, not a new breach.
`[INFERENCE: the contract text does not say whether read-only sibling code counts as own-work.]`

**Warning surfaced by the validator.** `W04` on S047/S048 (same PIT URL, different
scopes). This is the documented supersedes chain S041→S047→S048 (S047's teaches opens
`supersedes S041 —`, S048's opens `supersedes S047 —`); `E04` (same URL+scope) is
absent. W-codes never change status (`scripts/sources-census.sh:17-18`). Not a defect.

## Commands, exits, key lines

1. Maintained validator against the live fleet root (Target verbatim):

```
$ cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

2. Same validator on the committed /tmp copy (explicit lane dir):
`scripts/sources-census.sh validate --root /tmp/.../wt /tmp/.../wt` →
`wt W04 S047 …`, `wt W04 S048 …`, `wt ok /tmp/.../wt/corpus/SOURCES.md`, **EXIT=0**.

3. Maintained census, cross-checking the histograms:

```
$ ./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tameshi
tameshi	rows	55
tameshi	tier.A	47
tameshi	tier.B	6
tameshi	tier.C	2
tameshi	status.mined	28
tameshi	status.queued	24
tameshi	status.rejected	3
FLEET	rows	55
FLEET	tier.A	47 / tier.B	6 / tier.C	2 / tier.invalid	0
FLEET	status.queued	24 / status.mined	28 / status.rejected	3 / status.invalid	0
FLEET	missing	0
EXIT=0
```

4. Frozen manual census block (CORPUS.md §"Census — run from the lane root"), run in
`/tmp/.../wt`; per-command exit captured:

| # | command (abbreviated) | stdout | rc |
|---|---|---|---|
| 1 | `grep -cE '^\|…S[0-9]{3,}…\|' corpus/SOURCES.md` | `55` | 0 |
| 2 | malformed rows `NF!=13` | `0` | 0 |
| 3 | tier histogram | `A=47 B=6 C=2 ` | 0 |
| 4 | status histogram | `mined=28 queued=24 rejected=3 ` | 0 |
| 5 | duplicate ids (`sort \| uniq -d`) | *(empty)* | 0 |
| 6 | enum violations / tier inflation | *(empty)* | 0 |
| 7 | mined rows whose used-by paths do not exist | *(empty)* | 0 |

Row count reconciles: 37 ids in S001–S037 + 18 in S040–S057 = 55; tier 47+6+2 = 55;
status 28+24+3 = 55. Ids S038–S039 are absent but explicitly retired (see below), so
they are not a lost row.

Independent sweeps beyond the frozen block:
- no indented row-shaped lines (`grep -nE '^[ ]+\|[ ]*S[0-9]{3,}' corpus/SOURCES.md`
  → rc 1), i.e. the frozen column-zero regex did not miss a row;
- no row-shaped line outside `## Registry` (maintained `E12` absent);
- used-by: **51 path references (26 unique) across all statuses, 0 missing**; all 28
  mined rows carry non-`—` used-by (`W03` absent); no backticked/annotated used-by
  cells that the `[ -e "$p" ]` check would silently skip.
- exact-URL duplicate sweep: only `https://pitest.org/quickstart/incremental_analysis/`
  (S041/S047/S048), the supersedes chain above.

## Rules 1–2 for rows S052–S057

**Trimmed claim:** the six rows are new, appended, gate-recorded, and footered.

**Rule 2 — append-only.** Parent `e69b488` has 49 registry rows; `c699c8c` has 55.
Line-level set comparison of every matched row (id → full row line):

```
added    ['S052','S053','S054','S055','S056','S057']
removed  []
changed common rows []
```

Rows sit at `corpus/SOURCES.md:61-66`, after S051 and before `## Paths` (`:68`).
`git diff --stat e69b488 c699c8c -- corpus/SOURCES.md` = `16 insertions(+), 1 deletion(-)`;
the single deletion is the Id-allocation footer line `Next unused id: S052.`, replaced by
`corpus/SOURCES.md:186-187` — no registry row text changed, so no `status`/`recheck`/
`used-by` old→new log is owed. The lesson states exactly that (`corpus/lessons/round-16.md:40-43`:
"no existing row's status, recheck or used-by changed. Id-allocation footer: next unused S052 → S058").
S038–S039 gap remains explained at `corpus/SOURCES.md:176-179` ("allocated, never written,
retired — never reused or renumbered … a census gap at S038–S039 is this note, not a lost row").

**Footer.** `corpus/SOURCES.md:186` lists `S052–S057: round-16 rows …`; `:187` says
`Next unused id: S058`, matching the six added ids and the lesson's logged old→new.

**Rule 1 — write-after-open + `## Gate` record.** `corpus/lessons/round-16.md:29-38`
tabulates all six rows with URL/command, `Accessed 2026-10-20`, and a quoted sentence
with location. Quote-only word counts (contract limit ≤25): S052 16, S053 15, S054 17,
S055 18, S056 21, S057 8. `opened` cells are all `2026-10-20`, equal to the commit date
and not future (`E08` absent). Non-author re-open of every quote:

| row | re-check result |
|---|---|
| S052 | quote is opening paragraph sentence 2 of the Stryker page; Support table marks Assignment Expression ❌ for StrykerJS, the other five families ✅; HTTP `last-modified: Mon, 19 Oct 2026 18:02:59 GMT` matches the row anchor's 2026-10-19 |
| S053 | `git show 364f1d5:scripts/round-gate.mjs` blob sha256 = `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` (matches row anchor); quote verbatim at `:19-20`; `:45-48` is the `--selftest` hermetic description; `:635` `if (opts.selftest) return selfTest();`; `:677-681` emits the verdict line; `selfTest()` has **60** `check(` cases (matches "60-case hermetic selftest"); full hash `364f1d5954158ef8844bca4a5fef57b05d2f2ca5` resolves and is an ancestor of kumitate `HEAD` |
| S054 | quote present in §The compass; `¶22` verified as the 22nd `<p>` element in the served HTML (exact); HTTP `last-modified` 2026-08-06 matches the row anchor |
| S055 | quote is module-introduction first bullet of the Python 3.15.0 doctest page |
| S056 | quote present at §CONDITIONALS_BOUNDARY (served line-wrapped); sha256 of the fetched page body = `a31331daf89f246f3e02c0da92578d4ad2163c53741c3700437e75b9a1602da2`, matching the row's `a31331da…` |
| S057 | quote at PDF p. 29, §5.3.1 ("Detecting equivalent mutants is a well-known undecidable problem"); `pdfinfo` CreationDate `Thu Dec 14 19:37:04 2017 -02`, matching "preprint dated 2017-12-14"; p. 29 confirmed by page numbering in extracted text |

Used-by citations are real, not merely existing paths: `corpus/knowledge/mutation-case-kumitate-round-gate.md:1`
cites S052, S053, S056, S057 (with the full kumitate commit and blob hash);
`corpus/lessons/round-16.md` cites all six rows (`:33-38`, plus `:40-42`).

## Residual risk / verification gaps

- Access dates (2026-10-20) are the authors' claim; I re-opened the sources on 2026-10-20
  and content matched, but I cannot prove the earlier fetch time. `[INFERENCE]`
- The S052 page exposes no commit pin (only the HTTP `last-modified`), as the row says;
  the sha256 anchor of S056 pins that page's bytes but the page states no version.
- The lesson's "ScienceDirect returned 403" is not re-claimed here; a DOI HEAD resolves
  302→200 to the Elsevier linking hub, and the published text was not read by me either.
- A control run of `validate --file` on a copy outside the lane tree produced `E11` for
  every used-by path because the script resolves used-by against the registry file's
  parent directory (`scripts/sources-census.sh` `resolve_targets`: `dir_abs=$(realpath -- "$(dirname -- "$file_abs")/..")`).
  That is a control artefact, not a lane finding; the lane-mode run (lane root as base)
  is the authoritative one and is clean.

## Verdict

**Holds.** The registry (55 rows, 0 malformed, 0 duplicate ids, 0 enum/tier violations,
0 missing used-by references of 51) passes both the maintained validator/census and the
frozen manual block (exit 0, only the pre-existing W04 supersedes-pair warning), and
S052–S057 are a pure append with an updated, logged Id-allocation footer and a complete
`## Gate` record whose every quote I re-grounded at its named location.
