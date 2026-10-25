# SentinelIdGuard — round-44 w1

Seat `L1Tameshi44.SentinelIdGuard` (leaf). Read-only guard run; no subagents, no edits to
either input. Report finds with evidence.

## 1. Run

Command (verbatim from the item):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py \
  --registry /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md \
  --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json
```

Exit **1**. Full JSON (sort_keys, whole object):

```json
{"cascade": ["S160","S161","S162","S163","S164","S165","S166"],
 "cascade_count": 7,
 "collision_count": 7,
 "collisions": ["S153","S154","S155","S156","S157","S158","S159"],
 "column0_collisions": ["S153","S154","S155","S156","S157","S158","S159"],
 "column0_miss": [],
 "extractor": "0-3space",
 "held": {"S153": "S105", "S154": "S106", "S159": "S155"},
 "naive_map": {"S153": "S160", "S154": "S161", "S155": "S162", "S156": "S163",
                "S157": "S164", "S158": "S165", "S159": "S166"},
 "next_free": "S160",
 "refused": true,
 "registry_docs": 100,
 "registry_max": "S159",
 "registry_rows": 114,
 "registry_sha256": "c50ca1fbce6b1afb769735793d2ca520d05e5e8a830fd3ea88a7c48fb4c961fd",
 "safe_floor": "S256",
 "staged_max": "S255",
 "staged_rows": 103,
 "staged_sha256": "020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807",
 "unmapped": [],
 "verdict": "refused"}
```

Both sha256 values match the files on disk (`sha256sum` reproduced them exactly). On-disk
hashes and the guard's parse agree, so the refusal is about content, not stale bytes.

## 2. Guard report

- **Verdict: refused** (exit 1; `main` returns 1 for any verdict other than `admitted`/`answered`).
- **Collisions: 7 — S153–S159.** All seven are also `column0_collisions`
  (`^\|\s*S\d{3,}\s*\|`), i.e. census-valid rows, not indented-row blind spots; `column0_miss`
  is empty.
- **Held (doc already registered under another id): S153→S105, S154→S106, S159→S155.**
  Matches the merge report's "Rows whose source the lane's registry already holds" table
  (MERGE-REPORT.md:120-121; staged S159 → registry S155 PIT basic concepts, per round-42
  adoption, SOURCES.md:447).
- **Unmapped: none** (every collision carries a document).
- **Naive map / cascade:** remapping collisions to the registry's top+1..top+7 gives
  S153→S160 … S159→S166; every one of those targets is itself a staged id (staged spans
  S153–S255), so the guard refuses rather than emit a map that would collide on adoption.
- **safe_floor: S256** = `max(registry_max S159, staged_max S255) + 1`; **next_free: S160**
  is registry top + 1 only, and is NOT safe because staged already occupies S160.

## 3. The two confirmations the item asked for — both FAIL

1. **"S160 is not a staged id (the staged set tops out below S160)" — FALSE.**
   The staged set is **S153–S255, contiguous, 103 rows** (SOURCES.append.md; staged_max=S255).
   S160 is a staged row: `SOURCES.append.md:14` is
   `| S160 | Frequently Asked Questions (PIT documentation) — https://pitest.org/faq/ …`.
   The staged set does not top out below S160; it contains S160.
2. **"appending S160 does not collide with any staged id" — FALSE.**
   Appending a registry row `S160` makes the registry∩staged intersection grow from
   {S153..S159} to {S153..S160} — **8 collisions**, and S160 is exactly the new member.
   Additionally, staged S160's document (PIT FAQ, pitest.org/faq/) is already registered as
   **S156** (round-42 adoption, SOURCES.md:447), so staged S160 is a held-class row: once
   S160 becomes a collision, the guard's `held` mechanism maps it to S156. The C2 row S160
   (Stryker equivalent-mutants) and the staged row S160 (PIT FAQ) are different documents
   contesting the same id.

## 4. Id lists

Registry ids (corpus/SOURCES.md, 114 rows): spans **S1–S37, S40–S97, S99–S108, S132,
S152–S159**; max S159; tail ids (last 12 rows):
**S106 S107 S108 S132 S152 S153 S154 S155 S156 S157 S158 S159**.

Staged ids (SOURCES.append.md, 103 rows): **S153–S255** contiguous; tail:
**S244 S245 S246 S247 S248 S249 S250 S251 S252 S253 S254 S255**.

Intersection (before any append): **S153 S154 S155 S156 S157 S158 S159** (7).

## 5. Finding for round-44 C2 (freshness)

The C2 counting command (`grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` → 1 at landing) can
still succeed if the landing commit adds a registry row S160. But that row is *not* safe with
respect to the staged package:

- S160 is already a staged id (SOURCES.append.md:14) for a different document (PIT FAQ);
- the lane's own round-43 "Next unused id: S160" declaration (SOURCES.md:456) therefore
  collides with the staged set, which the guard now makes visible;
- after appending S160, the next staged-adoption round faces an 8-way collision
  (S153–S160), with staged S160 held at S156, and the safe floor for any *new* id stays
  **S256**.

Remediation (for the adopting seat, not this seat): before appending S160, resolve the staged
S160 row — renumber it (safe_floor S256) or drop it as held (doc already at S156) — so the
next assimilation does not hit id S160 twice. No tool install/upgrade was needed; nothing else
was changed.

## 6. Control

`python3 tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`,
`VERDICT: PASS`, exit 0.
