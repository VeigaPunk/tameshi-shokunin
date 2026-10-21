# CorpusSkill — round24 W1 critic: SKILL.md round24 addition

Seat: `TameshiR24-2.CorpusSkill` (critic, leaf). Target: `SKILL.md:2043-2059` at
`c8c5b88c8e961a929cdc351b95a7074c76958909`. Mode: read-only inspection. No "Run" was
assigned, so no gate, selftest or battery was executed. Exit claims below come from the
code paths cited plus Python's documented behaviour (an uncaught exception exits with
status 1); they are marked `[STATIC]`. No tools were installed or updated.

## Verdict

**Defects found (4 fixable, 1 tradeoff).** The registry row is complete for name, kind,
self-invocation and owner. Three things are wrong with it:

- The verdict map does not match the exits `--run` and `--plan` actually produce.
- The PROTOCOL field "pinned-value path" is missing, along with the Two-evidences frozen
  run.
- "writes only under `--out`" overstates the write scope.

A separate defect lets an earlier bundle survive a refused run. The accompanying claims
in `SKILL.md:2054-2059` (44/44, the pinned digests, append-only supersession) hold.

## Axes

- A1 verdict calibration (whether an exit code reads as the right class)
- A2 registry-row completeness (PROTOCOL.md:401-403 field list, plus Two evidences
  at PROTOCOL.md:390-397)
- A3 write-scope honesty
- A4 publication integrity (a refused run must not leave a bindable bundle behind)

## Findings

### F1 — Verdict map vs actual exits (A1) — fixable

Row `SKILL.md:2052` says: "2 invalid/unavailable input, could-not-evaluate". PROTOCOL.md:380
fixes 1 = `failed` fleet-wide. Several unavailable-input paths in `--run` raise instead of
returning 2, so they exit 1 and read as `failed`/refused `[STATIC]`:

| Input | Code | Exit |
|---|---|---|
| `--rev` not in the repo, or `--repo` not a git repo | `tools/registry-replay.py:135-136` `subprocess.run(..., check=True)` raises CalledProcessError | 1 |
| `--requirements` or `--registry-baseline` missing or not JSON | `:137-138` `read_bytes()` / `json.loads` raise | 1 |
| requirements file without `registry_sha256`; a baseline row without `status`/`argv`/`expect` | `:139`, `:142-143` raise KeyError | 1 |
| clone or checkout failure | `:153-154` `check=True` | 1 |
| revision whose clone has no `tools/registry-check.py` | `:162-166` raises FileNotFoundError | 1 |
| `--project good.json --out <existing regular file>` | `publish` `:119` `out.mkdir` raises FileExistsError | 1 |

Two more mismatches:

- `--plan --repo /no/such/lane --json` exits 0 and prints
  `{"fleet_root": "/no/such", "repo": "/no/such/lane", "siblings": []}` (`:63-69`). Nothing
  checks that the path exists, so invalid input reads as `clean`. `--plan` cannot fail at
  all; under PROTOCOL.md:376-378 that is a probe mode registered inside a gate row.
- `--help` exits 0. Under the row's map that reads as "bundle published or plan printed".
  The round22 row explicitly declared its help exit (`SKILL.md:2007-2008`); this row does
  not.

The map also never assigns a class to codes 0 and 1. The sibling rows do: `SKILL.md:1997`
says "0 clean; 1 failed invariant" and `SKILL.md:2019` says "0 clean …; 1 mismatch". Here
"0 bundle published or plan printed" folds a probe output into `clean`.

None of the `--run` exit-2 paths is exercised by the selftest. Its ten cases cover
`--project` (9 cases) and `--plan` (1 case) only (`:199-242`), so the "2" for `--run` is
asserted but not tested.

### F2 — Missing pinned-value path / frozen run (A2) — fixable

PROTOCOL.md:401-403 requires a "pinned-value path". PROTOCOL.md:390-397 adds that a gate
whose verdict depends on mutable fleet state must also ship a run over a committed snapshot
with a committed expected verdict. The row's "Persisted values" cell is "literal fixtures in
the tool; frozen requirement/registry digests come from the caller's files". It names no
path.

The only registry row for this tool is `registry-replay-selftest` (`tools/registry.json:990-999`).
PROTOCOL.md:390 calls selftest green "capability, not a measurement".

A committed snapshot does exist:

