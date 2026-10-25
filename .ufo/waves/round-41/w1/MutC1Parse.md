# MutC1Parse — mutation probe on the C1 counter (m9 tuple, m8 path filter)

Seat: `L1Tameshi41.MutC1Parse`. Base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`; freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937` never measured. Lane checkout untouched (only `/tmp` scratch and this report written). No tool installs or upgrades.

Scratch: `/tmp/tameshi-r41-mutc1parse-OdzXnL` (`measure.orig.py` = working copy, `measure.pristine.py` = byte-identical reference, `measure.mutA.py` = m9 mutant, `lane/` = base files + synthetic round-41 record, `lane-doctored/`, `lane-doctored2/` = round-40 corruption fixtures). Counter copy sha256 `f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2`, matching `.ufo/evidence/round-41/contract.json` `claims.C1.counter_sha256`.

Counter under test: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/calibration/measure.py`
- `quarantine_counts` 149-165, checked return at :165
- `path_tokens` 181-190, prefix/exact gate at :188, append at :189
- m7 loop 228-235, m8 loop 238-241, m9 branch 243-259 (`if table is not None and summary is not None and table != summary` at :248)

## 1. Baseline — pristine counter at base

```
cd /tmp/tameshi-r41-mutc1parse-OdzXnL && python3 measure.pristine.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046
```
```
MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 107
MISMATCH m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10) (no round-41 correction)
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=a3d6c690... C1_R41_PASS=false
exit=1
```
Matches the contract's declared `before`. `records=0` because `corpus/lessons/round-41.md` does not exist at base and neither round-41 head is present in `SCORECARD.md`/`LOG.md`, so m7 and m8 are vacuously 0 at base — the base score exercises neither.

## 2. Mutant A — `quarantine_counts` returns the summary tuple (defeats m9)

Mutation: `measure.py:165` `return adopted, refused, present` → `return quarantine_summary(lesson)`.

```
# base revision
C1_R41: m6=1 m7=0 m8=0 m9=0 total=1 records=0 ... C1_R41_PASS=false      exit=1
# fixture lane (--rev work), pristine for comparison
pristine: m6=1 m7=4 m8=2 m9=1 total=8 records=1 ... C1_R41_PASS=false
mutant A: m6=1 m7=4 m8=2 m9=0 total=7 records=1 ... C1_R41_PASS=false
```

**m9 reads 0 at base — yes.** Total falls 2 → 1; C1_R41_PASS stays false only because m6 (103 vs 107) is a class the mutation does not touch. m7 and m8 are bit-identical.

Strength of the mutant: it is not just a 1-off mask. On `lane-doctored2` (all 17 verdict rows of the round-40 table deleted, prose summary left intact):
```
pristine: MISMATCH m9 ... its table counts (0, 0, 0)
mutant A: m9=0
```
So the mutant silently accepts total loss of the verdict table. It survives every behavioural detector the counter contains, because the only consumer of `quarantine_counts` is the comparison that now compares the summary with itself (`:246-248`). The pinned `counter_sha256` is the sole thing that would catch it; m9 has no `--selftest`/`--control` mode (the C1 counter's argparse has only `--lane/--rev/--fleet`).

Verdict: **survived** (detector blind), **inconclusive only against the pin** — hash equality is the one killing signal, and it is a static check, not behaviour. A seat that edits the counter and reports the new hash would pass unnoticed by the counter itself.

## 3. Mutant B — the m8 path filter

`path_tokens` gate `:186-189` selects backticked tokens starting with `PATH_PREFIXES`/`PATH_EXACT`.

| variant | edit | fixture-lane result |
|---|---|---|
| B1 "admit nothing" (check disabled) | `:182` insert `return []` | `m6=1 m7=4 m8=0 m9=1 total=6` |
| B2 "pass-through" (filter no-op) | delete `:186-188`, keep only `out.append(raw)` | `m6=1 m7=4 m8=5 m9=1 total=11` |
| pristine | — | `m6=1 m7=4 m8=2 m9=1 total=8` |

Effect matrix, verified:
- B1: m8 2 → 0 (class silenced). m7 unchanged (4), m9 unchanged (1).
- B2: m8 2 → 5 — the 2 real unresolvable citations plus 3 false positives on ordinary backticked words (`adopted`, `refused`, `m6`). m7 unchanged (4), m9 unchanged (1).
- At base both variants are observationally inert (`records=0` ⇒ m8 already 0); only the fixture lane has coverage.

**m7 is independent of the m8 path filter in both directions.** `S_CITE_RE` runs over the raw record text at `:229`, never over `path_tokens` output, so no m8 mutation can move m7; conversely the m7 loop cannot move m8. Any claim that one filter "protects" the other class is false.

## 4. Coverage finding inside m7 — the counter mis-reads the registry column

`registry()` reads status from `cells[9]` (`measure.py:137`) and its docstring calls the rows "11-column". Registry rows carry 13 `split('|')` cells: status is `cells[8]`, `cells[9]` is the source date. Counted from the committed base bytes (`corpus/SOURCES.md`, 107 rows):

- `cells[8]`: `mined=79`, `queued=22`, `rejected=6`
- `cells[9]`: 6 distinct values, all dates (`2026-10-19` … `2026-10-24`)

Consequence: `rows[sid]` is always a date, so `status != 'mined'` at `:234` always holds for any cited id. m7 therefore fires on **every distinct S-id cited in a round-41 record**, mined or not. Observed on the fixture lane: `m7 S104 cited but status=2026-10-24`, `m7 S152 cited but status=2026-10-24`. At base this is invisible only because `records=0`.

A sibling seat applied `cells[9]` → `cells[8]` to the live work tree at 2026-10-25 03:40:20 (uncommitted). Verified against the same fixture lane: the fixed counter reads `m6=1 m7=2 m8=2 m9=1 total=6` — m7 drops 4 → 2, leaving only the two genuinely absent ids (`S998`, `S999`) while mined `S104`/`S152` pass. Diagnosis and fix agree.

This is the decisive C1 risk: the contract target is `m7=0` at the measurement revision, which under the pinned counter is reachable only if the three round-41 records cite no S-id at all. The round-40 records cite 20 distinct S-ids in `corpus/lessons/round-40.md` and 1 in its `SCORECARD.md` section; a round-41 lesson and scorecard section that discuss the registry will almost certainly cite some. Either the records avoid S-ids by construction, or C1 cannot reach `total=0` and the counter's pin must be revisited — that is an L1 contract decision, not a seat edit.

## 5. Coverage finding inside m9 — the None shortcut

`:248` requires both `table` and `summary` non-None. Deleting the `### Quarantine` section's prose sentence (the section's tail, `"One row adopted, seven refused …, nine present-but-not-appended."`) makes `quarantine_summary` return `None`; verified on `lane-doctored`: `counts=(0,0,0) summary=None` ⇒ m9 reads 0 with no round-41 correction and with the table already destroyed. So m9 can be silenced by removing evidence from `corpus/lessons/round-40.md` rather than by stating the counts in round-41. Any reviewer of C1 should require the round-40 `### Quarantine` section to still be present and its 17 rows intact, not merely `m9=0`.

