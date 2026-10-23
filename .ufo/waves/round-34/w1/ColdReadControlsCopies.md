# ColdReadControlsCopies — round-34 w1 cold re-read of the controls mint

Seat scope (r33 closure route): `.ufo/evidence/round-34/controls/` — do the four control
tool bytes equal the r33 seat scratch originals (`/fast/scratch/hyaku/tameshi-r33-seats/Ctl*/ctl.py`),
do `mint.stdout`/`mint.exit` record the mint at rev `6aaad5b3` with exit 0 and `all_false=True`,
and do the receipt's rows match `mint.stdout`. Lane verified at detached tip
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (fresh `--no-hardlinks` clone in
`/fast/scratch/hyaku/tameshi-r34-seats/ColdReadControlsCopies/lane`).

**Result: AGREE on every axis. No findings.** Beyond byte-compare, the rows were
independently re-derived by importing the amendment-6 counter as a module and re-scoring
all four controls against the public panel at the receipt's own seed — 104 fresh
sandboxed tool runs, exact match.

## 1. Pinned bytes verified before any run

```
git -C lane show 0b99d48...:tools/tally-audit-v2.py > tool.py   (exit 0)
git -C lane show 0b99d48...:tools/mutate-and-run.sh > pristine.sh (exit 0)
sha256sum tool.py pristine.sh
  7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py      == pin ✓
  a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh  == pin ✓
```

## 2. Control tool bytes == r33 seat scratch originals

`sha256sum` on both sides, lane dir vs seat scratch (both commands exit 0):

| tool | lane `.ufo/evidence/round-34/controls/` | r33 seat `/fast/scratch/hyaku/tameshi-r33-seats/<Seat>/ctl.py` | match |
|---|---|---|---|
| CtlAlwaysFail.py | `101dd5b625119df69c26b86fbd212e176d1502381ba9a0dd1f566748959f9509` | `101dd5b625119df69c26b86fbd212e176d1502381ba9a0dd1f566748959f9509` | ✓ |
| CtlAlwaysPass.py | `ed13d65e58c7662c4e238f53303b7aa31159a2316cace560dd3a65adb7c06f09` | `ed13d65e58c7662c4e238f53303b7aa31159a2316cace560dd3a65adb7c06f09` | ✓ |
| CtlDoNothing.py | `7587926d41161466abb244c775d4f20f3484376011c164a6ce697bacc1536d29` | `7587926d41161466abb244c775d4f20f3484376011c164a6ce697bacc1536d29` | ✓ |
| CtlShaOnly.py | `4bc160675c044904dc9069eeee93392f969d4be807ca48a41269b653b4e04630` | `4bc160675c044904dc9069eeee93392f969d4be807ca48a41269b653b4e04630` | ✓ |

Commands: `sha256sum lane/.ufo/evidence/round-34/controls/*.py` and
`sha256sum /fast/scratch/hyaku/tameshi-r33-seats/CtlAlways{Fail,Pass}/ctl.py .../{CtlDoNothing,CtlShaOnly}/ctl.py`.

## 3. Mint records: rev 6aaad5b3, exit 0, all_false=True

- `mint.exit` = `0` (2 bytes, `cat` output `0`).
- `mint.stderr` = 0 bytes (`wc -c` = 0).
- `mint.stdout` verbatim:

  ```
  C1_R33_CONTROLS: controls=4 all_false=True receipt=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-33/c1/controls-receipt.json
    CtlDoNothing.py kill=0/18 accept=8/8 predicate_pass=False
    CtlAlwaysPass.py kill=0/18 accept=8/8 predicate_pass=False
    CtlAlwaysFail.py kill=18/18 accept=0/8 predicate_pass=False
    CtlShaOnly.py kill=18/18 accept=1/8 predicate_pass=False
  ```

