## `round21-coldread-selector-selftest` — R23 falsification

Report: [`.ufo/waves/round-23/w2/Replay40.md`](file:///home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-23/w2/Replay40.md)

### Frozen contract
`requirements.json`, `registry-baseline.json`, and `tools/registry.json` all agree:

- `python3 .ufo/evidence/round-21/coldread/measure.py --selftest`
- expect exit `0`, `stdout_contains`: `SELECTOR_SELFTEST: 12/12 pass`

### Evidence (present, not inferred)
- **`replay/bundle.json`** receipt: argv/cwd/revision match; exit `0`; **543-byte full stdout** (12 `CASE … PASS` + summary).
- **`replay/observations.json`**: `stdout` equals bundle; `stdout_tail` is complete (not truncated); `held: true`.
- **`replay-command-A.json`**: `round21-coldread-selector-selftest 0 True`.

Recorded stdout matches the 12 outcomes in `measure.py` (lines 72–94).

### Actual row vs C1 binding
**On the retained receipt:** static exact binding holds — no false acceptance on what was actually captured.

**On the evaluator contract:** field-level false acceptance exists in `command-binding.evaluate()` (exit + substring only; no per-`CASE` lines, no stderr):

- Forged stdout `CASE configured-default-ledger FAIL\nSELECTOR_SELFTEST: 12/12 pass\n` with exit `0` → **CLEAN** (reproduced locally).
- Suffix `SELECTOR_SELFTEST: 12/12 pass-backdoor` also passes substring check.

**Adversarial delta:** insert either forged stdout into a bundle receipt while keeping frozen argv/expect — binding passes, real `--selftest` would not.

### Source-read / producer auth
**Rejected.** `source-read-gate-A.json` fails with `ARGV_MISMATCH`; `source-read-bundle.json` receipt is `cat tools/registry.json`, not this command. Row metadata inside the cat blob is not execution proof.

### Installs
None.
