# MutateLeg — seventh-ledger-leg mutation probe

- Seat: `TameshiR16.MutateLeg`; artifact-only advisory evidence, not a round judgment.
- Axes: **depth** (seventh-leg detector sensitivity) + **calibration** (attribution, survivor reporting, exact-byte restoration).
- Source: `c699c8c36d6e4eca4b796b81a8247904aa145ec8:tools/mutate-and-run.sh`.
- Source SHA-256: `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594`; 84,108 bytes.
- Owned scratch: `/tmp/tameshi-r16w2-MutateLeg-r73cRq`. Only the requested report was written in the lane; all mutated files, fixture repositories, helper and logs were under this scratch root. No lane source edits, commits, staging, CLI launches, installations or upgrades were performed. The runner's hermetic selftest itself makes fixture commits only inside scratch.

## Results

Every row used the same detector on pristine, independently mutated, and restored bytes. Four runner copies were used; each mutation was a single source change and was restored before the restoration run. Selftests ran concurrently in each phase; no detached/background jobs or delegation were used.

| Probe | Detector | Pristine | Mutated | Restored | Attribution |
|---|---|---|---|---|---|
| (a) one `TABLE_ROUNDGATE` cell flipped | `--selftest` | exit 0, `81/81 pass` | **exit 1, `80/81 pass`** | exit 0, `81/81 pass` | **KILLED** |
| (b) seventh `lent` tuple deleted | `--selftest` | exit 0, `81/81 pass` | **exit 0, `80/80 pass`** | exit 0, `81/81 pass` | **SURVIVED** |
| (c) seventh spec `-s` check deleted | `--selftest` | exit 0, `81/81 pass` | **exit 0, `81/81 pass`** | exit 0, `81/81 pass` | **SURVIVED** |
| (d) guarded suite replaced by bare Node | `--selftest`, clean Git environment | exit 0, `81/81 pass` | **exit 0, `81/81 pass`** | exit 0, `81/81 pass` | **SURVIVED this detector** |
| (d) same suite mutation | `--regression`, exported throwaway `GIT_DIR` | **exit 2, SETUP** | **exit 2, SETUP** | **exit 2, SETUP** | **INCONCLUSIVE**, not a kill |

No `--regression` run was made for (a)–(c); their survivor/kill claims are scoped to the exercised selftest. The contaminated (d) regression never reached any suite. No detector timed out.

## Mutants, expected detector, and observed lines

All source line numbers below refer to the committed source, not the shortened (b) mutant.

### (a) Recorded seventh-leg cell — killed

At `tools/mutate-and-run.sh:570`, changed only `A1:KILLED` to `A1:SURVIVED` in `TABLE_ROUNDGATE`. This changes its recorded killed count from five to four. Expected detector: `--selftest`'s seventh leg tuple at `:1667` still expects `10:5`, and the committed count checks at `:1682-1683` feed `st` at `:1685`.

Actual mutant output, `/tmp/tameshi-r16w2-MutateLeg-r73cRq/logs/a-mutated-selftest.out:78,82-83`:

```text
FAIL embedded leg js-round-gate: spec and recorded table agree
MUTATE_SELFTEST: 80/81 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r16w2-MutateLeg-r73cRq/runtime/a-mutated-selftest/tameshi-r4-2-selftest.KFuy3L)
```

Exit 1; pristine and restored exits 0. This is an attributable kill.

### (b) Seventh selftest leg-cut tuple — survived

Deleted exactly `tools/mutate-and-run.sh:1667`:

```text
    'js-round-gate:js-round-gate.spec:TABLE_ROUNDGATE:10:5'
```

Intended detector: `--selftest` should expose the loss of its seventh-leg check if its inventory is independently enforced. Instead, its loop at `:1669-1686` tests only the remaining tuples; the final success condition at `:1693-1697` uses accumulated failures, not a fixed test-count assertion.

Actual mutant output, `/tmp/tameshi-r16w2-MutateLeg-r73cRq/logs/b-mutated-selftest.out:71,77-82`:

```text
PASS embedded leg specs: seven files written
PASS embedded leg js-claims-check: spec and recorded table agree
PASS help exits 0
PASS missing --target exits 64
PASS --regression refuses --target (exit 64)
MUTATE_SELFTEST: 80/80 pass
VERDICT: PASS
```

There is no `embedded leg js-round-gate` result in this mutant's output. Exit 0, versus pristine/restored `81/81 pass`, exit 0. **Coverage finding:** deleting the seventh leg's selftest check reduces the denominator and stays green. The `seven files written` message does not enforce seven checked tuples.

### (c) Seventh spec existence predicate — survived

At `tools/mutate-and-run.sh:967`, replaced `     && -s "$d/js-round-gate.spec" ]]` with `  ]]`, preserving the preceding continuation and the other six checks.

