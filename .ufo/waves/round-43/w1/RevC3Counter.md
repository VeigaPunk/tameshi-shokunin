# RevC3Counter — is the C3 counter independent of the tool it measures?

Lane `tameshi`, round 43, wave 1. Bounds honoured: READ-ONLY on the lane checkout (one
write: this report), nothing written to `/home/vgpnk/Projects/shokuknow` or to the assimil
package; every probe ran from `/tmp/tameshi-r43-RevC3Counter/` (deleted before return).
No git/jj mutation. No tool installed or upgraded (pacman paused host-wide); `python3` 3.14.8
from the host, stdlib only.

## Subject and revisions (read this before the findings)

Two byte-sets are in play because an amendment landed **during** this review:

| Role | rev | C3 counter sha256 | guard tool sha256 |
|---|---|---|---|
| declared freeze | `17f6ef0c…` (2026-10-25T07:48:57-03:00) | `6278edcd…` | `8140945a…` |
| lane HEAD now | `5cd2154f…` (2026-10-25T07:56:24-03:00, "freeze A4/A5") | `fbc8ad3c…` | `efa5f129…` |

`A4` repairs the tool's map-shape check; `A5` changes the counter's pin source (only lines
139-144; every other line in the counter is byte-identical, so citations below are against
the frozen blob with "+2 after line 139" for the amended file). All counter runs I made are
at `--rev 487b8f0…` (base) or `--rev 17f6ef0…` (freeze); the `--tool-file` runs are controls.
I did **not** run the counter at HEAD (outside the allowed revision set) — HEAD-state
conclusions below come from running the HEAD *tool* directly, labelled as such.

Sanctioned run at the declared freeze, before A4 landed (07:5x):

```
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=13
selftest_failed=0 staged_rows=103 live_collisions=6 live_collisions_agree=1 live_held=2
live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1
safe_map_admitted=0 map_dedupe_live=1 safe_floor=S256 rev=17f6ef0c… freeze=17f6ef0c…
C3_R43_PASS=false          EXIT=1
```

Same command after A4/A5: `self_pin=0 … C3_R43_PASS=false EXIT=1`.

## Direct answer

**Separate process, separate code — but not an independent oracle.** The counter never
imports the tool and runs it under `-I` in a temp dir, yet `own_parse` (measure.py:85-97) is a
re-typed copy of the tool's `ROW_RE`/`URL_RE` constants (measure.py:58-59 == tool:54,56) and of
its URL branch (tool:64-99). The collision agreement check is therefore a self-comparison: it
can only prove two copies of one pattern agree, not that the collision set is complete
(H3). The dedupe is reimplemented *narrower* than the tool's document key (URL only, no
path-head branch) and yields false negatives (M3). The safe map and the naive map are not
independent at all: the safe map is built to the tool's own floor formula and the naive map is
the tool's own output fed back to it (M4, H4). `tool_sha_ok` certifies the git blob, not the
bytes that executed, and can read `1` for an arbitrary substitute (H2).

---

## Blocking

### B1 — at the declared freeze `safe_map_admitted=0`, so `C3_R43_PASS=false`
`tools/staged-id-guard.py:172` (pinned bytes): `re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0')`
joins every target into one string, so **any map with two or more entries fails the S-id
check**. The counter's safe map has six entries (measure.py:211-222), so the tool refuses it.
Isolated, two-entry map of valid ids `{S155:S256, S156:S257}`:

```
two_fresh  rc 1 verdict inadmissible reasons ['map has a target that is not an S-id', 'map does not cover every collision: …']
one_fresh  rc 1 verdict inadmissible reasons ['map does not cover every collision: …']
```

The tool's selftest stayed green (13/13) because its only admission case is one entry
(`T4_valid_map_admitted`, tool:286-288) and the only two-entry map it submits is *expected* to be
refused (`T4_non_injective_refused`) — the cardinality was never exercised. A4
(HEAD `tools/staged-id-guard.py:175`, per-target `all(...)`) repairs this; verified on HEAD
bytes: the counter's exact safe map returns `rc 0 verdict admitted dedupe {'S153':'S105','S154':'S106'}`,
selftest `cases=14 failed=0`. **Residual:** the repaired tool is not in the freeze commit, so
the freeze no longer passes (M1).

## High

