# T55W1ExecC1Full — C1 dry run at the target (round 55, w1)

Seat: executor, leaf. Item: build a scratch clone at the frozen counter set
`631cd64`, apply every in-place round-54 stale fix and add the
`## Round 55 - round-54 record corrections` section to `SCORECARD.md`, then run
the frozen C1 counter and paste the verdict. Lane production files were not
edited; the patch is `-receipts/proposed.patch` and was demonstrated in a
scratch clone.

## Verdict at the edited revision

```
EXPLAIN R54.1 ok premise=ok corrected=ok stale=0 derived=CTL_MISMATCH + 2/3
EXPLAIN R54.2 ok premise=ok corrected=ok stale=0 derived=freeze pointer=077d431e
EXPLAIN R54.3 ok premise=ok corrected=ok stale=0 derived=total=13
EXPLAIN R54.4 ok premise=ok corrected=ok stale=0 derived=c2 digest=8528ee85
EXPLAIN R54.5 ok premise=ok corrected=ok stale=0 derived=w1=28 w2=25 sections=12
EXPLAIN R54.6 ok premise=ok corrected=ok stale=0 derived=sweep commit=ff2a821
EXPLAIN R54.7 ok premise=ok corrected=ok stale=0 derived=rename commit=7fa9a5e
EXPLAIN R54.8 ok premise=ok corrected=ok stale=0 derived=config.yml + fabricated + seat marked
EXPLAIN R54.9 ok premise=ok corrected=ok stale=0 derived=reviewers=5 attack=21/76 seats=76 staged=81
EXPLAIN R54.10 ok premise=ok corrected=ok stale=0 derived=controls-a rekeyed=0/7
C1_R55: rev=1a92b7839c3d classes=10 premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true
```

Exit 0. Receipt: `-receipts/c1-at-fixed-rev.stdout` (rev `1a92b7839c3d5fe5ecdbe936c7eed246b77062f2`
in the ephemeral clone; the patch reproduces it on any clone at `631cd64`).
No class refused: all ten arms pass.

At the frozen set the same command reads
`premise=10/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`
(`-receipts/c1-at-frozen-set.stdout`), matching `before/c1.stdout`.

## Patch (5 files, 148 insertions / 16 deletions)

`-receipts/proposed.patch`, `git apply --check` clean on a fresh clone checked
out at `631cd64`.

**`SCORECARD.md` — in-place stale fixes**
- round-54 paragraph: drop the `7883e0e5` pointer claim, state the one pointer
  `077d431e` (5 amendments), `[ER-R54-2]`.
- C1 claim row: `CTL_POS_c1 true` → `CTL_POS_c1` `CTL_MISMATCH` `2/3` at the
  revision it cloned, true only when re-scored at the deciding revision
  `[ER-R54-1]`.
- C2 claim row: `total=14` → `total=13`, and the inverted `14`/`13` delta
  parenthetical replaced by the receipt-backed statement `[ER-R54-3]`.
- measured-close line: `fe70474d` → `077d431e` `[ER-R54-2]`.

