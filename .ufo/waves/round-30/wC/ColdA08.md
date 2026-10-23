# ColdA08 — cold reads, sections 22–24 of SKILL.md @ bb681566

Clone: `/tmp/ColdA08-Uc3O/fleet/tameshi-shokunin`, detached at `bb681566b18211adf8ae9c28df91e17678e3f545`; SKILL.md sha256 matches the pinned `c46ec02e…`. Every command below ran under `tools/trace-inputs.py` with its receipt in `.ufo/evidence/round-30/coldread/traces/`; all receipts carry `rev=bb681566…` and `live_lane_reads={}`.

```json
{
 "schema": "tameshi-coldread-report-v2",
 "seat": "ColdA08",
 "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6",
 "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
  {
   "start": 1754,
   "heading": "## Seventh recorded case and full-page cold-read — round 16",
   "class": "instruction",
   "verdict": "executed-ok",
   "blocking_gaps": [],
   "wrong_expectations": [],
   "minor_gaps": [],
   "commands_executed": [
    "bash -c 'W=$(mktemp -d /tmp/tameshi-r16-rg.XXXXXX); git -C /tmp/ColdA08-Uc3O/fleet/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > \"$W/round-gate.mjs\"; sha256sum \"$W/round-gate.mjs\"; E=.ufo/evidence/round-16/round-gate; bash tools/mutate-and-run.sh --target \"$W/round-gate.mjs\" --defects \"$E/round-gate.defects.spec\" --suite \"$(cat \"$E/suite.txt\")\" --label js-round-gate --workdir \"$W/work\"'"
   ],
   "opened": [
    ".ufo/evidence/round-16/measure.py",
    ".ufo/evidence/round-16/round-gate/round-gate.defects.spec",
    ".ufo/evidence/round-16/round-gate/runner-regression.txt",
    ".ufo/evidence/round-16/round-gate/runner-selftest.txt",
    ".ufo/evidence/round-16/round-gate/runner-sha256.txt",
    ".ufo/evidence/round-16/round-gate/suite.txt",
    ".ufo/evidence/round-16/round-gate/survivor-probes/A2-P1-mutant-A2.log",
    ".ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs",
    "corpus/knowledge/mutation-case-kumitate-round-gate.md",
    "tools/mutate-and-run.sh"
   ],
   "inputs": {
    ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
    ".ufo/evidence/round-16/round-gate/round-gate.defects.spec": "e99b87ebc16f045f43ffb31354e2fc2879d2be3a8504d4274239249b93ef11c4",
    ".ufo/evidence/round-16/round-gate/runner-regression.txt": "630c3806e106af550d4afc6cd79bf2b0846472530a33772038df443db6e591e4",
    ".ufo/evidence/round-16/round-gate/runner-selftest.txt": "1df28c867553a3ec48107b69c44714298537e5744bb44a973d620a68fbbf5505",
    ".ufo/evidence/round-16/round-gate/runner-sha256.txt": "9758a1d89fd301dd93095a611eb1738a9a9afeebba2c6dbe28cfdbb04a764d99",
    ".ufo/evidence/round-16/round-gate/suite.txt": "6e550d5a2f6a78fc0654c297b80bb042e8482423d80e2e16bab7374227931f7b",
    ".ufo/evidence/round-16/round-gate/survivor-probes/A2-P1-mutant-A2.log": "d68693431369b93296051bfe9817f20e59cd661e68be9c3898db5a325f7f4ca0",
    ".ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs": "131c2835b1b5ce5fab60960fbca864c444d2cd75c19f08da410616e49bd332fb",
    "corpus/knowledge/mutation-case-kumitate-round-gate.md": "1b907c8d2c756134783604b604b3dd0a65b0a5fcb0f5a82e5d24b037b82aeaec",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"
   },
   "external_inputs": {
    "kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs": "f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9",
    "tameshi-shokunin@e69b488f65b17bcfd41949abf7d538a77678dc26:.ufo/evidence/round-16/round-gate/predictions.json": "bb344eee3b034d774a829042717dc5c78517edcf8ef5f369831bc2fae0f70bc1"
   },
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-22-1.json"
   ]
  },
  {
   "start": 1806,
   "heading": "### Round-16 gate/probe registry",
   "class": "record",
   "verdict": "gap-minor",
   "blocking_gaps": [],
   "wrong_expectations": [],
   "minor_gaps": [
    "mutate-and-run.sh --regression not run end to end (replays nine sibling git legs, exceeds the 6-minute bound); its exit map was exercised piecewise inside --selftest (PASS/FAIL/SETUP tally vectors, case-tally mismatch, 64 usage) and cases=9 confirmed statically (nlegs=9, nine embedded specs)"
   ],
   "commands_executed": [
    "bash tools/mutate-and-run.sh --selftest",
    "python3 .ufo/evidence/round-16/measure.py --selftest",
    "python3 .ufo/evidence/round-16/coldread/assemble.py --selftest",
    "python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest",
    "python3 .ufo/evidence/round-16/measure.py --rev bb681566b18211adf8ae9c28df91e17678e3f545"
   ],
   "opened": [
    ".ufo/evidence/round-15/verification-3.json",
    ".ufo/evidence/round-16/attribution/reattribute.py",
    ".ufo/evidence/round-16/coldread/assemble.py",
    ".ufo/evidence/round-16/measure.py",
    "tools/mutate-and-run.sh"
   ],
   "inputs": {
    ".ufo/evidence/round-15/verification-3.json": "3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce",
    ".ufo/evidence/round-16/attribution/reattribute.py": "eaf564e42629634e21bc2ee1aa70932a1024d721eba664f8ed892640590015c1",
    ".ufo/evidence/round-16/coldread/assemble.py": "9ee9264aabe9f474b4ecf7cfa52b4d50274ee4a6b82d06df36812a006eb0a156",
    ".ufo/evidence/round-16/measure.py": "03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"
   },
   "external_inputs": {},
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-23-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-23-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-23-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-23-4.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-23-5.json"
   ]
  },
  {
   "start": 1814,
   "heading": "## Live-tree re-pin and entry-command monitor — round 17",
   "class": "instruction",
   "verdict": "gap-minor",
   "blocking_gaps": [],
   "wrong_expectations": [],
   "minor_gaps": [
    "recipe step 3 (tools/registry-check.py --rev) replays 56 registry rows each cloning the lane; it did not finish inside 75 s (exit 124 under timeout, receipt ColdA08-24-3) or 330 s, so it is skipped per the 6-minute bound; its ending line shape REGISTRY_CHECK: held=N/M superseded=K and exit map verified in tools/registry-check.py:906, registry.json superseded rows carry superseded_by"
   ],
   "commands_executed": [
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
    "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json",
    "timeout 75 python3 tools/registry-check.py --rev bb681566b18211adf8ae9c28df91e17678e3f545"
   ],
   "opened": [
    ".ufo/evidence/round-12/BashWitness/declaration.json",
    ".ufo/evidence/round-12/BashWitness/declared.tsv",
    ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
    ".ufo/evidence/round-12/BashWitness/summary.json",
    ".ufo/evidence/round-13/expected.json",
    ".ufo/evidence/round-13/pin-manifest.json",
    ".ufo/evidence/round-13/producer-before.py",
    ".ufo/evidence/round-13/producer-oracle-repair.json",
    ".ufo/evidence/round-13/producer-oracle.py",
    ".ufo/evidence/round-13/verification.json",
    ".ufo/evidence/round-13/witness-metadata-old-null.json",
    ".ufo/evidence/round-13/witness-metadata.json",
    ".ufo/evidence/round-14/dispositions-before.json",
    ".ufo/evidence/round-14/dispositions.json",
    ".ufo/evidence/round-17/dispositions.json",
    ".ufo/evidence/round-18/dispositions-before.json",
    ".ufo/evidence/round-18/dispositions.json",
    "corpus/SOURCES.md",
    "corpus/lessons/round-16-verifier-spotcheck.md",
    "tools/bash-witness-study.py",
    "tools/evidence-disposition.py",
    "tools/mutate-and-run.sh",
    "tools/pin-disposition.py",
    "tools/registry-check.py",
    "tools/registry.json",
    "tools/witness-metadata.py"
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
    ".ufo/evidence/round-17/dispositions.json": "55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f",
    ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
    ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676",
    "corpus/SOURCES.md": "b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7",
    "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
    "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
    "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
    "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
    "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
    "tools/registry-check.py": "cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad",
    "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
    "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
   },
   "external_inputs": {},
   "traces": [
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-24-1.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-24-2.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-24-3.json",
    "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdA08-24-4.json"
   ]
  }
 ]
}
```

