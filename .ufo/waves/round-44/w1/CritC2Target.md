# CritC2Target — C2 target reachability (do-nothing control + staged collision evidence)

Role: UFO-FSD critic. Attack on the C2 counting target, not on the claim owner.
Read-only on the lane; scratch under `/tmp/tameshi-r44-critc2-*` (deleted after).

## 1. Counting command at base / freeze / HEAD

All runs from the lane root, command exactly as in the contract:

```
grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md
```

| rev | result | exit |
|---|---|---|
| base `506e99c7b73c85711f066895984d501fcf7539cd` (`git show 506e99c:corpus/SOURCES.md \| grep -cE ...`) | `0` | 1 |
| freeze `ba01973c73ad7de60e5bd19ae08255a1b7ef917e` (same via `git show`) | `0` | 1 |
| HEAD `8bffd9b` (working tree, exact command) | `0` | 1 |

## 2. Do-nothing control: can any read-only state print 1? No.

Six probes on the HEAD file, all `0`:

```
grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md            # 0
grep -cE '^\| S160 ' corpus/SOURCES.md                  # 0 (column-zero)
grep -cE '^ {1,3}\| S160 ' corpus/SOURCES.md            # 0 (indented 1-3)
grep -cE '\| S160 ' corpus/SOURCES.md                   # 0 (anywhere in line)
grep -cE '^\| S160' corpus/SOURCES.md                   # 0
```

All `S160` mentions in the file are prose, none is a row line:

- `corpus/SOURCES.md:447` — round-42 note: `` (`staged:S159`, `staged:S160`) `` — starts with `Round`;
- `corpus/SOURCES.md:448` — round-42 renumber note: `` `staged:S160` (pitest.org/faq/) → S156 `` — starts with `-`;
- `corpus/SOURCES.md:456` — `` - Next unused id: S160. `` — starts with `-`, not with `|`.

The only shape that matches is a registry row line `| S160 …` with 0–3 leading spaces; none exists at base, freeze, or HEAD. Therefore no do-nothing control can make the grep print 1; the target is reachable only by actually appending a matching line (the intended row). The do-nothing control described in the contract ("with no row appended the grep prints 0") holds.

**Other ids matching the pattern:** none. The pattern pins the literal id `S160` followed by a space; the registry tail ends at `S159` (last row; "Next unused id: S160." at line 456). No existing id (`S001`…`S159`) matches. The next-unused line and the Search-log section (lines 137–250, bullet notes only, no `| S### |` rows) cannot match. The Leads section is bullets only.

## 3. Staged collision evidence — premise correction required

Staged package read (the exact file the guard consumes:
`/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`):

- 103 staged rows, ids **S153–S255** (min S153, max S255).
- **Staged id `S160` exists**: line 14 of the staged file, row `| S160 | Frequently Asked Questions (PIT documentation) — https://pitest.org/faq/ | …` (PIT FAQ).

So the dispatch premise "S160 is not staged (the staged set tops out below S160)" is **factually wrong** against the on-disk staged package: the staged set tops out at S255, and S160 is a staged id.

Read-only guard run at HEAD (`python3 -I tools/staged-id-guard.py --registry …/corpus/SOURCES.md --staged …/merge/tameshi/SOURCES.append.md --json`):

```
collisions: S153 S154 S155 S156 S157 S158 S159   (collision_count 7)
held:       S153→S105, S154→S106, S159→S155
unmapped:   []
safe_floor: 256
registry_max: S159, staged_max: S255, staged_rows: 103, registry_rows: 114
verdict:    refused (exit 1 = no admissible map supplied; not a setup refusal)
naive_map:  S153→S160 … S159→S166 (targets are staged ids — the cascade the guard refuses)
```

Mirror experiment: a copy of `corpus/SOURCES.md` with the S160 draft row (Stryker equivalent-mutants URL, same doc family as S089) inserted before the round-42 hazard note:

- `grep -cE '^ {0,3}\| S160 '` → `1` (as intended);
- guard on the mirror: `collision_count` 7 → 8, `S160` added to `collisions`, but `held["S160"] = "S156"` — staged:S160's document (PIT FAQ, `https://pitest.org/faq/`) is already carried by registry row S156, so it is deduped, `unmapped` stays `[]`, `safe_floor` unchanged.

Conclusion: appending lane row S160 introduces a numeric id overlap with a staged row, but only with a **held** staged row whose document is already in the registry (S156); under the guard's by-document semantics it is not an ambiguous collision, and the S256 safe floor for future partial adoption is unaffected. The C2 landing (grep 0 → 1) does not depend on the staged set.

## 4. Verdict (impacted axes)

- **freshness (C2 target reachability): PASS.** No do-nothing control can print 1; measurement is 0 at base/freeze/HEAD, and only an actual row append flips it to 1. The grep is a faithful "row exists" probe.
- **Claim premise accuracy: factual correction, not rejection.** "S160 is not staged" is false: staged id S160 exists (held, maps to S156). Suggested smallest safe correction to the dispatch/lesson wording: replace "S160 is not staged" with "staged:S160 is held (document already carried as S156); appending lane S160 adds no unmapped staged collision, safe floor S256 unchanged".

## Commands run (evidence)

- `git show 506e99c7b73c85711f066895984d501fcf7539cd:corpus/SOURCES.md | grep -cE '^ {0,3}\| S160 '` → 0 (exit 1)
- `git show ba01973c73ad7de60e5bd19ae08255a1b7ef917e:corpus/SOURCES.md | grep -cE '^ {0,3}\| S160 '` → 0 (exit 1)
- `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` (HEAD) → 0 (exit 1)
- probe battery (column-zero, indented, any-position, col0 prefix) → all 0
- `grep -nE 'S160' corpus/SOURCES.md` → lines 447, 448, 456 only (prose)
- `python3 -I tools/staged-id-guard.py --registry …/corpus/SOURCES.md --staged …/merge/tameshi/SOURCES.append.md --json` (HEAD) → collisions 7 (S153–S159), held S153→S105/S154→S106/S159→S155, unmapped [], safe_floor S256, verdict refused, exit 1
- same guard on mirror registry with S160 row appended → collision_count 8 incl. S160, held S160→S156, unmapped [], safe_floor S256
- `comm -12` (registry ids vs staged ids) → S153–S159 (7)
