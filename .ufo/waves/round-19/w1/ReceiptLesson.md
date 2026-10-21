# ReceiptLesson — raw failed invocation vs effective successful receipt (round 19, C1)

Scope: C1 calibration only (routed round-18 defects R18-4 and R18-5, with the
receipt-provenance part of the distinction). Read-only. No production file,
Git ref, index, sibling tree or tool was changed. No tool installed or updated.
No builds, tests, lints, formatters, lane selftests or gates were executed; the
round-19 receipts were read, digest-checked and counted, not re-run.

Baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`. Round-18 lane tip
`4b7c6823a462f5ea2eafcb262275300a545f3ed7`. Round-18 covered revision
`a85f7107c4167cd9968248722256fcaf617fc30c`. Round-18 mid revision
`a134a09d15c23b2c2f0373482bb36c292c175ea5`.

## 1. Sources opened

| Source | How opened | Outcome |
|---|---|---|
| `corpus/lessons/round-18-verifier-spotcheck.md` §5 (items 4–5) | read | Items 4 (`final/checks.json` bash-witness row, exit 64, empty stdout) and 5 (no receipt at `4b7c682`; receipt at `a85f710`). |
| `corpus/lessons/round-19.md` (Gate; Mistakes rows 3–5) | read | Gate admits R18-4 and R18-5; rejects overwriting `checks.json`; rejects a current full-page/coverage claim. |
| `corpus/QUALITY.md` criteria 37–39 (lines 332–363) | read | Criterion 39: final-success claim names one effective receipt with matching argv, measured revision, integer exit, retained stdout/stderr, both digests; failed attempt stays failed; successor names what it supersedes; later replay dated later. |
| `corpus/lessons/round-18.md` §"Erratum R18-3", §"Errata R18-4 / R18-5" (lines 121–150) | read | Errata state the failed row is "a failed raw invocation … not the effective successful selftest receipt" and point to `bash-witness-selftest-complete.json`. |
| `corpus/SOURCES.md` S049 row | grep | Row says the subprocess env mapping is an explicit child environment "not proof of a particular historical environment". Used-by includes `round-19.md`. |
| S049 primary source, `https://docs.python.org/3/library/subprocess.html` (Python 3.15.0 docs, opened 2026-10-21) | read (reopened) | See §4 quotes. |
| `.ufo/evidence/round-18/final/checks.json`, `bash-witness-selftest.{stdout,stderr}`, `bash-witness.stdout`, `measure-final-60.json`, `measure-final.json`, `registry.stdout`, `registry-branch-aligned.stdout` | read / digest / JSON parse | See §2–§3. |
| `.ufo/evidence/round-19/bash-witness-selftest.{json,stdout,stderr}`, `bash-witness-selftest-complete.{json,stdout,stderr}`, `round18-final-measure.{json,stdout,stderr}`, `sources-diff.txt`, `before.json`, `contract.json` | read / digest / JSON parse | See §2–§3. |
| `.ufo/evidence/round-19/measure.py` lines 54–140 (R18-4, R18-5 predicates) | read | See §5. |
| `.ufo/reports/round-18/tameshi.md` (fleet root) lines 3, 41–53 | grep | Report cites `4b7c682` as the final tip and "strict 60/60" at `a85f710`. |

## 2. Commands and observed outcomes

All digests below were computed with `sha256sum` on the retained files, and
compared with the digests recorded in the JSON receipts.

```
sha256sum .ufo/evidence/round-19/bash-witness-selftest.stdout      -> 3c345db7…6366  (recorded stdout_sha256 3c345db7… MATCH)
sha256sum .ufo/evidence/round-19/bash-witness-selftest.stderr      -> b50382f4…4b4   (recorded stderr_sha256 b50382f4… MATCH)
sha256sum .ufo/evidence/round-19/bash-witness-selftest-complete.stdout -> 316b9713…20be (recorded 316b9713… MATCH)
sha256sum .ufo/evidence/round-19/bash-witness-selftest-complete.stderr -> e3b0c442…b855 (empty; recorded e3b0c442… MATCH)
sha256sum .ufo/evidence/round-19/round18-final-measure.stdout      -> 55c530bb…4e0ae8 (recorded 55c530bb… MATCH)
sha256sum .ufo/evidence/round-19/round18-final-measure.stderr      -> e3b0c442…b855 (empty; recorded MATCH)
sha256sum .ufo/evidence/round-18/final/bash-witness.stdout         -> 316b9713…20be  (identical bytes to round-19 complete stdout; no checks.json row binds it)
sha256sum .ufo/evidence/round-18/final/bash-witness-selftest.stdout -> e3b0c442…b855 (0 bytes; = checks.json row stdout_sha256)
git --git-dir=.git show 4b7c682:tools/bash-witness-study.py | sha256sum -> 8dfaa25a…3a12 (= tool_sha256 in both round-19 witness receipts)
git --git-dir=.git show 4b7c682:tools/mutate-and-run.sh | sha256sum  -> d22c4025…94a8 (= runner_sha256 in complete receipt)
git --git-dir=.git cat-file -t {4b7c682, a85f710, a134a09, 183f87b, 7243e7f} -> commit (all five exist)
```

