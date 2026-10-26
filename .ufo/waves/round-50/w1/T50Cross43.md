# T50Cross43 — independent R43 coding

Base under review: `e3729de862f73ae080d98fcf522a7081ce16e40a`. I read the full routed text at `corpus/lessons/round-43-verifier-spotcheck.md:63-65` and the frozen R43 definitions in `.ufo/evidence/round-50/c1/defects.json:248-287`. I did not inspect any T50Disp file. Findings below describe the tree's disposition; they do not adjudicate C1.

## R43.1 — fixed

The ask was to reconcile the false `m7` unknown `S256` citation, re-run measurement at the intended final revision, and preserve an append-only correction without rewriting the filed report/lesson. `corpus/lessons/round-44.md:81-83` records the historical alarm and identifies its exact source as the `safe_floor=S256` assignment. The actual repair is the round-44 counter's assignment-value mask and dedicated regression case at `.ufo/evidence/round-44/calibration/measure.py:412-423`; the round-44 lesson's correction/mistake discussion is append-only and leaves the round-43 lesson intact. The strongest counterargument is that the lesson may just claim a fix, while the historical SCORECARD token remains. Checked the implementation: the value is masked as an assignment, with a case asserting it does not produce a citation; the counter separately preserves genuine unknown-id checks at its subsequent test cases. The new parser behavior, not a rewrite of history, resolves the defect.

Commands: `read corpus/lessons/round-44.md:81-83`; `read .ufo/evidence/round-44/calibration/measure.py:412-423`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --stat --oneline 83beaf980f246412368f89fbe7758375c8ca21e0`.

## R43.2 — fixed

The ask allowed restoring or explicitly dispositioning the modified tracked reviewer note. `corpus/lessons/round-44.md:85` explicitly dispositions it as retained, committed inherited evidence and states the updated note contains the A13/A14 corrections. The note exists in the base tree and contains the reviewer analysis (`.ufo/waves/round-43/w1/RevC2Classes.md:1-6`). Strongest counterargument: file presence alone does not establish that a formerly dirty change was intentionally resolved. The specific round-44 disposition resolves that concern; retaining the note is the chosen explicit disposition, not an unexplained dirty edit. The R44 landing changes include the tracked note as inherited evidence.

Commands: `read corpus/lessons/round-44.md:85-90`; `read .ufo/waves/round-43/w1/RevC2Classes.md:1-6`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show --stat --oneline 6f99eb5`.

## R43.3 — fixed

The ask was to refresh S089's stale source anchor append-only, with old→new recorded in a round lesson. `corpus/lessons/round-44.md:45-54` documents the re-open and explicitly says S160 supersedes S089's anchor only; lines 35-38 record old and new digest prefixes and same-offset quote persistence. `corpus/SOURCES.md:98` preserves the historical S089 row rather than editing it in place, consistent with the append-only registry rule; the new S160 row and snapshot are committed in round 44. Strongest counterargument: the old digest remains in S089, apparently contrary to “update its anchor.” Checked the item's “future append-only registry change” wording against the actual append-only correction: supersession is the valid update mechanism here; in-place mutation would break the registry contract. The new S160 row's supersession and committed reopened snapshot implement the requested correction.

Commands: `read corpus/lessons/round-44.md:35-54`; `read corpus/SOURCES.md:98-99`; `read .ufo/evidence/round-44/sources/stryker-equivalent-mutants.html:15-17`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -- corpus/SOURCES.md`.

## Summary
- R43.1 fixed: assignment-value mask and test resolve false S256 citation; historical record remains append-only.
- R43.2 fixed: round-44 explicitly retains/dispositions the tracked reviewer note.
- R43.3 fixed: S160 append-only supersession and reopened snapshot correct S089 anchor provenance.
- No tools installed or updated.