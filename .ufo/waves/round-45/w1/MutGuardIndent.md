seat: MutGuardIndent

# staged-id guard indent proof — 0-3-space extractor is load-bearing

Tool: `tools/staged-id-guard.py` (sha256 `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8`).
Scratch: `/tmp/tameshi-r45-MutGuardIndent/`. No tool installs (operator 2026-10-19: none needed).

## Verdict

**Mutant killed.** The single-line mutant `ROW_RE: '^ {0,3}\|…' → '^\|…'` (tool line 65, the only
line that differs) flips the guard from *catching* the indented S202 collision
(`collisions: ["S202"]`) to a silent false green (`collisions: []`, `collision_count: 0`, still
`exit=0`, `verdict: "answered"` — no error signal). Same fixture bytes both sides.

## Fixtures (scratch, 11 columns/row)

`reg-indent.md` — column-0 S001 + INDENTED (2-space) S202:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
| S001 | https://example.test/alpha | docs | A | alpha guide | "Alpha guide" | reading alpha pages | held | 2026-10-25 | 180d | w1 |
  | S202 | https://example.test/beta | docs | A | beta guide | "Beta guide" | reading beta pages | held | 2026-10-25 | 180d | w1 |
```
sha256 `27ac08c60527392a3f4a5aa6081753d1f514809b17e7aa6f69237db6dc8dbf51`

`staged-202.md` — S202 with a DIFFERENT URL (column-0):

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
| S202 | https://example.test/beta-v2 | docs | A | beta guide v2 | "Beta guide v2" | reading beta pages v2 | queued | 2026-10-25 | 180d | w1 |
```
sha256 `11f47f7812815cf2f441af1e76bbeeee86c349a407c6567c7f41efe9ccaca051`
(`staged-202-indent.md` = same row indented 2 spaces, for the `column0_miss` probe.)

## RUN1 — pristine tool, indented registry collision: CAUGHT

```
$ python3 -I /…/tameshi-shokunin/tools/staged-id-guard.py --registry reg-indent.md --staged staged-202.md --json
exit=0
{"cascade": [], "cascade_count": 0, "collision_count": 1, "collisions": ["S202"], "column0_collisions": ["S202"],
 "column0_miss": [], "extractor": "0-3space", "held": {}, "naive_map": {"S202": "S203"}, "next_free": "S203",
 "refused": false, "registry_docs": 2, "registry_max": "S202", "registry_rows": 2, "registry_sha256": "27ac08…",
 "safe_floor": "S203", "staged_max": "S202", "staged_rows": 1, "staged_sha256": "11f47f…", "unmapped": [],
 "verdict": "answered"}
```
S202 is in `collisions`: the 0-3-space ROW_RE (`tools/staged-id-guard.py:65`) parsed the indented
registry row. (Registry side is indented here, so `column0_miss` — computed over the *staged* text —
is `[]`; the field-level proof is RUN7.)

## RUN2 — selftest control

```
$ python3 -I tools/staged-id-guard.py --selftest
exit=0
STAGED_ID_GUARD_SELFTEST: cases=24 failed=0
VERDICT: PASS
```

## RUN3 — mutant (column-0-only pattern): FALSE GREEN

Mutant copy `/tmp/tameshi-r45-MutGuardIndent/staged-id-guard-column0.py`; whole diff vs pristine:

```
65c65
< ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')
---
> ROW_RE = re.compile(r'^\|\s*(S\d{3,})\s*\|')
```

```
$ python3 -I staged-id-guard-column0.py --registry reg-indent.md --staged staged-202.md --json
exit=0
{"…", "collision_count": 0, "collisions": [], "column0_collisions": [], "column0_miss": [], …,
 "registry_docs": 1, "registry_max": "S001", "registry_rows": 1, …, "refused": false,
 "safe_floor": "S203", "staged_max": "S202", "staged_rows": 1, …, "verdict": "answered"}
```
S202 dropped out of the registry parse entirely (`registry_rows` 2→1): the guard green-lights
appending a package whose S202 collides with a held registry row. Full outputs: `run1-pristine.json`,
`run3-mutant.json` in the scratch dir.

## RUN7/RUN8 — staged-side indent: `column0_miss` fires, mutant blind

```
$ python3 -I tools/staged-id-guard.py --registry reg-indent.md --staged staged-202-indent.md --json
→ {"collisions": ["S202"], "column0_collisions": [], "column0_miss": ["S202"], "verdict": "answered", "staged_rows": 1}  exit=0
$ python3 -I staged-id-guard-column0.py … same inputs
→ {"collisions": [], "column0_collisions": [], "column0_miss": [], "verdict": "answered", "staged_rows": 0}  exit=0
```
`column0_miss: ["S202"]` is the tool's own indent-proof field — matches the committed receipts
`.ufo/evidence/round-45/assimilation/guard-proof-collisions` (`S002`) /
`guard-proof-column0-collisions` (empty).

## RUN4 — real files + committed adoption-map: ADMITTED

```
$ python3 -I tools/staged-id-guard.py --registry /…/corpus/SOURCES.md \
    --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md \
    --map .ufo/evidence/round-45/assimilation/adoption-map.json --json
exit=0
{"analysis_refused": true, "cascade": ["S161"…"S168"], "cascade_count": 8, "collision_count": 8,
 "collisions": ["S153","S154","S155","S156","S157","S158","S159","S160"], "column0_miss": [],
 "held": {"S153":"S105","S154":"S106","S159":"S155","S160":"S156"},
 "map_dedupe": {"S153":"S105","S154":"S106","S159":"S155","S160":"S156"},
 "map_entries": 10, "map_floor": "S256", "map_ok": true, "map_reasons": [],
 "naive_map": {"S153":"S161",…,"S160":"S168"}, "next_free": "S161",
 "registry_rows": 115, "registry_max": "S160", "registry_docs": 100, "safe_floor": "S256",
 "staged_rows": 103, "staged_max": "S255", "unmapped": [], "verdict": "admitted"}
```
Reproduces the committed `guard-map.json` / `guard-map.exit`=0 exactly (115/103 rows, 8 collisions,
4 held, floor S256, S202→S256 / S203→S257 admitted).

## RUN5/RUN6 — refused maps: INADMISSIBLE

```
$ … --map .ufo/evidence/round-45/assimilation/refused-map-identity.json --json
exit=1   "map_ok": false, "map_staged_clash": ["S202","S203"],
         "map_reasons": ["map targets are still staged ids: S202,S203"], "verdict": "inadmissible"
$ … --map .ufo/evidence/round-45/assimilation/refused-map-next.json --json
exit=1   "map_ok": false, "map_staged_clash": ["S161","S162"],
         "map_reasons": ["map targets are still staged ids: S161,S162"], "verdict": "inadmissible"
```
Both reproduce the committed `refused-map-identity.{out,exit}` / `refused-map-next.{out,exit}`.

## Restoration evidence

Lane tool and both real inputs byte-identical before/after every run (mutant lives only in scratch):

```
before: 03a796c5… tool | d1a40043… SOURCES.md | 020fbeaa… SOURCES.append.md
after:  03a796c5… tool | d1a40043… SOURCES.md | 020fbeaa… SOURCES.append.md
diff hashes-before.txt hashes-after.txt → identical (HASHES-IDENTICAL)
```
No writes to the lane, the read-only package, jj state, or the Git index; no campaign counter run
beyond `--selftest`/guard invocations (measurement bounds respected).
