# S03 — registry-check baseline at 183f87b (round 18, wave 1)

Purpose: baseline the C2 no-harm ruler (`python3 tools/registry-check.py --rev REV --json`
held/total) at the round-18 dispatch tip, default and `--tag baseline`, and record the
registry bytes those two runs grade.

Environment: python 3.14.8, git 2.56.0. Clone at
`/tmp/tameshi-r18w1-S03BaselineRegistry-scE4cw/fleet/tameshi-shokunin`, checked out at
`183f87b899e6cae46be98d251cbc87fb5118f6ca` (rev-parse confirms). All git invocations
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`; nothing written in the lane.

## Registry identity at the rev

```
$ sha256sum tools/registry.json                       # in the clone at 183f87b
98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630  tools/registry.json
$ git -C <lane> show 183f87b...:tools/registry.json | sha256sum
98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630  -
```

Both runs report `"registry_sha256": "98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630"`.
Composition (`tools/registry.json:2`, schema `tameshi-entry-registry-v1`): 29 rows,
28 active / 1 superseded; tag census `baseline` 24, `new-r17` 5, `fleet-live` 1.
Two rows declare `"external": true` (`pin-disposition-read` line 106, `verify-round15`).

## Run 1 — default (all rows)

Command (from the clone root):

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  python3 tools/registry-check.py --rev 183f87b899e6cae46be98d251cbc87fb5118f6ca --json
```

- exit **0**; wall **138.379 s** (`date +%s%N` around the call; per-row `elapsed_s` sum 138.19 s).
- `REGISTRY_CHECK: held=28/28 superseded=1` (stderr trailer).
- 29 rows selected/run: 28 active + 1 superseded.
- `rev_resolved=183f87b899e6cae46be98d251cbc87fb5118f6ca`, `registry_sha256=98bdc23...`.
- **differs rows (active): none.**
- Superseded row (see below): `ROW evidence-disposition-round14-superseded superseded expect=0 got=2`.
- Slowest rows: `mutate-and-run-regression` 115.936 s, `mutate-and-run-selftest` 5.370 s,
  `measure-round17-selftest` 3.382 s, `registry-check-selftest` 2.999 s. The regression sweep
  alone is 83.8 % of wall time; all other 25 rows total ~22 s.

## Run 2 — `--tag baseline`

```
env -u ... python3 tools/registry-check.py --rev 183f87b... --tag baseline --json
```

- exit **0**; wall **132.460 s** (row-sum 132.25 s; `mutate-and-run-regression` 117.772 s).
- `held=23/23`, `superseded=1`, 24 rows selected (23 active + the 1 superseded, which also carries
  `baseline`), `tags: ["baseline"]`.
- **differs rows (active): none.**
- Same single superseded line: `ROW evidence-disposition-round14-superseded superseded expect=0 got=2`.

Tag selection semantics confirmed in source: `selected = [r for r in rows if wanted.intersection(r.get("tags", []))]`
(`tools/registry-check.py:526-537`), and held/total count only `status == "active"`
(`tools/registry-check.py:544-550`), so tag-filtered active denominator is 23, not 24.

## Superseded rows (the only observed non-held outcome)

One row: `evidence-disposition-round14-superseded` (`tools/registry.json:250`),
`superseded_by: evidence-disposition-round17`, `expect.exit=0`.

Observed `got=2`, with the row's own stdout ending:

```
"expectation": null,
"id": "expected_input_digest_mismatch",
"status": "could_not_evaluate",
"tool": "evidence-disposition.py r17.1 (tameshi-shokunin, 2026-10-20): hardened v2 historical inputs"
```

So the round-14 dispositions file no longer matches the hardened v2 input digests; the row is
correctly marked superseded and is excluded from N/M. It is a *stale registered outcome kept
visible*, not an active regression: no active row differed in either run. Flagging only because
the human dashboard line carries `got=2` while the trailer says `held=28/28`.

Corroborating C1 baseline in the same run: `mutate-and-run-regression` stdout tail reads
`REGRESSION: PASS (cases=7 passed=7; ledger legs exact: ...)` — consistent with the C1 claim
that the recorded mutation-case count at this rev is 7 before the eighth leg lands.

## Hermeticity guard observation (adjacent to C2 no-harm)

`--rev` rejects an undeclared absolute argv path under "the live fleet root"
(`_argv_outside_fleet`, `tools/registry-check.py:326-338`; applied in `run_row`, `:356-365`).
The reference root is `os.path.dirname(os.path.realpath(root_requested))`
(`tools/registry-check.py:1267`), i.e. the **executing copy's** parent directory — not the source
lane's. Empirically, with a crafted registry in /tmp (outside the lane):

| invocation | row argv token | result |
|---|---|---|
| live-lane script, cwd=/tmp | `/home/vgpnk/Projects/shokunin` | `got=non-hermetic`, exit 1 |
| clone script (this baseline's mode) | `/home/vgpnk/Projects/shokunin` | `held`, got 0, exit 0 |
| clone script | `/tmp/tameshi-r18w1-.../fleet` | `got=non-hermetic`, exit 1 |

Observed consequence: when registry-check is run from a /tmp clone (the contract's
committed-bytes mode), an argv naming the live fleet root is not flagged; when run from the
lane it is. No registry row in this baseline is affected in a way that changes held counting —
`pin-disposition-read` and `verify-round15` both declare `external: true`, so they are exempt by
design. [INFERENCE] Any future row that silently depends on live-fleet absolute state would be
caught only by the live-lane invocation.

`pin-disposition-read` shows the declared external dependency concretely: under `--rev` it ran in
0.071 s and its stdout tail cites live bytes
(`/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs`, `"status": "unchanged"`).

## Tools installed/updated

None.

## Verdict

holds — at 183f87b899e6cae46be98d251cbc87fb5118f6ca the registry-check baseline is 28/28 active rows held (exit 0, 138.4 s) and 23/23 under `--tag baseline` (exit 0, 132.5 s), with 0 active differs rows, 1 correctly-superseded row observed at exit 2, and registry sha256 98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630.
