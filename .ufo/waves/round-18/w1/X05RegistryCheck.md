# X05 — registry-check finite timeouts and descendant cleanup

## Scope and behavior

Changed only `tools/registry-check.py` in the round-18 staged tree. `timeout_s` parsing now rejects JSON `NaN`, `Infinity`, and `-Infinity` with a strict `parse_constant` callback; schema validation separately rejects booleans, non-numeric values, non-finite numbers (including `1e999`), zero, and negatives. Validation errors identify the row name and `timeout_s`.

On Linux, before a row starts, the checker requires child-subreaper and pidfd support and snapshots its pre-existing direct-child identities. Cleanup walks visible `/proc` process leaders by ancestry, revalidates start time and row ownership before and after opening a pidfd, signals only those identities, and reaps only row-owned adopted zombies. It runs after timeout and after a normal leader exit, covering `setsid`, `setpgid`, and double-fork descendants. Output draining and the final wait are bounded; if cleanup cannot establish that no visible row descendants remain, the row is not held. The detached-checkout and 7–40-hex source-revision contracts now have discriminating selftests.

Key staged source locations: finite timeout validation and row diagnostics `tools/registry-check.py:234-249`; strict parser and row-location diagnostics `:288-357`; subreaper, `/proc` identity and pidfd cleanup `:383-602`; bounded drain and row completion/timeout handling `:605-719`; detached/source/numeric/process falsifiers `:1149-1259`, `:1474-1577`, `:1605-1617`.

## Verification evidence

All commands ran in scratch clones or selftest `/tmp` fixtures, with inherited environment cleared using `env -i`.

| Check | Exit | Retained result |
|---|---:|---|
| Base `python3 tools/registry-check.py --selftest` at `183f87b899e6cae46be98d251cbc87fb5118f6ca` | 0 | `SELFTEST: PASS (34 cases)` |
| Staged `python3 tools/registry-check.py --selftest` | 0 | `SELFTEST: PASS (46 cases)` |
| Base clone `python3 tools/registry-check.py --json` | 0 | `held=28/28 superseded=1` |
| Staged clone `python3 tools/registry-check.py --json` | 0 | `held=28/28 superseded=1` |
| Staged monitor `python3 tools/registry-check.py --rev 183f87b899e6cae46be98d251cbc87fb5118f6ca --json` | 0 | `held=28/28 superseded=1`; `rev_resolved` exactly matched the requested revision |

The staged selftest recorded `timeout-kills-setsid-pipe PASS (exit=1 elapsed=1.203s survivor=False marker=False)`, `timeout-kills-setpgid-pipe PASS (exit=1 elapsed=1.279s survivor=False marker=False)`, and `normal-exit-kills-double-fork PASS (exit=0 survivor=False)`. The synthetic drain and stale-identity checks passed with `communicate_timeout=0.5 wait_timeout=0.5` and `stale_identity_rejected=True signals=0`.

### Mutant falsifiers

Each mutation below was applied only to a separate `/tmp` script copy and exercised with that copy's `--selftest`. Every pristine staged case passed above; every listed mutant selftest exited 1 with the indicated case failure.

| Mutant | Exit | Falsifying output |
|---|---:|---|
| Detached checkout changed to `git reset -q --hard` | 1 | `rev-clone-detached FAIL (exit=1)` |
| `SOURCE_RE` lower bound changed from 7 to 1 hex digit | 1 | `short-source-revision FAIL (exit=0)` |
| Removed `parse_constant=_reject_json_constant` | 1 | `timeout-nan`, `timeout-infinity`, and `timeout-negative-infinity` each `FAIL (exit=2)` because the strict-constant diagnostic disappeared |
| Removed `math.isfinite(ts)` | 1 | `timeout-overflow FAIL (exit=1)` |
| Removed the explicit bool exclusion | 1 | `timeout-boolean FAIL (exit=0)` |
| Restricted ownership to the original process group | 1 | `timeout-kills-setsid-pipe`, `timeout-kills-setpgid-pipe`, and `normal-exit-kills-double-fork` failed with `survivor=True` |
| Removed the timeout from bounded `communicate` | 1 | `bounded-pipe-drain FAIL (communicate_timeout=None wait_timeout=None)` |
| Skipped cleanup after a normal row exit | 1 | `normal-exit-kills-double-fork FAIL (exit=0 survivor=True)` |
| Removed the post-`pidfd_open` start-time revalidation | 1 | `pidfd-revalidates-starttime FAIL (stale_identity_rejected=False signals=1)` |

## Risks and residual limits

The cleanup guarantee depends on Linux `/proc`, `PR_SET_CHILD_SUBREAPER`, and pidfd support; if subreaper/pidfd setup fails, row execution is reported unavailable rather than falling back to process-group-only cleanup. A double-forked descendant cannot reparent past an active subreaper. A descendant that changes UID or is hidden/unreadable in procfs may be unobservable or unkillable. Rechecking start time and sending through a pidfd closes the ordinary PID-reuse window, but start-time tick granularity leaves a same-tick race before the pidfd is opened.

No tools were installed or updated. No live-lane gate, sibling-repository write, or Git write in the lane was run.

Verdict: **built** — staged selftest 46/46, every targeted mutant was falsified, and full-registry held counts remained 28/28 both live-clone and pinned-revision modes.