# Read11B — Round-20 gate/probe registry (SKILL.md lines 1938-1963 @ 9f3084bc)

```json
{"schema": "tameshi-coldread-report-v2", "seat": "TameshiR29.Read11B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1938, "heading": "### Round-20 gate/probe registry — frozen receipt instruments", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [], "commands_executed": [
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-1.json -- /bin/sh -c 'python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" \"$@\" > /tmp/TameshiR29.Read11B-dump.txt' sh corpus/lessons/round-20.md corpus/QUALITY.md corpus/SOURCES.md .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/final/receipts.json .ufo/evidence/round-20/public-cli-cases.json tools/registry.json .ufo/evidence/round-20/stage/measure.py .ufo/evidence/round-20/stage/receipt-window.py tools/receipt-window.py tools/receipt-measure.py .ufo/evidence/round-20/coldread/measure.py",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-2.json -- python3 tools/receipt-window.py --selftest",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-3.json -- python3 .ufo/evidence/round-20/coldread/measure.py --repo /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --ledger-file x.json",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-4.json -- /bin/sh -c 'python3 -c \"<consolidated verifier: receipt-window gate on committed contract+receipts, checks.json counting-entry scan, registry/stage field scans, dump greps>\"' (exact argv in receipt)",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-5.json -- /bin/sh -c 'timeout 280 python3 tools/receipt-measure.py --selftest 2>&1 | tail -6; echo \"rc=${PIPESTATUS[0]}\"'",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-6.json -- /bin/sh -c 'timeout 280 python3 tools/receipt-measure.py --repo /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --json 2>&1 | tail -20; echo \"rc=${PIPESTATUS[0]}\"'",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-7.json -- /bin/sh -c 'timeout 340 python3 .ufo/evidence/round-20/coldread/measure.py --selftest 2>&1 | tail -6; echo \"rc=${PIPESTATUS[0]}\"'",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-8.json -- /bin/sh -c 'timeout 100 python3 .ufo/evidence/round-20/coldread/measure.py --repo /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --explain 2>&1 | tail -15; echo \"rc=${PIPESTATUS[0]}\"'",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-9.json -- /bin/sh -c 'python3 tools/receipt-window.py --bogus 2>&1; echo \"rw-usage=$?\"; python3 tools/receipt-measure.py --bogus 2>&1; echo \"rm-usage=$?\"; python3 .ufo/evidence/round-20/coldread/measure.py --bogus 2>&1; echo \"cm-usage=$?\"'",
   "python3 tools/trace-inputs.py --root /tmp/TameshiR29.Read11B-dKQh/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-10.json -- /bin/sh -c 'python3 tools/receipt-window.py 2>&1 | tail -1; echo \"noargs=${PIPESTATUS[0]}\"; python3 tools/receipt-window.py --contract /nonexistent.json --receipts .ufo/evidence/round-20/final/receipts.json --json 2>&1 | tail -1; echo \"badcontract=${PIPESTATUS[0]}\"; grep -c \"expectations|install_window\" tools/receipt-window.py; grep -c \"<six predicate ids>\" .ufo/evidence/round-20/stage/measure.py'"
  ], "opened": [
   ".ufo/evidence/round-18/measure.py",
   ".ufo/evidence/round-20/coldread/measure.py",
   ".ufo/evidence/round-20/coldread/ledger.json",
   ".ufo/evidence/round-20/contract.json",
   ".ufo/evidence/round-20/final/checks.json",
   ".ufo/evidence/round-20/final/receipts.json",
   ".ufo/evidence/round-20/public-cli-cases.json",
   ".ufo/evidence/round-20/stage/measure.py",
   ".ufo/evidence/round-20/stage/receipt-window.py",
   "corpus/QUALITY.md",
   "corpus/SOURCES.md",
   "corpus/lessons/round-20.md",
   "tools/receipt-measure.py",
   "tools/receipt-window.py",
   "tools/registry.json",
   "tools/trace-inputs.py"
  ],
  "inputs": {
   ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37",
   ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13",
   ".ufo/evidence/round-20/coldread/ledger.json": "ddd15b21523cc25a80730b7899323b0129c1eab6263524e54cde1114bdebf04d",
   ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715",
   ".ufo/evidence/round-20/final/checks.json": "2f6f67a079c1f5243655d3f1d29b32942eb44d5b8d873c7d9045260c9b8f01b0",
   ".ufo/evidence/round-20/final/receipts.json": "4186b44e6f5ef95aeb39768e5b9d8a0e6953283961bcc009733dbbcde48cb5d6",
   ".ufo/evidence/round-20/public-cli-cases.json": "590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2",
   ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d",
   ".ufo/evidence/round-20/stage/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
   "corpus/QUALITY.md": "069ef729b7738927585f487afa3c26b4912b9d568cb9f0c69b00c3f172538e07",
   "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
   "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6",
   "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa",
   "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc",
   "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
   "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
  }, "external_inputs": {}, "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-2.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-4.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-5.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-6.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-7.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-8.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-9.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/TameshiR29.Read11B-10.json"
  ]}]}
```

