# T49Read05 — C1 reader, `## Mutation-sweep recipe`, pointer ordinals 20-24

Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `8ca67421111fa354b47b803358391d0b07fc6db9`.
Seat is a C1 reader for the five frozen pointers of heading
`## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` with ordinals 20-24.
Read-only on the lane except this report and the two deliverables below; no claim decided, no
deciding counter run, no SKILL.md edit, no git/jj mutation, nothing under `~/.local/state/` or the
two C2 panel receipts opened.

## Method (what was executed)

- Pointers copied from `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`
  (sha256 `92a2e532fb323bee556e44b0877107339f7faa9e1c8f9636a8a6b1a8de6d4d3c`), filtered to
  heading + ordinals 20-24. Frozen section: start 131, end 245, sha256
  `e37cf21e3155bdd39a68ef24a5135f2ad62861bbb5794ec954abf42bb0bd631d`.
- Extractor agreement: `python3 .ufo/evidence/round-49/c1/measure.py --list --lane
  /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8ca67421…` → exit 0, `n=90`,
  `missing_headings=[]`, and the emitted pointer list is byte-equal to the frozen control's
  (`equal True`).
- Every clause read at base `SKILL.md` line `skill_line`; every target read from
  `git -C LANE show 8ca67421:<file>` at the pointed lines.
- Containment proved with the frozen counter's own `norm()` / `pointed_text()` / `check_reads()`:
  each excerpt is 24-400 chars, whitespace-collapsed, and occurs in the collapsed pointed text;
  each `claim` also occurs verbatim in the collapsed section text. Receipt:
  `.ufo/waves/round-49/w1/T49Read05.excerpt-check.txt`. Result for this seat's five pointers:
  `5 rows, 5 ok, 0 not ok`; `check_reads` counters for the five: `excerpt_miss=0`, `not_holds=0`,
  `unverified=0` (the other pointed ordinals show `unverified` only because this seat read 20-24).
- No drift between base and the wave-1 tip for either target file:
  `git -C LANE diff --stat 8ca67421 HEAD -- corpus/knowledge/mutation-case-kimi-census.md
  corpus/knowledge/mutation-case-kagi-census.md` prints nothing.
- Tooling: nothing installed or upgraded. Python 3.14.8, git 2.56.0.

## Verdicts, one line each

| ord | pointer | SKILL.md clause at base | verdict |
|---|---|---|---|
| 20 | `corpus/knowledge/mutation-case-kimi-census.md:44-53` | :205-207 `**Survived** = green with the same count as control …` | **holds** |
| 21 | `corpus/knowledge/mutation-case-kimi-census.md:29-31` | :211-212 `Round 2: 8/10 = 80 %, no inconclusive run, 11 runs in 7.0 s` | **holds** |
| 22 | `corpus/knowledge/mutation-case-kagi-census.md:50-53` | :213 `Round 3: 8/10 = 80 %, 11 runs in 11.0 s` | **holds** |
| 23 | `corpus/knowledge/mutation-case-kimi-census.md:82-99` | :216-218 `JS D2 on an empty root: one fewer id … D10: frozen=24 (vs 25)` | **holds** |
| 24 | `corpus/knowledge/mutation-case-kagi-census.md:111-114, :118-122, :251-253` | :218-221 `Bash B5: mutant SURFACE OK … ; B10: ok=0 where pristine prints ok=1` | **holds** |

No pointer in 20-24 is stale and none is unresolved/absent. Two boundary facts are recorded
below for the L1 because they are range-precision issues, not support failures.

## Reasoning per pointer

**ord 20 — holds.** `mutation-case-kimi-census.md:44-53` is the §1 kill-rate table body (D1-D10);
:45 is the D2 row (quoted as the excerpt) and :53 the D10 row, both `exit 0`, `43/43 pass` /
`PASS`, `**survived**`, 0 failing cases — the clause's "green with the same count as control →
a finding, never a footnote". Boundary: the control row itself is :43, one line above the range,
so "same count as control" is read by comparing the survivors' `43/43 pass` with it. The "names a
gap until a case pins it" half is developed in §2 (:82-99), which the section cites separately at
SKILL.md:218. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show
8ca67421:corpus/knowledge/mutation-case-kimi-census.md | sed -n '44,53p'`.

**ord 21 — holds.** `:29-31` carries every element verbatim: `**kill rate 8/10 (80 %)**`,
`No inconclusive run`, `each of the 11 runs (control + 10) produced a definitive suite verdict`,
`the whole sweep took 7.0 s` (and continues `wall against the 300 s timeout`, the bound SKILL.md:183
cites). Round identity matches: `(TAMESHI-R2-1)` at :1, `round 2` at :3. Command: `git -C
/home/vgpnk/Projects/shokunin/tameshi-shokunin show
8ca67421:corpus/knowledge/mutation-case-kimi-census.md | sed -n '29,31p'`.

**ord 22 — holds.** `:50-53` states `**kill rate 8/10 (80 %)**`, `each of the 11 runs`,
`the whole sweep took 11.0 s wall for 11 runs (~1.0 s each) against the 280 s per-run bound`, and
the held 16-case denominator (`SELFTEST: PASS (16 cases)`) that SKILL.md:192-194 leans on. The
survivors named (B5, B10) match the kill-rate table at :64-76 (B5 :71, B10 :76) and the survivor
analyses at :107 and :118. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show
8ca67421:corpus/knowledge/mutation-case-kagi-census.md | sed -n '50,53p'`.

