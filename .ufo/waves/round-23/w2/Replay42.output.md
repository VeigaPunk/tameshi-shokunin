## Axes

Command identity, outcome binding, evidence presence (full stdout vs tail/source-read), gate semantics (`command-binding`), provenance (no source-read / producer auth as execution).

## Verdict

**Static exact binding confirmed** for `wave-accounting-selftest`: `requirements.json`, `registry-baseline.json`, and `496d212:tools/registry.json` agree on argv and expect; replay receipt matches on argv, cwd, revision, exit 0, and all three `stdout_contains` needles.

**Execution evidence is present (not inferred):** `replay/bundle.json` and `replay/observations.json` both retain **1112-byte identical full stdout** (8 + 16 case lines, summaries, `FINDING: SELFTEST_PASS`); `stdout === stdout_tail`. `replay-command-A.json` records `wave-accounting-selftest 0 True`; `replay-gate-A.json` exit 0 with empty `finding_ids`.

**No field-level false acceptance** on the retained replay row under `command-binding.evaluate()`.

**Concrete adversarial delta:** A tampered receipt with **91 bytes** of forged stdout (only the three registry needles + exit 0, correct argv/cwd/revision) still passes `command-binding.py` with no `ACCOUNTING_CASE` lines — by design (docstring: no producer authenticity). Observed replay stdout is stronger than that minimum.

**Rejected:** `source-read-gate-A.json` exit 1 `ARGV_MISMATCH`; `actual-source-read.json` is registry text, not `--selftest` subprocess output.

**Tooling installs:** none.

Report: [.ufo/waves/round-23/w2/Replay42.md](file:///home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-23/w2/Replay42.md)
