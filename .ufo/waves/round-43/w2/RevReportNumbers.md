# RevReportNumbers — round-43 report numbers and their sources

Wave-2 reviewer, lane bounds honoured (read-only; counters run only at `--rev 487b8f0da89fa0e2b8bea6930068accbf36e70a9` and `--rev 3aee2c078f8976499b587086af3577fc94dc8cf1`, inside `git clone --shared` scratch `/tmp/tameshi-r43-w2-RevReportNumbers-clone` so the moving worktree could not contaminate the run).

Purpose: list every number a round-43 report must state, where it must come from, the exact command that re-derives it, and flag every number a report could state from memory (or from a stale/superseded receipt) instead of a committed receipt.

Observation window: 2026-10-25 08:03–08:11 -0300. During the window HEAD moved `e20cf89 → b510ad1 (A11) → bb36f80 (A12)` and the worktree collected A13 receipts at a not-yet-committed rev `f551ca69`. Anything measured against the live worktree (not a cloned rev) is unstable; all commands below run in a scratch checkout of a named rev.

---

## A. Wave seat counts — source: registries + `ls` (never from memory)

| Number | Value (at 08:11) | Source | Re-derive |
|---|---|---|---|
| w1 seats declared | 34 | `.ufo/waves/round-43/w1/swarm-registry.json` `members` count | `python3 -c "import json;print(len(json.load(open('.ufo/waves/round-43/w1/swarm-registry.json'))['members']))"` (also `spec-w1.json` `items`: 34; `dispatch-w1.json` `counts`: `{"spawn":34,"resume":0,"total":34}`) |
| w2 seats declared | 34 | `.ufo/waves/round-43/w2/swarm-registry.json` | same path swap; spec-w2 items=34, dispatch-w2 counts total=34 |
| w1 role mix | reviewer 7, scout 8, critic 5, executor 4, mutation-tester 3, scribe 3, sentinel 2, connector 1, revenger 1 | registry `role` field | `python3 -c "import json,collections;print(collections.Counter(v['role'] for v in json.load(open('.ufo/waves/round-43/w1/swarm-registry.json'))['members'].values()))"` |
| w2 role mix | reviewer 16, mutation-tester 6, critic 5, scout 2, executor 2, sentinel 2, simplifier 1 | registry | same on w2 |
| w1 seats with a committed report | **32 tracked** (+2 still untracked: `CritC1Overfit.md`, `RevC1Counter.md`) | git index, NOT the registry | `git ls-tree -r --name-only c5335c70bff750218b3a6db0a92daae76509a0de -- .ufo/waves/round-43/w1 \| grep -c '\.md$'` → 32; `ls .ufo/waves/round-43/w1/*.md \| wc -l` → 34 (present ≠ committed) |
| w2 seats with a committed report | 0 committed; 19 files present at 08:11 and growing | git index + `ls` | `ls .ufo/waves/round-43/w2/*.md \| wc -l` (time-dependent; must be computed at publish time, not memorised) |
| dead seats / resume sends | must come from `dispatch-wN.json` `resumeSends`/`taskCall` results — the registry has **no** status or result field | dispatch JSON | `python3 -c "import json;d=json.load(open('.ufo/waves/round-43/dispatch-w2.json'));print(d['counts'],d.get('resumeSends'))"` |
| duplicated item texts | 0 in both waves | registry `item` strings | `Counter(v['item'] for v in members.values()).most_common(1)` |

**Flag:** both registries show `createdAt == updatedAt` (w1 `10:51:16.144Z`, w2 `11:03:27.139Z`) — the registry is written once at dispatch and never updated. It is evidence of *declaration only*; any "completed/report" number must come from `ls`/git, never from the registry.

## B. Counter fields — source: committed stdout (mostly absent at the right rev)

Committed receipts that exist: `before/` (8 files), `control/` (10), `prerun/` (2 tracked + 7 untracked A12/A13), `after/` (only `README.md`, zero receipts), `census-sources/` (3 files, all identical).

**There is no committed at-freeze receipt for any claim at any rev ≥ A10.** `prerun/c1-at-freeze.stdout` and `c3-at-freeze.stdout` were taken at `114ffacd` (A6/A7 bytes). `git ls-tree -r 3aee2c07 -- .ufo/evidence/round-43/after` → 0 objects; the directory is unrepresentable in git until receipts land (the A11 README is the only object at HEAD).

