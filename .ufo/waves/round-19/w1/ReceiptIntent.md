# ReceiptIntent — round 19, w1 (revenger, advisory)

Seat: `TameshiR19-2.ReceiptIntent`. Surface: what CLI the round-18 `final/checks.json` row `bash-witness-selftest` was meant to run (R18-4). I worked it out from the `tools/bash-witness-study.py` parser and the committed successful receipts. This report is advisory and closes nothing.
Method: read-only. Every git call was a read. Hashes came from `sha256sum`. I parsed committed JSON with stdlib `python3`. I did **not** run any lane tool, selftest or receipt argv. Nothing was installed or updated. No LSP device was used. Locations come from `grep`/`read` plus `git show` of the blobs, so they are source text, not semantic proof.

## 1. Reconstructed contract (answer)

The row was meant to run:

| Field | Recovered value | Basis |
|---|---|---|
| argv | `["python3", "tools/bash-witness-study.py", "selftest"]`. Positional subcommand, no options. | E1, E4, E5, E6 |
| cwd / revision | Root of a full checkout at `921ef8077440f90d092aab4b9fdc750a45de1224`. This is the row's own `revision`, and the tool path is relative. | E3, E4, E5 |
| inputs read | `tools/bash-witness-study.py` sha256 `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12` and `tools/mutate-and-run.sh` sha256 `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` | E4 trace `inputs`; E8 |
| outcome | exit `0`. stdout is 2502 B, sha256 `316b97139aaa2fafa1ab08c2df6471ba8dec5b4480efa1a9589ae0341e5020be`, and ends `WITNESS_SELFTEST: 43/43 pass` / `VERDICT: PASS`. stderr is 0 B (`e3b0c442…b855`). | E4, E5 |

`--selftest` has never been a CLI form of this tool at any revision (E1). The recorded argv `… --selftest` is a usage error. It is not a selftest outcome.

## 2. Evidence chain (observations)

**E1 — Parser, at every tool revision.** At blob `8dfaa25a…` (identical from `58e5d53` through `21e7932`; see E8):
- `tools/bash-witness-study.py:1701`: `sub = parser.add_subparsers(dest="mode", required=True)`
- `:1715`: `("selftest", "hermetic fixtures for the parser and classifier"),`
- `:1730-1731`: the handler map routes `"selftest": cmd_selftest`
- `:1685-1689`: `UsageParser.error` exits `EXIT_USAGE` (64, defined at `:119`)

The same shape exists at `9df9212` (`:1587/:1601/:1617`) and `4acc607` (`:1591/:1605/:1621`). The tool has no `add_argument("--selftest")` anywhere. In every blob the literal `--selftest` occurs exactly twice: at `:15` and `:107` in `8dfaa25a`, and at `:15` and `:106` in `249d9dcd` and `49e9e5e2`. Both occurrences are the *pinned bash target's* suite, `SUITE = 'bash "$MUTANT" --selftest'`, not this tool's CLI. `cmd_selftest` (`:1228-1681`) reads no `args.*` field, so `--evidence` and `--kagi` do not affect it. It does read `RUNNER` (`REPO/tools/mutate-and-run.sh`) at `:1584`, so the runner file must exist in the checkout.

**E2 — Why argparse gives exactly this error.** Read in `/usr/lib/python3.14/argparse.py` (host Python 3.14.8; opened 2026-10-21):
- At `:2476-2478`, an unknown dash token is treated as "meant to be an optional but there is no such option".
- At `:2343-2345`, the missing required positional raises `'the following arguments are required: %s'`.
- That happens before `parse_args` reaches `'unrecognized arguments'` at `:2009-2010`.

So `--selftest` yields `required: mode`, routed to exit 64. Unknown: the Python version used at 18:33 on 2026-10-20 is not recorded. The message matches, but the version match is [INFERENCE].

**E3 — The failed receipt.**
- `.ufo/evidence/round-18/final/checks.json:45-54` records argv `["python3","tools/bash-witness-study.py","--selftest"]`, `revision` 921ef80, `exit` 64, and `stdout_sha256` `e3b0c442…`, which is the digest of empty bytes.
- `final/bash-witness-selftest.stdout` is 0 B.
- `final/bash-witness-selftest.stderr` is 217 B, sha256 `6a192f7b…`. It is the usage line plus `bash-witness-study.py: error: the following arguments are required: mode`.
- The row has no stderr path or digest field.