Counts (`python3 -c` JSON parse of the retained receipts; read-only):

```
checks.json rows: 8; exit != 0 rows: 2
  registry              exit 1   rev 921ef80  (argv: registry-check.py --rev 921ef80 --json)
  bash-witness-selftest exit 64  rev 921ef80  (argv: bash-witness-study.py --selftest)
  other six rows        exit 0
```

Witness receipts:

| Receipt | argv | revision | exit | stdout | stderr | observed text |
|---|---|---|---|---|---|---|
| R18 `checks.json#bash-witness-selftest` (round-18) | `tools/bash-witness-study.py --selftest` (rev 921ef80) | 921ef80 | 64 | 0 bytes | `final/bash-witness-selftest.stderr`, 217 B: argparse "the following arguments are required: mode" | failed usage invocation |
| R19 `bash-witness-selftest.json` | `tools/bash-witness-study.py selftest` (isolated scratch clone) | 4b7c682 | 1 | `.stdout` (2059 B; partial check lines, no VERDICT) | `.stderr`, 799 B: `FileNotFoundError … tools/mutate-and-run.sh` | failed setup: runner absent from scratch |
| R19 `bash-witness-selftest-complete.json` | `tools/bash-witness-study.py selftest` (isolated scratch clone) | 4b7c682 | 0 | 2502 B; last lines `WITNESS_SELFTEST: 43/43 pass`, `VERDICT: PASS` | 0 B | successor; `supersedes` lists both the round-18 row and the R19 failed receipt; `historical_receipt_preserved: true` |

Final-revision measure receipts:

