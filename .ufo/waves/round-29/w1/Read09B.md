# Read09B — cold read, SKILL.md "## Live-tree re-pin and entry-command monitor — round 17" (line 1814)

Read at lane rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 (detached clone in /tmp, fleet siblings symlinked beside it; SKILL.md sha256 c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6 matches the served value). Section spans lines 1814-1845 (next heading `### Round-17 gate/probe registry — re-pin and monitor` at line 1846, outside fences).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read09B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
 "sections": [{"start": 1814, "heading": "## Live-tree re-pin and entry-command monitor — round 17", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": [
  "registry-check full replay (49 active + 7 superseded rows, timeouts up to 900 s) not run verbatim — skipped under the >6-minute rule; the replay machinery was verified with --rev plus --only on one active and one superseded row, including the REGISTRY_CHECK: held=N/M superseded=K summary line.",
  "tools/evidence-disposition.py --selftest not run: the round-18 registry notes it now needs jj on PATH, and jj is forbidden for this seat; the named selftests v2-historical-replace-ref and v2-gitdir-env are present at tools/evidence-disposition.py:2910,2925 and the anchor-scrub code path was read at :368-390.",
  "the probe row's live-fleet invocation (pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin) was not run from this seat because it reads the live fleet root; covered instead by pin-disposition --selftest 19/19 including SELFTEST_CASE detached-head-uses-branch-tip, and by the gate's pin_live row passing.",
  "waiver-abuse exits (historical_input_unneeded, historical_input_forbidden, historical_input_uncommitted) not directly exercised; the same could-not-evaluate exit 2 was demonstrated by running both round-17 manifests through the round-18 gate, which failed on the round-18-moved tools/bash-witness-study.py (expected_input_digest_mismatch).",
  "S061's ¶2 paragraph anchor is flagged stale in corpus/SOURCES.md errata (S076: the detached-HEAD sentence is ¶3); the conclusion the section draws from S061 stands.",
  "'some rows write receipts into their root' corroborated by the external:true registry row pinning --root /home/vgpnk/Projects/shokunin and registry-check's docstring, not by observing a receipt write."
 ],
 "commands_executed": [
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json",
  "python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --only repeat-control-selftest",
  "python3 tools/registry-check.py --rev 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 --only evidence-disposition-round17-before",
  "python3 tools/pin-disposition.py --selftest",
  "python3 -c <record-read printing tools/evidence-disposition.py:359-395, GIT_* scrub lines of tools/registry-check.py, receipt mentions, GIT_* names in tools/bash-witness-study.py, repo_identity_mismatch in tools/mutate-and-run.sh, GIT_* handling in .ufo/evidence/round-16/measure.py>",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json",
  "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json"
 ],
 "opened": [
  ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/evidence/round-12/BashWitness/summary.json",
  ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/producer-before.py", ".ufo/evidence/round-13/producer-oracle-repair.json", ".ufo/evidence/round-13/producer-oracle.py", ".ufo/evidence/round-13/verification.json", ".ufo/evidence/round-13/witness-metadata-old-null.json", ".ufo/evidence/round-13/witness-metadata.json",
  ".ufo/evidence/round-14/dispositions-before.json", ".ufo/evidence/round-14/dispositions.json", ".ufo/evidence/round-16/measure.py",
  ".ufo/evidence/round-17/dispositions-before.json", ".ufo/evidence/round-17/dispositions.json", ".ufo/evidence/round-18/dispositions-before.json", ".ufo/evidence/round-18/dispositions.json",
  "corpus/SOURCES.md", "corpus/lessons/round-16-verifier-spotcheck.md",
  "tools/bash-witness-study.py", "tools/evidence-disposition.py", "tools/mutate-and-run.sh", "tools/pin-disposition.py", "tools/registry-check.py", "tools/registry.json", "tools/witness-metadata.py"
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
  ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
  ".ufo/evidence/round-17/dispositions-before.json": "79f0b397b727152b260df90e3ba9aa886d20eb7b5e5a43f6c3d03c7d3ee32354",
  ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
  ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
  ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
  "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
  "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
  "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
  "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
  "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
  "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
  "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
  "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
  "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
 },
 "external_inputs": {},
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-7.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-8.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read09B-9.json"
 ]}]}
