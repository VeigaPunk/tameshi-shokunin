# Round 18 — SOURCES gate (staged)

Seat: TameshiR18.B13KnowExitErratum (L1 follow-up). Base: `corpus/SOURCES.md` at
`183f87b899e6cae46be98d251cbc87fb5118f6ca` (byte-identical to the working tree at
dispatch). Staged output: `.ufo/waves/round-18/staged/corpus/SOURCES.md`. The L1
installs it; no live lane file was edited.

## Gate quotes

Each quote was re-fetched on 2026-10-20 and matched after whitespace
normalisation and tag stripping. Each is at most 25 words. Quotes keep the source's
own punctuation and typography.

| Row | URL | Accessed | Quote (location) |
|---|---|---|---|
| S008 | https://arxiv.org/abs/2102.11378 | 2026-10-20 | "Mutants are selected based on the historical performance of mutation operators, further eliminating irrelevant mutants and improving mutant quality." (Abstract, item (3); arXiv:2102.11378v2) |
| S065 | https://docs.python.org/3/library/json.html | 2026-10-20 | "by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values" (§Standard Compliance and Interoperability › Infinite and NaN Number Values; inline code markup removed) |
| S066 | https://www.rfc-editor.org/rfc/rfc8259 | 2026-10-20 | "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted." (§6 Numbers) |
| S067 | https://man7.org/linux/man-pages/man2/prctl.2.html | 2026-10-20 | "PR_SET_CHILD_SUBREAPER" (§DESCRIPTION, operation list; the page has three occurrences in total; rejected row, quoted for its absence of a rule) |
| S068 | https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html | 2026-10-20 | "When a process becomes orphaned (i.e., its immediate parent terminates), then that process will be reparented to the nearest still living ancestor subreaper." (§DESCRIPTION, first paragraph after SYNOPSIS) |
| S069 | https://man7.org/linux/man-pages/man2/setsid.2.html | 2026-10-20 | "The calling process will be the only process in the new process group and in the new session." (§DESCRIPTION ¶2) |
| S070 | https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables | 2026-10-20 | "GIT_DIR is the location of the .git folder. If this isn’t specified, Git walks up the directory tree" (§10.8 Environment Variables, Repository Locations; curly apostrophe as printed) |
| S071 | https://docs.jj-vcs.dev/latest/working-copy/ | 2026-10-20 | "The working copy is where the current working-copy commit's files are written so you can interact with them." (§Introduction ¶1; rejected row, quoted for scope) |
| S072 | https://man7.org/linux/man-pages/man2/open.2.html | 2026-10-20 | "the access mode allows writing (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0." (§DESCRIPTION, O_TRUNC entry) |
| S073 | https://docs.python.org/3/using/cmdline.html | 2026-10-20 | "If this is set, Python will write .pyc files in a mirror directory tree at this path, instead of in __pycache__ directories" (§1.2 Environment variables, PYTHONPYCACHEPREFIX) |
| S074 | https://git-scm.com/docs/git-symbolic-ref | 2026-10-20 | "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently." (§OPTIONS, -q / --quiet) |

Source-line checks for the Gate table:

- S072: the quote is the tag-stripped text of the O_TRUNC sentence; the page's
  inline markup is removed without replacement, so no words are added or changed.
- S073: the draft recorded a served-HTML sha256 `a4863a38…b734`. A re-fetch on
  2026-10-20 returned `7642c278…dd5`, and the quotes still matched. The registry
  row therefore cites only the access date; the draft hash is not claimed.
- S074: the page shows `<name>` as `&lt;name&gt;` in HTML; the quote shows the
  rendered text.

## Registry changes (old → new)

Base lines are from `corpus/SOURCES.md` at `183f87b`.

1. **S008 (in-place, the only change to an existing row):** status `queued` → `mined`;
   used-by `—` → `corpus/knowledge/mutation-case-kumitate-sources-check.md`. The
   other cells are unchanged. Line 19.
