# bash-witness-selftest receipt audit (round-18 `final/checks.json` row)

Audit date: 2026-10-21. Seat: `TameshiR19-2.BundleBashWitnessSelftest` (read-only scout).
Scope: only row `bash-witness-selftest` of `.ufo/evidence/round-18/final/checks.json`,
its retained `.stdout`/`.stderr`, the CLI source, and the records that supersede or
corroborate it. Nothing was executed: not the row argv, the selftest, the ruler, or
any lane selftest. No production, Git, or JJ state was written. No tools were installed.
Labels: **[OBS]** observed bytes or command output, **[INF]** inference, **[UNK]** unknown.

## Verdict (advisory)

The row is a **failed raw attempt**. It is a usage error raised before subcommand
dispatch, so the selftest body never ran and produced 0 checks. Erratum R18-4 at `21e7932`
describes it correctly. The row and both of its stream files are byte-identical at
every revision from `5923d89` through `21e7932`. The effective current evidence is
`.ufo/evidence/round-19/bash-witness-selftest-complete.json`, and all 4 of its digests
match. These bytes support R18-4 = corrected at `21e7932`. The residual problems (§5, §6)
are about preserved-history precision and ruler failure capability. None of them reopens
R18-4 under the frozen predicate.

## 1. Digest match: 1/1 recorded digests match, but the match is vacuous

- [OBS] Row (`checks.json:45-54`): argv `python3 tools/bash-witness-study.py --selftest`,
  revision `921ef8077440f90d092aab4b9fdc750a45de1224`, exit `64`, and `stdout_sha256`
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- [OBS] `final/bash-witness-selftest.stdout` is 0 bytes and its `sha256sum` equals the
  row digest, so 1/1 recorded digests match. That digest is the SHA-256 of empty input.
  The row therefore binds only "printed nothing", not a selftest result.
- [OBS] `final/bash-witness-selftest.stderr` is 217 bytes in 3 lines, with SHA-256
  `6a192f7b98c44ed542761b9c38d889ab41202f835385e493c596f546dc287d66`. The row has no
  stderr digest or path field, so 0 stderr digests are recorded and these bytes are
  **unbound**. No `.exit` file is retained, so exit 64 is asserted rather than retained.
  It is still consistent with the stderr text and the source (§2).
- [OBS] Git blob ids are identical at `5923d89`, `4b7c682`, `7243e7f`, `21e7932`, and the
  worktree: `checks.json` `d8c98a92fd`, stdout `e69de29bb2`, stderr `f086b1934b`. Each
  file has a single adding commit, `5923d89`, and no deletion commits exist under
  `final/` or `round-19/`.

## 2. Argv spelling vs CLI source: 0/1, mis-spelled

- [OBS] `tools/bash-witness-study.py` has blob `bac63301`, SHA-256 `8dfaa25a…2e3a12`.
  The parser declares `sub = parser.add_subparsers(dest="mode", required=True)`
  (`:1701`) and registers `selftest` as a subcommand (`:1709-1717`). Dispatch goes
  through `handlers[args.mode]` (`:1730-1733`).
- [OBS] There is no `--selftest` option. Top-level options are `-h`, `--evidence`, and
  `--kagi` (`:1697-1700`). `UsageParser.error` exits `EXIT_USAGE` (`:1684-1689`), and
  `EXIT_USAGE` is 64 (`:119`).
- [OBS] Stdlib ordering, read from host `/usr/lib/python3.14/argparse.py`: the
  required-arguments error (`:2344`) is raised inside parsing, before `parse_args`
  reports unrecognized leftovers (`:2009-2012`). That ordering explains the retained
  stderr exactly: a usage line, then `the following arguments are required: mode`, then
  exit 64 rather than 2. The interpreter used on 2026-10-20 is [UNK]. This ordering is
  long-standing argparse behaviour [INF].
- [OBS] The canonical spelling is `selftest` in both `tools/registry.json:85-91` (row
  `bash-witness-selftest`, which expects exit 0 and `WITNESS_SELFTEST:`) and
  `SKILL.md:1504`.
- [INF] Probable cause: the other six selftest rows in the same `checks.json` use
  `--selftest` and exit 0, because their tools take a flag. This is the only
  subcommand-style CLI in the bundle. Its own `SUITE` constant also contains
  `--selftest`, for the bash target (`:107`).

## 3. Revision attribution: asserted, consistent, not bound

- [OBS] Commit `921ef80` is dated 2026-10-20 18:28:40 -0300. The two stream files have
  mtime 18:33:10, `checks.json` has 18:33:15, and all three were first committed in
  `5923d89` at 18:40:48. `921ef80` does not contain `checks.json` itself, so the row's
  `revision` names a code revision, not the commit that holds the receipt.
- [OBS] The tool blob `bac63301` is identical at `58e5d53`, `921ef80`, `5923d89`,
  `a85f710`, `4b7c682`, `7243e7f`, `78b99dd`, `21e7932`, and the worktree. The runner
  `tools/mutate-and-run.sh` SHA-256 is `d22c4025…2a8b` at `921ef80`, `5923d89`,
  `4b7c682`, `7243e7f`, and `21e7932`.