### H1 — the repaired tool admits an arithmetic map: "only a by-document map" is false
`tools/staged-id-guard.py:177-196` (HEAD). The only document check is the dedupe branch
(`if target in registry`, :184). A *fresh* target is judged solely on injectivity, staged
overlap and the floor; nothing ties it to the staged row's document. Pure arithmetic map,
no dedupe at all, every target above the floor:

```
map {'S153':'S256','S154':'S257','S155':'S258','S156':'S259','S157':'S260','S158':'S261'}
rc 0 verdict admitted reasons [] dedupe {}
```

`S153` and `S154` are documents the registry already holds (`S105`, `S106`); this map
appends duplicates of both under new ids. That is precisely the decision the tool's docstring
says it exists to refuse ("the URL or DOI is the evidence and the id follows it, never
arithmetic") and what C3's statement asserts ("admits only a by-document map"). Scenario: a
seat feeds its own `max+1` arithmetic after a cascade scare and the guard green-lights a
duplicate append.

The counter cannot see this class: its only admitted-map probe is `safe_map`
(measure.py:211-223), which is by-document **because the counter built it that way**, not
because the tool requires it. Add a probe: a fresh-target map over a *held* document must be
`inadmissible`; today it is `admitted`.

### H2 — `tool_sha_ok` can pass for a substitute
`tool_sha_ok` is computed from `show(lane, rev, TOOL_REL)` (measure.py:139-143 pinned;
141-143 amended). `--tool-file` replaces the executed `tool_path` (measure.py:156-159) and
never touches `tool_sha_ok`, and no printed field records that a substitute ran
(fields list, measure.py:244-266). Demonstration at `--rev 17f6 --freeze 17f6` with a
40-line substitute (column-0 extractor, `--selftest` prints `cases=13 failed=0` and exits 0)
whose sha `9acbd2b1…` differs from the pin `8140945a…`:

```
… tool_sha_ok=1 selftest_exit=0 selftest_cases=13 selftest_failed=0 … C3_R43_PASS=true
EXIT=0
```

Because the live registry (113 rows) and the staged package (103 rows) contain **zero**
indented rows, a column-0 extractor agrees with the census pattern on live data — so the
substitute passed every live field. Consequence: a receipt that says `tool_sha_ok=1
C3_R43_PASS=true` does not establish that the pinned tool ran. Fix: when `--tool-file` is
used, print `tool_source=substitute substitute_sha256=…` and force `tool_sha_ok=0`
(and `C3_R43_PASS=false`) unless the substitute sha equals the pin.

### H3 — the extraction is a copy, and the live data does not exercise the property it claims
`measure.py:58-59` is byte-identical to `tool:54,56`; `own_parse` (85-97) re-implements
`parse_rows`+`document_key`'s URL branch. Shared bug, shared blind spot: tab-indenting the
colliding `S153` row in a private copy of the package drops the collision in **both**
extractors and the counter reports perfect agreement:

```
live_collisions=5 live_collisions_agree=1 live_held=1 live_held_agree=1 staged_rows=102
```

(`staged_rows` falls 103→102 in the counter and in the tool.) A silent collision miss is
therefore green. Also, the claim's load-bearing property — the census-valid *0-3-space*
pattern — is only exercised by the tool's **self-reported** selftest text
(`re.search(r'cases=(\d+) failed=(\d+)', selftest_text)`, measure.py:171-173); `column0_miss`
is never read. Scenario: the tool regresses to column-0 and keeps a green selftest string
(H2's substitute is exactly that). Fix: carry a two-row indented fixture in the counter and
require the tool to report that collision itself.

### H4 — the naive-map round trip asks the tool to grade its own answer
`measure.py:205-209` writes `doc['naive_map']` and feeds it back through `--map`; the counter
never constructs a naive map of its own. An empty naive map still yields
`naive_refused=1` (`{'map': {}}` → every collision uncovered → `inadmissible`), and
`live_cascade` (measure.py:200-203) only checks that each reported cascade id is *some* staged
id, never that `cascade == sorted(naive_map.values ∩ staged)`. Both together, on a copy whose
`analyse` returns `naive_map={}` and `cascade=['S159']`:

```
… live_unmapped=0 live_cascade=1 naive_map_refused=1 safe_map_admitted=1 … C3_R43_PASS=true
```

So "refuses its own naive arithmetic map because its targets are still staged ids" is not
measured. Fix: build the naive map in the counter from `own_collisions` + its own registry max,
require the tool to refuse it, and assert the cascade equals the derived intersection.

## Medium

### M1 — the measurement revision is no longer the freeze
A4/A5 are commits *after* the freeze and after wave-1 seats ran. At `--rev 17f6` the amended
counter reads the old contract (pins `6278edcd`/`8140945a`) and prints `self_pin=0`; the
pinned tool with the amended contract cannot pass either. The only passing combination is
`--rev HEAD --freeze HEAD`, i.e. a revision created after seats ran, while
`contract.frozen_before` still reads "before any wave seat ran and before the first deciding
run". Whatever the L1 decides, the round report must name the deciding rev as post-freeze and
say the freeze bytes do not satisfy the target. (The `self_pin` check itself is sound and is
what caught this: it caught the edit at 07:56 while I was mid-review.)

### M2 — `live_unmapped=0` is not an independent check
`measure.py:200` only takes `len(doc['unmapped'])`; the counter never computes its own unmapped
set (it computes `own_held`, never `own_unmapped`). The tool's `document_key` (:86-99) falls
back to "a source head with `/` or `.` and length > 8", so prose with a period becomes a
document: with `S153`'s source cell set to `see above.` the tool reports
`unmapped=[] held={'S154':'S106'}` — the row is treated as documented. The counter's safe map
then assigns `S153` a fresh id (it is not in `own_held`), the tool admits that renumber, and at
`--rev 17f6 --freeze 17f6` with the join repair in place the counter prints
`live_unmapped=0 live_held_agree=1 safe_map_admitted=1 C3_R43_PASS=true`. A document-less row
renumbered by arithmetic, with the counter green — the tool's stated invariant violated and
invisible. Fix: compute `own_unmapped` from the counter's own parse and compare; never build
the safe map over a collision the counter cannot join to a document.

### M3 — `own_held` is URL-only: false negative on path-keyed documents
`measure.py:186-194` joins on URL equality; the tool joins on `document_key`, which for
`S032` is `kumitate \`scripts/kimi-census.mjs\` (fleet gate, read-only)` (8 of the 14
non-URL registry rows get such a key; 6 get `''`). Staged row `S153` given that same source:

```
tool      held {'S153': 'S032', 'S154': 'S106'}   (correct per its own contract)
counter   live_held=1 live_held_agree=0 C3_R43_PASS=false
```

A **correct** tool is failed, and the counter's safe map would have handed `S153` a fresh id
(duplicate of `S032`) had the agreement not tripped on something else. Fix: implement the
same documented key function in the counter (independently written, from the tool's prose
contract), not just the URL branch.

### M4 — the staged input is unpinned and read twice
`measure.py:146` only checks existence; `run_guard(..., args.staged)` (:175) reads the live
external file and `own_parse(read(args.staged))` (:184) reads it again. The contract's
`staged_input` names the path with no sha256, and the receipt prints no staged digest
(fields :244-266). Scenario: the package is a live file under `/home/vgpnk/Projects/shokuknow`
that other lanes may touch between the two reads → `live_collisions_agree` flips with no tool
defect; or `--staged` is pointed at a doctored copy with ≥100 rows, one held URL and one
cascade, and the run passes. Fix: snapshot the staged bytes once into `work/`, run the tool on
the snapshot, and print `staged_sha256` (plus pin it in the contract).

### M5 — the control is vacuous at zero collisions, and its exit polarity collides with a failing measurement
`measure.py:225-235`. Live: `stub_collisions_agree=0 expected_collisions=6 C3_R43_CONTROL_PASS=false`,
`EXIT=1`. With a collision-free staged copy:
`stub_collisions_agree=1 expected_collisions=0 C3_R43_CONTROL_PASS=true EXIT=0` — the constant-empty
stand-in agrees with an empty expectation, so the control proves nothing. There is no
`len(own_collisions) >= 1` guard, and `--control` exercises only the `collisions` field
(never `held`, `naive_map`, `map`), so the map paths have no do-nothing evidence. Also
`--control` returns 0 when the stand-in is **accepted** (i.e. when the counter is fooled) and
1 when rejected, which is the same exit code as a false measurement — a receipt reader cannot
tell "control correctly rejected the stub" from "predicate false". Fix: exit 0 only when the
stand-in is *rejected*, and require a non-empty expectation.

## Low

- **L1 — setup refusals exit 1, not 2.** Docstring (measure.py:40-41) says "2 on
  setup/refusal"; `raise SystemExit('refusing: …')` (:130,135,145,147) exits 1. Observed:
  `refusing: no contract at 000…` → `SETUP_EXIT=1`; missing `--staged` → `1`. A setup refusal is
  therefore indistinguishable from a false predicate. Use `sys.exit(2)`.
- **L2 — `map_dedupe_live` has an undeclared non-emptiness requirement.**
  `measure.py:223`: `… == own_held and own_held`. A package with no already-held document
  (both held rows replaced by new URLs) prints `live_held=0 live_held_agree=1
  map_dedupe_live=0 C3_R43_PASS=false` for a correct tool. Either gate the predicate on
  `own_held` or synthesize a held pair.
- **L3 — the tool publishes `next_free` as a staged id.** Tool:142 `next_free = registry
  max+1` = `S159`, which is a staged id (the live cascade is `S159…S164`); `safe_floor` is
  `S256`. The counter never reads `doc['next_free']` and prints only its own `safe_floor`
  (measure.py:263). A consumer following the advertised `next_free` recreates the cascade.
- **L4 — collision ordering can flap.** `measure.py:185` and tool:108 sort a **set** with a
  numeric key; two ids with the same number (`S153`, `S0153`) order by hash seed. Observed
  across `PYTHONHASHSEED`: `['S153','S0153']` for seeds 0/1/12345, `['S0153','S153']` for 2.
  Counter and tool are separate processes → a transient `live_collisions_agree=0`. Sort by
  `(number, id)`.

## What the counter gets right (so the fixes stay narrow)

Separate process, `-I`, no import of the tool; the registry is snapshotted from git into
`work/` so both parses read identical bytes; the `self_pin` double check (freeze blob *and*
running file) is genuine and caught the mid-wave edit; the URL-branch collision/held
comparison is a real cross-check; the base rev fails closed (`tool_absent=1 tool_sha_ok=0 …
PASS=false`); the predicate is exit-gated and prints every field; `map_dedupe_live` does
exercise the held→registry dedupe branch end to end (`dedupe {'S153':'S105','S154':'S106'}`
came back from the repaired tool).

## Residual risk and verification gaps

- HEAD-state claims (`safe_map_admitted` would be 1; H1's arithmetic admission) come from
  running the HEAD **tool** against a git-extracted registry and the live staged file, not from
  a counter run at HEAD (I am bounded to base and freeze). The counter at HEAD could still fail
  on something I did not launch.
- The staged package is a live external file (`sha256 020fbeaa…`, mtime 2026-10-24 23:33, read
  07:5x); my probes used byte copies except where the tool was run directly on it. The deciding
  run's package may differ.
- I did not probe the `whole_set` path (a map covering every staged row); `MutC3Selftest`
  already reports one survivor there (M4), and this review did not add to it.
- No `lsp` device is mounted in this seat (only aseprite/blender/godot/tripo/unity MCP), so no
  server covered these Python files: every caller/definition claim above is line-cited from
  the bytes, not from a language server. Noted rather than substituted.

## Reproductions (all under `/tmp/tameshi-r43-RevC3Counter/`, deleted after this report)

```
git -C LANE show 17f6ef0c…:corpus/SOURCES.md            > SOURCES.md
git -C LANE show 17f6ef0c…:tools/staged-id-guard.py     > tool_pinned.py     # 8140945a…
git -C LANE show HEAD:tools/staged-id-guard.py          > tool_head.py       # efa5f129…
# B1: two-entry valid-id map → 'map has a target that is not an S-id'
# H1: {S153..S158 → S256..S261} → admitted, dedupe {}
# H2: measure.py --rev FREEZE --freeze FREEZE --tool-file substitute_col0_v2.py → PASS=true
# H3: package copy with '\t| S153 |' → live_collisions=5, agree=1
# H4: tool copy returning naive_map={} cascade=['S159'] → naive_map_refused=1, live_cascade=1, PASS=true
# M2: S153 source cell ' see above. ' (join-repaired tool) → live_unmapped=0, PASS=true
# M3: S153 source cell = S032's path key → live_held_agree=0
# M5: --control with a collision-free --staged → CONTROL_PASS=true, EXIT=0
```