2. **Rows appended under `## Registry` (after S064, base line 73):** S065–S074
   (10 rows, lines 74–83). Mapping from the round-18 drafts:
   - S065 ← draft S067 (Python `json`), mined.
   - S066 ← draft S068 (RFC 8259), mined.
   - S067 ← draft S069 (prctl(2)), rejected. The draft's "see Lead" is now
     "see S068".
   - S068 ← new row for PR_SET_CHILD_SUBREAPER(2const). Its quote comes from draft
     S069's Lead, re-opened and verified here. Mined.
   - S069 ← draft S070 (setsid(2)), mined.
   - S070 ← draft S071 (Pro Git §10.8, tier B), mined.
   - S071 ← draft S072 (jj working copy), rejected.
   - S072 ← draft S073 (open(2)), mined.
   - S073 ← draft S074 (CPython command line and environment), mined.
   - S074 ← draft S075 (git-symbolic-ref), mined.
   - Every mined new row names `corpus/knowledge/guard-kill-closure.md` as its
     used-by path, as directed. Rejected rows use `—`.
3. **Draft wording changed when moved into the registry (not a verdict change):**
   - S065 teaches: the draft's "although RFC 7159 does not permit them" is replaced
     by the page's own wording, "as if they were valid JSON number literals". The
     page cites RFC 7159 for the format but does not state that prohibition.
   - S066 teaches: "a registry timeout_s … must refuse them" is marked
     `[INFERENCE: refusing it is a design choice]`, because §6 prescribes no parser
     behaviour.
   - S069 teaches: "a group-directed signal to the old group reaching it is
     [INFERENCE …]" was ambiguous. It now reads "does not reach it".
   - S073: the draft's served-HTML hash is dropped (see Gate table).
4. **Drafts not installed:** draft `S065` (Stryker states) is a DUPLICATE of S001.
   Draft `S066` (Google mutation) is a DUPLICATE of S008; its Q1 is the S008 gate
   quote above. Draft `S076` (subprocess) is a DUPLICATE of S049. The renumbering
   above does not use these numbers.
5. **Notes appended under the Registry (after the table, before `## Paths`):** one
   dated correction (2026-10-20) for S060 and S061. S060's anchor is corrected to
   the explicit syscall list (`trace-inputs.py:74-80`, `:630-631`), §Filtering
   `-e trace=syscall_set`, with `-f` in §Tracing. S061's detached-HEAD statement is
   ¶3, not ¶2. Both rows are unedited. Audit: `.ufo/waves/round-18/w1/S16SourcesRowsAudit.md`.
6. **Footer (`## Id allocation`), not a pure append:**
   - Appended `- S065–S074: round-18 rows (…)` after the round-17 line.
   - Replaced `- Next unused id: S065.` with `- Next unused id: S075.`. The old
     line is a pointer, not a historical record, so it is replaced. The closure
     noted footer edits are not pure appends; this is the one.
7. **Unchanged:** lines 1–18, 20–73, and 75–194 (Paths, Search log, Leads, and the
   Id allocation entries above the footer).

Totals: rows 62 → 72. Status `mined` 35 → 44, `queued` 24 → 23, `rejected` 3 → 5.

## Checks

- Row shape (awk, `-F'|'`, NF = 13 for each row starting `| S`): `rows=72 bad=0`
  on the staged file. The base file gave `rows=62`.
- Ids: no duplicates; the S065–S074 sequence is contiguous.
- Diff against base: hunks `19c19`, `73a74,85`, `195c207,208` only. `cmp` confirms
  base lines 1–18 and 20–73 are identical.
- `sources-census.sh validate --root <mirror> --file <staged>` (mirror = `git archive`
  of 183f87b with the staged file copied in):
  - Staged, as-is: exit 1. The 8 errors are E11 "used-by path missing" for
    `corpus/knowledge/guard-kill-closure.md`, which does not exist in the lane yet.
    Pre-existing W04 warnings (S047/S048) are unchanged.
  - Staged, with a placeholder `guard-kill-closure.md` in the mirror only: exit 0.
  - Base, same mirror layout: exit 0.
  - The guard-kill-closure file must land (or the used-by cells change) before the
    registry can validate clean in the lane.
