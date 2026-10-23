# ColdB06 — wave C cold reads (round-12/13 registry sections)

Mirror clone at `/tmp/ColdB06-Om3B/fleet` (siblings symlinked, tameshi cloned,
detached at bb681566b18211adf8ae9c28df91e17678e3f545; SKILL.md sha256 matches the
assigned c46ec02e…d6d). All traced receipts record `rev=bb681566…`, `exit=0`,
`live_lane_reads={}`.

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "ColdB06",
  "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6",
  "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
  "sections": [
    {
      "start": 1499,
      "heading": "### Gate/probe registry",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "The repeat-control verdict-map cell labels exit 0 'clean' and exit 1 'failed'; the tool's literal finding IDs are controls_match and controls_mismatch (tools/repeat-control.py:122; selftest output 'expected=controls_match/0', 'expected=controls_mismatch/1'). The exit numbers are right; the labels are loose."
      ],
      "commands_executed": [
        "python3 -c \"import sys;[(open(p).read()[:200000]) for p in sys.argv[1:]]\" .ufo/evidence/round-12/ControlGate/expected.json .ufo/evidence/round-12/ControlGate/mismatch/expected.json .ufo/evidence/round-12/BashWitness/declaration.json .ufo/evidence/round-12/BashWitness/declared.tsv .ufo/evidence/round-12/BashWitness/manifest.json",
        "python3 tools/bash-witness-study.py count",
        "python3 tools/repeat-control.py --selftest"
      ],
      "opened": [
        ".ufo/evidence/round-12/ControlGate/expected.json",
        ".ufo/evidence/round-12/ControlGate/mismatch/expected.json",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/manifest.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-12/BashWitness/sweep/results.tsv",
        "tools/repeat-control.py",
        "tools/bash-witness-study.py",
        "tools/mutate-and-run.sh",
        "SHONEN.md",
        "corpus/lessons/round-1-verifier-spotcheck.md",
        ".ufo/waves/round-27/w1/Read25.md"
      ],
      "inputs": {
        ".ufo/evidence/round-12/ControlGate/expected.json": "1b645be04d756c304a1ef5ecc221cf92f82c5f4afbdcfde4b77fe27117684aa1",
        ".ufo/evidence/round-12/ControlGate/mismatch/expected.json": "57f010e99e69a6632869c125229f8bcf0cfdaf866b6dcab9f16ed07ebc8f6771",
        ".ufo/evidence/round-12/ControlGate/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
        ".ufo/evidence/round-12/ControlGate/run-1.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
        ".ufo/evidence/round-12/ControlGate/run-1.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
        ".ufo/evidence/round-12/ControlGate/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
        ".ufo/evidence/round-12/ControlGate/run-2.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
        ".ufo/evidence/round-12/ControlGate/run-2.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
        ".ufo/evidence/round-12/ControlGate/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
        ".ufo/evidence/round-12/ControlGate/run-3.stderr": "05493420167e5e70d5fa9fa15420ad3861d936624ffe54848f183a03339264e1",
        ".ufo/evidence/round-12/ControlGate/run-3.stdout": "beee36e76df6089b6c1517fb582094e009c564424f61ae6d15020d08dd5faa3a",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-1.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-1.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-2.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-2.stdout": "5223d0557d70eaaa8555c648e04c01d463e4572853f782100b7afb15b3f2b6c8",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-3.exit": "9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stderr": "077f93c0194d67a870899e531b1903c62005610d8606525151ca1c95703f3096",
        ".ufo/evidence/round-12/ControlGate/mismatch/run-3.stdout": "b52929a30ae03d121fdd499fa74bd6ec58f06ebbc802c53c3b1918e67916b539",
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/manifest.json": "273ffc39308a6c55bdb1c8f7a86bac9f95886ec470773c99b4d1e2db5b25e1cf",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B1.out": "4552e10bbd12c7f271f725bf4829c3738e32d4dfe1d7c89881f5f0b7a250eace",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B10.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B2.out": "879b7d8e2cf90d13e4823e02e6130187bb072c77582a55b6bed129244c1675ee",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B3.out": "38737f1f34733faabba3dda448c7e380b90a380157d7a89a757f2d3d660b0868",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B4.out": "cca77bd91adfe019a8ef26e931c98ac21eaf0e13b607faad6b9014bba20e1ff4",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B5.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B6.out": "0691009001b8c808f60cb9a90a9481455d023106a1a14e8eb2197bee32ab37f3",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B7.out": "c76b809c8262c9ba3f715f63e594f5e06a1e4591da8ee8538fb963e1d8736884",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B8.out": "e972da147adbdbe7df0be252e981fdca3b772c972f338abefd8c92c06856beca",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/B9.out": "468723a0be9a5bcd716ea6c69fb3bb399b3f9a2a8bbf94267b773abc8f615e75",
        ".ufo/evidence/round-12/BashWitness/sweep/evidence/control.out": "09c21ee26b8b8b16618fe68a30043c612811da6bf008840a7a85bd3bce8a2fca",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B1.pristine.sh": "1d0e511055a74b11307d827913d264d87f43b93e21fdb679556439d96a4ca3cc",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B10.pristine.sh": "001b757454954cfac740530139d1416dc26e9dc40c2f7cd1c0e51bbbf2354bbd",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B2.pristine.sh": "443ce1fdd35e1a0de2c42ef809d30beef68252ba80972f67c681cc8760a908b3",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B3.pristine.sh": "5efd188121f8e7b9fb100caa27b973cb4603e1b6157fbf13c4b100a86603ba3d",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B4.pristine.sh": "c5f3b2b9d479fbf37aa28216d58f5f97220405cf0a140eef42409e0e97201a72",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B5.pristine.sh": "1e4ea1a6552f65895dd769d733a6c32e590503c0850a74cd3196cd05e2d0b95c",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B6.pristine.sh": "627a037aaa27104f286acc9220d176dd45df5fe9e1371fc418962d98af793c54",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B7.pristine.sh": "0c920258f41e6367f0a00b8b51d319372875b1d27b68b8e47a5702a286a31aaa",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B8.pristine.sh": "cce2b52381d0faed40ed7adc8f63f8d9a08d631ed7812357e8aec5ca757b47fa",
        ".ufo/evidence/round-12/BashWitness/sweep/mutant-B9.pristine.sh": "e1ee079ac2f3db7ed5f57f2b3d33c732f7913880e18dd91d5128f086d63a10ad",
        ".ufo/evidence/round-12/BashWitness/sweep/results.tsv": "6399660d94162245ef4d5011796e4f52c01ca61767865789049da2c5ee853fb9",
        "tools/repeat-control.py": "296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25",
        "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
        "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
        "SHONEN.md": "55a4fceb62b0a8f688f21beeb25003ccbb9d24caa3e03aad586799a09fd32e09",
        "corpus/lessons/round-1-verifier-spotcheck.md": "f99ef0ae2b3a3e4939c86b9ce5ab1e701733801c1cc1c7063767edf692e0edad",
        ".ufo/waves/round-27/w1/Read25.md": "6e6b3cca20d1fa6db9230f2a38a3398a8038b477b98a5edc86783e44f9e3e173"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB06-17-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB06-17-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB06-17-3.json"
      ]
    },
    {
      "start": 1517,
      "heading": "## Pin disposition and provenance correction — round 13",
      "class": "instruction",
      "verdict": "executed-ok",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "Step 2's printed --root is the live fleet root; per the wave bounds I ran the same command with --root pointed at my scratch mirror instead. On a mirror whose siblings are symlinks, all six legs correctly report 'unavailable' with reason 'repo_symlink' and exit stays 0 — the recipe's own 'unavailable, with reason' row describes exactly this outcome, and result_reuse stayed 'not_established' everywhere."
      ],
      "commands_executed": [
        "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /tmp/ColdB06-Om3B/fleet",
        "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json"
      ],
      "opened": [
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        "tools/pin-disposition.py",
        "tools/witness-metadata.py",
        "corpus/SOURCES.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/lessons/round-12-verifier-spotcheck.md"
      ],
      "inputs": {
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
        "corpus/SOURCES.md": "b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB06-18-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB06-18-2.json"
      ]
    },
    {
      "start": 1548,
      "heading": "### Round-13 gate/probe registry",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [
        "The pinned .ufo/evidence/round-13/expected.json still expects 'SELFTEST: PASS (18/18)' for pin_selftest; the tool at this revision runs and reports 19 cases ('SELFTEST: PASS (19/19)'). The frozen receipt is a historical record of the earlier tool revision, not a false claim of the section, so it is noted only as a minor gap."
      ],
      "commands_executed": [
        "python3 tools/pin-disposition.py --selftest",
        "python3 tools/witness-metadata.py --selftest"
      ],
      "opened": [
        "tools/pin-disposition.py",
        "tools/witness-metadata.py",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        "corpus/SOURCES.md",
        "tools/mutate-and-run.sh"
      ],
      "inputs": {
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        "corpus/SOURCES.md": "b830d6fa03699f15bcfaeb7579899d247284b7a85a17e7ddb61a979a451007c7",
        "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9"
      },
      "external_inputs": {},
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB06-19-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB06-19-2.json"
      ]
    }
  ]
}
```

## What I checked

**Section 17 (`### Gate/probe registry`, record → verified-record).**
`repeat-control.py --selftest` printed `SELFTEST: PASS (29 cases)` with exit 0,
and its output confirms the claimed exit map end-to-end: `controls_match`/0,
`controls_mismatch`/1, `baseline_nonzero`/`command_unavailable`/`snapshot_tampered`/2,
`invalid_usage`/64 — matching the row's "0 clean; 1 failed; 2 and 64
could-not-evaluate" up to the loose label wording (flagged minor). The pinned
ControlGate snapshots hold exactly the IDs the table implies (`controls_match`
exit 0, `controls_mismatch` exit 1). `bash-witness-study.py count` exits 0 with
`witness_classified=10`, `unresolved none`, killed 8 / survived 2 — and its
trace input list never contains `tools/mutate-and-run.sh`, empirically
confirming the paragraph's "count never reads the runner". The stale-pin claim
holds at this revision: the manifest and declaration pin runner sha256
`75ed934d…`, while the live `tools/mutate-and-run.sh` at bb681566 hashes
`a7d3f2dd…` (Read25.md, also present and cited correctly, records the same
DRIFT finding at the earlier revision `fb91ef76…`). The "not blind" claim is
verbatim in `declaration.json`'s disclosure, which names the target, spec,
aggregate outcomes and per-defect entries the author had seen. The calibration
correction is accurate: SHONEN.md box 3 currently shows `[~]`, and
`corpus/lessons/round-1-verifier-spotcheck.md` indeed does not credit the
box-3 increment. I deliberately did not run `check`/`run`/`rerun` since they
resolve the runner at the live-lane absolute path; the static digest mismatch
already substantiates the DRIFT claim.

