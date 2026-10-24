# ResMutation — residual falsification of the round-37 mutation receipts (attempt 3)

Seat: `L1-tameshi-r37-attempt3.ResMutation` (residual critic, read-only). Date: 2026-10-24.
Target: committed receipts at `.ufo/evidence/round-37/mutation/` (commit 583909a, lane tip ba3c35f).
Method: rebuilt both mutants **independently** from committed tool bytes in a fresh /tmp scratch git
lane, re-ran the committed frozen predicate, and re-ran wave-1's own unmodified extended probe.
No lane bytes outside this report were written; `.ufo/state` untouched; no git/jj writes on the lane.

## Verdict

**The receipts survive falsification.** Every claimed kill/survive result, every digest, and the
extended probe's pristine 0/14 reproduced exactly, using only committed bytes plus my own rebuilds.
One MINOR provenance finding (uncommitted probe-runner variant), no BLOCKER/MAJOR.

## My scratch lane and revs

- Scratch: `/tmp/resmut-r37-a3/lane` (fresh `git init -b master`, three commits, fixed identity/dates).
- Pristine copied from committed `tools/tally-audit-v3.py`; sha256 verified
  `da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede` (= counter-pin.json, digests.txt).
- Mutants built by unique-anchor byte surgery on the committed bytes (anchor count 1 each):
  - M1 branch-removal: deleted the entire 8-line `if quote == "ansi-c":` state branch
    (pristine `tools/tally-audit-v3.py:172-179`). Rebuilt sha256
    `835a0673a8ea71c5db5b6c85d82b18eb689b4123649106ec65079d96502be73d` = `digests.txt` mutant digest.
  - M2 parity-lookbehind: pair-skip → single-char lookbehind per wave-1 §4 diff
    (`if c == "'" and (i == 0 or text[i - 1] != '\\')`). Rebuilt sha256
    `1e6e7c98b79201809db6272f88a61dde4514653d4b6aa5f51d2ec83e3bef7be8` = receipt sha, and
    **byte-identical** (`==`) to wave-1's retired copy `/tmp/r37-ansi-probe/mutant_lookbehind.py.frozen`.
- My commits: pristine `6ba4ba05a98ab668cea70236fec3f373c815b2f9`, M1 `049d34af028fa8dc8a63902443e005ab9db542ee`,
  M2 `f6a05c60d948efa7f156282548e639064c77e40d`. (Receipt lane revs a0a6bfd/87115382/36a8c475 are
  per-lane commit ids and legitimately differ; blob digests are the identity and all match.)

## Kill confirmed — M1 under the frozen predicate

`python3 .ufo/evidence/round-37/code-view/measure.py --lane /tmp/resmut-r37-a3/lane --rev 049d34af…`:
both cases FAIL, `ansi_trailing_comment=0/1 ansi_literal_hash=0/1`, `C2_R37_PASS=false`, **exit 1**.
Rerun stdout is byte-identical to committed `branch-removal.stdout` modulo the `rev=` field
(machine-diffed). Same for the controls:

| rev | exit | C2_R37_PASS | receipt stdout ≡ rerun (mod rev) |
|---|---|---|---|
| pristine `6ba4ba05…` | 0 | true | yes (`pristine-frozen-predicate.stdout`) |
| M1 `049d34af…` | 1 | false | yes (`branch-removal.stdout`, incl. expected/actual reprs) |
| M2 `f6a05c60…` | 0 | true | yes (`parity-frozen-predicate.stdout`) |

So the branch-removal mutant is genuinely **killed** by the frozen two-case predicate and the
pristine control **passes** — harness fidelity holds on my independent lane.

## Survive + extended-probe kill confirmed — M2

Frozen predicate: `C2_R37_PASS=true`, exit 0 (survives), as receipted. Extended probe: wave-1's
`/tmp/r37-ansi-probe/probe.py` run **unmodified** against my rebuilt copies (bash
5.3.20(1)-release, same ground-truth lexer as wave-1; every fixture's bash stdout re-verified live,
`bash_ground_truth_failures=0` on all runs):

- `probe.py pristine.py` → `divergences=0 … fixtures=14`, **exit 0** — pristine 0/14 verified.
- `probe.py m2_lookbehind.py` → **divergences=4/14, exit 1**, exactly the even-parity fixtures
  `frozen_1_analogue_2bs`, `F2_even_2bs_quote_comment`, `F6_even_4bs_quote_comment`,
  `F10_even_2bs_nextline_comment`; `got=` reprs match committed `parity-lookbehind.stdout`
  structurally and, where fixtures coincide byte-for-byte, exactly.
- Supplementary (not receipted): M1 on the extended probe diverges 12/14 — grossly broken, consistent
  with the frozen kill.

bash -n parity witnesses re-measured: 1bs rc=2, 2bs rc=0, 3bs rc=2, 4bs rc=0 (odd open / even closed),
matching the receipt preamble and wave-1 §2.

## Provenance checks

- `measure.py`, all receipts, `digests.txt`, `scratch-revs.txt`, `scratch-dir.txt` are git-tracked,
  committed at 583909a; `git status` clean over `.ufo/evidence/round-37/`; `after.stdout` pins
  `tool_sha256=da8c1ef4…`.
- The retained receipt scratch lane `/tmp/r37-mut-receipt.8GXeDo/lane` still resolves:
  `a0a6bfd→da8c1ef4`, `87115382→835a0673`, `36a8c475→1e6e7c98` — exactly `scratch-revs.txt`/`digests.txt`.
- `counter-pin.json` tool pin matches the committed tool bytes.

## Findings

1. **MINOR — uncommitted runner behind `parity-lookbehind.stdout`.** The committed stdout was made by
   an adapted probe variant (fixture ids `frozen_1`/`frozen_1_2bs`/`F1_1bs_comment`…, frozen analogues
   reordered to the end, minimal `printf '%s'` fixture bodies, two `bash -n` witness preamble lines),
   not by wave-1's committed-to-/tmp `probe.py` (ids `frozen_1_escaped_quote_trailing_comment`,
   `F1_odd_1bs_quote_comment`…, order FROZEN then FIX). The generator of the committed stdout is in no
   branch — only wave-1's original survives in disposable /tmp. Substance is unaffected: I verified the
   14 fixture classes, worlds, and the 4/14 even-parity divergence set are equivalent under the
   original unmodified probe. Smallest fix: commit the receipt-generating runner beside its stdout
   (e.g. `.ufo/evidence/round-37/mutation/probe-receipt.py`) so the stdout receipts are regenerable
   from the lane alone.

## Residual risk / verification gaps

- 5+ backslash runs remain unprobed (wave-1's declared limit, unchanged); octal/hex ANSI-C escapes
  unprobed (cannot move close-parity per wave-1 §7).
- The out-of-bound word-start delimiter gap (`)`, `<`, `>` missing at pristine `:199`) is unchanged by
  these mutants and outside this receipt's scope; not re-adjudicated here.
- `rev=` fields in receipts are non-reproducible lane commit ids by design; identity rests on blob
  sha256, which I verified end-to-end.
