# Read09B — cold read of SKILL.md "## Effective expectation reconciliation — round 14" (start 1563)

Seat: TameshiR28.Read09B. Claim served: C1. Clone: /tmp/Read09B-F4mx/fleet/tameshi-shokunin
detached at b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a; SKILL.md sha256
c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6 (matches).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read09B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [{"start": 1563, "heading": "## Effective expectation reconciliation — round 14", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
    "Step 2's phrase 'both manifests now return 2 expected_input_digest_mismatch' reads as exit code 2 plus that finding id; the tool raises on the first mismatched pin only (tools/bash-witness-study.py, alphabetical) even though three of the thirteen pins actually drift at this rev, so a strict reader could misread '2' as a count of findings.",
    "Step 2 says 'Replay with cwd = an extracted git archive 28aeef4 tree' but does not spell out the extraction command; a reader must know `git archive 28aeef4 | tar -x -C DIR` (verified working) before the named evidence-disposition command can run."
  ],
  "commands_executed": [
    "python3 tools/trace-inputs.py --root /tmp/Read09B-F4mx/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-1.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json",
    "python3 tools/trace-inputs.py --root /tmp/Read09B-F4mx/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-2.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json",
    "python3 tools/trace-inputs.py --root /tmp/Read09B-F4mx/fleet/tameshi-shokunin --cwd /tmp/Read09B-F4mx/r14 --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-3.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json",
    "python3 tools/trace-inputs.py --root /tmp/Read09B-F4mx/fleet/tameshi-shokunin --cwd /tmp/Read09B-F4mx/r14 --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-4.json -- python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json",
    "python3 tools/trace-inputs.py --root /tmp/Read09B-F4mx/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-5.json -- python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-13-verifier-spotcheck.md corpus/knowledge/incremental-pin-disposition.md corpus/SOURCES.md .ufo/evidence/round-14/verification.json .ufo/evidence/round-14/verification-final.json .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/capture-context.py .ufo/evidence/round-14/context-receipt.json"
  ],
  "opened": ["corpus/lessons/round-13-verifier-spotcheck.md", "corpus/knowledge/incremental-pin-disposition.md", "corpus/SOURCES.md", "tools/evidence-disposition.py", "tools/trace-inputs.py", "tools/mutate-and-run.sh", "tools/bash-witness-study.py", "tools/pin-disposition.py", "tools/witness-metadata.py", ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-14/dispositions-before.json", ".ufo/evidence/round-14/verification.json", ".ufo/evidence/round-14/verification-final.json", ".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-14/context-receipt.json", ".ufo/evidence/round-14/disposition-delta.json", ".ufo/evidence/round-14/guardrails.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/witness-metadata.json", ".ufo/evidence/round-13/witness-metadata-old-null.json", ".ufo/evidence/round-12/BashWitness/summary.json", ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-18/dispositions.json"],
  "inputs": {
    "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420",
    "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
    "corpus/SOURCES.md": "a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
    "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
    "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
    ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
    ".ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939",
    ".ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2",
    ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89",
    ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
    ".ufo/evidence/round-14/disposition-delta.json": "b662908f13dfe516416c7ac5ea0407aef73286b3f447f2638b473826c9c2dc51",
    ".ufo/evidence/round-14/guardrails.json": "cca670b54f5da70873daec8d1bd54749ea63be99582f21138d43c8c715eaf784",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
    ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
    ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
    ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
    ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676"
  },
  "external_inputs": {}, "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09B-5.json"]}]}
```

What I checked (all at detached clone b05d2ee, traces under the collector):

- Recipe step 1: `.ufo/evidence/round-13/expected.json` carries exactly 12 `expected_checks` and 13 `inputs` pins — "twelve expected rows from thirteen pinned inputs" is literal.
- Recipe step 2 (live tree, both manifests): each traced run exits 2 with `expected_input_digest_mismatch` (traces 1–2). "The runner moved in round 16": `tools/mutate-and-run.sh` first drifted in c699c8c (round-16) after archive rev 28aeef4 (round-15 integrator); pin-disposition.py drifted in round 17 and bash-witness-study.py in round 18.
- Recipe step 2 replay: extracted `git archive 28aeef4` to /tmp/Read09B-F4mx/r14; `dispositions-before.json` → exit 1 with the single finding `expected_contains_missing` on expectation `producer_before` ("stdout lacks 'summary preserves top-level exposed declaration kind'") — exactly the "matching exit 1 alone is insufficient" case (trace 3).
- Recipe step 3 replay: `dispositions.json` → exit 0 clean, counts effective 11 / superseded 1 / findings 0 (trace 4). Diffing the two manifests: the only changed row is `producer_before` (effective → superseded); it retains `raw_receipt`/`.ufo/evidence/round-13/verification.json` and `raw_check: producer_before`, and both `superseded_by` rows (producer_before_oracle, producer_after_oracle) are effective. Identical inputs.
- Recipe step 4: `verification.json` retains `SELFTEST: FAIL (18/34 failed: …)` (initial 18-of-34 fixture failures, verbatim) plus failed unresolved_before (exit 1, failed:1) and clean resolved_after (exit 0). `verification-final.json` retains the corrected selftest (exit 0, 34/34 PASS) with the same frozen before/after outcomes; `measured_commit` is recorded separately in each file.
- Recipe step 5: `capture-context.py` writes only `.ufo/evidence/round-14/context-receipt.json` (OUTPUT_REL, atomic 0644), so rerunning it would replace the frozen receipt — the do-not-run warning is sound. The receipt itself declares `result_reuse: not_established` and a single GIT_DIR injection, matching the last table row's "bounded scrub observation" decision; the round-15 registry row (line 1741) names the maintained retained-only form.
- S049 (Python child-environment contract) and S003 Limitations exist in `corpus/SOURCES.md` at this rev; the lesson's Routed defects 1–3 map to table rows 1–4 (absent assertion → setup failure; supersession with two effective replacements; retained mismatched raw bytes; child env not recoverable from output equality); the knowledge doc's section 8 is the cited "empirical correction" (34/34 after two fixture-only corrections, initial 18-of-34 retained, one superseded of twelve).
- Live-tree pointer verified: `.ufo/evidence/round-18/dispositions.json` is a v2 manifest over the same 13-pin expected.json with `historical_inputs` waivers for exactly the three drifted tools (mutate-and-run.sh, pin-disposition.py, bash-witness-study.py).
- All five trace receipts carry `rev` = b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a. Tool installs: none.


COLDREAD Read09B: executed-ok
