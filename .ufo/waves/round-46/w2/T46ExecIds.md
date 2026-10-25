seat: T46ExecIds
item: re-ran the assimilation id checks (0-3-space extractor, `comm -12` collisions, in-registry duplicate check, `staged-id-guard` verdict and adoption-map re-validation, indented-row proof) on the FINAL registry at CONTENT `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` — ids are clean (120 rows, 8 collisions, 0 duplicates, next_free S261); the committed `adoption-map.json` is no longer admissible against that registry (guard exit 1, `map_clash S259,S260`), explained and isolated by counterfactual probe.

# Method and bounds

- Scratch: `/tmp/tameshi-r46-T46ExecIds/` (all artifacts below live there).
- Read-only on the lane: only `git -C <lane> show`/`log`/`ls-tree`/`status`/`diff --stat` and `sha256sum` of the worktree. No git add/commit/checkout, no jj command, no write under `/home/vgpnk/Projects/shokuknow`, no campaign counter run.
- Registry under test, extracted from the CONTENT revision, not the worktree:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  6f2168e028ce7ff6e82ac92093ac05dd1f147c32:corpus/SOURCES.md > /tmp/tameshi-r46-T46ExecIds/SOURCES.md
exit=0   wc -l = 470
sha256sum = 2ae73a7bf4e5d644768d6aeca10d0833bdca931a2df4389cec3f5d94b4ce86d8
```
  The guard's own `registry_sha256` field prints the same digest, so the tool read the same bytes I did.
- Staged package copied (not read in place) from the read-only package:
  `cp /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md /tmp/tameshi-r46-T46ExecIds/` → 109 lines, sha256 `020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807` (equals the guard's `staged_sha256`).
- Freeze registry also extracted for the reproduction of the freeze-time receipt: `git show 745a583…:corpus/SOURCES.md` → 467 lines, sha256 `f726a60186eee32db2927b3d22ecf1646ab5d7a5497b28acf9990416657d4710`.
- The worktree is clean for the files I measured: `git -C <lane> status --porcelain -- corpus/SOURCES.md tools/staged-id-guard.py` → no output; `git -C <lane> diff --stat 6f2168e0… -- corpus/SOURCES.md tools/staged-id-guard.py .ufo/evidence/round-46/assimilation/` → no output. Tool pin: `tools/staged-id-guard.py` at CONTENT and in the worktree are both `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`.

# 1. Extractor counts (CORPUS 0-3-space pattern)

Command, run once per file:

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <file> | grep -oE 'S[0-9]+' | sort
```

| file | ids | committed receipt | relation |
|---|---|---|---|
| `SOURCES.md` @ CONTENT | **120** (`reg-ids.final`) | `.ufo/evidence/round-46/assimilation/reg-ids` = 117 | `cmp` DIFF; `comm -13` → `S258 S259 S260`, `comm -23` → empty |
| `SOURCES.append.md` (package) | **103** (`staged-ids.final`) | `staged-ids` = 103 | `cmp` IDENTICAL |
| collisions (`comm -12`) | **8** (`collisions.final`) | `collisions` = 8 | `cmp` IDENTICAL |

The reg-ids delta is the intended +3: the receipt is a freeze-time artifact (registry max S257) and the CONTENT registry holds the three adoptions. Nothing was removed:

```
comm -13 .../assimilation/reg-ids reg-ids.final   → S258 S259 S260
comm -23 .../assimilation/reg-ids reg-ids.final   → (empty)
tail -8 reg-ids.final                             → S158 S159 S160 S256 S257 S258 S259 S260
```

Cross-check against the guard's own parser: `registry_rows=120`, `staged_rows=103`, i.e. the extractor and `ROW_RE` see the same rows on both files.

# 2. Collisions and duplicates

```
comm -12 reg-ids.final staged-ids.final
S153 S154 S155 S156 S157 S158 S159 S160        (8)
```

Byte-identical to the committed `collisions` receipt (`cmp` → IDENTICAL). All eight are the held staged rows; the guard still dedupes them to `{S153:S105, S154:S106, S159:S155, S160:S156}`.

