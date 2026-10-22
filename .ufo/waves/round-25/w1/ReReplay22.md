# ReReplay22: re-attack of round-23 Replay22 (`reattribute-round16-selftest`)

## Verdict

AGREE. The frozen round-23 receipt for `reattribute-round16-selftest` is bound exactly as `tools/command-binding.py` defines binding. Name, argv, cwd, revision, exit and the required stdout token all match. The receipt also agrees with its frozen inputs. I found no field-level false acceptance in the retained evidence.

The adversarial deltas below are real. A tampered or degenerate receipt for this row would still come back CLEAN. They fall outside the binding contract that the tool declares, and they do not contradict the retained receipt, so I record them as residual hazards rather than a counterexample.

The result still holds at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df. The row is not superseded, and `evaluate()` has not changed.

## What was checked (frozen round-23 artifacts)

### Requirement compared with its baseline source

- `requirements.json:333` (source_revision 28cae179, registry_sha256 ebd2e69a…) contains `argv=["python3",".ufo/evidence/round-16/attribution/reattribute.py","--selftest"]` and `expect={"exit":0,"stdout_contains":["SELFTEST: PASS"]}`.
- The same row appears byte-for-byte in `registry-baseline.json:550`, in `git show 28cae179:tools/registry.json` and in `git show 496d212:tools/registry.json`. Both registry blobs hash to ebd2e69a…, which equals the frozen `registry_sha256`.
- The row's declared source is `SKILL.md@98bea7d:1813`. That line reads `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` with exits "0 corrected rule passes the oracle · 1 it fails". The argv matches exactly, and exit 0 matches.
- The SKILL source does not name a stdout token. The `SELFTEST: PASS` needle is a registry-added strengthening, not something drawn from the source.
- Token soundness, checked against `reattribute.py` (blob eaf564e4…, unchanged since round 16): `SELFTEST: PASS` is printed only at `reattribute.py:326`, on the branch that returns 0 (line 329). Every failure branch prints `SELFTEST: FAIL` (lines 273, 306, 330). The needle therefore cannot match a correctly produced failing run.

### Retained invocation metadata and full output

- The bundle row at `replay/bundle.json:312/929` has a requirement identical to `requirements.json`.
- Its receipt records argv identical to the requirement, `cwd=/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin` (the bundle cwd), and `revision=496d212b…` (the bundle revision). It also records `exit=0`, `stderr=""`, and a complete 1039-byte stdout containing the token exactly once.
- `observations.json:1000-1009` has the same argv, cwd and revision. Its `runner_result.got=0`, `expect=0`, `held=true` and `elapsed_s=0.084` agree with the measurement interval (14:44:35.653627 to 14:44:35.737496, which is 0.0839 s).
- `runner_result.stdout` is identical to the receipt stdout. `stdout_tail` is also identical, because 1039 bytes is below the tail limit, so nothing was truncated.
- `expected.json` holds bundle_sha256 3d6c99b7…, and recomputing sha256 over the bundle bytes gives the same value.
- The stdout agrees with its frozen inputs:
  - **Receipt digest.** The first line reports `verification-3.json sha256=3c419055…`, and that equals the blob at 28cae179, at 496d212, at c9ff09f and in the working tree. The file's only commit is 9f2c86f.
  - **Fidelity count.** "old-rule fidelity 14/14" equals the 14 `kind=command` rows in that file, counted by parsing the JSON myself.
  - **Case list.** "new rule 8/8; old rule fails 5/8" matches the eight cases in `reattribute.py:281-309`: seven literal cases plus the first distinguishing JSON row, `gate-frozen-builtin`. Exactly five of those are old-rule failures.
  - **Path.** The path printed in stdout is under the bundle cwd.

### Binding run (in /tmp scratch, read-only)

I ran both binder versions against copies of the frozen files in `/tmp/rr22-scratch-TBR5`:

```
python3 cb-496d212.py --bundle bundle.json --expected expected.json --json
python3 cb-c9ff09f.py --bundle bundle.json --expected expected.json --json
```

Both printed `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": []}` and exited 0.

I did not run the registry command and did not run any suite.

## What is present and what is inferred

Present as retained bytes: the requirement, the receipt fields, the full stdout and stderr, the exit code, the timing interval, and the bundle digest.

`replay.py:54-71` explains where the receipt fields come from:
- The receipt `argv` is copied from the registry source row (line 62), and `cwd`/`revision` are the replay's own variables. None of them is observed from the child process.
- `run_row` at 496d212 (`tools/registry-check.py:676-683`) runs `subprocess.Popen(row["argv"], cwd=cwd, env=row_env())` with no shell. The copied argv and cwd therefore describe what was actually executed, by construction (from reading the code).

