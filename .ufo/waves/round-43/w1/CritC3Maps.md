# CritC3Maps — adversarial adoption maps against tools/staged-id-guard.py

Seat: L1Tameshi43.CritC3Maps (critic). Axis judged: operability. Milestone: adversarial
adoption maps. Read-only on the lane; scratch under `/tmp/tameshi-r43-CritC3Maps/` (deleted
after this report). No tool installed or upgraded.

Deciding clause for every judgement (fleet `/home/vgpnk/Projects/shokunin/CORPUS.md`,
SOURCES.md › Shape, line 89):

> `id` — `S` + 3 or more digits, the next unused; never reused. No `|` inside any cell.

Secondary clauses: CORPUS.md:116-117 ("**Append-only.** … A correction is a new row whose
`teaches` opens `supersedes S0NN —`") and CORPUS.md:142 (duplicate ids "must print nothing").

## 0. Substrate: the guard moved three times during this seat

| rev | what | tool sha256 | C3 counter sha256 | contract tool pin |
|---|---|---|---|---|
| `17f6ef0` (assignment's freeze) | freeze A2/A3 | `8140945a…f97b762` | `6278edcd…8d78601` | `8140945a…` |
| `5cd2154` | A4/A5 — guard shape repair, C1 kill oracle | `efa5f129…290f9b3c` | `fbc8ad3c…770c51e` | `efa5f129…` |
| `53cb32b` (HEAD when this report was written) | A6/A7/A8 — C2 extractors, guard document identity + held enforcement, contract narration | `365bf958…4b0c2` | `8c8147e7…93ff9b` | `365bf958…` |

Measured, not inferred:

```
$ git cat-file blob 17f6ef0:tools/staged-id-guard.py | sha256sum
8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762  -
$ git cat-file blob 5cd2154:tools/staged-id-guard.py | sha256sum   # (measured as working tree then)
efa5f129cba312c26c1fc453e6cd7f783efafeecccfac791e8c03d3d290f9b3c
$ git cat-file blob  53cb32b:tools/staged-id-guard.py | sha256sum
365bf95842ce9bb022af7edb5905f1d36e1a435a7365ff91469d2edcadb4b0c2  -
$ git cat-file blob  53cb32b:.ufo/evidence/round-43/guard/measure.py | sha256sum
8c8147e75a742dc1ad4da3c4354a9c8fc63e3a669d5f85dbf90c925d9893ff9b   # == contract pin at 53cb32b
```

Consequences for the round declaration, stated plainly:

1. The freeze rev in this seat's assignment (`17f6ef0`) no longer describes the tool under
   test: A4 repaired the map-shape check *after wave-1 seats began* (its own `when`:
   "during wave 1, before any deciding run"), A7 added document normalisation and held-document
   enforcement, A8 corrected the narration. With the current counter and `--freeze 17f6ef0`,
   `self_pin` compares the contract's `6278edcd…` against the running `8c8147e7…` → 0, so C3
   fails before any map is judged. C3 can only pass if the freeze is re-declared at
   `53cb32b`, where tool pin, counter pin and blobs agree. [INFERENCE from
   `guard/measure.py:128-146`; I did not run the counter at a rev outside my allowance.]
2. The earlier contract's `amendments_note` ("counters … byte-unchanged") was contradicted by
   A4/A5; A8 has since replaced it with a note that admits A4-A7 "change two counters, the
   guard tool and their pins, all before any deciding run". That disclosure is honest, but it
   means the round's C3 is a claim about repaired bytes, not about the bytes frozen at
   `17f6ef0`. The round must say which rev the deciding run uses.

Every map below was run with the exact command shape assigned:

```
python3 -I <tool> --registry <SOURCES.md> --staged <SOURCES.append.md> --map <map> --json
```

against the freeze registry (`git show 17f6ef0:corpus/SOURCES.md`, 113 rows, max S158, safe
floor S256, collisions S153–S158) and a staged copy whose sha256 equals the shokuknow original
(`020fbeaa…c807`, 103 rows S153–S255). Live-registry variants are marked **live** (the round-43
lane seat appended S159 → 7 collisions, held S153→S105, S154→S106, S159→S155).

## 1. The five assigned maps (exact `{"map": …}`)

1. `m1_registry_id_other_doc` — registry id reused for a different document: `S155→S107`
   (staged S155 `arxiv.org/abs/2302.09330`; registry S107 `raw.githubusercontent.com/tensorflow/
   federated/…`), plus `S153→S256 S154→S257 S156→S258 S157→S259 S158→S260`.
2. `m2_self_map` — one collision left on itself: `S153→S153`, plus `S154→S256 … S158→S260`.
3. `m3_wholeset` — all 103 staged rows covered, targets inside the staged range:
   `m3a` = cycle `S153→S154 … S255→S153`; `m3b` = shift `S153→S159 … S255→S261`. m3a is the
   only injective all-inside shape that exists: 103 rows against 97 non-registry ids in
   S153–S255, so any bijection inside the range must land on the six registry ids.
4. `m4_duplicate_targets` — `S155→S260, S156→S260`, plus `S153→S256 …`.
5. `m5_below_floor_gap_id` — `S155→S038` (S038 is a registry **gap**: in neither file), plus
   `S256…`; control `m5b` uses gap `S098`.

Additional maps that decide the same claim: `m6` partial target inside the staged range
(`S155→S200`); `m7` held documents re-appended under fresh ids (`S153→S256, S154→S257, …`);
`m3c` whole-set with held rows kept on their registry ids and the other 101 rows inside the
staged range (97 targets S159–S255 + S256–S259); controls `c0` (`S153→S105, S154→S106,
S155→S256 …`), `c1` (whole-set, all targets S256–S358), `c1b` (whole-set, held rows deduped,
rest S256–S356), `c2` (live by-document, 7 entries).

## 2. Results — verdict and reasons, verbatim

### 2.1 Frozen bytes `8140945a` (the tool at the assignment's freeze)

| map | verdict | reasons |
|---|---|---|
| m1 | inadmissible | `['map has a target that is not an S-id', 'map targets collide with registry ids: S107']` |
| m2 | inadmissible | `['…not an S-id', '…collide with registry ids: S153', 'map leaves a colliding id on itself: S153']` |
| m3a | inadmissible | `['…not an S-id', '…collide with registry ids: S153,S154,S155,S156,S157,S158']` |
| m3b | inadmissible | `['map has a target that is not an S-id']` — **only** reason; `map_clash=[] map_staged_clash=[] map_below_floor=[] map_uncovered=[]` |
| m4 | inadmissible | `['map is not injective (two staged rows share a target)', '…not an S-id']` |
| m5 | inadmissible | `['…not an S-id', 'partial map targets are below the safe floor S256: S038']` |
| m6 | inadmissible | `['…not an S-id', 'map targets are still staged ids: S200']` |
| m7 | inadmissible | `['map has a target that is not an S-id']` only (`map_dedupe={}`) |
| c0 | inadmissible | `['map has a target that is not an S-id']` only, `map_dedupe={'S153':'S105','S154':'S106'}` |
| c1 | inadmissible | `['…not an S-id']` only |
| c2 (live) | inadmissible | `['…not an S-id']` only |

`verdict="admitted"` is **unreachable** for any real map at this rev: the false reason fires on
every map with two or more entries.

### 2.2 Repaired bytes `efa5f129` (A4/A5)

m1, m2, m3a, m4, m5, m6 → inadmissible with only their true reasons. c0 → **admitted**
(`map_dedupe={'S153':'S105','S154':'S106'}`, exit 0); c1 → admitted; c2 (live) → **admitted**
(`map_dedupe={'S153':'S105','S154':'S106','S159':'S155'}`); **m3b → admitted**; **m7 →
admitted** (`map_dedupe={}`); m3b (live registry) → inadmissible
`['map targets collide with registry ids: S159']`.

### 2.3 Current bytes `365bf958` (A6/A7/A8), freeze registry

| map | verdict | reasons |
|---|---|---|
| m1 | inadmissible | `['map targets collide with registry ids: S107', 'map moves a held document off its registry id: S153 -> S256 (registry S105)', '… S154 -> S257 (registry S106)']` |
| m2 | inadmissible | `['map targets collide with registry ids: S153', 'map leaves a colliding id on itself: S153', '…held document off its registry id: S153 -> S153 (registry S105)', '… S154 -> S256 (registry S106)']` |
| m3a | inadmissible | `['map targets collide with registry ids: S153,S154,S155,S156,S157,S158', '…held … S153 -> S154 (registry S105)', '… S154 -> S155 (registry S106)']` |
| m3b | inadmissible | `['map moves a held document off its registry id: S153 -> S159 (registry S105)', '… S154 -> S160 (registry S106)']` — refusal is for the held rows, **not** the floor |
| m4 | inadmissible | `['map is not injective (two staged rows share a target)', '…held … S153 -> S256 (registry S105)', '… S154 -> S257 (registry S106)']` |
| m5 | inadmissible | `['partial map targets are below the safe floor S256: S038', '…held … S153 -> S256 …', '… S154 -> S257 …']` |
| m6 | inadmissible | `['map targets are still staged ids: S200', '…held … S153 -> S256 …', '… S154 -> S257 …']` |
| m7 | inadmissible | `['map moves a held document off its registry id: S153 -> S256 (registry S105)', '… S154 -> S257 (registry S106)']` |
| c0 | **admitted** | `[]`, `map_dedupe={'S153':'S105','S154':'S106'}`, exit 0 |
| c1 | inadmissible | `['…held … S153 -> S256 (registry S105)', '… S154 -> S257 (registry S106)']` |
| c2 (live) | **admitted** | `[]`, `map_dedupe={'S153':'S105','S154':'S106','S159':'S155'}` |
| **m3c** | **admitted** | `[]`, `map_dedupe={'S153':'S105','S154':'S106'}`, `map_below_floor=[]` — yet **97 of 103 targets (S159–S255) are below the safe floor S256** |
| c1b | **admitted** | `[]`, `map_dedupe` as c0 (held rows kept, rest S256–S356) |
| m3c (live) | inadmissible | `['map targets collide with registry ids: S159', 'map moves a held document off its registry id: S159 -> S163 (registry S155)']` |

The extra "held document" reasons on m1/m2/m4/m5/m6 are correct consequences of my maps: they
leave the held rows S153/S154 (documents already at S105/S106) on fresh ids. That does not
change the refusal these maps were built to test, and A7 is right to add it.

## 3. Judgements — CORRECT refusal, or false refusal

### 3.1 m1 — registry id reused for a different document → **CORRECT**
CORPUS.md:89 "never reused": S107 already keys a registry row; adopting the arXiv row under it
puts two documents on one id (and S107 is not "the next unused"). The frozen tool's
`'map has a target that is not an S-id'` co-reason is false — S107 and S256–S260 are well-formed
— so the receipt misdescribed its own decision, but the decision was right.

### 3.2 m2 — one collision left on itself → **CORRECT**
CORPUS.md:89 "never reused": S153 is a live registry id. The tool's own `held` field gives the
only admissible move — `S153→S105`, because the staged S153 document
(`pubs.opengroup.org/…/9699919799/utilities/diff.html`) is exactly registry S105's document.

### 3.3 m3 — whole-set maps with targets inside the staged range
- **m3a** (cycle inside S153–S255) → **CORRECT**. Six targets are registry ids held by other
  documents (S153 python/ast, S154 pathlib, S155 pitest basic_concepts, S156 pitest faq,
  S157 argparse, S158 pitest DetectionStatus) → "never reused". It is the only injective
  all-inside shape, so refusal is the only right verdict.
- **m3b** (shift, targets S159–S261) → frozen: **FALSE REFUSAL**; the sole reason names a
  target class that does not occur, and every semantic array is empty. Under CORPUS.md:89 the
  map is legal: S159–S261 are unused in the registry, unique after the whole-set remap, and
  S159 *is* "the next unused". At A4 the same map is admitted (consistent with CORPUS); at A7
  it is refused only because my map moves the held rows S153/S154 onto S159/S160 — a correct
  refusal for the map as written, not a decision about the floor.
- **m3c** decides the floor question cleanly (held rows kept on S105/S106): current bytes
  **admit** it with 97 targets below the safe floor. That is a **false admission against C3's
  own words** ("admits only … ids at or above the safe floor") and against the tool
  docstring's "never an id another staged row still holds", because the whole-set branch still
  skips both tests (`if target in staged and not whole_set`, line 226; `if not whole_set and
  id_number(target) < …`, line 229). It is not a CORPUS breach — the target ids are unused and
  unique — so what is false is the claim, not the corpus. It is also timing-dependent: the same
  map is inadmissible after the lane's own S159 append.

### 3.4 m4 — duplicate targets → **CORRECT**
Two staged rows on S260 mint one id twice, so the appended registry fails the CORPUS.md:142
duplicate-id sweep and re-uses an id within a single append (CORPUS.md:89).

### 3.5 m5 — target below the safe floor (S038) → **CORRECT**
S038 is a gap, so "never reused" does not bite; the deciding limb is "**the next unused**".
Local evidence for that reading: the registry's 45 gaps (S038, S039, S098, S109–S130,
S133–S151) are never backfilled while later ids exist, and the lane's own round-43 note
declares "Next unused id: S160". Refusal is the contract-aligned reading; the tool cannot
distinguish a never-used gap from a released id, but the corpus is append-only, so gaps are
unused.

### 3.6 m6 — partial map target inside the staged range → **CORRECT (conservative)**
A partial map leaves the unmapped staged rows holding their ids, so S200 is still in use by the
package being renumbered; adopting it either duplicates it inside the package or re-uses it if
the package is appended whole.

### 3.7 What the held rule fixed, and what is still open
`m7` (held document re-appended under a fresh id) was **admitted** at A4 with `map_dedupe={}` —
a false admission against the tool's own held rule and CORPUS.md:116-117 (a second row for a
carried document is legitimate only as a correction whose `teaches` opens `supersedes S0NN —`).
A7 now refuses it (`map moves a held document off its registry id`), so that hole is closed and
`c0`/`c1b`/`c2` dedupe exactly. **Still open**: the whole-set floor carve-out, demonstrated by
`m3c` (§3.3).

