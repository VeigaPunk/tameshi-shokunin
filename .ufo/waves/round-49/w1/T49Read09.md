# T49Read09 — C1 reader: `## Restore discipline`, pointer ordinals 5-9

Seat: C1 reader (wave 1). Section: `## Restore discipline — before/after identity, not continuous non-write proof`
(SKILL.md base lines 375-403). Base `8ca67421111fa354b47b803358391d0b07fc6db9` (lane tip observed `455b2cd6`;
all reads are `git show <base>:<path>` blobs, never working-tree bytes).

Deliverable: `T49Read09.rows.json` (`{"rows": [...]}`, 5 rows, one per pointer ordinal 5-9).
Receipts: `T49Read09.excerpt-check.txt` (mechanical excerpt/meta verification), `T49Read09.pointers-list.json`
(frozen counter `--list` at base).

Counters: `--selftest` and `--list` only, no measuring invocation, no deciding invocation, no scratch-tree run.
No tools installed (nothing was needed; pacman untouched per the host-wide pause).

## Pointer-by-pointer

| ordinal | pointer (raw) | base_verdict | one-line reasoning |
|---|---|---|---|
| 5 | `mutation-case-kagi-census.md:54-56` | **holds** | kagi:54-56 is the restore-proof bullet: sha256 before=after `275d8294…53009f`, `44212 B`, mtime `09:47:15` unchanged, `git status --porcelain` empty, `/tmp/…/pristine.sh` `cmp`-identical — every element of the clause, and the line numbers did not drift. |
| 6 | `SCORECARD.md:13` | **holds** | SCORECARD.md:13 (round-2 depth row) carries `sensitivity re-runs from the lane's retained scratch` plus `Re-run 2026-10-14 (TAMESHI-SCR)` and re-derivable `--selftest`/pin commands, which is what "The historical probes reran from scratch" cites; pointer attaches to that first half only. |
| 7 | `mutate_driver.py` | **absent** | The bare path resolves nowhere at base (root, `corpus/`, `corpus/knowledge/`, `corpus/lessons/` all miss; no filename matches `mutate_driver`), and the sentence names it as *unversioned* — a file deliberately not held. `--list` reports `file=None kind=None`; `absent` is the honest verdict the frozen counter accepts (measure.py:271-278). |
| 8 | `tools/mutate-and-run.sh` | **holds** | The file exists at base and its own header (tools/mutate-and-run.sh:215-219) defines `--regression` as the leg ledger that `replays every recorded mutation case as a leg ... at its pinned revision, materialized from the repo's git object store`, listing both case-note gates (`js-kimi-census`, `bash-surface-census`) — the "those pinned cases" claim, with the pinned-blob replay being exactly why it "does not recover the old driver". |
| 9 | `corpus/README.md` | **holds** | corpus/README.md:11 is the round-2 addendum row and its first item is G-R2-1 (`§1 claim-ledger pin corrected: 79301 B / sha256 first16 93c5827202b9cdec — the surveyed 79294/357fb245 was an intermediate dirty-tree state never committed`), i.e. precisely the "a dirty pin is not a clean baseline; re-pin a committed revision" lesson. |

Verification of every excerpt (collapsed with the counter's own rule `re.sub(r'\s+',' ',t).strip()` against the
pointed text: pointed lines for line pointers, whole blob for path pointers):

