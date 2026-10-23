# ColdA07 — cold read of SKILL.md sections 19–21 at bb681566b18211adf8ae9c28df91e17678e3f545

Read in a detached clone at /tmp/ColdA07-kPcJ/fleet/tameshi-shokunin (HEAD = bb681566b18211adf8ae9c28df91e17678e3f545,
SKILL.md sha256 c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6). All traced receipts carry
rev bb681566b18211adf8ae9c28df91e17678e3f545. Trace receipts:
/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-*.json

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdA07", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
  {"start": 1548, "heading": "### Round-13 gate/probe registry", "class": "record", "verdict": "verified-record",
   "blocking_gaps": [], "wrong_expectations": [],
   "minor_gaps": ["The probe row's normal-mode entry command (pin-disposition --root /home/vgpnk/Projects/shokunin) was not executed because it reads the live fleet, which is barred during cold reads; every other row claim was exercised (both selftest commands pass 19/19 and 39/39; witness-metadata --check --companion exits 0 metadata_consistent; all pinned files present at the stated paths; S048/S047 supersession and the item-4 prioritisation wording confirmed in corpus/SOURCES.md)."],
   "commands_executed": [
    "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" tools/pin-disposition.py tools/witness-metadata.py .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/witness-metadata.json .ufo/evidence/round-13/expected.json",
    "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
    "python3 tools/pin-disposition.py --selftest",
    "python3 tools/witness-metadata.py --selftest"],
   "opened": ["tools/pin-disposition.py", "tools/witness-metadata.py", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/witness-metadata.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json", "corpus/SOURCES.md"],
   "inputs": {
    "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
    "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
    ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
    ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    "corpus/SOURCES.md": "b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7"},
   "external_inputs": {},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-19-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-19-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-19-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-19-4.json"]},
  {"start": 1563, "heading": "## Effective expectation reconciliation — round 14", "class": "record", "verdict": "verified-record",
   "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
   "commands_executed": [
    "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" corpus/lessons/round-13-verifier-spotcheck.md corpus/knowledge/incremental-pin-disposition.md",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
    "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" .ufo/evidence/round-14/verification-final.json .ufo/evidence/round-14/verification.json .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/dispositions.json",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json  (cwd=/tmp/ColdA07-kPcJ/archive28, the extracted git archive 28aeef4 tree; exit 0 clean)",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json  (cwd=/tmp/ColdA07-kPcJ/archive28; exit 1, finding expected_contains_missing on producer_before)",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json  (live tree; exit 2 expected_input_digest_mismatch)"],
   "opened": ["corpus/lessons/round-13-verifier-spotcheck.md", "corpus/knowledge/incremental-pin-disposition.md", "corpus/SOURCES.md", ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-14/dispositions-before.json", ".ufo/evidence/round-14/verification.json", ".ufo/evidence/round-14/verification-final.json", ".ufo/evidence/round-18/dispositions.json", "tools/evidence-disposition.py", "tools/bash-witness-study.py", "tools/mutate-and-run.sh", "tools/pin-disposition.py", "tools/witness-metadata.py", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/witness-metadata.json", ".ufo/evidence/round-13/witness-metadata-old-null.json", ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json"],
   "inputs": {
    "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420",
    "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
    "corpus/SOURCES.md": "b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7",
    ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
    ".ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939",
    ".ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
    "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
    "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
    ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
    ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
    ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
    ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9"},
   "external_inputs": {
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/evidence-disposition.py": "1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d"},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-20-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-20-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-20-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-20-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-20-5.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-20-6.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-20-7.json"]},
  {"start": 1609, "heading": "## Context gate classification and explicit exit classes — round 15", "class": "record", "verdict": "verified-record",
   "blocking_gaps": [], "wrong_expectations": [], "minor_gaps": [],
   "commands_executed": [
    "python3 tools/context-capture.py --check",
    "python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected /tmp/ColdA07-kPcJ/expected-missing.json",
    "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" .ufo/evidence/round-14/capture-context.py .ufo/evidence/round-15/verification-3.json corpus/lessons/round-14-verifier-spotcheck.md corpus/lessons/round-15.md corpus/SOURCES.md",
    "python3 tools/context-capture.py --selftest",
    "python3 -c \"import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]\" .ufo/evidence/round-18/dispositions.json",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json  (exit 2, confirms the row's 'round 17's now 2' parenthetical)"],
   "opened": ["tools/context-capture.py", "tools/evidence-disposition.py", ".ufo/evidence/round-14/context-receipt.json", ".ufo/evidence/round-14/context-missing-env.json", ".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-15/verification-3.json", ".ufo/evidence/round-18/dispositions.json", ".ufo/evidence/round-17/dispositions.json", "corpus/lessons/round-14-verifier-spotcheck.md", "corpus/lessons/round-15.md", "corpus/SOURCES.md", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/witness-metadata.json", ".ufo/evidence/round-13/witness-metadata-old-null.json", ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json", "tools/bash-witness-study.py"],
   "inputs": {
    "tools/context-capture.py": "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
    ".ufo/evidence/round-14/context-missing-env.json": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
    ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
    ".ufo/evidence/round-15/verification-3.json": "3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
    ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
    "corpus/lessons/round-14-verifier-spotcheck.md": "d267576a0d165d81b734b6c40b5b80bf61ccd9c24c8765992093afbd097cf654",
    "corpus/lessons/round-15.md": "f13a8fe16eabbf3cfc34cd2c7d9b4ee7812cb7b98eb24955dce222e9f4db52ba",
    "corpus/SOURCES.md": "b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
    ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
    ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
    ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
    ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9"},
   "external_inputs": {"/home/vgpnk/Projects/shokunin/PROTOCOL.md": "886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a"},
   "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-21-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-21-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-21-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-21-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-21-5.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA07-21-6.json"]}]}
```

## What I checked

**Section 19 (record, verified-record).** All five cited lane files exist and the two registry rows hold up:
`python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` exits 0 with
`metadata_consistent reason=ok` (matching the 0-clean row). Both selftest commands run: `pin-disposition.py --selftest`
PASS 19/19, `witness-metadata.py --selftest` PASS 39/39 including blind-upgrade, tamper, path-escape and duplicate-key
cases (consistent with the 0/1/2 verdict map). The S048-supersedes-S047 note is confirmed verbatim in
`corpus/SOURCES.md` rows S047/S048 ("item 4 is prioritisation rather than a reuse skip"). One coverage gap, recorded as
minor: the probe's normal-mode command `pin-disposition.py --root /home/vgpnk/Projects/shokunin` was not run because it
reads the live fleet, which the cold-read bounds bar.

**Section 20 (record, verified-record).** Every checkable claim was exercised:
- At the read rev, `evidence-disposition.py --root .` exits 2 `expected_input_digest_mismatch` for BOTH the
  `dispositions.json` and `dispositions-before.json` manifests (observed bash-witness-study digest
  60575e62… vs pinned 49e9e5e2…) — exactly as the section states.
- Frozen replay in an extracted `git archive 28aeef4` tree (full rev 28aeef498cc070c3183271b709bc79d344ff547a):
  `dispositions.json` → exit 0 clean (11 passed + 1 superseded, 12 expected checks — matching "twelve expected rows
  from thirteen pinned inputs", since the tool verifies 13 historical input files); `dispositions-before.json` → exit 1
  failing `producer_before` with `expected_contains_missing` — matching step 2's "a matching exit 1 alone is
  insufficient" (the failure is the missing assertion, not merely the exit code).
- Live entry `.ufo/evidence/round-18/dispositions.json` → exit 0 clean.
- `verification.json` retains the initial failing `disposition_selftest` row (exit 1, `clean-superseded FAIL`),
  `verification-final.json` retains the corrected run and names its own `measured_commit` separately; the supersession
  note is present. `capture-context.py` was not run (as the section instructs).
- Cited sources exist: `corpus/lessons/round-13-verifier-spotcheck.md`, `corpus/knowledge/incremental-pin-disposition.md`,
  S003 Limitations and S049 rows in `corpus/SOURCES.md`.

**Section 21 (record, verified-record).** All pinned digests verified by sha256sum: archived
`capture-context.py` = 7313e9a2…, negative fixture `context-missing-env.json` = 1ee9d09b…, clean receipt
`context-receipt.json` = 05cb55b8… — all matching the text. `python3 tools/context-capture.py --check` exits 0
`context_consistent`. With a caller pin (`{"schema":"tameshi-context-expected-v1","receipt_sha256":"1ee9d09b…",
"id":"missing_injected_environment","exit":1}`), `--check --receipt context-missing-env.json` exits 1 with finding
`missing_injected_environment` plus `receipt_verdict_mismatch` — matching the "must fail at exit1" claim.
`context-capture.py --selftest` PASS 49/49, exercising exit classes 0/1/2/64 as the exit-class paragraph states.
Cited line ranges in `capture-context.py` hold: `:2-31` docstring describes the two-document comparison with only
top-level `observed_at` excluded, env delta and git control; `:553-580` is `decide()` returning ok/0 or mismatch/1;
`:605-643` is `main()` writing the receipt and returning code. `verification-3.json` exists (passed=true,
`scope: retained-receipt gate replay`). The round-15 registry's parenthetical claims check out:
`.ufo/evidence/round-18/dispositions.json` → 0 and `.ufo/evidence/round-17/dispositions.json` → 2. `../PROTOCOL.md`
(fleet root) exists and §Gate standard is at line 375; it was read by hand outside the collector and is recorded in
`external_inputs` with its sha256. The caller-supplied expected pin lived under /tmp and is outside every receipt
bucket; noted here for completeness.

Tooling: no installs or upgrades were needed (strace, python3, git all present).

COLDREAD ColdA07: verified-record, verified-record, verified-record
