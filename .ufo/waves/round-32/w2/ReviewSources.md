# ReviewSources — wave 2 report (TameshiR32.ReviewSources)

Review of the SOURCES.md rows re-opened/added at `a4f718138bdad20de741faeca57891645e5a64d9`
(the revision's widely read input edits). All reads were cold and independent; no editor or LSP
server applies to markdown, so text-level evidence is used throughout.

Scope: S097 and S099 (new rows), S094 (re-opened, used-by-only change),
11-cell check, used-by existence at the revision, trailing round-32 note, rows count 94 -> 96.

## Verdicts

- **S097 — PASS.** Live fetch of the row's URL returned exactly the pinned bytes/digest; both
  named quote anchors match the fetched bytes; row has 11 cells; both used-by paths exist at the
  revision.
- **S099 — PASS.** Live fetch of https://pitest.org/ returned exactly the pinned bytes/digest;
  the HTML lines 110–114 quote matches; row has 11 cells; both used-by paths exist at the revision.
- **S094 — PASS (used-by-only change).** Cell-level diff shows exactly one cell changed, the
  used-by cell; 11 cells before and after; both used-by paths exist at the revision; status and
  recheck cells unchanged.
- **Rows count 94 -> 96 — PASS.** Registry row lines: parent 94, revision 96; diff shows the two
  new rows are pure insertions (no row edited into existence).
- **Round-32 note at end — PASS.** Trailing block present, consistent with observed data
  (S098 unused, S094 used-by change, status/recheck unchanged, "Rows 94 → 96", next unused id S100).

No findings at any severity. No residual risk affecting the reviewed content; one contextual note
in "Verification gaps".

## Evidence

### Setup (all under /fast/scratch/hyaku/tameshi-r32-seats/ReviewSources/)
- `git -C …/tameshi-shokunin show a4f718138bdad20de741faeca57891645e5a64d9:corpus/SOURCES.md | tee SOURCES-new.md | sha256sum` -> `56838b80b69f38743c3ad2b252463afb2bb3ff6d1c6097f885c210629772c3d8`
- `git -C … show a4f718138bdad20de741faeca57891645e5a64d9^:corpus/SOURCES.md | tee SOURCES-prev.md | sha256sum` -> `489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741`
- `git -C … ls-tree -r --name-only a4f718138bdad20de741faeca57891645e5a64d9` -> 7945 paths, saved as tree-a4f7.txt

### Rows count
- `grep -c '^| S0' SOURCES-prev.md SOURCES-new.md` -> `SOURCES-prev.md:94` `SOURCES-new.md:96`
- `diff SOURCES-prev.md SOURCES-new.md` hunks: `103c103` (S094 row updated), `105a106,107`
  (S097 + S099 inserted), `377a380,390` (round-32 note appended). No other changes.

### S094
- Cell diff (`python3` split on `|`): 11 cells before and after; the only differing cell is
  index 11 (used-by), OLD ` corpus/knowledge/regression-tally-completeness.md ` -> NEW
  ` corpus/knowledge/regression-tally-completeness.md, corpus/knowledge/runner-tally-audit.md `.
  Status (`mined`) and recheck (`730d`) cells identical.
- Used-by existence at a4f7181: `corpus/knowledge/regression-tally-completeness.md` and
  `corpus/knowledge/runner-tally-audit.md` both present in tree-a4f7.txt.

### S097
- Row: `| S097 | GNU Bash Reference Manual, Bash 5.3 source (doc/bashref.texi) — https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303 … | docs | A | … | §Exit Status (@node Exit Status, lines 3890–3916) and §Conditional Constructs case (lines 1044–1084) @ Bash 5.3 commit b8c60bc9…, fetched 2026-10-23 UTC (415804 bytes; SHA-256 f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5) | … | mined | 2026-10-23 | on-release | tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md |` — 11 cells.
- Live fetch: `curl -fsSL '<URL as in row>'` -> `415804` bytes, `sha256sum` ->
  `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5` — byte count and digest
  equal the row's claim.
- Exit Status quote at lines 3896–3897 (fetched bytes):
  `Exit statuses fall between 0 and 255, though, as explained below,` / `the shell may use values above 125 specially.`
  The row's teaches "exit statuses fall between 0 and 255 (126 not executable, 127 not found,
  128+N fatal signal)" is corroborated by the adjacent lines in the same section (128+N / 127 /
  126 sentences appear immediately after, within the anchor range 3890–3916).
- case sentence at lines 1081–1082 (fetched bytes): `The first pattern that matches determines the` / `command-list that is executed.` — matches "`case` runs the command-list of the first matching pattern".
- Used-by existence at a4f7181: `tools/tally-audit.py` and `corpus/knowledge/runner-tally-audit.md` both present.

### S099
- Row: `| S099 | PIT Mutation Testing — https://pitest.org/ | docs | A | … | §What is mutation testing?, HTML lines 110–114 @ page fetched 2026-10-23 UTC (12,023 bytes; SHA-256 b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc) | … | mined | 2026-10-23 | 180d | tools/tally-audit.py, corpus/knowledge/runner-tally-audit.md |` — 11 cells.
- Live fetch: `curl -fsSL 'https://pitest.org/'` -> `12023` bytes, `sha256sum` ->
  `b0c7e0505c51c95b596060ef27babbce08e72d5aaf4557eb002c2637d2bf10cc` — byte count and digest
  equal the row's claim.
- HTML lines 110–114 (fetched bytes): "Faults (or mutations) are automatically seeded into your
  code, then your tests are run. If your tests fail then the mutation is killed, if your tests
  pass then the mutation lived." and "The quality of your tests can be gauged from the percentage
  of mutations killed." — matches the teaches cell.
- Used-by existence at a4f7181: `tools/tally-audit.py` and `corpus/knowledge/runner-tally-audit.md` both present.

### Whole-file audit (bonus, cheap)
- All 96 registry rows have exactly 11 cells (no exception).
- No `| S098 |` row exists (0 matches), consistent with the note.
- Trailing note block at file end (lines 381–390): rounds 32 text, ending `- Next unused id: S100.`
  Matches observed data.

## Verification gaps
- The git-side commit id `b8c60bc9…` is asserted by the row; what the live fetch proves is that
  the URL *with that id parameter* serves exactly the pinned bytes/digest — i.e. the content is
  tied to the id as fetched. This is the same evidence the row claims. No independent
  verification of the commit's existence in bash.git was attempted.
- The rendered gnu.org page-timeout event (2026-10-23) is historical and not re-testable here;
  the note records it and the row documents the substitution.
