# RevengerCounterDiff — reverse-check of the v3→v4 C1 counter change

- Seat: TameshiR30A2.RevengerCounterDiff-7 (wave A, attempt 2, policy v1)
- Date: 2026-10-23
- Scope: the frozen counter pair `.ufo/evidence/round-30/c1-measure-v3.py` / `c1-measure-v4.py`, the draft `.ufo/evidence/round-30/v4/c1-measure-v4-draft.py`, `contract-amendment-3.json`, and the base receipts. Read-only except this report. The sealed set under /fast/scratch/hyaku/tameshi-r30a2 was never opened, listed, or searched.

## Verdict

**CLEAN — no correction.** Every hunk of v3→v4 and of draft→v4 is one of the changes amendment 3 declares; no condition (a)–(i) is weakened (the predicate is strictly monotone); `sealed_items()` refuses a sealed file whose hash differs (counter error, exit 2); the block-mismatch path yields `sealed_block_match=0` and `PASS=false`, exit 1; and the bwrap-sandboxed selftest runs the pristine runner identically to v3 at base (all 46 `C1_R30_ROW` lines byte-identical, including the pristine row).

Confidence: high for the diff inventory, monotonicity, seal gate and receipts (directly observed). Medium-high for "no hidden leak remains in the sandbox" — that is the L1's own open question, attacked by control wave ctl2; nothing I observed contradicts the sandbox's stated isolation.

## Axes (godspeed)

1. Diff completeness — is the observed v3→v4 delta exactly the declared one, with nothing else?
2. Monotonicity — does any change turn a v3 failure into a v4 pass?
3. Seal integrity — does the counter bind itself to the committed sealed bytes and the frozen tally block?
4. Pristine equivalence — does the sandbox change what the pristine runner does at base?

## Evidence

### 1. v3→v4 diff inventory (command: `diff -u c1-measure-v3.py c1-measure-v4.py`)

77 insertions, 11 deletions, all in six hunk groups. Each maps to a declaration in `contract-amendment-3.json`:

| # | Hunk | Declared by amendment 3 |
|---|------|-------------------------|
| 1 | Docstring: title v3→v4, `--sealed` usage, v4 narrative, clauses (j)/(k), sealed counter-error sentence | `predicate` adds (j) and (k); `counter` line is `c1-measure-v4.py --sealed SEALED_JSON`; narrative matches the `reason` (CtlK8NoRun met v3, SealHeldout died, task not resent) |
| 2 | `import hashlib`, `import json` (c1-measure-v4.py:82-83) | Implied and required by (j): file sha256 gate and JSON parse of the sealed set |
| 3 | `SEALED_SHA256` (line 259), `SEALED_N` (260), `sealed_items()` (263-282) | `sealed_sha256: 44116804…3729` — byte-equal to the constant at line 259; (j) block_sha256 clause; counter-error sentence |
| 4 | `BWRAP` (321-327) + `selftest()` rewritten to mkdtemp + bwrap (329-340) | `predicate`: "(a)-(i) … hold under v4's sandboxed selftest runs"; docstring declares the draft's `st-<jobname>` directory leak that motivated it |
| 5 | `--sealed` required argument (line ~349) | `counter` command line includes `--sealed SEALED_JSON` |
| 6 | Sealed items in generator sanity checks, jobs list, `skilled`/`sequiv` tallies, `ok` conjuncts (432-434), output fields (435-438) | (j) `sealed_killed == 6`, (k) `sealed_equiv == 6`; the receipt `before.value` itself shows the three new output fields, so the format change is declared |

Observed file hashes: `sha256sum` gives c1-measure-v4.py = `cccae0bd984a7c67c22d83a1e67d19e3ebc76c015094106a1370d330030a5f07` (equals amendment 3 `counter_sha256`) and c1-measure-v3.py = `3188d4f8…6144f8` (equals amendment 2 `counter_sha256`). The diff output contains no other hunks.

### 2. Draft→v4 diff (command: `diff -u v4/c1-measure-v4-draft.py c1-measure-v4.py`)

Exactly two hunks, both the one declared change (selftest isolation):

- Docstring paragraph "v4 also isolates every --selftest run …" — the declaration of the sandbox and the draft leak it closes (a selftest could key on its own directory name `st-S-e-preinc`, on `/proc/$PPID/cmdline`, the counter source, or the sealed file).
- `BWRAP` + the `selftest()` body: `d = tempfile.mkdtemp(prefix='w', dir=os.path.dirname(tree))` and `subprocess.run(BWRAP + ['--bind', d, '/w', '--chdir', '/w', 'bash', RUNNER, '--selftest'], …)`.

