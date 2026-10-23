# Coldread ColdA02 — SKILL.md sections 4, 5, 6 at 2da841bd9913a2037d2bf612793382e572c9d205

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdA02",
  "skill_sha256": "2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a",
  "read_rev": "2da841bd9913a2037d2bf612793382e572c9d205",
  "sections": [
    {
      "start": 1517,
      "heading": "## Pin disposition and provenance correction — round 13",
      "class": "instruction",
      "verdict": "gap-minor",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Recipe step 2 is written with `--root /home/vgpnk/Projects/shokunin` (the live fleet root). Reading the live lane during traces is prohibited by this assignment, so I ran the identical command against my fleet-mirror root (lane clone plus sibling clones) instead; command semantics are unchanged.",
        "The first mirror run (trace 4-1) had sibling repos symlinked; pin-disposition.py refuses symlinked repos by design (`repo_symlink`), so all six legs reported `unavailable`. After cloning the four needed siblings (kumitate, kagi, tsukuroi, mado) into the mirror, the rerun (trace 4-4) produced a full disposition: 6 legs, pinned verification for all six, unchanged=1, changed=5, unavailable=0.",
        "The probe observes mirror clones' branch tips, not live fleet state; the dated-reading semantics of the recipe (retain stdout with sibling branch-tip commits) still hold because every leg row records `head.commit`."
      ],
      "commands_executed": [
        "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /fast/scratch/hyaku/tameshi-r31-seats/ColdA02/fleet",
        "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
        "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/incremental-pin-disposition.md corpus/lessons/round-12-verifier-spotcheck.md .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/witness-metadata.json"
      ],
      "opened": [
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/lessons/round-12-verifier-spotcheck.md",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        "tools/pin-disposition.py",
        "tools/witness-metadata.py"
      ],
      "inputs": {
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-4-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-4-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-4-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-4-4.json"
      ]
    },
    {
      "start": 1548,
      "heading": "### Round-13 gate/probe registry",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" tools/pin-disposition.py tools/witness-metadata.py .ufo/evidence/round-13/pin-manifest.json .ufo/evidence/round-13/witness-metadata.json .ufo/evidence/round-13/expected.json"
      ],
      "opened": [
        "tools/pin-disposition.py",
        "tools/witness-metadata.py",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-13/expected.json"
      ],
      "inputs": {
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-5-1.json"
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
        "Recipe step 3 (`python3 tools/registry-check.py --rev <40-hex lane commit>`) replays every row of tools/registry.json, including long selftests. A traced attempt with `timeout 320` was killed by the harness at 340s before a receipt was written, and an untraced probe with `timeout 240` exited 124 (did not finish within 4 minutes). It therefore needs more than the 6-minute bound, so it was skipped per the instruction; the registry file itself was read and its rows match the section's stated instrument set (round-13 pin/witness rows, round-17/18 evidence-disposition rows, registry-check row).",
        "Recipe step 2 says text mode prints one `HISTORICAL <path> rev=<rev> sha256=<sha>` line per waived instrument; I ran `--json` and verified the equivalent `historical_text` array (exactly 3 entries: tools/bash-witness-study.py, tools/mutate-and-run.sh, tools/pin-disposition.py at 4acc607dfd79f19d508bd50cdd06b77269fccd1d).",
        "The `--rev` placeholder was filled with the reviewed revision 2da841bd9913a2037d2bf612793382e572c9d205."
      ],
      "commands_executed": [
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
        "python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json",
        "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/lessons/round-16-verifier-spotcheck.md corpus/SOURCES.md tools/evidence-disposition.py tools/registry.json tools/pin-disposition.py"
      ],
      "opened": [
        "corpus/lessons/round-16-verifier-spotcheck.md",
        "corpus/SOURCES.md",
        "tools/evidence-disposition.py",
        "tools/registry.json",
        "tools/pin-disposition.py",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/producer-before.py",
        ".ufo/evidence/round-13/producer-oracle.py",
        ".ufo/evidence/round-13/producer-oracle-repair.json",
        ".ufo/evidence/round-13/verification.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-13/witness-metadata-old-null.json",
        ".ufo/evidence/round-14/dispositions-before.json",
        ".ufo/evidence/round-14/dispositions.json",
        ".ufo/evidence/round-18/dispositions-before.json",
        ".ufo/evidence/round-18/dispositions.json",
        "tools/bash-witness-study.py",
        "tools/mutate-and-run.sh",
        "tools/witness-metadata.py"
      ],
      "inputs": {
        "corpus/lessons/round-16-verifier-spotcheck.md": "5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37",
        "corpus/SOURCES.md": "489ee8af2ddc835afb4988e311be20aba6638de9ed407f8c440691516311a741",
        "tools/evidence-disposition.py": "39ee5c5effd9bbdaafda644aada0cdb008ddee1dbfee4ac6bea93fc5a1fe51c8",
        "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
        "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
        "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/producer-before.py": "592c5c3de86a684fbb694d3aa8dd4c1e2b62263e7a50d72a9169092ad3fab9a0",
        ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
        ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
        ".ufo/evidence/round-13/verification.json": "a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
        ".ufo/evidence/round-14/dispositions-before.json": "a7a965bbf0f28a1ed2951c1f762f16d1957aab0b95b1384e2b4ab801e0a89725",
        ".ufo/evidence/round-14/dispositions.json": "77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005",
        ".ufo/evidence/round-18/dispositions-before.json": "dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65",
        ".ufo/evidence/round-18/dispositions.json": "9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-6-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-6-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-31/coldread/traces/ColdA02-6-4.json"
      ]
    }
  ]
}
```

## Plain-English note

I read the three sections at 2da841bd9913a2037d2bf612793382e572c9d205 from a detached fleet-mirror clone; SKILL.md at that rev hashes to the stated 2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a, and all trace receipts record rev 2da841bd..., exit codes, and argv equal to what I ran, with no live-lane reads and no external input reads.

Section 4 (instruction): both named recipe commands ran under the trace collector. `witness-metadata.py --check` exited 0 `metadata_consistent`; `pin-disposition.py` exited 0 and emitted a valid six-leg disposition, but the literal `--root /home/vgpnk/Projects/shokunin` form was not run (reading the live lane during traces is prohibited), and a symlinked sibling mirror made the first run report all `unavailable` (`repo_symlink` refusal); after cloning the four needed siblings, the rerun verified all six pins and reported unchanged=1, changed=5. Source claims (S003/S047, routed defect item 3, manifest values) check out against the opened knowledge file, lesson, and manifest.

Section 5 (record): both registry rows match the actual tools, commands (the entry commands are byte-identical to what section 4 executed), verdict maps, selftest labels, pinned values (manifest and `expected.json` contents), read-only write scope, and owner; no discrepancy found.

Section 6 (instruction): recipe steps 1 and 2 reproduced exactly: `dispositions-before.json` → exit 1 failed with only `producer_before` unresolved; `dispositions.json` → exit 0 clean, effective=11, superseded=1, with the three `HISTORICAL` entries at 4acc607. The git-scrub claim at tools/evidence-disposition.py:368-390 is byte-verified, and the branch-tip reading claim is verified in pin-disposition.py source (branch resolution + `head_differs_from_branch`) and in my run (branch=master resolved). Sources S061/S062/S063 and the round-16 lesson §3/§6 (R16-OP1, R16-MON1) are present with matching content. Recipe step 3 (registry-check) could not complete within the allowed time (traced attempt killed at 340s before writing a receipt; untraced probe exit 124 at 240s), so it is reported as skipped per the >6-minute rule; the registry file itself was read and matches the stated instrument set.

No tools were installed or updated; no production files were edited; no git write or jj command was run; no processes from this seat are left running.

COLDREAD ColdA02: gap-minor, verified-record, gap-minor