## What I checked

**Section 22 (lines 1754–1805, instruction) — `executed-ok`.** Ran the fenced "Reproduce it" recipe verbatim in the clone (only the sibling repo path points at the fleet mirror instead of `~/Projects/shokunin`). Materialized `round-gate.mjs` at `364f1d5…` — sha256 `f890e277…a834d3e9` exactly as printed. Sweep: `CONTROL: GREEN`, `MUTATE: DONE (… killed=5 survived=5 inconclusive=0 kill-rate=50%)`, `MUTATE_RESTORE: OK`, exit 0. Every outcome matched the spec's PREDICT markers (A1/A3/B1/E3/C1060 KILLED; C1059/A2/B2/CKIND/E1 SURVIVED — the 1059 edge survivor and 1060 kill reproduce the projected-interval claim). Predictions commit `e69b488` exists and predates the sweep; `predictions.json` is in it. Recorded `runner-regression.txt` shows `js-round-gate=5/10`, `cases=7 passed=7` at round 16 (the `cases=8`/`cases=9` history confirmed in the tool's leg ledger and selftest tallies). `coldread.box3_full_page` exists in `measure.py`; survivor-probes dir and `probes.mjs` exist; case note `corpus/knowledge/mutation-case-kumitate-round-gate.md` documents the 5/10 result.

