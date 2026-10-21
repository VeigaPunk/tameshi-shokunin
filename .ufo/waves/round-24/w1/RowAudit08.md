# RowAudit08 — round24 replay row audit (five named rows)

Verdict: **no false acceptance found.** All five audited rows bind requirement →
receipt → observation, their exits equal `expect.exit`, every required stdout
token is literally present in the retained full stdout, and `held=true`.
One weak-but-not-exploitable requirement token (round19) and three scope bounds
are recorded below. No correction is required for the audited artifacts.

Audited rows: `witness-metadata-check`, `context-capture-selftest`,
`verify-round15`, `round19-correction-ruler-selftest`,
`round21-coldread-selector-selftest`.

## 1. Requirement identity (observations.requirement vs round-23/requirements.json)

For every row, `.rows[].requirement` in
`.ufo/evidence/round-24/replay/observations.json` is **byte-equal** to the
corresponding entry of `.ufo/evidence/round-23/requirements.json`
(`req_equal=true`, `argv_equal=true`, and the five rows carry exactly the keys
`name`/`argv`/`expect`). The same equality holds for all 43 rows.

The frozen file itself is anchored, not merely asserted:

- `cmp` of the active-row projection (`{name,argv,expect}`) of
  `git show 28cae179e4dc2c1fa7f032a79cdddf0b5d862d76:tools/registry.json`
  against `.ufo/evidence/round-23/requirements.json` → **IDENTICAL**.
- `registry-baseline.json` is byte-identical to that registry blob and hashes to
  `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a`, the
  `registry_sha256` recorded in both `requirements.json` and `observations.json`.
- `28cae17` is an ancestor of the round23 base `6a1821a`
  (`git merge-base --is-ancestor` → 0).
- 47 baseline rows, 47 unique names, 43 active — no name shadowing in
  `run_replay`'s `{name: row}` projection.

`tools/registry-replay.py:135-146` re-derives the requirement list from the
digest-checked baseline and refuses (exit 2) if it differs from the frozen
`requirements` list, so the replay cannot silently use a weakened requirement.

## 2. Receipt vs observation runner_result

`bundle.json` receipts were compared field-by-field to the observations:

| row | exit | stdout | stderr | argv | revision | cwd |
|---|---|---|---|---|---|---|
| witness-metadata-check | 0=0 | equal | equal | equal | equal | equal |
| context-capture-selftest | 0=0 | equal | equal | equal | equal | equal |
| verify-round15 | 0=0 | equal | equal | equal | equal | equal |
| round19-correction-ruler-selftest | 0=0 | equal | equal | equal | equal | equal |
| round21-coldread-selector-selftest | 0=0 | equal | equal | equal | equal | equal |

Stronger: rebuilding the bundle exactly as `project()`
(`tools/registry-replay.py:102-113`, `json.dumps(sort_keys=True, indent=2)+"\n"`)
from `observations.json` reproduces `bundle.json` **byte-for-byte**:
sha256 `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`,
which equals `expected.json.bundle_sha256`. The gate
`tools/command-binding.py --bundle … --expected …` exited 0 with
`finding_ids: []`, and its own tool digest matches the worktree and rev
(`9230c68e…`).

`held` is **not** carried in bundle receipts (receipt keys are exactly
`name,argv,cwd,revision,exit,stdout,stderr`). It is a publication precondition
(`registry-replay.py:87-90` refuses `RUNNER_NOT_HELD`/`RUNNER_CLEANUP_FAILED`)
and is recomputable from the bundle: exit vs `requirements[].expect.exit` plus
tokens in `receipts[].stdout`. Recomputing that for all 43 bundle rows yields
zero non-held rows. `command-binding.py:110-112` independently flags
`EXIT_MISMATCH`/`STDOUT_MISMATCH`.

## 3. Held semantics and token presence

`registry-check.py:648-731` executes `row["argv"]` directly (shell=False) in the
clone cwd and sets
`held = got == expect.exit and not missing and cleanup_ok` (line 720), where
`missing` is a literal, case-sensitive substring test over the **full** decoded
stdout (line 718); streams are retained whole (`communicate()`, no tail when
`retain_streams=True`). Observed: `held=true`, `got=0`, `expect=0`, stderr empty,
stdout 221 B / 5201 B / 5193 B / 1967 B / 543 B (max 8110 B across all 43 rows,
far below the 1 MiB `STREAM_LIMIT`), no `stdout_missing`, no `cleanup_error`.

Token presence and whether the token can also print on failure:

