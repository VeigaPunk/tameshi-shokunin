# Read29 cold read: "Context gate classification and explicit exit classes — round 15"

## Verdict

gap-minor. The section is a record: it states facts with pointers and tells no reader to run a command. Every factual claim I could run held at 2227d83. The section needs five wording or pointer fixes, listed below. None of them blocks the claim.

## Scope and setup

- Clone: /tmp/Read29-bYE9/fleet/tameshi-shokunin, detached at 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. HEAD and SKILL.md sha256 (386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95) both confirmed.
- Section bounds: SKILL.md:1609 to 1675. The next heading, "### Round-15 gate/probe registry", starts at 1676 and is not in this bucket.
- Monitor drift reasons name six files: corpus/SOURCES.md, tools/bash-witness-study.py, tools/evidence-disposition.py, tools/mutate-and-run.sh, tools/registry.json and tools/trace-inputs.py. All six are hashed at 2227d83 and listed in the inputs field. The section names SOURCES.md (S049, S051) and evidence-disposition.py (both gates) directly. The section's runner is tools/mutate-and-run.sh, pinned by the archived script and round-13 files. trace-inputs.py is the collector. bash-witness-study.py and registry.json are not cited by this section; I hashed them only because the monitor lists them.
- Every gate or selftest run used the clone under the trace collector. The listed receipts are Read29-1.json to Read29-12.json and Read29-14.json to Read29-19.json in the traces directory. Read29-13.json was renamed to EXCLUDED-Read29-13.json on L1 instruction and is not listed. No live-lane file was read during a trace.
- `git status --porcelain` in the clone printed nothing after the gate runs (listed receipt Read29-19), so the gate runs wrote nothing into the clone. An earlier git status run beside receipts 8 to 12 (now EXCLUDED-Read29-13.json) also printed nothing; no claim relies on it.
- No tools were installed or updated.

## Evidence for the held claims

- Hashes match the section: capture-context.py is 7313e9a2...fe89 (27781 bytes, 647 lines); context-receipt.json is 05cb55b8...c1a; context-missing-env.json is 1ee9d09b...208 (Read29-1).
- Frozen replay: `python3 tools/context-capture.py --check` printed `CONTEXT: OK (id=context_consistent ... exit=0 findings=0)` (Read29-2).
- Selftest: `--selftest` printed `SELFTEST: PASS (49/49)` (Read29-3). Disposition selftest printed `SELFTEST: PASS (66/66)` (Read29-6).
- Usage: `context-capture.py --bogus-flag` printed `CONTEXT: USAGE_ERROR (id=usage_error exit=64)` (Read29-4). For the disposition gate, the unknown argument printed usage, and main returns 64 at tools/evidence-disposition.py:3208 (Read29-5).
- Negative fixture, pinned with `.ufo/evidence/round-15/frozen/context-missing-env/expected.json`: exit 1, id missing_injected_environment. The findings are missing_injected_environment (injected_env absent) and receipt_verdict_mismatch (stored status ok, exit 0 versus recomputed mismatch, exit 1) (Read29-8).
- Duplicate key: a scratch copy with a duplicated key gives exit 2, receipt_json_invalid (Read29-10).
- Missing inputs: missing receipt gives exit 2 receipt_missing (Read29-16). Missing dispositions file gives exit 2 dispositions_missing (Read29-17).
- Stored verdict is never trusted: verify_recorded_verdict at tools/context-capture.py:1145-1166 compares stored status, exit and reasons with the recomputed values. The stored-verdict-lie, comparison-observed-at-lie and flag-lie selftest cases all pass (Read29-3).
- Check mode never executes retained argv or reads recorded roots. The only subprocess call is SelftestHarness.run (context-capture.py:1647), which invokes the tool itself with -I (lines 1688-1690). lane_root and fleet_root are validated as strings only (lines 498-511). Writes go only to a mkdtemp directory under /tmp (line 1624).
- The archived script is never invoked. Its name appears only in the tool's docstring.
- Both gates return only codes 0, 1, 2 and 64. Grep found no other return codes in either file.
- Round-14 recipe step 5 (SKILL.md:1592-1595) and the archived registry row (SKILL.md:1602) both say do not run, archive only.
- Source rows: corpus/SOURCES.md:58 (S049) and :60 (S051, used by corpus/lessons/round-15.md). I did not open S049's external documentation.
- Lessons: corpus/lessons/round-15.md:11 is "## Gate", :46 is "## Mistakes", and rows :50-51 record the former probe label and the missing 64 wording. corpus/lessons/round-14-verifier-spotcheck.md:154 is "## Routed defects and residuals" and item 5 is at :160.
- Protocol: /home/vgpnk/Projects/shokunin/PROTOCOL.md:375 is "## Gate standard" (external, read directly, see external_inputs).
- Effective evidence: verification-3.json has passed true (line 547) and failed_checks empty (line 546). Its observed digests for tools/context-capture.py (c4a1d165...), capture-context.py, and both receipts equal today's bytes at 2227d83.
- The two earlier failed receipts are verification.json (passed false, failed_checks selftest-new and selftest-new-full-count, lines 544-548) and verification-2.json (passed false, failed_checks runner-internal-error, lines 119-122).
- Persisted digests match the round-13 declarations: the probe digest 297253... is at .ufo/evidence/round-13/expected.json:9, and the runner digest 75ed934d... is at expected.json:12 and pin-manifest.json:5. The manifest and expected-file digests match the live files.

