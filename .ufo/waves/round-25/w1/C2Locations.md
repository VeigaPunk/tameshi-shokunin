# C2Locations: round 25, wave 1 (independent location recomputation)

**Verdict: PASS (scoped).** All 20 mutants of the two named legs (`js-kimi-census`, `bash-surface-census`) have emitted start and end line and column equal to an independent recomputation from the pinned target bytes and the spec `@old` strings (1-based, end exclusive). Mismatches: **0**. The same harness flags 3 of 3 seeded faults, so the zero is not vacuous. Counter observed: `MTE_INTEROP: PASS legs_conforming=8/8`, exit 0.

## Scope and inputs

- Clone: `/tmp/c2locations-r25`; `git rev-parse HEAD` = `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`.
- Pinned targets, read with `git show` from the sibling repos (read-only):
  - js: `kumitate-shokunin` @ `175de6ba2e9e904010411b19cab27e0af9aad3d4`, `scripts/kimi-census.mjs`. sha256 `83016d45…f426` equals PIN_JS. 43,273 bytes, 897 lines, LF only, no BOM, no tab characters, no astral characters.
  - bash: `kagi-shokunin` @ `fecee8743e52eb8fb5fbb40782934cb619a1a96e`, `corpus/surface-census.sh`. sha256 `275d8294…3009` equals PIN_BASH. 44,212 bytes, 887 lines, LF only, no BOM, no astral characters.
- `@old` strings: the embedded heredocs in `tools/mutate-and-run.sh:650-690` (js) and `:691-731` (bash). I extracted them with my own parser and did not reuse `mte-interop.py`'s parser. Neither spec body contains a literal tab character.

## Results: 20 of 20 match

| Leg | ID | Start (line:col) | End (line:col, exclusive) | Status | Recomputed equals emitted |
|---|---|---|---|---|---|
| js-kimi-census | D1 | 105:70 | 105:97 | Killed | yes |
| js-kimi-census | D2 | 378:17 | 378:41 | Survived | yes |
| js-kimi-census | D3 | 332:1 | 332:37 | Killed | yes |
| js-kimi-census | D4 | 351:1 | 354:1 | Killed | yes |
| js-kimi-census | D5 | 255:1 | 255:39 | Killed | yes |
| js-kimi-census | D6 | 124:61 | 124:108 | Killed | yes |
| js-kimi-census | D7 | 306:39 | 306:75 | Killed | yes |
| js-kimi-census | D8 | 396:1 | 397:1 | Killed | yes |
| js-kimi-census | D9 | 292:1 | 292:61 | Killed | yes |
| js-kimi-census | D10 | 145:1 | 145:55 | Survived | yes |
| bash-surface-census | B1 | 241:1 | 241:42 | Killed | yes |
| bash-surface-census | B2 | 435:1 | 435:123 | Killed | yes |
| bash-surface-census | B3 | 229:1 | 229:64 | Killed | yes |
| bash-surface-census | B4 | 200:1 | 205:1 | Killed | yes |
| bash-surface-census | B5 | 214:1 | 218:1 | Survived | yes |
| bash-surface-census | B6 | 371:1 | 371:82 | Killed | yes |
| bash-surface-census | B7 | 405:1 | 406:57 | Killed | yes |
| bash-surface-census | B8 | 85:1 | 85:58 | Killed | yes |
| bash-surface-census | B9 | 191:1 | 191:41 | Killed | yes |
| bash-surface-census | B10 | 862:1 | 862:56 | Survived | yes |

Method, all checks per mutant:
- Offset of `@old` in the pristine text. The unique-match check passed both as non-overlapping and as overlapping counts.
- Line from a bisect over newline offsets. Column = offset minus line start, plus 1. End = start offset plus `len(@old)`, which is the exclusive end.
- Round trip: slicing the pristine text from the recomputed start to the recomputed end returns `@old` exactly, for 20 of 20.
- `description` and `replacement` (equal to `@new`) match the spec. The emitted `status` matches the recorded ledger table (`TABLE_JS`, `TABLE_BASH`), so there are no verdict flips.
- The emitted `source` equals the pristine text for both legs.

Shape notes: 16 mutants start at column 1 because `@old` includes the line's indentation. Five mutants (D4, D8, B4, B5, B7) have a multi-line `@old`. Their end lies after the trailing newline or the last character, as the exclusive end requires. Example: D4 ends at 354:1.

