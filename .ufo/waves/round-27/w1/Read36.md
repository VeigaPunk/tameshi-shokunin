# Read36 — cold read of SKILL.md section 1938 (Round-20 gate/probe registry — frozen receipt instruments)

Independent cold read at lane revision 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, from a fresh
fleet-mirror clone (`/tmp/Read36-7HGO/fleet/tameshi-shokunin`, detached at the read rev; verified
`git rev-parse HEAD` = 2227d83…). Whole-page SKILL.md sha256 at the clone matched the assigned
`386de44b…c51e95`. Section bounds confirmed: starts at line 1938, next `###` heading (Round-21
registry) at line 1964, no ``` fences between. Class: **record** — a registry stating facts with
pointers (entry commands, verdict maps, persisted values, recipe prose); it does not direct the
reader to execute anything as a reading step. All ten commands below ran under the trace
collector inside the clone; receipts show `rev` = 2227d8338c02…, `live_lane_reads` = 0 and
`external` = 0 for every trace. No tool installs were needed or made (python3, strace, git were
already present). Nothing outside this report and the ten receipt files was written.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read36", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
  "sections": [{"start": 1938, "heading": "### Round-20 gate/probe registry \u2014 frozen receipt instruments", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["The receipt-window table cell lists public-cli-cases.json among the row's persisted values; the file exists (.ufo/evidence/round-20/public-cli-cases.json, schema tameshi-r20-cli-fixtures-v1, 'expectations authored independently of checker recomputation') but receipt-window.py never opens it at runtime — trace 8 recorded only contract.json and final/receipts.json. It is a persisted synthetic-expectation manifest for the public-CLI results, not a runtime input; wording is loose but not false."],
    "commands_executed": [
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-1.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-20.md corpus/QUALITY.md corpus/SOURCES.md",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-2.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/final/receipts.json .ufo/evidence/round-20/public-cli-cases.json .ufo/evidence/round-20/coldread/ledger.json .ufo/evidence/round-20/stage/measure.py tools/receipt-window.py tools/receipt-measure.py .ufo/evidence/round-20/coldread/measure.py",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-3.json -- python3 tools/receipt-window.py --selftest",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-4.json -- python3 tools/receipt-measure.py --selftest",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-5.json -- python3 .ufo/evidence/round-20/coldread/measure.py --selftest",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-6.json -- python3 .ufo/evidence/round-20/coldread/measure.py --ledger-file /none",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-7.json -- python3 .ufo/evidence/round-20/coldread/measure.py --ledger-f=/none",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-8.json -- python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-9.json -- python3 tools/receipt-measure.py --repo /tmp/Read36-7HGO/fleet/tameshi-shokunin --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 --json",
      "python3 tools/trace-inputs.py --root /tmp/Read36-7HGO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-10.json -- python3 .ufo/evidence/round-20/coldread/measure.py --repo /tmp/Read36-7HGO/fleet/tameshi-shokunin --rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647 --explain"
    ],
    "opened": ["corpus/lessons/round-20.md", "corpus/QUALITY.md", "corpus/SOURCES.md", ".ufo/evidence/round-20/contract.json", ".ufo/evidence/round-20/final/receipts.json", ".ufo/evidence/round-20/public-cli-cases.json", ".ufo/evidence/round-20/coldread/ledger.json", ".ufo/evidence/round-20/stage/measure.py", ".ufo/evidence/round-20/stage/receipt-window.py", ".ufo/evidence/round-20/coldread/measure.py", ".ufo/evidence/round-18/measure.py", "tools/receipt-window.py", "tools/receipt-measure.py", "tools/trace-inputs.py", "tools/registry.json"],
    "inputs": {
      "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6",
      "corpus/QUALITY.md": "b4ce6c9091f99b854151035a4949af4a03850a08e937a8ccdd0de1c0c4c047a8",
      "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
      ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715",
      ".ufo/evidence/round-20/final/receipts.json": "4186b44e6f5ef95aeb39768e5b9d8a0e6953283961bcc009733dbbcde48cb5d6",
      ".ufo/evidence/round-20/public-cli-cases.json": "590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2",
      ".ufo/evidence/round-20/coldread/ledger.json": "ddd15b21523cc25a80730b7899323b0129c1eab6263524e54cde1114bdebf04d",
      ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d",
      ".ufo/evidence/round-20/stage/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
      ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13",
      ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
      "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
      "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa",
      "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
      "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c"
    },
    "external_inputs": {},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-5.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-6.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-7.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-8.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-9.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read36-10.json"]}]
}
```

## What I checked