- [INF] The failure happens in the parser before any file read, so the exit-64 outcome
  is the same for every revision in that window. Attributing it to `921ef80` is
  plausible, but the row records no tool digest, cwd, or environment. That attribution
  cannot be confirmed or refuted from these bytes. [UNK] the tree or scratch that
  actually executed the row.

## 4. Failed raw attempts vs current evidence

| ID | Record | Argv | Revision | Exit | Digests recorded / matching | Class |
|---|---|---|---|---|---|---|
| A | `round-18/final/checks.json#bash-witness-selftest` + `final/bash-witness-selftest.{stdout,stderr}` | `--selftest` ✗ | `921ef80`, asserted | 64 | 1/1, stdout only and vacuous; stderr unbound | **failed raw attempt**: usage error, 0 checks run |
| B | `final/bash-witness.{stdout,stderr}` + `coldread/traces/L1/bash-witness.json` (mapped by name only in `traced-commands.json:10`) | `selftest` ✓, run under bwrap with `env -i` | `921ef80` (trace `:37`) | 0 (trace `:39`) | inputs 2/2 (tool `8dfaa25a…`, runner `d22c4025…`); **no stdout digest** in the trace | round-18 contemporaneous success, uncited by `checks.json`; stdout `316b9713…` is 2502 bytes, `43/43 pass`, `VERDICT: PASS` |
| C | `round-19/bash-witness-selftest.{json,stdout,stderr}` | `selftest` ✓ | `4b7c682` | 1 | 3/3 (stdout `3c345db7…`, stderr `b50382f4…`, tool) | **failed raw attempt**: incomplete scratch; 36 checks printed `ok`, then `FileNotFoundError` for the runner at `sha256_file(RUNNER)` (`:1584`); no tally line |
| D | `round-19/bash-witness-selftest-complete.{json,stdout,stderr}` | `selftest` ✓ | `4b7c682` | 0 | 4/4 (stdout `316b9713…`, empty stderr, tool `8dfaa25a…`, runner `d22c4025…`, which equals `git show 4b7c682:tools/mutate-and-run.sh \| sha256sum`) | **current effective evidence**; supersedes `[A, C]`; JSON SHA-256 `1939f9f4…` equals its input pin in `after-21e7932.json` |

- [OBS] D's stdout is byte-identical to B's stdout (`cmp` returned 0, same blob
  `b7e969e3e2`). Round-18 wave 2 had already recorded the same green digest 35 times
  (`.ufo/waves/round-18/w2/MutateBashWitness18.md:202`). The hermetic selftest output is
  stable across these runs.
- [OBS] C's `cwd_kind` says "isolated scratch clone", but its own stderr shows that
  `tools/mutate-and-run.sh` was missing. That file is tracked at `4b7c682`
  (`git cat-file -t` returns `blob`). [INF] C's scratch was a partial materialization,
  not a full clone of `4b7c682`. `LOG.md:1164-1165` and `corpus/lessons/round-19.md:54`
  already call it "incomplete scratch". [UNK] whether D ran in the same directory with
  only the runner added. D binds both traced inputs (B's trace lists exactly these two
  tracked inputs, with `untracked {}` and `external {}`), so D's content attribution holds.
- [OBS] C's receipt also says `"supersedes": ".ufo/evidence/round-18/final/checks.json#bash-witness-selftest"`
  and `historical_receipt_preserved: true`, even though C failed. Two records therefore
  claim to supersede A. D resolves this by superseding both.
- [OBS] Erratum R18-4 (`corpus/lessons/round-18.md:135-146`) is accurate on A, C, and D.
  It does not mention B. It does not state that tool and runner are byte-identical at
  `921ef80` and `4b7c682`, and that identity is what makes A (`921ef80`) → D (`4b7c682`)
  a valid supersession across revisions.

## 5. Preserved-history failure capability of the R18-4 ruler

This section is derived from source only; the ruler was not executed.

- [OBS] Committed ruler `.ufo/evidence/round-19/measure.py` at `21e7932` has SHA-256
  `c538c33d…`. That is the `ruler_sha256` in both `before.json` (`7243e7f`, 0/5, R18-4
  open) and `after-21e7932.json` (5/5).
  - `witness()` (`:112-120`) reads only D, D's streams, the erratum text, and a string
    inside D's `supersedes`.
  - Data is loaded only for `PATHS` (`:30-34`, `:240-243`). Those exclude A's two
    stream files and all of C.
  - `historical_receipt_preserved` is a self-asserted boolean. The selftest's
    `unpreserved` case (`:184`) only flips that boolean.
- **Concrete failing criterion [INF from source].** Each of the following would leave
  R18-4 `corrected` under `c538c33d`:
  - rewriting A's row to argv `selftest`, exit 0, and stdout digest `316b9713…`
    (laundering);
  - deleting `final/bash-witness-selftest.stderr`;
  - deleting C.

  So `round-19.md:52`'s "history-preservation cases reopen R18-4" covers only the
  boolean. At `21e7932` the history is in fact preserved (§1 blob ids). This gap is
  about failure capability, not a present defect in the bytes.
