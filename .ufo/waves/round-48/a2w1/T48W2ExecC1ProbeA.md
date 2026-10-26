# T48W2ExecC1ProbeA — C1 probe, group A

Seat `T48W2ExecC1ProbeA` (executor, round 48 wave 2, attempt 2; L1 `TameshiR48a2`).
Attacked: the round-48 restated standing rows of `SCORECARD.md` section `### Standing self-assessment — re-stated at round 48` at CONTENT `c7586b9a10effc63b4bd327f976edc094c1bdc17` for the five statements **sources-registry, depth, calibration, freshness, mutation sweep runner** (cap rows `SCORECARD.md:2332`, `:2333`; axis rows `:2354`, `:2355`, `:2356` in the file at REV, which is byte-identical to the worktree file since `git diff --quiet c7586b9 -- corpus tools SCORECARD.md` holds).

Read-only on the lane. Deliverables written only under `.ufo/waves/round-48/a2w1/`:
this report, `T48W2ExecC1ProbeA.stdout` (probe stdout), `T48W2ExecC1ProbeA.coldread-rev.json`, `T48W2ExecC1ProbeA.coldread-base.json`.
Nothing installed or upgraded (no pacman/uv/npx/binary channel used). Counter not edited (frozen sha `572a5670…` verified before and after).

## 1. Probe run (the assigned invocation)

```
$ export TMPDIR=/fast/scratch/hyaku/tameshi-r48/T48W2ExecC1ProbeA
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/calibration/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev c7586b9a10effc63b4bd327f976edc094c1bdc17 \
    --base 473336d9d789f6081195e7376d17836a24666bc3 \
    --work "$S/w" \
    --only "sources-registry,depth,calibration,freshness,mutation sweep runner"
```

Exit 1, elapsed 195 s, empty `--work` (created by the counter), six profiles P0–P5 × three rounds, stderr empty.
The `exit 1` is the `--only` construction: `partial = bool(only)` in `measure.py:572`, so the label is `C1_R48_PARTIAL` and `C1_R48_PASS=false` by definition. **This is a probe, not a verdict.**

STATEMENT lines, verbatim:

```
STATEMENT cap/sources-registry: claimed=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 sha=b9b754713c9c ROUNDS r1=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 r2=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 r3=rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT cap/mutation sweep runner: claimed=MUTATE_SELFTEST: 106/106 pass|0 sha=a7d3f2dd7d47 ROUNDS r1=MUTATE_SELFTEST: 106/106 pass|0 r2=MUTATE_SELFTEST: 106/106 pass|0 r3=MUTATE_SELFTEST: 106/106 pass|0 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT axis/depth: claimed=9 sha=a7d3f2dd7d47 ROUNDS r1=9 r2=9 r3=9 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT axis/calibration: claimed=6 sha=657f009bdf1c ROUNDS r1=6 r2=6 r3=6 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
STATEMENT axis/freshness: claimed=9 sha=ba64041f49ff ROUNDS r1=9 r2=9 r3=9 DEPS required=none unstable=none never=bwrap,env,fleet-root,jj,node declared= MATCH DEPS-OK
```

Verdict line, verbatim:

```
C1_R48_PARTIAL: self_pin=1 stmts_pin=1 statements=5 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=1 base=473336d9d789f6081195e7376d17836a24666bc3 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R48_PASS=false
```

So within this group: **0 MISMATCH, 0 DEP-MISMATCH, 0 UNATTESTED, 0 UNPARSED, 0 OVERSIZE, 0 UNOBSERVABLE**. All five rows parse (`claimed=` is populated), all five declared values are reproduced in every round and every profile, all five declare `deps none` and my run observed `required=none`, and no `EXTRA` line was printed (no declared member needed re-observation).

## 2. Finding

### F1 — `SCORECARD.md:2355`: the calibration row's qualifying detail “60 of 64 sections credited” is false at the measured revision (57 of 64); the value `6` is correct

The row, verbatim (line 2355 of the file at REV):

