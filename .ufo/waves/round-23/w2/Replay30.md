The `assemble-round18-selftest` row is statically bound exactly, so I found no false acceptance in this row's own fields. The gate does have one field-level false acceptance: it checks `revision` only against the bundle's own revision, so any well-formed 40-hex commit is accepted. I did not write `.ufo/waves/round-23/w2/Replay30.md`, because this wave forbids report writes; the findings are below for L1 to persist.

**Static binding: confirmed, from evidence I hashed myself**
- **Baseline source matches.** I read blobs straight from the git object store; L1's word that the copies match was not enough.
  - `registry-baseline.json` is byte-identical to `28cae179:tools/registry.json` (sha256 `ebd2e69a…`).
  - The row at `28cae179` has argv `["python3", ".ufo/evidence/round-18/coldread/assemble.py", "--selftest"]` and expect `{exit: 0, stdout_contains: ["SELFTEST: "]}`.
  - That argv and expect are identical in `requirements.json` row 29, `bundle.requirements[29]`, `bundle.receipts[29].argv` and `observations.rows[29]`.
  - All 43 bundle requirements equal the frozen list. The row is also unchanged in the current `tools/registry.json` at HEAD.
- **The executed files are the expected ones.**
  - `assemble.py` has the same blob (`bf7c12f7…`) at `28cae179`, `496d212b` and `336565fc`.
  - The runner `tools/registry-check.py` at `496d212b` (`cba16646…`) matches the recorded `runner_sha256`. That field actually hashes the live checkout, not the clone that ran; the values are equal here only because the blobs match.
- **Full output is present, not just a tail.**
  - The receipt stdout is 7,930 characters and identical to the observation's stdout. It has 80 `[ok]` lines and no failures, and ends with `SELFTEST: 80/80 pass`.
  - The 4,094-character `stdout_tail` is a true suffix of it; stderr is empty and the exit is 0.
  - `assemble.py` lines 1920–1925 return 1 whenever any check fails, so exit 0 does mean every check passed.
- **Timeline is consistent.**
  - Commit `496d212b` landed at 14:41:18 UTC and the replay ran from 14:42:22 to 14:44:58 UTC.
  - This row's 0.182 s interval matches its `elapsed_s`.
  - HEAD `336565fc`, committed at 14:47:40 UTC, contains `bundle.json` with the same digest as `expected.json` (`3d6c99b7…`).
- **What is inferred rather than observed:**
  - That the process really ran (producer authenticity, which this gate rejects as a claim).
  - That the temporary clone was checked out at `496d212b` when it ran.
  - Which interpreter `python3` resolved to; it is found via PATH and not recorded.
  - That the receipt argv was what actually ran: it is copied from the registry row, so for replay bundles `ARGV_MISMATCH` can never fire. That holds only because the runner calls `Popen(row["argv"])` unchanged.
  - No historical metadata was retrofilled: `registry-C.json` keeps tails only, and the receipt fields are new.

**False acceptance: the `revision` field (static, not executed)**
- `evaluate()` compares `receipt.revision` with `bundle.revision`, and `revision()` only checks the 40-hex format.
- Nothing ties the bundle revision to the contract base `28cae179`, the frozen implementation `336565fc`, or even an existing commit.
- `expected.json`, described as the "trusted caller-owned commitment", was written by `replay.py` in the same run. In practice it only pins the bundle's bytes to themselves.
- Counterexample: set `bundle.revision` and all 43 receipt revisions to `"0"*40`, regenerate `expected.json`, and the gate reports exit 0 with no findings. The `cwd` field has the same weakness: `/tmp/tameshi-r23-replay-naxu6fzi/...` is a temporary path that no longer exists, and only its syntax is checked.
- Affected axes: calibration and false provenance (revision identity).
- Smallest safe correction: have the caller-owned `expected.json` also pin `revision` and a digest of the requirements list (canonical JSON), and have `check()` report a mismatch on either.

**Adversarial delta for this row (a tradeoff, not a gate defect)**
- The frozen token `"SELFTEST: "` does not pin the number of checks. A regressed `assemble.py` that drops 79 checks prints `SELFTEST: 1/1 pass` and exits 0, and the gate would accept it.
- This weakness comes from the registry. Fixing it would mean changing the frozen contract, which is outside C1; record it as an accepted tradeoff.

**Scope and tooling**
- I ran only read-only fact commands: Python/JSON and sha256 checks, `date`, and reads of the git object store.
- I did not invoke git or jj, and did not run any suite, the registry command or the gate.
- Install: `dulwich` 1.2.17 through `uv run --no-project --with dulwich` (ephemeral uv cache, uv 0.13.0). Reason: read blobs at given revisions without spawning git.
- Historical R17-CMD-BIND is not claimed closed.