## Findings by severity

No blocking gap. Every executed verdict-mode check matched the section's exit classes and its stated expectations. M5 notes one self-test setup path that the exit-class wording reaches but that exits 1. Five minor items:

M1 (lines 1648-1650). The sentence calls absent, wrongly typed, duplicate-key and contradicting fields "findings". Observed: duplicate key gives exit 2 receipt_json_invalid (Read29-10). Wrongly typed fields give exit 2 receipt_structure_invalid (selftest cases in Read29-3). Absent injected_env gives exit 1 missing_injected_environment (Read29-8). Other absent required fields give exit 2 through require_object (context-capture.py:383-395). The table at 1662-1666 states the right classes. Smallest fix: name exit 2 for wrongly typed, duplicate-key and absent required fields, and exit 1 for contradicting fields and absent injected_env. In every case the result is never clean.

M2 (lines 1642-1650, table row at 1663). "Source digest disagrees" reads like a check of current source bytes. Check mode compares only stored strings (context-capture.py:1045-1063) and reads no live lane input (docstring lines 10-12). Live bytes at 2227d83 differ from the persisted values: tools/pin-disposition.py is 331529ea... against persisted and declared 297253...; tools/mutate-and-run.sh is fb91ef76... against 75ed934d.... Smallest fix: say "persisted source digest" and state the live drift.

M3 (lines 1616-1617, 1626, 1653-1655). These name no paths. Add: the two failed receipts (round-15/verification.json and verification-2.json), the round-13 files (.ufo/evidence/round-13/expected.json and pin-manifest.json), and the negative pin (.ufo/evidence/round-15/frozen/context-missing-env/expected.json, receipt_sha256 1ee9d09b..., id missing_injected_environment, exit 1). The registry check context-capture-missing-env in tools/registry.json (lines 372-395) uses that pin.

M4 (lines 1653-1655). The text says the negative fixture is "passed with" a pin and "must fail at exit1". It does not say the fixture stores status ok, exit 0 and empty reasons (round-14/context-missing-env.json:418-420). The gate returns exit 1 with primary missing_injected_environment and secondary receipt_verdict_mismatch (Read29-8). Smallest fix: say so, so that "passed" does not read as a clean verdict.

M5 (lines 1668-1674). The exit-class paragraph covers both gates in general. Verdict modes match: usage 64, missing input 2, mismatch 1, clean 0 (Read29-2, 4, 5, 8, 16, 17). The disposition --selftest does not match. Its mkdtemp call (tools/evidence-disposition.py:2351) has no try block, so a setup OSError exits 1 as an uncaught exception (Read29-18, simulated by patching tempfile.mkdtemp). SKILL.md:1705, outside this section, already records "uncaught setup traceback" as exit 1. Smallest fix: scope the paragraph to verdict mode.

