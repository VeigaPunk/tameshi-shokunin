# ColdB07 — cold read, three SKILL.md sections at bb68156

Independent cold read of SKILL.md sections at
`bb681566b18211adf8ae9c28df91e17678e3f545` (SKILL.md sha256
`c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6`, verified on
the clone). Clone: `/tmp/ColdB07-R7Sf/fleet/tameshi-shokunin`, detached at the
read rev, fleet-mirror layout with sibling `*-shokunin` symlinks. Every command
below ran under `tools/trace-inputs.py` from inside the clone; receipts are in
`.ufo/evidence/round-30/coldread/traces/`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB07", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
  {"start": 1563, "heading": "## Effective expectation reconciliation — round 14", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
   "commands_executed": [
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json",
    "bash -c 'cd /tmp/ColdB07-R7Sf/r14arch && python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json'",
    "bash -c 'cd /tmp/ColdB07-R7Sf/r14arch && python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json'",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-13-verifier-spotcheck.md corpus/knowledge/incremental-pin-disposition.md .ufo/evidence/round-14/verification-final.json .ufo/evidence/round-14/verification.json .ufo/evidence/round-14/capture-context.py"],
   "opened": ["corpus/lessons/round-13-verifier-spotcheck.md", "corpus/knowledge/incremental-pin-disposition.md", ".ufo/evidence/round-14/verification-final.json", ".ufo/evidence/round-14/verification.json", ".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-14/dispositions-before.json", "tools/evidence-disposition.py", "tools/bash-witness-study.py"],
   "inputs": {
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
    ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
    ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
    ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
    ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
    ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
    ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    ".ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2",
    ".ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939",
    "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
    "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8"},
   "external_inputs": {
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/evidence-disposition.py": "1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725"},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-20-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-20-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-20-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-20-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-20-5.json"]},
  {"start": 1609, "heading": "## Context gate classification and explicit exit classes — round 15", "class": "record", "verdict": "verified-record", "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
   "commands_executed": [
    "python3 tools/context-capture.py --check",
    "python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected /tmp/ColdB07-R7Sf/expected-missing-env.json",
    "python3 tools/context-capture.py --selftest",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-15.md corpus/lessons/round-14-verifier-spotcheck.md .ufo/evidence/round-15/verification-3.json .ufo/evidence/round-14/capture-context.py /home/vgpnk/Projects/shokunin/PROTOCOL.md"],
   "opened": ["corpus/lessons/round-15.md", "corpus/lessons/round-14-verifier-spotcheck.md", ".ufo/evidence/round-15/verification-3.json", ".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-14/context-receipt.json", ".ufo/evidence/round-14/context-missing-env.json", "tools/context-capture.py", "tools/evidence-disposition.py"],
   "inputs": {
    ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
    ".ufo/evidence/round-14/context-missing-env.json": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
    ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
    ".ufo/evidence/round-15/verification-3.json": "3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce",
    "corpus/lessons/round-14-verifier-spotcheck.md": "d267576a0d165d81b734b6c40b5b80bf61ccd9c24c8765992093afbd097cf654",
    "corpus/lessons/round-15.md": "f13a8fe16eabbf3cfc34cd2c7d9b4ee7812cb7b98eb24955dce222e9f4db52ba",
    "tools/context-capture.py": "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8"},
   "external_inputs": {
    "/home/vgpnk/Projects/shokunin/PROTOCOL.md": "886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a",
    "/tmp/ColdB07-R7Sf/expected-missing-env.json": "8fe7adc0bf9c95e269520b92950d85f1b12a6d5b1ad27759fdc0cccd3bf57357"},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-21-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-21-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-21-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-21-4.json"]},
  {"start": 1754, "heading": "## Seventh recorded case and full-page cold-read — round 16", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
   "commands_executed": [
    "bash -c 'bash tools/mutate-and-run.sh --target /tmp/ColdB07-R7Sf/round-gate.mjs --defects .ufo/evidence/round-16/round-gate/round-gate.defects.spec --suite \"$(cat .ufo/evidence/round-16/round-gate/suite.txt)\" --label js-round-gate --workdir /tmp/ColdB07-R7Sf/rgwork'",
    "python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest",
    "python3 .ufo/evidence/round-16/coldread/assemble.py --selftest",
    "python3 .ufo/evidence/round-16/measure.py --selftest",
    "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kumitate-round-gate.md tools/mutate-and-run.sh .ufo/evidence/round-16/round-gate/predictions.json .ufo/evidence/round-16/round-gate/sweep/results.tsv",
    "python3 .ufo/evidence/round-16/measure.py --rev bb681566b18211adf8ae9c28df91e17678e3f545"],
   "opened": ["corpus/knowledge/mutation-case-kumitate-round-gate.md", "tools/mutate-and-run.sh", ".ufo/evidence/round-16/round-gate/predictions.json", ".ufo/evidence/round-16/round-gate/sweep/results.tsv", ".ufo/evidence/round-16/round-gate/round-gate.defects.spec", ".ufo/evidence/round-16/round-gate/suite.txt", ".ufo/evidence/round-16/measure.py", ".ufo/evidence/round-16/coldread/assemble.py", ".ufo/evidence/round-16/attribution/reattribute.py", "tools/registry.json", ".ufo/evidence/round-15/verification-3.json"],
   "inputs": {
    ".ufo/evidence/round-15/verification-3.json": "3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce",
    ".ufo/evidence/round-16/attribution/reattribute.py": "eaf564e42629634e21bc2ee1aa70932a1024d721eba664f8ed892640590015c1",
    ".ufo/evidence/round-16/coldread/assemble.py": "9ee9264aabe9f474b4ecf7cfa52b4d50274ee4a6b82d06df36812a006eb0a156",
    ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
    ".ufo/evidence/round-16/round-gate/predictions.json": "bb344eee3b034d774a829042717dc5c78517edcf8ef5f369831bc2fae0f70bc1",
    ".ufo/evidence/round-16/round-gate/round-gate.defects.spec": "e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4",
    ".ufo/evidence/round-16/round-gate/suite.txt": "6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b",
    ".ufo/evidence/round-16/round-gate/sweep/results.tsv": "97a9377635817a28349ff74aa44352dc8081fb2ef6ba5401c255b350f6e8d0bb",
    "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c"},
   "external_inputs": {
    "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9"},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-22-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-22-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-22-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-22-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-22-5.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB07-22-6.json"]}]}
```

What I checked, per section.

**Section 20 (`## Effective expectation reconciliation — round 14`, line 1563) — instruction, executed-ok.** At the read rev, both historical manifests return exit 2 `expected_input_digest_mismatch`, exactly as the recipe claims (receipts 20-1, 20-2; the mismatching input today is `tools/bash-witness-study.py` — the wording says only that both manifests return 2, which held). In a `git archive 28aeef4` extraction the replay gives the recorded outcomes: `dispositions-before.json` → exit 1 on `producer_before` (`expected_contains_missing`, receipt 20-3), and `dispositions.json` → exit 0 with `producer_before` superseded and both oracle replacements passing (11 effective / 1 superseded, receipt 20-4) — "keep the raw row, supersede, both replacements pass" confirmed. Step 4's record claims verified: `verification-final.json` carries the corrected selftest (34/34 PASS, exit 0) and `verification.json` retains the initial fixture failures (18 of 34 FAIL, exit 1), with `measured_commit` recorded separately. The archived `capture-context.py` sha256 matches the section-21 pin (7313e9a2…). `evidence-disposition.py --selftest` was deliberately not run: at this rev its selftest builds `jj` colocated fixture repos (`_jj_init_fixture_repo` calls `jj git init --colocate`), and my bounds forbid any `jj` invocation; the entry commands above exercise the gate fully.

**Section 21 (`## Context gate classification and explicit exit classes — round 15`, line 1609) — record, verified-record.** Both pinned sha256s check out: `capture-context.py` = `7313e9a2…`, `context-missing-env.json` = `1ee9d09b…`, `context-receipt.json` = `05cb55b8…`. The maintained gate behaves as written: `--check` on the frozen receipt → `CONTEXT: OK (id=context_consistent … exit=0)`; `--check` on the negative fixture with a caller-committed `tameshi-context-expected-v1` pin (`missing_injected_environment`, exit 1) → `CONTEXT: MISMATCH`, exit 1, findings `missing_injected_environment` + `receipt_verdict_mismatch`; `--selftest` → PASS 49/49 covering the claimed exit classes (0 clean, 1 named findings, 2 could-not-evaluate kinds like `snapshot_tampered`/`receipt_json_invalid`, 64 `usage_error`). The retained receipt holds exactly six mapping legs with `all_match` and `injected_env == {"GIT_DIR": <poison>}` as claimed. Source pointers resolve: `verification-3.json` exists as the effective receipt, `round-14-verifier-spotcheck.md` item 5 (line 160) is exactly the routed gate-classification/exit-64 defect this section closes, `round-15.md` has the cited Gate and Mistakes sections, and `../PROTOCOL.md` §Gate standard exists at the fleet root (recorded as an external input, sha `886e459b…`).

**Section 22 (`## Seventh recorded case and full-page cold-read — round 16`, line 1754) — instruction, executed-ok.** The reproduce recipe ran end to end in my `/tmp`: `round-gate.mjs` materialized from `kumitate-shokunin@364f1d5` hashes to the pinned blob `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` (80,415 B); `MUTATE_SPEC … defects=10`; `CONTROL: GREEN`; each of the 10 pre-registered predictions held — A1, A3, B1, E3, C1060 KILLED; C1059, A2, B2, CKIND, E1 SURVIVED; `MUTATE: DONE (… killed=5 survived=5 inconclusive=0 kill-rate=50%)`; `MUTATE_RESTORE: OK` (receipt 22-1). This byte-for-byte matches `sweep/results.tsv` and `predictions.json` (`registered_at_utc 2026-10-20T13:39:42Z` vs `e69b488` committer `2026-10-20T10:39:59-03:00`, before the 13:40:15Z sweep). The ledger-leg claim verified by execution rather than the >6-minute `--regression` run: `measure.py --rev bb68156…` exits 0 with `recorded_cases: 9`, `ledger_guardrail.regression_calls: 9`, and `js-round-gate` among nine legs — consistent with "`cases=9` since round 26" (the section's `cases=7`/`cases=8` phrasing is explicitly dated to rounds 16/18). The registry's other rows executed as written: `reattribute.py --selftest` → PASS (8/8 new rule, 14/14 old-rule fidelity), `assemble.py --selftest` → all checks passed, `measure.py --selftest` → 38/38. `mutate-and-run.sh --selftest` alone was not run — the reproduce command is the stronger execution of that row; the full `--regression` was skipped because nine mutation legs exceed the six-minute per-command bound. One trace artifact: `measure.py --rev` read the live lane's `.git` objects (its documented `--rev` mechanism); every such read is under `.git/` and recorded in receipt 22-6's `live_lane_reads`, never a live-tree path.

Tooling: no installs were needed; `git`, `strace`, `python3`, `node` (v24.21.0), `bash` sufficed.

COLDREAD ColdB07: section 20 executed-ok, section 21 verified-record, section 22 executed-ok