- `witness-metadata-check` — `metadata_consistent` present. Success id
  `EXPECTED_VERDICT_ID="metadata_consistent"`; the negative path prints
  `metadata_inconsistent` (`tools/witness-metadata.py:261`), which does not
  contain the token as a substring. `--check` also requires
  `companion == build_companion()` (line 615) and re-hashes the three pinned
  round-12 inputs (lines 72-89, 394-400); independent recomputation of those
  three files matches the pins (`acc01268…`, `e8d2024a…`, `0def0d3b…`). Exit 0
  only on the consistent path (line 1212). Substantive, not vacuous.
- `context-capture-selftest` — `SELFTEST: PASS` present. The harness prints PASS
  only when `self.failed` is empty (`tools/context-capture.py:1779-1786`);
  FAIL returns 1. Observed 49 `SELFTEST_CASE` lines, all positive, summary
  `SELFTEST: PASS (49/49)`, exit 0.
- `verify-round15` — `measure-historical-preserved: PASS` present.
  `record_check` prints PASS only when `passed` is true
  (`.ufo/evidence/round-15/verify.py:170-176`); the check is recorded only when
  the after-document is a dict with `historical_evidence`, and passes only when
  `all_baseline_bytes_preserved == 1` (detail: `changed=[]`). All 44 check lines
  are `PASS`, exit 0.
- `round19-correction-ruler-selftest` — token `SELFTEST: ` present as
  `SELFTEST: 43/43`. All 43 `CASE … PASS` lines positive; the ruler returns 1
  on any failed case (`.ufo/evidence/round-19/measure.py:391-392`).
- `round21-coldread-selector-selftest` — `SELECTOR_SELFTEST: 12/12 pass`
  present exactly; 12 `CASE … PASS` lines; returns 0 only when all pass
  (`.ufo/evidence/round-21/coldread/measure.py:98-99`).

## 4. Freshness / non-fabrication

- Rows are strictly sequential: zero interval-order violations; inter-row gaps
  22 µs–544 µs; `|interval − elapsed_s|` max 0.57 ms; overall span 260.58 s
  (`15:56:41.156Z`–`16:01:01.739Z` with 43 real subprocess rows).
- `runner_sha256_clone_copy` `cba16646…` equals
  `git show d2eaecd:tools/registry-check.py | sha256sum`; the replay instrument
  `9fcd2dbb…` equals the worktree `tools/registry-replay.py`.
- `observations.json`, `bundle.json`, `requirements.json`, and
  `registry-baseline.json` in the worktree are byte-identical to HEAD
  `c8c5b88`; worktree is clean apart from untracked `.ufo/waves/round-24/`.

## 5. Bounds and residual weaknesses (calibration)

1. **Replay revision is `d2eaecd`, not the wave's delivered `c8c5b88`.**
   `d2eaecd` is an ancestor (2 commits back). `git diff --stat d2eaecd..c8c5b88`
   changes 26 files / 6019 insertions, all under `.ufo/evidence/round-24/`
   (replay outputs and source traces) — no audited row target, tool, companion,
   requirements, or registry file changed. The five outcomes therefore transfer
   to `c8c5b88`, but the replay itself certifies `d2eaecd`'s tree, not
   `c8c5b88`'s.
2. **round19's required token is a bare prefix.** `"SELFTEST: "` alone would
   also match `SELFTEST: 0/43`; acceptance rests on the exit binding, which the
   current ruler honours (returns 1 on any failed case). Not exploitable here
   (observed 43/43, all case lines PASS), but the requirement is not
   self-discriminating.
3. **verify-round15 is live-dependent by construction.** Its internal census
   hardcodes `CENSUS_TOOL=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
   and `--root /home/vgpnk/Projects/shokunin`
   (`.ufo/evidence/round-15/verify.py:105,835-836`). The row is declared
   `external: true` in the baseline and is listed in `live-dependent.json`
   (`revision_pinned 41/43`), so the projection does not falsely claim it
   revision-pinned. Its held verdict still depends on live fleet state.
4. **`project()` trusts the runner's `held` boolean** rather than recomputing it
   from `expect` + retained streams (`registry-replay.py:89`). [INFERENCE from
   code, not executed: a hand-written observations file with `held=true` but a
   mismatched `got`/stdout would publish a bundle.] In this artifact it is not a
   false acceptance: the published bundle is byte-identical to the projection of
   the audited observations, and the downstream gate recomputes exit and tokens
   (`command-binding.py:110-112`). Producer authentication is not claimed by the
   contract and is not claimed here.

## 6. Smallest safe correction

None for the five rows or their receipts. The only latent issue is the round19
token width; correcting it means editing the digest-pinned
`.ufo/evidence/round-23/requirements.json`, which would invalidate the replay's
`registry_sha256`/`requirements` guard. Leave it for the next requirements
revision, where `SELFTEST: 43/43` (or the expected fraction) would make the row
self-discriminating.

## Tooling

No installs or upgrades were performed.