- `.ufo/evidence/round-24/replay/observations.json`, sha256 `2d9b1b77…a7a88`.
- I re-derived the projection by hand without running the tool. `bundle.json` equals the
  projection of those observations byte for byte (sha256 `4f424023…a9c6`, matching
  `replay/expected.json`).
- `live-dependent.json` lists `pin-disposition-read` and `verify-round15`, with 41 of 43
  rows revision-pinned.

Neither the SKILL row nor any registry row cites or replays that snapshot. Two
consequences:

- A later edit to `project()` could change refusal or live-dependency behaviour and keep
  10/10 green. For example, it could drop the `external` arm at `:99` while a selftest
  fixture still sets `non_hermetic_argv`. Nothing frozen would catch that.
- The 43-row result is evidence prose only, not a pinned verdict.

### F3 — Write-scope honesty (A3) — fixable

The row says: "writes only under `--out`; rows run in a private clone whose fleet mirror
symlinks live siblings". Five problems:

1. **The clone itself is written outside `--out`.** `--run` creates a full
   `git clone --no-hardlinks` under `$TMPDIR` (`:149-154`). It is removed afterwards, but
   it is not under `--out`. The selftest also writes `$TMPDIR` scratch (`:208`, `:227-230`).
   Sibling rows declare this ("isolated selftest scratch only", `SKILL.md:1997`, `:2019`);
   this row does not.
2. **Rows can write into live siblings.** Rows can write through the sibling symlinks. One
   replayed row names the live fleet root directly: `pin-disposition-read` argv contains
   `--root /home/vgpnk/Projects/shokunin` (observations row, `non_hermetic_argv:
   ["/home/vgpnk/Projects/shokunin"]`). The tool's own docstring says "rows are not
   write-isolated from siblings; that is a limit, not a guarantee" (`:19-20`). The knowledge
   doc says "Realpath identity is not write isolation"
   (`corpus/knowledge/replay-projection-hardening.md:35-36`). The SKILL row drops that
   sentence and calls the clone "private". That wording also undercuts the appended
   round23 correction "The replay above is not an isolated clone" (`SKILL.md:2033`).
3. **Hooks are not disabled.** The clone omits `-c core.hooksPath=/dev/null`, unlike the
   runner it reuses (`tools/registry-check.py:786`). A `post-checkout` hook from
   `init.templateDir` would run on `:154` and can write anywhere. This is a parity
   regression against the existing runner.
