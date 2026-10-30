# T58W2MutC2 — mutation probes on the round-58 C2 counter (wave 2)

**Verdict: verified-record — 4/4 mutants killed.** Every kill is delivered by the
counter's own 23-case selftest; only one mutant is additionally caught by the
installed-registry run, because on a clean C0 ledger a weakened counter still
prints `total=0`. The decisive wave-1 bent-runner forgery was reproduced
verbatim (the frozen counter prints PASS on a lane whose executor never runs a
row). Pristine bytes restored; detector re-run green.

- Lane: `tameshi-shokunin`, C0 `8063d0a551fc5b3cb5a2d397da7353af53444534` (newest at dispatch; `git log --oneline -3` head)
- Target copy: `.ufo/evidence/round-58/c2/measure.py`, pristine sha256 `d4219039f02c1fd389cb47ca2b9968d0335e4254e8477c012fd2cdfbccd3b984` (== C0 blob `43fa0631`); `mutants.json` sha `d51f558c…` == the counter's pin
- Detector (identical for pristine / each mutant / restored):
  - `python3 measure.py --selftest --lane <c0-clone> --rev 8063d0a5…`
  - `python3 measure.py --lane <c0-clone> --rev 8063d0a5… --work <ABSOLUTE dir> --explain`
- Baseline (pristine): selftest `23/23 pass` exit 0; installed run `total=0 C2_R58_PASS=true` exit 0 (receipts `base-selftest.txt`, `base-measure.txt`)

## Mutants (one per axis, smallest behavior-bearing point)

| id | axis | line | mutation | selftest | installed-registry | killed by | verdict |
|----|------|------|----------|----------|--------------------|-----------|---------|
| MUT1 | executed tally | 404 | `held += state == 'held'` → `held += 1` | FAIL `22/23` (`executed arm: a row expecting the wrong exit does not hold FAIL held=3/3`) | PASS `total=0` exit 0 | selftest | killed |
| MUT2 | cell fixture | 333 | `receipt.write_text('VERDICT: rev=%s C1_X_PASS=true\n' % rev_a)` → `% rev_b` | FAIL `19/23` (`good fixture` + 3 cell-arm cases, `standing_cell=WRONG:fixture`) | FAIL `total=1 PASS=false` exit 1 | selftest + registry | killed |
| MUT3 | codes parser | 454 | `known = [t for t in tokens if t in codes]` → `known = list(tokens)` | FAIL `22/23` (`codes arm: a token the gate does not define is counted FAIL codes_known=3/3`) | PASS `total=0` exit 0 | selftest | killed |
| MUT4 | verdict total | 472 | `res['total'] = sum(short.values())` → `res['total'] = 0` | FAIL `21/23` (`cell arm: a gate that does not refuse` asserts `total>0`; `mutants pin` asserts `main_measure` rc≠0 → printed `total=0 C2_R58_PASS=true` inside the selftest output) | PASS `total=0` exit 0 | selftest | killed |

Exact diffs in `receipts/MUT{1,2,3,4}.diff`; full outputs in `MUT*-selftest.txt` /
`MUT*-measure.txt`; machine-readable scores in `mutants-score.json`.

The verdict lines carry `self=<sha12>` — `d4219039f02c` pristine/restored,
`3a1f577b6120`/`3a34e4b37108`/`7a7df78657e2`/`811de4332b4a` per mutant — so the
mutated bytes provably ran.

**Why the registry run alone cannot catch MUT1/MUT3/MUT4:** at C0 every arm is
already zero, so a counter that stops checking state (MUT1), stops checking
code membership (MUT3), or zeroes the total (MUT4) prints the identical
`total=0 C2_R58_PASS=true`. Coverage for those axes lives in the selftest's
fixture lanes, not in the ledger pass — this is expected coverage design, not
a gap: the selftest *is* the detector that fires.

## Decisive wave-1 finding — reproduced as evidence

The bent-runner forgery (T58W1RevengerC2 ATTACK B) was re-run against the
**pristine** counter in scratch (`repro_forgery.py`, `forgery-repro.txt`,
matches wave-1's `attack-b-out.txt` exactly):

- Forged lane commits a cheat gate (refuses any verdict receipt with
  `RECEIPT_REV_CONTENT_DRIFT`, exits 0/3) plus a bent `tools/registry-check.py`
  that **never executes a row**: on a clean gate worktree it prints
  `ROW <name> expect=E got=E held`; only when the counter dirties the gate
  (mutants arm) does it print a fabricated `differs` with `got=E+1` — credited
  as kills.
- Counter output on the forged lane:
  `gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 skill_row=1 codes_known=2/2 standing_cell=ok total=0 C2_R58_PASS=true`
- The same forged lane under the **real** registry-check (bytes from
  `clone@C0`): `c2-fx-ok expect=0 got=3 differs` (rc=1) — the PASS was printed
  without a single row executing. Supports the L1's "C2 not admitted" call.

## Notes

1. **Relative-path invocation quirk (observed, invocation-side, not an
   invariant falsification):** `--work work-rel` (relative) silently corrupts
   the run — children resolve `TMPDIR=<work>/tmp` and the cell fixture's
   `--lane <work>/c2-cell-*` against their own cwd → all rows `rc=2` error,
   mutants `SURVIVED 0/3`, `standing_cell=WRONG:fixture`, `total=7 PASS=false`.
   A counterfeit FAIL, not a missed PASS; an absolute `--work` gives the true
   `total=0`. Receipt `quirk-relative-work.txt`; diagnosed via
   `run_probe.py` (children pass under absolute paths).
2. Round-58 strictness verified live at C0: substring-only `codes=X …`
   elements name no code (element equality), and the exit-2 row must name
   `RECEIPT_REV_UNRESOLVABLE` exactly — both strict selftest cases pass on
   pristine bytes.
3. Frozen target untouched: all mutations were applied to a byte-identical
   copy; the lane evidence dir was never modified.

## Restoration

`cnt/measure.py` restored to sha256 `d4219039f02c…b984` (bytes_identical=true,
verified by sha256sum after the run); restored bytes re-scored: selftest
`23/23`, installed run `total=0 C2_R58_PASS=true` (`restored-*.txt`).

Tools installed: none (python3 + git + stdlib only).

Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2MutC2` deleted before yield.
Report: .ufo/waves/round-58/w2/T58W2MutC2.md
