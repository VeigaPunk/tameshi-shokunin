# MutC3Selftest — is the guard's own selftest load-bearing?

Lane `tameshi`, round 43, wave 1. Bounds: READ-ONLY on the lane checkout; every mutant copy under
`/tmp/tameshi-r43-MutC3Selftest-verify/` (deleted before return). No tool installed or upgraded
(pacman paused host-wide); `python3` 3.14, host packages only.

Measured bytes, in order (the tree moved under this seat during the run — see the timeline):
`17f6ef0` tool `8140945a…f97b762`, counter `6278edcd…78601`, 13 cases; `5cd2154` tool `efa5f129…f9b3c`,
counter `fbc8ad3c…0c51e`, 14 cases; working tree `365bf958…0b0c2` (uncommitted), 23 cases.

## 1. The three assigned mutants — 3/3 killed at the freeze they were written against

Pristine control (freeze `17f6ef0`, tool sha `8140945a…`):

```
STAGED_ID_GUARD_SELFTEST: cases=13 failed=0
VERDICT: PASS
```

| # | Single edit | Line | Mutant sha256 (16) | `--selftest` at 17f6ef0 | Catching case | Verdict |
|---|---|---|---|---|---|---|
| M1 | `ROW_RE` → column-zero `r'^\|…'` | 54 | `e6b1ef68fdb397d7` | cases=13 **failed=7** exit=1 | `T1_indented_collision_seen` (+6 collateral) | killed |
| M2 | staged-clash reason dropped | 196-198 | `fd9442372bce486a` | cases=13 **failed=1** exit=1 | `T3_map_onto_staged_refused` (`reasons=[]`) | killed |
| M3 | `document_key` always `''` | 88 | `ee07d3d5ab2d9c9f` | cases=13 **failed=2** exit=1 | `T5_dedupe_to_registry_id`, `T5_dedupe_map_admitted` | killed |

```
=== m1 exit=1
STAGED_ID_GUARD_SELFTEST: cases=13 failed=7
FAIL T1_indented_collision_seen collisions=[]
FAIL T1_column0_blind column0_miss=[]
FAIL T3_cascade_refused naive={} cascade=[]
FAIL T4_valid_map_admitted reasons=['map names a row the package does not carry: S002']
FAIL T3_map_onto_registry_refused reasons=['map names a row the package does not carry: S002']
FAIL T3_map_onto_staged_refused reasons=['map names a row the package does not carry: S002']
FAIL T4_partial_map_refused reasons=['map has a target that is not an S-id']
VERDICT: FAIL
=== m2 exit=1
STAGED_ID_GUARD_SELFTEST: cases=13 failed=1
FAIL T3_map_onto_staged_refused reasons=[]
VERDICT: FAIL
=== m3 exit=1
STAGED_ID_GUARD_SELFTEST: cases=13 failed=2
FAIL T5_dedupe_to_registry_id held={}
FAIL T5_dedupe_map_admitted reasons=['map targets collide with registry ids: S001'] dedupe={}
VERDICT: FAIL
```

Re-run against the A4/A5 bytes (`efa5f129`, 14 cases), still killed: M1 8 failed, M2 1, M3 2.

```
=== m1b exit=1 sha=307827089750a41a   cases=14 failed=8
=== m2b exit=1 sha=54e939e8b24f5af9   cases=14 failed=1  (FAIL T3_map_onto_staged_refused)
=== m3b exit=1 sha=0d8e75fb7cfde89d   cases=14 failed=2  (FAIL T5_dedupe_to_registry_id, T5_dedupe_map_admitted)
```

### The selftest is the *only* detector for M1 and M2

Scored through the counter's falsifier mode (`--tool-file`, `--rev/--freeze 17f6ef0`; note
`measure.py:142` pins `tool_sha_ok` from `git show REV:tools/…`, not from the substitute, so a
substitute has to be killed behaviourally):

| tool-file | selftest_exit | live_collisions_agree | live_held_agree | live_unmapped | naive_map_refused | `C3_R43_PASS` |
|---|---|---|---|---|---|---|
| pristine | 0 | 1 | 1 | 0 | 1 | false (join bug) |
| M1 | **1** | 1 | 1 | 0 | 1 | false (join bug) |
| M2 | **1** | 1 | 1 | 0 | 1 | false (join bug) |
| M3 | **1** | 1 | **0** | **6** | 1 | false |

