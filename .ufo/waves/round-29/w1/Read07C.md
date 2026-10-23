# Read07C — cold read, SKILL.md:1563-1596

Section: `## Effective expectation reconciliation — round 14` (lines 1563 to
1596; the next heading outside code fences is `### Round-14 historical
registry — superseded by round 15` at line 1597). Read at
9f3084bc60ad56aac01e4556ef4c7653df2f65e5 in a fleet-mirror clone at
/tmp/Read07C-JhOs/fleet/tameshi-shokunin (SKILL.md sha256 verified against
the given value).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read07C", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1563, "heading": "## Effective expectation reconciliation — round 14", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": ["The parenthetical '(the runner moved in round 16)' is a true but incomplete cause: at 9f3084bc the observed finding detail actually names tools/bash-witness-study.py (which moved in round 18, sha 49e9e5e2 -> 60575e62); the runner tools/mutate-and-run.sh also drifted (75ed934d -> fb91ef76 in round-16 commits c699c8c/05a2247) and alone would already force exit 2, so the stated reason is correct but the reported mismatch names the other drifted input."],
  "commands_executed": [
  "python3 tools/evidence-disposition.py --root /tmp/Read07C-JhOs/fleet/tameshi-shokunin --dispositions /tmp/Read07C-JhOs/fleet/tameshi-shokunin/.ufo/evidence/round-14/dispositions-before.json --json",
  "python3 tools/evidence-disposition.py --root /tmp/Read07C-JhOs/fleet/tameshi-shokunin --dispositions /tmp/Read07C-JhOs/fleet/tameshi-shokunin/.ufo/evidence/round-14/dispositions.json --json",
  "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-14/expected-outcomes.json .ufo/evidence/round-14/before.json .ufo/evidence/round-14/after-committed.json",
  "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-14/verification.json .ufo/evidence/round-14/verification-final.json .ufo/evidence/round-14/context-missing-env.json",
  "python3 -c \"import sys;[print(open(p).read()[:100000]) for p in sys.argv[1:]]\" tools/evidence-disposition.py .ufo/evidence/round-14/capture-context.py",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json (lane-root form, receipt Read07C-6)",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json (lane-root form, receipt Read07C-7)",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json (cwd = extracted git archive 28aeef4 tree, receipt Read07C-8)",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json (cwd = extracted git archive 28aeef4 tree, receipt Read07C-9)",
  "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/producer-oracle-repair.json",
  "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-13-verifier-spotcheck.md corpus/knowledge/incremental-pin-disposition.md",
  "python3 -c \"...SOURCES.md S049/S003 excerpt reader...\" corpus/SOURCES.md",
  "python3 -c \"import hashlib,sys; ...sha256 read...\" .ufo/evidence/round-14/context-receipt.json",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json"],
  "opened": [".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/witness-metadata-old-null.json", ".ufo/evidence/round-13/witness-metadata.json", ".ufo/evidence/round-14/after-committed.json", ".ufo/evidence/round-14/before.json", ".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-14/context-missing-env.json", ".ufo/evidence/round-14/context-receipt.json", ".ufo/evidence/round-14/dispositions-before.json", ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-14/expected-outcomes.json", ".ufo/evidence/round-14/verification-final.json", ".ufo/evidence/round-14/verification.json", ".ufo/evidence/round-18/dispositions.json", ".ufo/waves/round-26/w1/ColdreadPilot.md", "corpus/SOURCES.md", "corpus/knowledge/incremental-pin-disposition.md", "corpus/lessons/round-13-verifier-spotcheck.md", "tools/bash-witness-study.py", "tools/evidence-disposition.py", "tools/mutate-and-run.sh", "tools/pin-disposition.py", "tools/trace-inputs.py", "tools/witness-metadata.py"],
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
    ".ufo/evidence/round-14/after-committed.json": "0a3135ca219cfe92d72815f3c04835d98baedbfd777713a39287025a0a8eefef",
    ".ufo/evidence/round-14/before.json": "03f6e32c959307351be87a872b6951ed618d227363c55abe46cc3192980644b2",
    ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
    ".ufo/evidence/round-14/context-missing-env.json": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
    ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
    ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
    ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    ".ufo/evidence/round-14/expected-outcomes.json": "e7803c1e76980a4d8c7d89ffbab49a32e307f98b98e216a490f6d103c20e5d85",
    ".ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2",
    ".ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
    ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7",
    "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
    "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
    "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
    "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
    "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"},
  "external_inputs": {
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/evidence-disposition.py": "1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/bash-witness-study.py": "49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005"},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-5.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-6.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-7.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-8.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-9.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-10.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-11.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-12.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-13.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07C-14.json"]}]}
```

Checked: classed as instruction (the Recipe tells the reader to run the
evidence-disposition replay). At `--root .` in the clone, both
`dispositions-before.json` and `dispositions.json` exits 2 with
`expected_input_digest_mismatch` on tools/bash-witness-study.py, matching the
section's statement; the pinned runner tools/mutate-and-run.sh also moved in
round-16 commits, so the parenthetical reason holds (see minor gap above).
In an extracted `git archive 28aeef4` tree the verbatim recipe command on
`dispositions-before.json` exits 1 with finding `expected_contains_missing`
for `producer_before` ("stdout lacks 'summary preserves top-level exposed
declaration kind'"), and the same command on `dispositions.json` exits 0
(clean, counts effective=11 superseded=1), exactly as steps 2-3 claim; the
superseded row keeps raw_receipt/raw_check and both oracle replacements, and
the live `--dispositions .ufo/evidence/round-18/dispositions.json` run exits
0 at --root . (round-17 re-pin section exists at SKILL.md:1814). Step 4:
verification.json's disposition_selftest exits 1 with 18 FAIL / 16 PASS over
34 SELFTEST_CASE lines — the "initial 18-of-34 fixture failures" wording is
exact; verification-final.json shows the corrected selftest (exit 0) and the
same frozen before/after outcomes plus a `supersedes` note; measured_commit
fields record the revisions separately. Step 5: capture-context.py's
OUTPUT_REL is .ufo/evidence/round-14/context-receipt.json and write_receipt
does os.replace over that path, so re-running it would overwrite the frozen
receipt — the "must not be run again" instruction is correct; the retained
receipt sha256 05cb55b8… matches the round-15 registry's pinned value, and
the round-15 registry contains the retained-only gate
(`tools/context-capture.py --check`). Sources cited all exist: routed defects
1-3 in corpus/lessons/round-13-verifier-spotcheck.md map to the table rows;
SOURCES.md S049 = Python subprocess env mapping, S003 Limitations names
env/dependency/snapshot blind spots; incremental-pin-disposition.md §8 is
"Empirical correction and backlink — round 14". The "twelve expected rows
versus thirteen pinned inputs" distinction checks out: expected_checks=12,
expected.json's inputs map has 13 entries. Receipts 8/9 record the archive
replay with rev=9f3084bc; all 14 receipts exist.

COLDREAD Read07C: executed-ok