Intended detector: `--selftest` against the removed seventh-spec guard. Actual mutant output, `/tmp/tameshi-r16w2-MutateLeg-r73cRq/logs/c-mutated-selftest.out:71,78,82-83`:

```text
PASS embedded leg specs: seven files written
PASS embedded leg js-round-gate: spec and recorded table agree
MUTATE_SELFTEST: 81/81 pass
VERDICT: PASS
```

Exit 0 in all three phases. **Coverage finding, narrowly scoped:** removal of this existence predicate is not detected. The generator at `:905-963` still emits the file, and the selftest still parses it at `:1673`, so this run does not establish that a missing or empty spec would pass the remaining checks. No missing-file second mutation was introduced.

### (d) Guarded seventh suite replaced by bare Node — selftest survivor; contaminated regression inconclusive

Replaced only the suite argument at `tools/mutate-and-run.sh:1221`:

```text
# Original suite argument
'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest'
# Mutated suite argument
'node "$MUTANT" --selftest'
```

Expected distinguishing detector: `--regression` with a caller-exported throwaway `GIT_DIR`, such that the guarded control excludes that contamination and the bare suite does not. The clean-environment selftest does not execute this real seventh-ledger suite, and remained `81/81 pass`, exit 0 in all three phases (`logs/d-<phase>-selftest.out:82-83`).

The required contaminated regression was actually executed in all three phases with:

```text
GIT_DIR=/tmp/tameshi-r16w2-MutateLeg-r73cRq/throwaway.git
```

This was an initialized, empty, bare throwaway repository (`git init --bare -q`, exit 0). Actual mutant output, `/tmp/tameshi-r16w2-MutateLeg-r73cRq/logs/d-mutated-regression-gitdir.out:11-13`:

```text
REGRESSION_CASE js-round-gate: SETUP (revision not found: /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5)
REGRESSION: SETUP (cases=7 passed=0 cannot-verify=7)
REGRESSION_WORKDIR: /tmp/tameshi-r16w2-MutateLeg-r73cRq/runs/d-mutated-regression-gitdir (kept)
```

The first six legs also report `revision not found` at log lines 5–10. Pristine and restored contaminated runs have the same seventh-leg line at `:11`, the same final SETUP line at `:12`, and exit 2.

The outer materializer invokes `git -C "$repo" rev-parse ...` without clearing `GIT_DIR` at committed `:1000-1002`, before reaching the seventh suite's `env -i` guard at `:1221`. Thus a baseline SETUP cannot be credited as detecting this suite mutation. This is an **INCONCLUSIVE** regression probe, not KILLED and not proof of a regression survivor.

To distinguish pollution from an unavailable seventh pin, this read-only command was also executed (exit 0):

```sh
env -u GIT_DIR git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs | /usr/bin/sha256sum
```

Actual output:

```text
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9  -
```

That matches the committed `PIN_ROUNDGATE` at `tools/mutate-and-run.sh:562`. No shim was added to clear `GIT_DIR` for materialization: doing so would change the requested detector and conceal this baseline limitation.

## Commands and isolation

The source was obtained with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c699c8c36d6e4eca4b796b81a8247904aa145ec8:tools/mutate-and-run.sh` (exit 0) and materialized via the write tool into `/tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/mutate-and-run.sh`. Four byte-identical scratch copies were created as `probe-a.sh` through `probe-d.sh`, then edited and reversed with exact line patches. Each detector ran with CWD `/tmp/tameshi-r16w2-MutateLeg-r73cRq`.

The detector process environment copied the session environment, removed all `GIT_*` variables plus `BASH_ENV`, `ENV`, `SHELLOPTS`, and `BASHOPTS`, then set:

```text
PATH=/tmp/tameshi-r16w2-MutateLeg-r73cRq/bin:<inherited PATH>
HOME=/tmp/tameshi-r16w2-MutateLeg-r73cRq/home
TMPDIR=/tmp/tameshi-r16w2-MutateLeg-r73cRq/runtime/tmp
LC_ALL=C
GIT_CONFIG_NOSYSTEM=1
PROBE_CASE=<case>-<phase>-<mode>[-gitdir]
```

Only the three contaminated regression invocations then exported the `GIT_DIR` shown above. `<phase>` labels reflect the actual pristine/mutated/restored bytes; these were not unchanged-byte reruns.

A 264-byte scratch-only `bin/mktemp` helper redirected the runner's hard-coded `/tmp/tameshi-*` templates into `/tmp/tameshi-r16w2-MutateLeg-r73cRq/runtime/$PROBE_CASE/`, then exec'd `/usr/bin/mktemp`. This kept the runner's own fixtures inside the assigned scratch root without changing runner bytes. Source:

```bash
#!/usr/bin/env bash
set -eu
root='/tmp/tameshi-r16w2-MutateLeg-r73cRq'/runtime/${PROBE_CASE:-misc}
mkdir -p "$root"
args=()
for arg in "$@"; do
  case "$arg" in /tmp/tameshi-*) arg="$root/${arg##*/}" ;; esac
  args+=("$arg")
