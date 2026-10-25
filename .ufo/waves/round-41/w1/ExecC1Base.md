# ExecC1Base — C1 calibration counter at the base revision (before receipt)

Seat: `L1Tameshi41.ExecC1Base` (read-only). Lane checkout not modified; the only lane file
written is this report. Scratch work under `/tmp/tameshi-r41-ExecC1Base-*`.

## Exact command

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046
```

Run from the fleet root (`/home/vgpnk/Projects/shokunin`); absolute paths throughout. This is the
allowed `--rev <base>` control run, **not** the deciding run.

## stdout (verbatim, three lines, stderr empty)

```
MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 107
MISMATCH m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10) (no round-41 correction)
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=a3d6c690bcbf8914551d4f4e8e1612784c1c2046 C1_R41_PASS=false
```

stdout sha256: `37608516ba5691179015973fa5b9f150ec39e34e9251cfdba10ad6d529472467`
(two independent runs, byte-identical). The three-line block above **is** the measured
artifact: extracting report lines 18-20 reproduces 304 bytes and that exact sha
(`cmp` against `/tmp/tameshi-r41-ExecC1Base-before.stdout` → `BYTE_IDENTICAL`), so the receipt
verifies from the report body alone, with no scratch or `/tmp` dependency.

## exit code

```
1
```

Appended by the harness as `EXIT=1` after `; echo "EXIT=$?"`.

## Agreement with the frozen contract

The observed line matches `claims.C1.before` exactly:
`m6=1 m9=1 total=2 C1_R41_PASS=false at the base revision`
(`.ufo/evidence/round-41/contract.json`). `records=0` is expected at the base revision:
`corpus/lessons/round-41.md` is absent (`git cat-file -e a3d6c690…:corpus/lessons/round-41.md` →
exit 128) and `SCORECARD.md` / `LOG.md` carry no `## Round 41` / `## 2026-10-25 — round 41`
section (both `grep -c` → 0), so `round41_records()` returns no parts and m7/m8 are vacuous here.

## Retained evidence (re-checked, not asserted)

| Check | Command | Result |
|---|---|---|
| counter pin matches `claims.C1.counter_sha256` | `sha256sum .ufo/evidence/round-41/calibration/measure.py` | `f00917ddd7b519f0eb631f8a11dcc9bbcdcdfa0de9cbbb62639431f5794cb0c2` — identical to the frozen pin |
| base revision resolves | `git rev-parse a3d6c690…` | `a3d6c690bcbf8914551d4f4e8e1612784c1c2046` (2026-10-24T22:50:09-03:00, "round-40 verifier spot-check (integrator, hyaku): non-author admit/reject") |
| registry size / highest id | row scan of `corpus/SOURCES.md` at base with the counter's own `S_ROW_RE` | 107 rows, max `S152` |
| registry statuses | same scan, **status column 8** of the 11-column row | `mined 79 · queued 22 · rejected 6` (= 107) |
| m6 source | `SCORECARD.md:1851` (last `\| sources-registry \|` line at base) | `→ 103 rows at round 35 …` vs 107 → mismatch, 103−107 = −4 |
| m9 table vs prose | `corpus/lessons/round-40.md:73`; table rows 55–67 | table `quarantine_counts()` = `(1, 6, 10)`; prose `quarantine_summary()` = `(1, 7, 9)` ("One row adopted, seven refused … nine present") |
| snapshot pins | `sha256sum .ufo/evidence/round-41/sources/{ast,pathlib}.html` | `183a4f8c…5317` and `0044cae6…f093` — both match the briefed facts |
| contract untouched | `sha256sum .ufo/evidence/round-41/contract.json` | `058f43932f5376d6ef47b025e2e5b6898942e8a7f7628cc8a3ba4acf718442f2` (read-only this seat) |
| lane tree untouched | `git status --porcelain` | only `?? .ufo/evidence/round-41/sources/` and `?? .ufo/waves/round-41/` — pre-existing sibling artefacts, not mine |

## Finding the L1 needs before the one deciding run — m7 reads the wrong column

`measure.py:137` builds the registry map from `cells[9]`:

```
137:        status = cells[9].strip() if len(cells) > 9 else ''
```

