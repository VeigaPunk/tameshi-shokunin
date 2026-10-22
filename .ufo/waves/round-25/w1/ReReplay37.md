# ReReplay37 — re-attack of round-23 Replay37 (row `env-diff-selftest`)

Verdict: AGREE. The static exact binding of row `env-diff-selftest` holds in the frozen round-23 artifacts and is unchanged at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df. I found no field-level false acceptance under honest execution. I recorded two adversarial deltas below. Neither breaks the binding claim. One is a weakness in the oracle that a mutation can exploit, and it lies outside the binding. The other relies on a forged receipt, which belongs to the producer-authentication question this item excludes. The `runner_sha256` field has a latent provenance defect, but its value is correct for this run.

## What was checked

All checks were read-only. The only commands I executed were `command-binding.py` runs in a private `/tmp` scratch directory, which I deleted afterwards. I did not run the registry command (`python3 tools/env-diff.py --selftest`) or any suite. I installed no tools.

### Frozen argv and expect versus the baseline source

| Artifact | argv | expect |
|---|---|---|
| `.ufo/evidence/round-23/requirements.json` `requirements[36]` | `["python3","tools/env-diff.py","--selftest"]` | `{"exit":0,"stdout_contains":["ENVDIFF_SELFTEST: 9/9 pass"]}` |
| `registry-baseline.json` `rows[40]` (sha256 `ebd2e69a…ec92a`, equal to `requirements.json:registry_sha256`) | same | same, plus `timeout_s:120`, `status:active`, `tags:[new-r21]`, `source: SKILL.md@370f2df:1975` |
| `git show <rev>:tools/registry.json` at 28cae17, 496d212, 1f73157 (base) and c9ff09f | same row, byte-identical | same |
| `replay/bundle.json` `requirements[36]` and `observations.json` `rows[36].requirement` | equal to `requirements.json[36]` (Python `==` reports True for both) | equal |

- **Source anchor.** `SKILL.md@370f2df` line 1975 is the `tools/env-diff.py` instrument row. It gives the self-invocation as `python3 tools/env-diff.py --selftest`, which matches the argv exactly. The anchor does not state `9/9` or the selftest exit code; a grep of that `SKILL.md` for `ENVDIFF_SELFTEST` found nothing. The token therefore comes from the tool source, not from the cited SKILL line.
- **Tool source.** `tools/env-diff.py` has sha256 `e8b47ab7…9ead` at 28cae17, 496d212, base, c9ff09f and in the lane working tree.
  - `env-diff.py:143-195` defines exactly nine `check(...)` calls: invariant, tz, locale, home, columns, repeat, missing-bwrap, timeout and pin-mismatch-public-cli.
  - It prints `ENVDIFF_SELFTEST: {passed}/{len(checks)} pass` and returns `0 if passed == len(checks) else 1`.
  - So exit 0 together with the token `ENVDIFF_SELFTEST: 9/9 pass` holds exactly when there are nine checks and all of them pass. A case added or removed changes the denominator. A failing case yields exit 1 and `8/9`, which also does not contain the token.
  - Child output cannot leak the token into stdout: the bwrap probes and the pin-mismatch child both use captured pipes (`env-diff.py:74`, `:185`).
- **Requirement fields dropped by projection.** `timeout_s`, `kind`, `status`, `tags` and `source` are left out of the requirement. That loses nothing for the binding: `replay.py:58-60` executes the full source row, so `run_row` applies `timeout_s`. The recorded elapsed time is 0.228 s against a 120 s budget.

### Receipt and invocation metadata versus the observation (full streams)

- **Receipt fields.** In `bundle.json` `receipts[36]`: exit 0, stderr empty, stdout of 275 bytes (ten lines: nine `ENVDIFF_CASE … PASS` lines and the summary line). The receipt stdout and stderr are byte-equal to `observations.json` `rows[36].runner_result.stdout` and `.stderr`. Receipt cwd and revision equal the bundle's cwd and revision (`/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` and 496d212).
- **Full stream versus tail.** `stdout == stdout_tail` because the 275-byte stream is shorter than `TAIL_BYTES = 4096` (`registry-check.py@496d212:110`). For this row the retained full stream therefore adds no evidence over the tail. It is present, but it cannot demonstrate the full-versus-tail capture property.
- **How argv and cwd were produced.** Neither value was observed independently, for example from `/proc/<pid>/cmdline`. `replay.py:62` copies them from `row['argv']` and `str(clone)`. The runner executes exactly those values: `registry-check.py@496d212:676-683` calls `Popen(row["argv"], cwd=cwd, …)`. Their correspondence to the real exec is therefore established by reading the code, and that holds for this code path. The receipt exit is `runner_result.got`, which is `proc.returncode` (`:711-713`).
- **Revision.** `replay.py:50` checks out the resolved revision with `check=True`.
- **Bundle digest.** `sha256(bundle.json)` is `3d6c99b7…0b9`, which equals `replay/expected.json:bundle_sha256`.
- **Running the binder.** Command: `python3 cb.py --bundle bundle.json --expected expected.json --json`, where `cb.py` is `command-binding.py` extracted with `git show` at 496d212 and at c9ff09f. Both return `{"exit": 0, "finding_ids": [], …}`.
- **Retrofill check.** No historical metadata was retrofilled. `replay.py:62-63` records invocation fields only beside rows executed in that run. `observations.json:measurement_interval` (14:42:22Z–14:44:58Z) starts about one minute after 496d212 was committed (`2026-10-21T11:41:18-03:00`, which is 14:41:18Z). The row interval 14:44:56.22–14:44:56.45 is consistent with `elapsed_s` 0.228.