- [OBS] At about 02:53:48 -0300 the worktree ruler changed to SHA-256 `1d275750…`, which
  is not committed. Its `witness()` now also requires that A's row has `exit == 64` and
  an empty-input `stdout_sha256`, and that D has the pinned tool and runner digests.
  - No selftest case mutates A's row, so the new clause has no failing control.
  - A's stream files and C remain outside `PATHS`.
  - `before.json` and `after-21e7932.json` were measured with `c538c33d`. If L1 adopts
    `1d275750`, both receipts must be re-measured with it.

## 6. Recommended preserved-history treatment

1. **Keep A exactly as it is.** That means `checks.json` blob `d8c98a92fd` (row
   `:45-54`), stdout blob `e69de29bb2`, and stderr blob `f086b1934b`. Do not edit, add
   fields to, relabel, rename, or delete them. This already holds at `21e7932`.
2. **Append a dated, named erratum without rewriting R18-4.** For example, add
   "Erratum R18-4a (2026-10-21)" after `round-18.md:146`. It should state:
   - A's stderr SHA-256 `6a192f7b…6d87d66` (217 bytes) and stdout digest
     `e3b0c442…b855` (0 bytes), so the failure bytes become digest-bound;
   - the failure class: a usage error before dispatch, 0 checks, `--selftest` versus the
     required `mode` subcommand (`:1701`, `:1709-1717`);
   - that tool `8dfaa25a…` and runner `d22c4025…` are identical at `921ef80` and
     `4b7c682`, which justifies superseding across revisions;
   - B as the round-18 correct-argv run, byte-identical to D but not digest-bound in
     round 18, and never to be cited as a round-18 receipt;
   - that C's own `supersedes` and `historical_receipt_preserved` fields are claims made
     by a failed attempt and have no effect. Only D supersedes A.
   - that C's `cwd_kind` is a partial scratch, not a full clone of `4b7c682`.
3. **Ruler change (advisory, owned by L1).** Make R18-4 able to fail on lost history:
   - Require A's exact tuple: argv including `--selftest`, revision `921ef80`, exit 64,
     and empty-input stdout digest.
   - Add A's two stream files and C's three files to `PATHS` with pinned digests, and
     require C's exit to be 1.
   - Add selftest mutants for A's exit set to 0, A's argv set to `selftest`, A's digest
     set to `316b9713…`, A's stderr deleted, and C's receipt deleted. Each must reopen
     R18-4.
   - Then re-measure the baseline (`7243e7f`, expect 0/5) and the delivered revision
     with the new ruler SHA, and commit both receipts.

## 7. Unknowns

- [UNK] The cwd, tree, and interpreter of A's run.
- [UNK] Whether D ran in C's directory plus the runner, or in a fresh scratch.
- [UNK] Who produced `checks.json`. No producer script was found under the scoped paths.
- [UNK] Whether L1 will commit the in-flight ruler `1d275750`.

## Commands / sources

All commands were read-only, with `GIT_OPTIONAL_LOCKS=0` and no `jj` calls.

- `stat` and `sha256sum` on A, B, C, and D's streams and JSON files; `od -c` on A's stderr.
- `cmp` of D's stdout against `final/bash-witness.stdout`.
- `git log` and `git rev-parse <rev>:<path>` across the revisions above.
- `git show <rev>:tools/{bash-witness-study.py,mutate-and-run.sh} | sha256sum`.
- `git cat-file -t 4b7c682:tools/mutate-and-run.sh`.
- `git log --diff-filter=D` for `final/` and `round-19/`.
- `git show 21e7932:.ufo/evidence/round-19/measure.py` copied to `/tmp/bwst-audit-*`
  and diffed against the worktree (scratch removed afterwards).
- Read: `tools/bash-witness-study.py:75,107,119,1584,1684-1733`; `tools/registry.json:85-104`;
  `SKILL.md:1504`; `/usr/lib/python3.14/argparse.py:2007-2012,2344`; the round-18
  spot-check §5; `corpus/lessons/round-18.md:135-155`; `corpus/lessons/round-19.md:20-25,52-54`;
  `LOG.md:1160-1166`; `.ufo/evidence/round-19/{before,after-21e7932,frozen-runs}.json`.

Quotes, opened 2026-10-21:
- "bash-witness-study.py: error: the following arguments are required: mode"
  (`final/bash-witness-selftest.stderr:3`).
- "argparse's default usage exit is 2; the probe contract uses 64." (`tools/bash-witness-study.py:1685`).
- "Do not leave a failed invocation as the selftest row of the final receipt bundle."
  (`corpus/lessons/round-18-verifier-spotcheck.md:199-200`).
- "its failed output/receipt is also retained and explicitly superseded, never counted as green."
  (`corpus/lessons/round-18.md:145-146`).