**E4 — The L1's corrected run, same revision.**
- `.ufo/evidence/round-18/coldread/traces/L1/bash-witness.json:3-39`: argv `bwrap --ro-bind / / … --unshare-net … env -i PATH=… GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 … LC_ALL=C PYTHONDONTWRITEBYTECODE=1 python3 tools/bash-witness-study.py selftest`.
- The cwd is the L1 final clone `/tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin`.
- It records `"rev": "921ef80…"`, `"exit": 0`, and `inputs` = the two blobs in §1. `untracked`, `external` and `live_lane_reads` are all empty.
- Its outputs are `final/bash-witness.stdout` (2502 B, `316b9713…`) and `final/bash-witness.stderr` (0 B). They are linked by `final/traced-commands.json:10` (name → trace path) and by file name only. No digest links the stdout to the trace.

**E5 — The bundle already holds a correctly invoked, held run under the same name and revision.** This is the strongest evidence.
- `checks.json` row `registry` binds `final/registry.stdout` by `stdout_sha256` `fe15a4d0…`, and that matches the file.
- That registry-check report has `rev` 921ef80 and `registry_sha256` `3e6785ee90fcf75f7147ffdb8bee72ef0bce54343803604df857951cc279f1e6`. This equals `git show 921ef80:tools/registry.json | sha256sum`.
- In that registry blob, row `bash-witness-selftest` (`tools/registry.json:84-104`) has argv `["python3","tools/bash-witness-study.py","selftest"]`, expect exit 0, and `stdout_contains` `WITNESS_SELFTEST:`.
- `registry-check.py` runs `subprocess.Popen(row["argv"], cwd=…)` (`tools/registry-check.py:676-677`) inside a `git clone` + `checkout --detach` of the rev (`:781-796`).
- The report row reads `expect 0, got 0, held true`. Its `stdout_tail` is **2502 B and byte-equal to all of `final/bash-witness.stdout`**.
- The same byte equality holds in `final/registry-success.stdout` (rev 5923d89), `final/registry-branch-aligned.stdout` (rev 5923d89) and `registry-full-e08271a.json` (rev e08271a).
- In registry.json@921ef80, 16 rows are kind `selftest`. Fifteen end in `--selftest`; only `bash-witness-selftest` ends in positional `selftest`.

**E6 — Where the registered command comes from.**
- `SKILL.md:1504` gives the self-test as "`python3 tools/bash-witness-study.py selftest`". `git log -S` finds `9df9212` (round 12, 2026-10-20T01:01:32-03:00) as the only commit that added or removed that string, and the line is still present at baseline `7243e7f`.
- The registry row is already present at `2a22ade` (round 17, which introduced `tools/registry.json`; row at `:85`). The current row's `source` is `SKILL.md@98bea7d:1504`.
- The round-12 original receipts are `.ufo/evidence/round-12/BashWitness/selftest.prefix.out` (21/21) and `selftest.out` (40/40), with tool `249d9dcd…` pinned in `selftest.sha256.txt`.
- `.ufo/evidence/round-13/producer-oracle.py:19` calls `[sys.executable, …'bash-witness-study.py', 'selftest']`.

**E7 — The slip was known before round 18 and kept recurring.**
- Round 13, `.ufo/waves/round-13/w1/GateScribe.md:115`: "precedents use `--selftest` flag (`repeat-control.py`) and `selftest` subcommand (`bash-witness-study.py`). Pick one per tool; registry must match."
- In the same round, `MetadataSchema.md:87` and `MetadataSelftest.md:49` already recommended `bash-witness-study.py --selftest`.
- Round 17, `.ufo/waves/round-17/w1/S01RegistryEnumerate.md:40`: "(positional subcommand, **not** `--selftest`)".
- Round 18, `w2/ReviewSkillDiff.md:111`: "My first try used `--selftest`, which is the wrong form, and got 64 (usage)."
- Round 18, `w2/MutateBashWitness18.md:6`: "The actual owning invocation is positional `selftest` … not a literal `--selftest` option."
- Round-18 planner and seat prose also used the flag form: `spec2.json:325` says "run the owning `--selftest`", and `w1/R08Separability.md:18` and `w1/S11GitEnvSweep.md:160` write `bash-witness-study.py --selftest`.

