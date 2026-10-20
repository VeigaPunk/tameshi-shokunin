# S070 — draft row and Gate (B06SrcSetsid, round 18 wave 1)

Decision: **mined** (not a duplicate; source supports the C2 P10 purpose). Draft for the L1 to install in `corpus/SOURCES.md`; not written there by this seat.

## Duplicate sweep

- Command: `_grep` pattern `setsid|man2/setsid` over `tameshi-shokunin/corpus/SOURCES.md` → **No matches found** (2026-10-20).
- Adjacent, not duplicate: S060 is `strace(1)` (man1), S062/S063 are git docs.

## Registry row (draft, 11 cells, NF=13 under the census awk)

```
| S070 | Linux man-pages: setsid(2) — https://man7.org/linux/man-pages/man2/setsid.2.html | docs | A | Linux setsid(2) session and process-group semantics for a caller that leaves its group | §DESCRIPTION ¶2 and §ERRORS EPERM @ man-pages 6.19 (footer date 2026-06-05), fetched 2026-10-20 | the caller becomes the only process in a new process group and a new session, distinct from its old group; a group-directed signal to the old group reaching it is [INFERENCE: follows from the distinct group ID; killpg is not named on this page]; setsid fails with EPERM for a process group leader, so the escaping process must fork and let the child call setsid | mined | 2026-10-20 | 180d | .ufo/evidence/round-18/defect-probes.py |
```

Field notes:
- `source`: man7.org mirror of the man-pages project (Kerrisk); canonical project home is kernel.org man-pages, cited in the page COLOPHON.
- `tier A`: the project's own official reference for the Linux `setsid(2)` interface, scoped to Linux semantics. Not `community`.
- `teaches` keeps the killpg consequence explicitly marked `[INFERENCE]`; the probe P10 must measure it, the page does not establish it.
- `used-by` is provisional: `.ufo/evidence/round-18/defect-probes.py` does not exist yet (glob of `.ufo/evidence/round-18/*` returned only `census-start.txt`). The SOURCES census check `mined rows whose used-by paths do not exist` will print `missing: .ufo/evidence/round-18/defect-probes.py` until that file exists and cites `S070`. If the L1 does not land the citing file in this round, the row must be `queued` with used-by `—` instead; `mined` is not claimed by this draft alone.
- Id: `S070` is the id the Target assigns. `corpus/SOURCES.md` line 195 still reads `Next unused id: S065`; the L1 must reconcile the id allocation (S065–S069 are not visible in this file) before installing.

## Gate (round-18 lesson `## Gate` entry for S070)

- **URL:** https://man7.org/linux/man-pages/man2/setsid.2.html
- **Access date:** 2026-10-20 (opened with the `read` tool; a `curl -sSL` body of the same URL taken the same day has sha256 `52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30`, 2026-10-20 retrieval).
- **Anchor:** `§DESCRIPTION`, paragraph 2 (the paragraph beginning "The calling process will be"); page revision: man-pages 6.19, footer date 2026-06-05, page HTML created 2026-09-09.
- **Quote (verbatim, 18 words):** "The calling process will be the only process in the new process group and in the new session."
  - Word count: `echo "<quote>" | wc -w` → `18`.
  - Source line break after "process" is normalised to a single space; no other change (checked by `tr -s ' \n' ' '` over the stripped HTML text, grep match present).
- **Second location for the `teaches` EPERM clause (not a second Gate quote):** `§ERRORS`, EPERM: "setsid() fails if the calling process is already a process group leader." (12 words, verbatim, same check.)
- **Teaches grounding:** the quote supports the new-group/new-session half; the EPERM clause supports the fork-first half. The killpg half is `[INFERENCE]` and is the thing probe P10 must measure.

## Verdict

- Duplicate: no (`No matches found`).
- Source reachable: yes (HTTP fetch succeeded; `read` returned the page).
- Purpose supported: yes for the new-session/new-group fact and the fork-first constraint; no for killpg (stated as inference).
- Row status: `mined` per Target, conditional on the citing file existing (see used-by note).
