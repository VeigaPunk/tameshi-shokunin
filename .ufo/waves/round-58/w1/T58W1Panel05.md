# T58W1Panel05 — blind calibration

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538` (detached shared clone, confirmed by `git -C CLONE rev-parse HEAD`). Axes: verdict accuracy, independent evidence, complete five-item coverage, blind-boundary preservation. No lane content changes or staged fixes.

Receipts directory: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel05-receipts/`.
All actual Git commands and their stdout/stderr/exit codes are preserved there. `CLONE` below is `/fast/scratch/hyaku/tameshi-r58/T58W1Panel05/clone`; `BASE` is the full hash above. Source-object selectors such as `BASE:path` use Git's repository-relative object syntax, not a filesystem-relative write.

## Findings by severity

### R53.3 — open: unsupported execution claim

- `git -C CLONE ls-tree -r BASE -- CLONE/.ufo/evidence/round-53/control` lists only `break-fixtures.py`, `controls.py`, and `controls.{exit,stderr,stdout}`. See `r533-control-tree.txt`.
- `git -C CLONE show BASE:.ufo/evidence/round-53/control/controls.stdout` prints only two BASE controls and `CONTROLS: total=2 pass=2`, not a phase-B run. See `r533-control-tally.txt`.
- Literal `functions.grep` for `CONTROLS_B:` across the round-53 evidence and wave trees returns only the printer at `control/break-fixtures.py:169`. Exact request/output recorded in `tool-observations.txt`.
- `SCORECARD.md:2516-2519` still says phase-B fixtures each printed false and the positive candidate true. Later rounds' control receipts cannot establish execution of these round-53 fixtures.

### R53.4 — open: unresolvable receipt identity

- `git -C CLONE show BASE:.ufo/waves/round-53/w1/T53W1ExecTmpVerify-receipts/c2-counter-repaired.stdout` returns `rev=9c6ef7bc80c0 ... cr47=rc=1 ... C2_R53_PASS=true`.
- `git -C CLONE rev-parse --verify '9c6ef7bc80c0^{commit}'` exits **128**, `fatal: Needed a single revision`.
- Receipts: `r534-original.txt`, `r534-object.txt`. The original unanchored record remains; future-round binding rules do not anchor it retrospectively.

### R53.5 — open: stale freeze record

- `git -C CLONE show BASE:.ufo/evidence/round-53/verify-freeze.stdout` returns `FREEZE e62d99711a0d files=8 amendments=5`, only amendments 1–5, then `FREEZE_INTEGRITY: OK`.
- `git -C CLONE log --format='%H %s' -- CLONE/.ufo/evidence/round-53/verify-freeze.stdout` returns its sole introduction at `7d8aaac676cbcb6379f57659e7c3c4c12150a815`, not a refresh after the final amendment.
- `LOG.md:2468-2469` still says freeze `e62d9971`, amendments `1–5`. Receipts: `r535-original.txt`, `r535-freeze-history.txt`, `tool-observations.txt`.

### R53.7 — open: trace pins do not establish ledger pins

- `LOG.md:2491-2492` retains the round-53 assertion `three read revisions, inputs pinned at C7`.
- Ran `git -C CLONE show BASE:.ufo/evidence/round-21/coldread/ledger.json`, selected entries whose traces name `rekey-r53-`, and compared each recorded input SHA256 with `SHA256(git -C CLONE show 8f474419:PATH)`.
- Sweep output: `entries=37 input_occurrences=11771 C7_mismatches=17`. This includes historical entries; it is **not** presented as a reproduction of the routed item's narrower 747-input denominator. Full mismatch details are in `r537-ledger-pins.txt`.
- Concrete counterexample: heading `## Context gate classification and explicit exit classes — round 15`, read_rev `a41195dfc13a73958e4c5228ec196b28d03ded03`, input `SKILL.md` records `4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d`; C7 is `a0a34515a64713ddcd8663b06ce522ff17be1dcab4cf63533067215f6c4037ed`. The former equals the fix-pass-2 digest observed separately.
- Important negative control: the trace files themselves all match C7. Sweeps of the three original trace directories report respectively `28/11306/0`, `13/518/0`, `26/8800/0` (traces/input occurrences/mismatches). Those checks alone would incorrectly clear the ledger claim. Their outputs are preserved in the `r537-*` receipts. The original LOG claim is neither restated nor made universally true by those trace files.