```
| calibration | 6 | Restraint score of the strict cold-read monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` (`calibration_restraint_score`; `box3_full_page=false`, 60 of 64 sections credited): two points per restrained, evidence-linked `[~]` SHONEN box; box 3 is not credited. The round-31 table above stated 8; the monitor prints 6 at the round-46 base, so 8 was a stale standing value, tool sha256 `657f009bdf1c`, deps `none`, runs 3 stable | round-48 content revision | 48 (restated) |
```

Command that shows it (run twice: once inside the probe's P0 clone, once directly against the lane — same result):

```
$ python3 .ufo/evidence/round-21/coldread/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev c7586b9a10effc63b4bd327f976edc094c1bdc17
```

Observed (`T48W2ExecC1ProbeA.coldread-rev.json`): `calibration_restraint_score = 6`, `coldread.sections_covered = 57`, `coldread.sections_total = 64`, sum of `sections[i].credited` = **57**, `box3_full_page = false`.

Observed at BASE `473336d` with the same command (`…coldread-base.json`): `score = 6`, `sections_covered = 60`, `sections_total = 64`, credited = **60**, `box3_full_page = false` — i.e. the historical figure reproduced exactly, matching `.ufo/evidence/round-46/after/coldread-sections.stdout:1` and `.ufo/evidence/round-47/after/coldread-sections.stdout:1` (`COLDREAD_SECTIONS_CREDITED=60 (base 60)`). Intermediate revisions are already at 57: `15b1521` (the author's `--emit` revision) and `41c1bc0` both print 57 credited of 64. The `60` in the row is the round-46/47 number carried into a row that claims to be re-stated from round-48 observation.

Which sections were lost, and why (both readings parsed from the two JSON receipts):

| # | heading that lost credit | drift inputs shared with the base→REV change set |
|---|---|---|
| 43 | `## Repeated controls and gate registry — round 12` | `corpus/SOURCES.md`, `corpus/knowledge/repeated-control-precondition.md` |
| 45 | `## Pin disposition and provenance correction — round 13` | `corpus/SOURCES.md`, `corpus/knowledge/incremental-pin-disposition.md` |
| 47 | `## Effective expectation reconciliation — round 14` | `corpus/SOURCES.md`, `corpus/knowledge/incremental-pin-disposition.md` |

`git log 473336d..c7586b9 -- <each file>` returns the same single commit for all three inputs: `5054532 round-48: C2 records - rows S265-S268, snapshots and receipts, re-pointed entries, lesson draft`. The monitor's own ledger and the round-18 implementation are unchanged over `473336d..c7586b9` (`git diff --name-only` over `.ufo/evidence/round-21/coldread/` and `.ufo/evidence/round-18/measure.py` is empty), and no section gained credit, so the 60→57 drop is caused by those three record edits, not by the monitor.

Why the counter cannot see it: for kind `axis` the declared value V is the integer list from the score cell (`measure.py:211-216`), and the monitor is read only through `pick_line(..., 'monitor')` → `calibration_restraint_score` (`measure.py:255-264`). Everything in the evidence cell around the integer — including the “60 of 64” parenthetical — is unread text that the restated row still owes to observation. This is the shape of the round-47 mined mistake recorded at `.ufo/evidence/round-47/quality/round46-lesson-dash-restored.md:127` (“a same-round record edit costs a sub-measure the no-harm monitor did not track … `PROVINCE.md` append dropped the cold-read monitor from 60 to 55 credited sections (score 6 unchanged)”).

Consequence for the deciding run — **[INFERENCE]**, from my measured 57 plus lines 29–31 of the frozen script, which I did not run:

```
$ sed -n '29,31p' .ufo/evidence/round-48/deciding-run.sh
sections=$(python3 .ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$REV" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(sum(1 for s in d["coldread"]["sections"] if s["credited"]))')
echo "COLDREAD_SECTIONS_CREDITED=$sections (base 60)" | tee "$OUT/coldread-sections.stdout"
[ "$sections" -ge 60 ] || rc=1
```

The script's own sum is the same quantity I measured (57), so a deciding invocation at `c7586b9` should print `COLDREAD_SECTIONS_CREDITED=57 (base 60)` and set `rc=1`. The eight-line `no-harm.sh` monitor is *not* the source of the red: `.ufo/evidence/round-48/no-harm.sh:9-10` compares only `score=6 box3_full_page=False`, which holds; the red comes solely from `deciding-run.sh:31`. Note also `contract.json` `no_harm_monitors` pre-registers “cold-read sections 60”, so the content revision cannot satisfy its own pre-registered monitor as it stands.

Not mine to fix: the row is under the lane's `SCORECARD.md` write ban for this seat, and re-crediting sections (re-pinning the three sections' inputs) is an L1 decision. The finding is filed as data.

## 3. Rows that held (no finding), with the prose also checked

| statement | declared | observed (3 rounds × P0–P5) | verdict |
|---|---|---|---|
| sources-registry | `rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0, sha `b9b754713c9c` | identical in r1/r2/r3 and in all six profiles; raw census: `== A rows` 128, malformed 0, `A=114 B=11 C=3`, `mined=100 queued=22 rejected=6`, CLEAN | MATCH / DEPS-OK |
| mutation sweep runner | `MUTATE_SELFTEST: 106/106 pass`, exit 0, sha `a7d3f2dd7d47` | identical in r1/r2/r3 and all six profiles; raw tail `MUTATE_SELFTEST: 106/106 pass` + `VERDICT: PASS` | MATCH / DEPS-OK |
| depth | `9`, sha `a7d3f2dd7d47` | `9` in r1/r2/r3 and all six profiles | MATCH / DEPS-OK |
| calibration | `6`, sha `657f009bdf1c` | `6` in r1/r2/r3 and all six profiles | MATCH / DEPS-OK (prose defect: F1) |
| freshness | `9`, sha `ba64041f49ff` | `9` in r1/r2/r3 and all six profiles | MATCH / DEPS-OK |

Prose cross-checks (each an observation, not a re-derivation of the counter):

- **depth** (`SCORECARD.md:2354`): the cited ledger is exactly nine lines at `tools/mutate-and-run.sh:87-95` at REV — `git show REV:tools/mutate-and-run.sh | grep -cE '^#   (js|bash)-\S+\s+\S+\s+\d+/\d+'` → `9`, with lines 87–95 being the nine `js-*`/`bash-*` legs. The stated command prints `recorded_cases=9 depth_score=9` (`obs-depth.stdout`, 31 bytes).
- **freshness** (`SCORECARD.md:2356`): the row's `fresh=71`, `score=9` and “2 rows disputed: S048, S093” are all reproduced, including the exact disputed ids, from `obs-freshness.stdout`:
  `DISPUTED S048` / `DISPUTED S093` / `C1_R45: self_pin=1 population=73 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=c7586b9a10effc63b4bd327f976edc094c1bdc17 C1_R45_PASS=true`. The row's rule `floor(10 * fresh / 73)` equals the counter's `(10*fresh)//len(pop)` because `population=73`.