**E8 — Blob identity.**

| rev | `bash-witness-study.py` sha256 | `mutate-and-run.sh` sha256 |
|---|---|---|
| 9df9212 | `249d9dcd…` | `75ed934d…` |
| 4acc607 | `49e9e5e2…` | `75ed934d…` |
| 58e5d53, 921ef80, 4b7c682, 7243e7f, 78b99dd, 21e7932, worktree | `8dfaa25a…` | `d22c4025…` |

`final/checks.json` sha256 is `fed3c8e6…` at 4b7c682, 7243e7f and 21e7932, so the historical bytes were retained.

## 3. Divergences

- **D1 — Wrong argv form (round 18, observed).** The row ran `--selftest`, not the registered positional `selftest`, and exited 64 with empty stdout.
  - Likely cause [INFERENCE]: the bundle used one template for its selftest rows. Five of the six selftest rows in `checks.json` end in `--selftest` and are valid for their own tools. The tool's own text also contains `--selftest`, for the mutant suite (E1). The generator of `checks.json` is not committed, so the cause cannot be proven.
- **D2 — The bundle was never re-emitted after the corrected run (round 18).**
  - Worktree mtimes (weak evidence; their content equals the committed blobs):
    - `final/registry.stdout`: 18:32:16
    - failed `final/bash-witness-selftest.*`: 18:33:10
    - `checks.json`: 18:33:15
    - corrected trace + `bash-witness.stdout` + `traced-commands.json`: 18:40:20
  - All of these first entered history together in `5923d89` (18:40:48), whose message says only "retain final test runs". No disclosure names the failed row.
  - All 17 L1 audit traces (`coldread/traces/L1/audit-*.json`, rev `a9c94c5`) list `final/checks.json` among their inputs. None lists `final/bash-witness.stdout`. In all 17, `checks.json` is only a path in the spec, which the loop OPENs and hashes. The embedded code never names `checks.json` or `bash-witness`. Its 8 asserts cover registry-branch-aligned, probes, regression, historical, case7, case8, disposition, before and repeat. No assertion checks the `bash-witness-selftest` row, so the exit-64 row went through unexamined.
- **D3 — Schema gap (round 18, observed).** `checks.json` rows carry no stderr field. The usage error shows only in a sibling file that nothing in the bundle references.
- **D4 — Round-19 replacement compared with the recovered intent** (`21e7932`; committed bytes equal the worktree for all six round-19 witness files).
  - Argv equals the intent exactly.
  - `tool_sha256` and `runner_sha256` equal the 921ef80 blobs (E8).
  - exit is 0 and stderr is 0 B.
  - stdout `316b9713…` is **`cmp`-identical** to `final/bash-witness.stdout`, which in turn equals the 921ef80 registry tail byte for byte (E5).
  - Differences (none invalidates the content):
    - (a) The recorded `revision` is `4b7c682`, not the row's `921ef80`. This is content-equivalent because the tool and runner blobs are identical and the trace shows no other tracked input.
    - (b) `cwd_kind: "isolated scratch clone"` is generous for the first attempt. `bash-witness-selftest.stderr` shows `FileNotFoundError` for `/tmp/tameshi-r19-witness-r55qrr4e/tools/mutate-and-run.sh` at `cmd_selftest` `:1584`, yet `git ls-tree 4b7c682` contains that path (blob `fd1a63a3…`). The scratch was therefore not a full checkout of 4b7c682 [INFERENCE: a selective file materialization, consistent with LOG.md:1165 "missing runner supplied only in scratch"].
    - (c) Unlike the round-18 trace, the receipt records no env or sandbox envelope.
  - The ruler `.ufo/evidence/round-19/measure.py:67-85,127-139`:
    - Exact-matches argv, `revision == REV18` and integer exit 0.
    - Checks the stdout and stderr digests and requires empty stderr.
    - Requires the two stdout substrings.
    - Compares `tool_sha256` and `runner_sha256` to constants (`:22-23`), not to `git show` blobs. I checked those constants against the blobs today, and they are correct.
    - Requires the old row to stay `exit 64` with empty stdout.
    - A `--selftest` receipt would fail its argv equality.
