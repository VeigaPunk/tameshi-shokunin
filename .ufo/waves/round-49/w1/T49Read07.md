# T49Read07 — C1 reader, `## Mutation-sweep recipe`, ordinals 30-33

Seat item: read the four pointers of `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`
with ordinal 30-33 against their targets **at base** `8ca67421111fa354b47b803358391d0b07fc6db9`,
decide `holds | stale | unresolved | absent`, and record a located excerpt that the frozen counter's
collapse rule accepts. Deliverables: `T49Read07.rows.json`, `T49Read07.excerpt-check.txt`,
`T49Read07.counter-probe.txt`, this report. I decide nothing: C1 belongs to the L1.

## Method (every target read through git blobs at base, never the working tree)

```
S=/fast/scratch/hyaku/tameshi-r49/T49Read07
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <BASE>:SKILL.md > "$S/SKILL.md"     # 2136 lines
git -C … show <BASE>:corpus/README.md > "$S/corpus/README.md"                                 # 591 lines
git -C … show <BASE>:corpus/knowledge/gates-survey-kagi.md                                     # 619 lines
git -C … show <BASE>:corpus/knowledge/mutation-case-kimi-census.md                             # 237 lines
git -C … show <BASE>:corpus/knowledge/mutation-case-kagi-census.md                             # 274 lines
awk 'NR>=150 && NR<=160 {printf "%d| %s\n", NR, $0}' SKILL.md      # clause contexts, lines 156 and 235-236
grep -n "G-R2-1" corpus/README.md                                  # -> 1 hit, line 11
grep -n -i errata corpus/knowledge/gates-survey-kagi.md            # -> 503, 545
grep -n '^## ' corpus/knowledge/mutation-case-*.md                 # section inventories
```

Confirmed the frozen extractor sees these four exactly as the control file does (probe 1 in
`T49Read07.counter-probe.txt`): `--list` at base prints `pointers=90 missing_headings=[]` and, for
ordinals 30-33, `raw/file/ranges/skill_line` identical to
`.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`. All four are **path** pointers
(`ranges: null`, whole-file target), so no line number can drift for them.

## Rows

| ord | raw | file | skill_line | verdict | one-line reasoning |
|---|---|---|---|---|---|
| 30 | `corpus/README.md` | corpus/README.md | 156 | **holds** | The clause "…the kagi claim-ledger pin was once surveyed from a dirty intermediate state and had to be re-pinned (corpus/README.md G-R2-1 row; …)" is carried verbatim by the README coverage-map row at `corpus/README.md:11`: "the surveyed 79294/`357fb245` was an intermediate dirty-tree state never committed; … (10:05:10) re-pinned `stamps.tsv` (G-R2-1)". |
| 31 | `gates-survey-kagi.md` | corpus/knowledge/gates-survey-kagi.md | 156 | **holds** | The clause's second half "gates-survey-kagi.md errata block" resolves: `## 10. Errata (append-only)` at `:503` holds `### Errata (round 2)` at `:545`, and **G-R2-1** at `:554-566` states the same never-committed dirty survey, the `git cat-file -t 357fb24554cd0447` failure, and the `fecee87` re-pin. |
| 32 | `mutation-case-kimi-census.md` | corpus/knowledge/mutation-case-kimi-census.md | 235 | **holds** | Step 10's clause "the two mutation-case notes are the model (mutation-case-kimi-census.md §1, §3-§6; …)": all four cited sections exist at base (`:39 §1`, `:109 §3`, `:148 §4`, `:183 §5`, `:193 §6`) and supply the listed record elements — kill-rate table with class/edit-site/exit/suite-line/verdict/failing-case columns (`:39-53`), by-class tally (`:55-57`), protected/not-protected inventory (`:111+`), reproduce spec + commands (`:148+`), calibration E1 (`:185-191`), unknowns U1-U6 (`:195-207`). |
| 33 | `mutation-case-kagi-census.md` | corpus/knowledge/mutation-case-kagi-census.md | 236 | **holds** | Clause "mutation-case-kagi-census.md §1-§7)": all seven sections exist (`:62 :105 :128 :162 :184 :193 :208`) and cover the same elements, including the survivor sensitivity checks and driver commands at `:239-254`; the append-only `## Erratum R21` at `:261` lands *after* the cited range, so §1-§7 as cited is unchanged. |

