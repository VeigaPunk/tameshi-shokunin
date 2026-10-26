seat: T47ExecIdGuard
item: prompt section 10 id-collision check + `tools/staged-id-guard.py`, in scratch; staged-id guard and renumber map
rev: 9acfbe21435e1976636a276448dee1d5e7155915
base: 0b5b7cd2b2c15d23086e811a0f0348d84261277b
contract: `.ufo/evidence/round-47/contract.json` (read, never edited)
lane: /home/vgpnk/Projects/shokunin/tameshi-shokunin
package (read-only): /home/vgpnk/Projects/shokuknow
scratch root: /tmp/tameshi-r47-T47ExecIdGuard/assimilation
no verdict: this seat ran the guard as a probe and `--selftest` only; the deciding run belongs to the L1

## 1. Extractor commands and the two id lists

Run verbatim as assigned (absolute paths; scratch under /tmp):

```
S=/home/vgpnk/Projects/shokuknow; A=/tmp/tameshi-r47-T47ExecIdGuard/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > $A/reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/merge/tameshi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > $A/staged-ids
comm -12 $A/reg-ids $A/staged-ids > $A/collisions
```

Counts and identity:

| list | lines | ranges | sha256 |
|---|---|---|---|
| `reg-ids` (lane `corpus/SOURCES.md`, 0-3-space census-valid extractor) | **120** | S001–S037, S040–S097, S099–S108, S132, S152–S160, S256–S260 | `3a743db1ec852bfbd80b58887f9811b07316f1aa9a995ef3edcc9ed9b4e21347` |
| `staged-ids` (`merge/tameshi/SOURCES.append.md`) | **103** | S153–S255 (contiguous) | `31b1be336c7b8b240763e3db560f22b8d9fa06b91f7e5c4fa08d785617d58f9d` |
| `collisions` (comm -12) | **8** | S153–S160 | `bb1ccda6d98b4522a27fc9216d7afd74aef87d931870f421550b772ad25b013d` |

Full registry list (120): S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018 S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036 S037 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063 S064 S065 S066 S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080 S081 S082 S083 S084 S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S099 S100 S101 S102 S103 S104 S105 S106 S107 S108 S132 S152 S153 S154 S155 S156 S157 S158 S159 S160 S256 S257 S258 S259 S260

Full staged list (103): S153 S154 S155 S156 S157 S158 S159 S160 S161 S162 S163 S164 S165 S166 S167 S168 S169 S170 S171 S172 S173 S174 S175 S176 S177 S178 S179 S180 S181 S182 S183 S184 S185 S186 S187 S188 S189 S190 S191 S192 S193 S194 S195 S196 S197 S198 S199 S200 S201 S202 S203 S204 S205 S206 S207 S208 S209 S210 S211 S212 S213 S214 S215 S216 S217 S218 S219 S220 S221 S222 S223 S224 S225 S226 S227 S228 S229 S230 S231 S232 S233 S234 S235 S236 S237 S238 S239 S240 S241 S242 S243 S244 S245 S246 S247 S248 S249 S250 S251 S252 S253 S254 S255

Independent structural checks (read-only): no duplicate id in either list; the lane registry's id space is S001–S260 with **140 gaps**, S161–S199 and S200–S255 absent (so the package's S161–S255 stay reserved by document, as the registry's own round-45 note says).

## 2. Collisions

```
S153
S154
S155
S156
S157
S158
S159
S160
```

The collision is **id-only**: the same eight ids name different documents on the two sides. Documents the lane already holds (guard `held`, form-insensitive):

| staged id | staged document | held as lane row | lane row's document |
|---|---|---|---|
| S153 | POSIX `diff` spec, pubs.opengroup.org/…/diff.html | **S105** | POSIX `diff` utility specification |
| S154 | google/golden `golden.go` | **S106** | Package golden … google/golden |
| S159 | PIT `quickstart/basic_concepts/` | **S155** | `\| S155 \| Basic concepts (PIT docs) — https://pitest.org/quickstart/basic_concepts/ \|` |
| S160 | PIT `faq/` | **S156** | FAQ (PIT docs) — https://pitest.org/faq/ |

The collision that forces the re-point: staged **S155 is arXiv 2302.09330**, while the lane's **S155 is PIT basic concepts**. Neither the staged id nor the lane id can be reused for the other document.

## 3. The guard's verdict line

```
python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py \
  --registry /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md \
  --staged   /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md
```

