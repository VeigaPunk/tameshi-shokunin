# T56W3MutGate2 — gate mutants at PIN

Seat: T56W3MutGate2 · Milestone: gate mutants at PIN · Judged on: operability
Subject: `tools/receipt-revision-gate.py` at PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd`
(blob sha256 `c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`, equal to the
`freeze.json` pin). Lane files were not edited; every mutant lives in scratch.

## Method

- Scratch: `S=$HYAKU_SCRATCH/tameshi-r56/T56W3MutGate2`; `git clone --shared` of the lane, then
  `git -C "$S/pin" checkout --detach 2f5512a8…`. `rev-parse --show-toplevel` = clone dir.
- Each mutant is one exact-string replacement of the PIN gate (the script asserted
  `needle-count == 1` before writing). The selftest's fixture uses `Path(__file__)` as the gate,
  so each mutant runs its own selftest against itself. `TMPDIR` pointed into scratch.
- Command per mutant: `python3 $S/mut/<M>.py --selftest` (env `TMPDIR=$S/tmp`).
- Baseline on unmodified PIN gate: `GATE_SELFTEST: 19/19 pass`, rc 0.

## Results: 8/8 KILLED

Every mutant exits 1 with `GATE_SELFTEST: 18/19 pass`, exactly one `CASE … FAIL`, and no traceback.

| # | Mutant (single edit at PIN) | needle replaced | Killing selftest case | Fixture receipt (role) |
|---|---|---|---|---|
| M1 | drop `RECEIPT_REV_ABSENT` | `codes.append('RECEIPT_REV_ABSENT')` → `pass` | `absent-refused` | `VERDICT: no revision named` (positive) |
| M2 | `drifted_paths` returns `[]` | final `return [p … ] + gone` → `return []` | `content-drift-refused` | `VERDICT: rev=<c0> C1_X_PASS=true` (positive), `--paths` surface.txt+moved.txt, certified c1 |
| M3 | `is_ancestor` always true | body → `return True` | `control-not-ancestor-refused` | `CTL A rev=<side>` (control), certified c2; side branches from c0 |
| M4 | skip digest check | `if want != got:` → `if False:` | `digest-mismatch-refused` | `VERDICT: rev=<c2> C1_X_PASS=true` (verdict) with sidecar `000…0` |
| M5 | allow multiple revs in positive | `if len(revs) > 1:` → `if False:` | `ambiguous-refused` | `A rev=<c0>` / `B rev=<c1>` (positive), `--paths` surface+moved |
| M6 | skip required-line check | `if regex is not None and …:` → `if False:` | `required-line-refused` | `VERDICT: rev=<c2>` (verdict:`C1_X_PASS=`) |
| M7 | empty file treated as present | `if not data.strip():` → `if False:` | `empty-refused` | `\n` (positive) |
| M8 | drop `RECEIPT_CONTROL_NOT_ANCESTOR` | `codes.append('RECEIPT_CONTROL_NOT_ANCESTOR')` → `pass` | `control-not-ancestor-refused` | `CTL A rev=<side>` (control), certified c2 |

Mutant file sha256 prefixes: M1 `187b705b8cde`, M2 `384b6089da36`, M3 `38594a200dd7`, M4 `58bf3b3480fd`,
M5 `b8de83fdabde`, M6 `0f411c44f3df`, M7 `8f976274b5c1`, M8 `bec76182da11`.

Notes on the kills:
- M3 and M8 are both killed by `control-not-ancestor-refused`; the two mutants fail that case in
  different ways (M3 accepts everything; M8 never emits the code).
- The `codes-closed` case (`len(CODES) == 11`) is the guard for removing a code from the `CODES`
  tuple. That variant was not run as a mutant (outside the eight assigned).

## Round's own receipts at PIN: NOT PASS (receipts not yet committed)

Command (run in the PIN clone, `--paths` is the frozen surface list the deciding run uses):

```
python3 tools/receipt-revision-gate.py --lane <PIN-clone> \
  --certified 2f5512a8ab0771fb2eee463ec16db359174f5edd \
  --paths .ufo/evidence/round-56/control/frozen-surface.paths \
  --receipt .ufo/evidence/round-56/control/controls-a.stdout:control \
  --receipt .ufo/evidence/round-56/control/controls-b.stdout:positive
```

Output:

```
GATE REFUSED .ufo/evidence/round-56/control/controls-a.stdout role=control revs=none code=RECEIPT_MISSING path=.ufo/evidence/round-56/control/controls-a.stdout
GATE REFUSED .ufo/evidence/round-56/control/controls-b.stdout role=positive revs=none code=RECEIPT_MISSING path=.ufo/evidence/round-56/control/controls-b.stdout
GATE: receipts=2 ok=0 refused=2 codes=RECEIPT_MISSING verdict=REFUSED
```
exit 3.

Cause: at PIN `.ufo/evidence/round-56/control/` holds only `frozen-surface.paths`. The `controls-a/b.stdout`
files are not committed. I did not create them. The sibling executors' working-tree copies
(`.ufo/waves/round-56/w3/T56W3ExecControlsA-receipts/`, `…ControlsB-receipts/`) contain only a header line
and are uncommitted, so they are not admissible receipts.

Gate-run check on the real round-54 receipts, for contrast (same certified PIN):

```
GATE REFUSED .ufo/evidence/round-54/control/controls-a.stdout role=control revs=042655edec78,88afa9415454,d33053f7552d,de700f6ccc7c code=RECEIPT_REV_UNRESOLVABLE rev=de700f6ccc7c
GATE REFUSED .ufo/evidence/round-54/control/controls-b.stdout role=positive revs=077d431e6996,7df0e0426c98 code=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98
GATE: receipts=2 ok=0 refused=2 codes=RECEIPT_REV_UNRESOLVABLE verdict=REFUSED
```
exit 3. These refusals come from clone-local SHAs that the lane cannot resolve, not from a mismatch with PIN.

## Next step for the deciding run

Once controls run at the bootstrap PIN and the actual `controls-a.stdout`, `controls-b.stdout` (and their
`.sha256` siblings) are committed at a PIN, re-run the exact command above from a clean clone at that PIN.
`verdict=PASS` is only admissible if the receipts are committed at that revision and the lines are unedited.
Until then this item's verdict is `REFUSED (RECEIPT_MISSING)`.

## Tools

None installed. Only the host `python3` (3.14.8) and `git` were used.

## Mutations applied to the lane

None. Mutants and clone live under `$HYAKU_SCRATCH/tameshi-r56/T56W3MutGate2`, removed on exit.
