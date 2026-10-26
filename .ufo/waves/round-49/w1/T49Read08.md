# T49Read08 — C1 reader, `## Restore discipline`, pointer ordinals 0-4

Seat: T49Read08 (C1 reads, wave 1). Lane `tameshi-shokunin`; base `8ca67421111fa354b47b803358391d0b07fc6db9`;
contract `.ufo/evidence/round-49/contract.json` read first, never edited. I decide nothing: every verdict below is a
`base_verdict` for the L1 to integrate.

## Scope and method

Item: for each pointer of `## Restore discipline — before/after identity, not continuous non-write proof` with
ordinal 0-4 (frozen in `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`), read the SKILL.md clause
at `skill_line` and the pointed text at base, and decide whether the target really supports the clause.

Commands used (read-only; `--list` is the one sanctioned counter mode, everything else is library calls of the
counter's own `list_pointers()` / `norm()` / `pointed_text()` / `extract()` / `check_reads()`):

```
git -C LANE show 8ca67421111fa354b47b803358391d0b07fc6db9:SKILL.md | sed -n '375,404p'
git -C LANE show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/mutation-case-kimi-census.md | sed -n '1,45p;140,180p'
git -C LANE show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/mutation-case-kagi-census.md | sed -n '1,60p;200,225p'
git -C LANE show 8ca67421111fa354b47b803358391d0b07fc6db9:corpus/knowledge/mutation-case-kimi-census.md | grep -n 'cp -p'
python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list
git -C LANE log --oneline -3 -L 4,7:corpus/knowledge/mutation-case-kimi-census.md 8ca67421
git -C ../kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs | sha256sum
git -C ../kagi-shokunin show fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh | sha256sum
```

(`LANE` = `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.)

Preconditions checked, not assumed: `--list` at base reproduces the frozen pointer identities byte-for-byte for
ordinals 0-4 (raw, file, ranges, `skill_line`), and the section hashes to
`13d489ad9898567f2f6620120fa819eee3251302caf502a4b04b782c8bdaabf8`, the sha in the pointer control
(`T49Read08.excerpt-check.txt`, lines 5-6).

## Results — one line of reasoning per pointer

| ord | pointer (raw) | skill line | verdict | reasoning |
|---|---|---|---|---|
| 0 | `mutation-case-kimi-census.md:13-16` | 382 | **holds** | `:13-16` records every field the clause names — full sha256 `83016d45…4f426`, 43273 B, mtime 2026-10-13 18:53:12, kumitate repo `175de6ba…`, and `git status --porcelain -- scripts/kimi-census.mjs` empty at `:16` — inside the note's header region. |
| 1 | `mutation-case-kagi-census.md:13-17` | 382 | **holds** | `:13-17` records sha256 `275d8294…53009f`, 44212 B, 886 newlines (887th unterminated), mtime 2026-10-14 09:47:15 -0300, kagi `HEAD fecee874…` at `:16`, and empty porcelain at `:17`. |
| 2 | `mutation-case-kimi-census.md:4-7` | 384 | **stale** | `:4-7` supports the scratch/copies half ("every mutant is a copy under `/tmp/tameshi-r2-1-work/`, and no fleet file was written") but does **not** carry the `cp -p` the clause prescribes; that literal is at `:172` in the same note. |
| 3 | `mutation-case-kagi-census.md:44-45` | 385 | **holds** | `:44-45` is the literal mechanism: one exact-string edit "applied to a fresh copy of `pristine.sh` (a `cp -p` byte copy, `cmp`-verified)". |
| 4 | `mutation-case-kimi-census.md:34-35` | 388 | **holds** | `:34-35` is the endpoint proof verbatim: hash before `83016d45…4f426` and after the same, 43273 B, mtime unchanged, kumitate tree clean for the path. |

Mechanical check of the five rows against the frozen pointer identities and ranges (`check_reads` at base):
`{'unresolved': 0, 'unverified': 0, 'excerpt_miss': 0, 'not_holds': 1, 'absent': 0}` — ord 2 is the `not_holds`
row (the stale read); the other four are `ok` (`T49Read08.excerpt-check.txt`, lines 12-14).

## Finding 1 (stale pointer, ord 2) — the clause prescribes `cp -p`; the pointed range does not carry it

- Clause (`SKILL.md:383-385`): "**All edits in scratch:** `cp -p` the artifact into the lane namespace and edit only
  copies (mutation-case-kimi-census.md:4-7; mutation-case-kagi-census.md:44-45)."
- `corpus/knowledge/mutation-case-kimi-census.md:4-7` supports "all edits in scratch / edit only copies" — it says
  the substrate is read-only, "every mutant is a copy under `/tmp/tameshi-r2-1-work/`, and no fleet file was
  written", and no live path was read. Shown by
  `git -C LANE show BASE:corpus/knowledge/mutation-case-kimi-census.md | sed -n '4,7p'`.
- It contains no `cp -p`: `git -C LANE show BASE:corpus/knowledge/mutation-case-kimi-census.md | grep -n 'cp -p'`
  prints only `172:cp -p kumitate-shokunin/scripts/kimi-census.mjs /tmp/tameshi-r2-1-work/pristine.mjs`; the same
  note calls the scratch file a "byte-copy" at `:150`. `cp -p` is what preserves mtime for the step-3 endpoint
  proof, so the omission is the mechanism, not decoration.
- Two earlier cold reads recorded the same aim defect and kept it as a minor gap: `.ufo/waves/round-17/w2/CR10.md:84-87`
  ("item 2's kimi anchor is indirect … the literal `cp -p` command is at §4:172") and
  `.ufo/waves/round-29/w1/Read02C.md:7` ("the literal `cp -p` command in that note is at :172"). Neither round
  corrected it; the base text is unchanged since the point was written (`git -C LANE log --oneline -L 4,7:…`, one
  addition at 2587e0a), so this is a mis-aimed pointer, not line drift.
- Proposed correction (one pointer kept, section floor 10 untouched; simulated against the extractor —
  `T49Read08.excerpt-check.txt`, lines 15-18): change
  `evidence (mutation-case-kimi-census.md:4-7;` to `evidence (mutation-case-kimi-census.md:4-7, :172;` in the
  `skill_old`/`skill_new` pair carried in the row's `proposed_fix`, giving `raw = mutation-case-kimi-census.md:4-7,
  :172` and `ranges = [[4,7],[172,172]]`. After the fix the extractor still yields 10 pointers with ordinals 0-9
  otherwise identical, and the `fixed_excerpt`
  `cp -p kumitate-shokunin/scripts/kimi-census.mjs /tmp/tameshi-r2-1-work/pristine.mjs` is inside the corrected
  pointed text. The L1 must re-key the ord-2 row on the new raw.

## Finding 2 (base SKILL.md prose defect, no verdict attached) — the step-3 sentence lost its spaces

`SKILL.md:387` reads `Kimi recorded hash83016d45…4f426,43273B, unchanged mtime and path cleanliness` and `:390`
reads `Kagi recorded hash275d8294…53009f,44212B, unchanged09:47:15 mtime` — `hash`/the hash value, the size and
`unchanged`/the time have been fused. Shown by
`git -C LANE show BASE:SKILL.md | sed -n '386,391p' | od -c` (no space bytes between `hash` and `8`, between `,`
and `4`, between `unchanged` and `0`). The damage landed in commit `8eaae28` ("round-21: land 75-seat falsification
…", `git -C LANE log -L 380,391:SKILL.md 8ca67421`). The pointed records themselves are correct (`kimi:34-35`
"size 43273 B and mtime unchanged"; `kagi:54-56` "44212 B and mtime 09:47:15 unchanged"), so no pointer is stale
because of it — but the L1 edits this section this round and can restore the four missing spaces while keeping the
heading text unchanged.

Context for the L1's re-key, observed in the frozen monitor receipt: this section is uncredited at base with reason
`input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh`
(`.ufo/evidence/round-49/control/monitor-at-base-8ca67421.json`, the section's `reason` field) — i.e. the lapse is
record drift on the ledger's inputs, not the pointer set read here.

Both historical pins are still true of the substrate bytes, so ords 0, 1 and 4 rest on live evidence, not just on
the notes' own arithmetic: kumitate `175de6ba…:scripts/kimi-census.mjs` → sha256 `83016d45…4f426`, 896 lines,
43273 B; kagi `fecee874…:corpus/surface-census.sh` → sha256 `275d8294…53009f`, `wc -lc` 886 / 44212.

## Gates run (observed)

- `--list` at base: identity equality with the frozen control for ordinals 0-4 (`True`), section sha
  `13d489ad…` (`T49Read08.excerpt-check.txt`, lines 5-6).
- Excerpt gate, self-tested before writing (the item's requirement): each excerpt is 126-376 collapsed
  characters and occurs in the whitespace-collapsed pointed text of its own ranges (lines 7-12).
- Counter `check_reads` at base over my five rows: `not_holds: 1` (ord 2, the stale read), everything else `ok`
  (lines 13-14).
- Fix simulation on the section text in memory: `skill_old` occurs once, 10 pointers before and after, ord 2
  becomes `mutation-case-kimi-census.md:4-7, :172` with `ranges [[4,7],[172,172]]` (lines 15-18).
- No counter invocation other than `--list` and library calls; no deciding run, no scratch-tree measurement, no
  model passed, no `agent://all` message.

## Out of scope / known limits

- Base verdicts only; corrections, re-keying and any deciding run are the L1's. Ordinals 5-9 (`kagi:54-56`,
  `SCORECARD.md:13`, `mutate_driver.py`, `tools/mutate-and-run.sh`, `corpus/README.md`) belong to other seats —
  read here only where a neighbour sentence mattered, never judged.
- Support is judged semantically here; the counter cannot see it (contract `c1.cannot_see`). My `holds` rows quote
  text that supports the clause, not text that merely resolves.
- I did not read `/home/vgpnk/.local/state/`, the C2 panel, or `round-49/control/c2-*.stdout`; no fixture repo was
  created; nothing was committed or installed (pacman paused host-wide; no tool needed).
- Files written, all inside the wave dir: `T49Read08.rows.json`, `T49Read08.excerpt-check.txt`, this report.
  Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read08` removed before yield.

## Summary

- Ordinals 0-4 of `## Restore discipline` read at base against their targets: 4 `holds`, 1 `stale`, 0 unresolved/absent.
- ord 0 `kimi:13-16` and ord 1 `kagi:13-17` carry every before-sweep field the clause lists; both pins re-hash to the
  named substrate bytes at their pinned revisions.
- ord 4 `kimi:34-35` is the endpoint proof verbatim (hash before = after, size, mtime, clean path).
- ord 3 `kagi:44-45` carries the literal `cp -p` byte copy plus `cmp` verification.
- ord 2 `kimi:4-7` is stale: it supports "edits in scratch / only copies" but the clause's `cp -p` is at `:172`;
  proposed fix extends this one pointer to `:4-7, :172` (extractor-simulated, pointer count stays 10).
- Separate prose defect for the L1: `SKILL.md:387` and `:390` lost their spaces in `8eaae28`
  (`hash83016d45…4f426,43273B`, `unchanged09:47:15`).
- Rows: `.ufo/waves/round-49/w1/T49Read08.rows.json`; receipts: `T49Read08.excerpt-check.txt`.