```
STAGED_ID_GUARD: collisions=8 unmapped=0 held=4 cascade=0 next_free=S261 verdict=answered
  collision S153 naive->S261
  collision S154 naive->S262
  collision S155 naive->S263
  collision S156 naive->S264
  collision S157 naive->S265
  collision S158 naive->S266
  collision S159 naive->S267
  collision S160 naive->S268
```

exit 0. `--json` fields of record: `extractor="0-3space"`, `column0_miss=[]`,
`registry_rows=120`, `staged_rows=103`, `registry_docs=105`, `registry_max=S260`,
`staged_max=S255`, `safe_floor=S261`, `refused=false`, `cascade=[]`,
`registry_sha256=e44dcb0db374dcc41d50453cedc8ad6542a1904eb7f1ed1db9e936417bcf49e9`,
`staged_sha256=020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807`.

`--selftest`: `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` / `VERDICT: PASS`, exit 0.
`--help`: exit 0 (usage line: `--registry`, `--staged`, `--map`, `--json`, `--selftest`).

## 4. Renumber map — by document, never by arithmetic

Adoption ids are the contract's (frozen): staged S155→**S261**, S158→**S262**, S206→**S263**, S207→**S264**.

| staged id | document (evidence) | disposition | lane id |
|---|---|---|---|
| S155 | `https://arxiv.org/abs/2302.09330` (Gruber/Heine/Oster/Philippsen/Fraser) | **adopt** (row + cited entry) | **S261** |
| S158 | `https://mir.cs.illinois.edu/marinov/publications/LamETAL20ManyFlakyTestsAreNDOD.pdf` (Lam et al. camera-ready) | **adopt** (row; uncounted fourth row per contract `extra_row`) | **S262** |
| S206 | `https://arxiv.org/abs/2607.09345` (Baltes/McKim/Zaidman/Wagner) | **adopt** (row + cited entry) | **S263** |
| S207 | `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/ICST60714.2024.00037?fields=…` (Leinen et al., ICST 2024) | **adopt** (row + cited entry) | **S264** |
| S153 | POSIX `diff` spec | dedupe, do not append | S105 |
| S154 | google/golden `golden.go` | dedupe, do not append | S106 |
| S159 | PIT basic concepts | dedupe, do not append | S155 |
| S160 | PIT FAQ | dedupe, do not append | S156 |
| S156 | `https://arxiv.org/abs/2406.09843` (LLM mutation testing) | not adopted this round | — |
| S157 | `https://doi.org/10.21105/joss.01891` (Hypothesis, JOSS) | not adopted this round | — |
| S205 | `https://arxiv.org/abs/1810.05286` (Predictive Test Selection) | not adopted; **still cited at `r8-flakiness-not-static.md:22` and `r8-flaky-cost-baseline.md:36`** | **none — lane has no S205 row** |
| S208 | tameshi's own env-diff receipts (`lanes/tameshi/round8/evidence/…`) | not adopted; **still cited at `r8-flakiness-not-static.md:34`** | **none — lane has no S208 row** |
| S001, S152 | already lane ids used by the entries (`held S001`, `S152` receipt) | unchanged | S001, S152 |

The naive arithmetic alternative the guard prints is *wrong by document* in every row: `S155 naive->S263` lands arXiv 2302.09330 on the id the contract gives arXiv 2607.09345, and `S158 naive->S266` lands the Lam PDF on an id nothing adopts. That is the arithmetic-vs-document gap the map closes.