Duplicates inside each file (`sort | uniq -d`):

```
dupes_reg_count=0     # sort reg-ids.final | uniq -d      → empty  (MUST be empty: OK)
dupes_staged_count=0  # sort staged-ids.final | uniq -d   → empty
```

Each adopted id occurs exactly once as a row:

```
grep -cE '^ {0,3}\|[[:space:]]*S258[[:space:]]*\|' SOURCES.md → 1
grep -cE '^ {0,3}\|[[:space:]]*S259[[:space:]]*\|' SOURCES.md → 1
grep -cE '^ {0,3}\|[[:space:]]*S260[[:space:]]*\|' SOURCES.md → 1
```

No id at or above S261 is present (the awk filter over the extracted ids printed nothing), so no future id was burned. Cell shape of the three new rows matches the registry: histogram over all 120 rows is `Counter({11: 120})`; `S258/S259/S260` each parse with 11 cells like `S256/S257`.

# 3. Guard verdict on the FINAL registry (no map)

```
python3 -I <lane>/tools/staged-id-guard.py --registry SOURCES.md --staged SOURCES.append.md --json
exit=0
```

Key fields (`guard-final.json`):

```
verdict=answered   refused=false   next_free=S261   safe_floor=S261
registry_rows=120  registry_docs=105  registry_max=S260  staged_max=S255
collision_count=8  cascade_count=0  unmapped=[]  column0_miss=[]  extractor=0-3space
naive_map={S153:S261 … S160:S268}
```

Freeze baseline for the same command (same staged file, freeze registry): `registry_rows=117 registry_docs=102 registry_max=S257 next_free=S258 safe_floor=S258 collision_count=8 verdict=answered refused=false`. So the id surface moved exactly as the contract says: +3 rows, +3 distinct documents, floor S258 → S261, collision set and cascade unchanged.

Guard selftest, run read-only: `python3 -I tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` / `VERDICT: PASS`, exit 0.

(Note on stderr: `guard-final.err` holds 141 B and `guard-freeze.err` 148 B — `od -c` shows both contain only the harness's `+ python3 -I …` trace line, not tool output. An earlier attempt to pipe `2>&1` into a JSON reader failed on exactly that trace line; the tool's stdout is pure JSON.)

# 4. Guard with the committed adoption map: NO LONGER ADMISSIBLE

```
python3 -I <lane>/tools/staged-id-guard.py --registry SOURCES.md --staged SOURCES.append.md \
  --map <lane>/.ufo/evidence/round-46/assimilation/adoption-map.json --json
exit=1
verdict=inadmissible  refused=true  map_ok=false  map_floor=S261
map_clash=["S259","S260"]
map_dedupe={S153:S105, S154:S106, S159:S155, S160:S156, S195:S258}
map_reasons=["map targets collide with registry ids: S259,S260"]
```

The map file is unchanged since the freeze (`git show 745a583…:` and `git show 6f2168e0…:` both hash `0e2236f5c1783fbbc89b6eb827d805ac2335b48f5439c26c41948f016b915841`; `guard-map.json` likewise `e32dc587…` at both revisions).

Reproduction of the freeze-time receipt (freeze registry + same map) is exact:

```
python3 -I tools/staged-id-guard.py --registry SOURCES.freeze.md --staged SOURCES.append.md \
  --map .../adoption-map.json --json      → exit=0, verdict=admitted, map_ok=true, map_floor=S258
json.load(freeze_rerun) == json.load(committed guard-map.json)  → True   (every field equal)
```

**Why the map is no longer evaluated as admissible — and what the exit 1 actually is.** `adoption-map.json` is a *pre-adoption* artifact: its job is to decide ids before anything is appended. Post-append, its three new-document targets are registry ids *by construction*, and `validate_map` (`tools/staged-id-guard.py:220-232`) then routes them through the dedupe rule — "a target that is a registry id is admissible only when the staged row's document is the document of that registry row". That rule exists for held documents, not for adoptions that just landed. Re-running the map at CONTENT therefore cannot reproduce `admitted`; only S195→S258 survives it as a dedupe.

