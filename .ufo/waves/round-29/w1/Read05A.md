# Read05A — cold read of SKILL.md "## Pin disposition and provenance correction — round 13" (lines 1517–1562) @ 9f3084bc60ad56aac01e4556ef4c7653df2f65e5

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read05A", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 1517, "heading": "## Pin disposition and provenance correction — round 13", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": [], "commands_executed": [
      "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/incremental-pin-disposition.md corpus/lessons/round-12-verifier-spotcheck.md corpus/SOURCES.md",
      "python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin",
      "python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json",
      "python3 tools/pin-disposition.py --selftest",
      "python3 tools/witness-metadata.py --selftest"],
    "opened": ["SKILL.md", "corpus/SOURCES.md", "corpus/knowledge/incremental-pin-disposition.md", "corpus/lessons/round-12-verifier-spotcheck.md", "tools/pin-disposition.py", "tools/witness-metadata.py", "tools/trace-inputs.py", "tools/bash-witness-study.py", ".ufo/evidence/round-13/pin-manifest.json", ".ufo/evidence/round-13/witness-metadata.json", ".ufo/evidence/round-13/expected.json", ".ufo/evidence/round-13/pin-dispositions.json", ".ufo/evidence/round-12/BashWitness/summary.json", ".ufo/evidence/round-12/BashWitness/declaration.json", ".ufo/evidence/round-12/BashWitness/declared.tsv", ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json", ".ufo/waves/round-26/w1/ColdreadPilot.md"],
    "inputs": {
      "corpus/SOURCES.md": "804f0b4369e87fa87a45f194e8cbb315d7ea7af56957fd4c26775eddd3751dca",
      "corpus/knowledge/incremental-pin-disposition.md": "0cc87300978412e774c8768936dbbac08fe90581da762bfd5a8f20fbd6fcf0b9",
      "corpus/lessons/round-12-verifier-spotcheck.md": "6ec29ffdf3bbe2f5bbcda3405a6e0ba51c2f5d02467c681d7c892edb3feafe30",
      "tools/pin-disposition.py": "331529eadafe9138c88c1fe09666c9401d28c166f16bc92ecc092fc4d92c3a4c",
      "tools/witness-metadata.py": "df3390682a04ccbb2469060c3deab924f9d8df72ce1a5b195d3618ce6cc0bed4",
      "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
      "tools/bash-witness-study.py": "60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9",
      ".ufo/evidence/round-13/pin-manifest.json": "64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6",
      ".ufo/evidence/round-13/witness-metadata.json": "463282270a04bd46f4a0522ff6a349b77d268ede47725c4e1c52ca892210bd8d",
      ".ufo/evidence/round-13/expected.json": "a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336",
      ".ufo/evidence/round-13/pin-dispositions.json": "210850f51040fd11d5c63711417f72fb816171a55a23d82f52f7969be711a637",
      ".ufo/evidence/round-12/BashWitness/summary.json": "acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9",
      ".ufo/evidence/round-12/BashWitness/declaration.json": "e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901",
      ".ufo/evidence/round-12/BashWitness/declared.tsv": "0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3",
      ".ufo/evidence/round-12/BashWitness/rerun-20261020T035435Z/summary.json": "6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0",
      ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7"},
    "external_inputs": {
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf",
      "/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/claims-check.mjs": "0b2d0d24e4ee83c8934a9e9390aeee9105a8e3f9b203997c7a68b7b5b74de487",
      "/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs": "0f9c5a4c361316e111d0b2636780da5b8d848ccaa5c41507e8f8357ab6090075",
      "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh": "050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1",
      "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh": "d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05A-1.json",
               "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05A-2.json",
               "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05A-3.json",
               "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05A-4.json",
               "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read05A-5.json"]}]}
```

What I checked, in a fleet-mirror clone (`/tmp/Read05A-M5dZ/fleet`) detached at `9f3084bc` (SKILL.md sha256 `c46ec02e…36d6`, matches the named pin):

- **Class.** The section is an instruction: its "Recipe from this lane root" names concrete commands plus read-order steps, so `executed-ok` is the right credit.
- **Step 2 command ran as written.** `pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` exited 0 and emitted six leg rows: all `pinned: verified`, `worktree`/`content_status` = `changed` ×5 and `unchanged` ×1 (bash-checklist-run), every row `result_reuse=not_established`, each `head.commit`/`head.branch` populated and `observed_at` stamped — matching "observes only hashes and git metadata" and "retain stdout with its sibling branch-tip commits". The trace's external bucket contains exactly the six sibling target files hashed; `live_lane_reads` empty; it executed no sibling gate.
- **Step 3 command ran as written.** `witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` printed `WITNESS_METADATA: metadata_consistent reason=ok exit=0 … inputs=summary,declaration,declared,rerun_summary`, matching the registry's "0 metadata_consistent/clean" map and "digest-anchored frozen sources" wording.
- **Step 1 (read order).** Read `corpus/knowledge/incremental-pin-disposition.md` (source-backed scope, §4 leg table, §6 invariants) and observed `not_compared` = 8 entries (mode/exec-bit, runner/spec, suite command, toolchain, env vars, dependencies, fixtures, timeouts) — matching the first table row's "Mode, dependencies, environment, runner/spec and invocation identity remain unmeasured".
- **Step 4 claims verified against the frozen bytes.** Both `summary.json` and `rerun-20261020T035435Z/summary.json` retain `"kind": null` in their nested `declaration` blocks; the companion's `scope.covered_null_observations` covers only the canonical summary while `uncovered_null_observations` names the rerun null as `named-residual-uncorrected`; `declaration.kind` is the explicit top-level "declared-witness mapping (not a blind preregistration)" and `frozen_bytes_rewritten=false`. The historical summary's producer sha `249d9dcd…` differs from the current `tools/bash-witness-study.py` (`60575e62…`), consistent with "names the producer that actually ran, not the repaired current producer". `expected.json` pins the same frozen digests and contains the selftest assertion "summary preserves top-level exposed declaration kind"; the producer emits `# kind:` (line 377) so the nesting repair is present for future runs.
- **Registry rows.** Both selftests ran under the collector: `SELFTEST: PASS (19/19)` (pin-disposition, exit 0) and `SELFTEST: PASS 39/39` (witness-metadata, exit 0) — consistent with the "selftest 1 failed" / isolated-temp-repos verdict maps.
- **Source row claims.** SOURCES.md carries S003, S041 (retained), S047 (precision correction, "supersedes S041"), and S048 ("supersedes S047 — item 4 is prioritisation rather than a reuse skip"), matching the section's S047/S048 wording; `corpus/lessons/round-12-verifier-spotcheck.md` Routed defects item 3 is the named `declaration.kind=null` provenance repair this section answers, matching "outside routed … item 3".
- **Historical receipt.** `.ufo/evidence/round-13/pin-dispositions.json` exists with schema `pin-disposition-v1`, six legs, `observed_at` and the same 8-item `not_compared` — consistent with the knowledge note §6 invariants.

Minor: the recipe's `--root` is an absolute live-fleet path by design (the probe's whole job is reading the live fleet); the command was run verbatim in the mirror clone with `cwd` at the clone's lane root. One direct (untraced) repeat of the pin-disposition argv was used to capture the full JSON for verification; the same argv is already receipted in `Read05A-2.json`. No installs or tooling changes; no writes outside the report and the five trace receipts.

COLDREAD Read05A: executed-ok