```

What I checked, in plain English:

- Recipe step 1, verbatim: `evidence-disposition.py --dispositions .ufo/evidence/round-18/dispositions-before.json --json` exits 1 with `"status": "failed"` and exactly one finding carrying `"expectation": "producer_before"`. Matches.
- Recipe step 2, verbatim: same tool with `dispositions.json` exits 0, `"status": "clean"`, `"effective": 11`, `"superseded": 1`. Text mode (no `--json`) prints exactly 3 `HISTORICAL <path> rev=<rev> sha256=<sha>` lines, one per waived instrument (bash-witness-study.py, mutate-and-run.sh, pin-disposition.py, all pinned at 4acc607d). Matches.
- The step-1 parenthetical `(round 18; round 17's two now exit 2)`: ran both round-17 manifests through the same gate — both exit 2 `could_not_evaluate`, failing on `tools/bash-witness-study.py` `expected_input_digest_mismatch` (the round-18-moved tool absent from the round-17 manifests' historical_inputs). Matches.
- Recipe step 3: `registry-check.py --rev 9f3084bc… --only repeat-control-selftest` → `held=1/1 superseded=0`, exit 0; `--only evidence-disposition-round17-before` (a superseded row) → the row still ran, `expect=1 got=2`, `held=0/0 superseded=1`, overall exit 0. Confirms the summary-line format and the row-table claim "leaves active only as superseded with superseded_by, and still runs". The full unfiltered replay was skipped under the >6-minute rule.
- Recipe step 4 / probe row: `pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)` including `SELFTEST_CASE detached-head-uses-branch-tip`, supporting "branch tip, never HEAD". The live-fleet invocation was not run (it reads `/home/vgpnk/Projects/shokunin` live).
- Code-region claims: `tools/evidence-disposition.py:368-390` contains the G4 comment, `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null` and the inherited-`GIT_*` scrub in `git_environment()`; selftests `v2-historical-replace-ref` and `v2-gitdir-env` exist at :2910 and :2925. `tools/registry-check.py` scrubs every inherited `GIT_*` (:150-163) and has selftest legs exporting decoy `GIT_DIR`/`GIT_WORK_TREE` (:1084, :1120). `.ufo/evidence/round-16/measure.py` contains no `GIT_DIR`/`GIT_WORK_TREE`/`startswith("GIT_")` handling — the "still does not [scrub]" claim holds (its only GIT_* uses are envs it sets for its own commits). `repo_identity_mismatch` is present in `tools/mutate-and-run.sh`. `tools/bash-witness-study.py` carries `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_NOSYSTEM` env pins.
- Source rows: `corpus/SOURCES.md` rows S061 (jj colocated HEAD at the parent commit — conclusion stands, ¶2 anchor superseded by S076), S062 (`--show-toplevel`), S063 (repository discovery, `GIT_*` environment) match the section's glosses. `corpus/lessons/round-16-verifier-spotcheck.md` §3 and §6 carry the routed items R16-OP1 and R16-MON1 the section names.
- `tools/registry.json` at the rev: 56 rows, 49 active / 7 superseded; the round-17 disposition rows are marked `superseded` with `superseded_by` naming the round-18 rows — consistent with the section's supersession rule.

Auxiliary commands run outside the collector (clone/checkout, `git show` hashes for the inputs map, `grep`/`sed` reconnaissance reads of the lane files listed in `inputs`); none of them touched the live lane or fleet repos. No tooling installs were needed. No sibling or exempt-file reads, so `external_inputs` is empty.

COLDREAD Read09B: executed-ok
