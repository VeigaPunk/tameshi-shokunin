# ScribeReadme — coverage-map row for `knowledge/r41-variable-destination-writes.md`

Seat: `L1Tameshi41.ScribeReadme` (scribe, axis `coverage`, milestone "README row").
Read-only seat: the lane checkout was not edited; the only write is this report.

## Behavior (the deliverable)

One row, three cells, matching the `| Note | Holds | Sources |` shape already used at
`corpus/README.md:5`, `:45`, `:224`, `:244`, `:263` (verified: `grep -n '^| Note | Holds | Sources |' corpus/README.md`
returns exactly those five headers, all three-cell).

Drafted row, verbatim, single sentence in the Holds cell, no pipe characters inside any cell:

```markdown
| `knowledge/r41-variable-destination-writes.md` | Variable-held write destinations now resolve: `tools/write-path-census-v3.py` walks the `ast` tree to depth four through assignment, `os.path.join`, `+`, `/` and f-strings, and on `tools/repeat-control.py` resolves both live sites to scratch-exempt expected-value destinations — `:811` (open of `expected.json`, an expected-value destination v2 does not record) and `:820` (`os.symlink` destination, no v2 write site at all) — so the round adds visibility of the destination, with no aliases, closures, attribute reassignment or conditional assignment resolved, no dataflow guarantee and no gate coverage. | S153, S154 |
```

Placement: the `## Round 41 — variable-destination write census (round 41)` section landed
while this seat worked — `corpus/README.md:513` (file now 524 lines; round-40 section still
at `:505`). On my first read it was a two-cell table; a sibling normalized it before this
report closed: header `| Note | Holds | Sources |` at `:515` and the note row at `:517`,
both three-cell, Sources cell `S153, S154`:
`python3 -c "l=open('corpus/README.md').read().splitlines(); print([(i+1,l[i].count('|')-1) for i in (514,516)])"`
→ `[(515, 3), (517, 3)]`. The shape requirement is therefore met live; no landing is needed
for shape, and nothing above `:513` moved, so prior `path:line` cites stay valid.
My drafted row below is a **wording variant**, not a second entry: it names each live site
by write form and states the v2 miss per site (`:811` expected-value destination absent in
v2; `:820` no v2 write site), where the live `:517` Holds carries the unbound-attribute /
non-folding-call false-positive caveat instead. If the L1 prefers the per-site phrasing,
replace only the Holds text at `:517`; do not append a second Round-41 section, since
`:513-524` already carries the section and its `**Coverage-map move (F4).**` paragraph.

If a fresh section is ever required (only after `:513-524` is retired), append verbatim at
end of file — never insert:

```markdown
## Round 41 — variable-held write destinations (round 41)

| Note | Holds | Sources |
|---|---|---|
<the row above>
```

## Gates / checks actually run (all read-only)

1. `grep -n '^| Note | Holds | Sources |' corpus/README.md` → `5, 45, 224, 244, 263` at first
   run; re-run after the sibling append → `5, 45, 224, 244, 263, 515` (six headers, all
   three-cell);
   per-line cell counts computed as `l.count('|')-1` → all `3`. Shape matched, not invented.
2. `grep -n 'S15[34]\b' corpus/SOURCES.md` → rows landed at `corpus/SOURCES.md:123` (S153)
   and `:124` (S154); `awk` status cells both `mined`; `used-by` both
   `corpus/knowledge/r41-variable-destination-writes.md`. `grep -c '^| S[0-9]' corpus/SOURCES.md`
   → **109** rows; tally **81 mined / 22 queued / 6 rejected**. So the row cites no unmined
   S-id (C1 m7) as of this check.
3. `python3 tools/write-path-census-v3.py --file tools/repeat-control.py` →
   `:811 open expected=1 scratch=1 unflagged=0`, `:820 os.symlink expected=1 scratch=1 unflagged=0`,
   summary `expected_sites=2 parse_errors=0 scratch_expected=2 sites=6 symlink_expected=1 unflagged=0 variable_expected=1`.
   Both cited sites resolve as expected-value + scratch-exempt + unflagged, which is exactly
   what the Holds cell asserts.
4. `sha256sum .ufo/evidence/round-41/sources/*.html` → `ast.html`
   `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317`, `pathlib.html`
   `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093` — identical to the two
   `source:` header lines at `corpus/knowledge/r41-variable-destination-writes.md:1-2`.
5. The Holds wording was read off the note itself
   (`corpus/knowledge/r41-variable-destination-writes.md`, sections "The measured finding" and
   "What is not claimed"): depth four, `os.path.join`/`+`/`/`/f-string, aliases/closures/
   attribute reassignment/conditional assignment excluded, no dataflow guarantee, no gate
   coverage. No number in the row lacks a receipt.

