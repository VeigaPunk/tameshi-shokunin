# B05SrcPrctl — findings (round 18, wave 1)

Verdict: **partial** — the opened URL does not support the purpose; the rejected row is drafted in `.ufo/waves/round-18/sources/S069-B05SrcPrctl.md`; the supporting page is identified as a lead for L1.

## Checks run (2026-10-20)

| # | Command / action | Exit | Key output |
|---|---|---|---|
| 1 | read `/home/vgpnk/Projects/shokunin/CORPUS.md` (SOURCES.md contract section) | ok | 13-cell row shape; `status` ∈ {queued, mined, rejected}; rule 1: a row is a claim, Gate records URL, access date, ≤25-word quote |
| 2 | `grep -nE 'prctl|subreaper|SUBREAPER' corpus/SOURCES.md` | 1 | no matches → not a duplicate |
| 3 | `grep -noE '^\| S0[0-9]{2}' corpus/SOURCES.md \| tail -3` and `grep -n 'Next unused' …` | 0 | last row S064; line 195 `- Next unused id: S065.` (Target's provisional S069 differs — flagged) |
| 4 | read `https://man7.org/linux/man-pages/man2/prctl.2.html` | ok | operation list names PR_SET_CHILD_SUBREAPER / PR_GET_CHILD_SUBREAPER; no reparenting text; footer `Linux man-pages 6.19 2026-02-08 prctl(2)` |
| 5 | read `https://man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html` (lead; not the Target URL) | ok | §DESCRIPTION: "When a process becomes orphaned … reparented to the nearest still living ancestor subreaper." |
| 6 | `curl -fsSL` both pages into `/tmp/tameshi-r18w1-B05SrcPrctl-TCbGVx`; sha256 prefix prctl.2 = ef698f6c5aab0224 | 0 | 26266 bytes |
| 7 | `grep -inE 'reparent\|orphan\|subreaper' prctl2.html` | 0 | only operation-name lines (91, 92), SEE ALSO links (190–191), link rows (262, 287); no reparent/orphan wording |
| 8 | quote check on the 2const page (whitespace-normalised `grep -cF`) | 0 | `1` match |
| 9 | `echo "$Q" \| wc -w` | 0 | `23` (≤25) |

## Installs / tools
None. Only `curl`, `grep`, `sed`, `tr`, `wc`, `sha256sum` (host).

## Decisions
- **S069 (Target URL prctl.2): REJECTED.** Teaches-field reject: the page names the operation but states no semantics. Flip: the rule is cited from PR_SET_CHILD_SUBREAPER(2const) under its own row, or this URL's text gains the rule.
- **Lead for L1 (not drafted as a row by this seat):** PR_SET_CHILD_SUBREAPER(2const), 23-word verbatim quote above; likely S070 once the L1 reconciles ids (S065 is the file's stated next unused; the provisional S069 is held by this rejection).
- Duplicate check: none found for either URL.

## Scope notes
- Only the Target's owned file and this report were written. No edits to SOURCES.md, registry, or other lane files. No subagent dispatch. No git writes. No GIT_* variables set.
- The `Report:` path is written in addition to the owned S069 file, because the Target asks for findings there.

## Open items for L1
1. Reconcile provisional id S069 with the file's `Next unused id: S065`.
2. Decide whether to admit PR_SET_CHILD_SUBREAPER(2const) as a separate `mined`/`queued` row (quote and anchor in the S069 Gate's Lead section).