Nothing else differs; draft sha256 is `5450434c…3eac36` (not a committed value; it is the variant referenced by amendment 3's K9 receipt "on the draft v4/K9-on-draft.stdout PASS=true", which shows the draft is defeated by K9 while v4 is not). Provenance note: the draft file's mtime (02:36:37) is newer than v4's (02:33:47), consistent with the draft being preserved/reconstructed as the pre-hardening variant for that receipt. [INFERENCE on sequencing; bytes and hashes are observed.]

### 3. No weakening of conditions (a)–(i)

The `ok` conjunction at c1-measure-v4.py:432-434 is v3's line verbatim plus `and smatch == 1 and skilled == 6 and sequiv == 6`. No v3 term is removed, relaxed, or reordered; the predicate is a strict superset, matching amendment 3's own monotonic note (K1–K5, K7 stay failed). The only evaluation-environment change touching (a)–(i) is the bwrap wrapper around `--selftest` runs (the `harness()` block instrument at 308+ is untouched). The sandbox can only turn a selftest pass into a failure (non-zero exit or timeout=124), never the reverse: it clears the environment, hides the counter source and sealed file, unshares pid/net/ipc/uts/user namespaces, and gives every job the same mount path `/w` with a random directory name, so no job-label channel survives. Kills under "or times out" had the same 300 s timeout semantics in v3. Empirical cross-check: at base, v4/base.stdout reproduces every v3 field identically (`pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4 insert_killed=0/8 insert_equiv=4/4`).

### 4. sealed_items() refuses a wrong-hash sealed file

c1-measure-v4.py:265-267 reads the sealed bytes and raises `CounterError('sealed file sha256 does not equal SEALED_SHA256')` when `hashlib.sha256(raw)` differs from the constant at line 259. The handler at 442-445 prints `C1_R30: counter error: …`, `PREDICATE: C1_R30_PASS=false` and returns 2. So a forged or stale sealed file cannot inject items; it can only abort the measurement as a counter error (a miss under the contract, not a pass).

### 5. Block-mismatch path gives PASS=false

c1-measure-v4.py:269-271: after the file-hash gate passes, if `sha256(tally_block(text))` differs from the JSON's `block_sha256`, `sealed_items` returns `(0, [], [])` — no sealed jobs run, `smatch=0`, so `smatch == 1` fails in the `ok` conjunction at line 434 → `PREDICATE: C1_R30_PASS=false`, exit 1. Returning a measured 0 instead of a counter error is correct per (j)'s wording: the mismatch says the runner is not the frozen fix's, which is exactly what the predicate must detect. Observed at base: v4/base.stdout:47 `… insert_equiv=4/4 sealed_block_match=0 sealed_killed=0/6 sealed_equiv=0/6`, line 48 `PREDICATE: C1_R30_PASS=false`; corroborated by amendment 3's K8 receipt (`v4/K8.stdout`: sealed_block_match=0, PASS=false).

### 6. Pristine runner unchanged under the sandbox

`diff -u .ufo/evidence/round-30/v4/base.stdout .ufo/evidence/round-30/c1v3-at-base.stdout` reports a single hunk `@@ -44,5 +44,6 @@`. Both files hold 46 `C1_R30_ROW` lines, all byte-identical, including line 1:

```
C1_R30_ROW: pristine selftest_exit=0 verdict_pass=1
```

The only differences are the v4 summary line's three appended declared fields (`sealed_block_match=0 sealed_killed=0/6 sealed_equiv=0/6`) and a trailing `exit=1` line present only in c1v3-at-base.stdout:49 — a capture-wrapper artifact of the v3 receipt (`cmd; echo exit=$?`), not counter output; the counter's own last printed line is the `PREDICATE:` line in both (code tail, lines 435-445). So the bwrap selftest runs the pristine runner identically at base: exit 0, `VERDICT: PASS`, same rows, same summary values.

## Divergences found

None material. Two non-defects recorded so nobody reads them as drift: (1) the trailing `exit=1` line in c1v3-at-base.stdout (capture artifact, above); (2) draft mtime newer than v4 (variant preservation for the K9-on-draft receipt, above).

## Tooling

No tools installed or upgraded (none needed; diff/grep/sha256sum sufficed). No processes left running; no writes outside this report.

## Report

.ufo/waves/round-30/wA/RevengerCounterDiff.md
