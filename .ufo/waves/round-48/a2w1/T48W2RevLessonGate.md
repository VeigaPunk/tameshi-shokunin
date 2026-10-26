# T48W2RevLessonGate — round-48 lesson at CONTENT vs CORPUS SOURCES rules 1-2

Seat: T48W2RevLessonGate (a2w1, reviewer, leaf — no dispatch). Reviewed `corpus/lessons/round-48.md` and `corpus/SOURCES.md` at CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17` against `/home/vgpnk/Projects/shokunin/CORPUS.md:110-129` (SOURCES rules 1-2). Base for the diff: `473336d9d789f6081195e7376d17836a24666bc3`. Read-only seat; every command below was run and its output observed; no counter was run, no verdict issued.

## Checked and passing

1. **Rule 1 — new rows S265-S268 (SOURCES.md:140-143 at CONTENT).** All four rows carry URL (source cell), opened `2026-10-26`, and the Gate records a located quote per row. Token counts (whitespace-split, amendment 2): S265=15, S266=21, S267=25, S268=6 — all ≤25. All four `## Gate` `C2-QUOTE` lines match `^- C2-QUOTE (S\d{3,}) (S\d{3,}): ` and carry the contract's required phrases (`84%`; `should therefore be prioritised`; `--unshare-all`+`--unshare-cgroup-try`; `--update_goldens`).
2. **Quote location verified against committed snapshots (non-author re-open, all four).** With the amendment-2 extraction (UTF-8, script/style dropped, tags stripped, unescaped, whitespace collapsed), each quote is a substring and found exactly once: S026.html (offset 2137), S048.html (1014), S093.xml (2642), S108.html (2514). Raw-line claims verified: S026.html:1097 and :1132 both carry the sentence (lesson discloses both); S048.html:86 carries `prioritised`; S108.html:3609/3611 carry `update_goldens`; S093.xml:154-159 carry the unshare entries.
3. **Snapshot/receipt binding.** `sha256(S026.html)=a4c5c46b4af9…`, `S048.html=e9cbc3e1ab7c…`, `S093.xml=2cb77df2f4be…`, `S108.html=04e4c091715a…` — each equals its row's anchor prefix, its receipt's sha256, and the byte counts quoted in the rows (236387/8892/33289/111409). All four receipts: `http_status 200`, `fetched_at 2026-10-26T08:40-08:41Z`; S093's receipt url (raw.githubusercontent) is named inside S267's source cell (amendment 1 satisfied). Snapshots + receipts committed at CONTENT under `.ufo/evidence/round-48/freshness/sources/`.
4. **Rule 2 — append-only.** `git diff 473336d9 c7586b9a -- corpus/SOURCES.md` = exactly 4 appended lines (S265-S268), 0 modifications: no status/recheck/used-by change to any existing row. The lesson states "Rows touched old→new: none" — consistent, nothing unlogged. Ids are next-unused after S264, no `|` inside cells.
5. **used-by coherence.** Held rows S026/S048/S093/S108 keep their used-by cells; new rows S265-S268 list the same four entries; all four entries cite old id beside new (`incremental-pin-disposition.md` cites S048 ×2 and S266 ×1, etc.) — matches the Gate's "the entries keep the old ids beside the new".
6. **Gate admit/reject.** `## Gate` admits four superseding rows (detailed blocks for S265+S266 under `### Admit`, S267+S268 under `### Supersede`) and rejects twice (staged duplicates; package entry `r8-predictive-test-selection-cost.md`, each with reason and `Flip:`). ≥1 admit and ≥1 reject satisfied.
7. **Mistakes shape.** Nine rows (7 standing + 2 mined), each with class · evidence pointer · captured-by · fix. Red states d1-d7 all reproduce against artifacts present at CONTENT (`edd4ca44`/`663e0682` are ancestors; `spec-w2.json`, round-47 receipts, round-46 selftests all `cat-file -e` PRESENT). Mined rows' red receipts committed: `quality/pointer-check-red-15b1521.stdout` (2 MISSING lines, exit 1 at `15b1521e`), `quality/pointer-check-selftest.stdout` (cases=4 failed=0), round-47 `before/c1-at-freeze.stdout:18` vs `after/c1.stdout:18`.

## Findings (by severity)

**F1 — Low, factual drift (reference-drift).** The Gate's Supersede bullets cite stale SOURCES.md line numbers: lesson says "`corpus/SOURCES.md:140` appends S267" and "`corpus/SOURCES.md:141` appends S268"; at CONTENT S267 is line 142 and S268 is line 143 (140/141 are S265/S266). Show with:
`git -C tameshi-shokunin show c7586b9a10effc63b4bd327f976edc094c1bdc17:corpus/SOURCES.md | grep -n '^| S26'` → 140,141,142,143.

**F2 — Low, disclosed pending receipt (the mined-mistake-2 class, still open at CONTENT).** QUALITY 95 (`corpus/QUALITY.md:1418` at CONTENT) cites `.ufo/evidence/round-48/control/c1-controls.stdout` (CTL_B/CTL_E), and Mistakes row 1's fix rests on CTL_B; that receipt is ABSENT at CONTENT (`git cat-file -e c7586b9a:.ufo/evidence/round-48/control/c1-controls.stdout` fails; `control/` holds only `c2-controls.*` + `run-controls.py`) and also absent at the counter-freeze commit `755298415f8c` (ls-tree: `c2-controls.py`, `run-controls.py` only). Likewise `quality/c94-96-falsifiers.stdout` cited at `QUALITY.md:1398` is ABSENT at CONTENT. The lesson discloses this (row 1: "CTL_B and the counter receipts are freeze-step-2 artifacts and were not executed for this draft"; LOG attempt-2 entry: receipts "land with them"; pointer-check's green run deferred to the landing tip "a receipt cannot sit in the tree it measures"). Consequence for this item's standard: row 1's fix is shown able to fail only by the committed red input (`edd4ca44:.ufo/evidence/round-47/after/c1.stdout:5-6`), not by a committed receipt of the detector firing; rows 2-7 and both mined rows meet the standard. If the deciding-receipts commit lands without `c1-controls.stdout` / `c94-96-falsifiers.stdout`, F2 becomes a hard violation of the lesson's own QUALITY 96/97 gate.

## Minor observations (not gaps)

- S265/S266 anchor cells carry the snapshot sha256 prefix but not the snapshot path; contract C2 requires exactly the prefix, and the path resolves uniquely (one snapshot per target, hash-verified). S267/S268 anchors name both.
- My extraction offsets differ from the lesson's printed offsets by 1-19 chars (whitespace-collapse nuance); the material claims (substring, found once, line numbers) all verified.
- No live re-fetch was performed by this seat; quote verification is against the committed snapshots, which is what rule 1's location requirement and amendment 2 bind to.

## Residual risk and verification gaps

- CTL_A-E, the pointer-check green run at the landing tip, and the deciding receipts are pending by design; F2 is judged at the receipts-only commit, not at CONTENT.
- Review scoped to CONTENT `c7586b9a` as assigned; the lane worktree may have moved (deciding run in flight) and was not consulted.
- I ran no counter and no live fetch (bounds: probes are never verdicts); C2's live-fetch leg remains the frozen counter's deciding run.

Scratch dir `/fast/scratch/hyaku/tameshi-r48/T48W2RevLessonGate` deleted before finishing. No tools installed.
