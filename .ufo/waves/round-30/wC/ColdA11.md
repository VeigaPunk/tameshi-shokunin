# ColdA11 — cold read, round 30 wave C

Seat: ColdA11. Revision: bb681566b18211adf8ae9c28df91e17678e3f545 (clone at /tmp/ColdA11-GnKF/fleet/tameshi-shokunin, detached HEAD, GIT_* unset). SKILL.md sha256 verified c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA11", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
  "sections": [{"start": 2132, "heading": "### Round-26 gate/probe registry — report interop", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["The live `--check` replay (registry row mte-interop-check, expected PASS legs_conforming=9/9, registry timeout 900 s) was not re-executed: it runs tools/mutate-and-run.sh --regression --keep against live sibling object stores and exceeds the 6-minute bound. The 9/9 row claim was verified statically against tools/registry.json rows and the tool's LEG_TABLE only, not by observation."],
    "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/registry.json tools/mte-interop.py corpus/knowledge/mte-report-interop.md", "uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest", "python3 tools/mte-interop.py --check --selftest", "sed -n 620,640p tools/mutate-and-run.sh"],
    "opened": ["tools/registry.json", "tools/mte-interop.py", "corpus/knowledge/mte-report-interop.md", "tools/mutate-and-run.sh"],
    "inputs": {"tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c", "tools/mte-interop.py": "193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4", "corpus/knowledge/mte-report-interop.md": "6e10d010cd3a256e7fe51c9a202263d7a773d74324da2def54c5302de3e827f9", "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9", "tools/vendor/mutation-testing-metrics-3.9.0.tgz": "ce17812bf718cf2415fb429b2774c7ad3e1e0ca57234e7f8cfa0d794f38ec548", "tools/vendor/mutation-testing-report-schema-3.9.0.tgz": "adb78e132e8a0ff17849f842007848eb7a3796f7379e15d8a46a2311dc467280"}, "external_inputs": {}, "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA11-31-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA11-31-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA11-31-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA11-31-4.json"]}]}
```

What I checked (section 31, SKILL.md 2132–2136, the `tools/mte-interop.py` registry row):

- Class: `record` — the row states facts about a gate/selftest and its exit contract, with pointers to the tool, the registry, and the runner's tables.
- Registry rows `mte-interop-selftest` and `mte-interop-check` exist in `tools/registry.json` (rows 54–55) with argv matching the row's named commands (`uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py ...`) and expectations `MTE_SELFTEST: 17/17 pass` / `MTE_INTEROP: PASS legs_conforming=9/9` — the "(17/17)" and "(9/9)" claims check out.
- Selftest executed under the collector: `MTE_SELFTEST: 17/17 pass`, exit 0, in about 40 s (node v24.21.0, uv 0.13.0, jsonschema 4.25.1 via uv). Consistent with the row's "0 PASS".
- Usage path observed: mutually exclusive `--check --selftest` → usage printed to stderr, child exit 64 (receipt exit field). Consistent with "64 usage".
- Exit-2 SETUP claim verified statically: `check()` and `selftest()` return 2 on `Setup`, missing `jsonschema` import, missing node, vendored integrity/unsafe-tar failures, regression non-zero, and leg-set mismatch; the docstring enumerates the same cases. Not exercised live (would need a sabotaged environment).
- "Nine ledger legs" claim: `LEG_TABLE` in `tools/mte-interop.py` has exactly nine keys, and all nine names match `TABLE_*` blocks committed in `tools/mutate-and-run.sh` lines 623–631 (js-kimi-census→TABLE_JS … js-cite-check→TABLE_CITECHECK). The SETUP guard requires the leg set to equal these nine.
- "Reads the runner's committed tables": `recorded_verdicts()` reads `(ROOT/'tools/mutate-and-run.sh')` for TABLE_* lines; `TABLE` regex parses `REGRESSION_TABLE` lines from the regression stdout. Confirmed.
- "Writes only its own scratch and `--emit DIR`": scratch is `tempfile.mkdtemp` (selftest `tameshi-mte-selftest-`, check `tameshi-mte-regression-`, staged fleet `tameshi-mte-fleet-`), removed on exit; `--emit` writes `<leg>.mte.json`, `<leg>.spec`, `official-metrics.json`. One nuance: with `--workdir` it writes `regression.stdout` into the given workdir — that is the tool's own workdir argument, so the claim as written holds.
- "Replays live sibling object stores, not hermetic": `run_regression()` symlinks each sibling dir under `--fleet-root` into a staged private fleet and runs the copied runner against them. Confirmed by code read; not replayed.
- `corpus/knowledge/mte-report-interop.md` corroborates: verified-at names tool sha256 193ea6e3… (identical to the pinned bytes at bb681566), selftest 17/17 and check 9/9 at a08e85c; its stale "eight legs" wording is corrected by its own "Round 26 append — nine legs" section, so no defect carried into this row.

No installs were needed (node, uv, python3 already present). Verdict `gap-minor` rather than `verified-record` solely because the live 9/9 `--check` replay was not observed this read.

COLDREAD ColdA11: gap-minor