**`SCORECARD.md` — new section** `## Round 55 - round-54 record corrections`
(heading reproduced exactly, so the counter's `corrections()` finds it): ten
ER items, each old → derived value → command → receipt, plus a scope note that
names the two repairs the counter's stale arm cannot see (below).

**`corpus/QUALITY.md` 105** — falsifier no longer claims `rekeyed=7/7` "on its
positive control"; it now states `rekeyed=7/7` at the deciding revision and
`rekeyed=3/7` with `CTL_MISMATCH` at the freeze revision the phase-B check
cloned `[ER-R54-1]`.

**`corpus/lessons/round-54.md`** — `84 staged` → `81 staged`; R53.1 disposition
and the `## Mistakes` entry no longer claim the arm was "proven live by the
positive control … `rekeyed=7/7`".

**`LOG.md`** — round-54 entry: the `7883e0e5` parenthetical no longer calls it
"the freeze pointer the deciding run uses"; one pointer `077d431e` named.

**`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md`** — append-only SUPERSEDED
block (round 55, ER-R54-8): the operator-instruction claim is withdrawn, the
`config.yml` write named fabricated.

## Derivations (re-derived, not copied)

Every value was re-derived at `631cd64`; commands and raw output are in
`-receipts/derivations.txt`.

| Class | Derived | Command (abridged) | Receipt |
|---|---|---|---|
| R54.1 | `CTL_MISMATCH` + `2/3`, arm `rekeyed=3/7` | `grep -n 'CTL_MISMATCH\|CONTROLS_B' .ufo/evidence/round-54/control/controls-b.stdout` | `controls-b.stdout` |
| R54.2 | `077d431e` (5 amendments, 10 files) | `grep -o 'freeze=[0-9a-f]\{40\}' .ufo/evidence/round-54/after/frozen.stdout` | `after/frozen.stdout` |
| R54.3 | `total=13` | `grep -o 'total=[0-9]*' .ufo/evidence/round-54/before/c2.stdout` | `before/c2.stdout` |
| R54.4 | `8528ee85…` | `python3 -c '…freeze.json…["files"]["c2/measure.py"]'` | `round-54/freeze.json` |
| R54.5 | `w1=28 w2=25 sections=12` (23/23 reader files matched; 15 and 12 non-empty) | `git ls-tree -r --name-only <rev> -- .ufo/waves/round-54/<wave>` + `findings` length sum | `w1,w2/*Read*.json` |
| R54.6 | `ff2a821` | `git log --reverse --format=%h <rev> -- .ufo/waves/round-54/w2/T54W2Sent03.md` | `T54W2Sent03.md` |
| R54.7 | `7fa9a5e`, `R100` rename | `git show --name-status --format= 7fa9a5e \| grep forged-reader.json` | rename line |
| R54.8 | `config.yml` + `fabricated` + seat marked | seat grep; spot-check R54.8 | seat file, spot-check |
| R54.9 | `reviewers=5 attack=21/76 seats=76`, `staged=81` | `w1-registry.json` role_mix/attack_seats/seats; glob count under `merge/tameshi/knowledge` | registry, package |
| R54.10 | `controls-a.stdout` `rekeyed=0/7`; `0/30` belongs to `r53-counter-at-88afa941.stdout` | `grep -n 'CTL_R53' …/controls-a.stdout`; `grep -n 'rekeyed=' …/r53-counter-at-88afa941.stdout` | both receipts |

One self-correction during the run: my first R54.7 citation
(`git log --diff-filter=R <rev> -- <new path>`) returns **empty** — a
path-limited rename filter needs both paths. The section now cites the
reproducing form (`git show --name-status --format= 7fa9a5e | grep
forged-reader.json` → `R100 old new`; `git log -M --diff-filter=R -- <new>
<old>`), verified in `-receipts/blind-spots.txt`.

## Controls (frozen counter, unchanged bytes)

- **A — corrections section only, in-place fixes reverted**: `total=4`,
  `C1_R55_PASS=false`. The section is not a free pass; the stale arm still
  counts the untouched record. `-receipts/control-a-section-only.stdout`.
- **B — in-place fixes only, section removed**: `stale=0 classes_corrected=0/10
  total=10`, `C1_R55_PASS=false`. The corrected arm needs the section.
  `-receipts/control-b-inplace-only.stdout`.

Both clone commits are in ephemeral scratch (`99bcfb92aee7`, `64a18a9cdc24`);
the receipts carry their verdict lines.

## Findings against the frozen counter (reported, not fixed)

1. **R54.2's scan surface excludes `LOG.md`.** The stale arm reads only
   `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-54.md`, while
   `LOG.md:2500` carried the same false sentence ("the freeze pointer the
   deciding run uses"). The counter passes without it being repaired. Sweep:
   `git grep -n -E '7883e0e5|fe70474d|097985c1' 631cd64 -- '*.md'
   ':!.ufo/evidence' ':!.ufo/waves' ':!…spotcheck.md'` → `LOG.md:2500` plus the
   SCORECARD lines. Repaired in the patch; receipt `-receipts/blind-spots.txt`.
2. **R54.1's regex is same-line scoped.** `corpus/lessons/round-54.md:74-76`
   asserted "proves the arm on the positive control CTL_POS_c1, which /
   requires `rekeyed=7/7`" across a line break; the arm's
   `positive control[^\n]{0,160}rekeyed=7/7` matches neither line alone
   (`[False, False]`) and the counter passed with the false claim in place.
   Repaired in the patch; the regex/lines are shown in
   `-receipts/blind-spots.txt`.
3. **R54.8's seat arm is satisfied by coincidence.** The predicate is
   `"superseded" in seat.lower()`; at `631cd64` it is already true via an
   unrelated sentence (`LOG`-level: "the round-50 directive superseded it",
   seat line 299). The arm therefore cannot tell a marked claim from an
   unmarked one. My patch adds an explicit SUPERSEDED block anyway. Evidence:
   `-receipts/derivations.txt` (R54.8 section).
4. **R54.9's premise reads an out-of-lane path.**
   `STAGED_DEFAULT = /home/vgpnk/Projects/shokuknow`; if that tree is absent or
   moves, `staged=0` fails the class although the lane is unchanged. Measured
   `81` here (`-receipts/derivations.txt`).

## Integration notes for the L1

- The lane worktree at `631cd64` already carries an **uncommitted** repair of
  the same classes (`SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`,
  `corpus/lessons/round-54.md`, the seat file, tools). I did not touch it. My
  patch is an independent implementation: the two corrections sections quote
  the same erratum but differ in wording, and mine also repairs `LOG.md` and
  the wrapped `rekeyed=7/7` claim. **Apply one or the other, not both** — the
  additions conflict at the same anchors. The worktree version points at
  `corpus/lessons/round-55.md` (another seat's deliverable); mine names the
  corrections section itself, so it is self-contained.
- During this seat's run other seats also wrote the lane worktree: `M LOG.md`
  (the round-55 entry, appended after the round-54 close), `M corpus/SOURCES.md`
  (S280) and `?? corpus/lessons/round-55.md`. My patch's `LOG.md` hunk touches
  only the round-54 entry (lines ~2499-2502) and does not overlap the appended
  round-55 entry, but the `SCORECARD.md`, `corpus/QUALITY.md` and
  `corpus/lessons/round-54.md` hunks overlap the worktree's own edits at the
  same lines: rebase those by hand or take the worktree version for them and
  keep only the `LOG.md` hunk from this patch — the counter reads the same
  three files either way, and the two blind-spot repairs are the part the
  worktree version does not carry (it repairs `LOG.md`'s pointer only
  indirectly, if at all).
- The round-55 block and the re-stated standing axis table are not in this
  patch: they need the wave's measured results, which this seat does not own.

## No-harm / conformance

- `SKILL.md` untouched by this seat (no cold-read section drifted).
- Frozen path diff between `631cd64` and the edited commit under
  `.ufo/evidence/round-55/` is empty (`-receipts/clone.txt`).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  → exit 0 (`-receipts/census.txt`).
- Lane `git status`: only the pre-existing modifications plus the untracked
  `.ufo/waves/round-55/` (this seat's report and receipts). No lane production
  file written, no git/jj mutation in the lane.

## Tooling and environment

No installs or upgrades this round; nothing added to a PATH directory.
Incident: the first scratch tree (`/fast/scratch/hyaku/tameshi-r55/T55W1ExecC1Full`)
was deleted by a process outside this seat between 13:53 and 13:54 (only empty
`work-a`/`work-b` dirs survived; the clone, controls and required an immediate
redo). The redone work lives at `/fast/scratch/hyaku/t55-c1full-923625-1793206492`
and every artifact is persisted under the lane receipts dir, so nothing in the
delivery depends on scratch surviving.

## Risks

- The edited commit is in ephemeral scratch; the patch and the verdict receipt
  are the durable artifacts. Re-verification is
  `git clone --shared <lane> <d>; git -C <d> checkout --detach 631cd64;
  git -C <d> apply -receipts/proposed.patch; commit; python3
  .ufo/evidence/round-55/c1/measure.py --lane <d> --rev <new> --work <empty>`.
- `corrections()` terminates the block at the next `## ` line: any future
  round-55 section must be added after it with a `## ` heading, or its text
  will be swallowed as corrections.