M1 and M2 leave every live check at its good value — the live registry is column-zero, and the
naive map is refused by the cascade verdict, not by the reason M2 deleted. Only `selftest_exit`
moves. Load-bearing for these three axes: **yes**.

Case-quality notes (not gaps): `T1_extractor_label` asserts a hardcoded string and passes on M1;
`T4_partial_map_refused` fails on M1 only incidentally (empty map hits the S-id rule).

## 2. Gap A — the join bug, found at 17f6ef0, since repaired

`tools/staged-id-guard.py:172` (freeze bytes): `re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0')`
can only match a **one-entry** map, so every 2+ entry map was refused `'map has a target that is
not an S-id'`. Proof on the freeze bytes with the exact safe map the counter builds:

```
safe_map {'S153':'S105','S154':'S106','S155':'S256','S156':'S257','S157':'S258','S158':'S259'}
verdict=inadmissible ok=False reasons=['map has a target that is not an S-id']   rc=1
```

`map_clash=[] map_staged_clash=[] map_below_floor=[] map_uncovered=[] map_dedupe={'S153':'S105','S154':'S106'}`
— the map is otherwise admissible, so `safe_map_admitted=0` made `C3_R43_PASS` false at `17f6ef0`.

Status now: closed by `5cd2154` (per-target `all(re.fullmatch(...))` plus the new case
`T4_multi_entry_map_admitted`), and the live safe map is admitted (`verdict=admitted`, rc=0). The
new case is load-bearing: restoring `''.join` on the patched bytes gives
`cases=14 failed=1 — FAIL T4_multi_entry_map_admitted`.

## 3. Gap B (OPEN) — surviving mutant M4: the whole-set exemption is untested

M4 removes both `not whole_set` exemptions (`:191` and `:194` at 17f6ef0; `:226`/`:229` on the
working tree), so a whole-set map is held to the partial-map floor and staged-clash rules.

| bytes | M4 `--selftest` | live counter (`--tool-file`) |
|---|---|---|
| `17f6ef0` (13 cases) | cases=13 **failed=0 PASS** | every component identical to pinned; `C3_R43_PASS=false` (join bug, same as pinned) |
| `5cd2154` (14 cases) | cases=14 **failed=0 PASS** | `selftest_exit=0 selftest_failed=0 live_*=good safe_map_admitted=1 map_dedupe_live=1 **C3_R43_PASS=true**` — byte-for-byte the pinned tool's line |
| working tree `365bf958` (23 cases) | cases=23 **failed=0 PASS** | not scored (uncommitted, moving) |

It is not an equivalent mutant — the behaviour differs:

```
current: whole-set S011->S004 (floor S012) ok=True  reasons=[]
M4c:     whole-set S011->S004 (floor S012) ok=False reasons=['partial map targets are below the safe floor S012: S004']
```

**Missing case — `T4_whole_set_floor_refused`** (the case that should have existed):

```python
    # whole-set map (len(map) == len(staged)) must LOSE the floor exemption:
    # the floor is a partial-map rule, a whole-set renumber may go below it,
    # and a mutation that enforces it anyway must be caught.
    reg2 = REG_AT_S010_S011                    # floor S012
    whole2 = STAGED_ONE_ROW_NEW_DOC            # 1 row, id S011, new document
    ok8, reasons8, _ = validate_map(reg2, whole2, {'map': {'S011': 'S004'}})
    case('T4_whole_set_floor_admitted', ok8, 'reasons=%s' % reasons8)
    ok9, reasons9, _ = validate_map(reg2, whole2, {'map': {'S011': 'S013'}})
    case('T4_whole_set_above_floor_admitted', ok9, 'reasons=%s' % reasons9)
```

(`T4_whole_set_floor_admitted` is the discriminating assertion: it passes on the current tool and
fails on M4c. Without it the exemption is unconstrained in both directions.) Second half of M4 —
removing the staged-clash exemption for whole-set maps — needs a whole-set package whose map
targets an id another staged row holds; no existing fixture has that shape.

## 4. Reviewer divergences (RevC3Tool) — verified, and their selftest coverage

