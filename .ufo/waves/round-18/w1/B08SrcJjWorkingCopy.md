# B08SrcJjWorkingCopy — round 18 wave 1 report

Verdict: **REJECTED** (S072 draft). The source is open and quoted, but it does not support the purpose: it says nothing about colocated Git HEAD or bookmark divergence.

## Scope
Source: https://docs.jj-vcs.dev/latest/working-copy/ (Working copy - Jujutsu docs).
Purpose: C2 P08 — jj working-copy commit versus colocated Git HEAD, and HEAD versus bookmark divergence.
Owned write: `.ufo/waves/round-18/sources/S072-B08SrcJjWorkingCopy.md` (row draft, Gate, decision). This report is the Report-trailer output.

## Evidence
1. Duplicate check: `grep -c 'docs.jj-vcs.dev/latest/working-copy' corpus/SOURCES.md` → 0. No existing row carries this URL. The related row S061 (`/latest/git-compatibility/`) is a different URL, which is the source that already covers colocated HEAD.
2. Fetch: `curl -sSL --max-time 30 https://docs.jj-vcs.dev/latest/working-copy/` → exit 0, 47,694 B. The `read` tool returned the same text, so no mirror was needed.
3. Content sweep (article body, 1,048 words): `colocat` 0, `HEAD` 0, `bookmark` 0. The page covers snapshotting, conflicts, ignored files, workspaces and stale working copies. The only Git reference in the body is the ignore-file mechanism (`$GIT_DIR/info/exclude`).
4. Gate quote, §Introduction ¶1 (`#introduction`), 18 words, verbatim: "The working copy is where the current working-copy commit's files are written so you can interact with them." Checked with `q in txt` → True.

## Row
S072 (provisional), status `rejected`, tier A for its own scope. Teaches: `REJECTED: …; flip: …`. Full row text is in the owned draft.

## Flip condition
An official jj page that states what a colocated Git HEAD points at relative to the working-copy commit or a bookmark. The lane's existing S061 already carries the HEAD-versus-branch-tip claim.

## Installs and tools
None. Used only `curl`, `grep`, `sed` and `python3` (stdlib). No git or jj writes; no GIT_* variables set.

## Out of scope and limits
- The final id is for the L1. S065 is the registry's next unused id; S072 is the provisional id from the Target.
- The row does not change S061 or any knowledge entry. `used-by` is `—` because nothing cites a rejected row.
- The page's version is unstated (URL alias `latest`), so the anchor records the fetch date only.