The `fixed` gate (`:249-254`) is also count-blind: it accepts the round-41 lesson merely for containing the substrings `round-40`, `six refused`, `ten present`, never comparing them to `table`. Verified on `lane-magic`, where the round-40 table was cut to 4 rows — `counts=(1,2,1)`, `summary=(1,7,9)` — and the round-41 record says only `"round-40 correction: six refused and ten present"`: pristine counter scores `m9=0`. Both numbers are wrong for that table and neither is the table's, so the gate can be satisfied by wording that states nothing true. Independently reproduced by `L1Tameshi41.ReviewC1Counter`.

## 6. Restoration evidence

```
$ sha256sum measure.orig.py measure.pristine.py
f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2  measure.orig.py
f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2  measure.pristine.py
$ python3 measure.orig.py --lane .../lane --rev work | tail -1
C1_R41: m6=1 m7=4 m8=2 m9=1 total=8 records=1 ... C1_R41_PASS=false
$ sha256sum tameshi-shokunin/.ufo/evidence/round-41/calibration/measure.py
f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2
```
Scratch bytes restored to the pin after every mutant; post-restore behaviour equals pre-mutation behaviour (`m7=4 m8=2 m9=1`). Every measurement above ran against counter bytes `f00917dd…` (read at 03:38, hash-verified at 03:39, 03:41, 03:42). The lane counter was `f00917dd…` while this probe ran and the HEAD blob is still `f00917dd…` (`git cat-file -p HEAD:.ufo/evidence/round-41/calibration/measure.py | sha256sum`); a sibling's uncommitted edit changed the work-tree copy to `5ccb42d8…` at 03:40:20 (§4), not mine. `git -C tameshi-shokunin status --porcelain` shows that ` M .ufo/evidence/round-41/calibration/measure.py` plus sibling entries in `corpus/` and `.ufo/`; my only writes are the `/tmp` scratch and this report.