**ord 23 — holds.** §2, `:82-99`. D2 half at :90-92 (`on an empty root (28 findings) — pristine
prints six ids then +22 more; D2 prints five ids then +23 more; both exit 1`), D10 half at :98-99
(`same empty root — pristine FAMILY K2  members=0  checked=0 frozen=25; D10 … frozen=24`). Both
survivor labels also match the table at :45 and :53. Command: `git -C
/home/vgpnk/Projects/shokunin/tameshi-shokunin show
8ca67421:corpus/knowledge/mutation-case-kimi-census.md | sed -n '82,99p'`.

**ord 24 — holds, with a range boundary the L1 may tidy.** B5 pair at :113-114 (pristine
`SURFACE DIVERGED … (declared exec, no execute bit)` exit 1; mutant `SURFACE OK       … (exec 644)`
exit 0) and B10 pair at :121-122 (pristine's CLEAN summary carries `ok=1`, the mutant's carries
`ok=0`, both exit 0) quote both halves of the clause verbatim, so the pointer as a unit supports
the sentence. The third range `:251-253` is the reproduce block's sensitivity paragraph: it opens
on the blank line after the fence (:251) and stops at :253, while the paragraph is :252-254 and
its last line :254 ends `ok=0` (pristine `ok=1`), both exit 0. This is a precision defect present
since the file was created, not drift:
the paragraph is at 252-254 in both revisions (`git -C LANE show 53e74a8:… | sed -n '251,254p'`
and `… show 8eaae28:…` are identical there), and base..HEAD is unchanged. Optional tidy, exact and
pointer-preserving (`34/34` stays): `skill_old` = `(mutation-case-kagi-census.md:111-114, :118-122,
:251-253)`, `skill_new` = `(mutation-case-kagi-census.md:111-114, :118-122, :252-254)`;
`fixed_ranges` = `[[111,114],[118,122],[252,254]]`. Dry run on the base section text, recorded in
the receipt: `skill_old` occurs exactly once in the section and once in base `SKILL.md`; pointers
`34/34` before and after; ord 24 becomes `mutation-case-kagi-census.md:111-114, :118-122, :252-254`
with ranges `[[111,114],[118,122],[252,254]]`; the other 33 raws are identical; and a 161-char
`fixed_excerpt` (the B10 pair) occurs in the corrected pointed text. Command: `git -C
/home/vgpnk/Projects/shokunin/tameshi-shokunin show
8ca67421:corpus/knowledge/mutation-case-kagi-census.md | sed -n '111,114p;118,122p;251,254p'`.

## Gates observed

- `measure.py --list` at base: exit 0, 90 pointers, equal to the frozen control, `missing=[]`.
- Containment checker: exit 0; ords 20/21/22/23/24 `ok`; `excerpt_miss=0`, `not_holds=0`.
- `git -C LANE diff --stat 8ca67421 HEAD -- <both target files>`: empty.

## Touched surfaces

- `.ufo/waves/round-49/w1/T49Read05.rows.json` (new; sha256
  `0a72e6daa740a7f1e0e89a50028b15c47fa665837f44aad2f99277d462be49a6`).
- `.ufo/waves/round-49/w1/T49Read05.excerpt-check.txt` (new receipt; sha256
  `1990753ccc14dc36075e41244449c72caa8baeaa613e2f00fb72b504e216adda`).
- `.ufo/waves/round-49/w1/T49Read05.md` (this report).
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read05` — deleted before yielding.

## Out of scope (not done, by bound)

- No SKILL.md or target-file edit (the L1 integrates corrections), no `reads.json`, no
  `merge-reads.py` run, no contract edit, no counter deciding invocation, no git/jj mutation.

## Summary

Five pointers read at base — ordinals 20-24 of `## Mutation-sweep recipe`: all hold, none stale/unresolved/absent.
Verbatim support at kimi `:44-53`, `:29-31`, `:82-99`; kagi `:50-53`, `:111-114/:118-122/:251-253`; excerpts 143-284 chars.
Located with the counter's own `norm()`/`pointed_text()`/`check_reads()`: these five rows are `5 ok` (`excerpt_miss=0`, `not_holds=0`).
`measure.py --list` at base equals the frozen 90-pointer control; `git diff 8ca67421 HEAD` on both targets is empty (no drift).
Boundary, not a support failure: ord 20's control row is `:43`, one line above its range.
Boundary, not a support failure: ord 24's third range should read `:252-254` (paragraph is 252-254 in both revisions; tidy dry-run keeps `34/34`).
Deliverables: `T49Read05.rows.json` (sha256 `0a72e6da…be49a6`), `T49Read05.excerpt-check.txt`, this report.
No claim decided, no deciding counter run, nothing installed, no lane git/jj state touched, scratch deleted.
