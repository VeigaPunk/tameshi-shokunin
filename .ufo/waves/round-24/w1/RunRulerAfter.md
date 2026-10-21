# RunRulerAfter — round-24 W1 ruler run (calibration)

Verdict: **11/11 discriminated**, ruler exit **0**, schema `tameshi-r24-hardening-v1`, at implementation rev `c8c5b88c8e961a929cdc351b95a7074c76958909`. No defects, no non-discriminating predicates, no hangs observed.

## Exact invocation

- cwd: `/tmp`
- clone (private, no-hardlinks, detached):

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/RunRulerAfter-r24
git -C /tmp/RunRulerAfter-r24 checkout -q --detach c8c5b88c8e961a929cdc351b95a7074c76958909
# rev-parse HEAD → c8c5b88c8e961a929cdc351b95a7074c76958909
```

- argv (exact):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-24/measure.py --repo /tmp/RunRulerAfter-r24
```

- exit: `0`
- wall: ~11.4 s

## Result

Decisive lines (ruler stdout):

```json
{ "discriminated": 11, "total": 11, "schema": "tameshi-r24-hardening-v1" }
```

## Per-row

| id | name | discriminated | decisive observation |
|----|------|---------------|----------------------|
| K1 | argv-name-insensitive | true | mutant `exit=1`, control `0`, restored `0`; failing case `CASE argv-swapped-between-names FAIL`; `COMMAND_BINDING_SELFTEST: 43/44 pass` |
| K2 | argv-casefold | true | mutant `exit=1`; `CASE argv-case-only FAIL` |
| K3 | exit-negative-ignored | true | mutant `exit=1`; `CASE negative-exit-mismatch FAIL` |
| K4 | stdout-any-token | true | mutant `exit=1`; `CASE all-of-tokens FAIL` |
| K5 | frozen-clean-substitution | true | row `command-binding-frozen-clean-pinned`: control `true`, substituted `false` |
| K6 | source-read-red-substitution | true | row `command-binding-source-read-red-pinned`: control `true`, substituted `false` |
| K7 | runner-not-held-refused | true | `exit=1`, `finding_ids=["RUNNER_NOT_HELD"]`, `bundle_written=false`, `control_ok=true` |
| K8 | runner-cleanup-refused | true | `exit=1`, `finding_ids=["RUNNER_CLEANUP_FAILED"]`, `bundle_written=false`, `control_ok=true` |
| K9 | stream-limit-refused | true | `exit=1`, `finding_ids=["STREAM_LIMIT"]`, `bundle_written=false`, `control_ok=true` |
| K10 | live-dependent-listed | true | `exit=0`; report `live_dependent=["one"]`, `rows=1`, `refused_rows=[]`, `bundle_sha256=5c9aaf714c6d9339ce48cabf184d165524b8e496183729de3b684fc9c50ac245` |
| K11 | fleet-root-realpath | true | `exit=0`; plan `fleet_root=/tmp/tameshi-r24-measure-01u0aqib/replay/fleet`, `repo=.../fleet/lane-shokunin`, `siblings=[.../fleet/other-shokunin]` |

## Falsification statement

Attacked: (a) that "11/11" could hide a control failure — every mutant row carries `control_exit: 0` / `restored_exit: 0` or `control_ok: true`, so each discrimination is genuinely attributable to the injected predicate; (b) that exit 0 could mask a skip — `total` is 11 with a row for each of K1–K11, none absent; (c) clone identity — `rev-parse HEAD` returned exactly the pinned REV before the run. Counterexamples found: none.

## Scope / notes

- All commands ran only in `/tmp/RunRulerAfter-r24` and `/tmp`; nothing executed in the production tree except the measure.py script itself read from its canonical path (per assignment argv).
- No files written outside this report; no git write commands in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; no sibling lanes touched.
- No tool installs or upgrades were needed (recorded per operator directive: none performed).
- Not claimed: producer authentication, promotion, R17-CMD-BIND closure, numeric score uplift.
