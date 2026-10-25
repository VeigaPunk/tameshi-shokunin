# CritC3Maps — adversarial adoption maps against tools/staged-id-guard.py

Seat: L1Tameshi43.CritC3Maps (critic). Axis judged: operability. Milestone: adversarial
adoption maps. Read-only on the lane; scratch under `/tmp/tameshi-r43-CritC3Maps/`
(deleted after this report). No tools installed or upgraded.

Deciding clause used for every judgement (fleet `/home/vgpnk/Projects/shokunin/CORPUS.md`,
SOURCES.md › Shape, line 89):

> `id` — `S` + 3 or more digits, the next unused; never reused. No `|` inside any cell.

Secondary clause (CORPUS.md:116-117): "**Append-only.** … A correction is a new row whose
`teaches` opens `supersedes S0NN —`", and the census' duplicate-id sweep (CORPUS.md:142,
"duplicate ids — must print nothing").

## 0. Substrate moved under this seat — the two tool versions

The lane HEAD advanced from `17f6ef0` to `5cd2154` while this seat was measuring, and
`5cd2154` ("freeze A4/A5 — guard map-shape repair (wave-1 finding)") changed the tool and
both counter pins:

| substrate | tool blob sha256 | C3 counter sha256 | contract pin |
|---|---|---|---|
| `17f6ef0` (assignment's freeze) | `8140945a…f97b762` | `6278edcd…8d78601` | `8140945a…` |
| `5cd2154` (current HEAD) | `efa5f129…290f9b3c` | `fbc8ad3c…770c51e` | `efa5f129…` |

Measured directly:

```
$ git cat-file blob 17f6ef0:tools/staged-id-guard.py | sha256sum
8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762  -
$ sha256sum tools/staged-id-guard.py
efa5f129cba312c26c1fc453e6cd7f783efafeecccfac791e8c03d3d290f9b3c  tools/staged-id-guard.py
$ git diff --stat 17f6ef0 5cd2154
 tools/staged-id-guard.py | 8 +++++-   .ufo/evidence/round-43/contract.json | 24 +++-
 .ufo/evidence/round-43/guard/measure.py | 4 ++-  .ufo/evidence/round-43/mutants/measure.py | 31 +++--
```

A4 is disclosed ("during wave 1, before any deciding run", `rule_changed: false`) and it is a
real, necessary repair: at `17f6ef0` the C3 counter's own safe map (≥2 entries) is refused,
so `safe_map_admitted=0` and C3 could not pass. Two consequences the round must state, not
leave implicit:

1. `amendments_note` in the same contract claims "claims.\*, the predicates, **counters**,
   targets, kill rule and controls are byte-unchanged". A4 changed `frozen_tools`/
   `tool_sha256` (a predicate input: `measure.py:141-144` reads `frozen_tools` then compares
   `sha(git show REV:tools/staged-id-guard.py)`) and A5 rewrote the C1 counter's kill oracle.
   The note and the amendments contradict each other.
2. With the current (A5) counter and `--freeze 17f6ef0`, `self_pin` compares the contract's
   counter pin `6278edcd…` against the running counter `fbc8ad3c…` → `self_pin=0` → C3 fails
   before any map is judged. C3 can only pass with `--freeze 5cd2154`. [INFERENCE from
   reading `measure.py:128-146`; I did not run the counter at a rev outside my allowance.]

All map verdicts below are therefore given twice: **frozen** (`8140945a`, the bytes at the
assignment's freeze) and **repaired** (`efa5f129`, current HEAD), both against the freeze
registry (`git show 17f6ef0:corpus/SOURCES.md`, 113 rows, max S158, safe floor S256,
collisions S153–S158) and the staged copy whose sha matches the shokuknow original
(`020fbeaa…c807`, 103 rows S153–S255). Live-registry variants are marked **live**
(registry now also carries S159 → 7 collisions, held S153→S105, S154→S106, S159→S155).

## 1. The five assigned maps (exact `{"map": …}` files)

1. `m1_registry_id_other_doc` — reuses a registry id for a different document:
   `S155→S107` (staged S155 = `arxiv.org/abs/2302.09330`; registry S107 =
   `raw.githubusercontent.com/tensorflow/federated/…`), plus `S153→S256 S154→S257 S156→S258
   S157→S259 S158→S260`.
2. `m2_self_map` — leaves one collision on itself: `S153→S153`, plus `S154→S256 … S158→S260`.
3. `m3_wholeset` — covers all 103 staged rows with targets inside the staged range:
   - `m3a`: the cycle `S153→S154 … S255→S153` (only injective all-inside shape that exists:
     103 rows, 97 non-registry ids inside S153–S255, so any bijection inside the range must
     land on the six registry ids);
   - `m3b`: the shift `S153→S159 … S255→S261` (97 of 103 targets inside the staged range,
     6 above it).
4. `m4_duplicate_targets` — `S155→S260, S156→S260`, plus `S153→S256 …`.
5. `m5_below_floor_gap_id` — `S155→S038` (S038 is a registry **gap**: absent from
   `corpus/SOURCES.md` and from the staged set), plus fresh `S256…`. Control `m5b` repeats it
   with gap `S098`.

Extra controls I ran because they decide the same claim: `m6_partial_target_inside_staged`
(`S155→S200`), `m7_held_docs_reappended_fresh` (`S153→S256, S154→S257, …` — both documents are
**held** at S105/S106), `c0_by_document_correct` (`S153→S105, S154→S106, S155→S256 …`),
`c1_wholeset_above_floor` (whole-set, targets S256–S358), `c2_live_by_document`
(`S153→S105, S154→S106, S159→S155, S155→S256 …` on the live registry).

## 2. Results (verbatim `--json` fields)

Command shape, exactly as assigned, with the frozen files substituted for the lane files where
the lane had already moved:

```
python3 -I <tool> --registry <SOURCES.md> --staged <SOURCES.append.md> --map <map> --json
```

| map | frozen `8140945a` | repaired `efa5f129` | verdict on CORPUS clause |
|---|---|---|---|
| m1 | inadmissible: `['map has a target that is not an S-id', 'map targets collide with registry ids: S107']` | inadmissible: `['map targets collide with registry ids: S107']` | **CORRECT** (clause: "never reused") |
| m2 | inadmissible: `['…not an S-id', '…collide with registry ids: S153', 'map leaves a colliding id on itself: S153']` | same, minus the false reason | **CORRECT** ("never reused") |
| m3a | inadmissible: `['…not an S-id', '…collide with registry ids: S153,S154,S155,S156,S157,S158']` | same, minus the false reason | **CORRECT** ("never reused") |
| m3b | inadmissible: `['map has a target that is not an S-id']` — *that is the only reason*; `map_clash=[] map_staged_clash=[] map_below_floor=[] map_uncovered=[]` | **admitted**, `map_ok=true`, exit 0 | frozen: **FALSE REFUSAL** (see §3.3). Repaired: admission is CORPUS-legal but contradicts C3's wording |
| m4 | inadmissible: `['map is not injective (two staged rows share a target)', '…not an S-id']` | inadmissible: `['map is not injective (two staged rows share a target)']` | **CORRECT** (duplicate id; CORPUS.md:142 sweep must stay empty) |
| m5 | inadmissible: `['…not an S-id', 'partial map targets are below the safe floor S256: S038']` | inadmissible: `['partial map targets are below the safe floor S256: S038']` | **CORRECT** ("the next unused"; the never-reused limb does not apply to a gap) |
| m6 | inadmissible: `['…not an S-id', 'map targets are still staged ids: S200']` | same, minus the false reason | **CORRECT** (conservative: S200 is still held by the package) |
| m7 | inadmissible: `['map has a target that is not an S-id']` only | **admitted**, `map_dedupe={}` | frozen: false refusal. Repaired: **FALSE ADMISSION** vs the tool's own held rule and CORPUS.md:116-117 |
| c0 | inadmissible: `['map has a target that is not an S-id']` only, `map_dedupe={'S153':'S105','S154':'S106'}`, every other field clean | **admitted**, `map_dedupe={'S153':'S105','S154':'S106'}` | frozen: **FALSE REFUSAL**; repaired: correct |
| c1 | inadmissible: `['…not an S-id']` only | **admitted** | frozen: false refusal |
| c2 (live) | inadmissible: `['…not an S-id']` only | **admitted**, `map_dedupe={'S153':'S105','S154':'S106','S159':'S155'}` | frozen: false refusal; this is the actually-correct map for the live registry |
| m3b (live registry) | — | inadmissible: `['map targets collide with registry ids: S159']` | the same map flips verdict after the lane's own S159 append |

Exit codes: `inadmissible` → 1, `admitted` → 0 on both versions; the frozen tool prints the
false reason on every map with ≥2 entries, so `verdict="admitted"` is unreachable for any
real adoption map at the assignment's freeze.

## 3. Judgements, with clause and counterexample

### 3.1 m1 — registry id reused for a different document → refusal CORRECT
CORPUS.md:89 "never reused": S107 already keys a registry row, and adopting the arXiv row
under S107 gives one id two documents. Same for the "the next unused" limb (S107 is used).
The frozen tool's extra `'map has a target that is not an S-id'` is a **false** statement —
S107 and S256–S260 are all well-formed S-ids — so the receipt misdescribes its own decision,
but the decision is right.

### 3.2 m2 — one collision left on itself → refusal CORRECT
CORPUS.md:89 "never reused": S153 is a live registry id, so appending a row under S153
duplicates the key. The tool also reports the right alternative in its own `held` field
(`S153→S105`): the staged S153 document (POSIX diff, `pubs.opengroup.org/…/9699919799/
utilities/diff.html`) is exactly registry S105's document, so the only admissible move is
dedupe to S105.

### 3.3 m3 — whole-set maps with targets inside the staged range
- **m3a (permutation inside S153–S255)**: refusal **CORRECT**. Six targets are registry ids
  held by other documents (S153 python/ast, S154 pathlib, S155 pitest basic_concepts,
  S156 pitest faq, S157 argparse, S158 pitest DetectionStatus) → "never reused". This is the
  only injective all-inside shape, so refusal is the only correct verdict for it.
- **m3b (shift, targets S159–S261)**: the frozen tool refuses it for a reason that is false
  (both S-ids are well-formed; the semantic arrays are empty). Under CORPUS.md:89 the map is
  legal: S159–S261 are all unused in the registry and unique after the whole-set remap, and
  S159 is literally "the next unused". So the refusal is a **false refusal**, and the repaired
  tool's admission is CORPUS-correct — but it contradicts the claim's own wording
  (contract `claims.C3.statement`: "admits only a by-document map … ids at or above the safe
  floor") and the tool docstring's "never an id another staged row still holds". The verdict
  is also **time-dependent**: after the lane appended its own S159 row, the identical map is
  refused for a real clash. A pre-append guard whose admission depends on registry timing does
  not certify what the claim says it certifies.

### 3.4 m4 — duplicate targets → refusal CORRECT
Two staged rows landing on S260 mint one id twice, so the appended registry fails the
CORPUS.md:142 duplicate-id sweep (it "must print nothing") and re-uses an id inside one
append (CORPUS.md:89).

### 3.5 m5 — target below the safe floor (S038) → refusal CORRECT
S038 is a gap (present in neither file), so the "never reused" limb does **not** bite; the
deciding limb is "**the next unused**". Local evidence that the lane reads the clause this
way: the registry's 45 gaps (S038, S039, S098, S109–S130, S133–S151) are never backfilled
while later ids exist, and the lane's own round-43 note declares "Next unused id: S160". The
tool cannot distinguish an unused gap from a released id from bytes alone — but the corpus is
append-only, so gaps are unused, and refusal is the safe and contract-aligned reading.

### 3.6 m6 — partial map target inside the staged range → refusal CORRECT (conservative)
A partial map leaves the unmapped staged rows holding their ids, so S200 is still used by the
package the map renumbers; adopting S200 would either duplicate it inside the package or, if
the whole package is appended, reuse it. Same clause ("never reused"/"the next unused").

### 3.7 The two false admissions that survive the repair (the real findings)
**m7 — a held document re-appended under a fresh id is admitted.** `S153→S256, S154→S257, …`
is admitted (`map_ok=true`, `map_dedupe={}`) although staged S153 and S154 carry documents the
registry already holds at S105 and S106. The tool's docstring says held rows "dedupe to the
registry id, do not append", and CORPUS.md:116-117 admits a second row for a carried document
only as a correction whose `teaches` opens `supersedes S0NN —`. `held` is therefore reported
but **not enforced**: C3's "document-keyed dedupe" is advisory, and a map that drops it is
silently green.

**m3b — a whole-set map with 97 of 103 targets below the safe floor is admitted.** Same
paragraph: the code exempts whole-set maps from both the floor and the staged-clash test
(`if target in staged and not whole_set`, `if not whole_set and id_number(target) < …`), which
the docstring and the claim do not disclose.

## 4. Root cause and minimal reproducer for the frozen false refusal

Frozen `tools/staged-id-guard.py:172`:

```python
if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):
    reasons.append('map has a target that is not an S-id')
```

The pattern is matched against the concatenation of every target (`"S256S257"`), which can
never match a single-id pattern, so **every map with two or more entries** is refused. The
selftest at the freeze had 13 cases and its only admitted case used one entry
(`{'S002':'S010'}`), so it stayed green. Minimal isolation (synthetic registry S001–S003,
staged S002,S004):

```
map {"S002":"S010"}                 -> verdict admitted,     exit 0
map {"S002":"S010","S004":"S011"}   -> verdict inadmissible, exit 1,
   reasons ['map has a target that is not an S-id'],
   map_clash=[] map_staged_clash=[] map_below_floor=[] map_uncovered=[] map_dedupe={}
```

The repaired HEAD line is `if not all(re.fullmatch(...) for target in targets)` (line 175) and
its selftest is 14 cases (`T4_multi_entry_map_admitted` added). Verified: `--selftest` at HEAD
prints `cases=14 failed=0`.

## 5. Impacted axes

- **operability (C3)**: decisive. At the declared freeze (`17f6ef0`, tool `8140945a`) the
  claim's `safe_map_admitted=1` / `map_dedupe_live=1` are unreachable; the repaired bytes
  satisfy them for a by-document map (c0/c2 admitted, exit 0, dedupe exact) but admit two
  classes the claim's wording excludes (§3.7), and the A4/A5 commits changed the tool, both
  counter shas and a predicate input after the freeze the assignment names.
- **depth (C1)** and **calibration (C2)**: no impact from these maps. A5 changed the C1
  counter's kill oracle and the mutants counter sha; that is outside this seat's item and is
  left to the C1 seats.

## 6. Smallest safe correction

1. **Guard (HEAD `tools/staged-id-guard.py`)**: drop the whole-set carve-outs so every target
   must be unused by both files and ≥ the safe floor — delete `and not whole_set` at lines 188
   and 191. Then m3b and m3a are refused for a true reason and admission is exactly "held rows
   dedupe to their registry id, every other target is a fresh id at or above the safe floor",
   which is what C3 states. Cost, stated openly: a compact whole-set renumber starting at S159
   is refused; the lane's own 45-id gap history already tolerates that.
2. **Guard**: refuse a mapped collision whose document key is already in `registry_docs` when
   the target is not that registry id (m7), with a reason naming both ids. This is the only way
   "document-keyed dedupe" is enforced rather than reported; the check needs no new input
   because `document_key` already yields the URL/path key.
3. **Selftest**: add the two adversarial cases (whole-set in-range target; held document under
   a fresh id) so the next repair cannot reintroduce either by staying green.
4. **Round declaration**: name `5cd2154` as the frozen rev used for C3 (or re-freeze), and
   either correct `amendments_note` or record that A4/A5 changed a predicate input and both
   counter shas. As shipped, the note ("counters … byte-unchanged") is contradicted by the
   amendments it introduces.

## 7. Evidence receipts (commands run, in /tmp, now deleted)

```
python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md \
  --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
  -> collisions S153..S159 (live), 113->114 registry rows; before the S159 append:
     collisions S153..S158, registry_max S158, staged_max S255, safe_floor S256,
     held {S153:S105, S154:S106}, cascade 6, verdict refused
git cat-file blob 17f6ef0:tools/staged-id-guard.py | sha256sum      -> 8140945a…
sha256sum tools/staged-id-guard.py                                  -> efa5f129…
git cat-file blob 17f6ef0:.ufo/evidence/round-43/guard/measure.py   -> 6278edcd… (contract pin at 17f6ef0)
git cat-file blob 5cd2154:.ufo/evidence/round-43/guard/measure.py   -> fbc8ad3c… (contract pin at 5cd2154)
python3 -I <frozen tool>   --selftest -> cases=13 failed=0   (before A4)
python3 -I tools/staged-id-guard.py --selftest -> cases=14 failed=0   (HEAD)
```

No file outside `/tmp/tameshi-r43-CritC3Maps/` and this report was written; no git/jj command
beyond read-only `show`/`cat-file`/`diff`/`log`/`status`.
