## MistakeRule findings (C1 / QUALITY46 / round-23 Mistakes)

**No file was written.** The Target asks for `.ufo/waves/round-23/w2/MistakeRule.md`, but the wave context forbids writes and says L1 persists final-answer findings. I followed the context. I ran no commands and installed nothing; all evidence is from reading files and code.

### Verdicts

| Item | Verdict | Rationale |
|---|---|---|
| **QUALITY46** (`corpus/QUALITY.md:457-468`) | **Admit only with narrowing** | The gate binds bundle-declared receipts. It does not bind a frozen requirement set (see Finding A). |
| **Round-23 Mistake row 1** (`lessons/round-23.md:42`) | **Admit** | Pointers resolve (`Command30.json`, `CountReceipts.json`, `round-21/coldread/ledger.json`, `round-23/source-traces/source-1925.json`). Captured-by is supported: QUALITY39 (`QUALITY.md:361-363`) says it does not certify required-command coverage. |
| **Round-23 Mistake row 2** (`lessons/round-23.md:43`) | **Admit; fix pointer** | `route-mix-before.json:34/64` is a broken line anchor. The file has 5 lines. The 34/64 fact is on line 3, in stderr (`zai=34/64`). The "25/64" rebalance claim is unverified; I did not open `route-mix-final.json`. |
| **Round-23 Mistake row 3** (`lessons/round-23.md:44`) | **Admit** | `record1-refused.json:3` carries `invalid_registry_path`. |
| **Historical R17-CMD-BIND** | **Remains OPEN. Do not claim closed.** | Stated open in `lessons/round-23.md:109-112`, `LOG.md:1550`, `SCORECARD.md:1064`, `SKILL.md:2030-2031`, and QUALITY46's own text (`QUALITY.md:463-468`). The round-17 lesson's G5 row (`round-17-verifier-spotcheck.md:324`) still records the trace-argv residual. I found no live doc claiming closure. |

### Verified evidence (read, not re-run)
- Ruler: 10/10 discriminated, control clean (`c1-after-A.json`).
- Selftest: 38/38 (`selftest-A.json`).
- Mutants: 10/10 killed, restored and source-unchanged (`mutations-A.json`).
- Replay: `REPLAY: 43 / 43` (`replay-command-A.json:24`); gate exit 0 (`replay-gate-A.json`).
- Source-read substitution: `ARGV_MISMATCH` (`source-read-gate-A.json:22`). Correct command: clean (`correct-command-gate-A.json:22`).
- Every gate receipt pins the same tool bytes, `d533dc…`.

### Findings against the claim

**A. The gate cannot see the frozen requirement set (main issue).** `tools/command-binding.py:67-113` takes `requirements` only from the bundle and compares them to the bundle's own receipts. `check()` (`:115-130`) only checks the digest. Nothing reads `requirements.json` or the registry. A bundle that drops one requirement and its receipt, then re-pins its digest, returns exit 0. No ruler case, selftest case, or mutant covers this. The ruler's `missing-required-command` pops a receipt, not a requirement. None of the 19 extra cases drops a requirement. The lesson concedes this at `round-23.md:89-92`, but the knowledge doc's Bounds section does not. QUALITY46's "freezes its requirement set before execution" is therefore enforced only by `replay.py:34-41`, not by the gate. Either narrow the wording or add a falsifier: a frozen-digest mismatch for a truncated bundle.

**B. Replay receipts are declared, not observed, for argv, cwd and revision.** `replay.py:62,68-69` copies `argv` from the registry row, and `cwd` and `revision` from the variables it passed in. Only `exit` and `stdout` come from the runner. The runner executes `row["argv"]` in `cwd` (`registry-check.py:676-681`), so the values are equal by construction [INFERENCE]. The bundle's `cwd` is a `TemporaryDirectory` path that is deleted when `main()` exits (`replay.py:45`). The knowledge doc's workflow step 2 asks for actual argv, cwd and revision to be retained.

**C. "No live lane or sibling writes" is asserted, not evidenced.** `replay.py:51-53` symlinks every `*-shokunin` sibling into the fleet root. Round-18 N01 (`round-18.md:27`) rejected this condition as a write boundary. No before/after sibling digest is retained.

**D. Revision lineage is unresolved.** Gate and replay receipts pin `496d212bc46789cdf8cafab72978bdb7f4182963`. The contract and `.git/HEAD` give the delivered revision as `336565fc2e70e034307ef267aaa2018572c200d3`. The registry and monitor receipts (`registry-C`, `monitor-current-C`) use `336565fc`. `knowledge/required-command-binding.md:66` and `lessons/round-23.md:64` name `496d212` without relating it to `336565fc`. I did not run git. L1 must establish whether the two revisions hold the same `command-binding.py` bytes before treating `496d212` as delivered evidence.

### Recommended before L1 admission
1. Narrow QUALITY46 and the knowledge doc to bundle-declaration binding. Add a frozen-requirements-digest falsifier, or drop "freezes its requirement set" from the gate claim.
2. Fix the row-2 pointer to `route-mix-before.json` line 3.
3. Retain before/after sibling digests, or drop the "no sibling writes" claim.
4. Relate `496d212` to `336565fc`, or re-measure at the delivered revision.
5. Keep R17-CMD-BIND open in every live doc.

### Checks for main agent
None run by me. Suggested after integration: `python3 tools/command-binding.py --selftest`, and the frozen ruler `measure.py --repo REPO_AT_REV`.
