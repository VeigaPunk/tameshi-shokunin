# R03 — P03/P04 registry-check before-state repro

## Scope and setup

Reproduced the two round-17 surviving mutations against the pristine `tools/registry-check.py` at `183f87b899e6cae46be98d251cbc87fb5118f6ca`. The round-17 mutation table identifies M06 (detached checkout) and M07 (short source revision) as survivors at `.ufo/waves/round-17/w2/MutateRegistryCheck.md:52-53`. Their source anchors at this revision are `tools/registry-check.py:466` and `:96`, respectively.

Scratch fleet-mirror: `/tmp/tameshi-r18w1-R03ReproRC-c5GQSh`. Read-only `git rev-parse HEAD` returned `183f87b899e6cae46be98d251cbc87fb5118f6ca` for pristine, M03, M04, and combined-mutant clones. The pristine file SHA-256 was `0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765`.

Both mutant anchors occurred once in each clone (`grep -c` results: checkout argument `1`, `{7,40}` `1`). Mutations, applied only to scratch copies:

- **P03 / M06:** at `tools/registry-check.py:466`, replace `"checkout", "-q", "--detach", sha` with `"reset", "-q", "--hard", sha`.
- **P04 / M07:** at `tools/registry-check.py:96`, replace `[0-9a-f]{7,40}` with `[0-9a-f]{1,40}`.

## Selftest evidence

Each run was from its clone directory, with inherited Git selectors scrubbed:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  timeout 300 python3 tools/registry-check.py --selftest
```

| Clone state | Process exit | Selftest tally | Failure cases |
|---|---:|---:|---:|
| Pristine | 0 | `SELFTEST: PASS (34 cases)` | 0 |
| P03 detached-checkout mutant only | 0 | `SELFTEST: PASS (34 cases)` | 0 |
| P04 short-revision mutant only | 0 | `SELFTEST: PASS (34 cases)` | 0 |
| Both mutants together | 0 | `SELFTEST: PASS (34 cases)` | 0 |

Pristine command also reported `sha256sum` above; its captured stderr was empty. Mutated runs printed all 34 `SELFTEST_CASE ... PASS` lines and the PASS summary; none timed out.

## Result, residual risk, verification gap

Under the C2 probe rule, an open guard-removal probe is one whose owning selftest still exits 0. Both P03 and P04 are therefore **open at this before-state**; the assigned selftest does not distinguish either mutation, including when both are present. This does not falsify C2's before-state for these two probes; it reproduces it. The verification was scoped to mutant survival in `--selftest`; no separate runtime witness was run in this reproduction.

Verdict: **holds** — P03/P04 before-state reproduced (both mutants survive, 34/34 selftest cases pass).
