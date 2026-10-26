# T49Read06 — C1 reader, `## Mutation-sweep recipe`, pointer ordinals 25-29

Seat: T49Read06 (C1 reads). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base read: `8ca67421111fa354b47b803358391d0b07fc6db9` (lane HEAD at work time `455b2cd66fd9f237146a5355ca8bbc84f3071c50`; every target was read through `git show <base>:<path>`, never from the worktree).
Section: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`, frozen section sha256 `e37cf21e3155bdd39a68ef24a5135f2ad62861bbb5794ec954abf42bb0bd631d`, section_start 131 (`--list` reproduces the frozen value).
Slice: the five frozen pointers whose heading starts `## Mutation-sweep recipe` and whose ordinal is 25-29 — ordinals 0-24 and 30-33 of the same section are other seats'.

## Behavior

For each pointer: opened `SKILL.md` at base line `skill_line`, read the clause the pointer supports; opened the pointed target at base (line pointers: exactly `ranges`; multi-range: ranges joined, same as the counter's `pointed_text`); decided whether the target supports the clause; copied a verbatim excerpt and machine-tested it against the counter's own `norm()`/`pointed_text()` before writing it. All five rows are `holds`; no `proposed_fix` is emitted because no row is stale.

Commands that produce the evidence (all read-only):

```
python3 .ufo/evidence/round-49/c1/measure.py --selftest
python3 .ufo/evidence/round-49/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:SKILL.md | nl -ba | sed -n '224,229p;240,244p;375,378p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/mutation-case-kimi-census.md | nl -ba | sed -n '13,16p;20,21p;29,35p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/mutation-case-kagi-census.md | nl -ba | sed -n '13,17p;50,56p'
```

`--list` output is byte-identical to the frozen pointer file (`sha256 92a2e532fb323bee556e44b0877107339f7faa9e1c8f9636a8a6b1a8de6d4d3c` for both), so `skill_line`/`file`/`ranges` used here are the frozen ones, not re-derived ones.

## Per-pointer verdicts

| ord | raw | skill_line | verdict | one-line reasoning |
|---|---|---|---|---|
| 25 | `mutation-case-kimi-census.md:34-35` | 226 | holds | `corpus/knowledge/mutation-case-kimi-census.md:34-35` is the §0 restore proof: sha256 before/after both `83016d45…4f426`, `size 43273 B and mtime unchanged`, working tree clean for the path — exactly the three step-9 re-checks at `SKILL.md:224-227`. |
| 26 | `mutation-case-kagi-census.md:54-56` | 227 | holds | `corpus/knowledge/mutation-case-kagi-census.md:54-56` proves the same three plus `git status --porcelain` for the path empty and a `cmp`-identical scratch copy; sha abbreviation `275d8294…53009f` and `44212 B` match the pin at `:13-17`. |
| 27 | `SKILL.md:377-378` | 228 | holds | The self-pointer lands on the Restore discipline opening, whose second sentence is the cited limit verbatim: `Before/after fingerprints establish endpoint identity, not that no transient write occurred.` (`SKILL.md:377-378`); the `corrected in round 27, seat Read03` tag matches `.ufo/waves/round-27/w1/Read03.md:3` and `:19`. |
| 28 | `mutation-case-kimi-census.md:20-21,29-31` | 241 | holds | `:20-21` gives the control green and `(node v24.21.0)` (host/runtime version); `:29-31` gives 11 runs, `7.0 s wall` and `the 300 s timeout`; both halves of `Round2:7.0s for11 runs, nodev24.21.0` are located, no drift. |
| 29 | `mutation-case-kagi-census.md:50-53` | 243 | holds | `:50-53` gives 11 runs, `11.0 s wall for 11 runs (~1.0 s each)` and `against the 280 s per-run bound` — the round-3 cost half verbatim. |

No row is `stale`, `unresolved` or `absent`; no pointer's line numbers drifted at base (each pointed range still holds the text the clause needs, and every range is well inside the target's line count: kimi 238 lines, kagi 275, SKILL.md 2136).

## Gate / check receipts

