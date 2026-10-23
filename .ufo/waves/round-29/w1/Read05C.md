# Read05C — cold read of SKILL.md "## Pin disposition and provenance correction — round 13" (start 1517)

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "Read05C",
  "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6",
  "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [
    {
      "start": 1517,
      "heading": "## Pin disposition and provenance correction — round 13",
      "class": "instruction",
      "verdict": "executed-ok",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "python3 tools/pin-disposition.py --selftest",
        "python3 tools/witness-metadata.py --selftest",
        "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin",
        "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
        "python3 tools/bash-witness-study.py selftest"
      ],
      "opened": [
        "corpus/SOURCES.md",
        "corpus/knowledge/incremental-pin-disposition.md",
        "corpus/lessons/round-12-verifier-spotcheck.md",
        "tools/pin-disposition.py",
        "tools/witness-metadata.py",
        "tools/bash-witness-study.py",
        "tools/trace-inputs.py",
        "tools/mutate-and-run.sh",
        ".ufo/evidence/round-13/pin-manifest.json",
        ".ufo/evidence/round-13/pin-dispositions.json",
        ".ufo/evidence/round-13/expected.json",
        ".ufo/evidence/round-13/witness-metadata.json",
        ".ufo/evidence/round-13/witness-metadata-old-null.json",
        ".ufo/evidence/round-13/producer-oracle.py",
        ".ufo/evidence/round-13/producer-oracle-repair.json",
        ".ufo/evidence/round-12/BashWitness/summary.json",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json",
        ".ufo/evidence/round-12/BashWitness/declaration.json",
        ".ufo/evidence/round-12/BashWitness/declared.tsv"
      ],
      "inputs": {
        "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
        "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
        "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30",
        "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
        "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
        "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
        "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
        "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
        ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
        ".ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
        ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
        ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
        ".ufo/evidence/round-13/witness-metadata-old-null.json": "28067a1cb76b14677a26d86dadad8699177cf7eb1212140f3f06e9537a0b11c3",
        ".ufo/evidence/round-13/producer-oracle.py": "d5ae0bd4d4f75a461e7105b63eb737d249c3d09ffc15a3bfeb7aecea21ccd38b",
        ".ufo/evidence/round-13/producer-oracle-repair.json": "df83a72994a93cd8d38c5c228ed85f2ed6d978ebb86a7fb260db51b34dfbef8d",
        ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
        ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
        ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
        ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3"
      },
      "external_inputs": {
        "tameshi-shokunin@4eb4cf319c0eddd4ef0c6d1d4d11e51e0d4ee307:tools/mutate-and-run.sh": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
        "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
        "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "0f9c5a4c361316e111d0b2636780da5b8d848ccaa5c41507e8f8357ab6090075",
        "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
        "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"
      },
      "traces": [
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05C-1.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05C-2.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05C-3.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05C-4.json",
        "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05C-5.json"
      ]
    }
  ]
}
```

What I checked, in plain English:

- Section bounds: the heading at 1517 is exactly `## Pin disposition and provenance correction — round 13` (em dash); the next `#`/`##`/`###` heading outside fences is `### Round-13 gate/probe registry` at line 1548, so my span is 1517–1547 (Sources line, the five-row disposition table, and recipe steps 1–5). The registry subsection is a different seat's span; I verified its content informally anyway where it overlapped my claims, and everything I looked at held, but it is not part of this verdict.
- Class: instruction — recipe step 2 and 3 tell a reader to run `tools/pin-disposition.py` and `tools/witness-metadata.py --check`. Both ran as written under `tools/trace-inputs.py` (receipts 3 and 4, rev 9f3084bc…, exit 0). No live-lane reads in any receipt; the probe opened only the six sibling leg worktree files plus git metadata (recorded in `external`), matching the section's claim that it "observes only hashes and git metadata" and "executes no sibling gate" — every subprocess call in the tool is a read-only git plumbing command run with `GIT_OPTIONAL_LOCKS=0`.
- Probe output matches the table's contract: 6 legs, `result_reuse: not_established` on every row, `not_compared` carrying mode/exec-bit, runner/spec, suite command, toolchain, environment, dependencies, fixtures, timeouts — covering the "mode, dependencies, environment, runner/spec and invocation identity remain unmeasured" limit. The run today observed unchanged=1/changed=5; the committed `.ufo/evidence/round-13/pin-dispositions.json` records unchanged=3/changed=3 at 2026-10-20T04:59:26Z, matching `expected.json`'s `pin_live` values — the difference is exactly the "dated reading" the section warns about, and the one leg with all three identities agreeing (bash-checklist-run) still reads `unchanged` + `not_established`, confirming row 4's decision.
- Witness gate: `--check` on the companion prints `metadata_consistent reason=ok exit=0`, checking exactly `inputs=summary,declaration,declared,rerun_summary`. The companion's `covered_null_observations` contains only the canonical summary's `declaration.kind: null`; the rerun summary's null sits in `uncovered_null_observations` with `named-residual-uncorrected` — verifying step 4's "companion normalizes the canonical summary only; the rerun null is explicitly outside its normalized scope". Both frozen summaries still carry `kind: null` in their bytes; the companion records `frozen_bytes_rewritten: false`, `prior_exposure: true`, `blind: false`, and the disclosure verbatim — verifying "retain original bytes… preserve the exact non-blind kind and exposure disclosure; no retroactive preregistration".
- The historical summary's producer SHA `249d9dcd…` matches the companion's recorded producer identity and differs from both current `tools/bash-witness-study.py` (`60575e62…`) and the round-13-era pin (`49e9e5e2…`), confirming it "names the producer that actually ran, not the repaired current producer". The repaired producer's selftest ran 51/51 including `summary preserves top-level exposed declaration kind` (`tools/bash-witness-study.py:1680`), confirming step 4's regression-assertion claim.
- Sources line verifies: `corpus/SOURCES.md` holds S003 (StrykerJS incremental, "mined") and S041–S048 PIT rows; S047 is marked as superseding S041 with the original row retained (S041 row present; note at SOURCES.md:254); `corpus/knowledge/incremental-pin-disposition.md` exists and quotes the PIT items verbatim including "With the exception of 4), all these optimisations introduce a degree of potential error"; `corpus/lessons/round-12-verifier-spotcheck.md` "Routed defects" item 3 (line 146) is exactly the mandated repair shape this section performs; `.ufo/evidence/round-13/` holds the runtime receipts.
- Selftests (registry rows adjacent to the section, run under receipts 1–2): `pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`; `witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, including `old-null-red` → `metadata_inconsistent/normalized_kind_null/1` which independently exercises the old-null companion rejection in `witness-metadata-old-null.json`.
- `tools/mutate-and-run.sh` has drifted since round 13 (`fb91ef76…` now vs pinned `75ed934d…`, which is still the blob at pinned rev 4eb4cf319c… — verified by `git show`; recorded in `external_inputs`). The manifest's `derived_from` records the pinned hash and the knowledge file cites lines via `@ 4eb4cf3`, so the provenance claims remain internally consistent; the section itself makes no claim that the runner file is current. `expected.json`'s frozen selftest counts (18/18, 41/41) predate later test additions (19/19, 51/51 today) — dated receipts, not contradictions.

No installs needed (python3/git/strace already present). No blocking or minor gaps found; the section's commands run as written and its record claims check out against the cited artifacts at 9f3084bc.

COLDREAD Read05C: executed-ok