I did not run C1 or C2 (`measure.py`) in any mode — the deciding run belongs to L1.

## Touched surfaces

- Written: `.ufo/waves/round-41/w1/ScribeReadme.md` (this report) only.
- Read: `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/r41-variable-destination-writes.md`,
  `tools/repeat-control.py`, `tools/write-path-census-v3.py`, `.ufo/evidence/round-41/{contract.json,sources/*.html}`.
- Not edited: the lane checkout, SCORECARD.md, SOURCES.md, README.md, the note, sibling lanes, jj/Git state.

## Out of scope

- Landing the row (the L1 or a designated writer applies it; this seat is read-only).
- The round-41 lesson, SCORECARD block, and SOURCES rows (sibling scribe seats).
- Any judgment on C1/C2; no counter run.

## Findings

1. **F-R41-README-1 (dependency closed late, then satisfied):** when this seat started,
   `corpus/SOURCES.md` held 107 rows with highest id S152 and the note did not exist, so the
   requested row would have cited two unmined S-ids. Re-checked at write time: S153/S154 rows
   landed at `corpus/SOURCES.md:123-124`, both `mined`, `used-by` already naming the note, and
   the registry reads 109 rows / 81 mined / 22 queued / 6 rejected. The row is now citeable;
   if a later edit reverts either row's status, the row must not land.
2. **F-R41-README-2 (transient draft state — no standing defect, nothing routed):** this
   seat's first read of the note, before it settled, marked the S153 quote "(16 words)" and
   the S154 quote "(17 words)". The settled note at write time reads **15** and **16**
   (`corpus/knowledge/r41-variable-destination-writes.md:11` and `:17`), which matches
   whitespace tokenization exactly:
   `python3 -c 'print(len("The ast module helps Python applications to process trees of the Python abstract syntax grammar.".split()), len("Open the file pointed to in text mode, write data to it, and close the file".split()))'`
   → `15 16`. Recorded only because the earlier value is in this seat's transcript; both
   quotes stay ≤ 25 words and the note's counts now agree with the source text. No message
   sent to `L1Tameshi41.ReviewScribeEntry` and nothing left unedited as debt.
3. **F-R41-README-3 (transient shape deviation, resolved upstream — no standing defect):**
   the Round-41 section first landed as a two-cell table: no `| Note | Holds | Sources |`
   header, row at `:515` with `count('|')-1 == 2`, S153/S154 inside the Holds prose. Before
   this report closed a sibling normalized it — header now at `:515`, note row at `:517`,
   `[(515, 3), (517, 3)]`, Sources `S153, S154`. The remaining difference is wording only
   (live Holds adds the unbound-attribute / non-folding-call false-positive caveat and omits
   the per-site v2 statement my draft carries). Recorded because both states are in this
   seat's transcript; nothing is routed as a defect and I did not edit the file.
4. Observed, not mine: `git status --porcelain` at write time shows ` M corpus/QUALITY.md`,
   ` M corpus/README.md`, ` M corpus/SOURCES.md` and the untracked note — sibling seats'
   in-flight edits. I wrote none of them.
5. The Holds cell deliberately says "visibility of the destination", not "closes the
   write-path census": both live sites are scratch fixtures (`unflagged=0`), so no new open
   write path is asserted — consistent with the note's own non-claim section and the C2
   `declared_scope_limit`.

6. **Cross-lane scratch notice, checked and inapplicable:** mado seat IRC reported
   `.ufo/waves/round-35/scratch/<Seat>/` relocated to `scratch-evidence/<Seat>/` (a move, not
   a delete) and later that the checkpoint commit `4efaf63` tracks 240 such files. This report
   cites no path under any `round-35` tree —
   `grep -n 'round-35\|scratch/' .ufo/waves/round-41/w1/ScribeReadme.md` → exit 1 (before this
   item). Tameshi does have its own `round-35` wave tree — `git ls-files .ufo/waves/round-35 |
   wc -l` → **76** (dirs: `w1/` 7, `w2/` 55, `residual/` 5, plus dispatch/spec/validate
   files) — but it carries **no** `scratch/` or `scratch-evidence/` subdirectory
   (`find .ufo/waves/round-35 -maxdepth 1 -name 'scratch*'` → empty). No citation repaired,
   nothing rebuilt, no sha pinned to a rebuild. (An earlier draft of this item said tameshi had
   "no round-35 wave tree"; that was a check of `scratch-evidence` only and is corrected here,
   verbatim, rather than rewritten.)

Report: .ufo/waves/round-41/w1/ScribeReadme.md