| Receipt | revision | argv / exit / stream digests | `sections_covered` / `total` | `calibration_restraint_score` | `depth_score` | `overrides_used` | credited sections | sections with `input-drift:` reason |
|---|---|---|---|---|---|---|---|---|
| R18 `final/measure-final-60.json` | `a85f710` (`rev_input` = same) | **absent** (keys: no argv, exit, stdout/stderr or digests) | 60 / 60 | 8 | 8 | false | 60 | 28 |
| R18 `final/measure-final.json` | `a134a09` | (not re-read for keys) | 59 / 60, `box3_full_page` false | — | — | — | — | — |
| R19 `round18-final-measure.json` | `4b7c682` | argv `…measure.py --repo … --rev 4b7c682 --explain`, exit 0, stdout/stderr digests MATCH, env `GIT_*` removed + `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `PYTHONDONTWRITEBYTECODE=1` | 60 / 60 | 8 | 8 | false | 60 | 28 |

Derived counts: the round-19 replay at `4b7c682` and the round-18 receipt at
`a85f710` agree on 60/60, restraint 8, depth 8, no overrides, 60 credited, 28
drift-annotated sections. This is an agreement of two different revisions, not
a current-tip equivalence claim (round-19 `Mistakes` and `Measurements` say the
same).

`sources-diff.txt` (R19): `git diff --numstat 183f87b 4b7c682 -- corpus/SOURCES.md` → `25 5 corpus/SOURCES.md` (verified by the R18-3 erratum; not re-derived here).

Registry row, unrouted (see §6): `final/registry.stdout` at `921ef80`:
`exit 1`, `held 30`, 35 `held` booleans (31 true, 4 false). The branch-aligned
run at `5923d89` reads `exit 0`, `held 31`. No erratum or successor names the
round-18 registry row.

## 3. Distinction, as the receipts show it

- **Raw failed invocation.** One observed call: argv, revision, integer exit
  (here 64 or 1), and the captured stdout/stderr. Observed failure text is
  preserved verbatim (`usage: … the following arguments are required: mode`;
  `FileNotFoundError … tools/mutate-and-run.sh`). Its bytes and exit do not
  change when a later run succeeds (`historical_receipt_preserved: true`).
- **Effective successful receipt.** A separate record whose argv equals the
  claimed command, whose revision equals the measured revision, whose exit is
  integer 0, whose stdout and stderr match retained files by digest, and which
  names the earlier records it supersedes. In this round the effective witness
  receipt is `bash-witness-selftest-complete.json`; the effective measure receipt
  for the round-18 final-revision claim is `round18-final-measure.json` at
  `4b7c682`.
- **Exact measured revision.** A count or verdict belongs to the revision whose
  receipt measured it. `measure-final-60.json` measures `a85f710`; the report's
  sentence about `4b7c682` had no receipt until the R19 replay, which is dated
  2026-10-21T05:28:25Z (later than the round-18 report of 2026-10-20). A
  later replay is therefore a later receipt, not a retroactive one.

Observed in this round: the successful witness run used a different argv
(`selftest`, positional mode) from the failed round-18 row (`--selftest`). This
is the expected form for a successor that repairs a usage error; criterion 39
requires the successor's argv to match the claimed command, not the failed one.
The round-19 failed setup receipt (missing runner) shows a second failed class
that the same rule covers.

## 4. Sourced proposed prose (for corpus/lessons or QUALITY; not written)

Sources: S049 — Python 3.15.0 subprocess documentation, `run()` `env` paragraph
and `CompletedProcess` attributes, reopened 2026-10-21
(https://docs.python.org/3/library/subprocess.html).

Quotes (verbatim from the reopened page):
- `run()` env: "these are used instead of the default behavior of inheriting the current process' environment." (14 words; `env` paragraph under `subprocess.run`.)
- `CompletedProcess.returncode`: "Exit status of the child process. Typically, an exit status of 0 indicates that it ran successfully." (18 words; `CompletedProcess` section.)

Proposed prose:

> A **raw invocation record** is the observed outcome of one subprocess call:
> its argv, the revision it ran against, its integer exit status and its
> captured streams. Python defines a child's `env` as the explicit mapping
> passed to the call, used "instead of the default behavior of inheriting the
> current process' environment", and defines `returncode` as the "exit status
> of the child process" [S049]. A failed invocation (here exit 64 for a usage
> error, exit 1 for a missing runner) is such an observation and is kept
> byte-for-byte. An **effective successful receipt** is a different record: it
> names one invocation whose argv is the claimed command, whose revision is the
> measured revision, whose exit is integer 0, whose retained stdout and stderr
> match their digests, and which names the earlier records it supersedes. A
> later replay is dated as later. S049 establishes what a recorded call was
> configured to run and what status it reported; it does not establish that a
> historical run happened, that a stored file was produced by the named
> producer, or that a count is current at another revision.

## 5. Ruler coverage (R18-4 / R18-5 predicates, observed in measure.py)

`measure.py` lines 61–76 (`receipt()`) require the receipt's argv, revision,
integer exit (`type(...) is int`, exit 0), stream names and both digests, and
an empty stderr. Lines 112–120 (`witness()`) add the retained `VERDICT: PASS`
and `WITNESS_SELFTEST: 43/43 pass` text, the errata phrase "failed raw
invocation", `historical_receipt_preserved: true`, and the `supersedes` entry
for the round-18 row. Lines 121–136 (`measurement()`) require the exact argv and
`4b7c682`, 60/60, `overrides_used` false, restraint 8 and the errata sentence
"does not claim the receipt existed in round 18". These are presence and
equality tests over the retained files; they do not re-run argv (the header says
so) and they do not check that the successful witness output is the output of
the named tool at the named revision beyond its digest, which is the producer
gap QUALITY 39 already names.

The round-18 `measure-final-60.json` fails the measurement predicate by design:
it has no argv, exit or stream digests, so it cannot be the effective receipt.

## 6. Findings and limits

1. **Confirmed for R18-4 and R18-5 (observation):** the effective-receipt
   distinction is present in the committed round-19 bundle: failed exit 64 and
   failed exit 1 are retained; successor exit 0 is digest-bound at `4b7c682`;
   the R18-5 measure receipt is at `4b7c682` with argv, exit 0 and digests.
2. **Unrouted, not claimed as a C1 defect:** `round-18/final/checks.json` row
   `registry` is a non-zero exit (1) at `921ef80`. Its stdout shows `held 30`
   with four `held: false` rows. No erratum, supersession or round-19 receipt
   names it, and the R18-4 wording covers only the bash-witness row. The
   round-18 report cites a different revision (`5923d89`, exit 0, held 31) as
   the registry no-harm read. Whether the `921ef80` row is a legitimate negative
   verdict or a stale row is not established here; the ruler does not test it.
   Criterion 39's wording ("a final-success claim names one effective receipt")
   may or may not reach it depending on whether the bundle is read as a success
   claim. Route to the lane owner; do not treat as closed.
3. **Round-18 `bash-witness.stdout` (2502 B, sha 316b9713…):** byte-identical to
   the round-19 successful stdout, but it has no `checks.json` row, no argv, no
   revision and no exit record in the round-18 bundle. [INFERENCE] it is the
   earlier successful output of the same command; the record does not prove it.
   It is not used as evidence of an effective receipt here.
4. **Digests of the round-19 failed witness receipt** match the retained files;
   its `tool_sha256` matches the successor's, so the failure is a setup failure
   (missing runner), not a different tool revision.
5. **No independent verifier claim.** This is a lane-internal read of retained
   bytes plus a primary-source reopen of S049. It does not authenticate any
   historical producer, and it does not certify required-command coverage
   (criterion 33) or any current full-page cold-read. C1 numeric calibration is
   unchanged at 8; depth 8 is the same value at `4b7c682` and `a85f710`.
6. **Survivors:** the 18 earlier guard survivors and the EG-3 bounds are not
   touched by this distinction and remain open.

## 7. Commands the main agent may re-run (read-only)

- `sha256sum` on the files named in §2.
- `git --git-dir=.git show <rev>:<path> | sha256sum` for `tools/bash-witness-study.py`
  and `tools/mutate-and-run.sh` at `4b7c682`.
- `git --git-dir=.git cat-file -t <rev>` for the five revisions in §2.
- Read-only JSON parses of `checks.json`, the round-19 `*.json` receipts and
  `measure-final-60.json`.

No install, update, pacman, or host operation occurred in this lane.