Reproduced independently on the freeze bytes `8140945a` and again on the current working tree
`365bf958`:

| # | Divergence | At `17f6ef0` | At `365bf958` (now) | Selftest case? | Case that should exist |
|---|---|---|---|---|---|
| 1a | `HEXISH` strips 7-40 hex runs: `/data/deadbeef/notes.md` and `/data/feedface/notes.md` both → `/data//notes.md`; distinct documents collapse | `held={'S002':'S002'}` (false dedupe, silent non-append) | **fixed** (`held={}`, `normalise_document`) | no | `T7_hex_paths_stay_distinct` (`held == {}`) |
| 1b | a hex-only stem is deleted: `abc1234.md` → `''` → false unmapped | `unmapped=['S002'] refused=True` | **fixed** (`unmapped=[]`) | no | `T7_short_hex_filename_kept` |
| 2 | `analyse` can call a collision held on its own id (`held={X:X}`) while `--map {X:X}` is refused "map leaves a colliding id on itself" — the tool's own dedupe answer is unrepresentable | `held={'S002':'S002'}`, map ok=False | **still open** | no (`T5_dedupe_*` all use `S002→S001`) | `T5_self_held_dedupe_representable` — assert `analyse.held[X]==X ⟹ validate_map({X:X}) admits` (or that `analyse` must not report `X` as held) |
| 3 | `whole_set` skips the floor: a 1-row package may map below `safe_floor` while the identical target in a partial map is refused | admitted, `reasons=[]` | **still open** | no | `T4_whole_set_floor_admitted` (same case as M4 above) |
| 4 | empty map `{}` on a zero-collision package refused by the `'S0'` fallback | `reasons=['map has a target that is not an S-id']` | **fixed** (`ok=True`) | no | `T4_empty_map_zero_collisions_admitted` |

Divergence 3 is the design intent (a whole-set renumber may go below the floor), so it is a
*specification* item the contract should state, not necessarily a bug — but it is exactly the
semantics M4 mutates, and nothing pins it. Divergence 2 looks like a real contract hole: the tool
publishes `held` as an answer that `--map` will not accept.

## 5. Verdict for the milestone "guard selftest load-bearing"

* Assigned mutants: **3/3 killed**, at the freeze they were written against and again at `5cd2154`;
  for M1 and M2 the selftest is the sole detector (no live counter check moves).
* The selftest was **blind to both admission defects that existed at the freeze**: the
  `''.join(targets)` bug (fixed post-freeze with the case this seat proposed) and the whole-set
  exemption (M4, **still surviving all 23 cases** on the working tree). On the admission axis — the
  axis C3 actually claims — the selftest is therefore *not yet* load-bearing: it is load-bearing on
  the extractor, the refusal reasons and the dedupe join.
* Gap B is a coverage finding only; it does not license changing the contract. Divergence 3 must be
  pinned by the contract before any case asserts it.
* Structural: the selftest never calls `main()` (M6b, section 7). No case pins the exit-code/JSON
  contract, so the entire CLI surface the C3 counter consumes is unguarded from the selftest side.

## 6. Restoration, bounds, and tree drift

* No write outside `/tmp/tameshi-r43-MutC3Selftest-verify/`, `/tmp/tameshi-r43-MutC3Selftest-audit/`
  and this report; no
  `git add/commit/stash/checkout/switch/reset/pull/push`; no `jj` command; nothing written in
  `/home/vgpnk/Projects/shokuknow`.
* Scratch deleted after these numbers were recorded.
* `tools/staged-id-guard.py` was byte-identical to the pin (`8140945a…`) after this seat's first
  phase. It then changed **without this seat touching it**: `5cd2154` (L1, A4/A5 guard map-shape
  repair) re-pinned it to `efa5f129…`; an uncommitted edit took it to `365bf958…` (23 cases); commit
  `273c047` (A9) froze it at `e219007f…`. Every measurement names the bytes it was taken on.

## 7. Addendum — audit at the A9 freeze (`273c047`, tool `e219007f…`, counter `ae66342d…`, 23 cases)