Closure command that must be used instead (scratch clone, rev-explicit):

```
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/r43 && cd /tmp/r43 &&
git checkout -q 3aee2c078f8976499b587086af3577fc94dc8cf1 && PYTHONDONTWRITEBYTECODE=1 \
python3 -I .ufo/evidence/round-43/<mutants|calibration|guard>/measure.py \
  --lane /tmp/r43 --rev 3aee2c078f8976499b587086af3577fc94dc8cf1 --freeze 3aee2c078f8976499b587086af3577fc94dc8cf1
```

Measured in the clone at `3aee2c07` (reproducible; observed twice):

- **C1**: `C1_R43_PASS=true` exit 0, `self_pin=1 tool_sha_ok=1 fixtures_pass=12/12 live_ok=3/3 mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 unresolved=0 dead_code_arg_ok=1 kill_fixture_reachable=1`. Killed names: `attr_bind_several_assignments, attr_never_resolve_self, method_fold_disabled, outflag_dests_never_recorded, outflag_no_parse_args_check`; dead-code name `method_fold_several_returns` via `F12_method_two_returns`. Note: at ≥A11 bytes the fields become `kill_binding=1`, `kill_cases=…`, `mutants_sha_ok=1` — a report must quote whichever counter revision it cites.
- **C2**: `C2_R43_PASS=false` exit 1, `total=8` (`m7=5 m8=3`), `classes=7 records=4 sources_rows=114 standing=114 receipts=17 revisions=2`, `m13_probe=standing=7_column0=113_valid=114`. m7 hits: `corpus/lessons/round-43.md` UNKNOWN `S160, S166, S256, S259` + `LOG.md#round-43` UNKNOWN `S256`. m8 hits: `corpus/lessons/round-43.md:.ufo/waves/...`, `corpus/lessons/round-43.md:tools/*.py`, `SCORECARD.md#round-43:.ufo/evidence/round-43/after/`. (At the untracked A13 candidate `f551ca69` the L1's own receipt reads `total=1`, `first=m7:corpus/lessons/round-43.md_unknown_S259`.)
- **C3**: `C3_R43_PASS=true` exit 0, `selftest_cases=24 selftest_failed=0 staged_rows=103 live_collisions=7 live_held=3 live_unmapped=0 live_verdict=refused live_cascade=1 naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 safe_floor=S256 staged_sha256=020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807 naive_agree=1 substitute=0` (at A12+ also `held_refused=1`).

Committed before/control lines (numbers a report may quote, with the receipt path):

- C1 before = `mutants_declared=6 mutants_killed=4` — `before/c1-round42-at-base.stdout` (the **round-42** counter, exit=1) or `control/c1-round42-battery[-A10].stdout` (`C1_R43_CONTROL … mutants_killed=4 C1_R43_CONTROL_PASS=false`, exit=1).
- C2 before = `m12=2 m13=1 total=3` — `before/c2-at-base-A10.stdout` (rev=487b8f0, freeze=3aee2c07, exit `c2_base_exit=1`). **Superseded duplicate:** `before/c2-at-base.stdout` says `m12=1 m13=1 total=2` (freeze=f0f2636, A1 counter). Both are committed side-by-side; a report must name which.
- C3 before = `tool_absent=1 C3_R43_PASS=false` — `before/c3-at-base.stdout`.
- C3 control: `control/c3-constant-empty-A10.stdout` `expected_collisions=7` vs the superseded `control/c3-constant-empty.stdout` `expected_collisions=6`.
- Probe survivors: `control/c1-probe-survivors.stdout` (two `PROBE outcome=survived` lines).
- C2 do-nothing control: `control/c2-round42-counter.stdout`. **Defect in the receipt itself:** its header comment asserts "exit 0 … its own round-42 predicate passes" while the pasted line ends `C2_R42_PASS=false` — the narrative and the number disagree.

## C. Row counts — source: grep (never a receipt)

| Number | Value | Command |
|---|---|---|
| SOURCES.md rows at base | 113 | `git show 487b8f0da89fa0e2b8bea6930068accbf36e70a9:corpus/SOURCES.md \| grep -cE '^ {0,3}\| S[0-9]{3} \|'` |
| SOURCES.md rows at freeze | 114 | same, rev `3aee2c07` (worktree today also 114) |
| Staged rows | 103 | `grep -cE '^ {0,3}\| S[0-9]{3} \|' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` (109 total lines) |
| m13 delta proof | column0=113 vs valid=114 **on a constructed mirror** — on the live registry both forms count 114; the counter's `m13_probe` numbers are the mirror's, not the registry's | `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` vs `grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` (both → 114 today) |
| Quarantine rows | 17 (14 payload-absent: S105,S109,S110,S118,S119,S124,S126,S129,S131,S132,S137,S140,S141,S143; 3 could-not-be-fetched: S113,S123,S134) | `awk -F'|' -v l='tameshi' '$2 ~ ("\`" l "\`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4,$5}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` |
| Census rows | **none printed** — the census emits warnings only (`ok` line, 10×W04 + 1×W01 S101); any "114" must come from grep, not the receipt | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` |

## D. Commit hashes — source: git/jj lane state (never the contract's narration)

| Number | Value | Command |
|---|---|---|
| base rev | `487b8f0da89fa0e2b8bea6930068accbf36e70a9` | `git log --format='%H %s' -12` |
| records commit | `c5335c70bff750218b3a6db0a92daae76509a0de` (08:00:58; **inside** the freeze chain, between A9 `273c047` and A10 `3aee2c0` — records changed again after it at A11/A12/A13) | same |
| freeze of record | **ambiguous, moving**: ticket/`contract.frozen_before` name `114ffacd`/`3aee2c07`; committed freezes continue `b510ad1` (A11, 08:05:44), `bb36f80` (A12, 08:07:08); an untracked A13 receipt cites `f551ca69` | `git log --format='%h %ci %s' 487b8f0..HEAD`; `jj log --no-graph -n 6 --template 'change_id.short() ++ " " ++ commit_id.short()'` |
| jj change ids | A12 = `wxrplxkwozmu`/`bb36f80c6bcd`; working = `lkuyvykouyrv`/`8000de78f987` (at 08:11) | `jj log` (changes move) |
| commits base..HEAD | 12 (freeze chain 697d2f1 → bb36f80) | `git log --format='%h %s' 487b8f0..HEAD` |
| counter/tool pins | per-rev `git show REV:.ufo/evidence/round-43/<x>/measure.py \| sha256sum` vs `contract.json claims.<X>.counter_sha256` at the same rev | object-level: `git ls-tree REV .ufo/evidence/round-43/mutants/measure.py` (blob at 3aee2c07=`92dc46de`, at bb36f80 changed) |

**Do not copy these from SCORECARD.md:** its round-43 block says "frozen at `17f6ef0c…`" and its counting commands carry `--freeze 17f6ef0c…` (the A2/A3 freeze — five amendments stale); its capability row pins the guard tool at `8140945a…` which matches **no** committed guard bytes (actual `2e8f2e89…` at ≥A9). LOG.md's bullet repeats "Contract frozen at `17f6ef0c`" and "amendments A1–A3 … A4" — eight amendments stale at HEAD.

## E. Other numbers the report must state

- selftest cases: **24** (fresh run, `python3 -I tools/staged-id-guard.py --selftest` → `cases=24`) — the committed at-freeze receipt says 23 (114ffacd/A7 bytes); the w2 dispatch texts say 23.
- mutants declared: 6 (`.ufo/evidence/round-42/census/mutants.json` at REV — exists at base too).
- classes: 7; records scanned: 4 (round-42+43 lessons, SCORECARD block, LOG section); receipts scanned: 17; revisions: 2.
- source snapshots: 2 files, 38687 B sha `79f6501a` (Stryker), 170793 B sha `6e4a06c0` (Wikipedia), `sha256 -c .ufo/evidence/round-43/sources/sha256.txt`.
- axis scores: depth 9 → 9, calibration 6 → 6 — only inside `w1/ExecCommandD.md` (a seat report, not a machine receipt).
- QUALITY criteria: 83, 84 (`corpus/QUALITY.md` — grep the numbers, don't memorise).
- policy band: LOG claims "band 32–64"; declared total 34+34 = **68** — exceeds the top of band; the number's derivation (per-wave vs total) must be stated.
- staged file digest: `020fbeaa048f…` — `sha256sum SOURCES.append.md` (only printed by ≥A9 counters; no committed receipt contains it).
- guard pin: `2e8f2e89…` (`sha256sum tools/staged-id-guard.py`; matches contract `tool_sha256` and frozen_tools).

## Numbers a report could state from memory / a stale receipt — flags

1. **C2 verdict**: any `PASS=true`/`total=0` at the freeze is currently **untrue** — clone-run at `3aee2c07` prints `total=8 PASS=false`; at the A13 candidate `total=1`. No committed receipt shows C2 at any freeze.
2. **C1 `mutants_killed=4` as "before"**: the claim's own counting command at `--rev 487b8f0` prints `mutants_killed=5 … C1_R43_PASS=true` — the 4 lives only in the round-42-battery control receipts. If a report reproduces the "before" with the claim's counting command it will print 5.
3. **`selftest_cases=23`, `live_collisions=6`, `live_held=2`**: quoted only by the 114ffacd receipts; every counter run at ≥A9 prints 24/7/3. The w2 dispatch texts themselves repeat 23.
4. **`m12=1 total=2` "before"**: superseded by the committed A10 base receipt (`m12=2 total=3`) — SCORECARD and LOG both still say 2.
5. **census "exit 0 at start and end"**: `census-sources/start.stdout`, `after.stdout` and the untracked `after-2.stdout` are byte-identical (sha `bb8c4162…`) and predate the S159 append commit `c5335c7` — there is no committed post-append census run at all.
6. **"frozen at 17f6ef0c / freeze of record 114ffacd"**: both wrong at HEAD (A12 `bb36f80`, A13 `f551ca69` pending). `contract.json frozen_before` is 5–8 amendments stale; A12's own `when` says "during wave 2".
7. **`after/` evidence citations**: SCORECARD cites `.ufo/evidence/round-43/after/` as evidence for all three claims; it holds only a README — every "after" cell currently resolves to nothing (this is one of C2's m8 hits).
8. **guard tool sha `8140945a…` in the capability row**: matches nothing; the real pin is `2e8f2e89…`.
9. **w1 "34 reports"**: only 32 tracked at the records commit; `CritC1Overfit.md` and `RevC1Counter.md` remain untracked at 08:11.
10. **A12/A13 receipts** (`prerun/*-at-A12/A13.stdout`, 7 files): untracked, and A13's `rev=f551ca69` is not yet a commit — citable only after they land; A12's own `c1-at-A12.stdout` shows `self_pin=0 PASS=false` (pin `b56a34d7` ≠ blob `3d1ff3dc` at `bb36f80`).
11. **"7 collisions/3 held" in LOG**: consistent with fresh runs but contradicts the only committed at-freeze receipt (6/2); the sentence is right, the receipt is stale — either way a number is being quoted from memory.
12. **m13's 113/114**: those are mirror numbers, not registry counts; quoting them as if the real registry had an indented row would be wrong.
13. **`kill_fixture_reachable=1` vs `kill_binding=1`/`held_refused=1`/`substitute=0`**: the field names and new fields exist only at ≥A11/A12 bytes — a report must state which counter revision it is quoting, since committed receipts at 114ffacd print the old vocabulary.

## Residual risk / verification gaps

- The deciding run the contract calls "the ONE deciding run" has no committed home yet (`after/README.md` reserves the directory); every at-freeze number above is a clone-run result, not a receipt.
- Wave-2-derived amendments (A12 cites a wave-2 seat) mean the measurement code was still changing after seats dispatched; the wave-1 freeze-of-record framing no longer describes the lane.
- `records=4` includes the round-42 lesson; a report claiming "four records" must name which.
- If the L1 re-pins C1 at A13 the `self_pin=0` at `bb36f80` resolves; verify `git ls-tree` blob vs pin on whichever rev becomes the freeze of record before trusting any `self_pin=1` in a fresh receipt.
- `after-2.stdout`'s identical sha to the pre-append census may be a genuine fresh run (S159's URL may not add a warning) — but the report should not present three identical digests as three runs.
