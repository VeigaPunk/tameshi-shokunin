For `round20-coldread-selector-selftest`, I found a static exact binding but not execution identity. The argv and expectations match the baseline field for field, and the retained receipt passes them. However, the gate also accepts a field-level false positive: the receipt's stdout does not show which program ran. A second gap is that the replay ran at revision `496d212`, not the delivered `336565fc`.

I did not write `.ufo/waves/round-23/w2/Replay36.md`. The wave context forbids all file writes, including report trailers, so L1 holds these findings. I ran no registry command, suite, build or git command, and installed nothing. Early on I ran one read-only listing command; its `sha256sum` output did not come back, so I verified no digests myself.

**Static binding: confirmed.** All of these say `["python3", ".ufo/evidence/round-20/coldread/measure.py", "--selftest"]`, exit 0, and stdout must contain `["SELECTOR_SELFTEST: 12/12 pass"]`:
- `registry-baseline.json` lines 845–852.
- `requirements.json` lines 517–529.
- The requirement in `replay/bundle.json` (line 1125) and the requirement copy in `replay/observations.json` (line 1602).

The bundle receipt (lines 486–497) has the same argv, exit 0, and empty stderr. Its stdout contains the token. The frozen requirement leaves out `timeout_s: 300`, `kind`, `tags` and `source` (`SKILL.md@4fc1b80b…:1951`), so the gate does not bind the timeout.

**Evidence present versus inferred:**
- **Present:**
  - The complete stdout in the bundle and in `observations.runner_result.stdout`: 12 `CASE … PASS` lines plus the summary line. It equals `stdout_tail` because the output is under the tail limit, so full-versus-tail makes no difference for this row.
  - Timing: `measurement_interval` is about 0.500 s, matching `elapsed_s` 0.5.
  - `replay-command-A.json` shows the line `round20-coldread-selector-selftest 0 True`.
  - `replay-gate-A.json` reports exit 0 with no findings, and its `bundle_sha256` equals `replay/expected.json`.
- **Inferred only:**
  - That the child process actually ran. `argv`, `cwd` and `revision` come from `replay.py` lines 62–71, copied from the source row and the clone variable, not observed from the process.
  - That the `/tmp/tameshi-r23-replay-naxu6fzi/...` directory existed. It is a `TemporaryDirectory` and is gone now.
  - That `python3` resolved to a particular interpreter. It went through `PATH`, and the executable is not recorded.
  - That `measure.py` at `496d212` matches `336565fc`. No digest of the script is retained.
- **At the delivered revision:** `registry-C.json` at `336565fc` has only `stdout_tail`, `held: true`. `executed-receipt-index.json` names `496d212` as the tool revision and `336565fc` as the source revision.

**False acceptance (counterexample).** The stdout check in `command-binding.py` (lines 111–112) is a substring test. `round21-coldread-selector-selftest` has the same token (baseline line 888). Its retained stdout (bundle line 549) is byte-identical to round 20's (line 497). So a receipt labelled round 20, with round 20's argv but stdout from the round-21 program, gets `finding_ids: []`. The same happens if round 20's `measure.py` at the bundle revision is replaced by round 21's. Once stdout carries no information, argv is the only thing distinguishing the rows, and argv is producer-declared.

**Adversarial delta (revision and self-commitment).** `REVISION_MISMATCH` only compares each receipt with the bundle's own `revision`. Nothing ties that field to the contract base `28cae179` (also `requirements.source_revision`) or the delivered `336565fc`. The bundle declares `496d212` and passes. `replay.py` lines 74–75 write `expected.json` themselves. So the "trusted caller-owned commitment" in this run came from the producer, and `SNAPSHOT_TAMPERED` only shows the bytes have not changed since they were written. Likewise, `CWD_MISMATCH` compares two fields set from the same variable, so this replay can never trip it.

**Affected axes:** execution identity, freshness against the delivered revision, and duplicate authority (producer-written `expected.json`).

**Smallest safe correction:** have the caller-owned `expected.json` also pin `revision` and a `requirements_sha256`, and have the gate check both. Bind each receipt to the program it ran with an `argv_sha256` of the script resolved at the revision. If that is not taken up, a lighter option is to treat byte-identical stdout across different argv as `STDOUT_MISMATCH`.

None of this shows that producers are authentic, back-fills historical metadata, or closes R17-CMD-BIND. I also could not find the godspeed skill file under `~/.omp`, so I applied its four axes directly.