## 7. Fixture rebuild (self-contained; `/tmp` is disposable)

No evidence lives in a `scratch/` tree; everything needed to re-derive §2–§5 is below. `lane/` = `git -C LANE show a3d6c690:<path>` for `corpus/SOURCES.md`, `SCORECARD.md`, `LOG.md`, `corpus/lessons/round-40.md`, plus this literal `corpus/lessons/round-41.md`:

```
# Round 41 — synthetic C1 classifier fixture (mutation probe)

Synthetic record, not lane content. Planted so m7 and m8 both have cases to count.

Mined ids cited: S104 and S152. Duplicate id must count once: S104 S104.
Absent ids cited: S998 and S999.

Resolving paths: `corpus/lessons/round-40.md` and `SCORECARD.md:7`.
Unresolvable paths: `corpus/lessons/round-41-absent.md` and `tools/absent-probe.py`.

Ordinary backticked words that are not paths: `adopted`, `refused`, `m6`.
```

Derivatives, all run with `--rev work` on the copy:
- `lane-doctored`: in round-40.md, replace the span `### Quarantine` … next `\n### ` with `### Quarantine\n\n(table removed by mutation probe)\n` ⇒ `counts=(0,0,0)`, `summary=None`.
- `lane-doctored2`: delete every line matching `^\| S\d{3} \|` from round-40.md, keep all prose ⇒ `counts=(0,0,0)`, `summary=(1,7,9)`.
- `lane-magic`: keep only round-40 table rows `S105, S109, S132, S137` ⇒ `counts=(1,2,1)`, `summary=(1,7,9)`; append to round-41.md `round-40 correction: six refused and ten present (no count of the doctored table is given).`
- `measure.mutA.py`: pristine bytes with `    return adopted, refused, present` → `    return quarantine_summary(lesson)`.

Reported scratch `/tmp/tameshi-r41-mutc1parse-OdzXnL` was intact at 03:44 with `measure.orig.py` and `measure.pristine.py` both at `f00917dd…`. The round-35 tree was relocated, not deleted, in the **`mado-shokunin` lane**: `.ufo/waves/round-35/scratch/` → `.ufo/waves/round-35/scratch-evidence/`, checkpointed by `4efaf63` (235 files / 58 seat dirs at that commit; `261 / 59` at HEAD `1bb25c7`) — `git -C /home/vgpnk/Projects/shokunin/mado-shokunin ls-files .ufo/waves/round-35/scratch-evidence/ | grep -ci mutc1parse` → `0`. This seat has no files under any round-35 path and cites none; its evidence is this report body plus the round-41 `/tmp` scratch.

## Verdict

| mutant | expected detector signal | observed | verdict |
|---|---|---|---|
| A `quarantine_counts` → summary | m9 still 1 at base | m9=0, total 2→1 | survived behaviourally; only the sha256 pin kills it |
| B1 filter admits nothing | m8 stays 2 | m8=0, m7=4, m9=1 | killed by fixture lane (case 1 of the m8 check lost) |
| B2 filter pass-through | m8 stays 2 | m8=5 (3 false positives) | killed by fixture lane; m7 unaffected |

Both assigned mutants move exactly one class and no other. The m8 filter is load-bearing but m7's registry column is off by one and vacuous at base: no round-41 record citing any S-id can score `m7=0` under the pinned counter.