- "Minted at the amended rev": the adding commit is
  `git log -- .ufo/evidence/round-34/controls/` →
  `9dd3174c6daaa55ff5bee32878b700ee3bc731b7` — subject:
  *"round-34: controls receipt minted at the amended rev 6aaad5b3 (receipt-attestation rule;
  four seat controls all predicate_pass=false)"*. The same commit adds
  `.ufo/evidence/round-33/c1/controls-receipt.json`.
- Rev chain confirmed: `git merge-base --is-ancestor 6aaad5b3... 0b99d48...` → exit 0;
  `git show 6aaad5b3...:.ufo/evidence/round-33/c1/c1-measure.py | sha256sum` →
  `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`, identical to the
  receipt's `counter_sha256` and to the tip's counter bytes (`sha256sum` of the checkout,
  exit 0) — the amendment-6 counter is unchanged from the mint rev through the tip.
- Receipt at mint commit == receipt at tip: `git show 9dd3174c:…controls-receipt.json` and
  `git show 0b99d48:…` both sha256 `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa`;
  all four control `.py`, `mint.stdout` (`79523d86…`), `mint.exit` (`9a271f2a…`) likewise SAME
  between `9dd3174c` and tip.

## 4. Receipt rows match mint.stdout — and independently re-derive

`controls-receipt.json` rows: CtlDoNothing `kill=0/18 accept=8/8 predicate_pass=false`;
CtlAlwaysPass `0/18`, `8/8`, false; CtlAlwaysFail `18/18`, `0/8`, false; CtlShaOnly `18/18`,
`1/8`, false; `all_false: true`, `seed: a7acbc0ec97d2710`, `counter_sha256: f6b8868c…a07f28c`,
`runner_sha256: a7d3f2dd…2eb9`. Textual match against `mint.stdout` row-for-row: exact.

**Independent re-derivation (stronger than a diff):**
`/fast/scratch/hyaku/tameshi-r34-seats/ColdReadControlsCopies/rederive.py` imports the
tip's counter as a module (`importlib.util.spec_from_file_location`), calls only the
permitted functions — `mod.show`, `mod.public_panel(pristine, 'a7acbc0ec97d2710')`
(26 copies: 18 kill / 8 accept, asserted), and `mod.score_tool` on scratch copies of the
four controls — under `work=/fast/scratch/hyaku/tameshi-r34-seats/ColdReadControlsCopies/work`.
`python3 rederive.py` → exit 0, stderr empty, `ROWS_MATCH=True`, `all_false_rederived=true`,
every re-derived row byte-identical to the receipt's (verbatim JSON in `rederive.out`).
The mint's numbers are reproducible today, not just self-consistent.

## 5. Corroboration + residual caveats

- Seat-side receipts corroborate the rows independently: CtlDoNothing `receipt-amended.json`
  (0/18, 8/8, false), CtlAlwaysFail `receipt-scored.json` (18/18, 0/8, false),
  CtlAlwaysPass `receipt.json` (0/18, 8/8, false), CtlShaOnly `receipt-amended-rev.json`
  (18/18, 1/8, false). All show `runner_sha256` pinned correctly; their `counter_sha256`
  values are pre-amendment-6 (`7ff776df…`, `edd8fbb0…`) with different seeds — earlier mints,
  not the committed one; rows agree anyway.
- Caveats: byte-compare is as-observed (nothing proves the seat files weren't mutated
  between mint and now — the three-way agreement mint-commit / tip / seat is the evidence);
  `--write-controls` itself was not re-invoked (not in the permitted import list), so
  re-derivation covers `public_panel`+`score_tool`, not the writer; receipt `seed` is the
  receipt's own — re-derivation proves row truth at that seed, not panel entropy.
- No tool installs (nothing needed beyond git/python3/bwrap, all already present).
- Lane never written; all writes confined to `/fast/scratch/hyaku/tameshi-r34-seats/ColdReadControlsCopies/`
  (clone, tool.py, pristine.sh, controls/, work/, rederive.*) and this report. No `git`/`jj`
  write commands run; no default-mode counter invocation.

**Verdict: the r34 controls mint is faithful — bytes, mint record, receipt rows, and a
fresh re-derivation all agree. Zero findings.**
