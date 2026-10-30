# T58W1Verify02 — R51.1–R51.4

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. All four independently re-derived rows are `fixed` at base; machine-readable rows are in `T58W1Verify02.json`.

- **R51.1 — fixed, `bcba8924894216268afc4171f06eb8c28e912b46`.** On the detached base clone, `git show <base>:tools/registry.json` (file excerpt lines 1251–1270) shows active `mte-interop-check` expects `MTE_INTEROP: PASS legs_conforming=10/10`. The commit log names `bcba892` as the ten-leg registry-row correction. The baseline/routed source lacked this corrected expectation.
- **R51.2 — fixed, `bcba8924894216268afc4171f06eb8c28e912b46`.** `git show <base>:SKILL.md` lines 1003–1006 identifies exact ledger-leg accounting and the ten-leg round-51 milestone; lines 1359–1363 explicitly state `TMPDIR honoured since r51`. These provide whole-token key evidence and show the corrected guidance.
- **R51.3 — fixed, `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`.** `git grep -n -F 'T51W2Read20' <base> -- .ufo/evidence/round-21/coldread/ledger.json` locates the appended correction at lines 135654–135698. The record says `wrong_expectations: 7` and `corrects` the R26 entry's erroneous zero. Commit subject identifies round-52 wave-2 correction records.
- **R51.4 — fixed, `bcba8924894216268afc4171f06eb8c28e912b46`.** `git show <base>:SKILL.md` line 2157 identifies `tools/round21-measure.py --selftest`, records `ROUND21_MEASURE_SELFTEST: 13/13 pass`, and explicitly labels the facade `fleet-bound, not hermetic`; the surrounding text explains its sibling-blob dependency.

Commands and outputs relied on: created a shared clone and detached it at the specified base; `git -C "$C" log --format='%H %s' --all --grep='round-51\\|round-52'` showed `bcba892... round-52: C1 registry row 10/10 + fleet-bound round21 self-test; C2 SKILL corrections...`; `git -C "$C" grep -n -F 'T51W2Read20' <base> -- .ufo/evidence/round-21/coldread/ledger.json` returned line 135656 reader and line 135658 count 7; targeted `git show`/file reads supplied the excerpts above. No decline is recorded for these items.

No tools installed or updated. Scratch clone removed before handoff. No build, test, lint, or formatter run.