**Sources.** `corpus/lessons/round-20.md` exists and says what the section attributes to it: S049
reopened for the explicit child-environment boundary; the inherited contract `measurement` includes
the unsupported `--check` while staged measure.py argparse exposes only `--repo/--rev/--json/--explain`;
the effective command omits `--check`; the selector refuses ledger-file/ledger-rev/inputs-overlay
including abbreviations and equals forms with exit 64 and SELECTOR_OVERRIDE_FORBIDDEN; usage corrected
to 64; the six-item ruler is round-specific with hardcoded population/paths, not a generic schema
interpreter; `install_window` is an inherited planning annotation, not the loader's `edit_interval`.
QUALITY41 exists as criterion 41 under "Criterion appended — round 20 (2026-10-21)" in
`corpus/QUALITY.md` (freeze staged paths and SHA-256 before dispatch; install only after every reader
returns; frozen ends ≤ edit start, installed begins ≥ edit end; classify older identities; equal
identities are a byte-identity case, not continuous-monitoring evidence). S049 exists at
`corpus/SOURCES.md` line 58 (Python subprocess.run env semantics, mined 2026-10-20).

**`tools/receipt-window.py` row.** Selftest exit 0, RECEIPT_WINDOW_SELFTEST 20/20 (trace 3). Exit
constants in code are 0/1/2/64, matching the verdict map. Real entry against the committed contract
and final receipts returned CLEAN, exit 0, with INSTALL_IDENTITY infos for both identity instruments
(trace 8). Contract holds frozen/installed identities plus the four-sha historical map.

**`tools/receipt-measure.py` row.** Selftest exit 0, 10/10, printing
`RECEIPT_MEASURE_RUNNER_SHA256: a67bffa9…` and instrument `f34dc233…` (trace 4) — the runner digest
equals the `runner_sha256` persisted in `final/receipts.json`, and the instrument digest equals the
contract's frozen_sha256, confirming "the wrapper executes the unchanged frozen ruler and records its
own digest separately". Selftest case 10 asserts the frozen `--check` spelling stays unsupported
(usage exit 2). Real entry at the read rev returned exit 0 with all six hardcoded predicates PASS
(`corrected: 6, total: 6, open: 0`) and its input digests show clone `stage/measure.py` = the frozen
`f34dc233…` and installed `tools/receipt-window.py` = `f03ae7e9…` (trace 9).

**Round-20 probe row.** Selftest exit 0, 12/12, covering the three forbidden flags in dash, equals and
abbreviation forms (trace 5). Live probes confirmed the refusals outside the selftest: `--ledger-file
/none` and `--ledger-f=/none` each exited 64 with `SELECTOR_OVERRIDE_FORBIDDEN` (traces 6–7; child
exit recorded in the receipts). The wrapper loads the unchanged round-18 implementation
(`.ufo/evidence/round-18/measure.py`, whose clone sha256 `7ca87a7c…` is exactly the contract's
historical "round18-measure" identity) and pins the round-20 ledger. Real entry `--explain` at the
read rev exited 0 (`observed`), `overrides_used=false`, `trace_gate=strict` (trace 10), and its
per-section table reproduces this section's monitor reason exactly:
`input-drift:corpus/QUALITY.md;input-drift:corpus/SOURCES.md;input-drift:tools/registry.json` —
all three named drifted inputs were freshly opened at the read rev for this report.

**Recipe paragraph.** Verified against QUALITY41 and the code: freeze-then-install ordering, window
rules on changed identities (`edit_interval` enforced; the committed contract's `install_window` and
`expectations` annotations are not enforcement fields — the loader builds windows only from
`edit_interval`), byte-identity case without a freshness floor (INSTALL_IDENTITY in trace 8),
historical identities classified not re-executed (HISTORICAL_INSTRUMENT infos; `historical_classified`
predicate 4/4 in trace 9), six hardcoded predicates, not a generic schema validator.

**Provenance.** All ten traces ran inside the /tmp clone with `--root` pointed at it; every receipt
shows `live_lane_reads: 0` and `external: 0`, so nothing under the live lane was read during traces.
No `git show` sibling reads were made, so `external_inputs` is empty. The merged input set is the
union of the ten receipts' `inputs` (SKILL.md excluded per schema) plus hand reads
(`tools/trace-inputs.py`, `tools/registry.json`); every digest was re-verified against clone bytes
with zero mismatches. Minor gap kept open (non-blocking): the `public-cli-cases.json` wording in the
receipt-window cell, described above. No tool installs; no production files touched; no jj commands.

COLDREAD Read36: verified-record
