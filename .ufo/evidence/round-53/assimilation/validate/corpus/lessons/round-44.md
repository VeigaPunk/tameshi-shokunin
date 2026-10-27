# Round 44 lesson

author: tameshi L1 (hyaku run 6, attempt 1)
date: 2026-10-25

## Gate

Theme: **repair the record-agreement false positive and re-open S089's anchor**.
This round adopts no shokuknow package entries (`Assimilation: none`); the package
was read-only and the quarantine verdicts remain those already recorded in the
round-40 lesson. One new source row, S160, is grounded below and cited by the
new knowledge entry. The staged package was re-read for the id-collision check;
its staged S160 is the PIT FAQ already held as lane S156 (see the collision
record below), not the Stryker source adopted here.

### Admit — S160 (new row): Stryker Mutator, *Equivalent mutants*

- URL https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/;
  opened 2026-10-25 with `curl -fsSL`, 38687 bytes, 23 lines, title
  `Equivalent mutants | Stryker Mutator`; SHA-256
  `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`.
  Snapshot: `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`.
  Independent second open by `ScoutStrykerSnapshot` was byte-identical
  (same length and digest; `cmp -s` exit 0).
- Located quotes in the `Equivalent mutant` example:
  - line 15, 20 words: “Notice that 10 ** 0 = 1, so even if we change >= to <= and even < or > we will get the same output each time!”
  - line 16, 12 words: “There is no definitive way for Stryker to find and ignore them.”
  - line 17, 9 words: “the only solution is by finding these by hand”.
- Scope: Stryker's documentation says equivalent mutants can be behaviorally
  indistinguishable in the example and no definitive automatic find/ignore
  method is available. It does not distinguish equivalent mutants from
  unreachable-code survivors; that separation remains the lane's K/D/E/U rule.
- Row change: append S160 as `mined`, opened 2026-10-25, recheck 180d,
  `used-by` `corpus/knowledge/r44-anchor-refresh-rule.md`. Existing S089's
  status, recheck and `used-by` remain unchanged. The anchor digest changed
  from `bc572676…e04d` (S089, opened 2026-10-22) to
  `79f6501a…4079ce` (this snapshot); the located sentences persist at the
  same offsets. S160's `teaches` opens `supersedes S089 —` and limits the
  correction to the anchor only.
- Census on the source row in the lane corpus: `sources-census.sh validate
  --file /tmp/tameshi-r44-mirror/corpus/SOURCES.md` → exit 0, no E-code;
  expected W04 duplicate URL for S160 (S089 already holds the same document).
  Round-end root census receipt is `.ufo/evidence/round-44/census-end.stdout`.

### Re-open — S089 (held; no in-place edit)

- S089 at `corpus/SOURCES.md` still points to the 2026-10-22 HTML digest
  `bc572676…e04d`. The live page and the committed round-44 snapshot agree at
  `79f6501a…4079ce`; text at the quoted offsets survives. Per SOURCES.md
  contract rule 2, this row's anchor is not changed in place: S160 is the
  append-only correction and explicitly supersedes S089's anchor only.
- Round-43 lesson records the prior digest comparison and same-offset quote
  check (`corpus/lessons/round-43.md:39-55`); this round's fresh open and
  snapshot are in the Gate above. This round makes no S089 `used-by` change.

### Refused / not adopted — package rows

No package row or knowledge file was adopted. The read-only staged-id guard
found 7 current collisions S153–S159 and, after considering staged S160,
8 collisions S153–S160. Staged S160 is PIT FAQ, already held by lane S156; the
by-document map is `staged:S160` → `S156`, not a new source adoption. The guard
reports safe floor S256, unmapped 0, naive map refused (cascade), and no package
append was made. The S160 lane row above is the new Stryker source, not a
re-labeling of the staged PIT FAQ. Read-only guard evidence:
`.ufo/waves/round-44/w1/SentinelIdGuard.md` and
`.ufo/waves/round-44/w1/CritC2Target.md`.

### considerthese

`considerthese/2026-10-24.md` proposal 2, **“Unreachable-provenance check,”**
is mined, not implemented: it proposes flagging receipts that cite a revision
not reachable from the lane repo, after the round-36 closure found a scratch-only
mutant commit. The round-44 m11 class checks that cited 40-hex objects exist in
the lane; it does not check reachability (objects can exist without being
reachable from the branch). A future claim must not present m11 as implementing
proposal 2. This reflection is a pointer, not evidence for the proposal; no
new source row is added for it.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| scope | `.ufo/evidence/round-44/before/c2-old-at-base.stdout`: the round-43 counter reports `m7=1 total=1 first=m7:SCORECARD.md#round-43_unknown_S256`; source is the historical `safe_floor=S256` assignment at `SCORECARD.md:2091` | none; the old record grammar masked the prose phrase `safe floor` but no criterion required assignment-form values to be masked | add `ASSIGN_ID` assignment-value masking in the round-44 successor and four T6 tests. Shown able to fail: removing only the mask makes `T6_safe_floor_value_not_citation` and `T6_assign_with_spaces_masked` fail with `['r unknown S256']`, exit 1 (`.ufo/evidence/round-44/control/mask-removed.selftest.stdout`; `w1/MutMaskRemove.md`). Genuine unknown/unmined IDs remain errors (`w1/CritM7Recall.md`). |
| scope | `.ufo/waves/round-44/w1/SentinelIdGuard.md`: the wave item/initial plan assumed staged ids ended below S160; the staged package actually has S153–S255, including staged S160 | `tools/staged-id-guard.py` (read-only 0–3-space collision extraction plus document-keyed mapping) | correct the report and lesson: staged S160 is PIT FAQ already held as S156; map it by document, keep package read-only, and do not treat the lane's S160 Stryker row as an adopted package row. Shown by the guard's `staged:S160 -> S156` held result; no blind arithmetic mapping is accepted. |
| landing | `.ufo/waves/round-43/w1/RevC2Classes.md` was a modified tracked worktree file at base; round-43 verifier spot-check routed it (`corpus/lessons/round-43-verifier-spotcheck.md:12,64`) | none | retain and commit the updated reviewer note as round-44 inherited evidence; its diff carries the A13/A14 m7/m8/m10 pin and line corrections. |
| number-drift | `.ufo/evidence/round-44/after/c1-at-83beaf9.stdout` initially reported `m6=1 standing=114 actual=115` after S160 was appended | the frozen m6 class: the newest `sources-registry` row must state the census-valid row count | append a new round-44 standing row using the census-valid 0–3-space pattern and count 115, rather than leaving round 43's standing count as newest. Shown able to fail at `83beaf980f246412368f89fbe7758375c8ca21e0` (`m6=1`) and re-measured after the fix. |

The round-43 verifier spot-check's other routed items were addressed: the S256
m7 false alarm is fixed and measured; the dirty wave note is explicitly
retained; S089's stale anchor is superseded without editing the old row.

## Census and quarantine

Start: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, 114 rows, W04 ×8 and W01 ×1, no E-codes; stdout/stderr `.ufo/evidence/round-44/census-start.stdout` and `.stderr`.
End: same command → exit 0, 115 rows, prior warnings plus the expected S160 W04 duplicate-URL warning, no E-codes; stdout/stderr `.ufo/evidence/round-44/census-end.stdout` and `.stderr`.
Quarantine slice re-derived read-only: 17 rows, 14 `payload-absent` and 3
`could-not-be-fetched`, byte-identical to the round-40 lesson list; no new
verdicts. Evidence `.ufo/waves/round-44/w1/ScoutQuarantine.md`.
