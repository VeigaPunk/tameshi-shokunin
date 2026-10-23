# MutateToolA

**Verdict:** 4 killed; 5 survived against the tool selftest plus the public v1 families. Survivors are detector coverage gaps, not contract changes.

## Evidence

- Seat: `MutateToolA`. Axis: operability. Probe axes: behavioral coverage, single-edit isolation, exact restoration.
- Scratch clone revision: `a4f718138bdad20de741faeca57891645e5a64d9`.
- Public v1 counter imported with bytecode writes disabled. Its four fixture generators build the public families; `rep` also builds supplemental inputs. No counter main, v2 run, regression run, or production edit.
- Each seed 1–5 uses a fresh `random.Random(seed)`, kill generation before accept generation: 18 must-kill + 8 must-accept = 130 actual fixture invocations per tool.
- Expected detector: selftest exit 0 and `TALLY_AUDIT_SELFTEST: 11/11 pass`; must-kill exit 1 plus `TALLY_AUDIT: FAIL`; must-accept exit 0 plus `TALLY_AUDIT: PASS`.
- Shared pristine control: selftest `PASS`, v1 130/130 correct. Shared restored control: selftest `PASS`, v1 130/130 correct, run from the actually restored M01 root copy and its restored copy beside the runner. All nine mutants and all nine selftest copies were restored byte-for-byte to that same original tool.

| Mutant (original tool line) | One edit | Selftest observed | v1-family misses | Verdict |
|---|---|---|---|---|
| M01 (`tools/tally-audit.py:208`) | `if sorted(ops) != sorted(names):` → `if set(ops) != set(names):` | `TALLY_AUDIT_SELFTEST: 11/11 pass` (exit 0) | 0/130 | survived |
| M02 (`tools/tally-audit.py:212`) | `if nlegs != len(names):` → `if False and nlegs != len(names):` | `TALLY_AUDIT_SELFTEST: 10/11 pass` (exit 1) | 0/130 | killed |
| M03 (`tools/tally-audit.py:222`) | `for s in range(1, 256):` → `for s in range(1, 5):` | `TALLY_AUDIT_SELFTEST: 11/11 pass` (exit 0) | 5/130 | killed |
| M04 (`tools/tally-audit.py:224`) | `for pos in range(n):` → `for pos in range(n - 1):` | `TALLY_AUDIT_SELFTEST: 11/11 pass` (exit 0) | 0/130 | survived |
| M05 (`tools/tally-audit.py:245`) | `for kind, new in (('dup', ops[:i + 1] + ops[i:]), ('drop', ops[:i] + ops[i + 1:])):` → `for kind, new in (('drop', ops[:i] + ops[i + 1:]),):` | `TALLY_AUDIT_SELFTEST: 10/11 pass` (exit 1) | 10/130 | killed |
| M06 (`tools/tally-audit.py:245`) | `for kind, new in (('dup', ops[:i + 1] + ops[i:]), ('drop', ops[:i] + ops[i + 1:])):` → `for kind, new in (('dup', ops[:i + 1] + ops[i:]),):` | `TALLY_AUDIT_SELFTEST: 11/11 pass` (exit 0) | 0/130 | survived |
| M07 (`tools/tally-audit.py:240`) | `if g != exp:` → `if g[0] != exp[0]:` | `TALLY_AUDIT_SELFTEST: 11/11 pass` (exit 0) | 0/130 | survived |
| M08 (`tools/tally-audit.py:193`) | `if p != nlegs:` → `if p < nlegs:` | `TALLY_AUDIT_SELFTEST: 8/11 pass` (exit 1) | 50/130 | killed |
| M09 (`tools/tally-audit.py:240`) | `if g != exp:` → `if g[1] != exp[1]:` | `TALLY_AUDIT_SELFTEST: 11/11 pass` (exit 0) | 0/130 | survived |