Inferred, not evidenced: [INFERENCE] that the process really ran in a clone checked out at 496d212. The receipt's revision is the value the replay passed to `git checkout`, not a value read back from the clone after the run. The interpreter that `python3` resolved to on PATH and the child environment are not recorded either.

Producer authentication: rejected. `expected.json` was written by the same producer in the same run (`replay.py:74-75`). Its authority comes only from being frozen in git commit 8f66b5d, not from the caller owning it.

Historical retrofill: not present. The stdout path contains the round-23 temp dir `naxu6fzi`, which equals the bundle cwd. It is not a copy of the round-17 trace (`round-17/coldread/traces/CR54/04-reattribute-selftest.json`, cwd `/tmp/tameshi-r17w2-CR54-VmFLip`).

Provenance side note: `observations.runner_sha256` hashes the live repo's `tools/registry-check.py` (`replay.py:78`), not the clone copy that actually ran (`replay.py:54`). For this run the value is still right: cba16646… equals the blob at 496d212, 8f66b5d and c9ff09f. As a field, though, it describes the wrong file.

## Concrete adversarial deltas (scratch, each delta re-pinned with a fresh expected digest)

Each delta was checked with both the 496d212 and the c9ff09f binder, and both gave the same result.

| Delta applied to this row | Binder result |
|---|---|
| D1: `sha256=` on stdout line 1 replaced with 64 zeros | exit 0, CLEAN |
| D2: stdout replaced by `SELFTEST: PASS (new rule 0/0; old rule fails 0/0; old-rule fidelity 0/0)` | exit 0, CLEAN |
| D3: stdout `SELFTEST: FAIL (new rule failed 8 of 8)\nSELFTEST: PASS` | exit 0, CLEAN |
| D4: stdout path rewritten to the live lane `/home/vgpnk/Projects/shokunin/…`, cwd field left on /tmp | exit 0, CLEAN |
| D5: bundle requirement weakened to `{"exit":0}` and stdout emptied | exit 0, CLEAN |
| C1 (control): token changed to `SELFTEST: FAIL` | exit 1, STDOUT_MISMATCH |
| C2 (control): argv truncated | exit 1, ARGV_MISMATCH |
| C3 (control): exit set to 1 | exit 1, EXIT_MISMATCH |

What the deltas show:
- **Receipt digest and counts are unchecked (D1, D2).** The digest of the frozen round-15 receipt and the 8/8 and 14/14 counts are evidence-bearing, but nothing checks them. `reattribute.py` does not check them either: its docstring at line 14 says it "verifies and prints the file sha256", but `_load_receipt` (lines 144-148) only hashes and prints. Its pass condition at line 325 never looks at the row count or the digest.
- **Stdout can contradict cwd (D4).** A receipt whose stdout disagrees with its own cwd field is accepted.
- **Bundle requirements are not cross-checked (D5).** The binder never compares bundle requirements against the frozen `requirements.json` or registry. A producer who also writes `expected.json` can weaken a requirement unnoticed. For this row the retained bundle requirement does equal the frozen one, as checked above.

All five are outside the declared contract. The docstring at `command-binding.py:7-13` limits checks to the token and disclaims producer authenticity and independent cold reads. That is why they are hazards, not a FINDING.

Impacted axes, if a later round claims more than exact binding: evidence strength of the token, and provenance of `expected.json`.

## Status at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df

- The `tools/registry.json` row is identical, including argv, expect, timeout 60, source and `status: active`, at 1f73157, c9ff09f and HEAD 5b69fb2. It is not superseded.
- The registry blob digest changed from ebd2e69a… to a8f255f1… because of other rows, not this one.
- `reattribute.py` (eaf564e4…) and `round-15/verification-3.json` (3c419055…) are unchanged.
- The `command-binding.py` diff from 496d212 to c9ff09f only touches selftest fixture loading (lines 164-172, which add round-24 extra cases). `evaluate()` and `check()` are byte-identical.
- The frozen check and all eight deltas gave the same results under both binder versions. The AGREE verdict and the residual hazards both carry over unchanged.

## Smallest safe correction (for the residual hazards only; no binding defect to fix)

1. Strengthen this registry row's `stdout_contains` with `sha256=3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce` and `old-rule fidelity 14/14)`. That rejects D1 and D2, and needs only a registry edit plus a re-pinned requirements file.
2. Correct `reattribute.py:14`: either drop "verifies" or compare the digest against the pin in `round-16/attribution/correction.json:54`.
3. If a later claim depends on requirement provenance, have the binding consumer compare bundle `requirements` with the independently frozen `requirements.json` (rejects D5).

## Tooling

Nothing installed or updated. The only scratch is `/tmp/rr22-scratch-TBR5` and `/tmp/rr22-registry-check-496d212.py`. There were no repo writes other than this report.

R23-REATTACK Replay22: AGREE