## 4. Root cause of the frozen false refusal (already repaired at A4)

Frozen `tools/staged-id-guard.py:172`:

```python
if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):
    reasons.append('map has a target that is not an S-id')
```

The pattern is matched against the concatenation of every target (`"S256S257"`), which can never
match a single-id pattern, so every map with two or more entries was refused. The freeze's
selftest had 13 cases and its only admitted case used one entry (`{'S002':'S010'}`), so it
stayed green. Minimal isolation (synthetic registry S001–S003, staged S002,S004):

```
{"S002":"S010"}                  -> admitted,     exit 0
{"S002":"S010","S004":"S011"}    -> inadmissible, exit 1,
   reasons ['map has a target that is not an S-id'],
   map_clash=[] map_staged_clash=[] map_below_floor=[] map_uncovered=[] map_dedupe={}
```

Current bytes: each map key and target is validated per entry under `SID_RE` and a non-S-id is
a setup refusal, not a map reason (`tools/staged-id-guard.py:123,201-207`); selftest is
`cases=23 failed=0`.

## 5. Impacted axes

- **operability (C3)** — decisive. At the assignment's freeze the claim's `safe_map_admitted=1`
  cannot be reached; at the repaired bytes it is reached for a by-document map (`c0`, `c2`
  admitted, dedupe exact) but the same bytes admit `m3c`, which contradicts the claim's "at or
  above the safe floor". The frozen rev also no longer matches the tool/counter pins, so C3 can
  only pass with the freeze re-declared at `53cb32b`.