## Resolved primary behavior

### R53.6 — fixed, resolving commit `99c3bc88d704566197783f66b211ee0a830e0330`

- `git -C CLONE show 59c38109bf119d0e9d4f878644a82babc937bc1e --` the four affected absolute tool paths shows introduction of `ScratchRootUnusable` and CLI handlers. Located base excerpts: `bash-witness-study.py:1786-1790`, `env-diff.py:231-236`, `evidence-disposition.py:3228-3233`, and the pin-disposition selftest handler in the introduction diff.
- `git -C CLONE show 99c3bc88d704566197783f66b211ee0a830e0330 -- CLONE/tools/env-diff.py` adds the remaining ordinary-run handler, now `env-diff.py:263-265`:
  ```python
  except ScratchRootUnusable as exc:
      print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
      return 2
  ```
- `git -C CLONE merge-base --is-ancestor 99c3bc88d704566197783f66b211ee0a830e0330 BASE` exits **0**. Introduction, completion diff, and ancestry receipts: `r536-initial-fix.txt`, `r536-completion.txt`, `r536-ancestor.txt`.
- Executed four actual CLI refusal probes, concurrently, with `TMPDIR=/fast/scratch/hyaku/tameshi-r58/T58W1Panel05/DOES_NOT_EXIST` and `PYTHONDONTWRITEBYTECODE=1`: `python3 CLONE/tools/bash-witness-study.py selftest`, and `python3 CLONE/tools/{env-diff,evidence-disposition,pin-disposition}.py --selftest`. Each exited **2**, stdout empty, stderr named `could-not-evaluate` and the unusable TMPDIR, without a traceback. Exact commands/output: `r536-probe-*.txt`; the environment assignment is supplied by `capture.py`.
- Judgment concerns the primary exit-class defect. The explicitly secondary context-capture docstring nit still exists at `tools/context-capture.py:27` (`tempfile.mkdtemp(dir=tempfile.gettempdir())`); it is disclosed rather than claimed repaired.

## Residual risk and verification gaps

- No LSP device is mounted: `functions.read("xd://lsp")` returned `No such tool`. No references/definition/diagnostics claims are made; searches are literal evidence only.
- The executed probes cover precisely nonexistent-but-set TMPDIR refusals, not full successful selftests or every filesystem failure mode. The ordinary env-diff path was inspected in its introduction diff, not separately executed with a full surface contract.
- This is an independent base-tree panel, not an admission, runtime saturation claim, or C1/C2/no-harm counter certification. No forbidden round-57 wave files, panel files, other round-58 seats, or candidate routed ledger were opened. Later-round lesson status assertions were not used as verdict evidence.
- Tools installed or upgraded: **none**.
- Scratch cleanup executed: `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1Panel05 && test ! -e /fast/scratch/hyaku/tameshi-r58/T58W1Panel05 && printf 'scratch_removed=true\n'` → exit **0**, `scratch_removed=true`. Scratch was deleted before delivery.

Self-evaluation: accuracy 4 (secondary docstring nit remains explicitly separate from the fixed primary behavior); completeness 4 (five assigned verdicts, but original 747-input denominator not reconstructed); clarity 4 (receipts carry long commands); actionability 5 (exact remaining records and resolving commit named); conciseness 4 (trace/ledger distinction requires additional evidence). Overall 4.2/5. Highest-value improvement: preserve the primary/nit distinction and do not mistake trace-only checks for ledger validation; both are applied above.