## Residual risk and verification gaps

- I read my own receipts back after the traces finished, with grep. They are untracked outputs, so they are not listed as inputs. Every listed Read29 receipt has rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, rev_reason null, tracked_filter true and an empty live_lane_reads object. Receipt exits: 0 for receipts 1 to 3, 6, 7, 9, 11, 12, 14, 15 and 19; 1 for 8 and 18; 2 for 10, 16 and 17; 64 for 4 and 5. These match the printed outputs.
- Read29-13 was excluded on L1 instruction and renamed to EXCLUDED-Read29-13.json. Its git status run, beside receipts 8 to 12, made git re-read the tracked tree during index refresh on the fresh clone, so that receipt lists about 5,800 input lines of evidence files from other rounds. I did not read those files and did not copy them into inputs. No claim in this report rests on it. The clean check rests on Read29-19, which lists only .gitignore; .gitignore is in inputs.
- One broad grep over the traces directory also printed other seats' receipts while I was looking for mine. I did not use them, and they are not section inputs. The rename was a plain mv on L1 instruction, not a verification command, so it has no receipt and is not in commands_executed.
- S049's external documentation was not opened. I checked only the lane's SOURCES row.
- Process claims at lines 1618-1620 and 1671-1674 (no successor sweep, no promotion credit, no changed historical outcome, admission or C1 scalar) were not checked beyond the round-15 lesson's note that the sweep stayed unexecuted (corpus/lessons/round-15.md:6-7).
- The historical wording claim at lines 1671-1672 was checked against the round-15 lesson rows only, not against git history.
- `../PROTOCOL.md` resolves from the live fleet root only. The fleet mirror holds sibling lanes, not PROTOCOL.md, so a reader inside the mirror cannot check §Gate standard. I read the fleet-root file directly and recorded it under external_inputs.
- Registry rows at lines 1676-1706 are outside this bucket. I used them only as pointers.
- Step 1 setup ran outside the collector as the assignment prescribes: mktemp, the symlink loop, git clone, the detached checkout, sha256sum of SKILL.md, and a listing of the clone tools directory. Those commands opened no lane evidence beyond those listings.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read29", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 1609, "heading": "## Context gate classification and explicit exit classes \u2014 round 15", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": [
  "M1 lines 1648-1650 call absent, wrongly typed, duplicate-key and contradicting fields findings. Observed: duplicate key gives exit 2 receipt_json_invalid (Read29-10); wrongly typed fields give exit 2 receipt_structure_invalid (selftest cases in Read29-3); absent injected_env gives exit 1 missing_injected_environment (Read29-8); other absent required fields give exit 2 via require_object (context-capture.py:383-395). The table at 1662-1666 states the right classes. Fix the prose: exit 2 for wrongly typed, duplicate-key and absent required fields; exit 1 for contradicting fields and absent injected_env; never clean.",
  "M2 lines 1642-1650 and table row at 1663 read source digest disagreement as a failure, but check mode compares only stored strings (context-capture.py:1045-1063) and reads no live lane input (docstring lines 10-12). Persisted digests match the round-13 declarations (round-13 expected.json:9 and :12, pin-manifest.json:5). Live bytes at 2227d83 differ: tools/pin-disposition.py is 331529ea against persisted and declared 297253; tools/mutate-and-run.sh is fb91ef76 against 75ed934d. Fix: say persisted source digest and state the live drift.",
  "M3 lines 1616-1617, 1626 and 1653-1655 name no paths. The two earlier failed receipts are .ufo/evidence/round-15/verification.json (passed false, lines 544-548) and verification-2.json (passed false, lines 119-122). The round-13 files live under .ufo/evidence/round-13/. The negative pin is .ufo/evidence/round-15/frozen/context-missing-env/expected.json (receipt_sha256 1ee9d09b, id missing_injected_environment, exit 1); tools/registry.json lines 372-395 uses it. Fix: add these paths.",
  "M4 lines 1653-1655 say the negative fixture is passed with a pin and must fail at exit1, but do not say the fixture stores status ok, exit 0 and empty reasons (.ufo/evidence/round-14/context-missing-env.json:418-420). The gate returns exit 1 with primary missing_injected_environment and secondary receipt_verdict_mismatch (Read29-8). Fix: say so, so that passed does not read as a clean verdict.",
  "M5 lines 1668-1674 state exit classes for both gates in general. Verdict modes match: usage 64 (context-capture.py:2286, evidence-disposition.py:3208), missing receipt 2 (Read29-16), missing dispositions 2 (Read29-17), mismatch 1 (Read29-8), clean 0 (Read29-2). The disposition --selftest does not match: its mkdtemp call (evidence-disposition.py:2351) has no try, so a setup OSError exits 1 as an uncaught exception (Read29-18). SKILL.md:1705, outside this section, already records uncaught setup traceback as exit 1. Fix: scope the paragraph to verdict mode."
 ],
 "commands_executed": [
  "python3 -c <sha256 and line-count reader> tools/context-capture.py tools/evidence-disposition.py tools/pin-disposition.py tools/mutate-and-run.sh .ufo/evidence/round-14/capture-context.py .ufo/evidence/round-14/context-receipt.json .ufo/evidence/round-14/context-missing-env.json .ufo/evidence/round-15/verification.json .ufo/evidence/round-15/verification-2.json .ufo/evidence/round-15/verification-3.json .ufo/evidence/round-15/expected.json .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/pin-manifest.json corpus/lessons/round-15.md corpus/lessons/round-14-verifier-spotcheck.md corpus/SOURCES.md",
  "python3 tools/context-capture.py --check",
  "python3 tools/context-capture.py --selftest",
  "python3 tools/context-capture.py --bogus-flag",
  "python3 tools/evidence-disposition.py --bogus-flag",
  "python3 tools/evidence-disposition.py --selftest",
  "python3 -c <receipt leg and injected_env reader; opens .ufo/evidence/round-14/context-receipt.json and .ufo/evidence/round-14/context-missing-env.json>",
  "python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json --json",
  "mkdir -p /tmp/Read29-bYE9/scratch && python3 -c <duplicate-key fixture builder; opens .ufo/evidence/round-14/context-receipt.json; writes only under /tmp/Read29-bYE9/scratch>",
  "python3 tools/context-capture.py --check --receipt /tmp/Read29-bYE9/scratch/dup.json --expected /tmp/Read29-bYE9/scratch/dup-expected.json --json",
  "python3 -c <sha256 and line-count reader> .ufo/evidence/round-15/frozen/context-missing-env/receipt.json .ufo/evidence/round-15/frozen/context-missing-env/expected.json .ufo/evidence/round-15/frozen/context-clean/receipt.json .ufo/evidence/round-15/frozen/context-clean/expected.json .ufo/evidence/round-15/frozen/mapping-suffix/receipt.json .ufo/evidence/round-15/frozen/mapping-suffix/expected.json tools/trace-inputs.py",
  "python3 -c <sha256 and line-count reader> /home/vgpnk/Projects/shokunin/PROTOCOL.md",
  "git status --porcelain (Read29-19, run after all gate runs)",
  "python3 -c <persisted digest versus round-13 declaration reader; opens .ufo/evidence/round-14/context-receipt.json, .ufo/evidence/round-13/expected.json, .ufo/evidence/round-13/pin-manifest.json, tools/pin-disposition.py and tools/mutate-and-run.sh>",
  "python3 -c <sha256 and line-count reader> tools/bash-witness-study.py tools/registry.json",
  "python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/no-such-receipt.json --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json --json",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-99/no-such.json --json",
  "python3 -c <simulated /tmp setup-failure driver that patches tempfile.mkdtemp and runs tools/evidence-disposition.py --selftest>"
 ],
 "opened": [
  "tools/context-capture.py", "tools/evidence-disposition.py", "tools/trace-inputs.py", "tools/pin-disposition.py", "tools/mutate-and-run.sh", "tools/bash-witness-study.py", "tools/registry.json",
  ".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-14/context-receipt.json", ".ufo/evidence/round-14/context-missing-env.json",
  ".ufo/evidence/round-15/verification.json", ".ufo/evidence/round-15/verification-2.json", ".ufo/evidence/round-15/verification-3.json", ".ufo/evidence/round-15/expected.json",
  ".ufo/evidence/round-15/frozen/context-missing-env/receipt.json", ".ufo/evidence/round-15/frozen/context-missing-env/expected.json",
  ".ufo/evidence/round-15/frozen/context-clean/receipt.json", ".ufo/evidence/round-15/frozen/context-clean/expected.json",
  ".ufo/evidence/round-15/frozen/mapping-suffix/receipt.json", ".ufo/evidence/round-15/frozen/mapping-suffix/expected.json",
  ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-manifest.json",
  "corpus/lessons/round-15.md", "corpus/lessons/round-14-verifier-spotcheck.md", "corpus/SOURCES.md", ".gitignore"
 ],
 "inputs": {
  "tools/context-capture.py": "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726",
  "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
  "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
  "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
  "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
  "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
  "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
  ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
  ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
  ".ufo/evidence/round-14/context-missing-env.json": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
  ".ufo/evidence/round-15/verification.json": "4d2fb03f81df6aa92574187614a2a9ece5b3e928a03170f1e34809109428352d",
  ".ufo/evidence/round-15/verification-2.json": "4073c8c6d1362001cef861c049f66eea139073c14460e38372af78d284ab6ade",
  ".ufo/evidence/round-15/verification-3.json": "3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce",
  ".ufo/evidence/round-15/expected.json": "2e50f9a74cd1599b96976653c99566fffefd11c9e5503261d4fb3575d8d3bc4f",
  ".ufo/evidence/round-15/frozen/context-missing-env/receipt.json": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
  ".ufo/evidence/round-15/frozen/context-missing-env/expected.json": "831ce672dc795311238f58c122788bcd0e0334fc96c4624008f162f879fbb82d",
  ".ufo/evidence/round-15/frozen/context-clean/receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
  ".ufo/evidence/round-15/frozen/context-clean/expected.json": "34aac13399f996e2d46e3301b4d6cd396eccdee204b5d7a52b1bf13ca6326c77",
  ".ufo/evidence/round-15/frozen/mapping-suffix/receipt.json": "02204ef81bd63268eda1c00d98b68a6e5ad9795399c266e57b18f4f8cc58fe5e",
  ".ufo/evidence/round-15/frozen/mapping-suffix/expected.json": "c5779fa69a9244b4fb3f73ad275dd251f4ed75e798d85d4838f4473fa66850da",
  ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
  ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
  "corpus/lessons/round-15.md": "f13a8fe16eabbf3cfc34cd2c7d9b4ee7812cb7b98eb24955dce222e9f4db52ba",
  "corpus/lessons/round-14-verifier-spotcheck.md": "d267576a0d165d81b734b6c40b5b80bf61ccd9c24c8765992093afbd097cf654",
  "corpus/SOURCES.md": "0a66531dde7f086005ddf131a3bc5f920a15af5b614fccd631f8d5a668a58e5a",
  ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116"
 },
 "external_inputs": {"/home/vgpnk/Projects/shokunin/PROTOCOL.md": "886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a"},
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-7.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-8.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-9.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-10.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-11.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-12.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-14.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-15.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-16.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-17.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-18.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read29-19.json"
 ]}]}
```

Plain-English note: I cold-read SKILL.md lines 1609 to 1675 at revision 2227d83 and classed the section as a record. I hashed every cited lane file under the trace collector and compared the hashes with the values the section cites. I ran the context gate in frozen, selftest, pinned-negative, duplicate-key, missing-receipt and usage modes. I ran the disposition gate in usage, missing-input and selftest modes, and I simulated a selftest setup failure. I compared the persisted digests with the round-13 declarations and checked the cited lessons, source rows and protocol heading. The section's factual claims held. The five items above are wording or pointer fixes.

COLDREAD Read29: gap-minor