- `--selftest`: `C1_R49_SELFTEST: cases=34 failed=0`, exit 0 (`T49Read06.selftest.txt`).
- Excerpt containment (the counter's own check, same functions): 5/5 rows have `24 <= len(norm(excerpt)) <= 400` and `norm(excerpt) in pointed_text(base blob, ranges)` — lengths 76, 81, 92, 129, 90 (`T49Read06.excerpt-check.txt`).
- Claim verbatim: 5/5 `norm(claim)` occur in `norm(SKILL.md@base)` after whitespace collapse, so every `claim` is a real SKILL.md substring and not a paraphrase.
- Pointer identity: 5/5 rows equal the frozen row on `heading, ordinal, raw, file, ranges`.

## Findings

1. No stale pointer in this slice. Five of five resolve at base and support their clause; the recipe section's restore-discipline and cost-profile citations are current at `8ca67421`.
2. Nuance recorded, not ruled stale (ordinal 28): the kimi note phrases the bound as `the whole sweep took 7.0 s wall against the 300 s timeout` (`corpus/knowledge/mutation-case-kimi-census.md:30-31`), while `SKILL.md:240` asks for a **per-run** timeout. The per-run attribution comes from SKILL.md's own step 6 (`SKILL.md:183-184`, `300 s used in round 2, 280 s in round 3`), and the kagi half states `280 s per-run bound` explicitly (`mutation-case-kagi-census.md:53`); the cited ranges still carry the timeout value, the wall time and the runtime version, so the pointer is not corrected here.
3. Integration note for the L1: ordinals 25-29 depend on `SKILL.md:377-378` (ordinal 27 is a self-pointer). Any edit above line 377 in the corrected section shifts the re-derived `ranges` for that pointer, so reads must be re-derived at REV after the section edits — the base rows here are base verdicts, not REV rows.
4. Integration note for the reads merge: rows carry both `base_verdict` and `verdict` (`holds`) so `check_reads` in `.ufo/evidence/round-49/c1/measure.py:302-312` accepts them unchanged if the section text is untouched at those lines.
5. Cross-seat consistency: sibling `T49Read01` also records all-holds for recipe ordinals 0-4 (`.ufo/waves/round-49/w1/T49Read01.rows.json`); the two slices agree on the frozen section sha `e37cf21e…bd631d`, so no section drift happened between wave-1 readers.

## Touched surfaces

Wrote only (all inside `.ufo/waves/round-49/w1/`): `T49Read06.rows.json`, `T49Read06.excerpt-check.txt`, `T49Read06.pointers-list.json`, `T49Read06.selftest.txt`, `T49Read06.md`. Lane checkout, `SKILL.md`, the target notes, the contract, the counters and the Git/jj state were not modified. Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read06/` is deleted at the end of this seat.

## Out of scope

Section corrections and the pointer-floor-preserving rewrites (L1 integration); re-derivation of reads at REV; the monitor/durability leg and the deciding run; C2; other sections' pointers. No counter was run in scoring mode — only `--selftest` and `--list`. No tool was installed or upgraded (nothing needed).

## Artifact paths (relative to the lane)

- `.ufo/waves/round-49/w1/T49Read06.rows.json` — 5 rows, all `base_verdict: holds`, `sha256 192c5efec7489ac80ec1e1828aa7502f2ae724b30fb631da4e21cd99925a6247`
- `.ufo/waves/round-49/w1/T49Read06.excerpt-check.txt` — containment receipt
- `.ufo/waves/round-49/w1/T49Read06.pointers-list.json` — `--list` at base, byte-identical to the frozen pointer file
- `.ufo/waves/round-49/w1/T49Read06.selftest.txt` — counter selftest, `cases=34 failed=0`
- `.ufo/waves/round-49/w1/T49Read06.md` — this report

## Summary

Read the five recipe-section pointers (ordinals 25-29) at base `8ca67421`: all five `holds`, none stale, none unresolved.
25/26: kimi and kagi §0 restore proofs give sha256-before/after, size, mtime and clean-tree exactly as step 9 asks.
27: `SKILL.md:377-378` states the endpoint-identity limit verbatim; round-27 Read03 provenance tag checks out.
28/29: round-2 (7.0 s, 11 runs, node v24.21.0, 300 s) and round-3 (11.0 s, 280 s per-run) cost facts are at the cited lines.
One nuance logged, not corrected: the kimi 300 s bound is phrased against the sweep wall; proven per-run only by `SKILL.md:183-184`.
No `proposed_fix` rows; no section edits made; counters used only as `--selftest` (34/34) and `--list`.
Rows are base verdicts — re-derive at REV because ordinal 27 points into SKILL.md itself and section edits shift it.