```
HOLDS mutation-case-kagi-census.md:54-56 len=102 inside=True meta=True
HOLDS SCORECARD.md:13 len=52 inside=True meta=True
ABSENT mutate_driver.py meta=True file=None ranges=None -> True
HOLDS tools/mutate-and-run.sh len=105 inside=True meta=True
HOLDS corpus/README.md len=163 inside=True meta=True
FIX SCORECARD.md:16 len=150 inside=True occurs_once_in_section=1
ALL_OK=True
```
(`T49Read09.excerpt-check.txt`; produced by a replication of measure.py's `norm`/`pointed_text`/`check_reads`
rules, with `file`/`ranges` compared to the counter's own `--list` rows.)

Pointer inventory sanity (`--list` at base): `total 90`, `missing_headings []`, per-section counts
34/10/17/5/5/9/10 — identical to the contract floors and to
`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`. My section contributes ordinals 0-9
(10 pointers); this seat owns 5-9.

## Proposed fix (only non-`holds` row)

ordinal 7 `mutate_driver.py` (absent). No edit is *required* by the predicate (the counter accepts `absent` for
an unresolvable path pointer), but the section names an unheld file with no resolvable trace. The additive
correction keeps the name and its `absent` row and adds the record where the unversioned/one-off fact is
actually written:

- `skill_old`: `` `mutate_driver.py` and do not directly rebuild after scratch loss. `` (occurs once in the
  section and once in base SKILL.md — checked)
- `skill_new`: ``` `mutate_driver.py` (one-off and not in-tree; `SCORECARD.md:16`) and do not directly rebuild after scratch loss. ```
- `fixed_file`: `SCORECARD.md`, `fixed_ranges`: `[[16,16]]`
- `fixed_excerpt`: `the mutation method existed only as prose + a per-lane ad-hoc driver left in /tmp (round 2's mutate_driver.py was one-off, unversioned, not in-tree)` (150 collapsed chars, located in SCORECARD.md:16)
- `why`: SCORECARD.md:16 (round-3 operability row) is where "round 2's `mutate_driver.py` was one-off,
  unversioned, not in-tree" is written; the clause currently has no resolvable support. Restore pointer count
  10 → 11 (floor 10 still met, nothing deleted); the new line pointer takes ordinal 7 and shifts the three path
  pointers to 8/9/10, so the L1 must re-derive ordinals/rows at the corrected text.

## Findings

1. **Lost spaces inside the C1 target section (prose defect, not a pointer defect).** Base `SKILL.md:387` reads
   `Kimi recorded hash83016d45…4f426,43273B, unchanged mtime` and `SKILL.md:389` reads
   `Kagi recorded hash275d8294…53009f,44212B, unchanged09:47:15 mtime` — the hash/size/mtime triples are fused
   (`unchanged09:47:15`), where the pointed sources write `44212 B and` / `mtime 09:47:15 unchanged`
   (corpus/knowledge/mutation-case-kagi-census.md:54-55). Command:
   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:SKILL.md | sed -n '387,390p' | cat -A`.
   This does not make ordinals 4-5 stale (the text still says the true thing), but the L1 is rewriting this
   section and can repair the spacing while keeping both pointers.
2. **The second half of the section-6 sentence has no pointer.** "but the case-note commands rely on an
   unversioned `mutate_driver.py`" is documented at `SCORECARD.md:16`, not at the `SCORECARD.md:13` pointer that
   precedes it (SCORECARD.md:16: `| 3 | operability | ... round 2's mutate_driver.py was one-off, unversioned,
   not in-tree ...`). Command:
   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:SCORECARD.md | sed -n '13p;16p'`.
   Ordinal 6 stays `holds` (its pointer is scoped to the rerun clause); adopting row 7's fix closes the gap.
3. **Ordinal 8's tool genuinely covers "those pinned cases."** tools/mutate-and-run.sh:215-219 names
   `js-kimi-census` and `bash-surface-census` among 9 ledger legs replayed at pinned revisions from the git
   object store. Command:
   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:tools/mutate-and-run.sh | sed -n '215,219p'`.
4. **Ordinal 7's absence is by design, not a missing blob.** `git -C … ls-tree -r --name-only 8ca67421… | grep -c mutate_driver`
   → `0`; counter `--list` → `"raw": "mutate_driver.py", "file": null, "kind": null`. The only near-namesakes in
   the tree are `.ufo/evidence/round-23/mutate.py` and `.ufo/evidence/round-46/hardening/mutate.py`, which are
   different artifacts and are not what the sentence means.

## Observed counter output (non-measuring modes only)

- `TMPDIR=$S python3 -B .ufo/evidence/round-49/c1/measure.py --selftest` → `C1_R49_SELFTEST: cases=34 failed=0`
  (exit 0).
- `python3 -B .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list`
  → 90 pointers, `missing_headings []` (receipt: `T49Read09.pointers-list.json`).
  These are listing/self-test modes; no `measure()` call, no `--work`, no deciding run, no scratch tree.

## Out of scope / not done

- No claim decision, no SKILL.md edit, no reads.json assembly (L1's integration), no controls scored.
- Ordinals 0-4 and 10+ belong to sibling seats; I read only what ordinals 5-9 need.
- Scratch root `/fast/scratch/hyaku/tameshi-r49/T49Read09/` created and removed; no live clone created.

## Summary

- Ordinals 5, 6, 8, 9: `holds`; ordinal 7 (`mutate_driver.py`): `absent` (unversioned by design, resolves nowhere at base).
- All four `holds` excerpts are located verbatim in the pointed text under the counter's collapse rule; row metadata matches `--list` exactly.
- One proposed fix: qualify the absent `mutate_driver.py` with a resolvable `SCORECARD.md:16` record pointer, keeping the name and pointer count (10 → 11).
- No stale line drift found in this section; no line-number corrections are needed for 5-9.
- Flaggable prose defect at SKILL.md:389 (fused `unchanged09:47:15`, `hash…53009f,44212B`) for the L1's rewrite, plus the uncited second half of the section-6 sentence (SCORECARD.md:16).
- Counters observed only in `--selftest` (34/34) and `--list` (90 pointers) modes; no measuring or deciding invocation.
- Deliverables: `T49Read09.rows.json`, `T49Read09.excerpt-check.txt`, `T49Read09.pointers-list.json`, this report.