**Section 23 (lines 1806–1813, record) — `gap-minor`.** All four registry rows' commands run: `mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 (its failure paths — exit 1, SETUP 2, usage 64 — exercised inside the selftest). `measure.py --selftest` 38/38 exit 0 and `--rev` measured exit 0 with `box3_full_page` (selftest also covers exit 2/64 arms). `assemble.py --selftest` exit 0, exercising exit 1 (uncovered bucket) and exit 2 (heading mismatch, invalid override) paths. `reattribute.py --selftest` exit 0 with old rule failing the oracle and the new rule passing. Sole gap: no end-to-end `--regression` run (too long); its behavior is corroborated by the recorded `runner-regression.txt` and the selftest's tally vectors.

**Section 24 (lines 1814–1845, instruction) — `gap-minor`.** Recipe steps 1–2 ran exactly as written on the clone: `dispositions-before.json` → exit 1, `"failed": 1`, the `producer_before` expectation unresolved via `expected_contains_missing`; `dispositions.json` → exit 0, `clean`, `"effective": 11`, `"superseded": 1`, three `HISTORICAL <path> rev=… sha256=…` lines (one per waived instrument). Bonus check: the round-17 manifest indeed exits 2 (`expected_input_digest_mismatch`) as the section claims. Table claims verified by code and runs: `GIT_NO_REPLACE_OBJECTS=1`/`GIT_GRAFT_FILE=/dev/null`/GIT_* scrub at `evidence-disposition.py:368-390`; selftest names `v2-historical-replace-ref`, `v2-gitdir-env` exist; `historical_input_unneeded`/`_forbidden`/`_uncommitted` tokens exist; `repo_identity_mismatch` SETUP-exit-2 arm confirmed by the mutate selftest's repo-identity cases; `pin-disposition.py` carries `branch`/`head_differs_from_branch`; SOURCES.md rows S061/S062/S063 exist; the lesson's §3 operability verdict and §6 routed items match. Gap: step 3 (`registry-check.py --rev`) could not finish within any bound I gave it (75 s and 330 s; it clones the lane per registry row and replays each row's command) — recorded honestly as a `timeout` run; its summary-line shape and exit map verified in source.

No tools installed; nothing else needed. All ten trace receipts named literally in their tracer commands, `rev` matches `read_rev`, no live-lane reads.

COLDREAD ColdA08: executed-ok, gap-minor, gap-minor
