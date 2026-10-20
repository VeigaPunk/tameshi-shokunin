# Reopen S070 — Pro Git, 2nd ed., §10.8 Environment Variables (repository locations)

Seat: TameshiR18.ReopenS070 (scout, wave 2). Read rev
`01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (`round-18: C2 ruler v2 …`).
Reads were read-only `git show` / `git grep` / `git cat-file -e` against the lane repo and
`curl` against git-scm.com; no working-tree, index, jj or sibling-repo write was made.
Lane files are opened at the read rev; the staged lesson is opened from the same rev.

Verdict: **holds** — the gate quote is a verbatim 18-word fragment inside the stated
`Repository Locations` anchor, every clause of the `teaches` cell is on the page without
overstating it, `book`/tier B fit the registry's own precedent and the row's own draft,
and the single `used-by` path exists at the read rev and cites S070 twice.

## 1. Rev and row shape

```
$ git -C <lane> rev-parse 01d586ddbc5fcd78659557c4e93a6ee8517b87d1
01d586ddbc5fcd78659557c4e93a6ee8517b87d1                                    exit 0
$ git show REV:corpus/SOURCES.md | sed -n '79p'
| S070 | Pro Git, 2nd ed., §10.8 Environment Variables — https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables | book | B | GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE as repository-location overrides; secondary to the normative S063 | §10.8 Environment Variables, subsection Repository Locations @ 2nd-edition page, fetched 2026-10-20 (page version and last-modified not shown) | GIT_DIR names the .git folder and, when unset, git walks up parent directories; with GIT_DIR set and no work-tree override the cwd is the top level of the working tree; GIT_INDEX_FILE relocates the index for non-bare repositories only | mined | 2026-10-20 | 180d | corpus/knowledge/guard-kill-closure.md |
$ git show REV:corpus/SOURCES.md | awk -F'|' 'NR==79{print "NF="NF}'
NF=13                                                                       exit 0
$ git show REV:corpus/SOURCES.md | grep -c '^| S070 '
1                                                                           exit 0
```

`NF=13` is the 11-cell header (`corpus/SOURCES.md:9`: `id | source | kind | tier | scope |
anchor | teaches | status | opened | recheck | used-by`) plus two edge separators, so the
row has no missing or extra cell. The row appears once; `S070` elsewhere in the file is
only the round summary at `corpus/SOURCES.md:207` (`S070 Pro Git, tier B`), which agrees.
The row is new this round: `git show 183f87b:corpus/SOURCES.md | grep -c S070` → `0`
(exit 0), matching the staged lesson's "base line 73" append claim.
The landed file is byte-identical to the staged copy:
`git show REV:corpus/SOURCES.md | sha256sum` and
`git show REV:.ufo/waves/round-18/staged/corpus/SOURCES.md | sha256sum` both give
`1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` (exit 0), so the
installed row is exactly the gated row.

## 2. Page opened live

```
$ curl -sS -o /tmp/s070-page.html -w '%{http_code} %{url_effective}\n' https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables
200 https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables   exit 0
139272 bytes; sha256 c9e4e23f6a13321e1247bbfb427e4133ae0e66e24e55f8be839e465b2e7fcb32
```

The page is the 2nd-edition page ("2nd Edition" in the header), has the `### Repository
Locations` heading, and carries no build version or last-modified marker: zero hits for
`last modified`, `last-modified`, `Last updated`, `updated`, and no `YYYY-MM-DD` string.
That matches the anchor cell's parenthetical. (The edition itself *is* shown, and is
already named in the source cell as "2nd ed.".)

## 3. Quote verbatim at the stated anchor, ≤25 words

Gate quote (`staged/lesson-round-18-gate.md:22`):

> GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree

Verification on the tag-stripped, whitespace-normalised text of the fetched page, with the
`Repository Locations` section sliced from its heading to `GIT_CEILING_DIRECTORIES`:

```
quote_in_RepositoryLocations_section: True
section_len_chars: 290
words: 18                                                                   exit 0
$ printf '%s' "<quote>" | wc -w
18                                                                          exit 0
```

The page's sentence continues `until it gets to ~ or /, looking for a .git directory at
every step.` — the quoted part is a contiguous verbatim prefix, not a paraphrase; nothing
was added or re-spaced. The apostrophe is U+2019 (`isn’t`) exactly as the page and the
gate note ("curly apostrophe as printed") say; the ASCII apostrophe is absent, so the
gate's typography claim is exact. Inline `<code>`/`<strong>` markup is removed (the gate's
stated method), which is how `GIT_DIR` and `.git` appear in the rendered text.
Section context printed by the checker: `… interfaces with the current repository. GIT_DIR
is the location of the .git folder. If this isn’t specified, Git walks up the directory
tree until it gets to ~ or /, looking for a .git directory at every step.
GIT_CEILING_DIRECTORIES …`.

## 4. Teaches cell does not overstate the page

Each clause was tested against the page text; all four probes are present verbatim:

| Row clause | Page sentence (same fetch) | Probe |
|---|---|---|
| GIT_DIR / .git folder | `GIT_DIR is the location of the .git folder.` | True |
| unset → upward walk | `If this isn’t specified, Git walks up the directory tree until it gets to ~ or /` | True |
| GIT_DIR set, no work-tree override → cwd is top level | `If --git-dir or GIT_DIR is specified but none of --work-tree, GIT_WORK_TREE or core.worktree is specified, the current working directory is regarded as the top level of your working tree` | True |
| GIT_INDEX_FILE, non-bare only | `GIT_INDEX_FILE is the path to the index file (non-bare repositories only)` | True |

No clause claims more than the page: "relocates the index" is the page's "is the path to
the index file"; "with GIT_DIR set and no work-tree override" is the page's condition minus
the `--git-dir`/`--work-tree` spellings, which is a narrowing, not an extension. The
`scope` cell's three variables are exactly the three the page lists under `Repository
Locations` and that the teaches cell touches.

## 5. Tier / kind fit

- `kind: book` — the source is Pro Git, 2nd ed., a published book read on its own
  presentation page; this is a book, not `docs` (the git(1) manual) or a `spec`.
- The registry's only other `book` row, S024 (`corpus/SOURCES.md:35`, The Fuzzing Book), is
  also tier B. Both book rows are B; there is no book row at A or C.
- `tier: B` is the conservative fit: the row itself says "secondary to the normative S063"
  (line 79), S063 is `docs` tier A (`corpus/SOURCES.md:72`), and the used-by file repeats
  "S070 is Pro Git, tier B; the normative source is S063"
  (`corpus/knowledge/guard-kill-closure.md:95`). The draft records the same rationale:
  "Tier B, not A: a textbook is strong secondary under the SOURCES tier rule"
  (`.ufo/waves/round-18/sources/S071-B07SrcGitEnv.md:12`).
- Limitation: the contract document that would define the tiers is not in the tree at this
  rev — `git cat-file -e REV:.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` → `fatal: path …
  does not exist`, exit 128 (the known round-12 R6 gap; `corpus/SOURCES.md:4` names the
  file by bare name). Tier fit is therefore checked against registry precedent and the
  draft's recorded rule, not against a written tier table. This does not weaken the B
  verdict: B understates rather than overstates the source's authority, and the row is not
  used as sole support anywhere.

## 6. Used-by path exists at the read rev and cites S070

```
$ git cat-file -e REV:corpus/knowledge/guard-kill-closure.md ; echo $?
                                                                              exit 0
