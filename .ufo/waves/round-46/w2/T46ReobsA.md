seat: T46ReobsA
item: independent C1 re-observation at the content revision `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` of `sources-registry`, `depth`, `calibration` — ran each frozen argv once in a scratch clone, re-derived the standing claim with the counter's own `last_rows`/`claim_of`, and read the restated What/First (cap) and Rule/Commit/Round (axis) cells

Round 46, wave 2, C1 calibration seat. I did not write the standing rows, the statements list, the counter or wave 1's observations. Read-only on the lane: the only file I wrote is this report. All scratch under `/tmp/tameshi-r46-T46ReobsA/`. No pacman, no tool installed, no git/jj mutation in the lane, the fleet repo or any sibling lane.

## Setup (exact commands, all in this shell)

```
W=/tmp/tameshi-r46-T46ReobsA; mkdir -p $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ "$b" = tameshi-shokunin ] || ln -sfn $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone && git -C $W/clone checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin && git -C $W/fleet/tameshi-shokunin checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
```

Verification output:
```
clone=6f2168e028ce7ff6e82ac92093ac05dd1f147c32
mirror=6f2168e028ce7ff6e82ac92093ac05dd1f147c32
fleet_count=21
a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9  $W/clone/.ufo/evidence/round-46/calibration/statements.json
a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9  <lane>/.ufo/evidence/round-46/calibration/statements.json
```
(`stmts_pin` hash equals the contract's `statements_sha256` and `measure.py:STATEMENTS_SHA256`.)

All three statements have `"cwd": "clone"`, `"sha_file": null` — so the `git -C $W/clone show HEAD:<file> | sha256sum | cut -c1-12` line applies to none of them (nothing to print; stated rather than silently skipped). `REV=6f2168e028ce7ff6e82ac92093ac05dd1f147c32` in the env for every run. The `six-leg regression ledger` statement (the only `cwd: mirror` one) is not mine.

## Observations (each frozen argv run once; cwd `$W/clone`)

1. `sources-registry` — `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh`
```
exit=0 wall_ms=148 stderr_bytes=0 lines=41
head -3:  == A rows / 120 / == A malformed (must be 0)
tail -2:  == VERDICT / SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)
```
2. `depth` — `bash -c 'git show "$REV:tools/mutate-and-run.sh" | python3 -c …'`
```
exit=0 wall_ms=12 stderr_bytes=0
recorded_cases=9 depth_score=9
```
3. `calibration` — `python3 .ufo/evidence/round-21/coldread/measure.py --repo $W/clone --rev 6f2168e…`
```
exit=0 wall_ms=30212 stderr_bytes=0 out_lines=1889
score= 6        # json.load(...)['calibration_restraint_score']
```

Picked lines re-derived with the counter's own `pick_line` on the captured bytes (not by eye):
```
sources-registry pick='rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)'
depth            pick='9'      (obs regex `depth_score=(\d+)` matches exactly 1 line)
calibration      pick='6'      (obs 'monitor': json.loads(stdout)['calibration_restraint_score'])
census anchors: '^== A rows$' x1, '^SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)$' x1
```

Run-to-run identity, `calibration` only (an extra repeat run, beyond the single required run, to test the statement's stability; both runs are the same clone, same live fleet):
```
sha256sum $W/cal.out $W/cal2.out
e4e0ca2d8e85862483abd0f33c7dd2370035e01a196b0c52017d07f036b8e44e  cal.out
e4e0ca2d8e85862483abd0f33c7dd2370035e01a196b0c52017d07f036b8e44e  cal2.out
```

## Standing claim, read from the CONTENT revision with the counter's own functions

```
cd <lane> && python3 - <<'E'
import importlib.util, json, subprocess
spec = importlib.util.spec_from_file_location('c1','.ufo/evidence/round-46/calibration/measure.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sc = subprocess.run(['git','-C','<lane>','show','6f2168e…:SCORECARD.md'],capture_output=True,text=True).stdout
rows = m.last_rows(sc)
stmts = {s['id']: s for s in json.load(open('.ufo/evidence/round-46/calibration/statements.json'))['statements']}
for sid in ('sources-registry','depth','calibration'):
    s=stmts[sid]; print(sid, m.claim_of(s, rows.get((s['kind'],sid))))
E
```
Output:
```
sources-registry claim=('rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)', '0')
depth            claim=('9',)
calibration      claim=('6',)
n_cap_rows=22 n_axis_rows=3
```
The winning rows are SCORECARD.md:2176 (cap, 4 cells), :2198 and :2199 (axis, 5 cells) — the round-46 block, which is the last in file order for each id (the base-era rows at :1609/:1536/:1537 and the earlier blocks at :240/:1514/:1851/:1993/:2020/:2081/:2146/:2164 are superseded by `last_rows`).

Pin facts observed read-only at REV (context, not a verdict):
```
self_pin= 1                        # sha256(git show REV:.ufo/evidence/round-46/calibration/measure.py) == sha256(worktree file)
stmts_sha= a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9
append_only= 1 base_bytes= 207916 rev_bytes= 225496
```

## Per-statement result

| id | kind | claimed (as `claim_of` parses it) | observed | verdict |
|---|---|---|---|---|
| sources-registry | cap | `('rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)', '0')` | `('rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)', '0')`, exit 0 | **MATCH** |
| depth | axis | `('9',)` | `('9',)`, exit 0 | **MATCH** |
| calibration | axis | `('6',)` | `('6',)`, exit 0 | **MATCH** |

Programmatic equality (same script, `claim == obs`): `sources-registry True`, `depth True`, `calibration True`.

## Cell review — do the restated cells still describe the capability?

**sources-registry (cap, SCORECARD.md:2176)**
```
What:  curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated
First: fleet round 1 (kaika)
```
- `First` is corroborated, not invented: SCORECARD.md:240 (fleet round 1 / kaika block, K2 = "`sources-registry`: opened, tiered, rechecked source rows that mine into admitted entries") and LOG.md:551 ("fleet round 1 closes (kaika continuation…)"), with the census script itself carrying the header `# SOURCES census v2 (fleet round 1, kaika)`. Accurate.
- `What` matches what the frozen command actually gates *structurally*: `sources-census-v2.sh` checks 13-field rows, tier ∈ {A,B,C}, status ∈ {queued,mined,rejected}, kind enum, tier-inflation, duplicate ids, that every mined row's used-by path exists, and that it cites the row id or the source path token. It does **not** observe "opened" (that the source was fetched) or "rechecked" (a recheck cadence) — see F3 (INFO). The wording is carried unchanged from the base row (SCORECARD.md:2164: "curate opened, tiered and rechecked rows, mined into admitted entries, census-gated"), so the restatement did not introduce the gap.

**depth (axis, SCORECARD.md:2198)** — an axis row has no What/First; the analogous cells are:
```
Rule:   One point per recorded mutation case in the runner's ledger comment (`tools/mutate-and-run.sh:87-95`, nine legs), capped at 10; command D prints `recorded_cases=9 depth_score=9` (`before/no-harm-at-base.stdout`, `after/no-harm.stdout`)
Commit: round-46 content revision (deciding receipts `.ufo/evidence/round-46/after/`)
Round:  26 (held)
```
- The Rule cell is exact against the repo: `git show REV:tools/mutate-and-run.sh | grep -nE '^#   (js|bash)-…'` returns nine lines at 87–95 (first `87:#   js-kimi-census …`, last `95:#   js-cite-check …`), and command D printed `recorded_cases=9 depth_score=9`. The cited `before/no-harm-at-base.stdout` resolves and reads `NOHARM commandD recorded_cases=9 depth_score=9 ok`. The second citation `after/no-harm.stdout` does not exist at REV — see F2.
- `Round: 26 (held)` is corroborated by the round-26 block: SCORECARD.md:1308 `| C1 ninth recorded case | depth | recorded_cases=8 … | recorded_cases=9 … |`. No `| depth | 8` row exists anywhere in the file, so the 7→9 jump is only explained by that round-26 block, which does explain it.
- `Commit` now names the round-46 content revision; I measured 9 at that revision, so the claim of measurement there is true, but its receipt pointer is empty at REV (F2).

**calibration (axis, SCORECARD.md:2199)**:
```
Rule:   Restraint score of the strict cold-read monitor … (`calibration_restraint_score`; `box3_full_page=false`, 60 of 64 sections credited): two points per restrained, evidence-linked `[~]` SHONEN box; box 3 is not credited. The round-31 table above stated 8; the monitor prints 6 at the round-46 base, so 8 was a stale standing value
Commit: round-46 content revision
Round:  46 (restated 8 → 6; no raise claimed)
```
- The scoring rule is accurate against the implementation: `.ufo/evidence/round-18/measure.py:682` `restraint = 2 * sum(len(marks) >= b and marks[b-1] == '~' for b in (1,2,4)) + 2 * box3_points`, and `box3_points = box3_marked and box3_link and cr['box3_full_page']`. Observed `shonen: boxes=4, asserted=4, marks=["~","~","~","~"], box3_marked=true, box3_ledger_link=true, box3_points=false` → 3 credited boxes × 2 = 6. `box3_full_page=false` in both my runs. Correct.
- "The round-31 table above stated 8" is correct: the base standing axis table is headed `### Current axes — re-stated at round 31` (base SCORECARD.md:1528) and its calibration row (:1537) scored 8.
- `Round: 46` is right for a value change this round.
- **`60 of 64 sections credited` is false at REV** — the row's own command prints 55 of 64 there. See F1.

## Findings

### F1 — HIGH — the restated calibration row states a section count its own frozen command contradicts at REV
Attacks: SCORECARD.md:2199 (the deciding `calibration` standing row) and, indirectly, the C1 claim that "the last standing row of each statement states what the statement's frozen command prints at REV".
Command (same scratch clone, same live fleet, only `--rev` differs):
```
python3 .ufo/evidence/round-21/coldread/measure.py --repo $W/clone --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
python3 -c "import json;c=json.load(open('cal.out'))['coldread'];print(c['sections_covered'],c['sections_total'])"
  -> 55 64
python3 .ufo/evidence/round-21/coldread/measure.py --repo $W/clone --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d
python3 -c "import json;c=json.load(open('cal-base.out'))['coldread'];print(c['sections_covered'],c['sections_total'])"
  -> 60 64
```
So `60 of 64` is the **base**-revision value (true there, re-measured by me) written into the row that stands at REV, where the value is `55 of 64`. Five sections are credited at base and uncredited at REV; their veto reasons at REV name inputs, and for each of the five at least one named input is a file the round's record commits changed:
```
## Standing rules            input-drift:.ufo/evidence/round-18/measure.py;input-drift:LOG.md;input-drift:PROVINCE.md;input-drift:SCORECARD.md;input-drift:SHONEN.md;input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:corpus/knowledge/closeout-r11.md;… (string longer than my 768-byte capture)
## Mutation-sweep recipe …   input-drift:LOG.md;input-drift:PROVINCE.md;input-drift:SCORECARD.md;input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:corpus/knowledge/closeout-r11.md;input-drift:corpus/knowledge/survivor-fixture-minimization.md;input-drift:reports/round-1-calibration.md;… (truncated)
## Kill-rate bands …         input-drift:PROVINCE.md;input-drift:PROVINCE.md;input-drift:corpus/knowledge/mutation-case-kagi-census.md
## Restore discipline …      input-drift:corpus/README.md;input-drift:corpus/README.md;input-drift:tools/mutate-and-run.sh
## Cross-language divergence input-drift:PROVINCE.md
## Third case …              input-drift:PROVINCE.md
### The service's limits …   input-drift:PROVINCE.md;input-drift:PROVINCE.md;input-drift:tools/mutate-and-run.sh
```
Each of the five flipped sections names at least one input that `git diff --name-only 683eedd 6f2168e` shows changed (`LOG.md`, `PROVINCE.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/*`); `tools/mutate-and-run.sh`, `SHONEN.md` and `.ufo/evidence/round-18/measure.py` are named in some reasons but are **not** in that diff, so those drifts predate the round and are not attributable to it.
Mechanism (so this is not a flake): `.ufo/evidence/round-18/measure.py:input_failures` hashes each ledger entry's input **at `rev`** (`cat_file_blob(repo, rev, path)`) against the hash recorded in the ledger; `covered = credited > 0 and not vetoes` (:641). The section count is therefore a rev-content function that decays as each round appends to `PROVINCE.md`/`SCORECARD.md`/`corpus/*` — the same failure mode C1 exists to catch ("older stated values drift", contract C1.type), reintroduced inside the restated row itself.
Why C1 does not see it: `claim_of` for `kind == 'axis'` compares only `cells[1]` (the integer), so prose numbers in the Rule cell are outside the predicate. The counter therefore still passes while a stated observation in the deciding row is false. The score integer itself is insensitive to this drift (restraint is computed from SHONEN marks only; `box3_full_page=false` at both revs, so 6 at both) — which is why the drift is silent.
Not BLOCKING: `total` is unaffected (claimed `6` == observed `6`); no counter field moves. But a reader of the standing row at REV is told 60 sections are credited when 55 are.

### F2 — LOW — the depth row cites a receipt directory that does not exist at REV
Attacks: SCORECARD.md:2198, Rule cell (`` `after/no-harm.stdout` ``) and Commit cell ("deciding receipts `.ufo/evidence/round-46/after/`").
```
git -C <lane> ls-tree -r --name-only 6f2168e… -- .ufo/evidence/round-46/after .ufo/evidence/round-46/before
  -> only the seven before/* files (c1/c2/c3 .stdout+.exit, no-harm-at-base.stdout); no after/ entry
git -C <lane> cat-file -t 6f2168e…:.ufo/evidence/round-46/after
  -> fatal: path '.ufo/evidence/round-46/after' exists on disk, but not in '6f2168e…'
ls -la <lane>/.ufo/evidence/round-46/after
  -> total 0   (directory exists on disk and is empty)
```
The other citation in the same cell, `.ufo/evidence/round-46/before/no-harm-at-base.stdout`, resolves and prints `NOHARM commandD recorded_cases=9 depth_score=9 ok`. Per the contract's `landing_rule` a receipts-only commit follows the deciding runs, so this is a forward reference rather than a lost artifact — but at REV the pointer is unresolvable and the path is written without its `.ufo/evidence/round-46/` prefix (`after/no-harm.stdout`), which no reader can resolve on its own.

### F3 — INFO — the sources-registry What cell claims two things the frozen command does not observe
Attacks: SCORECARD.md:2176 What cell ("opened, tiered, rechecked source rows, mined into admitted entries, census-gated").
`git show REV:.ufo/evidence/kaika-round-1/sources-census-v2.sh` shows the command proves row count (120), 13-field shape, tier ∈ {A,B,C}, status ∈ {queued,mined,rejected}, kind enum, no tier-inflation (A+community), no duplicate ids, mined used-by path existence, and id-or-path citation (B2; B1 id-cite is printed as informational). It does not check that a source was fetched ("opened") or that a recheck happened ("rechecked"). The wording is identical to the base row (:2164), so this is inherited, not introduced by the restatement; `census-gated` keeps it from being a strong overstatement. No action implied for C1.

### F4 — INFO — the sources-registry claim is a live row count that moves with every registry append
Attacks: SCORECARD.md:2176 evidence cell (`rows=120`).
```
git show 683eedd:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  -> 117
git show 6f2168e:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  -> 120
git show 6f2168e:corpus/SOURCES.md | grep -E '^\|[[:space:]]*S2(58|59|60)[[:space:]]*\|' -> S258, S259, S260 present
```
The +3 is exactly the three rows wave 1 opened, and the restated cell's 120 is correct at REV. The claim is nonetheless only valid while `corpus/SOURCES.md` is byte-stable: any later append before the deciding run turns this row into a MISMATCH. (Contrast `depth`, whose input `tools/mutate-and-run.sh` is unchanged across base..REV.)

### F5 — differences from wave 1's observation of the same statements (`.ufo/waves/round-46/w1/ExecStmt01.md`)
Reported because the wave-2 brief makes any difference a finding. All three are differences in *observation*, explained by the records commit, and none is a regression:
1. `sources-registry`: wave 1 (at freeze `745a583`) recorded `claimed=-` / **UNPARSED**, with three named defects — arrow order (`→ exit 0, `line`` vs the required `→ `line`, exit N`), pipe misalignment (7 pipes → 6 cells, `cells[3]` = `S[0-9]{3} \`), and a stale count (`99 rows at round 35`). At CONTENT the row is 4 cells, arrow-ordered, and claims 120 — **MATCH**. All three wave-1 defects are gone.
2. `sources-registry` observed value moved `rows=117` (wave 1) → `rows=120` (mine), exactly the three rows wave 1 added (F4). Not a disagreement; a real content change between the two revisions.
3. `calibration`: wave 1 `claimed=8 observed=6` **MISMATCH** → at CONTENT `claimed=6 observed=6` **MATCH**. The value 6 itself did not move (wave 1's stdout sha `5d352f12cc1e…` at freeze vs my `e4e0ca2d…` at CONTENT differ because the monitor embeds rev-dependent section records; the picked scalar is 6 in both).
4. `depth`: **MATCH** at both revisions, value 9 in both. The row's Rule/Commit cells were rewritten (base: "command D above prints …", commit "round-31 measurement revision (measured-result row below)"; CONTENT: receipt citations and "round-46 content revision"), which is where F2 comes from.

## Not run (deliberately, out of seat scope)

- The deciding run of `measure.py --lane … --rev … --base … --work …`: the L1's, per the measurement bounds. I did not run it, nor `--emit`, nor `--selftest`; the committed `selftest/c1-selftest.stdout` at REV was not re-run.
- The C2 and C3 counters, `no-harm.sh`, and any build/lint/format gate: not my item; the parent owns post-integration gates.
- No git/jj mutation of any kind in the lane, the fleet repo or a sibling lane: only `git clone`/`checkout` under `/tmp/tameshi-r46-T46ReobsA/` plus read-only `git show`/`ls-tree`/`cat-file`/`diff --name-only`/`rev-parse` against the lane.

## Tooling

None installed or upgraded (nothing was missing for this item).
