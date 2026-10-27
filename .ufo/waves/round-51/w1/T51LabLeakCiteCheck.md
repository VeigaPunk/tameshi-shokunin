# Seat T51LabLeakCiteCheck — sandbox-id leak audit of recorded leg `js-cite-check` (round-51 C2 context)

Date: 2026-10-26/27 (UTC). Lane tip at read: `4e095c9caf8097c724ec347812ba2252ca2a74e4`; runner `tools/mutate-and-run.sh` sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (identical before and after the sweeps — the cold-read-sensitive runner was never written).

## Item
Audit the recorded leg `js-cite-check` for the round-51 C2 sandbox-id leak. The leg's suite (runner `tools/mutate-and-run.sh:1428`) names its sandbox `sandbox-$DEFECT_ID`. Hypothesis to falsify: **none of the recorded verdicts (TABLE_CITECHECK) depends on the defect id appearing in the sandbox path.**

## Method
1. **Materialize the pinned target.** `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > target.cite-check.mjs`; `sha256sum` = `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f` = `PIN_CITECHECK` (runner:621). `git ls-tree 1205c662… -- scripts/cite-check.mjs` → mode `100755` → `chmod +x`. Result: 2537 lines / 126735 bytes (matches the spec header comment at runner:1086).
2. **Extract the embedded spec verbatim** (heredoc lines 1085–1141 of the runner): `awk 'NR>=1085 && NR<=1141' tools/mutate-and-run.sh > js-cite-check.spec` → 10 `@defect` blocks. The runner's `py_helper` asserts exactly one `@old` occurrence per defect before any run; all 10 applied in both sweeps (mutant shas all differ from pristine).
3. **Two sweeps via the recorded runner CLI**, identical except the single variable — the sandbox-name expression in the suite string:
   - **A (recorded suite)**: `bash tools/mutate-and-run.sh --target target.cite-check.mjs --defects js-cite-check.spec --suite "$(cat suiteA.txt)" --workdir sweepA --label js-cite-check-A --timeout 300 --tail 8` with `suiteA.txt` = the line at runner:1428 verbatim (`h="$WORKDIR/sandbox-$DEFECT_ID"; …`).
   - **B (neutral sandbox)**: same invocation, `suiteB.txt` = the same line with the sandbox expression replaced by a per-run counter: `o=$(cat "$WORKDIR/ordinal" 2>/dev/null || echo 0); o=$((o+1)); echo "$o" > "$WORKDIR/ordinal"; h="$WORKDIR/sandbox-n$o"; …`. Observed sandbox dirs: `sandbox-n1` (control) … `sandbox-n11` — no defect-id string appears in any B path.

## Findings
1. **Sweep A reproduces the recorded table exactly.** `CONTROL: GREEN`, `MUTATE_RESTORE: OK`, `MUTATE: DONE (killed=5 survived=5 inconclusive=0 kill-rate=50%)`; `results.tsv` matches `TABLE_CITECHECK` (runner:631) 10/10, 0 flips; exit column matches KILLED→1 / SURVIVED→0.
2. **Sweep B yields identical results**: same verdicts and same exit code for every defect. `compare.txt` shows SAME on all 10 rows; `diff <(cut -f1-3 sweepA/results.tsv) <(cut -f1-3 sweepB/results.tsv)` → empty.
3. **No defect's verdict differs** ⇒ the hypothesis is **not falsified**: the recorded `js-cite-check` verdicts do not depend on the defect id appearing in the sandbox path.
4. **No selftest assertion matched the id** — the requested list is vacuous (zero differing verdicts). Mechanism: the suite oracle is the hermetic 62-case selftest *exit status* (spec header, runner:1087: "verdict oracle = exit status only"). The evidence logs print scratch paths (e.g. `control.out` tail: `src=/…/sandbox-CONTROL/tmp/kumitate-cite-selftest-…/…`; each `evidence/<id>.out` prints its `sandbox-<id>`/`sandbox-nN` path), but the id-in-path string never feeds the exit code — nothing in the node suite greps its own output.
5. **Only the variable differed**: all 10 mutant files are byte-identical across A and B (each mutant-sha256 pair identical), and every mutant differs from the pristine blob.

## Receipts — `.ufo/waves/round-51/w1/T51LabLeakCiteCheck/`
- `target.cite-check.mjs` (materialized pinned blob), `js-cite-check.spec` (extracted embedded spec)
- `suiteA.txt`, `suiteB.txt` (the two suite strings; the one variable)
- `sweepA.log`, `sweepA.exit`, `sweepB.log`, `sweepB.exit`
- `sweepA/` — `results.tsv`, `defects.tsv`, `spec.copy`, `pristine.target.cite-check.mjs`, 10 `mutant-<id>.target.cite-check.mjs`, `evidence/` (control.out + 10 `<id>.out`)
- `sweepB/` — same layout plus the `ordinal` counter file
- `compare.txt` — per-defect verdict+exit comparison (SAME × 10)

## Commands (all from the scratch root; lane checkout read-only)
- `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > target.cite-check.mjs`
- `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin ls-tree 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a -- scripts/cite-check.mjs`
- `sha256sum target.cite-check.mjs`
- `awk 'NR>=1085 && NR<=1141' /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh > js-cite-check.spec`
- `bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --target … --defects js-cite-check.spec --suite "$(cat suiteA.txt)" --workdir sweepA --label js-cite-check-A --timeout 300 --tail 8` (and identical with `suiteB.txt`/`sweepB`/`js-cite-check-B`)
- comparison: `awk -F'\t'` join of the two `results.tsv`; `diff <(cut -f1-3 sweepA/results.tsv) <(cut -f1-3 sweepB/results.tsv)`

## Summary
- Audited recorded leg `js-cite-check`: suite at `tools/mutate-and-run.sh:1428`, call at :1426–1429, recorded table `TABLE_CITECHECK` at :631, embedded spec at :1084–1142.
- Pin materialized from kumitate-shokunin @ `1205c662…`: sha256 = PIN_CITECHECK, mode 100755, 2537 lines; spec extracted with 10 defects.
- Sweep A (recorded `sandbox-$DEFECT_ID`) reproduces TABLE_CITECHECK 10/10 — 5 KILLED / 5 SURVIVED, control green, restore OK.
- Sweep B (neutral `sandbox-n<ordinal>`, n1..n11) gives identical verdicts and exits for all 10 defects.
- Zero differing verdicts ⇒ hypothesis not falsified: recorded js-cite-check verdicts do not depend on the defect id in the sandbox path; nothing to list under "assertion that matched the id".
- Oracle is the 62-case hermetic selftest exit status; evidence logs print scratch paths but the path string never influences the verdict.
- Mutant bytes identical across sweeps; runner untouched (sha stable `a7d3f2dd…`); no tools installed.