### Evidence present versus inferred

- **Present (retained bytes I checked):** argv, cwd, revision, exit, full stdout and stderr, the per-row interval, the bundle digest pin, and `registry_sha256`. `registry_sha256` equals the sha256 of the 496d212 registry blob.
- **Inferred, not observed:**
  - That the declared argv and cwd are the ones that ran. This rests on reading `replay.py` and `registry-check.py`; there is no OS-level record of the exec.
  - That the run actually happened, as opposed to receipts being composed. The binder disclaims producer authenticity (`command-binding.py:11-13`), and I make no producer-authentication claim.
  - That the 0.228 s elapsed time is plausible. The round-24 replay of the same row recorded 0.655 s with byte-identical stdout at d2eaecd. That supports the timing but does not prove it.

## Adversarial deltas

1. **A vacuous selftest case leaves the receipt byte-identical (unguarded oracle weakness, not a binding defect).**
   - Delta: in `tools/env-diff.py:164`, change `check("timeout", timed.get("error") == "TIMEOUT" and timed["exit"] is None)` to `check("timeout", True)`.
   - The mutant still prints `ENVDIFF_CASE timeout PASS` and `ENVDIFF_SELFTEST: 9/9 pass` and exits 0. Its receipt would be byte-identical to the retained one, so `command-binding.py` cannot tell the two apart.
   - The same applies to any of the nine predicates. Deleting the `print` at `:147` would also be accepted, because only the summary token is pinned.
   - No round-23, round-24 or round-25 mutation spec targets `env-diff.py`: the grep of `.ufo/evidence/round-25/guard-mutants.spec`, `multitoken-mutants.spec` and `round-23/mutations-A.json` found zero hits.
   - Not run: executing the mutant would mean running the registry command, which this item forbids. The conclusion is derived statically from `env-diff.py:143-195`.
2. **Token containment accepts receipts that contradict themselves (forgery only; out of scope).**
   - In `/tmp` scratch I edited only `receipts[36].stdout`, recomputed the expected digest, and ran both binder versions. All three variants returned exit 0 with `finding_ids: []` under both 496d212 and c9ff09f:

     | Variant | Edited stdout |
     |---|---|
     | `no-case-lines` | only `ENVDIFF_SELFTEST: 9/9 pass` |
     | `fail-line-plus-token` | `ENVDIFF_CASE timeout FAIL` with the `9/9` summary kept |
     | `token-then-regression` | the original stdout followed by `ENVDIFF_SELFTEST: 8/9 pass` |

   - The real `env-diff.py` cannot emit the second or third variant. They are reachable only by a forged or edited receipt written before the caller-owned digest pin, which is the excluded producer-authentication question.
   - Substring containment with surrounding text is also the intended contract, fixed by the `stdout-surround-clean` case in `round-23/extra-cases.json`. This is a tradeoff, not a defect.

## Latent provenance defect (no false value here)

- **Defect.** `replay.py:78` computes `runner_sha256` from `args.repo/tools/registry-check.py`, the live lane working tree. The runner that actually executed is `clone/tools/registry-check.py` at the replay revision (`replay.py:54`).
- **Effect if triggered.** If the lane copy diverges from the revision, the field names the wrong runner.
- **This run.** The recorded `cba16646…44ad` equals `git show 496d212:tools/registry-check.py | sha256sum`, and the file is unchanged through c9ff09f and the lane tree. The value is therefore correct.
- **Round 24.** The round-24 observations carry no `runner_sha256` at all (`None`).
- **Smallest safe correction**, if the replay instrument is ever reused: hash `clone / 'tools/registry-check.py'` at the point where it is loaded.

## Still applies at c9ff09f?

Yes, unchanged:
- The `registry.json` row is byte-identical; the registry sha changes (`a8f255f1…`) only because other rows were added.
- `env-diff.py` and `registry-check.py` are unchanged.
- `command-binding.py` differs from 496d212 only in selftest fixture loading. Round-24 extra cases were added at `:164-169`; `evaluate()` and `check()` are identical, as `git diff 496d212..c9ff09f -- tools/command-binding.py` shows.
- The round-24 replay at d2eaecd re-executed this row: same requirement, byte-identical stdout, exit 0.
- Lane HEAD is 5b69fb2, which descends from c9ff09f; that diff touches only `.ufo/waves/round-25/*`.

## Smallest safe corrections (optional; none needed for the binding)

- Close delta 1 with an `env-diff.py` predicate-vacuity mutant in a guard spec, or by pinning the nine `ENVDIFF_CASE <name> PASS` lines as additional `stdout_contains` tokens in the registry row. The token pin only blocks print-deletion mutants; a vacuity mutant still needs the guard spec. This falls under the R23-ROUTED-1 multi-token fixture's scope and is not a binding change.
- Fix the `runner_sha256` source path as described above.

R23-REATTACK Replay37: AGREE
