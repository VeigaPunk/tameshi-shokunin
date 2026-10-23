# COLDREAD Read07A — round-29 wave 1

Seat: Read07A. Section: `## Effective expectation reconciliation — round 14`
(SKILL.md:1563–1596 at rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5, page
sha256 c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6).
Class: instruction (recipe tells a reader to run the disposition tool in two
trees). Verdict: executed-ok.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read07A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1563, "heading": "## Effective expectation reconciliation \u2014 round 14", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [],
  "commands_executed": [
    "bash -c 'mkdir -p /tmp/read07a-nQoV/archive28t && git -C /tmp/read07a-nQoV/fleet/tameshi-shokunin archive 28aeef4 | tar -x -C /tmp/read07a-nQoV/archive28t' (tracer exit 0)",
    "python3 -c 'import sys;[print(p, len(open(p).read())) for p in sys.argv[1:]]' corpus/lessons/round-13-verifier-spotcheck.md corpus/knowledge/incremental-pin-disposition.md corpus/SOURCES.md .ufo/evidence/round-13/expected.json .ufo/evidence/round-13/producer-oracle-repair.json .ufo/evidence/round-14/expected-outcomes.json .ufo/evidence/round-14/verification.json .ufo/evidence/round-14/verification-final.json .ufo/evidence/round-14/capture-context.py .ufo/evidence/round-14/context-receipt.json .ufo/evidence/round-14/dispositions-before.json .ufo/evidence/round-14/dispositions.json tools/trace-inputs.py .ufo/waves/round-26/w1/ColdreadPilot.md (exit 0)",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json (cwd=clone root; exit 2, id expected_input_digest_mismatch)",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json (cwd=clone root; exit 2, id expected_input_digest_mismatch)",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json (cwd=/tmp/read07a-nQoV/archive28t via tracer --cwd; exit 1, one finding: producer_before expected_contains_missing; supersedes an earlier identical argv launched without --cwd that ran the HEAD tool and exited 2)",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json (cwd=/tmp/read07a-nQoV/archive28t via tracer --cwd; exit 0, clean, superseded=1; supersedes an earlier identical argv launched without --cwd that ran the HEAD tool and exited 2)"],
  "opened": ["SKILL.md", "corpus/lessons/round-13-verifier-spotcheck.md", "corpus/knowledge/incremental-pin-disposition.md", "corpus/SOURCES.md", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-14/dispositions-before.json", ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-14/expected-outcomes.json", ".ufo/evidence/round-14/verification.json", ".ufo/evidence/round-14/verification-final.json", ".ufo/evidence/round-14/capture-context.py", ".ufo/evidence/round-14/context-receipt.json", "tools/evidence-disposition.py", "tools/trace-inputs.py", "tools/mutate-and-run.sh", "tools/pin-disposition.py", "tools/witness-metadata.py", "tools/bash-witness-study.py", ".ufo/waves/round-26/w1/ColdreadPilot.md"],
  "inputs": {
    "corpus/lessons/round-13-verifier-spotcheck.md": "6b8d2cafdab33c72", "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e7", "corpus/SOURCES.md": "804f0b4369e87fa8",
    ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336", ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d", ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f", ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6", ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0", ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b", ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d", ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9", ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901", ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725", ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005", ".ufo/evidence/round-14/expected-outcomes.json": "e7803c1e76980a4d8c7d89ffbab49a32e307f98b98e216a490f6d103c20e5d85", ".ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939", ".ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2", ".ufo/evidence/round-14/capture-context.py": "7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89", ".ufo/evidence/round-14/context-receipt.json": "05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8", "tools/trace-inputs.py": "f59c9312c56eb458", "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9", "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c", "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
    ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e"},
  "external_inputs": {
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/evidence-disposition.py": "1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/bash-witness-study.py": "49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/pin-disposition.py": "297253971dab3a558b470a04162b9d768287844dc0e81bf41a1f9f263ff14f11",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/expected-outcomes.json": "e7803c1e76980a4d8c7d89ffbab49a32e307f98b98e216a490f6d103c20e5d85",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/verification.json": "1d480a0ddd0cd8a801d0ae38f7d774b6d772c8d0910bf6200c3e666696532939",
    "tameshi-shokunin@28aeef498cc070c3183271b709bc79d344ff547a:.ufo/evidence/round-14/verification-final.json": "e904e6938a123de55db492f7d04c1e18087c1783128ab9ed96e55d93c3ef52f2"},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07A-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07A-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07A-3.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07A-4.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07A-5.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read07A-6.json"]}]}
```

## What I checked

Fleet-mirror clone at `/tmp/read07a-nQoV/fleet/tameshi-shokunin`, detached at
9f3084bc; SKILL.md sha256 matches the pinned page digest. The section runs
1563–1596 (ends before `### Round-14 historical registry` at 1597).

Step 1: `dispositions-before.json` and `dispositions.json` each carry exactly
12 rows; `expected.json`'s `inputs` block pins 13 inputs — the "twelve
expected rows from thirteen pinned inputs" distinction is real and
observable.

Step 2: at `--root .` on the HEAD checkout both manifests exit 2 with
`id: expected_input_digest_mismatch`. One nuance worth recording: the gate
reports the first drifted pin, `tools/bash-witness-study.py` (observed
60575e62… vs pinned 49e9e5e2…), and stops; `tools/mutate-and-run.sh` is also
drifted (fb91ef76… vs pinned 75ed934d…) but is never reached. The runner id
`75ed934d…` in the section is the sha256 pin of `tools/mutate-and-run.sh`,
not a git object — `git cat-file -t 75ed934d` fails, matching it requires the
expected.json pin. Both drifted files are consistent with the runner-move
explanation (round-16 refactor).

Step 2 replay: `git archive 28aeef4` extracted (traced, receipt 1); inside
that tree, `python3 tools/evidence-disposition.py --root . --dispositions
.ufo/evidence/round-14/dispositions-before.json --json` → exit 1, exactly one
finding `expected_contains_missing` on `producer_before` (the unresolved
assertion), 11 pass, 0 superseded. Step 3: same argv with `dispositions.json`
→ exit 0, clean, `superseded: 1`, raw receipt/check retained, both oracle
replacements `pass`. The archive tool itself is the r14 byte pin
(1609a9df…), and every file it read inside the tree matches its pinned
digest — replay fidelity is byte-exact.

Step 4: `verification-final.json` retains the corrected selftest (34
SELFTEST_CASE lines, 0 FAIL, exit 0) plus frozen before/after runs with a
separate `measured_commit` (6431478…); `verification.json` retains the
initial failures — I counted 34 SELFTEST_CASE lines, 18 FAIL lines:
"18-of-34" is literal.

Step 5: `capture-context.py` declares `OUTPUT_REL =
.ufo/evidence/round-14/context-receipt.json` — running it would overwrite the
frozen receipt; correctly archived, not run. The round-15 registry's
maintained retained-only gate (`tools/context-capture.py --check`) exists at
line 1678ff as pointed.

Sources cited: `corpus/lessons/round-13-verifier-spotcheck.md` Routed defects
1–3 exist (defect 1 = stale `producer_before` expected row needing explicit
supersession; defect 2 = retained GIT_DIR row lacking injected-env record;
defect 3 = pre-integration knowledge §6 needing an empirical backlink) and
map onto the section's table rows and recipe steps. S049 is the official
Python subprocess `run()` env paragraph — the "Python child-environment
contract". S003's row names §Limitations (env vars/dependencies/.snap blind
spots). `corpus/knowledge/incremental-pin-disposition.md` §8 "Empirical
correction and backlink — round 14" exists and records exactly this
correction (18-of-34 retained, supersession wording). No blocking or wrong
expectation found; the one fidelity detail above (first-reported pin names
bash-witness-study.py, mutate-and-run.sh also drifted) is left in prose
rather than minor_gaps since the claim as written — exit 2,
expected_input_digest_mismatch, runner moved in round 16 — is what the gate
does.

Bounds: no production edits, no git writes in the lane, no `jj`, no live-lane
reads under trace (all receipts `live_lane_reads={}`); archive extraction and
replays ran inside `/tmp/read07a-nQoV` only. No tools installed.

COLDREAD Read07A: executed-ok