**The two clashes are document-key artefacts, not id defects** — computed with the tool's own functions (`importlib` load of `tools/staged-id-guard.py`, scratch only):

```
registry S258 key = https://arxiv.org/abs/2504.16777                                   norm arxiv.org/abs/2504.16777
staged   S195 key = https://arxiv.org/abs/2504.16777                                   → equal  (dedupe)
registry S259 key = https://portal.fis.tum.de/en/publications/an-empirical-study-…-failures/
staged   S190 key = https://doi.org/10.1109/TSE.2026.3729363                           → NOT equal (same work, different document URL)
registry S260 key = https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json
staged   S216 key = https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json**   → NOT equal (markdown bold tail)
staged rows whose doc key ends with markup: ['S212','S216'];  registry: none
```

Counterfactual probe (scratch copy `SOURCES.append.probe.md`, only those two strings changed — S190's URL replaced by the portal URL, S216's trailing `**` dropped; no id touched):

```
python3 -I tools/staged-id-guard.py --registry SOURCES.md --staged SOURCES.append.probe.md \
  --map .../adoption-map.json --json   → exit=0
verdict=admitted  map_ok=true  map_clash=[]
map_dedupe={S153:S105, S154:S106, S159:S155, S160:S156, S190:S259, S195:S258, S216:S260}
```

So the whole CONTENT-time inadmissibility is the two document-key divergences; with them resolved the committed map validates against the post-adoption registry with all three adoptions as dedupes.

**Does this touch a claim or the deciding run?** No. At CONTENT, `adoption-map.json`/`guard-map.json` are read only by `contract.json`, `deciding-run.sh`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md`, `corpus/lessons/round-46.md` (`git grep -l`). In `deciding-run.sh` the map appears solely in the `FROZEN` hash list (`deciding-run.sh:22`, checked by step 0 `FROZEN_UNCHANGED`) — the script never re-runs the guard. Neither `.ufo/evidence/round-46/coverage/measure.py`, `calibration/measure.py` nor `hardening/mutate.py` mentions the guard or the map (`grep -nE 'adoption-map|guard-map|staged-id-guard'` → none; `coverage/measure.py` contains only literal id strings in its selftest fixtures, lines 198, 286, 298, 304).

# 5. Indented-row proof (`guard-proof-collisions`) reproduced in scratch

Scratch fixture `proof-registry.md` / `proof-staged.md` (registry S001/S002; staged carries `  | S002 |` with two leading spaces plus S003):

```
indent-pattern collisions: S002
col0-pattern collisions:
cmp guard-proof-collisions.final .../assimilation/guard-proof-collisions → IDENTICAL
```

The 0-3-space pattern catches the indented row; the column-0 pattern misses it — the committed receipt reproduces byte for byte.

Reality check on the two real files: the final registry has **no** indented row (`col0_count=120 == space03_count=120`, `comm -13` empty) and the package has none either (`staged_col0=103 == staged_space03=103`). No row indented 4+ spaces exists in the registry (`grep -cE '^ {4,}\|…'` → 0), and the only line that matches an id-in-a-pipe-cell pattern without starting with `|` is prose at `SOURCES.md:454` (the round-42 collision note). The indentation hazard is therefore demonstrated only by the fixture, as designed.

# 6. Id history (never-reuse)

- Freeze registry holds none of the three: `grep -cE '^ {0,3}\|[[:space:]]*S(258|259|260)[[:space:]]*\|' SOURCES.freeze.md` → `0`.
- CONTENT vs its parent `e630ae79…`: 120 ids vs 120 ids, `comm -23` empty, `comm -13` empty (the rows landed one commit earlier, `a6892b1`, which is an ancestor of CONTENT).
- `git log --all -S'S258' -- corpus/SOURCES.md` also hits `726ba86`, `9ef5d8a`, `c1e101d` (and `3bf8bcd`, which has 0 such rows, prose only). Those three are jj working-copy snapshots (empty subject, reachable through `refs/jj/keep/…`, **not** ancestors of CONTENT: `merge-base --is-ancestor 726ba86 <CONTENT>` → no). Their S258/S259/S260 rows are byte-identical to CONTENT's (`diff` over the three rows → IDENTICAL for all three), i.e. the same authoring content captured by jj before the git commit — not a different document previously holding these ids.

# Findings

**F1 — LOW (reproduced).** The committed `.ufo/evidence/round-46/assimilation/adoption-map.json` is inadmissible against the CONTENT registry: `staged-id-guard --map` exit 1, `verdict=inadmissible`, `map_clash=["S259","S260"]`, reason `map targets collide with registry ids: S259,S260`. Attacks the adoption-map receipt as a standalone artifact. Impact bounded: the map is a pre-adoption decision artifact, no claim counter and no step of `deciding-run.sh` re-validates it (only its bytes are pinned by `FROZEN_UNCHANGED`), so C1/C2/C3 and the deciding run are unaffected. Reader hazard: anyone re-running the guard with `--map` at CONTENT sees `inadmissible` and may read it as a C3 defect.

**F2 — LOW (reproduced, isolated).** The map's "by document" wording (and `contract.json` `id_map`) is guard-established for only 1 of 3 adoptions. `S195→S258` is a true document match; `S190→S259` maps a staged row whose document key is the DOI URL `https://doi.org/10.1109/TSE.2026.3729363` onto the registry row keyed by the TUM portal record URL (same work, different document URL → by-work, not by-document); `S216→S260` fails only because the staged URL is wrapped in markdown bold (`…?alt=json**`) and `normalise_document` strips scheme/`www.`/case/trailing slash but not emphasis. Counterfactual (`SOURCES.append.probe.md`) fixing just those two strings makes the same map `admitted` with `map_dedupe` covering all three. No id is wrong and no arithmetic renumber occurred.

