# ExecC3Live — live guard run (C3, operability)

Seat: `L1Tameshi43.ExecC3Live` (leaf executor, milestone "live guard run").
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `487b8f0d…`, freeze `17f6ef0c…`.
Read-only on the lane: this seat ran tools, wrote nothing in the checkout except this report; maps and scratch tool copies live in `/tmp/tameshi-r43-ExecC3Live-/`.

## Axes this run moved

- **operability** — the guard is the round-42 post-append hazard's answer; the live run showed it could not admit *any* by-document map, i.e. the one decision it exists to make was unavailable.
- **calibration** — the 13-case selftest was green with the admitted path dead for every real map; the fixture set had no multi-entry admitted case.
- **depth** — C3's target line `safe_map_admitted=1` would have printed 0 at the freeze rev, by this defect and not by the staged data.

## Inputs at run time (bytes + sha256)

| # | when | file | bytes | sha256 |
|---|------|------|-------|--------|
| 1 | item run | `corpus/SOURCES.md` | 95387 | `afb6e5cb014be1a1a4a3621f10d34fe7afa6f9df241517ddf869896c709c38da` |
| 1 | item run | `SOURCES.append.md` (shokuknow, read-only) | 154031 | `020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807` |
| 1 | — | `tools/staged-id-guard.py` | 16786 | `8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762` (== contract pin) |
| 2 | 07:53:44 | `corpus/SOURCES.md` | 98152 | `8e404f302d4b52422cc49f6af461b0ee8cc042d716e7db624a602a78be1c4807` (transient, superseded) |
| 3 | 07:54:09 → 07:55:50 | `corpus/SOURCES.md` | 98046 | `5e556fdc23f73e37c18179ccea7ea26ae524ff97298e88db36340f8e520a4f72` |
| 3 | 07:55:30 | `tools/staged-id-guard.py` | 17248 | `efa5f129cba312c26c1fc453e6cd7f783efafeecccfac791e8c03d3d290f9b3c` |

Input 1 is **byte-identical to the registry blob at the freeze commit** (`git show 17f6ef0c:corpus/SOURCES.md` = `afb6e5cb…`), so the item's run was a clean, freeze-consistent measurement. The registry then changed twice under this seat (see Race), and the tool changed once (see Defect).

## Receipt 1 — the item's command, frozen tool

```
python3 -I tools/staged-id-guard.py --registry <lane>/corpus/SOURCES.md \
  --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
```

```json
{"cascade": ["S159", "S160", "S161", "S162", "S163", "S164"], "cascade_count": 6, "collision_count": 6, "collisions": ["S153", "S154", "S155", "S156", "S157", "S158"], "column0_collisions": ["S153", "S154", "S155", "S156", "S157", "S158"], "column0_miss": [], "extractor": "0-3space", "held": {"S153": "S105", "S154": "S106"}, "naive_map": {"S153": "S159", "S154": "S160", "S155": "S161", "S156": "S162", "S157": "S163", "S158": "S164"}, "next_free": "S159", "refused": true, "registry_docs": 99, "registry_max": "S158", "registry_rows": 113, "safe_floor": "S256", "staged_max": "S255", "staged_rows": 103, "unmapped": [], "verdict": "refused"}
```
exit 1 (`refused`).

Reproduced exactly from pinned bytes: `git show 17f6ef0c:tools/staged-id-guard.py` → `/tmp/tameshi-r43-ExecC3Live-/tool.frozen.py` (sha256 `8140945a…`), run against `/tmp/tameshi-r43-ExecC3Live-/registry.freeze.md` (`afb6e5cb…`) + `staged.snapshot.md` (`020fbeaa…`) prints the same object, field for field.

Selftest (frozen tool):

```
STAGED_ID_GUARD_SELFTEST: cases=13 failed=0
VERDICT: PASS
```
exit 0.

## Receipt 2 — same command after the sibling append

At 07:54:09 the registry had gained an uncommitted `S159` row; same command, hashes pinned before and after the run (`5e556fdc…`, unchanged across the run):

```json
{"cascade": ["S160", "S161", "S162", "S163", "S164", "S165", "S166"], "cascade_count": 7, "collision_count": 7, "collisions": ["S153", "S154", "S155", "S156", "S157", "S158", "S159"], "column0_collisions": ["S153", "S154", "S155", "S156", "S157", "S158", "S159"], "column0_miss": [], "extractor": "0-3space", "held": {"S153": "S105", "S154": "S106", "S159": "S155"}, "naive_map": {"S153": "S160", "S154": "S161", "S155": "S162", "S156": "S163", "S157": "S164", "S158": "S165", "S159": "S166"}, "next_free": "S160", "refused": true, "registry_docs": 100, "registry_max": "S159", "registry_rows": 114, "safe_floor": "S256", "staged_max": "S255", "staged_rows": 103, "unmapped": [], "verdict": "refused"}
```