- **depth (C1)** and **calibration (C2)** — no impact from these maps; A5/A6 changed the C1/C2
  counters, which is outside this seat's item.

## 6. Smallest safe correction

1. **Guard floor rule (open)**: drop the two whole-set carve-outs (`and not whole_set` at
   `tools/staged-id-guard.py:226,229`) so every target must be unused by both files and at or
   above the safe floor. Then `m3c`/`m3b` are refused for a true reason and admission is exactly
   "held rows dedupe to their registry id, every other target is a fresh id at or above the
   floor", which is what C3 states. Cost, stated openly: a compact whole-set renumber starting
   at S159 becomes refused; the lane's 45-id gap history already tolerates that gap.
   Alternative, not available under the frozen contract: narrow the claim's sentence. If the
   round keeps the carve-out, the claim must be re-declared, because as written it is false.
2. **Selftest**: add `m3c` as a case (whole-set, held rows deduped, targets inside the staged
   range must be refused) and the `m7` case A7 introduced; both holes were invisible to a green
   suite.
3. **Round declaration**: re-declare the C3 freeze at `53cb32b` (tool `365bf958`, counter
   `8c8147e7`, pins aligned) or re-freeze; state that A4-A7 repaired the tool and counters after
   wave-1 seats began, which the round's `frozen_before` sentence currently predates.

## 7. Receipts (all under /tmp, now deleted)

```
python3 -I <tool> --registry <reg> --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --map <map> --json
  baseline (before the lane's S159 append): collisions S153..S158, registry_rows 113,
    registry_max S158, staged_rows 103 (S153..S255), safe_floor S256,
    held {S153:S105, S154:S106}, cascade 6, verdict refused
  live baseline (after S159): collisions 7 (…S159), held + S159:S155, floor still S256
frozen selftest: cases=13 failed=0      current selftest: cases=23 failed=0
m3c (freeze registry, current tool): verdict=admitted ok=True reasons=[] dedupe={S153:S105,S154:S106}
    entries 103, 97 distinct targets below the safe floor
m3c (live registry, current tool): inadmissible ['…collide with registry ids: S159', '…held … S159 -> S163 (registry S155)']
```

No file outside `/tmp/tameshi-r43-CritC3Maps/` and this report was written; no git/jj command
beyond read-only `show`/`cat-file`/`diff`/`log`/`status`.