Checked at detached clone rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 (SKILL.md sha matches the given c46ec02e...). The section is a record (facts with pointers, not a directive). Verified:

- Source line: `corpus/lessons/round-20.md` exists; QUALITY41 is corpus/QUALITY.md line 390 (freeze staged paths + SHA-256 before dispatch; install only after readers return — matches the section's recipe prose); S049 is the Python subprocess env source, reopened by round-20 for the child-environment boundary (SOURCES.md:58, :197-203, :267-270).
- Byte-preserved stage files: tools/receipt-window.py == .ufo/evidence/round-20/stage/receipt-window.py (same sha256 f03ae7e9...); stage/measure.py sha256 f34dc233... equals the contract frozen_sha256/installed_sha256.
- "--check" claim: the inherited contract `measurement` string carries `--check`, but the active counting entries in final/checks.json (c1-before-current, c1-after) run the wrapper with `--json`; the wrapper docstring says `--check` is not accepted or translated; selftest case 10 confirms it stays unsupported; checks.json also holds the separate "inherited-unsupported-check" refusal receipt.
- runner_sha256: receipts.json records runner_sha256 a67bffa9... == sha256(tools/receipt-measure.py) beside instrument_sha256 f34dc233... (the frozen ruler); selftest prints the same pair (RECEIPT_MEASURE_RUNNER_SHA256 / ROUND20_MEASURE_INSTRUMENT_SHA256).
- receipt-window gate: `python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json` exits 0, verdict CLEAN with two INSTALL_IDENTITY infos; `--selftest` prints RECEIPT_WINDOW_SELFTEST: 20/20 pass (exit 0). Exit codes observed: 0 clean, 2 could-not-evaluate (unreadable contract prints CONTRACT_INVALID), 64 usage (no args). Unrecognized argparse args exit 2, which the map also covers under could-not-evaluate.
- receipt-measure gate: documented counting invocation `tools/receipt-measure.py --repo CLONE --rev 9f3084bc... --json` exits 0, six predicates all PASS, open=0; selftest 10/10 pass over isolated git fixtures; hardcoded six-item ITEM_IDS; 2 usage (argparse).
- coldread measure probe: plain run exits 0 observed (89-row ledger summary, strict trace gate); `--selftest` prints SELECTOR_SELFTEST: 12/12 pass; refusal of --ledger-file / --ledger-rev / --inputs-overlay observed with SELECTOR_OVERRIDE_FORBIDDEN and exit 64, including abbreviation and equals forms per the selftest output; it delegates to .ufo/evidence/round-18/measure.py (sha 7ca87a7c... == the contract historical "round18-measure" identity) — the "unchanged round18 credit algorithm" claim.
- edit_interval/install_window: the tool requires `edit_interval` when frozen != installed (receipt-window.py:89-101) and never reads `install_window` or `expectations` (0 grep hits) — both fields sit in contract.json as descriptive text, as claimed. Receipts record aware measurement_interval start/end plus instrument_sha256, as the recipe requires.
- public-cli-cases.json is a 20-case synthetic fixture set (schema tameshi-r20-cli-fixtures-v1). Historical block holds four shas and the gate classifies all four ("4/4 identities classified"), consistent with "classified, not authenticated or re-executed".

One nuance, non-blocking: the probe's ledger is fetched at --rev via git objects, so the collector receipts for the probe runs show only code inputs; I hashed the worktree ledger.json myself and put it in inputs.

No installs or tool changes were needed; no live-lane reads; all commands ran inside /tmp/TameshiR29.Read11B-dKQh under the trace collector.

COLDREAD Read11B: verified-record