What the adopting edit must leave behind in the three package entries (package ids are the left column; `source:` line numbers are the package copy's):

| package entry | must become |
|---|---|
| `flaky-aware-verdict-evidence.md` | `source: S155 —` (line 2) → `S261`; `source: S158 —` (line 3) → `S262`; `source: S160 —` (line 4) → `S156`; body refs: S155 at lines 19/42/45/60 → S261, S158 at 13/34/39/60/64 → S262, S160 at 26/46 → S156 |
| `r8-flakiness-not-static.md` | `source: S206 —` (line 2) → `S263`; line 22 `S205` and line 34 `S208` **must not survive** (no lane row exists) |
| `r8-flaky-cost-baseline.md` | `source: S207 —` (line 2) → `S264`; line 36 `S205` **must not survive** |

Counted occurrences: `flaky-aware-verdict-evidence.md` S155×5, S158×6, S160×3, S001×1; `r8-flakiness-not-static.md` S152×1, S205×1, S206×1, S208×1; `r8-flaky-cost-baseline.md` S205×1, S207×1. The round-47 package copies in `.ufo/evidence/round-47/assimilation/package/` are byte-identical to the read-only package (`3a962fe5…`, `4fab9714…`, `9f778247…`).

## 5. S261–S264 unused — and the one place they are not

| check | result |
|---|---|
| row ids `^ {0,3}\|\s*S26[1-4]\s*\|` in `corpus/SOURCES.md` | **0** (grep -c → 0, exit 1) |
| `^source:` lines naming S261–S264 across the package's 85 knowledge files (81 `knowledge/corpus/knowledge` + 4 `amendments/corpus/knowledge`), 106 `source:` lines total | **0** |
| any occurrence of S261–S264 in those 85 files | **0 files** |
| any occurrence in the three round-47 package copies | **0 files** |
| any occurrence anywhere under `merge/tameshi` | **0** |

**Conflict to record, not to fix here.** The lane registry's own prose names S261–S264 twice, as a round-46 reservation with a *different* document assignment:

- `corpus/SOURCES.md:471` — “the guard map `.ufo/evidence/round-46/assimilation/adoption-map.json` is admitted (`guard-map.json`) and also moves staged S155–S158 to S261–S264 in the map only, so those four ids are reserved by the map and unused in the registry.”
- `corpus/SOURCES.md:474` — “- Next unused id: S265 (S261–S264 are map-only reserved; staged ids S161–S255 stay reserved by document for the package).”

Round-46's admitted map (`.ufo/evidence/round-46/assimilation/adoption-map.json`) is `S155→S261, S156→S262, S157→S263, S158→S264`. The frozen round-47 contract is `S155→S261, S158→S262, S206→S263, S207→S264`. So:

| id | round-46 map (map-only, no row landed) | round-47 contract | status |
|---|---|---|---|
| S261 | S155 (arXiv 2302.09330) | S155 (same document) | **agrees** |
| S262 | S156 (arXiv 2406.09843) | S158 (Lam camera-ready) | **reassigned** |
| S263 | S157 (JOSS Hypothesis) | S206 (arXiv 2607.09345) | **reassigned** |
| S264 | S158 (Lam camera-ready) | S207 (S2 ICST24 record) | **reassigned** |

No *landed* row is contradicted (round 46 appended none of the four; row ids stop at S260), so the guard admits the round-47 map on row ids alone — the guard does not read prose. But if the round-47 rows land without amending lines 471/474, the registry states two documents for S262–S264. Resolution is the L1's: either land the contract map and record the supersession in the round-47 registry note, or re-open the contract's id assignment. This seat does not decide it.

## 6. Map admissibility (guard `--map`)

**(a) The four-entry contract map alone is refused** (`adoption-map-four.json`: `{"S155":"S261","S158":"S262","S206":"S263","S207":"S264"}`):

```
verdict = "inadmissible"
refused = true
map_ok = false
map_reasons = ["map does not cover every collision: S153,S154,S156,S157,S159,S160"]
map_uncovered = ["S153", "S154", "S156", "S157", "S159", "S160"]
map_entries = 4
```

exit **1**. A partial map cannot be admitted: the guard requires every collision decided.

**(b) The collision-complete map is admitted** (`adoption-map-r47.json` — the four adoptions, the four held dedupes, and map-only targets for the two unadopted collisions S156/S157):

```
{"map": {"S153":"S105","S154":"S106","S159":"S155","S160":"S156",
         "S155":"S261","S158":"S262","S156":"S265","S157":"S266",
         "S206":"S263","S207":"S264"}}
```

```
verdict = "admitted"
refused = false
analysis_refused = false
map_ok = true
map_reasons = []
map_dedupe = {"S153":"S105","S154":"S106","S159":"S155","S160":"S156"}
map_entries = 10
map_targets = 10
map_floor = "S261"
map_uncovered = []
map_staged_clash = []
map_clash = []
map_below_floor = []
```

exit **0**. `S265`/`S266` are map-only riders (round-46's precedent) so the collision set stays covered without adopting S156/S157; `S261`–`S264` are exactly the contract's four. If the L1 prefers no map-only riders, the four-entry map cannot pass and the two rows must be adopted or the map rule relaxed — that is a contract-level choice, flagged not taken.

## 7. Proof the guard can fail

Scratch registry with the indented row the item specifies, and a staged set that collides with it:

```
/tmp/tameshi-r47-T47ExecIdGuard/failreg.md
  | S002 | Gamma docs — https://example.test/gamma | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |
/tmp/tameshi-r47-T47ExecIdGuard/failstaged.md
  | S002 | Delta docs — https://example.test/delta | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |
```

The item's own extractor (0-3 spaces) vs the column-zero extractor on the same bytes:

```
0-3space on registry: S001 S002 S003
column0 on registry:  S001 S003
scratch collisions: S002      (comm -12, 1 line — nonempty)
```

Guard on the scratch pair:

```
STAGED_ID_GUARD: collisions=1 unmapped=0 held=0 cascade=1 next_free=S004 verdict=refused
  collision S002 naive->S004
```

exit **1**; `--json`: `collision_count=1`, `collisions=["S002"]`, `refused=true`,
`cascade=["S004"]` (the naive arithmetic target is itself a staged id).

Second can-fail on real bytes — the lane registry with one indented row `  | S205 |` appended in scratch (S205 is one of the 140 absent lane ids), staged carrying S205:

```
verdict = "answered"
collision_count = 1
collisions = ["S205"]
registry_rows = 121
extractor = "0-3space"
column0 registry S205 count: 0      (grep -cE '^\|\s*S205\s*\|', exit 1)
0-3space registry S205 count: 1     (grep -cE '^ {0,3}\|\s*S205\s*\|', exit 0)
```

exit **0** (`answered`, no refusal).

Observation on the guard's own diagnostic: `column0_miss` is computed from the **staged** text only (`analyse`: `column0 = {… for line in staged_text.splitlines()}`), so it reports an indented *staged* row (its T1 selftest: `column0_miss == ['S002']`) but is silent when the **registry** row is indented — the run above yields `column0_miss = []` although the column-zero registry extractor misses the very collision the guard found. Detection is correct either way (`ROW_RE` is 0-3-space on both files); only the "indented-row proof" field is one-sided. Recorded, not edited: `tools/` is outside this seat's write scope.

## 8. Exit-code ledger

| command | exit |
|---|---|
| `grep … > reg-ids` / `> staged-ids` / `comm -12 > collisions` | 0 / 0 / 0 |
| `staged-id-guard.py --help` | 0 |
| `staged-id-guard.py --selftest` | 0 (`cases=24 failed=0`, `VERDICT: PASS`) |
| `staged-id-guard.py --registry … --staged …` (plain) | 0 (`verdict=answered`) |
| `… --json` | 0 |
| `… --map adoption-map-four.json --json` | **1** (`inadmissible`) |
| `… --map adoption-map-r47.json --json` | 0 (`admitted`) |
| `… --registry failreg.md --staged failstaged.md` (specified indented proof) | **1** (`refused`, collisions=1) |
| `… --registry failreg.md --staged failstaged.md --json` | **1** |
| `… --registry failreg-real.md --staged failstaged-real.md --json` | 0 (`answered`, collisions=1) |
| `grep -cE '^ {0,3}\|\s*S26[1-4]\s*\|' corpus/SOURCES.md` | **1** (0 matches) |

All scratch artefacts: `/tmp/tameshi-r47-T47ExecIdGuard/assimilation/{reg-ids,staged-ids,collisions,guard-plain.txt,guard.json,guard-selftest.txt,adoption-map-four.json,adoption-map-r47.json,guard-four.json,guard-r47.json,guard-fail.json,guard-fail-real.json,failreg.md,failstaged.md,failreg-real.md,failstaged-real.md}` and `/tmp/tameshi-r47-T47ExecIdGuard/{failreg.md,failstaged.md}`. Lane writes: this file and the report only.

## 9. What the L1 must decide (flagged, not decided)

1. **Prose supersession.** Land the contract map (S262→S158, S263→S206, S264→S207) and record in the round-47 registry note that it supersedes the round-46 map-only reservation of S155–S158; otherwise `SOURCES.md:471,474` states the older assignment.
2. **Map completeness.** The guard needs a collision-complete map for a `--map` receipt. Adopt `adoption-map-r47.json` (10 entries, admitted) or accept that only the four-entry adoption is being landed *without* a `--map` receipt (the no-map run is `answered`, exit 0, which is not an adoption map).
3. **Dangling package ids in the adopted entries.** S205 and S208 are cited by two of the three entries and have no lane row (S161–S255 are all absent from the registry). Either those sentences are re-grounded to lane-held evidence, or the citation is dropped, or two more documents are adopted — the last is outside the frozen C3 scope.
4. **`source: S160` inside `flaky-aware-verdict-evidence.md`** must become `S156` (the lane's PIT FAQ row), not `S263`-style arithmetic; the guard's `held` already says `staged:S160 → S156`.