Hand check of one row: D1 `@old` is `kind: 'dir', counted: 18 },`, which is 27 characters. Starting at column 70, the exclusive end is column 97.

## Negative control

Three faults were seeded into copies of the two emitted reports: js D3 start column +1, js D8 end line +1, and bash B1 end column -1. The recomputation flagged exactly D3, D8 and B1 (`NEGATIVE_CONTROL: flagged=3`) and no other mutant.

## Findings

1. **No blocking finding.** No location mismatch in the scoped legs.
2. **Low, evidence gap.** On PASS, `mte-interop.py` removes the regression workdir (`check()`, `shutil.rmtree(workdir)` when no `--workdir` is given). `spec.copy` and the materialized pristine copy are therefore not kept beside the emitted reports. The reports carry `source`, `description`, `replacement`, `status` and `location`, but not the `@old` text. An auditor can re-derive `@old` only from the runner heredocs, as I did. Smallest correction: when `--emit` is set, copy each leg's `spec.copy` into the emit directory before the PASS-path removal.
3. **Unit not exercised here.** Columns are Unicode code points (`position()` in `mte-interop.py`). The schema says only "both line and column start at one" and does not state the unit. For all 20 start and end positions in these two legs, the code-point column equals the UTF-8 byte column and the UTF-16 column. Other legs may differ and were not checked. Smallest correction: state the unit (code points) in the module docstring.
4. **Latent divergence.** `parse_spec` in `mte-interop.py` uses `str.splitlines()`, while `mutate-and-run.sh` splits on `\n` only. The two differ only if a spec contains U+2028, U+2029, VT, FF, FS, GS, RS, NEL or CR. The runner file contains none of these (count 0 for each). Smallest correction: split on `'\n'` to match the runner.

## Scope limits

- Only the two named legs were recomputed independently. The other six legs were checked only through the tool's own arithmetic, its schema validation and the counter.
- Per-mutant statuses were compared with the recorded ledger tables, not with a separate sweep. The sweep itself ran inside the tool's live regression run.

## Commands and observed output

1. `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/c2locations-r25 && git -C /tmp/c2locations-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df`. Output: `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`.
2. `git show <rev>:<path>` for both targets into `/tmp/c2/scratch`. Both sha256 values equal their pins.
3. `GIT_OPTIONAL_LOCKS=0 uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin --emit /tmp/c2/emit`, run from the clone. Exit 0, wall time 140.98 s. Eight `MTE_LEG <leg>: CONFORMS` lines, including `MTE_LEG js-kimi-census: CONFORMS (schema=ok official_score=80 tameshi_score=80.0 official_killed=8 recorded_killed=8 official_valid=10 recorded_defects=10)` and the same shape for `bash-surface-census`. Last line: `MTE_INTEROP: PASS legs_conforming=8/8`. Emitted to `/tmp/c2/emit/<leg>.mte.json` (8 files) and `official-metrics.json`.
4. `python3 /tmp/c2/scratch/recompute.py`. Output: `RECOMPUTE: mutants=20 mismatches=0`, exit 0.
5. Negative control with `EMIT` pointed at `/tmp/c2/neg`. Output: `NEGATIVE_CONTROL: flagged=3`, listing D3, D8 and B1.
6. Schema check of the two emitted reports, using a schema I extracted from the vendored tarball with my own code: 0 errors each. Both vendored tarball sha512 values match the integrity strings in `tools/mte-interop.py`.
7. Read-only probes: `GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin status --porcelain=v1` (exit 0). The runner's repo access is limited to `rev-parse`, `cat-file`, `show` and `ls-tree` (`tools/mutate-and-run.sh:1118-1142`), so nothing is written to the repos.

## Tooling record

- Installed: none. Pre-existing, unchanged: uv 0.13.0, node v24.21.0, Python 3.14.8, git 2.56.0.
- Used through `uv run --with`: jsonschema 4.25.1, an ephemeral environment built by uv from PyPI. This is the counter's own requirement and uses the official uv channel. No persistent install, no pacman, no sudo.

## Checks for the integrator

- Re-run the counter once in the lane: `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin`. Expected last line: `MTE_INTEROP: PASS legs_conforming=8/8`. I ran nothing in the lane.
