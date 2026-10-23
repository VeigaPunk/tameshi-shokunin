Read11C cold read — SKILL.md section `### Round-20 gate/probe registry — frozen receipt instruments`
(start line 1938, runs through line 1963; next heading `### Round-21 gate/probe registry` at line 1964).
Read from a detached clone at 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 (SKILL.md sha256 verified
equal to the given c46ec02e…36d6). All commands ran under `tools/trace-inputs.py` from inside the
clone; receipts are at `.ufo/evidence/round-29/coldread/traces/Read11C-*.json`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read11C", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1938, "heading": "### Round-20 gate/probe registry — frozen receipt instruments", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [],
  "commands_executed": [
    "python3 -c \"<open+sha256 printer>\" .ufo/evidence/round-20/contract.json .ufo/evidence/round-20/final/receipts.json .ufo/evidence/round-20/stage/measure.py  [receipt Read11C-1, exit 0]",
    "python3 -c \"<open+sha256 printer>\" corpus/lessons/round-20.md tools/receipt-window.py  [Read11C-2, exit 0]",
    "python3 -c \"<open+sha256 printer>\" corpus/QUALITY.md corpus/SOURCES.md  [Read11C-3, exit 0]",
    "python3 -c \"<open+sha256 printer>\" tools/receipt-measure.py .ufo/evidence/round-20/coldread/measure.py  [Read11C-4, exit 0]",
    "python3 /tmp/Read11C-2w5F/sha.py .ufo/evidence/round-20/stage/receipt-window.py .ufo/evidence/round-20/public-cli-cases.json  [Read11C-6, exit 0]",
    "python3 tools/receipt-window.py --contract .ufo/evidence/round-20/contract.json --receipts .ufo/evidence/round-20/final/receipts.json --json  [Read11C-7, exit 0 CLEAN]",
    "python3 tools/receipt-window.py --selftest  [Read11C-8, exit 0, 20/20]",
    "python3 tools/receipt-measure.py --selftest  [Read11C-11, exit 0, 10/10]",
    "timeout 300 python3 tools/receipt-measure.py --repo <clone> --rev c144dcd807166dfc275c1ac2936fd2fa4b678bda --json  [Read11C-12a, exit 1, corrected 0/6]",
    "timeout 300 python3 tools/receipt-measure.py --repo <clone> --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --json  [Read11C-12b, exit 0, corrected 6/6]",
    "timeout 300 python3 .ufo/evidence/round-20/coldread/measure.py --repo <clone> --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --explain  [Read11C-13, exit 0]",
    "timeout 60 python3 tools/receipt-measure.py --check  [Read11C-14, exit 2 usage rejection]",
    "python3 .ufo/evidence/round-20/coldread/measure.py --selftest  [Read11C-15, exit 0, 12/12]"
  ],
  "opened": ["SKILL.md", "tools/trace-inputs.py", ".ufo/waves/round-26/w1/ColdreadPilot.md", ".ufo/evidence/round-20/contract.json", ".ufo/evidence/round-20/final/receipts.json", ".ufo/evidence/round-20/stage/measure.py", ".ufo/evidence/round-20/stage/receipt-window.py", "tools/receipt-window.py", "tools/receipt-measure.py", ".ufo/evidence/round-20/coldread/measure.py", ".ufo/evidence/round-20/coldread/ledger.json", ".ufo/evidence/round-18/measure.py", ".ufo/evidence/round-20/public-cli-cases.json", "corpus/lessons/round-20.md", "corpus/QUALITY.md", "corpus/SOURCES.md"],
  "inputs": {"tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4", ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7", ".ufo/evidence/round-20/contract.json": "9b2813342768fdaa51bfd670a19d8573f87169a59b98207200e622f8e2b62715", ".ufo/evidence/round-20/final/receipts.json": "4186b44e6f5ef95aeb39768e5b9d8a0e6953283961bcc009733dbbcde48cb5d6", ".ufo/evidence/round-20/stage/measure.py": "f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d", ".ufo/evidence/round-20/stage/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc", "tools/receipt-window.py": "f03ae7e91607750e2690f7819c486a3d9db03ee13f0b8cf51958462834dcf7cc", "tools/receipt-measure.py": "a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa", ".ufo/evidence/round-20/coldread/measure.py": "48927bfeaf9c70108270e022478366bfdb2a47821724eaba1001aefe1264fe13", ".ufo/evidence/round-20/coldread/ledger.json": "ddd15b21523cc25a80730b7899323b0129c1eab6263524e54cde1114bdebf04d", ".ufo/evidence/round-18/measure.py": "7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37", ".ufo/evidence/round-20/public-cli-cases.json": "590df60420a60bec1f6dddad6b5eaf34a5d700cdd86c5cf231b1ef8f5a3b27b2", "corpus/lessons/round-20.md": "7dab5fc4c3e18153c919fd46f5c2d534ccf2ff0904462177d6e31fe2ceb31dc6", "corpus/QUALITY.md": "069ef729b7738927585f487afa3c26b4912b9d568cb9f0c69b00c3f172538e07", "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca"},
  "external_inputs": {},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-6.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-7.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-8.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-11.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-12a.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-12b.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-13.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-14.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read11C-15.json"]}]}
```

## What I checked

The section is a three-row registry (receipt-window gate, receipt-measure wrapper, coldread
selector probe) plus a receipt-window recipe paragraph. I ran every named entry at the clone.

**Row 1 `tools/receipt-window.py` (gate).** Bytes at this rev are f03ae7e9…, identical to
`.ufo/evidence/round-20/stage/receipt-window.py` and to contract frozen_sha256 and
installed_sha256 — the identity case the text describes. The published entry
`--contract … --receipts … --json` ran exit 0 with `verdict: CLEAN`, two INSTALL_IDENTITY
infos (no freshness-floor check, matching the stated identity rule). `--selftest` ran exit 0,
`RECEIPT_WINDOW_SELFTEST: 20/20`. Verdict map 0/1/2/64 matches the code's
EXIT_CLEAN/EXIT_FAIL/EXIT_CE/EXIT_USAGE. `public-cli-cases.json` exists (sha 590df604…)
and is a synthetic-fixtures file with independent expectations exactly as the row claims.

**Row 2 `tools/receipt-measure.py` (gate wrapper).** Bytes a67bffa9… equal the
`runner_sha256` persisted in final/receipts.json. `--selftest` ran exit 0, 10/10, printing
runner sha and instrument sha f34dc233… separately — matching "the wrapper executes the
unchanged frozen ruler and records its own digest separately as runner_sha256". The stage
ruler is byte-identical to the contract's frozen_sha256 (f34dc233…). The counting command
reproduces the round-20 claim at both ends: baseline c144dcd → exit 1, corrected 0/6
(every item FAIL, inputs null because the files are absent at that rev); rev 9f3084bc →
exit 0, corrected 6/6 with all six population items PASS — the same six hardcoded
predicates the section names. `--check` is not accepted anywhere: `tools/receipt-measure.py
--check` exits 2 with a usage error, matching "the active round20 counting entry omits the
inherited unsupported `--check` spelling" (contract.json does carry an
`"instruments": … "measurement": "… --check"` string — descriptive, not enforced).

**Row 3 `.ufo/evidence/round-20/coldread/measure.py` (probe).** `--explain` at the clone
ran exit 0, `overrides_used: false`, `trace_gate: strict`, and its per-section output
reproduces the monitor's own reason for this section
(`input-drift:corpus/QUALITY.md;corpus/SOURCES.md;tools/registry.json`, start 1938 end 1963).
`--selftest` ran 12/12: it loads `.ufo/evidence/round-18/measure.py` (sha 7ca87a7c…, the
classified `round18-measure` historical identity) and refuses `--ledger-file`,
`--ledger-rev`, `--inputs-overlay`, equals forms and abbreviations (`--i`, `--ledger-f`,
`--inputs-o`) with exit 64 `SELECTOR_OVERRIDE_FORBIDDEN` — matching "refuses ledger-file,
ledger-rev and inputs-overlay flags, including abbreviations and equals forms, with
SELECTOR_OVERRIDE_FORBIDDEN". The probe reads only the clone's ledger
(`.ufo/evidence/round-20/coldread/ledger.json`, sha ddd15b21…); no live-lane reads in any
receipt (every receipt's `live_lane_reads` is empty).

**Recipe paragraph.** QUALITY41 (QUALITY.md:390–406) states exactly the freeze/install/
edit_interval/aware-interval rules the paragraph summarizes; "use `edit_interval` (not the
inherited planning annotation `install_window`)" matches receipt-window.py: lines requiring
`edit_interval` when frozen != installed and accepting it as optional when equal, while
`install_window`/`expectations` in contract.json are never read by the gate — "descriptive,
not enforced schema fields". Historical identities: all four contract historical shas are
classified (receipts 12a/12b item `historical_classified` PASS, "4/4 identities
classified"). "Stage files and older receipts are historical evidence and remain
byte-preserved" holds: the stage gate/measure bytes equal the contract's frozen digests.

The `Round-20` section's own Source line (`corpus/lessons/round-20.md`, QUALITY41, S049)
checks out — the lesson exists (sha 7dab5fc4…), QUALITY41 is the receipt-window rule, and
SOURCES.md records S049's used-by gaining the round-20 lesson. One harmless observation:
receipts.json literal duplicate keys under `installed-gate-selftest` (stdout_path/stderr_path
each appear twice — a `.get` read takes the last) do not change any claim.

Tool installs: none. Time in seat ≈ 15 min. No files written outside the traces dir and
this report; clone and /tmp scratch left as scratch only.

COLDREAD Read11C: executed-ok
