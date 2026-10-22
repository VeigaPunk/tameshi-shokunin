# Read09A — cold read, SKILL.md "## Effective expectation reconciliation — round 14" (lines 1563–1596)

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read09A",
  "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6",
  "read_rev": "b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a",
  "sections": [
    {
      "start": 1563,
      "heading": "## Effective expectation reconciliation — round 14",
      "class": "instruction",
      "verdict": "executed-ok",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-13-verifier-spotcheck.md corpus/knowledge/incremental-pin-disposition.md .ufo/evidence/round-14/verification-final.json .ufo/evidence/round-14/verification.json .ufo/evidence/round-14/dispositions.json .ufo/evidence/round-14/dispositions-before.json",
        "bash -c 'cd /tmp/Read09A-L9uR/extract && exec python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json'",
        "bash -c 'cd /tmp/Read09A-L9uR/extract && exec python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json'",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json"
      ],
      "opened": [
        "corpus/lessons/round-13-verifier-spotcheck.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/SOURCES.md",
        ".ufo/evidence/round-14/verification-final.json",
        ".ufo/evidence/round-14/verification.json",
        ".ufo/evidence/round-14/dispositions.json",
        ".ufo/evidence/round-14/dispositions-before.json",
        ".ufo/evidence/round-14/context-missing-env.json",
        ".ufo/evidence/round-14/context-receipt.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/verification.json",
        ".ufo/evidence/round-13/producer-oracle-repair.json",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/producer-before.py",
        ".ufo/evidence/round-13/producer-oracle.py",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-13/witness-metadata-old-null.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        "tools/evidence-disposition.py",
        "tools/bash-witness-study.py"
      ],
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
        ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
        ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
        ".ufo/evidence/round-14/context-missing-env.json": "1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208",
        ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
        ".ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2",
        ".ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72f71a10ecc275865f74e2cd0331257264ef4ec8d6e9080420",
        "corpus/SOURCES.md": "a1624b7faaf17353d869ccf33cc811e53978e87115871cb449837561c3f85a45",
        ".ufo/evidence/round-14/context-missing-env.json": "9a3a3f9b5a62c1e5a0cf4a0a4b4f7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b",
        "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
        "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8"
      },
      "external_inputs": {
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/evidence-disposition.py": "1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
        "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09A-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09A-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09A-2b.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09A-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09A-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-28/coldread/traces/Read09A-5.json"
      ]
    }
  ]
}
```

## What I checked

Section class: `instruction` (the numbered recipe names runnable commands; the table is a record-style decision matrix that the recipe operationalizes).

- Extracted `git archive 28aeef4` (rev `28aeef498cc070c3183271b709bc79d344ff547a`) into `/tmp/Read09A-L9uR/extract` and replayed the recipe's exact command there.
- `dispositions-before.json` in the archive → exit 1, `status: failed`, with exactly the named unresolved `producer_before` assertion failing (`expected_contains_missing`); observed exit 1 alone did not save it — matches step 2's claim.
- `dispositions.json` in the archive → exit 0, `status: clean`; `producer_before` row is `state: superseded`, `raw_retained: true`, `raw_mismatches: [expected_contains_missing]`, and both declared replacements (`producer_before_oracle` exit 1 pass, `producer_after_oracle` exit 0 pass) are effective — matches step 3's claim that the only repair is that row's explicit supersession.
- At lane `--root .` both manifests → exit 2 with `expected_input_digest_mismatch` on `tools/bash-witness-study.py` (observed `60575e62…`, expects `49e9e5e2…`) — matches step 2's "both manifests now return 2" claim; the live `tools/evidence-disposition.py` (`39ee5c5e…`) differs from the archive `1609a9df…`, consistent with "the runner moved in round 16" (the pinned tool bytes are what flag mismatch).
- `verification.json` retains the initial selftest `18/34` fixture failure lines inside the `disposition_selftest` check stdout plus the real before/after outcomes; `verification-final.json` retains the corrected selftest and `supersedes: "verification.json disposition_selftest failure only"` — matches step 4.
- `context-receipt.json` records the explicit child override (`environment.injected_env = {GIT_DIR: /nonexistent/tameshi-round14-poison}`); `context-missing-env.json` is the earlier receipt lacking the injected-env field — consistent with the "new context experiment explicitly records its child override" and "one GIT_DIR injection" table rows; no general hermeticity claim is made by the section.
- Step 5's `capture-context.py` was not run (as the recipe requires); no sibling gate executed.
- Citations resolve: `corpus/lessons/round-13-verifier-spotcheck.md` has "## Routed defects and residuals" with items 1–5 (items 1–3 match the table rows); `corpus/SOURCES.md` at this rev carries S049 (Python subprocess env contract, "round-14 Python child-environment contract, not historical setup proof") and S003 (StrykerJS incremental, §Limitations names env/dependencies/.snap blind spots); `corpus/knowledge/incremental-pin-disposition.md` carries section "## 8. Empirical correction and backlink — round 14" (correction 8).
- `expected.json` has 12 `expected_checks` and 13 pinned `inputs` — matches step 1's "twelve expected rows from thirteen pinned inputs".

All executed commands produced the outcomes the section predicts; no wrong expectations, no gaps found. One caveat noted, not a gap: the replay commands read archive-revision bytes under `/tmp` (outside the trace root), so those opens do not appear in the trace `inputs`; they are recorded under `external_inputs` with the archive revision and sha256 of the bytes read. Traces Read09A-2 and Read09A-2b are the same replay run twice (2b captured the failing row detail); all receipts carry `rev = b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a` and `live_lane_reads = {}`. Tool installs/updates: none.

COLDREAD Read09A: executed-ok