- **D5 — Optional strengthening, not a defect.** Neither the round-19 receipt nor the lesson erratum cites E5. E5 is the in-bundle held run at the row's own revision 921ef80, and it would bind the intent without any new execution.

## 4. Concrete failing criterion (for a failure-capable audit of R18-4)

An effective `bash-witness-selftest` receipt fails the recovered intent if any of the following holds:
- argv ≠ `["python3","tools/bash-witness-study.py","selftest"]` (any `--selftest` form ⇒ exit 64);
- the tool blob ≠ `8dfaa25a…` or the runner blob ≠ `d22c4025…`;
- exit ≠ int 0, or stderr is not empty;
- stdout lacks `WITNESS_SELFTEST: 43/43 pass` + `VERDICT: PASS`. The strict byte form is stdout sha256 ≠ `316b9713…`.

Separately, a correction fails if `final/checks.json` sha256 changes from `fed3c8e6…`.

As observed at `21e7932`, all of these criteria hold. This is an observation, not a closure.

## 5. Confidence

- **High**: the intended argv and its outcome. The parser (E1) and the argparse source (E2) account for the failure exactly. Every successful execution on record uses positional `selftest` and yields byte-identical stdout: E4, the four registry reports in E5, and the round-19 receipt.
- **Medium**: the cause is a template slip [INFERENCE].
- **Unknown**:
  - the uncommitted script that generated `checks.json`;
  - the Python version at the 18:33 run;
  - whether the L1 noticed the exit-64 row before committing. The corrected run seven minutes later suggests it did [INFERENCE], but nothing records it.

## 6. Commands run (read-only)

- `git -C L show REV:tools/bash-witness-study.py | sha256sum` and the same for `tools/mutate-and-run.sh`, with `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin` and REV ∈ {9df9212, 4acc607, 58e5d53, 921ef80, 4b7c682, 7243e7f, 78b99dd, 21e7932}.
- `git show REV:tools/bash-witness-study.py | grep -nE 'add_subparsers|add_parser\(|"--selftest"|…'` and `grep -c -- '--selftest'` over the three historical blobs.
- `git show 921ef80:tools/registry.json | sha256sum` and a stdlib JSON count of the selftest rows' argv forms.
- `git show {4b7c682,7243e7f,21e7932}:.ufo/evidence/round-18/final/checks.json | sha256sum`.
- `git ls-tree -r --name-only 21e7932 -- .ufo/evidence/round-19`, `git ls-tree 4b7c682 tools/mutate-and-run.sh tools/bash-witness-study.py`.
- `git log -S'tools/bash-witness-study.py selftest' -- SKILL.md`, `git log --diff-filter=A` on the receipts, `git log 921ef80..4b7c682`.
- `sha256sum`, `cmp`, `stat` and `wc -c` over the round-18 and round-19 receipt files.
- Stdlib `python3` reads (no lane code imported):
  - the `bash-witness-selftest` rows of the four registry-check reports, with a tail-vs-stdout byte comparison;
  - the L1 audit traces' inputs and embedded code.

## 7. Sources opened (2026-10-21; quotes ≤25 words)

- `tools/bash-witness-study.py:1701,1715,1685,107,1479,1584` (blob `8dfaa25a…`).
- `/usr/lib/python3.14/argparse.py:2343-2345,2476-2478,2007-2010`.
- `.ufo/evidence/round-18/final/{checks.json,bash-witness-selftest.stderr,bash-witness.stdout,registry.stdout,traced-commands.json}`, `coldread/traces/L1/{bash-witness.json,audit-921.json}`.
- `tools/registry.json:84-104`, `tools/registry-check.py:676-677,781-796`, `SKILL.md:1504`.
- `.ufo/evidence/round-19/{bash-witness-selftest*.json,.stderr,contract.json,measure.py}`.
- `corpus/lessons/round-18-verifier-spotcheck.md:196-200`.
- The wave notes cited in E7.

Report: .ufo/waves/round-19/w1/ReceiptIntent.md
