# C2Mutants — mutation probe

## Verdict

At the assigned revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`, four named mutations survive both detectors:

- INCONCLUSIVE mapped to Timeout.
- Location column one too high.
- End position equal to start.
- Score tolerance widened from `1e-9` to `1.0`.

The reverse column mutation (one too low) is killed by schema validation. KILLED mapped to Timeout, dropped ledger checking, and skipped schema validation are also killed.

Supplementary comparison against amendment-2 commit `09dc114`: its new emitter selftests kill the first three survivors. **The tolerance mutation still survives both detectors.** This comparison does not replace the assigned-revision results.

Axes: detector coverage, mutation specificity, scratch isolation, exact restoration. No production correction was applied. These are coverage findings, not changes to the contract.

## Environment and procedure

Private clone created as assigned:

```sh
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/C2Mutants-r25
git -C /tmp/C2Mutants-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
```

Commands executed in scratch; sibling repositories were read-only inputs. A staged fleet held a copied runner at `/tmp/c2m/stage/tameshi-shokunin/tools/mutate-and-run.sh` and symlinks to sibling repositories. Regression command:

```sh
bash /tmp/c2m/stage/tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /tmp/c2m/work/regression --keep
```

Observed exit 0:

```text
REGRESSION: PASS (cases=8 passed=8; ledger legs exact: killed-delta<=0 flips<=0)
REGRESSION_WORKDIR: /tmp/c2m/work/regression (kept)
```

Captured runner stdout was copied into `/tmp/c2m/work/regression/regression.stdout`, matching the interop tool's own kept-workdir layout. All eight result tables contained KILLED/SURVIVED only, with zero INCONCLUSIVE rows.

Dependency setup:

```sh
uv venv /tmp/c2m/venv --python 3
uv pip install --python /tmp/c2m/venv/bin/python jsonschema==4.25.1
```

Tool/dependency installation: jsonschema 4.25.1 through uv/PyPI into an isolated temporary environment, for the detector's required Python schema validator. Interpreter: CPython 3.15.0; existing Node: v24.21.0. No pacman transaction or host service operation.

The same bounded commands were used on pristine, each mutated tool, and restored bytes:

```sh
cd /tmp/C2Mutants-r25
/tmp/c2m/venv/bin/python tools/mte-interop.py --selftest
/tmp/c2m/venv/bin/python tools/mte-interop.py --check --workdir /tmp/c2m/work/regression
```

Both pristine commands exited 0:

```text
MTE_SELFTEST: 10/10 pass
MTE_INTEROP: PASS legs_conforming=8/8
```

Each mutation was applied separately from saved pristine bytes. Every replacement site was asserted unique before mutation. The tool was restored after every probe. Raw assigned-revision detector outputs and full hashes are retained in `/tmp/c2m/results.json`; baseline outputs in `/tmp/c2m/base-selftest.txt` and `/tmp/c2m/base-check.txt`.

## Assigned-revision results

References below are to `tools/mte-interop.py` in the pinned clone, not the subsequently advanced lane checkout. Exit 1 indicates a detected failure; no setup failure occurred in this table.

| Mutant and smallest changed site | Expected detector | Actual selftest output; exit | Actual check output; exit | Verdict |
|---|---|---|---|---|
| M1, line 58: `INCONCLUSIVE: RuntimeError` → `Timeout` | Emitter mapping fixture | `MTE_SELFTEST: 10/10 pass`; 0 | `MTE_INTEROP: PASS legs_conforming=8/8`; 0 | SURVIVED |
| M2, line 58: `KILLED: Killed` → `Timeout` | Ledger killed-count comparison | `MTE_SELFTEST: 10/10 pass`; 0 | `MTE_INTEROP: FAIL legs_conforming=0/8`; 1 | KILLED |
| M3a, line 111: column formula final `+ 1` → `+ 2` | Exact emitter coordinates | `MTE_SELFTEST: 10/10 pass`; 0 | `MTE_INTEROP: PASS legs_conforming=8/8`; 0 | SURVIVED |
| M3b, directional control at line 111: remove final `+ 1` | Schema minimum column | `MTE_SELFTEST: 10/10 pass`; 0 | `MTE_INTEROP: FAIL legs_conforming=1/8`; 1 | KILLED |
| M4, line 138: end offset `start + len(d['old'])` → `start` | Exact end-exclusive emitter coordinates | `MTE_SELFTEST: 10/10 pass`; 0 | `MTE_INTEROP: PASS legs_conforming=8/8`; 0 | SURVIVED |
| M5, line 210: score tolerance `< 1e-9` → `< 1.0` | Small-delta score negative control | `MTE_SELFTEST: 10/10 pass`; 0 | `MTE_INTEROP: PASS legs_conforming=8/8`; 0 | SURVIVED |
| M6, lines 211–212: ledger predicate → `True` | Ledger negative controls | `MTE_SELFTEST: 7/10 pass`; 1 | `MTE_INTEROP: PASS legs_conforming=8/8`; 0 | KILLED |
| M7, lines 173–174: `schema_errors()` → `return []` | Schema negative controls | `MTE_SELFTEST: 6/10 pass`; 1 | `MTE_INTEROP: PASS legs_conforming=8/8`; 0 | KILLED |

M2 sample observed detail:

```text
MTE_LEG bash-mado-verify: FAILS (schema=ok official_score=40 tameshi_score=40.0 official_killed=0 recorded_killed=4 official_valid=10 recorded_defects=10)
```

Timeout preserves detected-score credit in the official library, so it is the killed-count comparison that detects this mutation.

M3b sample observed detail:

```text
MTE_LEG bash-checklist-run: FAILS (schema=invalid:0 is less than the minimum of 1|0 is less than the minimum of 1 official_score=46.666666666666664 tameshi_score=46.666666666666664 official_killed=7 recorded_killed=7 official_valid=15 recorded_defects=15)
```

M6 failed cases: `inconclusive-leaves-denominator`, `ledger-count-mismatch`, `no-ledger-row`. M7 failed cases: `tameshi-vocabulary-status`, `line-zero-location`, `missing-thresholds`, `bad-schema-version`.

## Missing checks and materiality

### M1 — INCONCLUSIVE mapping is not exercised

`STATUS` is defined at line 58 and consulted only by `leg_report()` at line 139. The selftest's inconclusive case at lines 311–312 supplies literal `RuntimeError`; it does not exercise that mapping. The eight kept fleet legs contain no INCONCLUSIVE verdicts. Consequently neither detector sees a change to this entry.

The distinction is material: the vendored metrics implementation counts Timeout in `totalDetected = timeout + killed`, whereas RuntimeError contributes to invalid mutants. This is not an interchangeable spelling.

Smallest correction: a synthetic leg routed through the real `leg_report()` with an INCONCLUSIVE result, asserting the emitted status and resulting official invalid count. Amendment 2 already supplies an emitter-level case that kills M1.

### M3a and M4 — no emitter location oracle

The official schema bounds positions to integers starting at one; it does not establish correspondence to source text or a nonempty range. Metrics/count comparisons do not establish location fidelity either. The old selftest constructs locations manually instead of exercising `position()` and `leg_report()`.

Commands exercised for concrete artifact evidence:

```sh
/tmp/c2m/venv/bin/python /tmp/C2Mutants-r25/tools/mte-interop.py --check --workdir /tmp/c2m/work/regression --emit /tmp/c2m/emit-pristine
# Same command under M3a and M4, with emit-M3a / emit-M4 destinations.
```

All three exited 0. For `js-kimi-census` D1, the true old text starts at line 105, column 70:

| Bytes | Emitted start | Emitted end |
|---|---|---|
| Pristine | `(105,70)` | `(105,97)` |
| M3a | `(105,71)` | `(105,98)` |
| M4 | `(105,70)` | `(105,70)` |

Thus a shifted range and a zero-width range both conform. Smallest correction: emitter fixtures asserting exact one-based, end-exclusive coordinates, including an indented and multiline old string. Amendment 2's `emitter-locations` case kills both.

### M5 — score tolerance lacks a narrow-delta negative control

The negative case uniquely requiring the score arm has a roughly 33.33-point discrepancy. It does not distinguish `1e-9` from `1.0`. Replacing only the judge's tolerance and running the same `--selftest` command produced:

| Tolerance | Pinned output; exit | Amendment-2 output; exit |
|---|---|---|
| `1e-9`, `1.0`, `10.0`, `30.0`, `33.0`, `33.3` | `10/10 pass`; 0 | `16/16 pass`; 0 |
| `33.4`, `34.0` | `9/10 pass`; 1 | `15/16 pass`; 1 |

At the last two values, `timeout-is-not-a-tameshi-kill` fails. This bounds only the exercised cases; it is not evidence that such tolerances are acceptable.

Smallest correction, experimentally checked in scratch: add `narrow-score-delta`, a 200-mutant report with all statuses Killed, but one statusReason reporting SURVIVED. Official score is 100.0; the reason-derived fraction is 99.5. Supply matching official ledger counts so the score arm must reject the discrepancy independently. On amendment 2, supply a per-mutant table of KILLED for all IDs.

Observed scratch-only check-addition results:

```text
Pinned, added case:          MTE_SELFTEST: 11/11 pass; exit 0
Pinned, added case + M5:     MTE_SELFTEST: 10/11 pass; exit 1
Amendment 2, added case:     MTE_SELFTEST: 17/17 pass; exit 0
Amendment 2, added case + M5: MTE_SELFTEST: 16/17 pass; exit 1
```

Only `narrow-score-delta` fails under M5. No such check was integrated.

## Supplementary probes and limitations

A synthetic 200-defect leg containing 99 KILLED, 100 SURVIVED, and one INCONCLUSIVE was tested. **Its pristine baseline fails**, so it is not counted as a killed-mutant result:

```text
MTE_LEG synth: FAILS (schema=ok official_score=49.74874371859296 tameshi_score=49.74874371859296 official_killed=99 recorded_killed=99 official_valid=199 recorded_defects=200)
```

The pinned ledger predicate compares valid count against all recorded defects; RuntimeError is invalid, explaining the mismatch. Under M1 alone, the leg still fails, now with official score 50 versus 49.74874371859296. Combined M1+M5 accepts that discrepancy:

```text
MTE_LEG synth: CONFORMS (schema=ok official_score=50 tameshi_score=49.74874371859296 official_killed=99 recorded_killed=99 official_valid=200 recorded_defects=200)
MTE_INTEROP: PASS legs_conforming=1/1
```

This is supplementary interaction evidence, not an independent single-mutant kill claim.

A doctored regression table (`recorded-killed=8` → `3` on the first matching leg) made pristine check fail 7/8, while M6 passed 8/8. Combining the real column-underflow mutation with skipped schema validation made check pass 8/8 where column-underflow alone failed 1/8. An initial supplementary attempt at the latter was a no-op replacement and is excluded; the corrected attempt asserted and applied the full unique line replacement.

## Amendment-2 comparison

While the probe ran, the lane advanced to `09dc114` with emitter fixtures and stronger ledger/per-mutant checks. A second private clone, `/tmp/c2m-head`, was detached at that commit. A fresh runner workdir was retained at `/tmp/c2m/headwork/regression`; its regression exited 0, eight cases passed.

Commands on that private clone:

```sh
/tmp/c2m/venv/bin/python /tmp/c2m-head/tools/mte-interop.py --selftest
/tmp/c2m/venv/bin/python /tmp/c2m-head/tools/mte-interop.py --check --workdir /tmp/c2m/headwork/regression
```

Baseline: `MTE_SELFTEST: 16/16 pass` and `MTE_INTEROP: PASS legs_conforming=8/8`, both exit 0.

| Mutant | Selftest output; exit | Check output; exit | Verdict |
|---|---|---|---|
| M1 | 15/16 pass; 1 | PASS 8/8; 0 | KILLED by emitter-inconclusive case |
| M2 | 14/16 pass; 1 | FAIL 0/8; 1 | KILLED |
| M3a | 15/16 pass; 1 | PASS 8/8; 0 | KILLED by emitter-locations |
| M3b | 14/16 pass; 1 | FAIL 1/8; 1 | KILLED |
| M4 | 15/16 pass; 1 | PASS 8/8; 0 | KILLED by emitter-locations |
| M5 | 16/16 pass; 0 | PASS 8/8; 0 | SURVIVED |
| M6 | 12/16 pass; 1 | PASS 8/8; 0 | KILLED |
| M7 | 12/16 pass; 1 | PASS 8/8; 0 | KILLED |

Full supplementary result summary: `/tmp/c2m/head-results.json`.

## Hashes and restoration evidence

Pinned pristine and restored SHA-256:

```text
311448d92c10891e2fd9513586c203d4d245f94559ab7843de48bef4de1db422
```

Every assigned-revision mutant was restored to that hash. Mutated hashes:

```text
M1  54d23627e2f85188e0392ce77e63ae60e2e8e4e9051a625801113f8d2b504ebe
M2  21143462b82bc25a2f80f900dbcf6e817d1aad2f61cb5878efa7beb95271d6d1
M3a 41057560dabb8461d5de77b764839875c32ace22469dc57feceb27030b5f15fa
M3b 535324eea50cbc1fd3e7cf4b7cf4a70d3b73a0d8b25c10d3f1225024560ceadf
M4  64800f85681f954c23de42a3239d516ff1d0e6524da0298665bc5139cb0137d5
M5  ed31c9ad01d9ee5c4840fbec59b75b8b41446e6de2c95f875227f70270a0079d
M6  84725bf97ce061273ec3c8ea58d70d21d7fad721dc9ad0c49fda03ea38bc84af
M7  87cbd429e666f877ca50faf3a4defa5d10e6fbf16898cf935274ce3628b5185d
```

Amendment-2 pristine and restored SHA-256:

```text
8c24255c9e482751772e958e5ba9a615891ca7e5dfc9426d2fb5667ceae65552
```

Supplementary mutated hashes:

```text
M1  afaab8b0d6007e64e9abb46864fdab7c7da0242e8b11ed7346fe2318d0442084
M2  4d3f00b69f802aa7bfbfe0cd6a8bf8d3fb459495394b9845b7c1b10bdd1a1786
M3a 7b457c3429a7207fce03378aceb61fe4c05299c3fc7165013ac665782336048e
M3b edaccf963fa9aa44c8aa2c4d8cd3839715ef679794ec20582017304fb8f54be0
M4  a226716fdd5ae7178b862aa7293fcad39ea4e3ca5310e05f5f78eb4b26d32ab9
M5  de1c741dcb81f206a27450dce71435b860b75651de2121bfc104f1b4192b32b8
M6  36eaebabeaa89245016ec52b8f327df90390b8ff19c2cc31a46ac8a22d905596
M7  87895295bc975640cc1b2b3ef05fa989fcdae40d71b037a1a6107b3eafd1f5b0
```

Final restored-byte reruns, after all supplementary checks and scratch-only proposed-case edits:

```text
Pinned restored:      --selftest exit 0, MTE_SELFTEST: 10/10 pass
Pinned restored:      --check exit 0, MTE_INTEROP: PASS legs_conforming=8/8
Amendment 2 restored: --selftest exit 0, MTE_SELFTEST: 16/16 pass
Amendment 2 restored: --check exit 0, MTE_INTEROP: PASS legs_conforming=8/8
```

The pinned clone was observed clean after restoration. Production source files, lane Git index, and sibling source were not modified by this probe. The report is the only retained lane-file deliverable.