Selftest control: `cases=23 failed=0 PASS`. At A9 the counter adds `substitute == 0` to the predicate
(`measure.py:279`), so any `--tool-file` run scores `C3_R43_PASS=false` **by construction**; a
falsifier must be read component by component. (Section 3's M4 line at `5cd2154` predates that
marker; all its components were nevertheless identical to the pinned tool's.)

### RevC3Tool's F-items, re-probed on A9 bytes

| Item | Verdict at `e219007f` | Selftest pins it? | Case that should exist |
|---|---|---|---|
| F2 documentless collision admitted by `--map` | **fixed** — `reasons=['map decides an undocumented row: S002']`, new `map_undocumented` field | **yes** — M7 (reason dropped) is killed: `cases=23 failed=1 FAIL T8_undocumented_row_refused_in_map reasons=[]` | — |
| F8 non-S map key / non-str target → traceback, exit 1, no JSON | **fixed** — both now `REFUSED` with `verdict=setup_refusal`, exit 2, JSON on stdout | **no** | `T9_cli_contract` (below) |
| F9 map file's `staged`/`registry` keys never read | **open** — `{"staged":"/nonexistent","registry":"/nonexistent"}` still `map_ok=true`, exit 0 | no | `T12_map_input_paths_checked` |
| F11 `column0_extract` key absent; `cells`/`lineno` written never read; `<5` cells vs an 11-column schema | **partly open** — key still absent (`column0_collisions`/`column0_miss`), `'cells'`/`'lineno'` have zero readers, threshold still `len(cells) < 5`; the unused `os` import is gone (`os.stat` now used) | no | `T12_json_field_names`, `T6_malformed_threshold` (a 6-cell row must be refused) |
| F12 marked id / 4-space / tab indent silently unparsed | **open** — `| S002* |`, 4-space and tab rows all give `staged_rows=0 collisions=[]`, no refusal | no | `T13_no_silent_row_drops` |

F12 is the highest-severity selftest gap left after M4: the guard answers "no collisions, nothing to
map" about a package it did not parse, and 23 green cases do not notice. The invariant to encode:
**`analyse` must never drop a line that looks like a row** — either it parses (and every data line is
counted, `staged_rows == len(data lines)`) or it raises `Refusal` naming the line.

### M6b — the selftest never exercises `main()`

`grep -c 'main('` = 2 (definition, `__main__` guard); no case calls `main`, `--json`, `--map` file
loading, or any exit code. So the whole CLI contract the C3 counter consumes is unpinned by the
selftest. M6b collapses it:

```
    return 0  # MUTANT M6b: exit contract collapsed to 0
    if result['verdict'] in ('admitted', 'answered'):
        return 0
    return 1
```

```
M6b --selftest: cases=23 failed=0 PASS   -> SURVIVED
M6b CLI, self-map {S001:S001}: exit=0 (pinned: 1)  -> the guard now exits 0 on an inadmissible map
M6b counter: naive_map_refused=0 (pinned 1)        -> killed live, invisible to the selftest
```

(M6b sits after `if args.selftest: return selftest()`, so `--selftest` still runs and the
mutant is a pure CLI-contract collapse. The cruder variant — `return 0` as `main`'s first
statement — does NOT survive: `--selftest` prints nothing and the counter reports
`selftest_exit=0 guard_error=no_json`, caught upstream of `MIN_CASES`.)

**Missing case — `T9_cli_contract`:** call `main(['--registry', REG, '--staged', STG, '--map', M,
'--json'])` and assert the triple `(exit, verdict)` is `(0,'admitted')`, `(1,'inadmissible')`,
`(2,'setup_refusal')`, plus that nothing but JSON reaches stdout and that `--map` absent yields
`answered`/`refused` with exit 0/1. This is the case that would have made F8 and M6b findable
pre-freeze.

### Counter note (confirms the reviewer)

`measure.py:223` computes `map_dedupe_live` from `safe_doc` without checking `safe_code`, so
`map_dedupe_live=1` is observable on an inadmissible safe map (it read 1 at `17f6ef0` while
`safe_map_admitted=0`). Harmless for the predicate (both components are required separately a line
later), but a falsifier reading components in isolation can mistake it for admission.

## 8. Addendum — A10 (`3aee2c0`, tool `2e8f2e89…`, 488 lines, **24** cases; A9 was 23)

Selftest control at A10: `cases=24 failed=0 PASS`. RevC3Tool's F-statuses confirmed where I
re-probed them: F5 code fix present (no whole-set exemption in `validate_map`), F11 threshold still
`len(cells) < 5` — a 5-cell staged row is **accepted** (`staged_rows=1`), F12 still silent
(`| S001* |`, 4-space and tab rows all `staged_rows=0`, no `Refusal`).

### Three mutants pass all 24 cases

| Mutant | Edit | Selftest | Live counter (A10 freeze, `--tool-file`, per-component) |
|---|---|---|---|
| **M9** | below-floor check deleted (`if id_number(target) < id_number(floor)` removed) | cases=24 **failed=0 PASS** | **every component identical to pinned** (`live_*=1`, `naive_map_refused=1`, `safe_map_admitted=1`, `map_dedupe_live=1`, `selftest_exit=0`; only `substitute=1` differs) |
| **M8** | whole-set exemption restored (`… and not (len(mapping) == len(staged))`) | cases=24 **failed=0 PASS** | identical to pinned |
| **M6b** | exit contract collapsed (early `return 0` after the `--selftest` branch) | cases=24 **failed=0 PASS** | `naive_map_refused=0` (killed live only) |

M9 is the serious one: the **safe-floor rule** — a component the contract's own C3 predicate names
("at or above the safe floor") — can be deleted outright and neither detector notices. The counter
cannot see it because its safe map targets sit *at* the floor (`S256`), never below it.

### Why `T12_whole_set_in_range_refused` pins nothing

`:366` uses `{'S002': 'S003', 'S004': 'S003'}` — non-injective, and `S003` is a **registry** id.
Observed reasons, identical on the pinned tool and on M9:

```
['map is not injective (two staged rows share a target)',
 'map targets collide with registry ids: S003,S003']
```

The assertion is `any('not injective' in r or 'safe floor' in r …)`, satisfied by the first reason.
The staged-clash and below-floor branches are never reached, so the A10 whole-set repair is unpinned
in every direction. (`T4_partial_map_refused` uses `{}` — no targets — so it cannot cover the floor
either.)

### The case that discriminates — `T12b_floor_enforced`

Verified on the A10 bytes: registry `S001`, staged one row `S001` with a new document →
`safe_floor=S002`, `collisions=['S001']`; map `{'S001': 'S000'}` is injective, covers the collision,
clashes with neither set — only the floor rule can refuse it.

```
pinned:  ok=False reasons=['partial map targets are below the safe floor S002: S000']
M8:      ok=True  reasons=[]      (whole-set exemption restored)
M9:      ok=True  reasons=[]      (floor rule deleted)
```

```python
    floor_map = {'map': {'S001': 'S000'}}      # floor S002; S000 free, injective, covers all
    ok11, reasons11, _ = validate_map(REG_ONE_ROW, STG_ONE_ROW, floor_map)
    case('T12b_floor_enforced',
         not ok11 and any('safe floor' in r for r in reasons11), 'reasons=%s' % reasons11)
```

Passes on A10, fails on both M8 and M9. Suggested companion invariants from the same probe:
`T6_malformed_threshold` (a 6-cell row must raise; today 5 cells are accepted) and
`T13_no_silent_row_drops` (a row-looking line is parsed and counted, or `Refusal` names it).

### Doc vs code (F5 flipped)

`:33` still reads "…disjoint from the staged set and at or above the safe floor **unless the map
covers the whole staged set**", and the refusal at `:238` still says "**partial** map targets are
below the safe floor" even for whole-set maps. No selftest can catch a docstring; the doc must move
in the same commit as the code, and the message wording must stop claiming a distinction the code no
longer makes. Which side is right (exemption or no exemption) is a contract decision — not a test
decision, and not this seat's.

### A10 verdict

* Selftest: **24/24 green, and it is the wrong 24.** On the A10 bytes it cannot distinguish the real
  guard from one with the floor rule deleted (M9) or the whole-set exemption restored (M8), and it
  never exercises `main()` (M6b). Load-bearing for the extractor, refusal reasons, dedupe join and the
  undocumented-row rule; **not** load-bearing for the map-admission rules that C3 actually scores.
* Minimal repair, in priority order: `T12b_floor_enforced`, `T9_cli_contract`, `T13_no_silent_row_drops`,
  `T6_malformed_threshold`. Each is written above or in §7 and each fails on at least one mutant.