This is the guard behaving correctly on a moving registry: registry `S159` (Stryker equivalent-mutants) and staged `S159` (PIT basic concepts) are **different documents**, so `S159` is a collision but not held; staged `S159`'s own document is already at registry `S155`, so it dedupes there. Arithmetic would have mapped it wrongly; the document join did not.

## By-document safe maps built by this seat

Rule used (per the contract's C3 statement): a held row targets the registry id that carries its document; every other colliding row takes the next id at or above `safe_floor`, assigned in ascending staged-id order.

- `/tmp/tameshi-r43-ExecC3Live-/safe-map-freeze.json` — 6 entries against the freeze-consistent registry:
  `S153→S105, S154→S106, S155→S256, S156→S257, S157→S258, S158→S259`
- `/tmp/tameshi-r43-ExecC3Live-/safe-map-live.json` — 7 entries against the pinned live registry (receipt 2 state):
  `S153→S105, S154→S106, S155→S256, S156→S257, S157→S258, S158→S259, S159→S155`
- `/tmp/tameshi-r43-ExecC3Live-/naive-map.json` — the tool's own `naive_map` (6 entries) for contrast.

### Frozen tool (`8140945a…`) + safe map → **inadmissible**

```
verdict=inadmissible  exit 1
map_ok=false
map_reasons=["map has a target that is not an S-id"]
map_dedupe={"S153":"S105","S154":"S106"}          # live 7-entry: plus "S159":"S155"
map_entries=6  map_targets=6  map_floor=S256
map_clash=[]  map_staged_clash=[]  map_below_floor=[]  map_uncovered=[]
```
Every rule the tool exists to enforce passes; the single refusal comes from the S-id check. Same result for the 7-entry live map.

### Post-fix working-tree tool (`efa5f129…`) + safe map → **admitted**

```
verdict=admitted  exit 0
map_ok=true  map_reasons=[]
map_dedupe={"S153":"S105","S154":"S106","S159":"S155"}   (7-entry live map)
map_entries=7  map_targets=7  map_floor=S256
map_clash=[]  map_staged_clash=[]  map_below_floor=[]  map_uncovered=[]
```
The 6-entry freeze map is likewise `admitted` with `map_dedupe={"S153":"S105","S154":"S106"}`.

## Defect: the frozen tool refused every multi-entry map

`tools/staged-id-guard.py:172-173` (frozen blob):

```python
if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):
    reasons.append('map has a target that is not an S-id')
```

`''.join(targets)` concatenates all targets, so a fullmatch against one `S\d{3,}` fails for **any map with two or more entries** (`'S105S106'`), and also for an empty map (`'S0'`). Since a safe map must cover every collision and the live package has 6+ collisions, the admitted path was unreachable for the exact input C3 measures.

Selftest blind spot (same blob): the only admitted cases are single-entry — `:286-288` `good = {'map': {'S002': 'S010'}}` (`T4_valid_map_admitted`) and `:301-304` `dedupe_map = {'map': {'S002': 'S001'}}` (`T5_dedupe_map_admitted`). The 13 cases are green while no case exercises a multi-entry admitted map, so `selftest_cases>=13` in the target did not detect it.

Counter consequence, measured at the freeze rev (`--rev 17f6ef0c… --freeze 17f6ef0c…`, default tool from `git show`):

```
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=13 selftest_failed=0 staged_rows=103 live_collisions=6 live_collisions_agree=1 live_held=2 live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=0 map_dedupe_live=1 safe_floor=S256 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C3_R43_PASS=false
```
exit 1. Only `safe_map_admitted` is 0; `map_dedupe_live=1` already.

Same counter, same rev/freeze, substitute tool = current working tree (`--tool-file`, allowed control mode):

```
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=14 selftest_failed=0 staged_rows=103 live_collisions=6 live_collisions_agree=1 live_held=2 live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 safe_floor=S256 rev=17f6ef0c72ec27e1aea305b5c95806b43bb2caef freeze=17f6ef0c72ec27e1aea305b5c95806b43bb2caef C3_R43_PASS=true
```
exit 0.

### The fix now in the working tree (not this seat's — `MutC3Selftest`)

`git diff -- tools/staged-id-guard.py`, working tree `efa5f129…` vs frozen `8140945a…`:

```
-    if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):
+    # Per-target, not over the concatenation: a multi-entry map's targets run
+    # together when joined, so a whole-string fullmatch refused every map with
+    # two or more entries (wave-1 mutation-tester MutC3Selftest, round 43).
+    if not all(re.fullmatch(r'S\d{3,}', target) for target in targets):
...
+    multi_map = {'map': {'S002': 'S010', 'S004': 'S011'}}
+    ok7, reasons7, _ = validate_map(SELFTEST_REGISTRY, SELFTEST_STAGED_INDENTED, multi_map)
+    case('T4_multi_entry_map_admitted', ok7, 'reasons=%s' % reasons7)
```

This is the same one-line change this seat derived independently (per-target instead of joined), plus the missing fixture. Post-fix selftest: `cases=14 failed=0`, `VERDICT: PASS`.

## Remaining operability defects in the post-fix tool (`efa5f129…`)

1. **The documented map key form crashes the tool.** `:27-30` documents `{"map": {"staged:S001": "S161", …}, "staged": path, "registry": path}`, but `validate_map` indexes keys with `id_number(kv[0])` (`:180`) → `int('taged:S153')` → `ValueError: invalid literal for int() with base 10: 'taged:S153'` (`:102`). Receipt (freeze registry + a map using the documented key form): exit 1, **no `--json` object**, traceback on stderr. Exit 1 is also the "inadmissible" code, so a caller cannot tell a crash from a verdict by exit status; the round-43 counter's `run_guard` would report `guard_error`/`no_json`. A key that is not an S-id belongs in the `Refusal` path (exit 2).
2. **Documented JSON field that does not exist.** `:43-46` names `column0_extract`; the object emits `column0_collisions` and `column0_miss`. Anything built on the docstring's field list reads a missing key.
3. **The map file's `staged`/`registry` keys are ignored.** `main` (`:340-350`) takes both paths from argv only, so the documented in-file paths are never checked — a caller can hand a map built against one registry while the tool validates it against another, silently.

## Freeze integrity (decision for L1, not taken here)

`contract.json` pins `tool_sha256` and `frozen_tools["tools/staged-id-guard.py"]` at `8140945a…` (the refusing blob). The counter's `tool_sha_ok` compares the tool at `REV` via `git show`, not the working tree, so:

- a deciding run at `REV=17f6ef0c…` measures `8140945a…` and prints `safe_map_admitted=0`, `C3_R43_PASS=false` — regardless of the working-tree fix;
- to pass, the fixed blob must be the one at the deciding `REV` **and** the contract's `tool_sha256` / `frozen_tools` pin amended to it (a post-freeze amendment; `claims`/predicates/counters stay byte-unchanged). Absent that, C3's statement "admits only a by-document map" is false as frozen, and the round should record C3 as failed-by-defect rather than fix it after the fact.

This seat took no such decision and edited no lane file.

## Race: the registry is being edited while seats run

`corpus/SOURCES.md` is `M` in the index-free working tree and changed under this seat three times (`95387` → `98152` → `98046` bytes within ~2 minutes; mtime 07:53:22 for the surviving append). The surviving append adds `S159` (Stryker equivalent-mutants) and, briefly, `S160` (Wikipedia mutation testing). Consequences:

- the round-43 counter reads the registry at `REV` via `git show`, so its numbers are stable and this seat's `--tool-file`/default receipts are unaffected;
- any seat that runs the guard against the *working tree* gets the larger collision set (7 now, 8 during the transient state) — my two live receipts document that — and must pin hashes around the run, as done here.

## Tooling

No installs, no upgrades: `python3` (system) only; nothing was installed for this seat.

## Retained artifacts (item names this directory)

`/tmp/tameshi-r43-ExecC3Live-/`: `safe-map-freeze.json`, `safe-map-live.json`, `naive-map.json`, `docstring-map.json`, `registry.freeze.md` (`afb6e5cb…`), `registry.live.md` (`5e556fdc…`), `staged.snapshot.md` (`020fbeaa…`), `tool.frozen.py` (`8140945a…`), `staged-id-guard.fixed.py` (this seat's independent build, `30434415…`), `runA.json`, `safe-map.out`, `safe-map-fixed.out`, `naive-map-fixed.out`.

## Net effect on the C3 target line

With the working-tree tool (`efa5f129…`, 14 cases): `self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=14 selftest_failed=0 staged_rows=103 live_collisions_agree=1 live_held_agree=1 live_unmapped=0 live_verdict=refused live_cascade=1 naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 safe_floor=S256 → C3_R43_PASS=true`. With the frozen pin, `safe_map_admitted=0` → `C3_R43_PASS=false`.