**Section 18 (`## Pin disposition and provenance correction — round 13`,
instruction → executed-ok).** Both named commands ran under the collector:
`pin-disposition.py` emitted `pin-disposition-v1` JSON, exit 0, with the
`not_compared` list and `result_reuse=not_established` the section describes;
on my symlinked-mirror root it honestly reported `unavailable/repo_symlink`
for all six legs rather than silently borrowing (a documented verdict-map
outcome). `witness-metadata.py --check --companion …` printed
`WITNESS_METADATA: metadata_consistent reason=ok exit=0` — matching the
recorded `WITNESS_CHECK: CLEAN` expectation. Step-4 claims verified byte-for-
byte: canonical `summary.json` and the rerun summary both still carry
`declaration.kind: null`; the companion covers the canonical null and marks
the rerun null `named-residual-uncorrected`; the normalized kind is the exact
non-blind string with the verbatim disclosure. Sources S003/S041/S047 and the
"outside routed" pointer (round-12 lesson, Routed defects item 3, which names
the `declaration.kind=null` defect) all check out.

**Section 19 (`### Round-13 gate/probe registry`, record → verified-record).**
`pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)` exit 0, covering
exit-0 observation cases and exit-2 invalid-input cases exactly as the verdict
map says. `witness-metadata.py --selftest` → `SELFTEST: PASS 39/39` exit 0,
covering `metadata_consistent`/0, `metadata_inconsistent`/1,
`snapshot_tampered`/`input_unavailable`/2 — the row's map including usage under
argparse exit 2. `expected.json` exists and pins exactly the literal digests
the tool's `ALL_PINNED` verifies. The producer-SHA claim checks out: the
historical `summary.json` records producer `249d9dcd…` while the repaired tool
at this revision hashes `60575e62…`. SOURCES.md S048 text matches the section's
"item 4 is prioritisation, not a reuse skip" and "no test-versus-mutation
pronoun" wording.

COLDREAD ColdB06: verified-record, executed-ok, verified-record