But the registry header (`corpus/SOURCES.md:10`) is
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`,
i.e. after `line.split('|')` the **status** cell is index **8** and index **9** is the **`opened`
date**. Verified by importing the counter's own `registry()` against the base registry:

```
S001 -> '2026-10-19'   S005 -> '2026-10-19'   S152 -> '2026-10-24'
mined count per registry(): 0        (the real column holds 79 mined)
```

`measure.py:234` then tests `status != 'mined'`, so **every** S-id cited in a round-41 record is
reported as unmined, whatever its real status. Reproduced end-to-end on a scratch extraction of
the base tree; both variants carry the same two legitimate edits and differ only in whether the
lesson cites an S-id. The full recipe, so the evidence does not depend on `/tmp` surviving:

```
BASE=a3d6c690bcbf8914551d4f4e8e1612784c1c2046; LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
for v in A B; do mkdir -p /tmp/tameshi-r41-ExecC1Base-sim$v
  git -C $LANE archive $BASE | tar -x -C /tmp/tameshi-r41-ExecC1Base-sim$v; done
# both variants, edit 1: in SCORECARD.md, the last `| sources-registry |` row
#   "→ 103 rows at round 35"  becomes  "→ 107 rows at round 35"
# both variants, edit 2: create corpus/lessons/round-41.md stating, verbatim, that the
#   round-40 lesson "closes with a prose summary claiming seven refused and nine present.
#   Its own verdict table lists ten source rows: one adopted, **six refused** and **ten
#   present**"   (satisfies measure.py:249-255: "round-40" + "six refused" + "ten present")
# variant A only, edit 3: append the line "S152 is a mined row."  (variant B cites no S-id)
python3 $LANE/.ufo/evidence/round-41/calibration/measure.py \
  --lane /tmp/tameshi-r41-ExecC1Base-sim$v --rev work
```

Scratch is `/tmp/tameshi-r41-ExecC1Base-*` and therefore volatile by construction (no round-35
scratch is referenced anywhere in this report). Observed outputs:

| Sim | Difference | Counter stdout at `--rev work` | Exit |
|---|---|---|---|
| A | lesson cites **mined** `S152` | `MISMATCH m7 S152 cited but status=2026-10-24` then `m6=0 m7=1 m8=0 m9=0 total=1 records=1 sources_rows=107 … C1_R41_PASS=false` | 1 |
| B | identical lesson, **no S-id cited** | `C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=1 sources_rows=107 rev=work C1_R41_PASS=true` | 0 |

Consequences for the deciding run, stated plainly:

- C1's `target` (`total=0`, `C1_R41_PASS=true`) is reachable **only if no round-41 record cites a
  single S-id** — m7 is satisfied vacuously, not by agreement, which contradicts the class
  definition "a round-41 record cites an S-id the registry does not hold as **mined**".
- Any S-id citation in `corpus/lessons/round-41.md`, the `## Round 41` SCORECARD section or the
  `## 2026-10-25 — round 41` LOG section — including `S152`/`S132`, the ids this round's own
  correction discusses — forces `m7≥1` and `C1_R41_PASS=false` regardless of registry truth.
- The fix is one character of index (`cells[8]`), but the counter is byte-pinned by
  `claims.C1.counter_sha256`, so correcting it is a contract/freeze decision for the L1, not a
  seat edit. This seat made no such edit.

Everything else in the counter behaves as its contract says: m6 is a genuine standing-row drift
(103 vs 107), m9 is the genuine round-40 prose/table contradiction, and the m9 clear condition
(`measure.py:249-255`) is the literal triple `round-40` + `six refused` + `ten present` in
`corpus/lessons/round-41.md` — sim B satisfies it.

## Scope discipline

- No `--rev work` run against the live lane, no tip run, no `--control`, no `--selftest`; the
  single deciding run stays with the L1. Only `--rev a3d6c690…` and scratch
  `--rev work` on `/tmp/tameshi-r41-ExecC1Base-sim{A,B}`.
- No lane checkout edit, no jj/Git index touch, no sibling lane touch.

## Tooling

No install or upgrade (nothing needed; `python3`, `git`, `sha256sum` present). pacman untouched
per the host-wide pause.

## Risks / blockers

None for this receipt. The m7 column defect above is the material risk for the deciding run and is
reported, not remediated.

Report: .ufo/waves/round-41/w1/ExecC1Base.md