- **sources-registry** (`SCORECARD.md:2332`): `rows=128` is the census's own `== A rows` value; base has 124 rows (`git show 473336d:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'` → 124), REV 128 (+S265–S268), consistent with the row value and with C2's target set.
- **mutation sweep runner** (`SCORECARD.md:2333`): exit 0 and `106/106` observed; pinned sha `sha256(git show REV:tools/mutate-and-run.sh)[:12] = a7d3f2dd7d47` matches the row. (The `--regression` clause in the “what it can do” cell is demonstrated by the same selftest run, which the probe observed passing.)
- **calibration** (`SCORECARD.md:2355`): `6`, `box3_full_page=false` and “box 3 is not credited” all reproduce; only the section count in the same parenthetical does not (F1). The row's historical sentence “the monitor prints 6 at the round-46 base” also reproduces (base reading: score 6).

## 4. Nondeterministic rows in this group

None. All five rows declare `stable`, and my run saw exactly **one** member per statement — identical tuple in r1, r2, r3 and in profiles P0–P5 — so the question “did your run see more than one member?” is **no for all five**. No `EXTRA` observations were needed (`attested_extra=0`).

## 5. Fleet / lane state seen by the probe

Four FLEET points (in the `.stdout`), summarised:

| point | census_sha | lane_clean |
|---|---|---|
| 1 (before round 1) | `3fb7261569f4` | 1 |
| 2 | `3fb7261569f4` | 1 |
| 3 | `3fb7261569f4` | 1 |
| 4 (after round 3) | `3fb7261569f4` | 1 |

`fleet_drift=0` — the lane was clean against REV for `corpus/`, `tools/`, `SCORECARD.md` at every point during this probe. `sibling_moves=1`: `souji-shokunin` moved `d805d1d61324` → `9da5e9a559f7` between points 2 and 3 (disclosure only, per amendment 5). For contrast, the author's own emit receipt `.ufo/evidence/round-48/calibration/emit-15b1521.stdout` prints `lane_clean=0` at points 2–4; that receipt is not mine to attack and its verdict line already says `fleet_drift=1`.

## 6. Risks, limits, cleanliness

- One probe run of five statements is not the deciding run and cannot be one; the label `C1_R48_PARTIAL` with `PASS=false` is the correct receipt for it.
- F1's value-level consequence is limited to the row text; the C1 predicate's integer for `calibration` passes. If the L1 treats the deciding run as the round gate, the pre-registered `>= 60` section requirement is the blocker, not C1's value.
- Nothing written outside `.ufo/waves/round-48/a2w1/`; no lane git state touched (no add/commit/stash/checkout/switch/reset/pull/push; no jj mutation). Scratch `/fast/scratch/hyaku/tameshi-r48/T48W2ExecC1ProbeA` deleted at the end of the seat (verified absent).
- Disk guard checked before the probe: `/fast/scratch/hyaku` 23% used, 620 G free.

## 7. Receipts in this directory

| file | sha256 |
|---|---|
| `T48W2ExecC1ProbeA.stdout` (probe stdout, exact) | `56f8e01ed3d9c97e86101f4a3a49f2ab0dfdc1cab63adfe518874e0a4d549a6e` |
| `T48W2ExecC1ProbeA.coldread-rev.json` (monitor at `c7586b9`) | `17e55ca072298ad58f062d7071f204c9fd5e9f25e9d7a5496f67c947d3e45a59` |
| `T48W2ExecC1ProbeA.coldread-base.json` (monitor at `473336d`) | `b63afd82b15b8d2828b9d4f1e29b5b18757bbf924020f88207ecc265299a9603` |

Raw observation files produced by the counter inside the probe work dir (`round{1,2,3}/P0/obs-*.stdout`, includes `obs-calibration.stdout`, `obs-freshness.stdout`, `obs-depth.stdout`, `obs-sources-registry.stdout`, `obs-mutation-sweep-runner.stdout`) were in the scratch tree and were deleted with it; the numbers above are quoted from them before deletion, and the same values are re-derivable from the two JSON receipts plus the commands given in sections 2 and 3.