No row is `stale`, `unresolved` or `absent`; therefore no `proposed_fix` object is emitted (the item
requires one only for non-`holds` rows) and **no SKILL.md text needs changing in this range**. Pointer
count for the section stays at its base 34 (`--list` prints 34 recipe pointers, ordinals 0-33), which is
the frozen floor (`contract.json` floors.recipe = 34) — the section cannot fall below it.

## Findings

**F1 — All four pointers hold; nothing in ordinals 30-33 is stale at base.** Evidence per row above.
The only mechanical gate that could fail is the excerpt collapse rule; all four excerpts pass it:
`T49Read07.excerpt-check.txt` (`30 … len=182 in_pointed=True`, `31 … 380`, `32 … 236`, `33 … 223`),
computed with the counter's own normaliser `re.sub(r'\s+',' ').strip` at
`.ufo/evidence/round-49/c1/measure.py:202-203` and the whole-file rule for path pointers at
`.ufo/evidence/round-49/c1/measure.py:309-311`.

**F2 (integration hazard, not a C1 semantic finding) — the frozen reader keys on `verdict`, not
`base_verdict`.** `check_reads` branches on `row.get('verdict')`
(`.ufo/evidence/round-49/c1/measure.py:270` row lookup, `:274` absent arm, `:304` the
`row.get('verdict') != 'holds'` arm) while the wave-1 seat items ask for
`base_verdict`. Observed, by importing the frozen module and calling `check_reads` against the base
blobs (probe 3 in `T49Read07.counter-probe.txt`): with only `base_verdict` present, my four rows scored
`not_holds` — `ALL90 {"unresolved": 9, "unverified": 77, "excerpt_miss": 0, "not_holds": 4, "absent": 0}`;
after adding `"verdict": "holds"` beside `"base_verdict": "holds"`, the same rows score
`{"unresolved": 9, "unverified": 77, "excerpt_miss": 0, "not_holds": 0, "absent": 0}` and every one of
mine prints `ok`. Three sibling row files currently carry `base_verdict` only (checked read-only with a
`json.load` tally over `.ufo/waves/round-49/w1/*.rows.json` and then per-seat `check_reads`, probe 5 in
`T49Read07.counter-probe.txt`): `T49Read02.rows.json` 5 rows → 5 `not_holds`; `T49Read10.rows.json`
6 rows → 4 `not_holds` + 2 `unresolved` (ords 0-1 hit file-null pointers); `T49Read11.rows.json` 6 rows →
5 `not_holds` + 1 `unresolved` (ord 11, same reason). So the copy-straight-in cost is **14 rows scoring
`not_holds`**, while the 3 rows on unresolvable pointers are their seats' already-stated re-key items.
The counter's own `unresolved` total (9) is pointer-level and constant regardless of rows — 8 file-null
pointers plus the external `../PROTOCOL.md:63-68` that no row supplies a `fleet_commit` for (probe 6) —
so it must not be read as a per-seat bad-row count. T49Read10 independently re-read the code and made the
same correction (its `.md:152-170` carries a reads-assembly note asking the L1 to map `base_verdict →
verdict` on ords 2-5 and re-key ords 0-1). Either the integrator maps the key when assembling
`.ufo/evidence/round-49/c1/reads.json`, or those 14 rows register `not_holds`. I did not edit a sibling
file. Observed at the end of the seat, read-only: the lane has since acquired an untracked
`.ufo/evidence/round-49/c1/merge-reads.py` (93 lines, another seat's deliverable, not in the freeze) whose
row picker requires `base_verdict == 'holds'` and emits `verdict='holds'` carrying the row's excerpt
(`merge-reads.py:45-46`); rows merged through it are therefore safe, and my four rows qualify on the
key the picker compares (heading, raw, file, ranges, base_verdict). F2 is thus a hazard only for a
verbatim concatenation that bypasses that merge.

**F3 (observation, no fix proposed) — kimi's survivor-probe narrative sits outside the cited
§1/§3-§6.** Step 10 lists "survivor probes" among the record elements; the kimi pointer cites §1 and
§3-§6, but the D2 boundary probe narrative is in §2 at `mutation-case-kimi-census.md:83` and in the
round-5 append at `:218`. The pair still covers the element: kagi §7 carries the survivor sensitivity
commands and expected outputs at `mutation-case-kagi-census.md:247-254`. Adding §2 to the kimi pointer
would raise the section's pointer count above the base 34 that the contract's work-plan expects the L1
to keep ("each section keeping its base pointer count", `contract.json` C1.predicate), so I record it
rather than propose it.

**F4 — Probes are not verdicts.** Everything above is `--list`, `--selftest`, or a read-only function
call of the frozen `check_reads` against base blobs. No `measure.py` full invocation was made in any
lane; `C1_R49_SELFTEST: cases=34 failed=0` (exit 0) is recorded as observed only.

## Touched surfaces

- Written (only these): `.ufo/waves/round-49/w1/T49Read07.rows.json`,
  `.ufo/waves/round-49/w1/T49Read07.excerpt-check.txt`,
  `.ufo/waves/round-49/w1/T49Read07.counter-probe.txt`, `.ufo/waves/round-49/w1/T49Read07.md`.
- Read-only: the lane checkout via `git show` blobs and `glob`/`grep`/`awk`; the frozen counter
  (imported, not executed to a verdict); the frozen control pointer file; `contract.json`; sibling
  `*.rows.json` files (JSON tally only); and the untracked `.ufo/evidence/round-49/c1/merge-reads.py`
  (93 lines) and `refresh.py` (127 lines) that landed during the seat from another owner — `wc -l` and
  `grep` only, neither executed.
- No git/jj mutation, no `git add/commit/...`, no writes outside the four files above, nothing under
  `/home/vgpnk/Projects/shokunin` (fleet root), `/home/vgpnk/Projects/shokuknow`,
  `/home/vgpnk/.local/state/`, and neither `c2-WITNESS.stdout` nor the other C2 control stdouts.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read07/` was the only working area and is deleted before
  yield (`rm -rf`), so no scratch path is cited as evidence; the receipt files carry the commands and
  observed lines instead.
- Tooling: no install or upgrade was needed; nothing added to PATH; no pacman transaction attempted.

## Out of scope (left to the L1)

- Editing the seven SKILL.md sections (no correction is needed for 30-33 per F1).
- Assembling `.ufo/evidence/round-49/c1/reads.json` and the section re-key (F2 is the handoff hazard).
- Any deciding invocation, the monitor re-run, and the C1 label.

## Summary

- Ordinals 30, 31, 32, 33 of `## Mutation-sweep recipe` are all **holds** at base `8ca67421`; none stale.
- 30/31 (path pointers at SKILL.md:156) are backed by `corpus/README.md:11` and `gates-survey-kagi.md:503-566` (G-R2-1).
- 32/33 (path pointers at SKILL.md:235-236) are backed by the kimi §1/§3-§6 and kagi §1-§7 section inventories and their record contents.
- All four excerpts pass the frozen collapse rule (182/380/236/223 chars, `in_pointed=True`).
- `--list` at base reproduces the frozen 90-pointer list with missing_headings empty; `--selftest` 34/34.
- No `proposed_fix` emitted: no non-holds row; the section stays at its 34-pointer floor.
- Hazard for integration: `check_reads` keys on `verdict`; 14 sibling rows carry only `base_verdict` and would score `not_holds` if concatenated verbatim, though `merge-reads.py:45-46` maps the key (3 further rows sit on unresolvable pointers, already routed to re-key).
- Probes only — the deciding run and the C1 label remain the L1's.