done
exec /usr/bin/mktemp "${args[@]}"
```

Read-only symlinks under `/tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/` named `kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, and `mado-shokunin` pointed to the corresponding original repositories, solely for the runner's Git object-store lookup. No sibling gate was run in a sibling tree.

Exact detector argv and exits (environment as above; `GIT_DIR` only where labeled):

- `a/pristine/selftest`: exit **0**; 5.256 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-a.sh --selftest
  ```
- `a/mutated/selftest`: exit **1**; 5.358 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-a.sh --selftest
  ```
- `a/restored/selftest`: exit **0**; 5.252 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-a.sh --selftest
  ```
- `b/pristine/selftest`: exit **0**; 5.252 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-b.sh --selftest
  ```
- `b/mutated/selftest`: exit **0**; 5.354 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-b.sh --selftest
  ```
- `b/restored/selftest`: exit **0**; 5.256 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-b.sh --selftest
  ```
- `c/pristine/selftest`: exit **0**; 5.253 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-c.sh --selftest
  ```
- `c/mutated/selftest`: exit **0**; 5.371 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-c.sh --selftest
  ```
- `c/restored/selftest`: exit **0**; 5.256 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-c.sh --selftest
  ```
- `d/pristine/regression + exported GIT_DIR`: exit **2**; 0.022 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-d.sh --regression --workdir /tmp/tameshi-r16w2-MutateLeg-r73cRq/runs/d-pristine-regression-gitdir
  ```
- `d/pristine/selftest`: exit **0**; 5.254 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-d.sh --selftest
  ```
- `d/mutated/regression + exported GIT_DIR`: exit **2**; 0.025 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-d.sh --regression --workdir /tmp/tameshi-r16w2-MutateLeg-r73cRq/runs/d-mutated-regression-gitdir
  ```
- `d/mutated/selftest`: exit **0**; 5.358 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-d.sh --selftest
  ```
- `d/restored/regression + exported GIT_DIR`: exit **2**; 0.023 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-d.sh --regression --workdir /tmp/tameshi-r16w2-MutateLeg-r73cRq/runs/d-restored-regression-gitdir
  ```
- `d/restored/selftest`: exit **0**; 5.257 s.
  ```sh
  /usr/bin/timeout 120s /usr/bin/bash /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-d.sh --selftest
  ```

The subprocess wrapper also had a 130-second kill-and-reap fallback; it was never used. The 120-second outer timeout was identical between phases. Full outputs and structured command/exit/source-hash records remain in `/tmp/tameshi-r16w2-MutateLeg-r73cRq/logs/` and `/tmp/tameshi-r16w2-MutateLeg-r73cRq/runs.json`; the quoted observations and commands above are embedded here so the finding does not depend on retained `/tmp` files.

## Exact-byte restoration

All four before and restored hashes are `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594`. The observed intermediate mutant hashes are:

| Probe | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| (a) | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` | `5272bc282b8a540384650f369110c567962d8e974d337d3ef9eacf3fce588694` | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` |
| (b) | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` | `d731c94bd07acd83116058af08254dd384b01c79ed01533e7217640076f6ee0a` | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` |
| (c) | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` | `6c92135a6d0ed8f8f8fc6c8cb0a4787021854bedf4f612db91e2bb7ff9856472` | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` |
| (d) | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` | `8438409c1c8e578a205924ed7cc1a88194940fc1910b482c5f0239b9af988bb3` | `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` |

After reversing all four patches, the following command exited 0:

```sh
/usr/bin/sha256sum /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/mutate-and-run.sh /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-a.sh /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-b.sh /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-c.sh /tmp/tameshi-r16w2-MutateLeg-r73cRq/fleet/tameshi-shokunin/tools/probe-d.sh
```

Its five output lines all carry SHA-256 `89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594` (the untouched committed copy and all four restored copies). Each restored selftest separately returned `81/81 pass`, exit 0. The three-phase contaminated regression remains inconclusive exactly as recorded, including after restoration.

## Tooling

Existing tools used: GNU Bash `5.3.20(1)-release`, Git `2.56.0`, Node `v24.21.0`, Python `3.14.8`, and installed coreutils. No installs or upgrades. A prerequisite version pipeline ending in unqualified `timeout --version` exited 125 because this session exposes a `timeout` shell builtin requiring a command; all actual detector bounds explicitly used `/usr/bin/timeout`, so this was not a detector failure.

Verdict: **partial** — the seventh table-cell invariant holds for (a); selftest coverage falls for (b), (c), and guard removal in (d), while the requested GIT_DIR-contaminated regression is inconclusive because pristine already returns SETUP before any suite.
