# ScribeGate — reject paragraph for staged `r4-gate-write-path-audit` (S137)

Seat: scribe (leaf, no delegation). Axis: discernment. Date: 2026-10-24.
Dispatch: `.ufo/waves/round-40/dispatch-w1.json:179-183` / `.ufo/waves/round-40/spec-w1.json:148-149`.
Lane writes: this report only. Live lesson untouched. No pacman (paused); no tools installed; scratch `/tmp/tameshi-r40-ScribeGate/` unused (nothing needed it).

## Draft reject paragraph (paste-ready; house two-field convention)

```markdown
### Reject — staged `r4-gate-write-path-audit` (S137)

Reason: quarantined `payload-absent`; the round-39 flip is still unmet. The cited revision
`31687496` is `31687496b5f34b153626e123d12ae2febdbd86a0` (2026-10-23 18:57:14 -0300), a
round-35 tally-receipt commit — subject "round-35: final before + v2 control receipts on the
9-copy panel (before exit 1; control 0/6 kill 0/3 accept exit 1) + tool selftest 33/33 under
the final pins" — touching only `.ufo/evidence/round-35/control/c1-v2-control.stdout` (M) and
`.ufo/evidence/round-35/lessons/selftest-33.out` (A). No write-path census payload is in that
tree: no path matches `write-path`, `tools/write-path-census.py` is absent at that revision,
and `.ufo/evidence` there ends at round-35. `payload-absent`, not a fetch failure.
Flip: a hand-check that locates a write-path census artefact at that revision whose counts
reproduce — the artefact must exist in `31687496`'s tree, and re-running it at that revision
must return the counts the row claims (zero write sites over the four
`kumitate-shokunin/scripts/{kimi-census,claims-check,round-gate,cite-check}.mjs` pins).
```

## What was rejected

- Staged entry: `/home/vgpnk/Projects/shokuknow/lanes/tameshi/round4/KNOWLEDGE-PROPOSED.md:160-165`
  — `corpus/knowledge/r4-gate-write-path-audit.md`, header `source: S141 … the four pinned gate
  blobs … @ revision 31687496 — measured 2026-10-23`, recheck "re-run the `git show` write-site
  grep over the same four pins (expect zero matches for every write pattern)".
- Its source row: `/home/vgpnk/Projects/shokuknow/lanes/tameshi/round4/SOURCES-PROPOSED.md:22`
  (S141, claim "the surveyed gates contain no file-write call sites at all").
- Id note (discernment): the wave item and the round-39 verifier table
  (`corpus/lessons/round-39-verifier-spotcheck.md:54`) call the staged payload **S137**; the
  staged header names source row **S141**. Both ids denote this one staged entry — not two items.

## Evidence — my own read-only commands (lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`)

1. `git rev-parse '31687496^{commit}'` → `31687496b5f34b153626e123d12ae2febdbd86a0`.
2. `git show -s --format='%H%n%ci%n%s' 31687496` → `2026-10-23 18:57:14 -0300`;
   subject "round-35: final before + v2 control receipts on the 9-copy panel (before exit 1;
   control 0/6 kill 0/3 accept exit 1) + tool selftest 33/33 under the final pins".
3. `git show --no-color --name-status --format='%s' 31687496` → exactly two paths:
   `M .ufo/evidence/round-35/control/c1-v2-control.stdout`,
   `A .ufo/evidence/round-35/lessons/selftest-33.out`.
4. `git ls-tree -r --name-only 31687496 | grep -i write-path` → no output (0 hits).
5. `git cat-file -e 31687496:tools/write-path-census.py` → exit 128, "fatal: path
   'tools/write-path-census.py' exists on disk, but not in '31687496'" (present in the working
   tree, absent at the cited revision).
6. `git ls-tree --name-only 31687496:.ufo/evidence` → ends at `round-35`; `31687496:tools/`
   lists tally/witness/mutate tools only — no census tool, no round-39/40 evidence.

Items 3-6 are the payload-absent proof; item 2 is the tally-receipt proof. No census artefact
exists at `31687496`, so the flip cannot be tested against this tree — it stays unmet.

## Discernment notes

- Class: `payload-absent` (unreproducible citation), not the prose `could not be fetched` class
  (S113/S123) — the lane already keeps these apart (`corpus/lessons/round-39.md:31-33`).
- Not load-bearing but recorded: the row also fails on the merits. The source owner's own
  correction, `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r5-gate-write-site-census-corrected.md:13-23`,
  says "That count was wrong. The same command on the same blobs returns 15 for `kimi-census`"
  (corrected six-gate total: 86 sites). A "counts reproduce" flip would therefore also have to
  survive that contradiction.

## Live-lesson status (not edited by this seat)

- Original reject: `corpus/lessons/round-39.md:21-24`.
- Verifier agreement: `corpus/lessons/round-39-verifier-spotcheck.md:54` ("`payload-absent`
  holds. Flip condition is still unmet.").
- The live round-40 lesson already carries this reject at `corpus/lessons/round-40.md:24-27`;
  per dispatch I did not edit it. The block above is this seat's independent draft, grounded in
  the commands of the previous section.

## Known limits

- The frozen counters (`.ufo/evidence/round-40/census/measure.py`, `.ufo/evidence/round-40/s108/measure.py`)
  were not run in any mode — not needed for a text draft; the deciding default-mode run stays
  with the L1 after settlement.
- `git show`/`ls-tree`/`cat-file -e` reads only; no lane, jj, git-index, `.ufo/state`, or
  shokuknow mutation. Reports on shokuknow staged rows are quoted, not modified.