4. **Retained streams are not bounded.** `observations.json` is written under `--out`
   before projection (`:181-183`) and holds complete, unbounded, unredacted streams, even
   when STREAM_LIMIT refuses. The docstring "each retained stdout/stderr is bounded by
   --max-stream-bytes" (`:9`) is false for retention. So is the knowledge-doc row
   "unbounded retained streams → refuses" (`replay-projection-hardening.md:17`). Only the
   bundle is withheld.
   - The cited routed defect (`fresh-adjudication.json@6a1821a:93`, "retained without size
     bounds or redaction") is the source of `registry-replay-selftest`, but it is only
     partly closed. SKILL's own sentence ("refuses to publish … over-limit runner row") is
     accurate.
5. **Fleet-root files are not mirrored.** The fleet mirror symlinks only `*-shokunin`
   siblings (`:66`). Fleet-root files such as `PROTOCOL.md` are absent from the mirror.
   This is not a write issue. It is an identity limit worth one clause, because rows that
   read `../X` diverge from the live layout.

### F4 — A refused run leaves an earlier bundle bindable (A4) — fixable

`publish()` returns without touching `--out` when the bundle is None (`:116-118`), and
`--run` overwrites only `observations.json` (`:183`). Counterexample `[STATIC]`:

1. Run `--run … --out D` cleanly. `D/bundle.json`, `D/expected.json` and
   `D/live-dependent.json` are published.
2. Rerun into the same `D` with one row not held. The run exits 1 with RUNNER_NOT_HELD and
   writes a new `observations.json`.
3. The stale `bundle.json` and `expected.json` from step 1 remain.
   `command-binding.py --bundle D/bundle.json --expected D/expected.json` still exits 0.

The same applies to `--project` with a reused `--out`. The claim "refuses to publish a
binding bundle" holds per invocation, but the directory can still be bound.

### T1 — Tradeoff, not a defect: self-generated expected.json

`publish()` derives `expected.json` from the bundle it just wrote (`:121-124`). The
`replay-gate.json` exit 0 therefore cannot fail on the digest by construction; only the
receipt-vs-requirement binding can fail. This is within contract bounds
(`contract.json:62`). The row's "Persisted values" cell should not imply independence, and
it currently doesn't claim it. No change is required beyond F2.

## Checked and holding

- **Selftest tally.** `REGISTRY_SELFTEST: 10/10` = 9 `--project` cases + 1 `plan-realpath`
  (`tools/registry-replay.py:199-243`). This matches `tools/registry.json:994`.
- **44/44.** 38 (round23) + 6 cases in `.ufo/evidence/round-24/extra-cases.json`
  (round23 file: 19). The loader is `tools/command-binding.py` (diff `6a1821a..c8c5b88`).
- **Pinned digests match the files.** `sha256(.ufo/evidence/round-23/replay/bundle.json)
  = 3d6c99b7…0b9` and `sha256(source-read-bundle.json) = db620668…cf` match
  `tools/registry.json:974,984`. The needle format `"bundle_sha256": "<hex>"` matches
  command-binding's sorted-key report (`replay-gate.json` stdout).
- **Supersession.** The three round23 rows changed only `status` and `superseded_by`; their
  argv, expect and source are unchanged. Each target is an active row, which satisfies
  `registry-check.py:277-297`. The runner still executes superseded rows.
- **Refusal ids.** RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT and
  INVALID_OBSERVATIONS match `:76-110` and the selftest.
- **Runner digest.** `runner_sha256_clone_copy = cba16646…44ad` equals
  `git show d2eaecd:tools/registry-check.py | sha256sum`.
- **Replay revision.** The replay ran at `d2eaecd`, not `c8c5b88`. The blobs of
  `registry-replay.py` (`9fcd2dbb…`) and `command-binding.py` (`9230c68e…`) are identical at
  both revisions, and `d2eaecd..c8c5b88` adds evidence only, so this is benign.
- **`fleet_root` argument.** `fleet_root` passed to `run_row` is the live root, but it is
  used only for the `non_hermetic_argv` check (`registry-check.py:632-646, 662`). This
  matches registry-check's own `--rev` mode, so it is not a defect.
- **Low-severity convention drift.** The new `tools/registry.json` rows cite
  `.ufo/waves/round-23/fresh-adjudication.json@6a1821a:…` as `source`. Earlier rows cite
  their `SKILL.md@rev:line` registry-home row (for example `tools/registry.json:913, 936`).
  The schema accepts both forms.

## Smallest safe correction

1. **F1.**
   - In `run_replay`, catch `(OSError, ValueError, KeyError, TypeError,
     subprocess.CalledProcessError)` around input loading, clone/checkout and runner
     import, and return 2. Catch OSError in `publish` and return 2.
   - Make `--plan` return 2 when `os.path.isdir(repo)` is false.
   - Add selftest cases for a `--run` digest mismatch → 2 and a missing requirements file → 2.
   - Rewrite the map as: "0 clean (bundle published; `--plan` printed, probe output); 1
     failed (refused: …); 2 could-not-evaluate; 64 could-not-evaluate; `--help` 0 is help".
2. **F2.**
   - Add an active registry row that runs `python3 tools/registry-replay.py --project
     .ufo/evidence/round-24/replay/observations.json --out <scratch> --json`. It should
     expect exit 0 with needles `"bundle_sha256": "4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6"`,
     `"live_dependent": ["pin-disposition-read", "verify-round15"]` and
     `"revision_pinned": 41`.
   - `--out` must point at a scratch path. A relative path would write into the lane in
     live mode.
   - Name that snapshot and its digest in the "Persisted values" cell.
3. **F3.**
   - Change the write scope to: "own writes: `--out` (observations.json retains complete
     unbounded streams) plus a `$TMPDIR` clone and selftest scratch; row commands are not
     write-isolated from live siblings or absolute live-fleet argv".
   - Add `-c core.hooksPath=/dev/null` to the clone at `:153`.
   - Correct the docstring at `:9` and the knowledge-doc row `:17` from "bounded" to
     "publication refused when over the bound".
4. **F4.** Refuse a non-empty `--out`, or remove `bundle.json`, `expected.json` and
   `live-dependent.json` from `--out` before projecting. Add a selftest case: a clean run
   followed by a refused run into the same directory must leave no `bundle.json`.

No producer authentication, promotion, historical R17-CMD-BIND closure or score uplift is
claimed or implied by this review.