$ git show REV:corpus/knowledge/guard-kill-closure.md | grep -n S070
1:source: … S070 — Pro Git §10.8 Repository Locations, https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables (tier B); …
95:… Repository location variables are defined in [src: S070, quote "GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree"] and in the git(1) ENVIRONMENT VARIABLES list [src: S063]. S070 is Pro Git, tier B; the normative source is S063.
```

`:95` is a substantive use, not a bare mention: it carries the row's quote, the tier, and
the deference to S063. The entry's `source:` header also names S070 at `:1`. The index
`corpus/README.md:266` lists S070 among the sources of that same entry, which agrees with
the `used-by` cell. A corpus-wide sweep
(`git grep -n S070 REV -- corpus/`) returns only `SOURCES.md:79`, `SOURCES.md:207`,
`README.md:266`, and `guard-kill-closure.md:1,:95` — no second consumer is missing from the
cell. `status: mined` is therefore supported: the cited path exists and cites the row.

## 7. Staged gate entry

`staged/lesson-round-18-gate.md:22` carries the same URL, the same access date
(2026-10-20), and the same quote string as the registry row; the checker's
`gate_quote_verbatim` and `gate_url_match` probes both pass. The mapping at `:54`
(`- S070 ← draft S071 (Pro Git §10.8, tier B), mined.`) agrees with the draft
(`.ufo/waves/round-18/sources/S071-B07SrcGitEnv.md:9`, provisional id S071, tier B,
`mined`). The lesson's own structural claims also check out at this rev: `Base lines are
from corpus/SOURCES.md at 183f87b` (`:40`) and `S065–S074 … base line 73` (`:45`) — lines
73–83 at the read rev are exactly S064, S065 … S074, with S070 at 79. The gate's quote
rules (`:10-11`: re-fetched 2026-10-20, matched after whitespace normalisation and tag
stripping, ≤25 words, source punctuation kept) are all satisfied by this row on the
current fetch.

## 8. Minor, non-blocking observations

1. **Walk bound omitted.** The page says the upward walk stops at `~` or `/`; the teaches
   cell says only "walks up parent directories". That is under-specification, not an
   overstatement (it does not say "to the filesystem root"), but a downstream entry should
   not use this row to claim an unbounded walk. The row's actual consumer (`P11`/guard-kill
   closure) uses the `GIT_DIR` override, not the walk bound.
2. **"names" for "is the location of".** The first clause compresses the page's wording;
   it reads correctly as "designates the `.git` folder" in the context of the scope cell,
   and the gate quote carries the exact sentence. Wording nit only.
3. **The gate quote ends mid-sentence without an ellipsis.** The gate states only
   "verbatim, ≤25 words"; S072's gate entry (`staged/lesson-round-18-gate.md:24`) also
   begins mid-sentence, so the truncation follows the table's own convention and adds no
   words.
4. **Tier rule document absent** (see §5) — a pre-existing lane gap, not a defect of this
   row; the fit was checked by precedent.

Commands and exits for the consolidated probe (all checks pass, exit 0):
`PASS row_cells=11`, `PASS quote_verbatim_in_anchor`, `PASS words=18`,
`PASS curly_apostrophe`, `PASS GIT_DIR location`, `PASS unset walk`,
`PASS cwd top-level`, `PASS index non-bare`, `PASS gate_row_line=22`,
`PASS gate_quote_verbatim`, `PASS gate_url_match`, `PASS used_by_cites_quote`,
`PASS used_by_names_tier`, `PASS status_and_usedby`.

Verdict: **holds** — row S070 and its gate entry survive re-opening: 18-word verbatim quote inside `Repository Locations`, teaches clauses are all on the page without overstating it, `book`/tier B fits the registry's only other book row and the row's own draft, and `corpus/knowledge/guard-kill-closure.md` exists at `01d586d` and cites S070 (lines 1 and 95).