**F3 — INFO.** The freeze verdict `admitted` never tested document identity for the three new-document targets: `validate_map` only compares documents when the target is already a registry id, so at the freeze registry it checked injectivity (`map_targets=11`), staged-disjointness (`map_staged_clash=[]`) and floor (`map_floor=S258`). "Adopted at guard-admitted ids S258/S259/S260" is accurate as an id statement; "by document" is not what the guard's `admitted` established for S190/S216.

**F4 — INFO.** Id hygiene at CONTENT is clean: 120 registry ids, 8 collisions byte-identical to the receipt, 0 duplicates in either file, each adopted id once, nothing removed, no id ≥ S261 burned, `next_free=safe_floor=S261` (above `staged_max=S255`, `cascade_count=0`), `registry_docs` 102 → 105.

**F5 — INFO.** The 0-3-space extractor and the guard's `ROW_RE` agree exactly on both files (120/120, 103/103); neither real file contains an indented row, so the committed indented-row proof is a fixture demonstration and reproduces byte-identically.

# Not run / limits

- No claim counter (`calibration/measure.py`, `hardening/mutate.py`, `coverage/measure.py`) was run by this seat — out of item scope, and the deciding run is the L1's. Nothing here is a verdict on C1/C2/C3.
- The staged package was not fetched or re-derived; it was copied byte-for-byte from the read-only package and pinned by sha256 (`020fbeaa…`), matching the guard's `staged_sha256`.
- The `--map` result at CONTENT is reported as observed (exit 1). I did not attempt to make the committed map pass by editing anything in the lane; the only mutation is the scratch probe copy used in F2.
- No tool installed or upgraded this seat (nothing needed; `python3` 3.14 + coreutils sufficed).
- Evidence files retained in `/tmp/tameshi-r46-T46ExecIds/`: `SOURCES.md`, `SOURCES.freeze.md`, `SOURCES.parent.md`, `SOURCES.append.md`, `SOURCES.append.probe.md`, `reg-ids.final`, `staged-ids.final`, `collisions.final`, `dupes-reg.final`, `dupes-staged.final`, `reg-ids.freeze`, `reg-ids.parent`, `reg-ids.col0.final`, `staged.col0`, `guard-final.json`, `guard-final-map.json`, `guard-freeze.json`, `guard-freeze-map.json`, `guard-final-map-probe.json`, `guard-proof-collisions.final`, `proof-registry.md`, `proof-staged.md`.
