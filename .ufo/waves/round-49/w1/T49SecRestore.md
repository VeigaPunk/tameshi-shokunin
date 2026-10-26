# T49SecRestore — C1 section audit: `## Restore discipline` (SKILL.md:375-404 @ base 8ca67421)

Seat: C1 section critic (number / count / status / command / file-name / lane-claim audit beyond the line pointers).
Read-only on the lane; the only lane writes are this report and the four receipts beside it in
`.ufo/waves/round-49/w1/`. Scratch root `/fast/scratch/hyaku/tameshi-r49/T49SecRestore` (fixture clone
`clone/`, ledger replay workdir `regwork/`) is deleted before yielding. No tool was installed or upgraded.

Deliverable: `T49SecRestore.findings.json` (15 findings; 1 false, 2 unverifiable, 12 true, 5 with a
whitespace- or scope-only fix). Receipts: `T49SecRestore.section-at-base.txt`,
`T49SecRestore.proposed-fixes.diff`, `T49SecRestore.pointer-list-after-fixes.json`,
`T49SecRestore.ledger-replay-base.txt`.

## False (report first)

**SKILL.md:396 — "The historical probes reran from scratch".**
`cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && git show 8ca67421:SCORECARD.md | sed -n '13p' | grep -o "sensitivity re-runs[^;]*"`
→ `sensitivity re-runs from the lane's retained scratch: node /tmp/tameshi-r2-1-work/mutant-D2.mjs …`
The cited line records re-runs that *read the retained* /tmp scratch; "retained" contradicts "from scratch"
(the same row's "fresh /tmp copies" describes the sweep's mutants, not the re-runs). The clause was introduced
by `git show 8eaae28 -- SKILL.md`, which replaced step 6 "**Retain the scratch as evidence.** Both lanes' probes
re-ran from `/tmp/tameshi-r2-1-work/` and `/tmp/tameshi-r3-1-work/`; each note's reproduce spec rebuilds the
sweep even if /tmp is wiped" with "The historical probes reran from scratch" — the destination was collapsed
from `/tmp/…` to "from scratch" (the rebuild claim was rightly dropped, kagi's Erratum R21 refutes it). Fix:
`The historical probes reran from scratch` → `The historical probes' sensitivity re-runs\n   read the lane's
retained scratch`; `SCORECARD.md:13` and every other word of step 6 are kept.

## Unverifiable (undefined scope / undefined term)

**SKILL.md:383-384 — "`cp -p` the artifact into the lane namespace and edit only copies".**
`git show 8ca67421:corpus/knowledge/mutation-case-kimi-census.md | sed -n '4,5p'` → "every mutant is a copy
under `/tmp/tameshi-r2-1-work/`, and no fleet file was written"; `…kagi-census.md | sed -n '242,243p'` →
`cp -p kagi-shokunin/corpus/surface-census.sh /tmp/tameshi-r3-1-work/pristine.sh`.
`git grep -n 'lane namespace' 8ca67421 -- SKILL.md corpus tools` → exactly 1 hit, this line: the term is
defined nowhere and both cited copies land in /tmp *outside* the lane. The `cp -p` half is recorded
(kimi:172, kagi:44-45), so only the destination phrase is defective. Fix: "into scratch outside / the lane and
edit only copies".

**SKILL.md:377 — "All edits must stay in scratch."**
Prescriptive, and the universal reading is contradicted by the section itself (step 1 records in the note's
header, step 6 retains evidence in the lane) and by the cited record:
`git show 8ca67421:corpus/knowledge/mutation-case-kagi-census.md | sed -n '6,7p'` → "this note is the only
fleet file written by this run"; `git log --format='%h %ad %s' --date=short -- corpus/knowledge/mutation-case-kagi-census.md`
→ `53e74a8 2026-10-14 probation round 3 …` (the run's own lane commit). Scoped to the artifact the sentence
holds; unscoped it does not. Fix: "All substrate edits must stay in scratch."

## True, with a text-integrity fix (values verified)

**SKILL.md:387 / :389 — the two fingerprint sentences are garbled in the 8eaae28 rewrite.**
`git show 8ca67421:corpus/knowledge/mutation-case-kimi-census.md | sed -n '14p;34,35p'` →
``83016d45049b009a…2724f426``, 896 lines, 43273 B; before/after `83016d45…4f426`, mtime unchanged, path clean.
`…kagi-census.md | sed -n '14,15p;54,56p'` → ``275d8294a94e…b53009f``, 44212 B, mtime 09:47:15, path clean,
`cmp`-identical scratch copy. Prefixes/suffixes, both sizes and the mtime all match, but the section renders
`hash83016d45…4f426,43273B` and `hash275d8294…53009f,44212B, unchanged09:47:15`. Fixes are whitespace-only
(`hash 83016d45…4f426, 43273 B`; `hash 275d8294…53009f, 44212 B, unchanged 09:47:15`); no value changes.

## True (verified)

- **:380-382 step 1.** Both cited headers carry all five fields — `git show 8ca67421:corpus/knowledge/mutation-case-kimi-census.md | sed -n '13,16p'` and `…kagi-census.md | sed -n '13,17p'` (full sha256, size, mtime, repo revision, `git status --porcelain -- <path>` empty).
- **:388 "no after-repo revision was recorded".** `git show 8ca67421:corpus/knowledge/mutation-case-kimi-census.md | grep -n -Ei 'after|rev-parse|HEAD|revision'` → 11,13,34,103; the revision is pinned once (before), the after-proof has no HEAD. (SCORECARD.md:13 later re-reads `kumitate HEAD 175de6ba`; that closes the gap outside the note, which is what the sentence's own scope says.)
- **:391 "Its after-repo revision is likewise not established by those records".** `…kagi-census.md | grep -n -Ei 'after|rev-parse|revision'` → 10,54,56,256,272; no after HEAD.
- **:397-398 unversioned driver.** `…kimi-census.md | sed -n '174,175p'` and `…kagi-census.md | sed -n '245,246p'` both invoke `/tmp/…/mutate_driver.py`; `git ls-tree -r --name-only 8ca67421 | grep -c mutate_driver` → 0; kagi's Erratum R21 (:271-272) says it verbatim. Note: the section carries no pointer to kagi :271-274, and a new pointer would change the base pointer count (10), so none is proposed.
- **:399-400 maintained ledger replay.** `git show 8ca67421:tools/mutate-and-run.sh | wc -l` → 2080, `--regression` documented at :198/:215-223; its legs 1-2 are exactly the two cited sweeps (`grep -E '^PIN_JS=|^PIN_BASH='` equals the notes' hashes at kimi:14 / kagi:14). Probe, read-only on the lane with the workdir in scratch: `TMPDIR=$S/tmp bash tools/mutate-and-run.sh --regression --workdir $S/regwork` → exit 0, `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`, legs 1-2 `match=10/10 … kill-rate=80%` each. `grep -n mutate_driver` in the tool → only :745, a provenance comment: it does not recover the driver. Receipt: `T49SecRestore.ledger-replay-base.txt`.
- **:403 G-R2-1 / round-2 addendum.** `git show 8ca67421:corpus/README.md | sed -n '11p'` → the `gates-survey-kagi.md — round-2 addendum (G-R2-1…6)` row, whose G-R2-1 entry is the dirty-at-pin correction. Bare path pointer resolves at :11; left unnumbered (converting it to a line pointer would change the pointer kind).
- **:377-378 thesis.** "Before/after fingerprints establish endpoint identity, not that no transient write occurred" is a correct epistemic claim, consistent with steps 1 and 3; it is an unsourced inference with no `(I)` mark although SKILL.md:34 states inferences carry one (step 5 at :395 is marked). Recorded without a fix — the credit algorithm scores trace-bound inputs, not prose markers.
- **:394-395 never restore via git checkout/restore.** Correct (both rewrite the worktree) and marked `(I)`.
- **:401-403 step 7.** G-R2-1 is exactly the dirty-pin case: "the surveyed 79294/`357fb245` was an intermediate dirty-tree state never committed … kagi's own round-18 `fecee87` re-pinned `stamps.tsv`" (README:11).
- **:375 heading.** Matches the content (`grep -c continuous` in :375-404 → 1, the heading only). Not renamed.

## Pointer-count safety of the proposed fixes

The C1 predicate requires each section to keep its base pointer count. Applied to a scratch clone at base
(`git clone --shared`, fixes committed in `clone/`, toplevel asserted), the frozen extractor still reports:
`python3 -I .ufo/evidence/round-49/c1/measure.py --lane $S/clone --rev HEAD --list` → exit 0,
`total 90, restore 10`, raws identical (`mutation-case-kimi-census.md:13-16`, `…kagi-census.md:13-17`,
`…kimi-census.md:4-7`, `…kagi-census.md:44-45`, `…kimi-census.md:34-35`, `…kagi-census.md:54-56`,
`SCORECARD.md:13`, `mutate_driver.py`, `tools/mutate-and-run.sh`, `corpus/README.md`). This was a `--list`
probe, not a verdict; no filing fix deletes a pointer or renames the heading. Receipt:
`T49SecRestore.pointer-list-after-fixes.json`; the applied diff is `T49SecRestore.proposed-fixes.diff`.

## Summary

- One false statement: SKILL.md:396 says the historical probes "reran from scratch"; SCORECARD.md:13 records re-runs from the *retained* /tmp scratch (8eaae28 mis-rewrote that step).
- Two unverifiable-scope claims: :383 "lane namespace" (used nowhere else; both cited copies go to /tmp) and :377 "All edits must stay in scratch" (contradicted by the section's own steps 1/6 and by kagi:6-7).
- :387/:389 values are true but the 8eaae28 rewrite lost spaces ("hash83016d45…", "43273B", "unchanged09:47:15"); fixes are whitespace-only.
- :380-382, :388, :391, :397-398, :399-400, :403, :377-378, :394-395, :401-403 and the heading check out true at base.
- The maintained ledger replay was exercised at base: 9/9 legs PASS, exit 0, legs 1-2 = the two cited sweeps at the notes' own pins; it does not reconstruct the old driver.
- Five proposed fixes (3 claim/scope + 2 whitespace) keep all 10 restore pointers and the total at 90 (`--list` on the scratch fixture).