### Exact commands and observed outputs

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/c
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/c checkout -q --detach a4f718138bdad20de741faeca57891645e5a64d9
timeout 1800 python3 -B /fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/probe.py
```

Clone and checkout returned exit 0 with no output. The probe uses at most 24 fixture workers plus nine selftest workers, each in its own bounded scratch directory. Every actual argv, cwd, exit code, stdout, stderr, input hash and tool hash is retained in `results.json` and `runs/<phase>/<id>/result.json`.

Example exact pristine detector command:
```sh
timeout 900 /usr/bin/python3 -B -I /fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/c/tools/tally-audit.py --selftest
```
```text
CASE pristine PASS (exit 0)
CASE dup-drop operand PASS (exit 1)
CASE nlegs wrong PASS (exit 1)
CASE status 4 passes PASS (exit 1)
CASE guard undercount only PASS (exit 1)
CASE harness exit-only PASS (exit 1)
CASE harness swallowed PASS (exit 1)
CASE harness position 8 skipped PASS (exit 1)
CASE harness position 0 skipped PASS (exit 1)
CASE harness position 1 skipped PASS (exit 1)
CASE reversed operands PASS (exit 0)
TALLY_AUDIT_SELFTEST: 11/11 pass
```

Missed public inputs:
- M03: seed 1 `gT08(arm=36)` (ACCEPT; exit 0); seed 2 `gT08(arm=246)` (ACCEPT; exit 0); seed 3 `gT08(arm=62)` (ACCEPT; exit 0); seed 4 `gT08(arm=62)` (ACCEPT; exit 0); seed 5 `gT08(arm=161)` (ACCEPT; exit 0).
- M05: seed 1 `N05` (ACCEPT; exit 0); seed 1 `gN05(<= nlegs - 1)` (ACCEPT; exit 0); seed 2 `N05` (ACCEPT; exit 0); seed 2 `gN05(< nlegs)` (ACCEPT; exit 0); seed 3 `N05` (ACCEPT; exit 0); seed 3 `gN05(<= nlegs - 1)` (ACCEPT; exit 0); seed 4 `N05` (ACCEPT; exit 0); seed 4 `gN05(< nlegs + 0)` (ACCEPT; exit 0); seed 5 `N05` (ACCEPT; exit 0); seed 5 `gN05(< nlegs + 0)` (ACCEPT; exit 0).
- M08: seed 1 `N05` (ACCEPT; exit 0); seed 1 `gN05(<= nlegs - 1)` (ACCEPT; exit 0); seed 1 `B0-pristine` (KILL; exit 1); seed 1 `B1-T07` (KILL; exit 1); seed 1 `B3-decoys` (KILL; exit 1); seed 1 `B2-reversed` (KILL; exit 1); seed 1 `B5-renamed` (KILL; exit 1); seed 1 `B4-cosmetic` (KILL; exit 1); seed 1 `gB6-permuted` (KILL; exit 1); seed 1 `gB7-nonce` (KILL; exit 1); seed 2 `N05` (ACCEPT; exit 0); seed 2 `gN05(< nlegs)` (ACCEPT; exit 0); seed 2 `B0-pristine` (KILL; exit 1); seed 2 `B1-T07` (KILL; exit 1); seed 2 `B3-decoys` (KILL; exit 1); seed 2 `B2-reversed` (KILL; exit 1); seed 2 `B4-cosmetic` (KILL; exit 1); seed 2 `B5-renamed` (KILL; exit 1); seed 2 `gB7-nonce` (KILL; exit 1); seed 3 `N05` (ACCEPT; exit 0); seed 2 `gB6-permuted` (KILL; exit 1); seed 3 `gN05(<= nlegs - 1)` (ACCEPT; exit 0); seed 3 `B1-T07` (KILL; exit 1); seed 3 `B0-pristine` (KILL; exit 1); seed 3 `B2-reversed` (KILL; exit 1); seed 3 `B3-decoys` (KILL; exit 1); seed 3 `B4-cosmetic` (KILL; exit 1); seed 3 `B5-renamed` (KILL; exit 1); seed 3 `gB7-nonce` (KILL; exit 1); seed 3 `gB6-permuted` (KILL; exit 1); seed 4 `N05` (ACCEPT; exit 0); seed 4 `gN05(< nlegs + 0)` (ACCEPT; exit 0); seed 4 `B0-pristine` (KILL; exit 1); seed 4 `B1-T07` (KILL; exit 1); seed 4 `B5-renamed` (KILL; exit 1); seed 4 `B2-reversed` (KILL; exit 1); seed 4 `gB7-nonce` (KILL; exit 1); seed 4 `B3-decoys` (KILL; exit 1); seed 4 `B4-cosmetic` (KILL; exit 1); seed 4 `gB6-permuted` (KILL; exit 1); seed 5 `N05` (ACCEPT; exit 0); seed 5 `gN05(< nlegs + 0)` (ACCEPT; exit 0); seed 5 `B0-pristine` (KILL; exit 1); seed 5 `B3-decoys` (KILL; exit 1); seed 5 `B4-cosmetic` (KILL; exit 1); seed 5 `B1-T07` (KILL; exit 1); seed 5 `B2-reversed` (KILL; exit 1); seed 5 `B5-renamed` (KILL; exit 1); seed 5 `gB7-nonce` (KILL; exit 1); seed 5 `gB6-permuted` (KILL; exit 1).

### Survivor discriminators

These supplemental inputs are outside the public-v1 count. A survivor must accept its discriminator while the pristine and restored tool reject it. Full bytes and exact stdout are in `supplements/` and `runs/*-supplement/`.

- **M01**: Append a second `"$st_js"` operand while retaining all nine original operands. This preserves the set but not the multiset. Input `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/supplements/M01.sh`; pristine KILL/exit 1, mutant ACCEPT/exit 0, restored KILL/exit 1.
  Observed mutant final line: `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`.

- **M04**: Immediately after the tally declaration, map only `st_citecheck=126` to 0. Other statuses and positions remain unchanged. Input `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/supplements/M04.sh`; pristine KILL/exit 1, mutant ACCEPT/exit 0, restored KILL/exit 1.
  Observed mutant final line: `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`.

- **M06**: Change only the actual tally guard from `!= nlegs` to `> nlegs`; this drops undercount detection. Input `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/supplements/M06.sh`; pristine KILL/exit 1, mutant ACCEPT/exit 0, restored KILL/exit 1.
  Observed mutant final line: `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`.

- **M07**: Change only the tally FAIL label to `REGRESSION: FAILURE`, preserving exit 1. Input `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/supplements/M07.sh`; pristine KILL/exit 1, mutant ACCEPT/exit 0, restored KILL/exit 1.
  Observed mutant final line: `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`.

- **M09**: Change only the tally failure exit from 1 to 0, preserving the exact FAIL first line. Input `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/supplements/M09.sh`; pristine KILL/exit 1, mutant ACCEPT/exit 0, restored KILL/exit 1.
  Observed mutant final line: `TALLY_AUDIT: PASS (static=pass runtime=pass harness=pass)`.

### Hashes and restoration

- Pristine tool, clone tool after probe, and every restored mutant/copy: `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`.
- Runner before and after: `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (exact original bytes, never edited).
- Public v1 counter before and after: `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca`.

| Mutant | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|
| M01 | `1ca2bd12b9c90409e2f02acff9bd1aa54fb4cab17cebccfa7132a7092191f04f` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M02 | `7b569f4be189e36485a589bd8230b6c20e24413ce7bd8f82d20fcb3890128e81` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M03 | `684e50a6977cec8cfd875f6f0e10b4d73e02998db0f241b825454d77c43565d4` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M04 | `e2dec78eb3e94f9f835102ffbb3f674cdc5580f024b68aad2452ac5440af02f4` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M05 | `38311986e9a713f83d2a576b59c53393439d1f596325e3025960801c6c5ced72` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M06 | `7b61a98488ae94aab54e632822a89414b8fbca4408e42216e560a596ccb06c11` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M07 | `facf73457390d671ccad2f94c6ef3f4867cd6ca5f3421a3832a9a3f2f48f7344` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M08 | `a8209accd3a963fb51c4fccb40e01c99f28436ea5539c1c5548f54e56046b7fb` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |
| M09 | `95f265f221ef72731c419132562044d5476c5eec5af50ffce101ff433440af47` | `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef` |

Evidence files (all within `/fast/scratch/hyaku/tameshi-r32-seats/MutateToolA/`):
- `probe-config.json:1`: named axes and seeds.
- `probe.py:1`: bounded detector source, including process-tree cleanup and exact-byte restoration in `finally`; reconstruct the recorded single-line mutants from `manifest.json` before replaying because the probe restored them.
- `manifest.json:1`: all single-line edits, mutated hashes, all 130 public fixture labels and hashes, and supplemental input hashes.
- `results.json:1`: actual outputs and all detector judgments; one bounded `runs/<phase>/<id>/result.json:1` per invocation.
- `restoration.json:1`: before/restored hashes and exact-byte comparison for all 18 mutant copies; runner, clone tool and public counter hashes.

## Smallest safe correction

Keep the frozen tool unchanged for this measurement. In a later permitted change, extend its own selftest with the five named survivor discriminators (assert the specific failed check), and include them in any replacement fixture contract before collecting new data. The public-v1 suite misses the static nlegs check removal (M02); the tool selftest already kills that mutant. No production correction was applied.

Tools: existing Python 3.14.8 and GNU bash 5.3.20; no install or update. The initial `timeout --version` probe returned usage/exit 125; actual `timeout DURATION COMMAND` executions are recorded above. No process started by this probe remains live after completion.

Elapsed detector time: 929.174 seconds.
